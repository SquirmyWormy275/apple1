# Historical plans

Plans in this directory preserve design intent at the time they were written. A plan's original front matter is **not current execution authority** after later evidence changes the safety state.

## Current status

| Plan | Original readiness | Current status | Controlling evidence |
|---|---|---|---|
| [`2026-08-25-1324-fix-replica1-propeller-serial-plan.md`](2026-08-25-1324-fix-replica1-propeller-serial-plan.md) | `implementation-ready` on 2026-08-25 | **SUPERSEDED AS EXECUTION AUTHORITY / PHYSICAL WORK BLOCKED** | The later no-transmit FT232R open produced a STOP: opening the host serial stack was sufficient to disturb the Replica display and physical Reset was required. See [`../troubleshooting.md`](../troubleshooting.md), [`../captures/2026-08-27-open-no-transmit-retry1.metadata.json`](../captures/2026-08-27-open-no-transmit-retry1.metadata.json), and the prepared-but-not-executed [`../captures/logic-analyzer-open-event-test-card.md`](../captures/logic-analyzer-open-event-test-card.md). |

The original plan remains unedited as a historical planning artifact. Do not resume its RAM-load, EEPROM, wiring, CA2, or repeated serial-open stages from the old `artifact_readiness` field.

Repository/off-device work may continue. Any future physical step requires a separate, current, explicitly approved evidence gate.
