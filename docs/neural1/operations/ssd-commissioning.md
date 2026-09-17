# Dedicated SSD commissioning and migration

This procedure executes the storage lifecycle defined in [storage-lifecycle.md](../architecture/storage-lifecycle.md) and the target layout defined in [storage-layout.md](../architecture/storage-layout.md).

## Before the SSD exists

Keep temporary NEURAL1 bulk data isolated on internal Omarchy storage. Mark the temporary root with:

```bash
neural1-storage init-temporary-root /path/to/temporary/NEURAL1
```

The user's 1.8 TB Seagate Portable Drive remains protected general backup/recovery storage and is not an SSD substitute.

## Commission the dedicated SSD

Formatting/partitioning is outside the repository tool. Positively identify, prepare, and mount the new SSD first. Then initialize only the mounted NEURAL1 storage root:

```bash
neural1-storage init-ssd-root /mnt/neural1-ssd \
  --volume-id <operator-recorded-id> \
  --confirm-role NEURAL1_DEDICATED_SSD
```

This writes a role marker and creates the canonical directory layout. It does not format or repartition a device.

## Plan

Create the migration manifest in a small state location outside the temporary tree:

```bash
neural1-storage plan-migration /path/to/temporary/NEURAL1 /mnt/neural1-ssd \
  --manifest ~/.local/state/neural1/storage-migration.json
```

Planning hashes every regular payload file. Symlinks are not migrated as payload files. The manifest records source and destination paths separately so the existing pre-SSD layout can be normalized into the canonical SSD layout. In particular, the current temporary `pi-images/` tree maps to `preservation/pi-images/`, and the temporary root `README.md` maps to `manifests/temporary-storage-README.md`. Any destination-path collision aborts planning.

Review the generated manifest before copying. It is the exact allowlist for both copying and later source deletion.

## Copy

```bash
neural1-storage copy-migration ~/.local/state/neural1/storage-migration.json
```

Existing regular destination files are accepted only when byte size and SHA-256
already match. Symlinks and conflicting destination files abort the operation.
Each new file is copied to an exclusively created `.neural1-copy-*.partial`
file on the destination filesystem, flushed, and verified before atomic
no-overwrite publication. A retry reuses verified completed files and restarts
incomplete files from the beginning; this is not byte-offset resume. Normal
exceptions remove the attempt's own partial. A hard kill can leave a partial,
which is preserved for inspection and never mistaken for a complete payload.
The copy requires space for the full next file plus a 64 MiB reserve.

An installed application must additionally call
`neural1.deployment.verify_storage` before workloads and bulk-write stages.
Unlike a role marker alone, this checks the actual mountpoint, expected
filesystem UUID, writable mount, free space, and resolved write paths. Its role
marker's `volume_id` must equal the filesystem UUID. It refuses a plain directory
when the SSD is absent, symlink escapes, and nested write mounts. This check
creates no directories and cannot silently fall back to microSD storage.

## Verify

```bash
neural1-storage verify-migration ~/.local/state/neural1/storage-migration.json
```

Verification re-hashes both source and destination copies. Do not proceed to deletion unless this succeeds and NEURAL1 application paths/configuration have also been validated against the SSD-backed layout.

## Finalize and reclaim internal storage

After application-path validation and explicit operator confirmation:

```bash
neural1-storage finalize-migration ~/.local/state/neural1/storage-migration.json \
  --confirm-delete DELETE_VERIFIED_TEMPORARY_NEURAL1_COPY
```

The finalizer re-runs byte-size/SHA-256 verification immediately before deletion. It deletes only source files enumerated by the verified migration manifest and rejects manifest paths that escape either storage root. It writes the migration receipt to `manifests/storage-migration-verified.json` on the SSD before deleting the source payload.

If no unexpected files were added to the temporary root, the temporary role marker and empty source directories are also removed. If unexpected residual paths exist, they are preserved and recorded rather than deleted implicitly.

Required lifecycle:

**copy → hash/verify → validate paths → confirm SSD copy → delete temporary internal copy → verify reclaimed space**
