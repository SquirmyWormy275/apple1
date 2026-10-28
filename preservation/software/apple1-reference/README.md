# Identified interpreter and card-firmware references

These small binaries are read-only derivatives of the project's preserved
original CF image. [The provenance record](provenance.json) gives their original
paths, byte lengths and SHA-256 identities.

| File | Role in the host course | Virtual mapping |
|---|---|---|
| `apple1-basic.bin` | Execute Apple-1 Integer BASIC on an NMOS 6502 | `$E000–$EFFF` |
| `cffa1-v1.1.bin` | Execute CFFA1's real ProDOS and BA1 routines against modeled ATA | `$9000–$AFDF` |

The CFFA1 file's original auxiliary address is `$2000`: that is the preserved
file's loading metadata, not the execution mapping of the installed card ROM.
Its bytes also match the author's v1.1 distribution. The BASIC copy writes the
display at `$D012`. Another publicly circulated interpreter copy uses `$D0F2`
at two instruction operands; the host tests deliberately identify this copy
rather than treating all BASIC binaries as interchangeable.

These are third-party preservation artifacts, not project-authored code.
The repository's license makes no new license grant for them. Original ROM
authorship, rights and the source image's provenance remain separate questions.
No claim of an installed ROM identity or hardware qualification follows from
a passing hash or emulator session.

[Run BASIC](../../../docs/textbook/reference/basic.md) · [Build the card candidate](../../../cf-card/README.md)
