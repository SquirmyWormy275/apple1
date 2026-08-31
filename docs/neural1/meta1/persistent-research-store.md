# Persistent research store

`ResearchDatabase` is a local SQLite query index for claims, evidence, edges,
append-only events, research questions, forecasts, blind reviews, and candidate
discoveries. Canonical large artifacts remain in the content-addressed store.
Claim history can be reconstructed through an event sequence. The research
queue publishes its normalized inputs and exact additive-minus-cost score.

Forecasts are sealed before reveal and use Brier score. Blind reviews retain
hidden field names and a reveal event. Tribunal verdicts apply a declared causal
threshold and opposing-evidence rule to stored records; no model vote can create
support.
