# Installed virtual NEURAL1 terminal

The normal installed entry point is `neural1`, from any working directory.
`neural1 console` is equivalent. Installation alone is not Pi acceptance: the
five real-provider workflows, reboot, resource behavior and recovery must be
observed on the identified target before declaring it commissioned.

The console shows only implemented operations:

- `1` through `5` select 4K MIND, 1976 MULTIVERSE, SELFHOST/1,
  256-BYTE UNIVERSE, or RAM REPUBLIC.
- `MODELS` lists the deployment registry; `MODEL model-id` verifies the live
  local Ollama manifest identity before selecting it.
- `START` creates a bounded preset with its own seed and campaign ID.
  `STATUS`, `RUNS`, `SHOW run-id`, and `TRANSCRIPT run-id` expose progress,
  checkpoints, actual family evaluation, and recorded model/Monitor exchanges.
- `STOP run-id` requests owned cancellation and interrupts only the verified
  matching worker. `RESUME run-id` preserves committed turns and snapshots;
  a crash tail is retained separately for audit. It never removes another run's
  cancellation marker.
- `META`, `META CLAIM claim-id`, `META HISTORY claim-id`, and `META QUEUE`
  browse actual persisted run observations and their evidence relationships.
- `EXPORT run-id` makes a verified bundle including referenced snapshots and
  a consistent SQLite backup. `OPEN bundle-path` verifies and reopens it.
- `SELFHOST` lists the persistent artifact archive. `SELFHOST INGEST run-id`
  imports verified SELFHOST stage-one run evidence. `SELFHOST REBUILD artifact-id`
  repeats its recorded virtual construction and checks exact bytes.
  `SELFHOST QUALIFY evidence-path` evaluates later-stage ancestry, virtual builds,
  exact repeat reconstruction, and declared behavioral controls from an SSD file.
  It records a negative result when the actual candidate fails; it does not
  supply or invent an assembler. `SELFHOST EXPORT artifact-id` includes its
  dependency closure; `SELFHOST OPEN bundle-path` verifies and reopens it.
  Operation receipts also appear in META. Synthetic/replayed origins retain
  that label through every descendant.
- `LESSONS` lists existing lesson folders. `SOURCE lesson sources`,
  `ASK lesson question`, `HINT`, `EXPLAIN`, and `CHECK` use the real corpus.
  `TRACE lesson "assembly with \n separators"` assembles and executes through
  the existing deterministic harness before asking for explanation.
- `QUIT` closes the console; an active run continues in its user service.

Output is labeled `[V]` and wraps at 40 columns. These operations never open
physical transport. A valid negative domain result is distinct from provider
failure, parser rejection, blocked data, or scientific success. Inspect the
family result, not only the campaign summary.

The defaults are bounded starting experiments. SELFHOST begins with a raw
machine-code execution task; it does not claim a discovered assembler or
compiler. Exact-256 evaluates explicitly deposited 256-byte candidates against
an executable output/return task with independent controls; it does not claim
a complete replacement Monitor. RAM REPUBLIC evaluates isolated participants'
shared-memory interactions without claiming protocol emergence. Multiverse
uses the separately reviewed year-end 1976 corpus and validates partial CPU/RAM
structure and provenance; unknown prices and electrical claims stay unknown.

## Deployment and persistence

`tools/neural1_install_pi.py` is an operator deployment tool, not a first-launch
setup task. It refuses a non-Pi host, unidentified/unmounted storage, uncommitted
source, an incompatible provider executable, or a missing native model store.
It acquires no models and performs no formatting. Its exact arguments come from
verified live inventory, not guessed device nodes.

The installer uses a complete pinned checkout under `/opt/neural1/releases/`,
a native Python environment, `/etc/neural1/config.json`, and resolved wrappers
under `/usr/local/bin/`. This deliberately includes `tools.apple1_emulator`,
lesson documents, and historical resources, which a neural1-only wheel omits.
The tested source revision is recorded separately from deployment acceptance.

On the expected SSD, console output lives under `runs/console/campaigns/ID`,
content-addressed snapshots under `runs/console/artifacts`, META under
`meta/console.sqlite`, and provider/worker logs under `logs`. SELFHOST artifacts,
ancestry, evidence, and operation receipts live under `research/selfhost`. Historical model
registries are preserved; each run retains its effective generation registry.
Ollama uses its native `blobs`/`manifests` layout on the same verified volume.

The expected filesystem UUID, mount source, role marker, capacity and resolved
write paths are checked before work. Missing storage never becomes a directory
fallback on the boot card. Normal boot uses a `nofail` mount; the provider is
bound to the SSD mount and an explicit identity check. A worker pins its working
directory on the volume to block ordinary unmount while active.

Workers use transient user services, a global run lock, per-campaign lock,
unique startup identity and durable logs. The installer records the account's
prior linger setting before enabling it when needed for logout persistence.
A two-second watchdog checks temperature, available memory, storage identity,
capacity and current Pi throttling flags; violations interrupt the client.
Transport/output bounds limit inference. Foreground Field Library model calls
run in a bounded child process; the console checks resources while waiting and
terminates that child on failure, timeout, or cancellation. It does not retain a
watchdog thread after the operation. Actual provider cancellation latency
and cooling still require measurement on the installed Pi; a log alone is not
acceptance. No automatic retry loop repeats failed scientific work.

Configuration backups and byte hashes are written under `/var/backups/neural1/`
before changes. The installation receipt records prior linger state and its
exact rollback command. Operator rollback restores recorded configuration
files, reloads systemd, and restores the previous launcher/release; it never
formats storage or deletes retained evidence. This procedure must be rehearsed
on the real target before being described as tested recovery.
