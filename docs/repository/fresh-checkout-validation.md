# Fresh-checkout validation

**Branch:** `refactor/repository-architecture-v1`

**Status:** PENDING FINAL CI / ACCEPTANCE GATE

This record is intentionally created before final validation and updated with exact results only after the final branch commit is available. Do not read `PENDING` as a pass.

## Required commands

A completely fresh checkout must run:

```bash
python -m pip install -e '.[dev]'
ruff check neural1 tools/neural1_validate.py tests/test_neural1*.py
mypy neural1
python -m pytest -q
python tools/neural1_validate.py .
python -m neural1.demos --out out/neural1-demo
```

Additional repository-structure and safety assertions introduced by this migration must also run through the normal test/validator/CI path.

## Acceptance assertions

- [ ] Fresh checkout starts from the final branch commit.
- [ ] Editable install succeeds using declared project dependencies.
- [ ] Ruff passes.
- [ ] mypy passes.
- [ ] Full pytest passes; exact test count recorded below.
- [ ] Repository/schema/link/art/provenance validation passes.
- [ ] Deterministic demo completes.
- [ ] Demo reports `serial_opened=false`.
- [ ] No physical serial device is opened.
- [ ] No Replica access or transmission occurs.
- [ ] No firmware is loaded or compiled for physical deployment.
- [ ] No EEPROM/CFFA1/GPIO/wiring/jumper/solder/camera action occurs.
- [ ] Validation does not modify tracked files.
- [ ] No hidden dependency on the prior working checkout is observed.
- [ ] Frozen archive branch still points to `f1ac1958c2e8906510fc963422ed1801f0231b1b`.

## Final evidence

To be filled from the final branch CI/fresh-checkout run:

| Check | Exact result |
|---|---|
| Final branch SHA | `PENDING` |
| Python install | `PENDING` |
| Ruff | `PENDING` |
| mypy | `PENDING` |
| pytest | `PENDING` |
| repository validator | `PENDING` |
| deterministic demo | `PENDING` |
| `serial_opened` | `PENDING` |
| tracked tree after validation | `PENDING` |
| archive ref | `PENDING` |

## Interpretation

GitHub Actions uses `actions/checkout` on the proposed branch, so a green CI run is fresh-checkout evidence for the commands actually encoded in `.github/workflows/ci.yml`. Any acceptance assertion not directly covered by those commands must be separately evidenced or added to CI before this record can be marked PASS.
