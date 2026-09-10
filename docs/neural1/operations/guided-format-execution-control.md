# Instruction-guided format control v3

A native Pi probe using the existing Phi4-mini model, explicit Ollama chat
transport, and the format example below produced all three accepted Monitor
commands. Both recorded execution and an independent virtual check printed A and
returned to the Monitor in four instructions. Its durable probe record is
`logs/qualification/phi4-chat-fewshot-1789054447849376051.json` on the NEURAL1 SSD.
This establishes that specific model/transport/prompt combination. It does not
establish that chat alone caused the improvement: prompt and transport changed.
The earlier unsuccessful Qwen, Phi and ISA-only probes remain negative evidence.

The source preset preserves the exact successful instructional core: an example
at 0400 prints B, then requests the corresponding program at 0200 printing A.
Family-specific context precedes that core. The model must generate the new
deposit, examination and run command itself; the example is never executed by
application code or used as a fallback. The requested A program is not inserted
into the prompt as a replacement response. Repeating the B example cannot pass
the unchanged 0200 execution evaluator.

New matching transcripts record `guided-format-output-and-return-v3`. Existing
v1 and ISA-only v2 transcripts retain their respective criteria. This is an
instructional formatting/execution control, not autonomous program discovery.
The complete shipped family variants still require native acceptance after
installation; one successful provider probe does not satisfy every family gate.

4K keeps its persistent world/lineage and bounded private feedback. RAM REPUBLIC
retains its declared shared-memory examination and isolated private contexts.
SELFHOST starts at raw stage 1, with later stages requiring persistent independent
qualification. No parser, byte acceptance, ancestry or evaluator rule is relaxed.

Exact256 retains the B example and A request but replaces the three-line/no-padding
instruction with sixteen sixteen-byte deposits plus examination and execution.
All 256 bytes must come from the actual response, with explicit 248-byte zero
padding around the eight-byte routine. The application never fills omitted
bytes. Its declared call stack and Monitor API scope and strict execution-memory
checks remain unchanged. This variant is a bounded executable control, not a
blinded replacement-monitor result.

The 256-byte preset applies its boundary during live Monitor turns as well as
independent evaluation. Deposits, examinations, and requested entry points are
restricted to 0200-02FF. CPU execution permits only candidate memory, the declared
NMOS call stack, and the existing Monitor services; an escape yields explicit
error feedback without exposing outside-memory output. Other families retain
their normal 4K Monitor surface.
