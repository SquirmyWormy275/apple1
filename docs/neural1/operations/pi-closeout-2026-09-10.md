# NEURAL1 native Pi commissioning closeout

**DONE: Pi-hosted NEURAL1 is installed and usable.** This consolidates the
completed commissioning evidence; publishing this report did not repeat setup,
downloads, campaigns, or power tests. The Apple-1 execution target is **VIRTUAL**.
Physical Replica/FT232R qualification remains separate and blocked by its existing
hardware evidence gate. No serial device was opened or firmware/EEPROM changed.

## Revisions and publication scope

- Task branch: `neural1/pi-completion-r3`.
- Laptop HEAD before this documentation closeout:
  `507cb6448a80c80f29c80a4c9f121bc87026da9e`; working tree was clean, with no
  uncommitted implementation changes.
- Actual Pi application release:
  `4f06e6d10bcbffca47c0f7554800972555085c78`, installed under
  `/opt/neural1/releases/4f06e6d10bcbffca47c0f7554800972555085c78`.
- Applied late-SSD startup wiring comes from installer commit
  `462ec40fdb41a5f009574b84b824442ebabd9be6`.
- The Pi uses a pinned full-source release archive and native Python environment,
  not a writable Git checkout. It includes the emulator and lesson resources.
  All 39 top-level `neural1/*.py` hashes were compared read-only during closeout
  and match the laptop runtime files. Later laptop commits changed the installer,
  its focused test, and documentation; they did not change those runtime modules.
- The laptop also has a detached historical verification worktree at `47a9eed`;
  it is not the deployed application or a source of new changes.

The publishing commit contains this report and small evidence extracts. Its full
SHA is supplied in the GitHub handover (a commit cannot embed its own SHA).
No force-push or merge of main is part of closeout.

## Machine, provider and models

Raspberry Pi 5 Model B Rev 1.1, ARM64, 8 GB RAM (8,454,012,928 OS-visible bytes),
Debian 13.6, kernel `6.18.39+rpt-rpi-2712`, Python 3.13.5, native ARM64 Ollama
0.32.14. The existing compatible installations were reused. The normal account
runs inference against the Pi-local loopback provider; no host daemon is needed.

| Artifact | Identity and role |
|---|---|
| Default `phi4-mini:latest`, registry ID `phi4-mini-38b` | 3,836,021,856 parameters, Q4_K_M; used for final native acceptance |
| Phi manifest SHA256 | `78fad5d182a7c33065e153a5f8ba210754207ba9d91973f57dffa7f487363753` |
| Phi GGUF weight SHA256 | `3c168af1dea0a414299c7d9077e100ac763370e5a98b3c53801a958a47f0a5db` |
| Selectable `qwen2.5-coder:1.5b`, registry ID `qwen25-coder-15b` | Q4_K_M; existing staged artifact reused, not the final acceptance model |
| Qwen manifest SHA256 | `d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668` |
| Qwen shared GGUF SHA256 | `29d8c98fa6b098e200069bfb88b9508dc3e85586d20cba59f8dda9a808165104` |

Manifest digests are distinct from weight digests. Other existing model stores,
qualified historical registries, and their license/provenance metadata remain
preserved; this is not a claim that every stored model passed this final run.
No model was downloaded. Missing native git dependencies and ARM64 mypy/librt
verification wheels were acquired for documented compatibility reasons; cached
py65 was reused. Exact acquired-wheel identities are in the completion extract.

Defaults use a 4096-token context, two inference threads, one concurrent request,
bounded output/timeouts, and a verified 256 MiB native prompt-cache cap. The
application enforces its 75°C resource guard, rather than merely logging heat.

## Normal use

From a normal Pi login, in any directory:

```text
neural1
```

No environment activation, configuration edit or setup command is required.
The console uses `[V]` and the existing 40-column conventions.

| Purpose | Supported commands |
|---|---|
| Select family/model | `1`–`5`, `MODELS`, `MODEL model-id` |
| Run and inspect | `START`, `STATUS`, `RUNS`, `SHOW run-id`, `TRANSCRIPT run-id [page]` |
| Lifecycle | `STOP run-id`, `RESUME run-id`; page `0` begins the transcript |
| META and bundles | `META`, `META CLAIM claim-id`, `META HISTORY claim-id`, `META QUEUE`, `EXPORT run-id`, `OPEN bundle-path` |
| SELFHOST archive | `SELFHOST`, `SELFHOST INGEST run-id`, `SELFHOST REBUILD artifact-id`, `SELFHOST QUALIFY evidence-path`, `SELFHOST EXPORT artifact-id`, `SELFHOST OPEN bundle-path` |
| Field Library | `LESSONS`, `SOURCE lesson sources`, `ASK/HINT/EXPLAIN/CHECK lesson question`, `TRACE lesson "assembly with \n separators"` |
| Console | `HELP`, `QUIT` (a running experiment continues in its user service) |

