# Apple-1 world runtime

The world is a byte-exact 64 KiB image with a bounded 1K/2K/3K/4K experimental
RAM region. The restriction is an experiment policy, not a claim that every
budget maps identically to historical hardware. WozMon interactions support
modeled examine, block examine, deposit, and bounded run. Deposited NMOS 6502
bytes execute through Py65 and stop on BRK, Monitor warm entry, escape from
allowed RAM, or an instruction limit. Monitor ECHO is captured. Exact register
traces are verifier evidence and are never exposed as an agent debugger API.

The host verifier can inspect bytes for scoring and intervention, but agents
must receive only a `WozMonSession`. This boundary is structural and tested.
