# Hook state machines · `spec:hooks:hook-state-machines`

This part realizes the hook-machine outline (`sec:assembly:hooks-outline`). It specifies the two deployed callbacks as total transition systems whose observable decisions, state changes, timing bounds, and recovery behavior can be carried unchanged into a direct graph implementation. Every label minted here has area `hooks`.

## Scope · `sec:hooks:scope`

This part governs the rulebook-injection callback and the stop-time heartbeat guard from receipt of one harness event through one semantic verdict. It owns event classification, graph states and edges, hook-maintained persistence, deduplication, structural transcript inspection, bounded timing decisions, and fail-open effects. It does not choose orchestration policy, worker lifecycle, watchdog cadence, dispatch recovery, or the contents of the rulebook it transports.

The injection machine delivers the orchestration rulebook only to the top-level audience selected here; it does not grant that audience to a worker or derived context. This boundary specializes audience separation (`rule:architecture:audience-separation`). The heartbeat machine enforces a stop handshake only. It neither polls for results nor decides whether work is stalled. Both machines produce semantic hook verdicts; the hook JSON stream and process encoding remain governed by (`[TOOLS-spec:output:hook-json-streams]`).

## Shared machine contract · `sec:hooks:shared-machine-contract`

This division fixes the representation and safety rules shared by both machines. Machine-specific divisions refine the common event, state, verdict, and effect classes without acquiring policy outside this part.

**Definition (Hook machine)** · `def:hooks:hook-machine`

A hook machine is a total transition from one event, prior owned state, and evaluation-time observation to exactly one terminal semantic verdict and a finite ordered effect list. A verdict is either allow or block. An allow may carry no response, additional context for the intended agent, or a user-directed system message. A block carries one agent-directed reason. Effects may inspect declared inputs, replace hook-owned state, rotate a snapshot, append a redacted log record, or wait for one specified retry.

Totality applies to the complete input domain, not only to valid harness events. Rejection, disablement, refusal, and internal failure are ordinary terminal paths. A process adapter encodes the semantic verdict in the harness-owned hook JSON mode; graph evaluation itself must not invent a workspace report, a worker message, or a second verdict.

**Signature (Hook event)** · `sig:hooks:hook-event`

The common event record contains a hook-event class, a harness payload, an optional session identity, a project working directory, an optional transcript identity, an explicit UTC wall-clock evaluation instant, and a monotonic start instant. The prior-state member is either a complete parsed hook record or the declared missing, unreadable, or invalid condition. The result record contains the terminal graph node, semantic verdict, response class, ordered persistence and logging effects, and elapsed wall time.

Payload text, transcript bytes, rulebook bytes, and prompt text are inputs, not diagnostic fields. Wall time used for deduplication and transcript timestamps used for scheduling are distinct clocks. Elapsed time is measured from the monotonic instant so a wall-clock correction cannot produce a negative runtime measurement.

**Definition (Hook state store)** · `def:hooks:hook-state-store`

The hook state store is the implementation-owned directory containing project toggle flags, per-session machine records, per-session rulebook snapshots, turn-local heartbeat counters and warning markers, and the injection log. The hook implementation is its sole maintaining authority under (`rule:architecture:mutable-state-ownership`). Toggle commands are authorized writers only for their matching flag; callbacks read those flags and write only their own machine records. Harness transcripts and the live rulebook remain inputs owned elsewhere.

Project keys are formed by replacing every slash in the working-directory string with a hyphen. Injection session keys use a nonempty string session identity, replace slashes and NUL bytes with hyphens, and otherwise use the literal fallback `unknown`. Heartbeat count and warning records are keyed by the supplied session identity and contain the marker of the latest real user turn. Internal filenames and JSON layouts may migrate, but project/session partitioning, allowed writers, update triggers, and observable recovery semantics must remain equivalent.

State has bounded operational retention by logical role: one injection record per session key, two named rulebook snapshots per session key, one heartbeat count and one warning marker per heartbeat session, project/global toggle flags, and an append-only injection log. Cleanup policy, physical state-root location, and log retention are deployment data; cleanup must not occur during an invocation or manufacture a protocol decision.

The deployed compatibility names are displayed here so a replacement can read old state or declare a migration before changing them:

```text
orchestrator-disabled-GLOBAL
orchestrator-disabled{folded-project}
orchestrator-scope-{safe-session}.json
orchestration-snapshot-{safe-session}-current.md
orchestration-snapshot-{safe-session}-prev.md
orchestrator.log
heartbeat{folded-project}
guard-count-{session}
guard-warn-{session}
```

**Rule (Direct state graph)** · `rule:hooks:direct-state-graph`

Each machine must be represented directly as graph nodes and directed edges. Nodes name decision states or terminal verdict states. An edge names its input predicate, time predicate if any, ordered effects, and destination. Evaluation starts at the event-entry node and follows exactly one satisfied outgoing edge at each decision node until one terminal verdict is reached. Mutually overlapping guards, an input with no edge, a hidden state switch outside the graph, or a wrapper that reproduces the decision tree instead of traversing it is nonconforming.

