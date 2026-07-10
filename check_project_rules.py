#!/usr/bin/env python3
"""Lightweight Markdown project checks for book repositories."""

from __future__ import annotations

import re
import sys
from collections.abc import Mapping
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parent
SKIP_DIRS = {
    ".agent",
    ".git",
    ".mdpress",
    "_book",
    "_site",
    "dist",
    "node_modules",
}
LINK_RE = re.compile(r"(!?)\[[^\]]*\]\(([^)\s]+(?:\s+\"[^\"]*\")?)\)")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
VOLATILE_META_RE = re.compile(
    r"`verified_at`:\s*(\d{4}-\d{2}-\d{2})\s*·\s*"
    r"`expires_at`:\s*(\d{4}-\d{2}-\d{2})\s*·\s*"
    r"`ttl_days`:\s*(\d+)"
)
VOLATILE_STATUS_RE = re.compile(
    r"<!--\s*volatile-status:\s*id=([^\s]+)\s+status=([^\s]+)\s*-->"
)
SONNET_46_RE = re.compile(r"(?:Claude\s+)?Sonnet 4\.6|claude-sonnet-4-6")


def _sonnet_46_entries(
    path: str,
    lines: tuple[int, ...],
    reason: str,
) -> dict[tuple[str, int], str]:
    """Expand a reviewed context into explicit file-and-line approvals."""

    return {(path, line): reason for line in lines}


SONNET_46_ALLOWLIST: dict[tuple[str, int], str] = {
    **_sonnet_46_entries(
        "01_intro/1.1_born.md",
        (76,),
        "Historical release timeline entry for the February 2026 launch.",
    ),
    **_sonnet_46_entries(
        "01_intro/1.2_model_family.md",
        (75, 97, 99, 101, 109, 174),
        "Historical model-family evolution and the 4.5-to-4.6 comparison.",
    ),
    **_sonnet_46_entries(
        "01_intro/1.2_model_family.md",
        (95, 152),
        "Sonnet 5 migration target and legacy thinking compatibility reference.",
    ),
    **_sonnet_46_entries(
        "01_intro/1.3_capabilities.md",
        (12,),
        "Explicit migration-period context-window compatibility baseline.",
    ),
    **_sonnet_46_entries(
        "01_intro/1.4_model_selection.md",
        (40, 41, 74, 83, 114, 128),
        "Explicit Sonnet 5 migration, token recount, and rollback guidance.",
    ),
    **_sonnet_46_entries(
        "02_prompt/2.1_basics.md",
        (39,),
        "Explicit migration-period context-window compatibility baseline.",
    ),
    **_sonnet_46_entries(
        "02_prompt/2.5_cot.md",
        (110,),
        "Legacy thinking-mode compatibility reference for migration only.",
    ),
    **_sonnet_46_entries(
        "02_prompt/2.6_format.md",
        (10,),
        "Compatibility warning that documents the legacy prefill boundary.",
    ),
    **_sonnet_46_entries(
        "02_prompt/2.7_optimization.md",
        (98,),
        "Regression-testing example for a Sonnet 4.6-to-5 migration.",
    ),
    **_sonnet_46_entries(
        "03_tools/3.5_programmatic.md",
        (17, 21),
        "Model table marks Sonnet 5 as the target and 4.6 as legacy-only.",
    ),
    **_sonnet_46_entries(
        "05_computer_use/5.2_loop.md",
        (48,),
        "Legacy Computer Use tool-version compatibility baseline.",
    ),
    **_sonnet_46_entries(
        "08_agent/8.4_extended_thinking.md",
        (12, 37, 50),
        "Legacy thinking syntax retained only for migration compatibility.",
    ),
    **_sonnet_46_entries(
        "08_agent/summary.md",
        (9,),
        "Summary explicitly routes new work to Sonnet 5 and legacy work through migration.",
    ),
    **_sonnet_46_entries(
        "10_optimization/10.2_caching.md",
        (251,),
        "Legacy model retained only as a cache-threshold compatibility baseline.",
    ),
    **_sonnet_46_entries(
        "10_optimization/10.3_context_mgmt.md",
        (3,),
        "Legacy model retained only as a context-window compatibility baseline.",
    ),
    **_sonnet_46_entries(
        "12_appendix/12.3_glossary.md",
        (20, 55),
        "Glossary records legacy context-window and prefill compatibility boundaries.",
    ),
    **_sonnet_46_entries(
        "12_appendix/12.5_pricing.md",
        (27,),
        "Legacy price row is explicitly limited to migration, regression, and rollback.",
    ),
    **_sonnet_46_entries(
        "12_appendix/12.6_model_comparison.md",
        (34, 54, 68, 70, 89, 109, 140, 153, 163, 172, 197, 211, 434, 633, 640, 661, 817, 823),
        "Historical comparison snapshot; the chapter notice forbids production routing from it.",
    ),
    **_sonnet_46_entries(
        "12_appendix/12.6_model_comparison.md",
        (9, 315, 327, 402, 432, 448, 545, 826, 831, 837),
        "Explicit Sonnet 5 migration, token recount, legacy baseline, or rollback guidance.",
    ),
    **_sonnet_46_entries(
        "12_appendix/12.7_volatile_facts.md",
        (18,),
        "Volatile-facts ledger records required changes for a 4.6-to-5 migration.",
    ),
    **_sonnet_46_entries(
        "13_advanced/13.1_claude5_preview.md",
        (17, 52, 55, 57, 67, 89),
        "Explicit Sonnet 5 migration checklist and legacy compatibility reference.",
    ),
    **_sonnet_46_entries(
        "13_advanced/13.2_infinite_chats.md",
        (956,),
        "Legacy model retained only as a context-window compatibility baseline.",
    ),
    **_sonnet_46_entries(
        "13_advanced/summary.md",
        (11, 22, 166, 174, 177),
        "Summary explicitly limits 4.6 to migration, compatibility, and rollback.",
    ),
}


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return sorted(files)


