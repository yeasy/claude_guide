from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

import check_project_rules as rules


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "12_appendix" / "12.7_volatile_facts.md"


class VolatileFactsTests(unittest.TestCase):
    def write_ledger(
        self,
        directory: str,
        *,
        verified: str = "2026-07-10",
        expires: str = "2026-08-09",
        ttl: int = 30,
        status: str = "current",
    ) -> Path:
        path = Path(directory) / "facts.md"
        path.write_text(
            "# Facts\n\n"
            f"> `verified_at`: {verified} · `expires_at`: {expires} · `ttl_days`: {ttl}\n\n"
            f"<!-- volatile-status: id=models status={status} -->\n",
            encoding="utf-8",
        )
        return path

    def test_fresh_ledger_and_inclusive_boundaries(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_ledger(directory)
            self.assertEqual(rules.check_volatile_facts(path, date(2026, 7, 10)), [])
            self.assertEqual(rules.check_volatile_facts(path, date(2026, 8, 9)), [])
            issues = rules.check_volatile_facts(path, date(2026, 8, 10))
            self.assertTrue(any("expired" in issue for issue in issues), issues)

    def test_future_dates_invalid_ttl_and_open_conflicts_fail_closed(self):
        cases = (
            ({"verified": "2026-07-11", "expires": "2026-08-10"}, "future"),
            ({"expires": "2026-07-09"}, "after verified_at"),
            ({"expires": "2026-09-08", "ttl": 60}, "exactly 30 days"),
            ({"status": "open-conflict"}, "unresolved conflict"),
        )
        for arguments, marker in cases:
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as directory:
                path = self.write_ledger(directory, **arguments)
                issues = rules.check_volatile_facts(path, date(2026, 7, 10))
                self.assertTrue(any(marker in issue for issue in issues), issues)

    def test_resolved_conflict_and_current_official_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_ledger(directory, status="resolved-conflict")
            self.assertEqual(rules.check_volatile_facts(path, date(2026, 7, 10)), [])

        text = LEDGER.read_text(encoding="utf-8")
        required = (
            "`verified_at`: 2026-07-10",
            "`expires_at`: 2026-08-09",
            "`ttl_days`: 30",
            "status=resolved-conflict",
            "`claude-sonnet-5`",
            "Fable 5 已于 2026-07-01 恢复全球访问",
            "Mythos 5 非普遍可用",
            "Project Glasswing 获批客户",
            "无自助注册",
            "$2 / $10",
            "adaptive thinking 默认开启",
            "`stop_reason: \"refusal\"`",
            "https://platform.claude.com/docs/en/about-claude/models/migration-guide",
            "https://platform.claude.com/docs/en/build-with-claude/prompt-caching",
            "https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback",
        )
        for marker in required:
            self.assertIn(marker, text)
        self.assertEqual(rules.check_volatile_facts(LEDGER, date(2026, 7, 10)), [])

    def test_current_mythos_guidance_uses_catalog_contract_not_event_geography(self):
        current_snapshots = (
            "01_intro/1.2_model_family.md",
            "03_tools/3.5_programmatic.md",
            "12_appendix/12.6_model_comparison.md",
            "12_appendix/12.7_volatile_facts.md",
            "13_advanced/README.md",
        )
        for relative in current_snapshots:
            with self.subTest(path=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                for marker in ("非普遍可用", "Project Glasswing", "获批客户"):
                    self.assertIn(marker, text, relative)
                self.assertNotIn("部分美国机构", text, relative)

        ledger = LEDGER.read_text(encoding="utf-8")
        self.assertIn("无自助注册", ledger)

    def test_historical_timeline_retains_july_1_us_organization_event(self):
        historical_snapshots = {
            "01_intro/1.1_born.md": 1,
            "12_appendix/12.3_glossary.md": 1,
            "13_advanced/13.1_claude5_preview.md": 2,
        }
        for relative, minimum_occurrences in historical_snapshots.items():
            with self.subTest(path=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                self.assertIn("2026-07-01", text, relative)
                self.assertGreaterEqual(
                    text.count("当时恢复给一组美国机构"),
                    minimum_occurrences,
                    relative,
                )

    def test_main_checker_enforces_volatile_facts(self):
        source = (ROOT / "check_project_rules.py").read_text(encoding="utf-8")
        self.assertIn("issues.extend(check_volatile_facts())", source)

    def test_reader_chapters_route_current_pricing_thinking_cache_and_migration(self):
        expectations = {
            "12_appendix/12.5_pricing.md": (
                "Claude Sonnet 5",
                "$2.00",
                "$10.00",
                "2026-08-31",
                "2026-07-01 恢复全球访问",
            ),
            "01_intro/1.2_model_family.md": (
                "`claude-sonnet-5`",
                "Fable 5 已于 2026-07-01 恢复全球访问",
            ),
            "08_agent/8.4_extended_thinking.md": (
                "Sonnet 5 默认启用 Adaptive Thinking",
                '`thinking={"type": "disabled"}`',
                "手动 Extended Thinking 会返回 400",
            ),
            "10_optimization/10.2_caching.md": (
                "1 小时断点必须放在 5 分钟断点之前",
                '"ttl": "1h"',
            ),
            "13_advanced/13.1_claude5_preview.md": (
                "Sonnet 4.6 → Sonnet 5 迁移检查清单",
                "约增加 30% token",
                '`stop_reason: "refusal"`',
                "移除非默认 `temperature`、`top_p`、`top_k`",
            ),
        }
        for relative, markers in expectations.items():
            text = (ROOT / relative).read_text(encoding="utf-8")
            for marker in markers:
                self.assertIn(marker, text, relative)

    def test_current_selection_guidance_routes_new_projects_to_sonnet_5(self):
        intro = (ROOT / "01_intro" / "1.4_model_selection.md").read_text(encoding="utf-8")
        for marker in (
            "新项目首评：Claude Sonnet 5",
            "既有 Sonnet 4.6",
            "2026-08-31",
            "约增加 30% token",
            '| **Claude Sonnet 5** | ~$3.6 |',
            'MODEL_BALANCED = "claude-sonnet-5"',
        ):
            self.assertIn(marker, intro)
        for stale in (
            "默认首选：Claude Sonnet 4.6",
            'MODEL_BALANCED = "claude-sonnet-4-6"',
        ):
            self.assertNotIn(stale, intro)

        comparison = (ROOT / "12_appendix" / "12.6_model_comparison.md").read_text(encoding="utf-8")
        for marker in (
            "新项目先评测 Claude Sonnet 5",
            "既有 Sonnet 4.6 系统按迁移清单灰度升级",
            "推荐：**Claude Sonnet 5**",
            'model="claude-sonnet-5"',
            "历史快照严格 2D Pareto 前沿",
        ):
            self.assertIn(marker, comparison)
        for stale in (
            "推荐：**Claude Sonnet 4.6**",
            'model="claude-sonnet-4-6"',
            "推荐: Claude Sonnet 4.6",
            "推荐: Sonnet 4.6 + 少量 Opus 4.8",
        ):
            self.assertNotIn(stale, comparison)


class Sonnet46UsageContractTests(unittest.TestCase):
    def test_unmarked_active_sonnet_46_example_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "active.md").write_text(
                'response = client.messages.create(model="claude-sonnet-4-6")\n',
                encoding="utf-8",
            )
            issues = rules.check_sonnet_46_usage(root=root, allowlist={})
            self.assertEqual(
                issues,
                ["active.md:1: Sonnet 4.6 use is not explicitly allowlisted"],
            )

    def test_repository_contains_only_reasoned_sonnet_46_uses(self):
        self.assertEqual(rules.check_sonnet_46_usage(), [])
        self.assertTrue(rules.SONNET_46_ALLOWLIST)
        for (relative, line_no), reason in rules.SONNET_46_ALLOWLIST.items():
            with self.subTest(path=relative, line=line_no):
                self.assertTrue(reason.strip())

    def test_main_checker_enforces_sonnet_46_usage_contract(self):
        source = (ROOT / "check_project_rules.py").read_text(encoding="utf-8")
        self.assertIn("issues.extend(check_sonnet_46_usage())", source)


if __name__ == "__main__":
    unittest.main()
