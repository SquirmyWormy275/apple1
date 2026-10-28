# Ready-built CF content

These are retained binaries and exact-source archives, alongside the build
tools. Downloading a package does not require rebuilding the readers.

| Edition | Download | Contents and verification |
|---|---|---|
| October 27, 2026 installed snapshot | [APPLE1-CF-CONTENT-2026-10-27.zip](APPLE1-CF-CONTENT-2026-10-27.zip) | Six original files, 518 additions, build manifest and installation/readback receipts. Source revision `fcefe714a94b130aba090fb188740f6fbf9638ed`. |

[SHA-256 checksums](SHA256SUMS) · [Installation audit](../AUDIT-2026-10-27.md) ·
[Reading and reconstruction guide](../DEPLOYMENT.md)

## Inside the package

- `original/`: all six original programs with their ProDOS metadata in NAPS
  filename suffixes, also [browsable individually](../original/README.md).
- `overlay/`: the exact 518 added card files. This includes 514 reader binaries,
  two RAM-only demonstration binaries, `HOSTSRC/SOURCE.ZIP` and `BUILD.JSON`.
- `metadata/`: original-file inventory, build hashes, public deployment receipt
  and complete-readback audit.

`HOSTSRC/SOURCE.ZIP` retains the original text, code and images at the deployed
build revision. Subsequent source/documentation work does not silently rewrite
this retained snapshot. The ZIP is a content package, not a raw disk image and
not a directory tree to copy onto a FAT-formatted card. The original ProDOS
image remains the separately preserved reconstruction baseline.

The October 27 snapshot records a verified storage installation and emulator
checks. Later teaching/reader revisions need their own dated build and card
verification before they replace it. Physical Replica display/keyboard
acceptance remains a separate observation.
