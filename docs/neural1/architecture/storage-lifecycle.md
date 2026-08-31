# NEURAL1 storage lifecycle

## Current temporary layout

Until a dedicated NEURAL1 SSD is purchased and commissioned, the Omarchy
workstation's internal storage is a temporary holding location for Pi
preservation images and explicitly approved NEURAL1 bulk artifacts. Operators
must keep temporary data under one isolated, clearly labeled root and maintain
a local manifest containing sizes, hashes, purpose, and intended destination.

The user's existing 1.8 TB Seagate Portable Drive is protected general backup
and recovery storage. It is not a NEURAL1 primary, model, dataset, experiment,
cache, scratch, or archival volume. Its available capacity does not authorize
NEURAL1 writes or reorganization.

Machine-specific paths, device names, serial numbers, and credentials belong
only in the private local manifest, not in this repository.

## Dedicated SSD commissioning requirement

The future dedicated SSD is the permanent target for NEURAL1 bulk storage,
including Pi images, model files and persistent caches, datasets, campaigns,
runs, snapshots, lineage and provenance, META/1 data, research artifacts,
exports, and other large outputs created before SSD installation.

Migration is a verified copy operation:

1. Copy the temporary data to the SSD, preserving useful directory structure.
2. Compare file sizes and verify SHA-256 for preservation-critical artifacts.
3. Update and validate NEURAL1 paths and configuration against the SSD layout.
4. Run relevant software checks using the SSD-backed paths.
5. Confirm that every destination copy is complete and usable.
6. Only then delete the corresponding temporary internal copy.
7. Verify that internal space was reclaimed and record completion in the local
   storage manifest.

Do not use `mv` as the sole migration mechanism for preservation-critical
material. The required lifecycle is **copy → hash/verify → validate paths →
confirm SSD copy → delete temporary internal copy → verify reclaimed space**.
