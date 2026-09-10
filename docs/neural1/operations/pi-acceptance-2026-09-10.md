# Native Pi acceptance — 2026-09-10

Status: **PARTIAL**. The tested application revision is
`4f06e6d10bcbffca47c0f7554800972555085c78`. This record describes actual
Raspberry Pi 5 Model B Rev 1.1 execution, ARM64, 8 GB RAM. The Apple-1 world
remains **VIRTUAL**. No physical serial commissioning was performed.

The installed normal entry point is `neural1`. It was exercised from a normal
runtime-account login outside the checkout. The final post-reboot workflow is
not yet accepted: the Pi rebooted and reconnected with its verified SSH identity,
but its USB controller did not enumerate the SSD. Reconnecting the SSD restored
its identity. The mount/provider recovery and a stable boot connection remain
unresolved at this record's preparation. The application refused the missing
mount instead of writing fallback data to the microSD.

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

- Resolve SSD availability across normal boot/reboot and restore its guarded
  mount/provider without leaving a setup task for the user.
- Repeat the ordinary launch and a small real-model workflow after the final
  restart; verify persistent models, results, META and export reopening.
- Finish and verify the existing historical image migration. The original image
  is preserved; an owned incomplete destination is not a verified migration.
- Finish the private morning report and machine ledger, then remove temporary
  task helpers/inhibitors while leaving the usable Pi and SSD operating.

Private device identities, credentials, account configuration, complete logs,
backups, weights and raw images are kept outside Git. The private acceptance
ledger contains exact paths, hashes, gate evidence and recovery receipts. A final
four-file launcher/config rollback-and-restore rehearsal passed on the actual
installed revision; no full-system restore is claimed. **DONE has not been
established.**
