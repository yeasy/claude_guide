from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
EXPECTED = ("ci.yaml", "preview-pdf.yml", "auto-release.yml", "dependabot-automerge.yml")
PUBLICATION_WORKFLOWS = ("ci.yaml", "preview-pdf.yml", "auto-release.yml")
FULL_SHA = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")
REPOSITORY = "owner/repo"
SHA = "a" * 40
STEPS = (
    "Synchronize mutable preview tag",
    "Create or update preview release",
    "Replace preview assets",
)


FAKE_GH = r'''#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
with open(os.environ["GH_LOG"], "a", encoding="utf-8") as stream:
    stream.write(json.dumps(args) + "\n")
scenario = os.environ["GH_SCENARIO"]
repo, sha = "owner/repo", "a" * 40
get_ref = ["api", "--include", "--method", "GET", f"repos/{repo}/git/ref/tags/preview-pdf"]
patch_ref = ["api", "--silent", "--method", "PATCH", f"repos/{repo}/git/refs/tags/preview-pdf", "--raw-field", f"sha={sha}", "--field", "force=true"]
post_ref = ["api", "--silent", "--method", "POST", f"repos/{repo}/git/refs", "--raw-field", "ref=refs/tags/preview-pdf", "--raw-field", f"sha={sha}"]
view = ["release", "view", "preview-pdf"]
edit = ["release", "edit", "preview-pdf", "--title", "Latest Preview Publications", "--notes-file", "dist/release-notes.md", "--prerelease"]
create = ["release", "create", "preview-pdf", "--title", "Latest Preview Publications", "--notes-file", "dist/release-notes.md", "--prerelease", "--latest=false", "--verify-tag"]
upload = ["release", "upload", "preview-pdf", "dist/claude_guide.pdf", "dist/claude_guide.html", "dist/SHA256SUMS", "--clobber"]
if os.environ.get("GH_REPO") != repo:
    raise SystemExit(2)
if args == get_ref:
    if scenario == "ref_404_exit2":
        print("HTTP/2.0 404 Not Found"); raise SystemExit(2)
    if scenario.startswith("ref_network"):
        print("network failure", file=sys.stderr); raise SystemExit(1)
    for code in ("401", "403", "404", "429", "503"):
        if scenario.startswith(f"ref_{code}"):
            print(f"HTTP/2.0 {code} Error"); print(code, file=sys.stderr); raise SystemExit(1)
    print("HTTP/2.0 200 OK"); raise SystemExit(0)
if args == view:
    if "release_missing_exit2" in scenario:
        print("release not found", file=sys.stderr); raise SystemExit(2)
    if "release_missing" in scenario:
        print("release not found", file=sys.stderr); raise SystemExit(1)
    if "release_network" in scenario:
        print("network failure", file=sys.stderr); raise SystemExit(1)
    for code in ("401", "403", "404", "429", "503"):
        if f"release_{code}" in scenario:
            print(code, file=sys.stderr); raise SystemExit(1)
    raise SystemExit(0)
if args in (patch_ref, post_ref, edit, create, upload):
    raise SystemExit(0)
print(f"unexpected argv: {args!r}", file=sys.stderr); raise SystemExit(2)
'''


def step_names(text: str) -> list[str]:
    publish = text.split("\n  publish:\n", 1)[1]
    return [
        match.group(1).strip()
        for match in re.finditer(r"(?m)^      - name:\s*(.+?)\s*$", publish)
        if match.group(1).strip() in STEPS
    ]


def step_script(text: str, name: str) -> str:
    marker = f"      - name: {name}\n"
    start = text.index(marker) + len(marker)
    run = text.index("        run: |\n", start) + len("        run: |\n")
    end = text.find("\n      - name:", run)
    return textwrap.dedent(text[run : end if end >= 0 else len(text)])


def job_text(text: str, name: str) -> str:
    marker = f"  {name}:\n"
    start = text.index(marker) + len(marker)
    next_job = re.search(r"(?m)^  [A-Za-z0-9_-]+:\n", text[start:])
    end = start + next_job.start() if next_job else len(text)
    return text[start:end]