See [operator command semantics](terminal-application.md). Inspect family results;
a campaign summary alone is not evidence of scientific success.

## Storage, startup and recovery

The dedicated approximately 1 TB Inland SSD uses GPT/ext4 at `/mnt/neural1-ssd`.
Serial, filesystem UUID, account IDs and private configuration are intentionally
omitted here; the installed configuration and private operator report retain them.
The root microSD and unrelated storage were preserved.

| SSD-relative path | Contents |
|---|---|
| `models/canonical/ollama` | Native provider blobs/manifests |
| `models/deployment-registry.json` | Deployment-specific model registry |
| `runs/console/campaigns/ID` | Run state, checkpoints, transcripts, resource samples |
| `runs/console/artifacts` | Content-addressed snapshots |
| `meta/console.sqlite`, `meta/preferences-UID.json` | Persistent evidence and model preference |
| `research/selfhost` | Ancestry, artifacts, operation receipts |
| `logs/provider/ollama.log`, `logs/commissioning-r3` | Durable provider and commissioning logs |
| `exports`, `preservation/pi-images` | Verified bundles and preserved historical image |

The UUID-based fstab entry uses `nofail,x-systemd.device-timeout=10s`. Ollama has
`Requires`/`After` dependencies on the SSD mount, an identity-checking
`ExecStartPre`, bounded restart (`RestartSec=10`, two starts per 60 seconds), and
its native store/log paths on the SSD. A UUID/ext4-scoped udev arrival rule
requests Ollama when the enclosure appears; the service dependency mounts the
volume first. Missing/wrong storage refuses work, with no microSD data fallback.
The launcher and config are `/usr/local/bin/neural1` and
`/etc/neural1/config.json`; the installer and storage guard preserve resolved paths.

Normal recovery uses `STOP`/`RESUME` and `EXPORT`/`OPEN`; do not edit cancellation
markers. A real cancellation after one committed turn took 1.280 seconds, and
same-ID resume preserved completed work and the effective registry. Workers have
bounded resource supervision, task-owned identities/locks and durable user services.

Operator backups remain in `/var/backups/neural1/` and `/var/backups/neural1-r3/`.
The tested rollback was exactly the config and three launchers: deployed `4f06`
→ prior `cef` → byte-exact `4f06`, with normal-user STATUS checks. It did not restore
the OS, provider data, SSD, or later udev rule. The protected receipt identifies
verified bytes/modes and prior backups. `~/NEURAL1-RECOVERY.md` on the Pi gives
the complete procedure: confirm target/storage and an idle window, verify backup
hashes/ownership, retain current copies, atomically replace only the four files,
restore in a finally path, and verify normal-user status. Future system rollback
requires ordinary operator authentication; no persistent privileged helper remains.

## Actual acceptance results

| Mode/feature | Existing native evidence and interpretation |
|---|---|
| 4K MIND | Final `N1-P-5898735E8998CC35`: three responses, eight accepted commands, persistent RAM/lineage, private feedback and configured reset; independently checked A/Monitor return |
| SELFHOST/1 | `N1-P-8F46A3AC87392679`: stage-one qualified archive, ancestry/stage checks, exact rebuild and dependency export/reopening; no assembler/compiler discovery claim |
| RAM REPUBLIC | `N1-P-7BCE70401CD99FD1`: two isolated participants, six responses/31 accepted commands, permitted shared-RAM observations, matching replay; final BRK is a valid negative result |
| 1976 MULTIVERSE | `N1-P-FA6767B745263F82`: three typed model genomes reached the period-source-backed validator; unsupported 64K ranges rejected for the documented 4096-byte bank |
| 256-BYTE UNIVERSE | `N1-P-B90E14C4EEF3FC2D`: 18 responses/21 accepted commands; initial A/return, then wrong-address writes, 232 explicit bytes and BRK correctly rejected by exact coverage/behavior checks; meaningful positive/negative controls passed |
| Lifecycle | `N1-P-BB49DACBD19E575B`: bounded cancel/same-ID resume without duplicate committed turns, unchanged registry, provider idle afterward |
| META | Actual claims/history/queue, saved results, verified export/reopening; old ROM evidence and new post-boot claim survived/reopened |
| Field Library | 42 real lessons including SP01; grounded ASK/HINT/EXPLAIN, deterministic TRACE, CHECK confirmation/abstention and full transcript paging |
| Software checks | Existing 25 focused native tests, mypy across 39 modules, earlier 199-test software gates, and nine native installer tests; not rerun for publication |
| Preservation | 196 files / 127,870,246,926 bytes verified; 127,865,454,592-byte historical image fully hashed/promoted, originals retained |

