"""Pure text formatting for an Apple-1-sized terminal display.

This module deliberately has no serial, model, or hardware dependency.  It is
the deterministic boundary a future Pi bridge can use before handing text to
the evidence-gated serial owner.
"""

from __future__ import annotations


class TextContractError(ValueError):
    """Text is outside a currently measured Apple-1 serial contract."""


def format_for_apple1(text: str, *, width: int = 40) -> list[str]:
    """Return upper-case, printable seven-bit text wrapped to ``width``.

    Non-ASCII display characters intentionally become ``?``.  This is visible
    and deterministic; silently discarding them would make transcript review
    misleading.  Empty input yields one empty display line.
    """
    if width < 1:
        raise ValueError("width must be positive")

    lines: list[str] = []
    for source_line in text.splitlines() or [""]:
        normalized = "".join(_display_character(character) for character in source_line)
        lines.extend(_wrap_line(normalized, width))
    return lines or [""]


def _display_character(character: str) -> str:
    uppercase = character.upper()
    if len(uppercase) != 1 or not (" " <= uppercase <= "~"):
        return "?"
    return uppercase


def _wrap_line(line: str, width: int) -> list[str]:
    if not line:
        return [""]
    return [line[offset : offset + width] for offset in range(0, len(line), width)]
