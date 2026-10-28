# Ready-built CF content

These are retained binaries and exact-source archives, alongside the build
tools. Downloading a package does not require rebuilding the readers.

| Edition | Download | Contents and verification |
|---|---|---|
| October 28, 2026 combined build | [APPLE1-CF-CONTENT-2026-10-28.zip](APPLE1-CF-CONTENT-2026-10-28.zip) | All six originals and 380 additions: the reviewed 50-book core, six BA1 programs, 319 supplemental readers and exact-source archive. [Build verification](2026-10-28-build.json). Physical-copy verification is recorded separately. |
| October 27, 2026 installed snapshot | [APPLE1-CF-CONTENT-2026-10-27.zip](APPLE1-CF-CONTENT-2026-10-27.zip) | Six original files, 518 additions, build manifest and installation/readback receipts. Source revision `fcefe714a94b130aba090fb188740f6fbf9638ed`. |

The October 28 combined build is now **installed and fully read back**.
Its separate [physical-copy receipt](../deployments/2026-10-28.json) and
[audit](../AUDIT-2026-10-28.md) record the exact image/readback identity and
preserved originals. The ready-built ZIP above is unchanged from the verified
candidate; the receipt records its completed installation.

[SHA-256 checksums](SHA256SUMS) · [Installation audit](../AUDIT-2026-10-27.md) ·
[Reading and reconstruction guide](../DEPLOYMENT.md)

## Inside the package

The October 28 package contains `original/` with all six preserved files,
`overlay/` with the exact 380 additions, and `metadata/` with the core and
supplement manifests, original inventory and independent byte/runtime checks.
It contains 50 main books, six BA1 programs, 319 supplemental readers, two
RAM demonstrations and the offboard source archive/manifest. The complete
edition represents 3,374 display pages and all 110 captured examples.
Its build receipt does not itself claim a physical installation. The package
bytes remain the same when the separate media-copy receipt is published.

The October 27 historical snapshot contains:

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
checks. Later teaching/reader revisions receive their own dated build and
card-copy verification. Physical Replica display/keyboard acceptance remains
a separate observation.
