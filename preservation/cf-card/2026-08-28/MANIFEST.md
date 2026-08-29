# Apple1 CF card raw-image manifest

- **Capture time (UTC):** 2026-08-29T01:34:28.2054665Z
- **Source:** Original Apple1 CF card, read through a USB CF reader
- **Captured capacity:** 128,974,848 bytes
- **Image file:** `apple1-cf-card-lexar-disk2-128974848.img`
- **Image SHA-256:** `5C98A3BB8C77E4155167A1C8DF353AE07697F57C939DE9196B838ECF097AD836`

## Acquisition and verification

The source was opened with read access only. No file was mounted, repaired,
formatted, or written. The image was read in 4 MiB chunks. A second full
read-only pass of the same 128,974,848 bytes produced the same SHA-256 value as
the image.

## Restore boundary

This is a sector-for-sector image for a separately approved restore to an
identified target card of at least this capacity. Before any restore, verify the
downloaded image's SHA-256, confirm the target device identity, write only the
target, and read it back for hash comparison. This manifest and image do not
establish the card's content provenance or the current state of the Replica 1
Plus.
