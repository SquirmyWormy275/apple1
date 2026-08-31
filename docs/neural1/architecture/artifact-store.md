# Artifact store

Artifacts are addressed by SHA-256 and written atomically under
`sha256/XX/DIGEST`. Records include size, media type, and one of `canonical`,
`derived`, `cache`, or `discardable`. Canonical evidence is never automatically
deleted. This intentionally simple filesystem design can be indexed by SQLite
later without changing artifact identity.