Several semantic states may converge on the same terminal verdict node, and a state family may use persisted phase bits to select different outgoing edges. Those phase bits are part of the graph state, not permission to decide outside the graph. Every exceptional and fail-open path therefore remains visible to edge enumeration and replacement testing.

**Invariant (Fail-open safety)** · `inv:hooks:fail-open-safety`

Malformed input, an unsupported event, missing or unreadable optional state, an unreadable required input, and an internal evaluation failure must never fabricate a block or trap the harness. Unless a machine has already reached an intentional block node, inability to judge terminates at allow with no partial hook response. An unreadable heartbeat transcript never implies that a wakeup is pending. A failed injection never publishes a truncated rulebook or change notice.

State and log effects that completed before a failure may remain; fail-open is not rollback. The next invocation must be able to classify those effects as complete, missing, or stale and reconcile them without relying on untrusted partial output. Injection failure further obeys the declared external fail-open scenario (`[TOOLS-scenario:output:orchestrator-hook-fail-open]`).

**Requirement (Redacted diagnostics)** · `req:hooks:redacted-diagnostics`

Every operational error record must name a stable action or failure class and may include only the event class, opaque session identity, content digest, numeric size or stamp, elapsed time, and registry-approved configured-resource identity needed to diagnose that class. It must exclude rulebook and transcript content, prompt identifiers and text, raw stdin, exception messages, tracebacks, credentials, and caller-supplied paths. An internal error records the exception type only, never its value.

Diagnostics use the out-of-band injection log or a declared harness response; they never share a partial response publication. Failure to append an out-of-band log is itself fail-open. Heartbeat lapse alarms and protocol corrections are verdict outputs rather than operational diagnostics and must still contain no classified value.

## Orchestration injection · `sec:hooks:orchestration-injection`

This division specifies the rulebook-injection graph. Its persistent facts record which content edition was delivered, which callback output was already emitted, and which two snapshot generations support change reconciliation.

**Signature (Injection input)** · `sig:hooks:injection-input`

The injection callback accepts only `SessionStart` and `UserPromptSubmit` events. A `SessionStart` source belongs to one of three classes:

```text
fresh sources:   startup, clear, compact
resumed sources: resume, fork
other source:    every other string, including the empty string
```

The payload supplies the source, session identity, prompt identity, working directory, transcript path, and optional derived-agent identity. A nonstring session identity becomes `unknown`; a nonstring working directory is replaced by the process working directory; a nonstring source becomes empty. Prompt identity participates only when it is a string. The transcript path is an optional recognition input and is never parsed as conversational prose.

An event outside the accepted pair reaches an output-free allow before toggle, audience, rulebook, transcript, or session-state access. A fresh source always selects fresh-session handling after the common guards. A resumed source selects reconciliation. A prompt event and an unrecognized session-start source use ordinary existing-state change detection.

**Signature (Scope marker)** · `sig:hooks:scope-marker`

A scope marker contains the SHA-256 digest of the exact rulebook byte string and the integer nanosecond modification stamp observed before that string was read. The full-injection response has this displayed shape:

```text
ORCHESTRATION_SCOPE_MARKER v1 sha256={lowercase-hex-digest} mtime={mtime-ns}
{UTF-8 rulebook text}
ORCHESTRATION_SCOPE_MARKER_END v1 sha256={lowercase-hex-digest}
```

Exactly one line-feed is inserted before the closing sentinel when the rulebook does not already end in one. The digest defines the content edition; the modification stamp records the observation that selected it and drives the stat-only fast path. Transcript recognition searches for the opening version-and-digest byte sequence of the current content edition anywhere in the bounded tail. The deployed predicate does not require a line boundary, compare the marker's modification stamp, or validate the closing sentinel. It does not parse rulebook prose, accept a digest for another edition, or use modification time alone as proof that content is present.

**Diagram (Injection state machine)** · `diag:hooks:injection-state-machine`

The displayed graph separates output-free refusal from exception-driven fail-open. `PRESENT` means that no full response is required for the current content edition; it does not mean that all persisted metadata is already fresh.

