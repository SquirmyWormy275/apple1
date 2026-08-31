# Apple1-Slideshow heritage artwork reference

This source record pins the Apple-1 ASCII-art slideshow repository used as the
heritage visual reference for this project. It is a provenance record, not a
license grant and not permission to redistribute upstream artwork.

## Source identity

- **Project:** `Apple1-Slideshow`
- **Author:** David Schmenk (`dschmenk`)
- **Upstream repository:** https://github.com/dschmenk/Apple1-Slideshow
- **Upstream branch:** `master`
- **Pinned commit:** `d436e3b088f94919f135e48af6303295058b3d51`
- **Pinned commit date:** 2014-12-04T19:33:36Z
- **Retrieved/verified for this project:** 2026-08-30

The upstream README describes the project as an "ASCII art slideshow for Apple
1 (as seen on most Apple 1 auctions)." It documents a 40 x 23 pixel source-art
workflow converted to RLE for Apple-1 display, and states that a slideshow
binary of 3456 bytes or less can run on a minimal 4K Apple-1.

## Heritage assets of interest

The pinned upstream tree includes, among other files:

- `WozJobsApple-I-lo.pbm` — Steve Wozniak / Steve Jobs / Apple-1 composite
- `woz-lo.pbm` and `woz.rle` — Steve Wozniak portrait
- `jobs-lo.pbm` and `jobs.rle` — Steve Jobs portrait
- `apple-logo-lo.pbm` and `apple-logo.rle` — Apple logo artwork
- `apple-logo-stripe-lo.pbm` and `apple-logo-striped.rle` — striped Apple logo artwork
- `slideshow.a65` — Apple-1 slideshow program
- `pbmtorle.c` / `dumprle.c` — artwork conversion / inspection utilities

The filenames identify the upstream assets; this repository must not claim
original authorship of them or of derivatives based on them.

## License and redistribution status

At the pinned revision, this review found **no `LICENSE` file** and no license or
permission text through the indexed repository search. Therefore:

- public availability on GitHub must **not** be treated as a license;
- the exact upstream artwork must not be vendored into a distributable release
  until permission or applicable license terms are established;
- attribution is mandatory even if separate permission is later obtained;
- a derivative must be labeled as a derivative and identify the upstream asset
  used as its source;
- if license/permission cannot be established, create original 40 x 23 artwork
  from separately cleared source material rather than redistributing the
  upstream image files.

## Required attribution format

For an unmodified upstream asset, use at minimum:

> Source: David Schmenk, *Apple1-Slideshow*, `<asset filename>`, commit
> `d436e3b088f94919f135e48af6303295058b3d51`, retrieved 2026-08-30,
> https://github.com/dschmenk/Apple1-Slideshow. License/redistribution status
> must be documented separately.

For a derivative, use at minimum:

> Derived from: David Schmenk, *Apple1-Slideshow*, `<source asset filename>`,
> commit `d436e3b088f94919f135e48af6303295058b3d51`, retrieved 2026-08-30,
> https://github.com/dschmenk/Apple1-Slideshow. Changes: `<describe changes>`.
> License/redistribution status must be documented separately.

Any README, Wiki page, article, screenshot set, video description, generated
asset catalog, or machine-facing heritage-art package that uses or derives from
this source must carry an adjacent attribution or an unambiguous source key
that resolves to this record.

## Reproducible upstream checkout

When a network-enabled development host is used, obtain the exact reviewed
revision with:

```bash
git clone https://github.com/dschmenk/Apple1-Slideshow.git external/Apple1-Slideshow
git -C external/Apple1-Slideshow checkout d436e3b088f94919f135e48af6303295058b3d51
git -C external/Apple1-Slideshow rev-parse HEAD
```

The final command must print:

```text
d436e3b088f94919f135e48af6303295058b3d51
```

Do not substitute a later upstream revision without updating this provenance
record and rechecking the license/permission status.
