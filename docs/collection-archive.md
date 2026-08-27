# Collection archive manifest

`tools/archive_manifest.py` creates a SHA-256 inventory from only the files
explicitly named by the operator. It does not crawl drives, copy artifacts, or
publish anything.

```powershell
python .\tools\archive_manifest.py .\out\manuals-manifest.json `
  --category manual `
  "..\Manuals and Documentation\Replica_One_Plus_Manual_-_June_2014.pdf"
```

Run separate manifests for manuals, photographs, source archives, test
captures, and packaging records. Beside each manifest, retain a human note
covering original location, source/provenance, access permission, date, and
whether the file is an original, a derivative, or a working copy.

The hashes establish file identity at capture time. They do not prove a manual,
photo, or candidate source describes the installed firmware or current board.