```text
ENTRY
  | malformed/non-object --------------------------> FAIL_OPEN --> ALLOW_EMPTY
  | unsupported event -----------------------------> REFUSED_EVENT --> ALLOW_EMPTY
  v
DISABLE_CHECK -- global/project flag present ------> DISABLED --> ALLOW_EMPTY
  |
  v
AUDIENCE_CHECK -- derived id or subagent path -----> REFUSED_AUDIENCE --> ALLOW_EMPTY
  |
  v
RULEBOOK_GUARD -- missing/unreadable/oversized ----> REFUSED_RULEBOOK --> LOG --> ALLOW_EMPTY
  |
  v
EVENT_CLASS
  | fresh source ----------------------------------> FRESH
  | resumed source --------------------------------> RESUMED
  | prompt or other SessionStart source ----------> TRACKED

FRESH -- duplicate callback -----------------------> DEDUPED --> ALLOW_EMPTY
  | new callback
  +------------------------------------------------> INJECT_FULL --> SNAPSHOT --> STATE --> LOG --> ALLOW_CONTEXT

RESUMED -- state file absent ----------------------> INJECT_FULL
  | current marker witness absent -----------------> INJECT_FULL
  | current marker witness present ----------------> PRESENT

TRACKED -- state file absent ----------------------> INJECT_FULL
  | observed mtime equal --------------------------> PRESENT --> ALLOW_EMPTY
  | observed mtime different ----------------------> CHANGED

CHANGED -- digest equal ---------------------------> REFRESH_STATE --> ALLOW_EMPTY
  | digest different, duplicate prompt -----------> DEDUPED --> ALLOW_EMPTY
  | digest different ------------------------------> ROTATE --> SNAPSHOT --> STATE --> NOTICE --> LOG --> ALLOW_CONTEXT

PRESENT -- digest/stamp metadata stale ------------> REFRESH_SNAPSHOT_STATE --> ALLOW_EMPTY
  | metadata current ------------------------------> ALLOW_EMPTY

any effect or evaluation exception before publication
  +------------------------------------------------> FAIL_OPEN --> LOG_CLASS_IF_POSSIBLE --> ALLOW_EMPTY
```

**Rule (Top-level only)** · `rule:hooks:top-level-only`

Injection is permitted only when the payload does not identify a derived agent. A truthy derived-agent identity refuses injection. Independently, a string transcript path containing the structural path segment `/subagents/` refuses injection. A null or empty derived-agent identity alone does not refuse a main session. These checks use payload structure and path structure, never prompt or transcript content.

Audience refusal is output-free allow and creates no session state, snapshot, or log entry. It occurs after disablement but before rulebook stat or read, so an unintended audience cannot learn rulebook existence, size, digest, or content through the hook response.

**Rule (Disable precedence)** · `rule:hooks:disable-precedence`

The injection toggle is enabled by absence: injection is disabled when either the global disable flag or the current project's disable flag exists. The project flag uses the folded project root resolved by the same rule as the heartbeat toggle (`rule:hooks:per-project-heartbeat-toggle`), while the persisted session record keeps the raw payload working directory. The toggle command's project `off` operation creates that flag and `on` removes it; the global form does the same for the single global flag. Status reports both scopes, and the effective state is off if either one is off.

Disablement is evaluated after event acceptance and before audience classification, rulebook metadata, session state, snapshot, or transcript access. It returns output-free allow without logging an injection refusal. Changing a flag affects the next invocation and does not rewrite an existing session record or remove a marker already in context.

**Rule (Rulebook size bound)** · `rule:hooks:rulebook-size-bound`

The stable maximum rulebook size is 9,500 bytes. The machine first stats the configured rulebook and refuses any reported size greater than that maximum before reading bytes. After the read it checks the actual byte length again, so growth between stat and read cannot cross the boundary unnoticed. Exactly 9,500 bytes is admissible. Character count and decoded code-point count are irrelevant.

An admissible byte string must also decode completely as UTF-8. Missing, unreadable, undecodable, or oversized input follows rulebook refusal rather than internal failure. The same bound is reported by the toggle status command so operator diagnosis and callback enforcement use one protocol constant.

**Invariant (Exactly once in context)** · `inv:hooks:exactly-once-in-context`

For one top-level session and one content digest, the machine emits a full scope marker only when a fresh-context boundary requires it, session state is absent, or resumed-context evidence lacks the current digest witness. A repeated callback inside its deduplication boundary emits nothing. Ordinary prompt events with present state and unchanged modification time perform no rulebook read and emit nothing. A content change emits a notice rather than a second full marker into the running context.

Historical markers for older digests may remain in a retained transcript; they do not prove presence of the current edition. Recognition inspects only the last 1,048,576 transcript bytes, the bounded region treated as evidence for the active context. A current witness outside that region is deliberately absent for reconciliation purposes. Correctness therefore requires event serialization per session and an append-only transcript while one invocation is deciding; concurrent writers may not race one session record.

**Protocol (Fresh-session injection)** · `proto:hooks:fresh-session-injection`

For `startup`, `clear`, or `compact`, and for absent-state recovery reached by another accepted event, the machine performs these steps in order:

1. Apply event, disablement, and top-level guards, then stat and size-check the configured rulebook.
2. Resolve whether the per-session state path exists and load its complete object, treating an unreadable or invalid body as an empty record.
3. Read the rulebook bytes, verify the post-read size, decode UTF-8, compute SHA-256, and retain the observed nanosecond modification stamp.
4. Evaluate the event-specific deduplication key. On a hit, allow without snapshot, state, log, or output.
5. Atomically replace the session's current snapshot with the exact rulebook bytes; a fresh injection does not rotate current to previous.
6. Update the complete session record with session, working directory, digest, stamp, current-snapshot identity, update time, and deduplication facts, then atomically replace the record.
7. Append an injection record containing the stable action, event, opaque session, digest, stamp, and elapsed time. Log failure does not undo state.
8. Compose and publish one full marker response as additional context.

