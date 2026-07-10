"""Complete client-tool loop with replayed assistant calls and matched results."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from inspect import Parameter, signature
from typing import Any


MODEL = "claude-sonnet-5"


@dataclass(frozen=True)
class ToolLoopResult:
    answer: str
    messages: tuple[dict[str, Any], ...]


def _value(value: Any, name: str, default: Any = None) -> Any:
    return value.get(name, default) if isinstance(value, Mapping) else getattr(value, name, default)


def _plain_block(block: Any) -> dict[str, Any]:
    if isinstance(block, Mapping):
        return dict(block)
    model_dump = getattr(block, "model_dump", None)
    if callable(model_dump):
        return dict(model_dump(mode="json", exclude_none=True))
    result = {"type": _value(block, "type")}
    for name in ("id", "name", "input", "text"):
        item = _value(block, name)
        if item is not None:
            result[name] = item
    return result


def _tool_schema(name: str, tool: Callable[..., Any]) -> dict[str, Any]:
    parameters = signature(tool).parameters
    properties = {parameter: {"type": "string"} for parameter in parameters}
    required = [
        parameter
        for parameter, details in parameters.items()
        if details.default is Parameter.empty
        and details.kind in {Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY}
    ]
    return {
        "name": name,
        "description": (tool.__doc__ or f"Execute the local {name} tool.").strip(),
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": False,
        },
    }


def run_tool_loop(
    prompt: str,
    *,
    tools: Mapping[str, Callable[..., Any]],
    create: Callable[..., Any] | None = None,
    max_turns: int = 8,
) -> ToolLoopResult:
    if create is None:
        from anthropic import Anthropic

        create = Anthropic().messages.create
    messages: list[dict[str, Any]] = [{"role": "user", "content": prompt}]
    definitions = [_tool_schema(name, tools[name]) for name in sorted(tools)]
    for _ in range(max_turns):
        response = create(
            model=MODEL,
            max_tokens=2048,
            messages=messages,
            tools=definitions,
        )
        stop_reason = _value(response, "stop_reason")
        blocks = [_plain_block(block) for block in _value(response, "content", [])]
        if stop_reason == "refusal":
            raise RuntimeError("Claude refused during the tool loop")
        if stop_reason != "tool_use":
            answer = "".join(block.get("text", "") for block in blocks if block["type"] == "text")
            return ToolLoopResult(answer=answer, messages=tuple(messages))

        calls = [block for block in blocks if block["type"] == "tool_use"]
        if not calls:
            raise RuntimeError("tool_use stop reason without a tool_use block")
        messages.append({"role": "assistant", "content": blocks})
        results = []
        for call in calls:
            name = str(call["name"])
            if name not in tools:
                raise KeyError(f"unknown tool: {name}")
            result = tools[name](**dict(call.get("input", {})))
            results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": str(call["id"]),
                    "content": str(result),
                }
            )
        messages.append({"role": "user", "content": results})
    raise RuntimeError("tool loop exceeded max_turns")


if __name__ == "__main__":
    print("Import run_tool_loop() and provide explicitly authorized local tools.")
