"""Virtual portal state machine; launch adapters remain replaceable."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class Mode(StrEnum):
    PORTAL = "PORTAL"
    COMPUTER = "COMPUTER"
    FIELD_LIBRARY = "FIELD_LIBRARY"
    NEURAL1 = "NEURAL1"
    ABOUT = "ABOUT"


class LaunchAdapter(Protocol):
    def enter_computer(self) -> str: ...


@dataclass(frozen=True)
class VirtualLaunchAdapter:
    def enter_computer(self) -> str:
        return "[V] COMPUTER / MODELED WOZMON"


class Portal:
    def __init__(self, adapter: LaunchAdapter | None = None) -> None:
        self.adapter = adapter or VirtualLaunchAdapter()
        self.mode = Mode.PORTAL

    def select(self, key: str) -> str:
        normalized = key.strip().upper()
        if normalized == "1":
            self.mode = Mode.COMPUTER
            return self.adapter.enter_computer()
        if normalized == "2":
            self.mode = Mode.FIELD_LIBRARY
            return "[V] FIELD LIBRARY / SOURCES AUTHORITATIVE"
        if normalized == "3":
            self.mode = Mode.NEURAL1
            return "[V] NEURAL1 / EXPERIMENTAL COMPUTING LAB"
        if normalized == "?":
            self.mode = Mode.ABOUT
            return "COMPUTER / FIELD LIBRARY / NEURAL1"
        if normalized == "0":
            self.mode = Mode.PORTAL
            return "APPLE-1 PORTAL"
        return "?"


PORTAL_FRAME = """----------------------------------------
               APPLE-1
----------------------------------------

1  COMPUTER
   ORIGINAL 6502 ENVIRONMENT

2  FIELD LIBRARY
   LEARN / EXPLORE / BUILD

3  NEURAL1
   EXPERIMENTAL COMPUTING LAB

?  ABOUT
----------------------------------------
SELECT:"""