Snapshot or state failure before response publication follows internal fail-open. The next invocation treats whatever complete files remain as its prior state and repeats the ordinary guards; it never assumes that an output was delivered merely because a snapshot exists.

**Protocol (Resumed-session reconciliation)** · `proto:hooks:resumed-session-reconciliation`

For `resume` or `fork`, reconciliation is ordered as follows:

1. Apply the common guards, resolve whether the per-session state path exists, and load its body when present.
2. Read and validate the live rulebook and compute its digest and observed modification stamp.
3. If the per-session state path does not exist, invoke full injection and its session-start deduplication check.
4. Otherwise search the transcript tail for the current digest's opening marker witness. A missing, nonstring, empty, or unreadable transcript path, or a tail without that witness, invokes full injection.
5. When the witness is present, emit nothing. If the loaded state's digest or stamp differs, atomically refresh the current snapshot and complete state from the live bytes; if both agree, perform no write.

An invalid state body at an existing state path is treated as an empty record, not as an absent path. A present transcript witness therefore repairs that record without reinjection; an absent witness reinjects. Reconciliation never uses a historical snapshot as proof of context presence.

**Protocol (Prompt deduplication)** · `proto:hooks:prompt-deduplication`

Before a `UserPromptSubmit` full injection or content-change notice, the machine compares a string prompt identity with the remembered prompt list. A match suppresses the complete output-producing transition, including snapshot, state-update, rotation, and log effects. On a miss, a nonempty string identity is moved to the newest position and only the newest 64 unique identities are retained. Missing, nonstring, and normally empty identities are not recorded and cannot provide deduplication.

A `SessionStart` output uses a separate key consisting of session identity, source, and current digest plus its recorded wall-clock time. The same key is a hit when the new wall time is not earlier and differs by at most 5.0 seconds, inclusive. A different source or digest, a negative delta, an invalid recorded time, or a delta greater than 5.0 seconds is a miss. This bound absorbs one duplicate harness start; it is not a session lifetime or supervision cadence.

**Protocol (Rulebook change notice)** · `proto:hooks:rulebook-change-notice`

For an accepted ordinary tracked event with existing state, the machine performs these steps:

1. Stat the live rulebook. If its nanosecond modification stamp equals the stored stamp, allow without reading bytes.
2. On a different or missing stored stamp, read and validate the bytes and compute the live digest.
3. If the digest equals the stored digest, update the stored stamp and base metadata atomically, but emit no notice and do not rotate snapshots.
4. If the digest differs, apply prompt deduplication when the event is a prompt. A duplicate emits nothing and leaves the old state for a later event to reconcile.
5. Rotate an existing current snapshot to previous, atomically write the new bytes as current, update the complete state to the new digest and stamp, and atomically replace it.
6. Emit one additional-context notice naming the old and new stamps and directing the agent to diff the previous snapshot against the live rulebook, then append the structured change action.

When the existing record has no parseable old stamp, the notice renders the old value as zero. The new value is always the nanosecond stamp observed for the bytes just stored.

An unrecognized `SessionStart` source follows this protocol but has no prompt identity deduplication. Modification time is a fast-path trigger, so deployment must preserve a content-changing modification-time transition; changing bytes while preserving the exact stamp is outside the detectable input contract.

**Requirement (Atomic state write)** · `req:hooks:atomic-state-write`

Every injection session record is serialized as one complete JSON object plus one terminating line-feed in a sibling temporary file and made visible by one atomic replacement. Readers see the old complete object, the new complete object, or an invalid/missing condition; they must not observe a partially serialized object. The temporary identity is private to the session writer, and the harness must serialize writers for one session key.

Atomic visibility does not make the state record, snapshots, and append-only log one transaction. A failure between those effects may leave a complete new snapshot with old state or complete new state without its log record. Recovery uses live bytes, transcript evidence, and the transition protocols above; it does not roll back one complete file by guessing another file's intent.

**Requirement (Snapshot rotation)** · `req:hooks:snapshot-rotation`

Each injection session retains exactly the named current and previous snapshot roles needed for a change diff. A full injection atomically replaces current without rotation. A digest-changing notice first atomically replaces previous with the former current when current exists, then atomically writes the new live bytes as current. A further change replaces the older previous; no third generation is part of the contract.

The state record points to current. The notice points to previous and the live rulebook, not to an in-memory diff. If no current snapshot exists, rotation is a no-op and current is still written; the notice may identify a previous path whose absence is evidence of incomplete prior persistence. Snapshot writes use sibling temporary files and atomic replacement, but the two-file rotation is intentionally not claimed to be one filesystem transaction.

**Scenario (Rulebook refusal)** · `scenario:hooks:rulebook-refusal`

