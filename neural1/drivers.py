"""Experiment-specific prompts and safe response parsers for shared campaigns."""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass

from .campaign import CampaignCell

_MONITOR_COMMAND = re.compile(r"^(?:[0-9A-F]{1,4}(?::(?: [0-9A-F]{2})+|\.[0-9A-F]{1,4}|R)?)$")


@dataclass(frozen=True)
class ExperimentDriver:
    experiment_id: str
    system_constraint: str
    objective: str

    def prompt(self, cell: CampaignCell, generation: int) -> str:
        return (
            f"NEURAL1 EXPERIMENT: {self.experiment_id}\n"
            f"GENERATION: {generation}\nSEED: {cell.seed}\n"
            f"CONSTRAINT: {self.system_constraint}\nOBJECTIVE: {self.objective}\n"
            "Return only permitted WozMon command lines when machine interaction is applicable. "
            "Do not use shell, Python, assembler APIs, debugger APIs, or prose disguised as execution evidence."
        )

    @staticmethod
    def commands(response: str) -> Sequence[str]:
        commands = []
        for raw in response.upper().splitlines():
            candidate = raw.strip().strip("`")
            if _MONITOR_COMMAND.fullmatch(candidate):
                commands.append(candidate)
        return commands[:32]


DRIVERS = {
    "4k-mind": ExperimentDriver("4k-mind", "Persistent knowledge must reside in allowed Apple-1 RAM and interaction is WozMon-only.", "Improve or document a tiny reusable routine in RAM."),
    "1976-multiverse": ExperimentDriver("1976-multiverse", "Proposals are hypotheses; only source-backed components can become authoritative.", "Propose a structural machine design for later deterministic validation."),
    "selfhost1": ExperimentDriver("selfhost1", "Use only the currently qualified bootstrap stage and WozMon machine entry.", "Advance one reproducible bootstrap tool or validation routine."),
    "256-byte-universe": ExperimentDriver("256-byte-universe", "The monitor must fit exactly 256 bytes; WozMon reference bytes are hidden.", "Improve a candidate monitor routine against stated functional requirements."),
    "ram-republic": ExperimentDriver("ram-republic", "No host-side agent chat; durable communication must use shared Apple-1 RAM.", "Observe shared state and make one compatible contribution without assuming a protocol."),
}


def objective(cell: CampaignCell, generation: int) -> str:
    return DRIVERS[cell.experiment_id].prompt(cell, generation)


def parse_commands(response: str) -> Sequence[str]:
    return ExperimentDriver.commands(response)
