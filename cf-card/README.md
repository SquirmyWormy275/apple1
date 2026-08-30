# Apple1 CF-card source control

This directory is the **host-side control plane** for material associated with
the project's CF card. It is deliberately separate from both the preserved raw
card image and the learner-facing source documents.

It does **not** define the CFFA1 file system, on-card directory names, boot
mechanism, menu implementation, or a physical write procedure.

## The model: baseline + approved overlays

```text
IMMUTABLE ORIGINAL BASELINE
preservation/cf-card/2026-08-28/
        |
        |  never edited in place
        V
FUTURE WORKING COPY / BUILD
        +
APPROVED CONTENT OVERLAYS
        |
        V
HOST-SIDE STAGING OUTPUT
```

### 1. Original baseline

The original Lexar CF card has a verified sector-for-sector image under
`preservation/cf-card/2026-08-28/`. That image is preservation evidence and is
never used as a scratch file. See [`original/README.md`](original/README.md).

### 2. Field Library

The authoritative educational source remains `docs/field-library/`. The new
SP01 packet contains a `card/` subtree of display-native 40x24 ASCII screens and
is currently the first item marked for approved staging. See
[`field-library/README.md`](field-library/README.md).

The pre-existing forty lesson packets remain cataloged as candidates until their
review gates and eventual card-facing formatting are resolved. They are **not**
silently exported just because they exist in the repository.

### 3. Software

`software/ram-only/` remains a separate RAM-only candidate library with no
live-run authority. It is indexed here but not included in the approved overlay
by default. See [`software/README.md`](software/README.md).

### 4. Machine-readable manifest

[`manifests/current.json`](manifests/current.json) is the authoritative source
registry for host-side staging. Each source has an explicit status and an
`include_in_default_export` flag.

### 5. Export

`tools/export_cf_card_sources.py` reads the manifest and creates a **host-side
staging tree only**. It does not mount, format, image, or write a CF card. The
default output is `out/cf-card-staging/`, which is ignored by Git.

The exporter validates any source declared as `ascii-40x24` before copying it.
Use `--include-baseline-image` only on a clone where Git LFS has hydrated the
original image; the exporter verifies its size and SHA-256 before copying it.

## Rule for future work

When new material is intended for the card:

1. keep the authoritative source in its normal repository location;
2. add it to `manifests/current.json` with an explicit status;
3. do not set `include_in_default_export` until it is approved;
4. never modify the preserved original image in place;
5. use generated staging/build output rather than hand-copying an ad hoc mix of
   repository files.

This keeps preservation, authored content, and future build output distinct.