Refusal is detected when stat reports the rulebook missing or unreadable, reported size exceeds 9,500 bytes, reading fails, UTF-8 decoding fails, or the actual bytes exceed the bound after a successful stat. The machine appends a redacted `guard4_refusal` action with the stable reason `rulebook_missing`, `rulebook_unreadable`, or `rulebook_oversized` and the permitted numeric evidence, then allows with no hook response. It does not create or update session state or snapshots.

Recovery is external repair of the configured file, access, encoding, or size. The next accepted event repeats the guards from entry and may inject or reconcile normally. A refusal never marks the edition as delivered, and log failure cannot turn refusal into a block.

**Scenario (Injection internal error)** · `scenario:hooks:injection-internal-error`

An exception not classified as rulebook refusal is detected at the outer machine boundary before response publication. The machine discards the composed response if publication has not begun, attempts one structured `internal_error` record containing only the exception type and elapsed time, and returns output-free allow. It subsequently records a `slow_run` action when the deployment's telemetry threshold is exceeded; that threshold is registry data and does not select a machine transition.

Recovery preserves any already completed atomic file effects and starts the next invocation at entry. A missing state record selects full injection; a present marker can repair stale state on resume; and an ordinary changed event can rebuild snapshots through rotation. No recovery path emits exception text, a traceback, or a synthetic success response. Failure after publication has begun is governed by the hook stream contract and cannot be repaired with a second response.

## Heartbeat guard · `sec:hooks:heartbeat-guard`

This division specifies the stop-hook graph. It separates a pending scheduler fact, which can outlive a user turn, from violation, warning, and block-count facts, which are scoped to the latest real user turn. The wakeup itself exists only to check Sonnet watcher liveness, absolute UTC deadlines and complete duty coverage (`proto:dispatch:heartbeat-supervision`); the hook mechanics do not authorize lane, gate or inbox polling by the session.

**Rule (Mail notice)** · `rule:hooks:letters-context`

At SessionStart, UserPromptSubmit and Stop, the mail hook resolves the loop from the working-directory project and checks its mail inbox. A nonempty inbox contributes only the line `You've got mail.`; an empty inbox contributes nothing (`rule:mail:notice`). The five-second entry deadline, fail-open behavior, composition ceiling and heartbeat counters remain in force. The hook parses no letter or legacy metadata and emits no count, sender, subject, timestamp or content; read history does not trigger it. The label remains the hook entry point for existing citations, while the mail part owns the notice and ordinary inbox watcher (`proto:mail:watch`).

**Signature (Stop input)** · `sig:hooks:stop-input`

The stop evaluation accepts one JSON object containing working directory, transcript path, session identity, and the `stop_hook_active` flag, together with the current UTC evaluation time. The folded project root selects the heartbeat toggle and is resolved from an absolute working directory by examining the nearest of the working directory and its ancestors strictly below the exclusive home boundary when that boundary is a lexical prefix of the working directory, the working directory included, and otherwise unbounded through the filesystem root; the first existing `.git` entry ends the walk and selects its directory only when plausible, meaning a directory containing a `HEAD` file or a file whose first bytes are `gitdir:`, while an implausible first entry or no entry leaves the working directory itself as the root; a relative or empty working directory is returned unchanged without a filesystem probe. A false or absent toggle terminates before transcript or session-state access. A missing session identity uses `unknown` for persistence.

The transcript is UTF-8 JSON Lines. Blank lines, unparsable lines, and parsed values that are not objects are skipped. Sidechain entries never participate. A real user turn is a nonsidechain user entry that is neither a tool-result carrier nor guard feedback beginning with the stable feedback prefix. The index of the latest such entry, rendered as a string, is the turn marker; if none exists, the marker is the string form of no index.

The input's active-stop flag means that the current evaluation follows an earlier stop-hook block. It authorizes only the one flush-race retry. It does not prove that an arm occurred, increment a counter, or select a verdict by itself.

**Definition (Pending wakeup)** · `def:hooks:pending-wakeup`

A pending wakeup is established by the newest structurally matched, successfully completed `ScheduleWakeup` tool call that supplies usable evidence. Completion requires a later user tool-result block with the call's identifier and no truthy error flag. Result prose is ignored. A truthy `stop` input on that newest usable call establishes not pending. A non-stop call requires a numeric delay and at least one calendar-valid UTC timestamp with a Z suffix; failed, in-flight, malformed-delay, or wholly untimestamped calls are skipped in favor of an older usable call.

For an arm, scheduling time is the result entry's validated explicit UTC timestamp when usable and otherwise the tool-call's validated explicit UTC timestamp. Delay is clamped to the scheduler's 60-through-3,600-second range, then 120 seconds of scheduler slack is added. The wakeup is pending exactly while evaluation time is strictly earlier than that sum. Equality is expired. Pending status persists across a user-turn boundary because it is reconstructed from transcript structure rather than a turn-local state flag.

**Diagram (Heartbeat state machine)** · `diag:hooks:heartbeat-state-machine`

