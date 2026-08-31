# 1976 source ingestion

Historical source records require ID, title, author/issuer, publication date,
archive path or URL, retrieval date, SHA-256, source type, rights status, and
notes. An authoritative component requires at least one registered source and
explicit availability evidence dated no later than 1976-12-31. Unknown sources,
invalid hashes/dates, and later availability are rejected.

The preserved manuals manifest supplies byte identities for candidate research
sources, but later books and replica manuals are not automatically treated as
1976 component evidence. The JSON fixture remains synthetic and rejection-only.

## Integrated March-1976 research tranche

The archived 1976 MULTIVERSE research tranche is now present under
`docs/neural1/research/` and registered by
`data/neural1/history/1976-research-index.json`.

The integration is intentionally two-stage:

1. **Research staging** preserves source discoveries, cutoff rules, lifecycle
   notes, price regimes, capability contracts, procurement observations, and the
   preregistered `N1-MV-C001` challenge.
2. **Runtime promotion** happens only after the exact supporting artifact is
   acquired, SHA-256 identified, the extracted claim is reviewed, and cutoff
   eligibility is validated.

A strong historical note is therefore not automatically an authoritative
`HistoricalComponent`. This prevents web-derived or secondary observations from
silently entering blind MULTIVERSE runs.

The staging index must retain:

- `requires_sha256: true`;
- `requires_claim_review: true`;
- `requires_cutoff_validation: true`;
- `missing_prices_remain_null: true`;
- `no_llm_estimates: true`.

Repository validation rejects a staging index that declares authoritative
runtime component IDs. `neural1 history-status` exposes the current readiness
state without loading staged facts into an experiment.

## Promotion procedure

For each claim or component proposed for promotion:

1. acquire or identify the exact source artifact permitted by rights policy;
2. record its SHA-256 and retrieval metadata;
3. extract the specific supported claim without broadening it;
4. verify publication date and `DESIGN_1976_03_10` or later-world eligibility;
5. record lifecycle/procurement caveats and economic regime where relevant;
6. create the authoritative `HistoricalSource`;
7. create the linked `HistoricalComponent` only after source registration;
8. run repository validation and focused historical-corpus tests;
9. update the staging index promoted-record count and IDs only when its status is
   moved out of `RESEARCH_STAGING` under a reviewed change.

Until that procedure is complete, unresolved prices stay unresolved and no
model-generated estimate may fill them.
