# Apple-1 world runtime

The world is a byte-exact 64 KiB image with a bounded 1K/2K/3K/4K experimental
RAM region. The restriction is an experiment policy, not a claim that every
budget maps identically to historical hardware. WozMon interactions support
modeled examine, block examine, deposit, and run intent. Run intent is recorded;
arbitrary 6502 execution is not yet implemented in this world layer.

The host verifier can inspect bytes for scoring and intervention, but agents
must receive only a `WozMonSession`. This boundary is structural and tested.
