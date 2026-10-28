# Original CF-card software

All six original files are available individually under [`files/`](files/).
They were extracted from the verified original Lexar card image. Their bytes,
ProDOS types, load addresses, dates and directory entries are recorded in the
[extraction manifest](EXTRACTED-FILES.json).

| Original card path | Type | Aux/load field | Bytes | Preserved download |
|---|---|---|---:|---|
| `UTILITIES/BASIC` | BIN `$06` | `$E000` | 4,096 | [BASIC](files/UTILITIES/BASIC%2306e000) |
| `UTILITIES/CFFAROMV1.1.BIN` | BIN `$06` | `$2000` | 8,160 | [CFFA ROM image](files/UTILITIES/CFFAROMV1.1.BIN%23062000) |
| `UTILITIES/FLASHERV1.1.BIN` | BIN `$06` | `$1000` | 704 | [Flasher](files/UTILITIES/FLASHERV1.1.BIN%23061000) |
| `UTILITIES/UPDATERV1.1.BIN` | BIN `$06` | `$0E00` | 12,768 | [Updater](files/UTILITIES/UPDATERV1.1.BIN%23060e00) |
| `GAMES/LUNAR` | BIN `$06` | `$0300` | 5,817 | [Lunar](files/GAMES/LUNAR%23060300) |
| `GAMES/STARTREK` | BA1 `$F1` | `$0300` | 3,840 | [Star Trek](files/GAMES/STARTREK%23f10300) |

The `#ttaaaa` suffix is CiderPress NAPS metadata: the original ProDOS file type
and auxiliary/load address. It is not part of the original on-card name. Keep
it when importing these extracted files with CiderPress. The JSON manifest also
retains the original directory bytes and timestamps, which Git file dates do
not preserve.

For the BA1 Star Trek file, `$0300` is the recorded auxiliary field, not a
binary execution address. CFFA1 restores BA1 files as BASIC state rather than
using the ordinary binary load-address prompt.

These are original card artifacts, not newly authored project software. Their
presence establishes the captured bytes; it does not establish authorship,
licensing, compatibility with other machines, or permission to redistribute
them as original work. Maintenance files are preserved; none was executed
during the educational card installation.

## Complete original image

The authoritative sector-for-sector baseline remains unchanged at
[`preservation/cf-card/2026-08-28/`](../../preservation/cf-card/2026-08-28/).
It includes filesystem structure, sparse regions and the rest of the card,
which an extracted-file set cannot replace.

- Capacity: **128,974,848 bytes**.
- SHA-256: `5c98a3bb8c77e4155167a1c8df353ae07697f57c939de9196b838ecf097ad836`.
- Storage: Git LFS. A normal checkout may contain its small LFS pointer until
  hydrated; the six individual files above require no LFS.

On October 28, the original image was downloaded again from GitHub's LFS media
URL and its complete size and SHA-256 matched the baseline. The original card
files were also unchanged in the verified installed-card readback.

[Installed-edition audit](../AUDIT-2026-10-27.md) ·
[Ready-built content packages](../releases/README.md)