### Existing final power test

The completed sequence was clean shutdown, operator boot without SSD, authenticated
reconnection, missing-storage refusal with an empty fallback tree, then operator
SSD connection/activation. The exact identified SSD mounted and Ollama started
**without manual mount, service-start or reset-failed commands**. Prior results,
models and META reopened, followed by the genuine native run below. Two initial
mDNS resolution failures were retained; strict host-key login via the existing
Wi-Fi address succeeded. [Timestamped sanitized observations](evidence/pi-closeout-2026-09-10/startup-observation.json)
retain the failed lookups as well as the passing phases.

### Post-boot run and hashes

Run **N1-P-5898735E8998CC35**, Phi4-mini Q4_K_M, started
**2026-09-11 03:45:39.671878 UTC** (September 10, 20:45:39 PDT) and finished
**03:47:31.022454 UTC**. Engine elapsed time: **111.291 seconds**.
Three genuine responses accepted **3, 2, 3 commands** respectively. The middle
response echoed observations; the strict parser rejected its noncommand STOP
text. Turns one and three actually executed the program. Independent replay
matched **A**, four instructions and `MONITOR_WARM_ENTRY`. Turn two received its
private observations; turn three used the documented context reset.

Peak 63.9°C, throttling flags zero, minimum available RAM 4,407,525,376 bytes,
minimum SSD free space 856,484,814,848 bytes. Request latencies were 86.34, 18.19
and 6.61 seconds, including the measured first request after boot.

| Original evidence | SHA256 |
|---|---|
| Provider records | `3a343f72d5778266818eb5a8f270daa583bdc5cf98cf1dd9318e9e941eaf1278` |
| Transcript | `035cda02653d4fe6cce59ca0f056addfc1d6e7487eb9b42bd5ffd8132456215a` |
| Resource samples | `81db3c93e98fcd235e337d4a5ec4028c8f1eaa3a70c97d51eff0104c5305af79` |
| Effective registry | `39e0ca6b221d4b6d09ccf19731e9078c1599653c3da6b20ac981852e0c2d651d` |
| Export/META artifact | `3e7d93859b8c8c5247ecf62fd6b55da4325183ffa314403f3bf66e15d2c35dba` |

The new claim is `N1-C-5DA21D6803488059`; its export verified all 13 files and
reopened. The [run extract](evidence/pi-closeout-2026-09-10/post-boot-run.json)
includes actual prompts/responses, parser results, execution trace, individual
raw-response hashes and further original-artifact hashes. The
[independent review](evidence/pi-closeout-2026-09-10/independent-review.json)
distinguishes native evidence from its supporting host-memory replay.

## Limits and preserved history

No required NEURAL1 software gate remains incomplete. Bounded presets establish
correct operation, not autonomous discovery, compiler self-hosting or a complete
replacement Monitor. Multiverse claims are limited to reviewed CPU/RAM structure;
unknown prices/electrical properties remain unknown. CHECK abstention is not a
definitive false classification. Valid negative family results stay negative.

The enclosure needs its normal physical activation and the current connection
runs at USB 2 speed despite the blue port. Poor Wi-Fi, intermittent mDNS, earlier
host thermal stops (including 102°C), malformed provider responses and earlier
failed acceptance attempts remain recorded. They are not hidden or counted as
successful experiments. Pi resource limits were measured separately; prior ROM
peak was 73.25°C. There is no claim of unattended enclosure power control.

Historical Pilot 001 remains unchanged: 45 planned cells, six completed,
156 turns, 102°C stop, zero strict-parser acceptances and zero automatic findings.
Its evidence and qualified registries were not rewritten or replaced by this run.

The final operating state is Pi/SSD/provider powered and usable, writes flushed,
temporary helpers and host sleep inhibition removed. Private reports and recovery
notes are available from the normal Pi account and SSD commissioning-log directory.

## Published evidence

The [evidence directory](evidence/pi-closeout-2026-09-10/README.md) contains only
small sanitized extracts and a checksum list. Original-file hashes identify
retained private artifacts; they are not hashes of the redacted extracts. No
credentials, private account/network configuration, raw disk images, weights or
full private logs are included. The prior [native acceptance record](pi-acceptance-2026-09-10.md)
remains available as commissioning history.
