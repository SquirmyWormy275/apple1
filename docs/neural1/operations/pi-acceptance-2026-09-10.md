# Native Pi acceptance — 2026-09-10

Status: **RUNNING** a guarded preservation transfer; the installed application is usable. The tested application revision is
`4f06e6d10bcbffca47c0f7554800972555085c78`. This record describes actual
Raspberry Pi 5 Model B Rev 1.1 execution, ARM64, 8 GB RAM. The Apple-1 world
remains **VIRTUAL**. No physical serial commissioning was performed.

The installed normal entry point is `neural1`. It was exercised from a normal
runtime-account login outside the checkout. After the first restart and manual
SSD activation, run `N1-P-601F189D870A1210` produced three genuine responses,
eight accepted Monitor commands and independently checked A output/Monitor
return. Saved META and the ROM export reopened intact.

Both controlled restart attempts lacked SSD enumeration until manual activation.
The operator subsequently clarified that the enclosure must be clicked back on;
the earlier assumption of unattended Pi/SSD restart was not established. Further
reboots, shutdowns and USB power cycling were stopped at the user's direction.
The prepared USB power test never reached its power-changing operation.

A UUID-scoped udev rule now requests the existing guarded Ollama service when
the ext4 SSD appears after boot. The service requires its configured mount and
checks storage identity before writing. Native udev validation and nine focused
installer tests passed. A physical off/on test of the new rule has not been
performed. This rule controls service startup, not enclosure power. The Pi and
SSD are left powered and mounted. Final ordinary-login run
`N1-P-FC1298236505CB0F` passed with three genuine responses, eight accepted
commands and independently checked A/Monitor return. Saved META and the ROM
export reopened. This run peaked at 65.55°C, with zero throttling flags and at
least 4.37 GB available memory. The temporary privileged operator was removed
without stopping the provider or unmounting the SSD.

## Actual family evidence

| Family | Run | Observed result |
|---|---|---|
| 4K MIND | `N1-P-BB49DACBD19E575B` | Three genuine responses, eight accepted Monitor commands, independently checked A output and Monitor return. Cancellation after one committed turn took about 1.28 seconds; same-ID resume preserved the committed prefix and original effective registry. |
| SELFHOST/1 | `N1-P-8F46A3AC87392679` | Three genuine responses and eight accepted commands. Stage-one ingestion, exact rebuild, persistent browsing and dependency export/reopening passed. No later-stage compiler discovery is claimed. |
| RAM REPUBLIC | `N1-P-7BCE70401CD99FD1` | Six responses and 31 accepted commands. Two isolated participants observed actual shared RAM changes. Independent shared-state replay matched; final BRK behavior was a valid negative experiment. |
| 1976 MULTIVERSE | `N1-P-FA6767B745263F82` | Three typed model genomes reached the provenance-aware validator. Their 64K ranges were rejected for the documented 4096-byte RAM bank. Specific feedback and context resets were verified. The source-backed corpus makes bounded structural claims, not invented price or electrical claims. |
| 256-BYTE UNIVERSE | `N1-P-B90E14C4EEF3FC2D` | Eighteen genuine responses and 21 accepted commands. The initial program printed A and returned; later wrong-address deposits overwrote it and left 24 bytes without explicit deposits. The evaluator rejected the 232-byte coverage and independently observed BRK. Meaningful positive and negative controls passed. |

These are bounded instructional or structural starting tasks, not discovery
claims. Model responses were not replaced by canned deposits. Earlier provider
timeouts, malformed JSON, zero-acceptance Monitor output and incorrect Field
Library explanations remain preserved as failed attempts. They are not counted
as qualifying scientific negatives.

## Interface, evidence and resource checks

The console selects actual family implementations and supports model status,
start/progress, bounded stop, same-ID resume, prior results, chronological
transcript pages, META claims/history/queue, export and verified reopening.
The default transcript display is the latest twelve turns; explicit page 0 starts
at the beginning. The 18-turn ROM transcript was also inspected in full and its
export reopened through the installed workflow.

The Field Library lists 42 resolvable lesson directories, including SP01. Other
existing documentation collections are preserved without advertising them as
lesson IDs. Final ASK, HINT and EXPLAIN responses were correct against the supplied
sources. TRACE matched the actual A output, four instructions, Monitor return and
program bytes. CHECK confirmed a correct documented answer and abstained on an
incorrect statement and an indirect question. Abstention and model explanations
remain distinct from deterministic execution evidence; a metadata flag alone is
not factual acceptance proof.

