# Logic-trace packet validation

`tools/trace_packet.py` validates packet structure and local-file integrity without arming an analyzer, opening a serial device, or collecting a trace. Experimental result (`PASS`, `STOP`, or `INCONCLUSIVE`) is independent of execution, archival completeness, and portability.

Version 2 packets support two display-evidence modes:

- `local`: every media path must be relative, remain within the packet, name a non-empty file, and match its SHA-256. A complete packet uses `COMPLETE_LOCAL_MEDIA` and `SELF_CONTAINED`.
- `external_hash_identified`: each artifact must record its filename, lowercase SHA-256, custody, absence reason, direct-inspection attribution and method, and observation summary. A non-empty local custody record is required. A complete packet uses `COMPLETE_WITH_EXTERNAL_MEDIA` and `NOT_SELF_CONTAINED_MEDIA`.

The validator checks the structure and internal consistency of an external-media record; it does not claim to verify bytes it cannot access. Bare placeholders such as `UNAVAILABLE`, `MISSING`, `NONE`, and `N/A` are invalid. Legacy `display_video` packets remain accepted as mappings, but path-aware CLI validation requires the value to be a safe relative path naming a real, non-empty local file.

The packet must also record `physical_changes: none`, analyzer model/input rating, safely identified channels, native raw captures, the exclusive owner's JSONL, and either a safely evidenced `RESn` channel or a substantive `resn_unavailable_reason`.

```powershell
python .\tools\trace_packet.py .\docs\captures\YYYY-MM-DD-ft232r-open-analyzer\metadata.json
```

External media remain outside local `SHA256SUMS`; their hashes belong in the external-media manifest. When verified copies later enter the packet, add them to the local manifest and update custody/portability status without changing the historical experiment result.
