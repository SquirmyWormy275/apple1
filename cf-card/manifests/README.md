# CF-card manifests

`current.json` is the canonical host-side source registry.

The manifest distinguishes:

- the immutable original-card baseline;
- approved card-facing overlays;
- candidate sources that must **not** be exported by default.

`staging_path` values describe the generated **host-side staging tree only**.
They are not claims about the eventual CFFA1 filesystem or on-card names.
