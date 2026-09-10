# Persistent SELFHOST qualification

The installed console supports `SELFHOST`, `SELFHOST INGEST run-id`,
`SELFHOST REBUILD artifact-id`, `SELFHOST QUALIFY evidence-path`,
`SELFHOST EXPORT artifact-id` and `SELFHOST OPEN export-path`.

INGEST independently replays a completed successful SELFHOST run, compares all
4096 artifact bytes with its recorded identity, and checks the output/return
starting task. It archives the exact transcript, provider registry and artifact.
The immutable archive under `research/selfhost` survives application restart;
REBUILD works from archived evidence even after the original run is unavailable.
Synthetic/replay provenance remains visibly synthetic. A successful raw run
qualifies **stage 1 only**, never an assembler or a compiler automatically.

Later stages consume actual compiler/assembler research evidence. A JSON evidence
file on the SSD has these fields (addresses and bounds are integers):

- `stage`: 2, 3 or 4; `candidate_artifact`: an archived qualified candidate ID.
- `parents`: qualified archive IDs; `builder_parent`: a member at the immediate
  previous stage. Unknown, failed, same-stage and skipped-stage ancestry fail.
- `language_contract`: the precise bounded syntax and semantic claim being tested.
- `build`: `input_hex`, `input_address`, `entrypoint`, `output_address`,
  `output_bytes`, `max_instructions`.
- `tests`: two to eight objects containing `input_hex`, `input_address`,
  `entrypoint`, `output_address`, `expected_hex`, `max_instructions`.
- Stage 4 also requires `compiler_region`: `address` and `length` identifying
  the current compiler bytes whose removal is asserted.

Every build starts with the retained parent's archived image, never the current
candidate image. Source input is limited to 2048 bytes and must occupy previously
zero workspace. Builds run twice and must reproduce all 4096 candidate bytes
exactly. Each execution is capped at 100000 instructions. Stage 4 additionally
rejects a declared compiler region retained literally anywhere in the parent
image or build input. The region must describe the real compiler, not an
unrelated marker; the archived declaration remains inspectable evidence.

Behavior tests execute the candidate with distinct inputs and distinct expected
outputs, require bounded successful execution, and reject a zero-image control.
Stage-two source/expectation vectors are independently checked with the existing
lesson assembler; mnemonic source is required, not an unconditional byte dump.
Later custom-language contracts remain explicitly scoped to their supplied
vectors. This does not establish general language correctness or prove that a
misdeclared compiler region identifies a compiler. Failed exact rebuilds and
behavior tests remain persisted **unqualified** evidence and cannot parent a
later stage. No supplied Python, shell script or callback is executed.

EXPORT includes the candidate and qualified parent dependency closure. OPEN
verifies immutable record/evidence/image identities and repeats reconstruction.
Normal archive operations also produce queryable META evidence through the
console. A later-stage evidence file is experiment input, not software setup;
there is no fabricated compiler example promoted as live scientific evidence.

Qualification now records `cpu-writes-v1` provenance: addresses actually written
by executing 6502 instructions, the addresses required for acceptance, and any
missing writes. Host source loading is excluded. All behavioral vectors use the
same input address, entry point, and output address, with disjoint input/output
regions. Every behavioral output byte must receive a CPU write; overwriting an
identical prefilled byte is valid, while returning a prefilled table with NOP/BRK
is not. Rebuilds may retain unchanged bootstrap bytes, but every byte changed
from the retained image must receive a CPU write, so input preloading alone
cannot reconstruct a candidate. Reopening/rebuilding applies this production
check as well. These are bounded declared-language controls, not a claim of
general compiler correctness from two vectors; stage-one raw transcript replay
remains explicitly distinct from later-stage builder execution.
