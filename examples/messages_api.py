"""Minimal Messages API path with an injectable transport for offline tests."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any


MODEL = "claude-sonnet-5"


class ClaudeRefusalError(RuntimeError):
    """The API returned a successful response whose stop reason is refusal."""


def _value(response: Any, name: str, default: Any = None) -> Any:
    return response.get(name, default) if isinstance(response, Mapping) else getattr(response, name, default)


def _block_value(block: Any, name: str, default: Any = None) -> Any:
    return block.get(name, default) if isinstance(block, Mapping) else getattr(block, name, default)


def send_message(
    prompt: str,
    *,
    create: Callable[..., Any] | None = None,
    model: str = MODEL,
) -> str:
    """Send one user message and return concatenated text blocks."""

    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    if create is None:
        from anthropic import Anthropic

        create = Anthropic().messages.create
    response = create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    if _value(response, "stop_reason") == "refusal":
        raise ClaudeRefusalError("Claude refused the request")
    return "".join(
        str(_block_value(block, "text", ""))
        for block in _value(response, "content", [])
        if _block_value(block, "type") == "text"
    )


if __name__ == "__main__":
    print(send_message("用一句话解释 Claude Messages API。"))
