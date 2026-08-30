# Original CF-card baseline

The original project CF card is preserved as a sector-for-sector image at:

`preservation/cf-card/2026-08-28/apple1-cf-card-lexar-disk2-128974848.img`

Its preservation manifest records:

- captured capacity: **128,974,848 bytes**;
- SHA-256: `5C98A3BB8C77E4155167A1C8DF353AE07697F57C939DE9196B838ECF097AD836`;
- source opened read-only;
- a second full read produced the same SHA-256.

The image is tracked through Git LFS. This `cf-card/` control layer does not
move, rename, rewrite, mount, or extract it.

## Why the raw image remains separate

The raw image is evidence of the original card state. New educational material
is an overlay candidate, not a reason to modify the baseline. A future build
should operate on a separate working copy after the card mechanism and file
placement are deliberately resolved.

## File-level inventory

A file-level inventory of the original card is **not established here**. The
preserved sector image is authoritative; do not invent original filenames or a
CFFA1 directory structure from memory. If the project later performs an
approved off-device filesystem inspection, record the resulting inventory as a
new derived artifact with provenance back to this image.
