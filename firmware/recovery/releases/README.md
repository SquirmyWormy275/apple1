# Ready-built recovery bundle

[Download APPLE1-RECOVERY-110REV03-2026-10-28.zip](APPLE1-RECOVERY-110REV03-2026-10-28.zip)
· [ZIP SHA-256](SHA256SUMS) · [Package guide](../110REV03-2026-10-28/README.md)

Extract into a new directory and start with `firmware/recovery/110REV03-2026-10-28/README.md`.
The bundle includes the images, laptop compiler/loader, pinned source archives,
original vendor source, verification/rebuild tool, loading procedure and repair
context/photos. It requires no source download to rebuild. Linux build tools
and Python are system prerequisites.

The firmware is built and checked **off-device**. Hardware recovery/acceptance
remains pending. The bundle does not execute an uploader automatically; the
original EEPROM stays preserved, and only a compatible spare is a persistent
recovery target. The installed CF card is unchanged.