The four exception names are a family over violation and armed/unarmed/lapsed configuration. Bracketed warning phase is persisted state and therefore selects graph edges without an out-of-graph decision.

```text
ENTRY -- malformed/non-object/internal inability ------> FAIL_OPEN --> ALLOW_SILENT
  |
TOGGLE -- flag absent ---------------------------------> OFF --> ALLOW_SILENT
  |
TRANSCRIPT -- unreadable ------------------------------> FAIL_OPEN --> ALLOW_SILENT
  |
  +-- initially unarmed + active stop --> RETRY_ONCE --> TRANSCRIPT
  v
RESOLVE(armed, violated, prompt_count, warned)
  |
  +-- armed, not violated -----------------------------> ARMED --> ALLOW_SILENT
  +-- unarmed, count below cap, not violated ----------> PROMPT --> BLOCK_PROMPT
  +-- unarmed, count at cap, not violated -------------> EXCEPTION_LAPSE --> ALLOW_LAPSE_ALARM
  |
  +-- armed, violated, warning fresh ------------------> EXCEPTION_UNPROMPTED_ARMED[fresh]
  |                                                       --> BLOCK_VIOLATION
  +-- armed, violated, warning recorded ---------------> EXCEPTION_UNPROMPTED_ARMED[warned]
  |                                                       --> ALLOW_SILENT
  +-- unarmed, count below cap, violated, warning fresh -> EXCEPTION_UNPROMPTED_UNARMED[fresh]
  |                                                       --> BLOCK_VIOLATION_AND_PROMPT
  +-- unarmed, count below cap, violated, warning set --> EXCEPTION_UNPROMPTED_UNARMED[warned]
  |                                                       --> BLOCK_PROMPT
  +-- unarmed, count at cap, violated, warning fresh --> EXCEPTION_UNPROMPTED_LAPSE[fresh]
  |                                                       --> ALLOW_LAPSE_AND_VIOLATION_ALARM
  +-- unarmed, count at cap, violated, warning set ---> EXCEPTION_UNPROMPTED_LAPSE[warned]
                                                          --> ALLOW_LAPSE_ALARM

BLOCK_* -- prompted successful arm --------------------> RESOLVE(armed)
BLOCK_* -- heartbeat flag removed ---------------------> OFF
BLOCK_* -- any other next stop ------------------------> RESOLVE(unarmed, incremented count)
LAPSE_* -- next real user turn ------------------------> RESOLVE(reset turn-local state)
```

**Rule (Structural wakeup detection)** · `rule:hooks:structural-wakeup-detection`

Detection scans transcript entries backward. It skips sidechains. Successful tool results encountered in user entries are indexed by tool-use identity and result timestamp. Assistant content is then inspected in reverse block order for `ScheduleWakeup` calls whose successful result has already been seen. The first usable call decides pending status; result text, assistant prose, and older usable calls cannot override it.

Any nonsidechain entry with a calendar-valid explicit UTC timestamp more than 3,720 seconds older than evaluation time terminates the scan as not pending. This horizon is the 3,600-second maximum clamp plus 120-second slack; no compliant older arm can remain pending. The 60-second lower clamp is equally load-bearing because the scheduler promotes shorter requests. Future timestamps do not trigger the old-entry cutoff. A malformed timestamp is no evidence but does not itself end the scan. Horizon soundness requires append order to agree with timestamp order; a transcript that places newer scheduling evidence before a later old entry violates the structural input contract.

**Rule (Per-project heartbeat toggle)** · `rule:hooks:per-project-heartbeat-toggle`

Heartbeat enforcement is enabled only while the flag named by the folded project root exists; for an absolute working directory, the toggle and every hook examine the nearest of the working directory and its ancestors, strictly below the exclusive home boundary when that boundary is a lexical prefix of the working directory, the working directory included, and otherwise unbounded through the filesystem root, stop at the first existing `.git` entry, and select its directory only when plausible, meaning a directory containing a `HEAD` file or a file beginning with `gitdir:`; calls at that directory or below it with no nearer `.git` entry agree on one key, while an implausible first entry or no entry in the walk keys on the supplied working directory itself, as before; a relative or empty working directory is returned unchanged without a filesystem probe. Absence is the default and resolves to `OFF`. The toggle command uses its current working directory to select the same project key: `on` creates the flag, `off` removes it, and `status` reports presence. There is no global heartbeat flag.

The flag is checked before transcript access on every stop evaluation, so removing it is the blocked-on-user exit even after a prior block or violation. Creating it does not arm a wakeup, create a turn counter, or select a watchdog cadence. Cadence belongs to supervision registry data outside this machine.

**Protocol (Heartbeat state resolution)** · `proto:hooks:heartbeat-state-resolution`

Each enabled, readable evaluation resolves in this order:

