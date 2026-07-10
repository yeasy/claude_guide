"""Minimal Agent SDK event consumer with an injectable offline event source."""

from __future__ import annotations

from collections.abc import AsyncIterator, Callable, Mapping
from dataclasses import dataclass
from typing import Any


class AgentRunError(RuntimeError):
    """The Agent SDK emitted a terminal error result."""


@dataclass(frozen=True)
class AgentRunResult:
    result: str
    assistant_messages: tuple[str, ...]


def _value(value: Any, name: str, default: Any = None) -> Any:
    return value.get(name, default) if isinstance(value, Mapping) else getattr(value, name, default)


def _assistant_text(event: Any) -> str:
    direct = _value(event, "text")
    if direct:
        return str(direct)
    return "".join(
        str(_value(block, "text", ""))
        for block in _value(event, "content", [])
        if _value(block, "type", block.__class__.__name__).lower() in {"text", "textblock"}
    )


async def _sdk_events(prompt: str) -> AsyncIterator[Any]:
    from claude_agent_sdk import ClaudeAgentOptions, query

    options = ClaudeAgentOptions(allowed_tools=[])
    async for event in query(prompt=prompt, options=options):
        yield event


async def run_agent(
    prompt: str,
    *,
    event_source: Callable[[str], AsyncIterator[Any]] | None = None,
) -> AgentRunResult:
    source = event_source or _sdk_events
    assistant: list[str] = []
    result_text: str | None = None
    async for event in source(prompt):
        event_type = str(_value(event, "type", event.__class__.__name__)).lower()
        subtype = str(_value(event, "subtype", "")).lower()
        if event_type in {"assistant", "assistantmessage"}:
            text = _assistant_text(event)
            if text:
                assistant.append(str(text))
        if event_type in {"error", "errorevent"} or subtype == "error" or _value(event, "is_error", False):
            errors = _value(event, "errors", [])
            detail = (
                _value(event, "error")
                or _value(event, "result")
                or "; ".join(map(str, errors))
                or "agent run failed"
            )
            raise AgentRunError(str(detail))
        if event_type in {"result", "resultmessage"} and subtype in {"", "success"}:
            result_text = str(_value(event, "result", ""))
    if result_text is None:
        raise AgentRunError("agent stream ended without a success result")
    return AgentRunResult(result=result_text, assistant_messages=tuple(assistant))


if __name__ == "__main__":
    import asyncio

    print(asyncio.run(run_agent("只回复：Agent SDK 已连接")))
