# Read-only support bundles

`tools/support_bundle.py` gathers already-recorded evidence into a portable zip
file. It does not enumerate, configure, open, lock, or transmit to a serial
device. It copies only paths named on its command line and includes a manifest
with each copied file's SHA-256 and size. Filenames must be unique, and the
destination archive cannot also be supplied as evidence.

Run it from the repository root after a capture has already stopped:

```powershell
python .\tools\support_bundle.py .\out\open-event-support.zip `
  .\docs\captures\2026-08-27-open-no-transmit-retry1.jsonl `
  .\docs\captures\2026-08-27-open-no-transmit-retry1.metadata.json
```

Review the selected paths before sharing a bundle. Include raw captures,
metadata, an instrument export, and the relevant test-card version; exclude
credentials, SSH configuration, model files, general Pi logs, and unrelated
personal photographs unless a separately reviewed support request requires
them.

The archive's `manifest.json` is a transfer-integrity record, not a claim that
the captured observation was correct or repeatable.
