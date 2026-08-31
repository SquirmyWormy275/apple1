"""Read-only gate evaluation; this module has no hardware access capability."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class QualificationDecision:
    ready: bool
    target: str
    passed_gates: tuple[str, ...]
    blocked_gates: tuple[str, ...]
    prohibited_actions: tuple[str, ...]


REQUIRED_GATES = (
    "ft232r_stop_explicitly_superseded",
    "named_artifact_reviewed",
    "reset_recovery_prepared",
    "electrical_measurement_coverage",
    "exclusive_output_boundary_verified",
    "operator_approval_recorded",
)


def evaluate_physical_qualification(evidence: Mapping[str, bool]) -> QualificationDecision:
    passed = tuple(gate for gate in REQUIRED_GATES if evidence.get(gate) is True)
    blocked = tuple(gate for gate in REQUIRED_GATES if evidence.get(gate) is not True)
    prohibited = ("serial_open", "transmit", "firmware_load", "eeprom_write", "cffa1_write", "gpio_control", "generated_program_execution") if blocked else ()
    return QualificationDecision(not blocked, "PHYSICAL_QUALIFICATION", passed, blocked, prohibited)
