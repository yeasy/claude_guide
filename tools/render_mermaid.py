#!/usr/bin/env python3
"""Render every published Mermaid block to SVG; strict and source-safe by default."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


STANDARD_CHROME_PATHS = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
)
SAFETY_MESSAGE = "must be an independent directory outside protected source trees"


def paths_overlap(left: Path, right: Path) -> bool:
    return left == right or left in right.parents or right in left.parents


def validate_output_directory(book_dir: str, svg_out: str) -> tuple[Path, Path]:
    book = Path(book_dir).expanduser().resolve()
    output = Path(svg_out).expanduser().resolve()
    repository = Path(__file__).resolve().parents[1]
    if (
        output in {Path(output.anchor).resolve(), Path.home().resolve(), Path.cwd().resolve()}
        or paths_overlap(output, book)
        or paths_overlap(output, repository)
    ):
        raise ValueError(f"--svg-out {output} {SAFETY_MESSAGE}")
    return book, output


def clean_generated_files(output: Path) -> None:
    generated = re.compile(r"^(?:d-\d+|_c(?:-\d+)?)\.svg$")
    for entry in output.iterdir():
        if entry.name in {"_chunk.md", "_pptr.json", "_rc.json"} or generated.fullmatch(entry.name):
            if entry.is_file() or entry.is_symlink():
                entry.unlink()


def find_chrome() -> str | None:
    configured = os.environ.get("CHROME_BIN")
    candidates = [configured] if configured else [
        *(shutil.which(name) for name in ("google-chrome-stable", "google-chrome", "chromium-browser", "chromium", "chrome")),
        *STANDARD_CHROME_PATHS,
    ]
    return next((str(Path(path).resolve()) for path in candidates if path and Path(path).is_file()), None)


def published_sources(book: Path) -> list[str]:
    order: list[Path] = []
    seen: set[Path] = set()
    for line in (book / "SUMMARY.md").read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\s*[-*]\s+\[.*?\]\(([^)]+?)\)", line)
        if not match:
            continue
        relative = match.group(1).split("#", 1)[0].strip()
        path = (book / relative).resolve()
        if relative.endswith(".md") and path.is_file() and path not in seen:
            if book not in path.parents:
                raise ValueError(f"SUMMARY entry escapes book directory: {relative}")
            seen.add(path)
            order.append(path)
    sources: list[str] = []
    for path in order:
        text = path.read_text(encoding="utf-8")
        sources.extend(re.findall(r"```mermaid[ \t]*\n(.*?)\n[ \t]*```", text, re.DOTALL))
    return sources


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book-dir", default=".")
    parser.add_argument("--svg-out", required=True)
    parser.add_argument("--chunk", type=int, default=25)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--strict", dest="strict", action="store_true", default=True)
    mode.add_argument("--allow-fallback", dest="strict", action="store_false")
    args = parser.parse_args()
    if args.chunk <= 0:
        parser.error("--chunk must be positive")
    try:
        book, output = validate_output_directory(args.book_dir, args.svg_out)
        sources = published_sources(book)
    except (OSError, ValueError) as error:
        print(f"Mermaid rendering failed: {error}", file=sys.stderr)
        return 2
    output.mkdir(parents=True, exist_ok=True)
    clean_generated_files(output)
    count = len(sources)
    print(f"mermaid diagrams found: {count}")
    if count == 0:
        return 0

    chrome = find_chrome()
    mmdc = shutil.which("mmdc")
    missing_tool = "no Chrome executable found" if not chrome else "mmdc is not on PATH" if not mmdc else None
    if missing_tool:
        if args.strict:
            print(f"Mermaid rendering failed: {missing_tool}", file=sys.stderr)
            return 1
        print(f"WARNING: {missing_tool} -> diagrams fall back to source")
        return 0

    print(f"using Chrome: {chrome}")
    pptr, config = output / "_pptr.json", output / "_rc.json"
    pptr.write_text(json.dumps({"executablePath": chrome, "args": ["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]}), encoding="utf-8")
    config.write_text(json.dumps({"theme": "default"}), encoding="utf-8")

    def done() -> int:
        return sum((output / f"d-{index + 1}.svg").is_file() for index in range(count))

    def render(indices: list[int]) -> None:
        chunk_file = output / "_chunk.md"
        chunk_file.write_text("\n".join(f"```mermaid\n{sources[index]}\n```\n" for index in indices), encoding="utf-8")
        for stale in output.glob("_c*.svg"):
            stale.unlink()
        result = subprocess.run([mmdc, "-i", str(chunk_file), "-o", str(output / "_c.svg"), "-p", str(pptr), "-c", str(config), "-b", "transparent"], capture_output=True, text=True, check=False)
        if result.returncode:
            print((result.stderr or result.stdout).strip(), file=sys.stderr)
        for position, index in enumerate(indices, 1):
            source = output / f"_c-{position}.svg"
            if len(indices) == 1 and not source.is_file():
                source = output / "_c.svg"
            if source.is_file() and source.stat().st_size:
                source.replace(output / f"d-{index + 1}.svg")
        for stale in output.glob("_c*.svg"):
            stale.unlink()

    for start in range(0, count, args.chunk):
        render(list(range(start, min(start + args.chunk, count))))
        print(f"  rendered: {done()}/{count}", flush=True)
    for _ in range(4):
        missing = [index for index in range(count) if not (output / f"d-{index + 1}.svg").is_file()]
        if not missing:
            break
        for start in range(0, len(missing), 8):
            render(missing[start : start + 8])
    for temporary in (pptr, config, output / "_chunk.md"):
        temporary.unlink(missing_ok=True)
    missing = [index + 1 for index in range(count) if not (output / f"d-{index + 1}.svg").is_file()]
    print(f"RENDERED {done()}/{count} diagrams")
    if args.strict and missing:
        print(f"Mermaid rendering failed for diagrams: {missing}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
