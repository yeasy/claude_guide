from __future__ import annotations

import asyncio
import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


def load(name: str):
    path = EXAMPLES / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class GoldenPathTests(unittest.TestCase):
    def test_messages_request_schema_and_refusal_handling(self):
        module = load("messages_api")
        calls = []

        def fake_create(**request):
            calls.append(request)
            return {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "text", "text": "你好"}],
                "stop_reason": "end_turn",
            }

        result = module.send_message("你好", create=fake_create)
        self.assertEqual(result, "你好")
        self.assertEqual(
            calls,
            [
                {
                    "model": "claude-sonnet-5",
                    "max_tokens": 1024,
                    "messages": [{"role": "user", "content": "你好"}],
                }
            ],
        )

        def refused(**_request):
            return {"content": [], "stop_reason": "refusal"}

        with self.assertRaises(module.ClaudeRefusalError):
            module.send_message("unsafe", create=refused)

    def test_tool_loop_replays_assistant_call_and_matched_tool_result(self):
        module = load("tool_use_loop")
        calls = []

        class ThinkingBlock:
            type = "thinking"

            @staticmethod
            def model_dump(**_kwargs):
                return {"type": "thinking", "thinking": "plan", "signature": "sig"}

        responses = iter(
            (
                {
                    "content": [
                        ThinkingBlock(),
                        {
                            "type": "tool_use",
                            "id": "toolu_weather_1",
                            "name": "weather",
                            "input": {"city": "Paris"},
                        }
                    ],
                    "stop_reason": "tool_use",
                },
                {
                    "content": [{"type": "text", "text": "Paris: 21 C"}],
                    "stop_reason": "end_turn",
                },
            )
        )

        def fake_create(**request):
            calls.append(request)
            return next(responses)

        result = module.run_tool_loop(
            "weather?",
            tools={"weather": lambda city: f"{city}: 21 C"},
            create=fake_create,
        )
        self.assertEqual(result.answer, "Paris: 21 C")
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0]["tools"][0]["input_schema"]["required"], ["city"])
        self.assertEqual(calls[0]["tools"][0]["input_schema"]["properties"]["city"]["type"], "string")
        replay = calls[1]["messages"]
        self.assertEqual(replay[1]["role"], "assistant")
        self.assertEqual(replay[1]["content"][0], {"type": "thinking", "thinking": "plan", "signature": "sig"})
        self.assertEqual(replay[1]["content"][1]["id"], "toolu_weather_1")
        self.assertEqual(replay[2]["role"], "user")
        self.assertEqual(replay[2]["content"][0]["type"], "tool_result")
        self.assertEqual(replay[2]["content"][0]["tool_use_id"], "toolu_weather_1")
        self.assertEqual(replay[2]["content"][0]["content"], "Paris: 21 C")

    def test_agent_sdk_success_and_error_events_without_network(self):
        module = load("agent_sdk_minimal")

        async def successful_events(_prompt):
            for event in (
                {"type": "assistant", "content": [{"type": "text", "text": "working"}]},
                {"type": "result", "subtype": "success", "result": "done"},
            ):
                yield event

        result = asyncio.run(module.run_agent("task", event_source=successful_events))
        self.assertEqual(result.result, "done")
        self.assertEqual(result.assistant_messages, ("working",))

        async def failing_events(_prompt):
            yield {
                "type": "result",
                "subtype": "error_during_execution",
                "is_error": True,
                "result": None,
                "errors": ["tool failed"],
            }

        with self.assertRaisesRegex(module.AgentRunError, "tool failed"):
            asyncio.run(module.run_agent("task", event_source=failing_events))

    def test_dependencies_are_exact_and_chapters_link_all_examples(self):
        requirements = (EXAMPLES / "requirements.txt").read_text(encoding="utf-8")
        self.assertEqual(
            requirements.splitlines(),
            ["anthropic==0.116.0", "claude-agent-sdk==0.2.115"],
        )
        routes = {
            "12_appendix/12.1_api_ref.md": ("messages_api.py",),
            "03_tools/3.3_results.md": ("tool_use_loop.py",),
            "08_agent/8.6_agent_sdk_deep_dive.md": ("agent_sdk_minimal.py",),
            "README.md": ("messages_api.py", "tool_use_loop.py", "agent_sdk_minimal.py"),
        }
        for relative, markers in routes.items():
            text = (ROOT / relative).read_text(encoding="utf-8")
            for marker in markers:
                self.assertIn(marker, text, relative)
        self.assertIn("python3 -m unittest", (ROOT / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
