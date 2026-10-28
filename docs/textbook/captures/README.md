# Recorded textbook output

Each ID has a raw `.txt` transcript and a readable `.png` render. The manifest
records the reviewed source-file hashes and the retained stdout/image hashes.
The text was actually executed; authored classifications and mock responses
retain their explicit evidence labels.

Run `python -m tools.textbook verify docs/textbook/captures --rerun` from the
checkout root to check source identities, artifact hashes, and exact output.
Image rendering can vary with Pillow and available fonts; verification checks
the retained PNG bytes, while rerun equality compares the actual text output.
Use a new directory with `capture --out ... --images` for another capture set.

[Textbook home](../README.md) · [Coverage and modes](../coverage.md)
