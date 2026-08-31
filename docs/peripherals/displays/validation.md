# Display-history validation record

**Validation date:** 2026-08-30

This record covers the Apple-1 display/Sanyo research packet, its H06 Field
Library lesson, and the repository checks available in the validation
environment.

## Documentation checks

| Check | Result |
|---|---|
| Relative Markdown links across reconstructed repository | **PASS** — 265 Markdown files checked; no broken relative links found. |
| Display-dossier source IDs | **PASS** — 28 IDs defined, 27 referenced, 0 missing references. The unused ID is retained as a source record. |
| `git diff --check` | **PASS** |
| H06 curriculum review gate | **PASS** — see `../../field-library/H06-the-monitor-that-wasnt/REVIEW.md`. |
| Image/document rights review | **PASS WITH RESTRICTIONS** — only reviewed public-domain/CC images are embedded; uncleared Sanyo, museum, auction, Registry and seller images remain links only. |
| Unresolved historical claims | **PASS AS OPEN ITEMS** — they remain explicitly `UNVERIFIED`/open in `open-research.md` rather than being inferred into facts. |

## Test-suite check

A full `python -m pytest tests -q` run was attempted. Test collection is blocked
in this validation environment because `py65` is not installed; the environment
also lacks outbound package-network access, so the missing dependency could not
be installed for this run.

The test files that do not depend on `py65` and are unrelated to the existing
firmware-source provenance audit were run explicitly:

```text
29 passed in 0.66s
```

The existing firmware-source audit was also run separately:

```text
1 failed, 1 passed
```

Its failure is a pre-existing provenance/hash mismatch under
`firmware/vendor/110REV03/`; the display-history changes do not touch those
files. The live repository blob IDs for the affected vendor source and
`provenance.json` were checked against the validation checkout and match, so the
mismatch is present independently of this documentation update. No firmware or
provenance file was altered to hide that failure.

## Rights implementation

The visual chronology uses remote embeds for:

- the October 1976 Apple-1 advertisement — Wikimedia Commons records U.S.
  public-domain status;
- the December 1977 Apple II advertisement pages — Wikimedia Commons records
  U.S. public-domain status;
- the 2023 Apple-1 Computer History Museum photograph by The wub — CC BY-SA 4.0,
  with creator/source/license recorded.

The repository does **not** copy the eBay seller photographs, RR Auction
VM-4209 photographs, Smithsonian VM-4092/VM-4209 photographs, Sotheby's,
Christie's, Digibarn/Getty, Apple-1 Registry images, or the Sanyo service-manual
PDF because redistribution permission was not established for those materials.

## Scope

This validation does not claim that all pre-existing Field Library packets have
passed their curriculum review gate. H06 has been reviewed separately; the
older library-wide review item remains open as V-36.
