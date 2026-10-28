from pathlib import Path
from tempfile import TemporaryDirectory

from neural1.meta import ClaimGraph
from neural1.meta_store import ResearchDatabase

graph = ClaimGraph()
claim = graph.create_claim("FIXTURE X SUPPORTS Y", {"experiment": "textbook fixture"})
evidence = graph.add_evidence("synthetic", "a" * 64, ["FIXTURE"], "authored test evidence", causal_level=2)
with TemporaryDirectory() as d:
    db = ResearchDatabase(Path(d) / "meta.sqlite")
    try:
        db.put_claim(claim)
        db.put_evidence(evidence)
        db.relate(evidence.evidence_id, "supports", claim.claim_id)
        print("History entries:", len(db.claim_history(claim.claim_id)))
        print("Threshold 2:", db.tribunal(claim.claim_id, minimum_causal_level=2)["verdict"])
        print("Threshold 3:", db.tribunal(claim.claim_id, minimum_causal_level=3)["verdict"])
        db.enqueue(
            "Repeat the controlled test",
            uncertainty=1,
            novelty=0,
            information_gain=1,
            cross_experiment_relevance=0,
            normalized_compute_cost=1,
        )
        print("Queue entries:", len(db.research_queue()))
        assert len(db.claim_history(claim.claim_id)) == 1
    finally:
        db.close()