Native final checks passed: 25 focused tests and mypy across all 39 application
modules. Earlier repository software gates and focused domain, lifecycle,
installation and storage checks are retained separately. Tests use virtual
hardware and visibly synthetic controls where appropriate.

The final ROM experiment took 244.696 seconds, peaked at 73.25°C and reported no
throttling flags. The application enforces a 75°C guard. Native Ollama's actual
runner confirmed a 256 MiB prompt-cache cap; workloads use bounded contexts,
output, concurrency and retries. Host thermal stops are separate evidence and
are not Pi acceptance results.

The Pi's compatible OS, Python and native Ollama 0.32.14 were reused. Existing
model stores, staged Qwen artifacts, historical registries/results, the period
manual and six historical META databases were preserved. No model download was
needed. Active acceptance used Phi4-mini Q4_K_M with manifest SHA256
`78fad5d182a7c33065e153a5f8ba210754207ba9d91973f57dffa7f487363753` and GGUF SHA256
`3c168af1dea0a414299c7d9077e100ac763370e5a98b3c53801a958a47f0a5db`.

## Remaining contract requirements

- End-to-end physical late-power/startup acceptance remains unverified. Do not
  repeat power tests against the user’s instruction to keep both devices on.
- Finish and verify the existing historical image migration. The original image
  is preserved; an owned incomplete destination is not a verified migration.
  A revised image-only transfer skipped redundant small-file checks and added
  about 1.2 GB, but the host reached 81°C and the 75°C guard stopped it. The
  3,911,385,074-byte partial remains; no final image was promoted. This followed
  another host thermal stop at 83°C under verified efficiency-core affinity and
  a 5% CPU limit. No unchanged transfer retry is queued.
- A later controller proved three cooling pauses/resumptions on the actual
  transfer, with frozen CPU work verified and no thermal transport restart.
  It then stopped at a critical host spike of 102.05°C. The source and partial
  were retained, and task workers/inhibitors were removed. The Pi remained on.
  The operator subsequently confirmed clear vents. Actual fan readings showed
  both fans spinning, while the host platform profile was set to performance.
  A temporary supported power-saver hold changed that profile to low-power.
  A ten-minute resumed transfer then peaked at 58°C with no cooling pauses and
  advanced the owned partial to 4,791,648,232 bytes. A second ten-minute trial
  with a 4 MiB/s transfer cap and 25% CPU allowance also peaked at 58°C without
  cooling pauses, reaching 5,822,611,424 bytes. The longer guarded continuation
  uses those measured limits; this is not yet full-image verification.
- The guarded transfer owns its temporary sleep inhibitor and power-saver hold;
  the watchdog stops on loss of the qualified power profile. Existing thermal,
  UUID, capacity, partial-ownership and full-hash promotion guards remain in
  force. No automatic transport retry or final completion claim is made.
  Privileged setup helpers are removed; the Pi application, provider and SSD
  remain on. No further device power changes are scheduled.
- Cleanup now requires successful termination and no live task processes before
  thawing for service cleanup. A native synthetic frozen-service test verified
  that a rejected kill leaves the worker frozen, followed by successful kill
  and cleanup without more work. Watcher cleanup is pinned to its originating
  transfer invocation, and long-run qualification binds the reviewed controls.

Saved-data persistence is established. Automatic startup following a genuine
post-install SSD activation remains unobserved; earlier recovery used an
authenticated mount operation. If no such observation becomes available under
the current power constraints, the final contract status remains **PARTIAL**
even after image verification. Current service status or rule validation alone
does not replace that acceptance test.

A bounded host audit service now waits for the exact running preservation
transfer to finish. Its process and startup log were verified. It requires the
image completion marker, the receiver's full-hash receipt and unchanged final
file identity, then checks all 195 smaller destinations against their saved
verification fingerprints. Changed or missing evidence fails the audit; it does
not silently assume a match or repeat a full-image read. The audit pins its
verifier hash, rejects a replaced transfer, and publishes a result without
overwriting earlier evidence. Its synthetic failure controls passed. The audit
has not yet run against a completed image and cannot establish application DONE.

Private device identities, credentials, account configuration, complete logs,
backups, weights and raw images are kept outside Git. The private acceptance
ledger contains exact paths, hashes, gate evidence and recovery receipts. A final
four-file launcher/config rollback-and-restore rehearsal passed on the actual
installed revision; no full-system restore is claimed. **DONE has not been
established.**