def strip_fenced_blocks(text: str) -> str:
    output: list[str] = []
    in_fence = False
    fence_marker = ""
    fence_len = 0
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)
            char = marker[0]
            length = len(marker)
            if not in_fence:
                in_fence = True
                fence_marker = char
                fence_len = length
            elif char == fence_marker and length >= fence_len:
                in_fence = False
            output.append("")
            continue
        output.append("" if in_fence else line)
    return "\n".join(output)


def check_fences(path: Path, text: str) -> list[str]:
    issues: list[str] = []
    stack: list[tuple[str, int, int]] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        match = FENCE_RE.match(line)
        if not match:
            continue
        marker = match.group(1)
        char = marker[0]
        length = len(marker)
        if not stack:
            stack.append((char, length, line_no))
            continue
        open_char, open_len, _ = stack[-1]
        if char == open_char and length >= open_len:
            stack.pop()
        else:
            stack.append((char, length, line_no))
    for _, _, line_no in stack:
        issues.append(f"{path.relative_to(ROOT)}:{line_no}: unclosed fenced code block")
    return issues


def is_local_target(target: str) -> bool:
    parsed = urlparse(target)
    return not parsed.scheme and not parsed.netloc and not target.startswith("#")


def normalize_target(raw_target: str) -> str:
    target = raw_target.strip()
    if " " in target and target.count('"') >= 2:
        target = target.split(" ", 1)[0]
    return unquote(target.split("#", 1)[0])


def check_links(path: Path, text: str) -> list[str]:
    issues: list[str] = []
    body = strip_fenced_blocks(text)
    for match in LINK_RE.finditer(body):
        raw_target = match.group(2).strip()
        target = normalize_target(raw_target)
        if not target or not is_local_target(raw_target):
            continue
        target_path = (path.parent / target).resolve()
        try:
            target_path.relative_to(ROOT)
        except ValueError:
            continue
        if not target_path.exists():
            line_no = body[: match.start()].count("\n") + 1
            issues.append(
                f"{path.relative_to(ROOT)}:{line_no}: missing local link target: {raw_target}"
            )
    return issues


