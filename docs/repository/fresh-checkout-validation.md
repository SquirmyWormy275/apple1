# Fresh-checkout validation

**Branch:** `refactor/repository-architecture-v1`

**Status:** IMPLEMENTATION GATE PASSED; FINAL DOCUMENTATION HEAD MUST REPRODUCE THE SAME GREEN CI BEFORE MERGE

## Validation model

GitHub Actions checks out the pull-request merge ref into a clean runner using `actions/checkout`, installs only declared project dependencies, and runs the repository acceptance pipeline. This provides a clean/fresh-checkout test of the branch against the current PR base rather than relying on a developer's pre-existing environment.

The first complete green implementation gate was branch commit:

```text
7aed69c71e7ed987700c876d6d46bacfcd71f69f
```

GitHub Actions run:

```text
33358655553
```

That run checked PR merge ref `4f6b8b0b437225891611814889ed3a70abf37729`, combining the branch commit above with starting/current PR base `3c06a857b93409e4c681e1d794fa757bf66db3cc`.

Documentation-only closure commits after this evidence are required to pass the same workflow before merge. No claim in this document overrides the live CI state.

## Commands and exact results

```bash
python -m pip install -e '.[dev]'
```

**PASS.** Editable wheel built and installed successfully under CPython 3.12.14 on Ubuntu 24.04 GitHub Actions.

```bash
ruff check neural1 tools/neural1_validate.py tests/test_neural1*.py
```

**PASS:** `All checks passed!`

```bash
mypy neural1
```

**PASS:** `Success: no issues found in 34 source files`

```bash
python -m pytest -q
```

**PASS:** `99 passed in 2.52s`

```bash
python tools/neural1_validate.py .
```

**PASS:**

```json
{
  "errors": [],
  "valid": true
}
```

The repository validator includes schema checks, required structural anchors, all first-party relative Markdown links, historical-promotion safety policy, ASCII constraints, and art provenance.

```bash
python -m neural1.demos --out out/neural1-demo
```

**PASS:**

```json
{"run_id":"N1R-5331C71E7C841101","serial_opened":false,"summary":"out/neural1-demo/summary.json"}
```

The CI then independently re-opened the generated summary JSON and asserted:

```python
assert data["serial_opened"] is False
```

**PASS.** No physical serial path is used by this deterministic demo.

Finally:

```bash
git diff --exit-code
```

**PASS.** Validation and demo generation produced no tracked-file changes.

## Acceptance assertions

- [x] Fresh checkout installs using declared project dependencies.
- [x] Ruff passes.
- [x] mypy passes on 34 source files.
- [x] Full pytest passes: 99 tests.
- [x] Repository/schema/link/art/provenance validation passes with zero errors.
- [x] Deterministic demo completes.
- [x] Demo reports `serial_opened=false`.
- [x] An independent CI assertion rechecks `serial_opened=false` from the generated summary.
- [x] No physical serial command is invoked by the acceptance workflow.
- [x] No Replica access or transmission occurs in the acceptance workflow.
- [x] No firmware load, EEPROM/CFFA1/GPIO/wiring/jumper/solder/camera/physical qualification action occurs.
- [x] Validation leaves the tracked tree unchanged.
- [x] No dependency on a prior developer checkout is required by the workflow.
- [x] The required frozen archive ref was independently verified during archaeology; it must be rechecked immediately before and after merge.

## Negative/failed-gate history

Two early CI failures were retained in branch/Actions history rather than hidden:

1. Ruff initially found only import-layout formatting in the new validator/test file; the exact Ruff-proposed formatting was applied.
2. The first run to reach pytest found one incorrect new structural assumption: the preserved CF snapshot contains `MANIFEST.md`, not `README.md`. The validator was corrected to require the real preservation manifest rather than fabricating a file to satisfy the check.

After those corrections, the complete acceptance pipeline passed. No failed run reached or invoked a physical serial action.

## Physical interpretation

This validation proves that the repository's deterministic/off-device acceptance path completes without opening serial hardware and that the generated demo records `serial_opened=false`. It does **not** prove the physical Replica, serial transport, firmware, CFFA1, or logic-analyzer path works. The historical FT232R STOP remains controlling physical evidence until a separately authorized measurement procedure supersedes it.
