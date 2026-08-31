# Pi image software archaeology — 2026-08-30

Status: **READ-ONLY BASELINE COMPLETE; DETAILED INVENTORY RETAINED LOCALLY**

This report records durable, sanitized findings derived from the preserved raw
image identified by the [preservation record](pi-image-2026-08-30.md). The
image was mapped through a kernel-enforced read-only loop device. The ext4
filesystem was mounted with journal recovery disabled. No image-resident
program was executed, no filesystem repair was attempted, and the physical
card and Apple-facing hardware were not used.

## Partition and filesystem layout

The repository image inspector reproduced the preserved identity without a
discrepancy. The MBR contains two non-bootable partitions:

| Partition | Type | Start LBA | Sectors | Byte offset | Byte length | Filesystem |
|---|---:|---:|---:|---:|---:|---|
| 1 | `0x0c` | 16,384 | 1,048,576 | 8,388,608 | 536,870,912 | FAT32, `bootfs` |
| 2 | `0x83` | 1,064,960 | 248,672,256 | 545,259,520 | 127,320,195,072 | ext4, `rootfs` |

`fstab` addresses both filesystems through the preserved disk signature's
partition identifiers. The boot configuration selects 64-bit operation. The
local evidence bundle retains exact filesystem UUIDs, boot-file hashes, and
the full boot inventory; those machine-level details are not duplicated here.

The ext4 filesystem reported 125,335,547,904 bytes of mounted capacity,
16,874,008,576 bytes used, and 103,332,450,304 bytes available. A read-only
`du` traversal accounted for 6,654,943,232 allocated bytes. The
10,219,065,344-byte difference remains unexplained. It was not treated as
reclaimable space because doing so would require filesystem analysis beyond
this mounted software inventory and might require recovery or repair.

## Operating-system and runtime baseline

- Debian GNU/Linux 13 (`trixie`), recorded full Debian version 13.6.
- AArch64/arm64 userspace, confirmed from ELF headers and package architecture.
- Python 3.13.5; 643 installed Debian package records were collected with exact
  versions and architectures in the local evidence bundle.
- 35 enabled systemd units were collected. The project-relevant enabled unit is
  the local Ollama service; no NEURAL1-specific unit or timer exists.
- No NEURAL1-related cron entry, desktop autostart entry, or shell startup hook
  was found. Shell PATH customization is limited to conventional per-user
  `bin` and `.local/bin` additions.

## NEURAL1 and local-inference findings

The image contains no NEURAL1 installation, Apple1 Git checkout, campaign,
run, snapshot, checkpoint, lineage, META/1, dataset, export, model registry, or
generated NEURAL1 output tree. A small non-Git serial-recovery evidence
workspace exists, with two tools, two capture manifests, and a Python 3.13.5
virtual environment containing pip 25.1.1 and pyserial 3.5. It is preservation
material of unconfirmed authority, not a canonical project checkout.

Ollama is installed under `/usr/local`, enabled at boot, and configured with
`OLLAMA_KEEP_ALIVE=-1`. Its runtime libraries occupy about 2.20 GB and include
libllama/libggml plus CUDA 12 and CUDA 13 libraries. The Ollama service
account's default storage root is empty: no model manifests, blobs, GGUF/GGML,
Hugging Face cache, or other recognized model-weight files were found. No
standalone llama.cpp checkout was found. Ollama's exact release remains unknown
because the preserved executable was deliberately not run.

## Storage and recovery implications

There is no current bulk model, dataset, checkpoint, or experiment tree in the
image to relocate. Before models are installed on a recovered or commissioned
Pi environment, configure model and cache storage against the future dedicated
NEURAL1 SSD; otherwise Ollama will use internal root storage. The small
serial-recovery manifests are preservation candidates only after provenance,
duplication, and sensitivity review. The virtual environment and pip cache are
reproducible/cache material rather than canonical migration payloads.

The raw image and host-local baseline remain temporary internal preservation
data pending the dedicated SSD. Migration must follow the required verified
copy lifecycle in [SSD commissioning](../operations/ssd-commissioning.md). The
general backup drive is not an eligible destination.

## Evidence boundaries and gaps

The local evidence package contains the raw image-inspection JSON, rootfs BOM,
package and service inventories, filesystem/boot hashes, capacity analysis,
path classifications, and SHA-256 manifest. Credentials, private keys, SSH
material, browser profiles, cookies, shell history, and capture contents were
excluded. Deleted or unallocated-content recovery was outside scope. The
filesystem allocation difference and exact Ollama version remain explicit
unknowns.

