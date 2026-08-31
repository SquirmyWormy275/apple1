from __future__ import annotations

import pytest

from neural1.artwork import ArtworkCandidate, RightsRegistry
from neural1.commissioning import REQUIRED_GATES, evaluate_physical_qualification
from neural1.core import Neural1Error
from neural1.experiments import HistoricalComponent
from neural1.history import HistoricalCorpus, HistoricalSource


def test_historical_authority_requires_source_and_1976_availability(tmp_path) -> None:
    corpus = HistoricalCorpus()
    source = HistoricalSource("SRC", "TEST SOURCE", "ISSUER", "1976-01-01", "archive:test", "2026-08-30", "a" * 64, "DATASHEET", "REVIEW_REQUIRED")
    corpus.add_source(source)
    component = HistoricalComponent("PART", "CPU", "MAKER", "1976-12-31", ("SRC",), {"fixture": True}, True)
    corpus.add_component(component)
    assert len(corpus.export(tmp_path / "corpus.json")) == 64
    with pytest.raises(Neural1Error, match="outside"):
        corpus.add_component(HistoricalComponent("FUTURE", "CPU", "MAKER", "1977-01-01", ("SRC",), {}, True))


def test_artwork_cannot_be_published_without_rights_evidence() -> None:
    registry = RightsRegistry()
    blocked = ArtworkCandidate("A", "WOZNIAK_PORTRAIT", "external", ("HERITAGE-APPLE1-SLIDESHOW",), "David Schmenk", "NOT_ESTABLISHED", (), "ATTRIBUTION", False)
    registry.add(blocked)
    assert registry.concept_status()["WOZNIAK_PORTRAIT"] == "BLOCKED"
    with pytest.raises(Neural1Error, match="rights"):
        registry.add(ArtworkCandidate("B", "JOBS_PORTRAIT", "external", ("SRC",), "AUTHOR", "UNKNOWN", (), "ATTR", True))


def test_physical_gate_defaults_to_complete_stop() -> None:
    decision = evaluate_physical_qualification({})
    assert decision.ready is False
    assert decision.blocked_gates == REQUIRED_GATES
    assert "serial_open" in decision.prohibited_actions
    assert evaluate_physical_qualification({gate: True for gate in REQUIRED_GATES}).ready is True
