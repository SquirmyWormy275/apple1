from __future__ import annotations

from neural1.meta import ClaimGraph
from neural1.meta_store import ResearchDatabase
from neural1.meta_console import main


def test_persistent_claim_query_history_and_rule_based_tribunal(tmp_path) -> None:
    graph = ClaimGraph()
    claim = graph.create_claim("X IMPROVES Y", {"experiment": "fixture"})
    evidence = graph.add_evidence("replay", "a" * 64, ["RUN"], "matched", causal_level=2)
    database = ResearchDatabase(tmp_path / "meta.sqlite3")
    database.put_claim(claim)
    database.put_evidence(evidence)
    database.relate(evidence.evidence_id, "supports", claim.claim_id)
    assert database.claim(claim.claim_id)["statement"] == "X IMPROVES Y"
    assert len(database.claim_history(claim.claim_id)) == 1
    assert database.tribunal(claim.claim_id, minimum_causal_level=2)["verdict"] == "SUPPORTED"
    assert database.tribunal(claim.claim_id, minimum_causal_level=3)["verdict"] == "INSUFFICIENT_EVIDENCE"
    database.close()


def test_transparent_research_queue_orders_information_value(tmp_path) -> None:
    database = ResearchDatabase(tmp_path / "meta.sqlite3")
    low = database.enqueue("LOW", uncertainty=.2, novelty=.1, information_gain=.1, cross_experiment_relevance=.1, normalized_compute_cost=.8)
    high = database.enqueue("HIGH", uncertainty=1, novelty=1, information_gain=1, cross_experiment_relevance=1, normalized_compute_cost=.1)
    assert database.research_queue()[0]["question_id"] == high.question_id
    assert high.priority > low.priority


def test_forecast_blinding_and_candidate_discovery_are_first_class(tmp_path) -> None:
    database = ResearchDatabase(tmp_path / "meta.sqlite3")
    forecast = database.forecast("WILL IT PASS?", .75, "POSITIVE", "MEDIUM")
    assert database.reveal_forecast(forecast, True) == .0625
    review = database.blind_review("RUN", ["model", "outcome"], "NO ANOMALY")
    database.reveal_review(review)
    discovery = database.discovery("detector-v1", "b" * 64, "POSSIBLE TRANSITION")
    assert discovery.startswith("N1-D-")


def test_meta_console_queries_without_a_model(tmp_path, capsys) -> None:
    path = tmp_path / "meta.sqlite3"
    database = ResearchDatabase(path)
    database.enqueue("QUESTION", uncertainty=1, novelty=1, information_gain=1, cross_experiment_relevance=1, normalized_compute_cost=0)
    database.close()
    assert main(["--db", str(path), "queue"]) == 0
    assert "QUESTION" in capsys.readouterr().out
