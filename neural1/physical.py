"""Replaceable launch target; physical access is intentionally unavailable."""

from __future__ import annotations

from .core import Neural1Error, Target


class PhysicalQualificationAdapter:
    target = Target.PHYSICAL_QUALIFICATION
    available = False

    def launch(self, _: str) -> None:
        raise Neural1Error("physical adapter disabled: commissioning gates are not satisfied")
