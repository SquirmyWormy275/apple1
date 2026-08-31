# SELFHOST/1

Stages are raw machine code, a model-created assembler, a model-created
language, and self-hosting. Parent artifacts must already be qualified; later
stages inherit the required earlier infrastructure. A stage-four fixture passes
only if a rebuild callback reproduces the expected compiler bytes. A research
criterion must additionally define the minimal retained bootstrap, removal of
the current compiler, reconstruction steps, validation source, deterministic
behavior comparison, and reproducibility across declared seeds.
