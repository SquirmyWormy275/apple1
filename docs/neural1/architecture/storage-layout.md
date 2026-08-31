# NEURAL1 dedicated SSD layout

The dedicated SSD is the permanent bulk-storage layer for NEURAL1. The layout is intentionally separate from the repository checkout and from the user's general-purpose backup disks.

```text
<NEURAL1-SSD>/
├── .neural1-ssd.json
├── preservation/
│   └── pi-images/
├── models/
│   ├── canonical/
│   ├── candidates/
│   └── cache/
├── datasets/
├── campaigns/
├── runs/
├── checkpoints/
├── research/
├── meta/
├── exports/
├── logs/
└── manifests/
```

The `.neural1-ssd.json` marker is a safety control, not a device-discovery mechanism. An operator must positively identify and mount the intended SSD before creating the marker. The storage tool never formats or partitions disks.

The migration engine refuses to target a directory unless it contains a marker whose role is exactly `NEURAL1_DEDICATED_SSD`. This is intended to prevent a general backup drive or arbitrary mount from becoming an accidental destination.

## Directory roles

- `preservation/pi-images/`: verified raw Pi media images and their checksums/metadata.
- `models/canonical/`: retained model artifacts selected for reproducible use.
- `models/candidates/`: models under evaluation.
- `models/cache/`: reproducible/rebuildable persistent model cache data.
- `datasets/`: curated datasets used by NEURAL1.
- `campaigns/`: campaign definitions and campaign-scoped retained state.
- `runs/`: retained run outputs that are not already packaged elsewhere.
- `checkpoints/`: resumable checkpoints.
- `research/`: research material that belongs in bulk storage rather than Git.
- `meta/`: META/1 bulk state and exports.
- `exports/`: generated exports intended for downstream use.
- `logs/`: operational logs that are intentionally retained.
- `manifests/`: SSD identity, migration receipts, verification records, and storage inventories.

Repository source, small canonical configs, schemas, documentation, and source-controlled evidence remain in Git. The SSD is not a substitute for repository history.