class WorkflowSafetyTests(unittest.TestCase):
    def text(self, name: str) -> str:
        return (WORKFLOWS / name).read_text(encoding="utf-8")

    def test_actions_pinned_and_checkout_credentials_disabled(self):
        failures = []
        for name in EXPECTED:
            lines = self.text(name).splitlines()
            for number, line in enumerate(lines, 1):
                match = re.search(r"\buses:\s*([^\s#]+)(?:\s+#\s*(\S+))?", line)
                if match and (not FULL_SHA.fullmatch(match.group(1)) or not (match.group(2) or "").startswith("v")):
                    failures.append(f"{name}:{number}:{line.strip()}")
                if "uses: actions/checkout@" in line:
                    self.assertIn("persist-credentials: false", "\n".join(lines[number - 1 : number + 8]))
        self.assertEqual(failures, [])

    def test_permissions_integrity_html_and_provenance(self):
        for name in EXPECTED:
            self.assertIn("\npermissions: {}\n", self.text(name), name)
        for name in ("ci.yaml", "preview-pdf.yml", "auto-release.yml"):
            text = self.text(name)
            for marker in (
                "MDPRESS_SHA256",
                "PANDOC_SHA256",
                "sha256sum -c -",
                "npm ci --prefix tools/mermaid --ignore-scripts",
                "tools/render_mermaid.py",
                "--strict",
                "tools/build_html_reader.py",
                "tools/verify_artifacts.py",
                "SHA256SUMS",
                "if-no-files-found: error",
            ):
                self.assertIn(marker, text, f"{name}: {marker}")
            self.assertNotIn("continue-on-error: true", text)
        auto = self.text("auto-release.yml")
        self.assertIn("actions/attest-build-provenance@", auto)
        self.assertRegex(auto, r"(?s)subject-path:.*?\.pdf.*?\.html.*?SHA256SUMS")
        self.assertRegex(auto, r"(?s)files:.*?\.pdf.*?\.html.*?SHA256SUMS")
        self.assertIn("fail_on_unmatched_files: true", auto)

    def test_exact_example_dependencies_are_installed_in_read_only_build_jobs(self):
        install = "python3 -m pip install --disable-pip-version-check -r examples/requirements.txt"
        tests = "python3 -m unittest discover -s tests -p 'test_*.py' -v"
        for name in PUBLICATION_WORKFLOWS:
            text = self.text(name)
            build = job_text(text, "build")
            self.assertIn("permissions:\n      contents: read", build, name)
            self.assertIn(install, build, name)
            self.assertLess(build.index(install), build.index(tests), name)
            self.assertEqual(text.count(install), 1, name)

    def test_mermaid_lock_is_exact(self):
        package = json.loads((ROOT / "tools/mermaid/package.json").read_text())
        lock = json.loads((ROOT / "tools/mermaid/package-lock.json").read_text())
        self.assertEqual(package["dependencies"]["@mermaid-js/mermaid-cli"], "11.16.0")
        self.assertEqual(lock["packages"][""]["dependencies"]["@mermaid-js/mermaid-cli"], "11.16.0")

    def run_preview(self, scenario: str, *, repo: str = REPOSITORY, sha: str = SHA):
        text = self.text("preview-pdf.yml")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fake = root / "gh"
            fake.write_text(FAKE_GH, encoding="utf-8")
            fake.chmod(0o755)
            log = root / "log"
            env = os.environ.copy()
            env.update({"PATH": f"{root}{os.pathsep}{env['PATH']}", "GH_LOG": str(log), "GH_SCENARIO": scenario, "GH_REPO": repo, "GITHUB_SHA": sha, "GH_TOKEN": "test"})
            result = None
            for name in step_names(text):
                result = subprocess.run(["/bin/bash", "-c", step_script(text, name)], cwd=ROOT, env=env, text=True, capture_output=True, check=False)
                if result.returncode:
                    break
            commands = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
            return result, commands

    def test_preview_yaml_order_and_exact_argv(self):
        text = self.text("preview-pdf.yml")
        self.assertEqual(step_names(text), list(STEPS))
        swapped = text.replace(STEPS[0], "__A__", 1).replace(STEPS[1], STEPS[0], 1).replace("__A__", STEPS[1], 1)
        self.assertEqual(step_names(swapped), [STEPS[1], STEPS[0], STEPS[2]])
        success, commands = self.run_preview("ref_200_release_exists")
        self.assertEqual(success.returncode, 0, success.stderr)
        self.assertEqual([command[:3] for command in commands[:2]], [["api", "--include", "--method"], ["api", "--silent", "--method"]])
        self.assertEqual(commands[1][-4:], ["--raw-field", f"sha={SHA}", "--field", "force=true"])
        self.assertEqual(commands[-1][-4:], ["dist/claude_guide.pdf", "dist/claude_guide.html", "dist/SHA256SUMS", "--clobber"])

    def test_preview_creates_only_for_exact_not_found_and_fails_closed(self):
        created, commands = self.run_preview("ref_404_release_missing")
        self.assertEqual(created.returncode, 0, created.stderr)
        self.assertIn(["release", "create", "preview-pdf", "--title", "Latest Preview Publications", "--notes-file", "dist/release-notes.md", "--prerelease", "--latest=false", "--verify-tag"], commands)
        for scenario in ("ref_401", "ref_403", "ref_429", "ref_503", "ref_network", "ref_404_exit2"):
            result, commands = self.run_preview(scenario)
            self.assertNotEqual(result.returncode, 0, scenario)
            self.assertEqual(len(commands), 1, scenario)
        for scenario in ("ref_200_release_401", "ref_200_release_403", "ref_200_release_404", "ref_200_release_429", "ref_200_release_503", "ref_200_release_network", "ref_200_release_missing_exit2"):
            result, commands = self.run_preview(scenario)
            self.assertNotEqual(result.returncode, 0, scenario)
            self.assertEqual(commands[-1], ["release", "view", "preview-pdf"], scenario)

    def test_preview_rejects_invalid_inputs_before_gh(self):
        for repo, sha in (("owner/repo/extra", SHA), (REPOSITORY, "a" * 39)):
            result, commands = self.run_preview("ref_200_release_exists", repo=repo, sha=sha)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(commands, [])


if __name__ == "__main__":
    unittest.main()
