# Pi recovery runbook

This runbook defines recovery from a failed or corrupted Pi microSD using a previously verified raw image. It is a recovery procedure, not authorization to overwrite any currently functioning card.

## Preconditions

- A replacement target card has been positively identified.
- The preserved image SHA-256 matches its trusted preservation record/local checksum.
- The target device is not the Omarchy system disk, the general backup drive, or the dedicated NEURAL1 SSD.
- Any required physical Apple1/Replica qualification remains separately blocked unless explicitly authorized.

## Recovery sequence

1. Re-hash the preserved image and compare it to the trusted checksum.
2. Record the replacement card identity and capacity.
3. Confirm the target is disposable/recoverable and contains no needed data.
4. Write the raw image to the replacement card with an operator-visible imaging tool.
5. Flush writes and re-read the written media independently.
6. Compare the restored media layout with the image partition table.
7. Where practical, hash the restored byte range corresponding to the image and compare it to the source image.
8. Mount restored filesystems read-only first and run the [Pi image baseline](pi-image-baseline.md) checks.
9. Only after media-level verification should the Pi be booted from the replacement card.
10. Validate the Pi software/runtime environment before any Apple-facing physical interaction.

## Physical boundary

Restoring or booting a Pi image does not authorize FT232R serial open/transmit, EEPROM or firmware writes, CFFA1 writes, GPIO manipulation, wiring/jumper/solder changes, or physical Replica qualification. Those remain governed by the project's physical safety gates.