1. Load transcript entries and compute pending status at the current UTC time. If initially unarmed and active-stop is true, perform the single retry protocol and recompute from the replacement entry list.
2. Compute the latest real-user-turn marker. Load the stored prompt count only when its stored marker equals this marker; otherwise use zero.
3. Detect whether the current turn contains a successful unprompted non-stop arm. Load whether this turn's warning marker is already recorded.
4. Select `ARMED` or `EXCEPTION_UNPROMPTED_ARMED` when pending. When not pending and count is below three, select `PROMPT` or `EXCEPTION_UNPROMPTED_UNARMED`. When not pending and count is at least three, select `EXCEPTION_LAPSE` or `EXCEPTION_UNPROMPTED_LAPSE`.
5. If a violation warning is fresh, attempt to persist its turn marker before selecting the state's fresh-warning edge. For a prompt-family block, attempt to persist count plus one before publishing the reason.
6. Publish exactly the terminal verdict and message effects shown by the graph. Empty allow states emit no response. Lapse allow states emit one user-directed system message; the unprompted lapse includes the violation message only while its warning is fresh.

`OFF` and `FAIL_OPEN` are resolved by earlier edges but are states of the same total machine. Negative, malformed, mismatched-marker, or unreadable count state is recovered as zero; a stored count of at least three selects lapse.

**Rule (Prompt three exits)** · `rule:hooks:prompt-three-exits`

A prompt-family block tells the agent that no wakeup is pending and permits exactly three subsequent classes of exit. First, a successful non-stop `ScheduleWakeup` call after guard feedback makes pending status true at the next evaluation. Second, removal of the project flag selects `OFF` before any other decision. Third, every other next stop remains unarmed, consumes another prompt-count unit, and eventually selects lapse.

The second exit is legitimate whenever the turn is genuinely blocked on the user with nothing in flight. A `stop` scheduler call without flag removal, ordinary prose, a failed or in-flight arm, a malformed delay, and no action at all belong to the third class. No fourth path may reset the count inside the same real user turn.

**Rule (Unprompted-arm violation)** · `rule:hooks:unprompted-arm-violation`

Within the latest real user turn, a successful non-stop `ScheduleWakeup` call is unprompted when it precedes the first guard-feedback entry. Failed and in-flight calls are ignored, and a `stop` call is exempt. Once guard feedback has occurred, later successful arms in that turn are prompted. The violation fact remains true for the turn even if the arm later expires or is cancelled.

The first detected violation in a turn produces one agent-visible correction. If the wakeup remains pending, the correction alone blocks once; the next stop with the recorded warning allows the pulse. If unarmed below the cap, the correction is prepended to the ordinary prompt reason. At lapse, where another block is forbidden, the correction joins the user-directed lapse alarm. A new real user turn resets violation and warning scope; a still-pending arm then becomes a legitimate previous-turn arm and resolves to `ARMED`.

**Rule (Turn-local block cap)** · `rule:hooks:turn-local-block-cap`

The prompt-count cap is the protocol constant three. Only prompt-family blocks increment that deployed counter; an armed unprompted correction block uses the separate once-per-turn warning marker. Consequently, with writable state the deployed transition system permits at most three prompt-family blocks plus one armed correction block in one real user turn. The fourth unarmed evaluation after three prompt blocks must allow as lapse.

Guard feedback and tool-result carrier entries do not create a new turn marker. A real user entry does, causing old count and warning records to be treated as zero and absent without requiring file deletion. Persistence failure must itself take an anti-wedge edge; it may reduce enforcement or emit a diagnostic, but it must not allow an unrecorded counter or warning to repeat blocks without a finite bound.

**Scenario (Heartbeat lapse)** · `scenario:hooks:heartbeat-lapse`

Lapse is detected when the project flag remains present, no wakeup is pending, and the turn's prompt count is at least three. `EXCEPTION_LAPSE` allows the stop and emits a user-directed alarm stating that three prompts produced neither legal exit and the heartbeat is no longer armed. `EXCEPTION_UNPROMPTED_LAPSE` emits the same alarm and, when not already recorded, the unprompted-arm correction; it also allows. Neither state may publish another block.

Recovery occurs on the next real user turn. The changed marker makes count and warning state turn-locally absent, and the transcript is evaluated again. A still-valid prior-turn wakeup selects `ARMED`; an unarmed enabled project re-enters `PROMPT`; removal of the flag selects `OFF`; inability to read the transcript selects `FAIL_OPEN`. Lapse is therefore observable but never absorbing.

**Scenario (Transcript flush race)** · `scenario:hooks:transcript-flush-race`

The race is detected only when the first structural scan finds no pending wakeup and `stop_hook_active` is truthy, meaning this stop follows a hook block. The machine waits exactly 1.0 second, reloads the complete transcript once, samples a new UTC evaluation time, and recomputes pending status. It then continues with the replacement entries whether the verdict is armed or unarmed. There is no loop and no retry on the first unprompted stop.

If the second load is unreadable, recovery is immediate fail-open allow. If it is readable but still lacks a completed arm, normal prompt-count or lapse resolution proceeds. The retry never treats elapsed sleep, result prose, or the active-stop flag as evidence of an arm.

