# Field Library AI

Operations are ASK, HINT, EXPLAIN, SIMPLER, DEEPER, SOURCE, CHECK, TRACE,
COMPARE, and CHALLENGE. The assistant loads the active lesson, SOURCE-NOTES,
STATUS, activity, and—only for CHECK—answers. Empty support returns `NOT
ESTABLISHED BY THE AVAILABLE LIBRARY SOURCES.` Coding explanations first run
the existing Py65 harness and pass its exact screen/buffer/Monitor/instruction
record to the model. The model cannot decide the execution result.

Pi model requests select matching complete, verbatim paragraphs deterministically
from those lesson files. CHECK prioritizes a matching answer paragraph; other
operations never include ANSWERS.md. SOURCE still returns the complete sources.
Each request is limited to 3000 UTF-8 bytes including instructions, question,
selected sources, and deterministic evidence; questions over 512 bytes are
refused without inference. This reserves context space and bounds prefill work
for the deployed 4096-context, 192-output-token model.

TRACE prioritizes exact output, bytes, stop reason, and instruction evidence.
Detailed instruction traces remain in returned deterministic evidence; the
model instead receives an explicit omission notice and trace digest. If the
remaining authoritative evidence cannot fit, interpretation is refused and
full evidence is retained. No evidence values are silently shortened. Selected
source paths and source keys accompany the result. An unsupported response is
preserved; the `grounded` flag indicates absence of that refusal, not an
independent factual correctness verdict.
