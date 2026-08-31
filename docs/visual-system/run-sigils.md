# Run sigils

A run sigil is a mirror-symmetric printable fingerprint. SHA-256 of the ASCII
run ID supplies two-bit values mapped cyclically to `.`, `+`, and `#`; one half
of each row is reflected. Default output is 7x7. The mapping encodes identity
only—not fitness, model quality, or outcome—and therefore remains stable when a
claim about the run changes. Collisions are visually possible; the run ID and
manifest remain authoritative.