**Scenario (Heartbeat fail-open)** · `scenario:hooks:heartbeat-fail-open`

Malformed JSON, a top-level value that is not an object, invalid field types that prevent safe classification, an unreadable or undecodable transcript, and any internal parsing, timestamp, state, or output-composition failure are detected as inability to judge. The terminal state is `FAIL_OPEN`: allow with no block reason, no fabricated pending status, and no lapse or violation message. A syntactically malformed JSONL line inside an otherwise readable transcript is merely skipped and does not fail the complete evaluation.

Recovery is the next stop evaluation after the harness or operator repairs the payload, transcript, or store. Toggle absence remains the earlier `OFF` path. Already readable transcript entries and complete state files are not rewritten on fail-open, and an internal error cannot be converted into a prompt on the assumption that no arm was found.

## Hook evidence · `sec:hooks:hook-evidence`

This division defines evidence at graph-edge, persistence, timing-boundary, and subprocess boundaries. A replacement is judged against complete transition behavior rather than source-code resemblance.

**Verification (Injection transitions)** · `verif:hooks:injection-transitions`

Graph verification enumerates every injection node and edge and proves one terminal path for each of the following classes:

- malformed and nonobject input; each unsupported event; both accepted events; all three fresh sources, both resumed sources, and an unrecognized source;
- global disabled, project disabled, both disabled, main payload, truthy derived identity, null derived identity, and a structural subagent path, including proof that refused paths perform no later read or write;
- missing, unreadable, undecodable, exactly-9,500-byte, oversized-at-stat, and growth-after-stat rulebooks;
- absent, valid, invalid, and stale state; current marker witness present, absent, unreadable, exactly inside the transcript-tail boundary, and just outside it; and digest/stamp refresh with no output;
- equal mtime, changed mtime with equal digest, changed digest with and without a current snapshot, and a second change that replaces previous;
- prompt-identity hit and miss, missing and invalid identities, 64-to-65 entry eviction, session-start deltas at zero, 5.0 seconds, greater than 5.0 seconds, and negative wall-clock delta; and
- injected failures before snapshot, between snapshot and state, after state, during logging, during response composition, and after publication begins.

Each fixture asserts semantic verdict, complete captured standard streams and status under hook JSON mode, exact marker or notice when present, log action and redaction, state JSON completeness, snapshot bytes and roles, and absence of forbidden effects. A graph-coverage report must show every edge taken at least once and every node reachable; branch coverage that merges distinct refusal, dedupe, refresh, notice, or fail-open edges is insufficient.

**Verification (Heartbeat transitions)** · `verif:hooks:heartbeat-transitions`

Graph and subprocess fixtures cover `OFF`, `FAIL_OPEN`, `ARMED`, `PROMPT`, all four exception states, and every fresh-warning and already-warned edge. The structural matrix includes successful, failed, in-flight, stopped, malformed- delay, and untimestamped calls; result-before-call association; multiple calls; sidechains; rejected naive, zero-offset and nonzero-offset timestamps (every form without the trailing `Z`), and accepted canonical UTC timestamps with the trailing `Z`; past and future entries; strict expiry; 59/60/3,600/3,601-second delay inputs; 120-second slack; and the 3,720-second horizon boundary. No assertion may inspect result prose.

State fixtures cover absent, malformed, mismatched, negative, zero, two, three, and larger counts; warning absent/present; no real user turn; new real user turn; string and list guard feedback; tool-result carriers; session and project isolation; and write failure for both counter and warning. Transition fixtures exercise all three prompt exits, unprompted arm while pending and after stop or expiry, first and repeated correction, three prompt blocks, the additional armed-correction path, both lapses, and next-turn recovery.

Timing fixtures use a controlled clock and controlled retry so the 1.0-second reload occurs exactly once only on an active post-block unarmed evaluation. Subprocess fixtures separately capture allow, prompt block, correction block, lapse message, malformed stdin, unreadable transcript, invalid field types, and forced internal failure, asserting the hook JSON stream/status contract and absence of traceback or fabricated arm. Edge coverage is complete only when every displayed state-to-verdict edge and every resolution path out of an exception is observed.

**Gate (Hook conformance)** · `gate:hooks:hook-conformance`

A hook implementation or replacement is blocked from deployment until its direct graph inventory, edge-coverage record, persistence fault matrix, controlled-clock timing evidence, and captured subprocess results all agree with this part and the hook JSON contract. Every event must reach exactly one terminal verdict; every graph edge must be exercised; every intentional block must remain distinguishable from fail-open; and every exception must have its declared recovery path.

For a replacement, observational equivalence includes top-level audience filtering, full marker and notice content, deduplication boundaries, snapshot roles, structural scheduler detection, project/session/turn state partition, the complete exception family, and safety under malformed input and failed persistence. A deployed behavior that fails an invariant here is a finding to resolve, not a compatibility behavior to preserve. Unit tests or graph shape alone cannot admit the replacement without subprocess and fault evidence.
