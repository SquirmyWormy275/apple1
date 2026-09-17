# Native Pi acceptance — 2026-09-10

Consolidated publication: [Pi commissioning closeout](pi-closeout-2026-09-10.md).

Status: **DONE**. The final coordinated physical startup and live workflow passed.
The installed application is usable and preservation verification has passed.
The tested application revision is
`4f06e6d10bcbffca47c0f7554800972555085c78`. This record describes actual
Raspberry Pi 5 Model B Rev 1.1 execution, ARM64, 8 GB RAM. The Apple-1 world
remains **VIRTUAL**. No physical serial commissioning was performed.

The historical 127,865,454,592-byte image was fully hashed on the native Pi,
matched SHA256 `58e46686e02a54fbe8c7060afdb8a2fdc5eea5e3107478366c7881c7957169da`,
and was promoted to its final SSD destination. The aggregate audit passed all
196 preservation files, totaling 127,870,246,926 bytes. Existing verification
fingerprints were reused for the 195 smaller files; source checks passed and
originals remain retained. Native full-image verification took 3117.69 seconds,
with sampled temperatures around 49–51.8°C, zero throttling flags, and no
matching kernel I/O warnings during the verification interval.

The earlier host guard stopped during verification when its required power
profile was lost, at 49°C. That failed attempt and earlier thermal stops remain
preserved as historical evidence. Native verification reused the completed
transfer; no image recopy or model download was needed.

The final clean shutdown and user-assisted boot with the SSD disconnected
passed: the actual Pi booted normally, the application returned a clear missing
storage error, and the underlying mountpoint remained empty. Connecting and
powering the identified SSD then automatically mounted it and started the local
Ollama service. No manual mount, service start or reset-failed command was used.
Two initial `.local` resolution attempts failed; strict host-key authentication
at the existing Wi-Fi address established the same Pi and its new boot.

Final post-power run `N1-P-5898735E8998CC35` produced three genuine responses and
eight accepted strict Monitor commands. Independent replay/execution printed A
and returned to `MONITOR_WARM_ENTRY`. Turn two received its private Monitor
observations; the configured context reset applied at turn three. The run took
111.291 seconds, peaked at 63.9°C, reported zero throttling flags, and retained
at least 4,407,525,376 bytes of available memory. Normal-login `neural1` from `/`
passed, prior META and a saved ROM export reopened, and the new run's export
verified all 13 files and reopened with its actual META claim.

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
installer tests passed. The final physical arrival test above passed. This rule controls service startup, not enclosure power. The Pi and
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

## Final operating state

All required gates passed. The SSD enclosure still needs its normal physical
activation and connects at USB 2 speed with the existing cable. Its arrival now
starts storage-dependent software automatically; no software setup remains.
The Pi, SSD and local Ollama service remain on. Task-owned host sleep inhibition
and completed temporary helpers are stopped. Writes were flushed; the active
SSD was not unmounted. Originals and historical failed attempts remain retained.

Application release remains `4f06e6d10bcbffca47c0f7554800972555085c78`;
late-SSD wiring is from `462ec40fdb41a5f009574b84b824442ebabd9be6`.
Implementation and this sanitized acceptance record are committed on
`neural1/pi-completion-r3`; publication status is recorded in the consolidated GitHub handover.

Private device identities, credentials, account configuration, complete logs,
backups, weights and raw images are kept outside Git. The private acceptance
ledger contains exact paths, hashes, gate evidence and recovery receipts. A final
four-file launcher/config rollback-and-restore rehearsal passed on the actual
installed revision; no full-system restore is claimed. The complete private morning report and machine-readable gate ledger are
available to the normal Pi account.