def check_summary_links() -> list[str]:
    summary = ROOT / "SUMMARY.md"
    if not summary.exists():
        return []
    return check_links(summary, summary.read_text(encoding="utf-8", errors="ignore"))


def check_volatile_facts(
    path: Path = ROOT / "12_appendix" / "12.7_volatile_facts.md",
    today: date | None = None,
) -> list[str]:
    """Reject stale, future-dated, or unresolved fast-changing facts."""

    name = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
    if not path.is_file():
        return [f"{name}: volatile facts ledger is missing"]
    issues: list[str] = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    metadata = VOLATILE_META_RE.search(text)
    if metadata is None:
        issues.append(f"{name}: volatile facts metadata is missing")
    else:
        try:
            verified_at = date.fromisoformat(metadata.group(1))
            expires_at = date.fromisoformat(metadata.group(2))
        except ValueError as error:
            issues.append(f"{name}: invalid volatile facts date: {error}")
        else:
            current_date = today or date.today()
            ttl_days = int(metadata.group(3))
            if expires_at <= verified_at:
                issues.append(f"{name}: volatile facts expires_at must be after verified_at")
            if ttl_days != 30 or expires_at != verified_at + timedelta(days=30):
                issues.append(f"{name}: volatile facts TTL must describe exactly 30 days")
            if verified_at > current_date:
                issues.append(f"{name}: volatile facts verified_at is in the future")
            if current_date > expires_at:
                issues.append(f"{name}: volatile facts ledger expired on {expires_at}")

    statuses = VOLATILE_STATUS_RE.findall(text)
    if not statuses:
        issues.append(f"{name}: volatile facts status metadata is missing")
    for fact_id, status in statuses:
        if status == "open-conflict":
            issues.append(f"{name}: {fact_id} has an unresolved conflict")
        elif status not in {"current", "resolved-conflict"}:
            issues.append(f"{name}: {fact_id} has unknown status {status!r}")
    return issues


def check_sonnet_46_usage(
    root: Path = ROOT,
    allowlist: Mapping[tuple[str, int], str] | None = None,
) -> list[str]:
    """Allow Sonnet 4.6 only in exact, reasoned legacy or migration contexts."""

    root = root.resolve()
    approved = SONNET_46_ALLOWLIST if allowlist is None else allowlist
    files = [
        path
        for path in root.rglob("*.md")
        if not any(part in SKIP_DIRS for part in path.relative_to(root).parts)
    ]
    examples = root / "examples"
    if examples.is_dir():
        files.extend(examples.rglob("*.py"))

    issues: list[str] = []
    observed: set[tuple[str, int]] = set()
    for path in sorted(set(files)):
        relative = path.relative_to(root).as_posix()
        for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if not SONNET_46_RE.search(line):
                continue
            key = (relative, line_no)
            observed.add(key)
            if key not in approved:
                issues.append(f"{relative}:{line_no}: Sonnet 4.6 use is not explicitly allowlisted")

    for key, reason in approved.items():
        relative, line_no = key
        if not reason.strip():
            issues.append(f"{relative}:{line_no}: Sonnet 4.6 allowlist reason is empty")
        if key not in observed:
            issues.append(f"{relative}:{line_no}: Sonnet 4.6 allowlist entry no longer matches")
    return issues


def main() -> int:
    issues: list[str] = []
    files = iter_markdown_files()
    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        issues.extend(check_fences(path, text))
        issues.extend(check_links(path, text))
    issues.extend(check_summary_links())
    issues.extend(check_volatile_facts())
    issues.extend(check_sonnet_46_usage())

    if issues:
        print("\n".join(sorted(set(issues))))
        print(f"\n{len(set(issues))} issue(s) found across {len(files)} Markdown files.")
        return 1
    print(f"All {len(files)} Markdown files passed project checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
