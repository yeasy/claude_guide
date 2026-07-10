#!/usr/bin/env python3
"""Verify PDF/HTML title, complete Mermaid rendering, and SHA-256 integrity."""

from __future__ import annotations

import argparse
import hashlib
import html
import re
import shutil
import subprocess
import sys
from pathlib import Path


class ArtifactVerificationError(ValueError):
    pass


def require_file(path: Path) -> None:
    if not path.is_file() or path.stat().st_size == 0:
        raise ArtifactVerificationError(f"{path} is missing or empty")


def normalized(value: str) -> str:
    return " ".join(html.unescape(value).split())


def command_output(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        raise ArtifactVerificationError((result.stderr or result.stdout).strip())
    return result.stdout


def verify_pdf(path: Path, title: str) -> None:
    require_file(path)
    if path.read_bytes()[:5] != b"%PDF-":
        raise ArtifactVerificationError(f"{path} has no PDF signature")
    if not shutil.which("pdfinfo") or not shutil.which("pdftotext"):
        raise ArtifactVerificationError("pdfinfo and pdftotext are required")
    metadata = command_output(["pdfinfo", str(path)])
    match = re.search(r"(?m)^Title:\s*(.*)$", metadata)
    if match and normalized(match.group(1)) == normalized(title):
        return
    cover = command_output(["pdftotext", "-f", "1", "-l", "2", str(path), "-"])
    if normalized(title) not in normalized(cover):
        raise ArtifactVerificationError(f"{path} title mismatch")


def summary_mermaid_count(root: Path) -> int:
    root = root.resolve()
    summary = root / "SUMMARY.md"
    require_file(summary)
    seen: set[Path] = set()
    total = 0
    for match in re.finditer(r"(?m)^\s*[-*]\s+\[[^]]*\]\(([^)]+)\)", summary.read_text(encoding="utf-8")):
        relative = match.group(1).split("#", 1)[0].strip()
        if not relative.endswith(".md"):
            continue
        path = (root / relative).resolve()
        if root not in path.parents:
            raise ArtifactVerificationError(f"SUMMARY escapes source root: {relative}")
        if path in seen:
            continue
        require_file(path)
        seen.add(path)
        total += len(re.findall(r"(?m)^\s*```mermaid\s*$", path.read_text(encoding="utf-8")))
    return total


def verify_html(path: Path, title: str, expected_mermaid_count: int) -> None:
    require_file(path)
    text = path.read_text(encoding="utf-8")
    match = re.search(r"<title(?:\s[^>]*)?>(.*?)</title>", text, re.I | re.S)
    if not match or normalized(match.group(1)) != normalized(title):
        raise ArtifactVerificationError(f"{path} title mismatch")
    placeholder = re.search(r"MERMAIDZZ\d+ZZ|PGBKZZ|<pre\b[^>]*\bdiagram-fallback\b", text, re.I)
    if placeholder:
        raise ArtifactVerificationError(f"{path} has unresolved placeholder")
    figures = re.findall(r"<figure\b[^>]*\bclass=[\"'][^\"']*\bdiagram\b[^\"']*[\"'][^>]*>.*?</figure>", text, re.I | re.S)
    if len(figures) != expected_mermaid_count or any("<svg" not in item.lower() for item in figures):
        raise ArtifactVerificationError(f"{path} Mermaid mismatch: expected {expected_mermaid_count}, got {len(figures)}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_checksums(paths: list[Path], manifest: Path) -> None:
    manifest.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for path in sorted(paths, key=lambda item: item.name):
        require_file(path)
        if path.parent.resolve() != manifest.parent.resolve():
            raise ArtifactVerificationError("artifacts must be beside SHA256SUMS")
        lines.append(f"{sha256(path)}  {path.name}\n")
    manifest.write_text("".join(lines), encoding="utf-8")


def verify_checksums(manifest: Path) -> None:
    require_file(manifest)
    names: set[str] = set()
    for number, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\]+)", line)
        if not match or match.group(2) in names or match.group(2) == manifest.name:
            raise ArtifactVerificationError(f"{manifest}:{number}: malformed entry")
        expected, name = match.groups()
        names.add(name)
        path = manifest.parent / name
        require_file(path)
        if sha256(path) != expected:
            raise ArtifactVerificationError(f"checksum mismatch for {path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--html", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--checksums", type=Path, required=True)
    args = parser.parse_args()
    try:
        verify_pdf(args.pdf, args.title)
        count = summary_mermaid_count(args.source_root)
        verify_html(args.html, args.title, count)
        write_checksums([args.pdf, args.html], args.checksums)
        verify_checksums(args.checksums)
    except ArtifactVerificationError as error:
        print(f"artifact verification failed: {error}", file=sys.stderr)
        return 1
    print(f"verified artifacts: {args.pdf}, {args.html}; Mermaid={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
