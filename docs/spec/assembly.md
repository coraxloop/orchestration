# Specification assembly manifest · `reg:assembly:specification-assembly`

This manifest declares the seven-part generic specification assembly. The original specification programme is recorded in (`proposal:spec:assembly-and-benchmarks`); command and output contracts belong to the tools specification (`[TOOLS-spec:outputspec:command-and-output-contracts]`). The displayed-head vocabulary follows (`conv:spec:area-vocabulary`) and (`conv:spec:mint-families`), while conformance measures the authored corpus. Every internal participating label minted by this manifest has area `assembly`; the title mint names the register as a document.

## Assembly and outline conventions · `sec:assembly:conventions`

**Convention (Assembly)** · `conv:assembly:assembly`

The following one-column table is the exact membership and owner-approved order of the authored parts. Each part appears exactly once and stands beside this manifest. `docs/spec.md` is the committed generated publication; it is not a part and does not participate in the label calculus.

|Part|
|----|
|`architecture.md`|
|`dispatch.md`|
|`hooks.md`|
|`lanes.md`|
|`server.md`|
|`deployment.md`|
|`conformance.md`|

**Convention (Displayed future-head outline)** · `conv:assembly:displayed-outline`

Every record in the fenced outlines has four fields: kind token, full displayed label, displayed head, and one-line scope. Fencing makes all of these records displayed material: they neither mint nor cite. A `sec` record is a division; all other records are named environments. Each displayed label occurs once and uses the conceptual-home area of its part. Shape measurement ranges over the whole subscribed corpus rather than selecting benchmark documents from these outlines.

## Architecture and authority outline · `sec:assembly:architecture-outline`

Part: `docs/spec/architecture.md`. It fixes the system boundary, actors, authority layers, instruction audiences, harness boundaries, trust domains, mutable-state ownership, and host/server direction without freezing registry facts that the accepted concept leaves mutable.

```text
sec | sec:architecture:purpose-and-boundary | Purpose and boundary | Delimit the orchestration system from lane application work and model-provider internals.
sec | sec:architecture:actors-and-roles | Actors and roles | Organize the actors, their responsibilities, and their owned decisions.
sec | sec:architecture:authority-layers | Authority layers | Organize precedence across machine rules, orchestration policy, charters, briefs, runbooks, and executables.
sec | sec:architecture:harness-boundaries | Harness boundaries | Organize the distinct Claude and Codex instruction and launch surfaces.
sec | sec:architecture:trust-and-state | Trust and state | Organize trust domains, information flow, and mutable-state ownership.
sec | sec:architecture:architecture-evidence | Architecture evidence | Organize the architecture-specific acceptance evidence.
def | def:architecture:system-subject | Definition (System subject) | Define the orchestration system whose behavior the specification governs.
def | def:architecture:orchestrator | Definition (Orchestrator) | Define the top-level coordinator that dispatches, reviews, integrates, and gates work.
def | def:architecture:worker | Definition (Worker) | Define a dispatched execution context governed by a harness charter and a brief.
def | def:architecture:harness | Definition (Harness) | Define the provider-specific surface that launches and resumes a worker.
def | def:architecture:compute-server | Definition (Compute server) | Define the untrusted shared execution domain used for routine computation.
def | def:architecture:trusted-host | Definition (Trusted host) | Define the authoritative domain that reviews returned material and records final verdicts.
term | term:architecture:authority | Terminology (Authority) | Fix authority as the right to decide a class of facts rather than mere access to them.
term | term:architecture:evidence | Terminology (Evidence) | Fix evidence as reviewable output that supports but does not itself issue a trusted verdict.
sig | sig:architecture:actor-roles | Signature (Actor roles) | Name the role relation between orchestrator, worker, harness, server, and corpus owner.
sig | sig:architecture:instruction-surfaces | Signature (Instruction surfaces) | Name the rule-bearing surfaces and the audiences to which each is delivered.
tab | tab:architecture:actor-responsibilities | Table (Actor responsibilities) | Map each actor to its duties, prohibited duties, and authoritative outputs.
diag | diag:architecture:trust-domains | Diagram (Trust domains) | Show the trusted host, harness contexts, shared server, and one-way review boundary.
inv | inv:architecture:layered-authority | Invariant (Layered authority) | Preserve the deployed split among machine facts, orchestration policy, charters, briefs, runbooks, and code.
rule | rule:architecture:machine-facts-precede | Rule (Machine facts precede) | Give universal machine constraints precedence within every instruction audience they govern.
rule | rule:architecture:orchestration-policy-owner | Rule (Orchestration policy owner) | Assign dispatch and supervision policy to the specification parts and deliver their location through the orchestrator-only rulebook.
rule | rule:architecture:charter-plus-brief | Rule (Charter plus brief) | Limit a worker's standing authority to its harness charter plus its dispatched brief.
rule | rule:architecture:audience-separation | Rule (Audience separation) | Prevent an instruction surface from being discovered or injected into an unintended audience.
inv | inv:architecture:two-harnesses-one-evidence-path | Invariant (Two harnesses, one evidence path) | Require both harnesses to return evidence to the same reviewing orchestrator.
spec | spec:architecture:claude-harness-boundary | Specification (Claude harness boundary) | Specify the Claude worker's launch, instruction, callback, and transcript boundary at system level.
spec | spec:architecture:codex-harness-boundary | Specification (Codex harness boundary) | Specify the Codex lane's launch, resume, charter, run-directory, and report boundary at system level.
req | req:architecture:harness-equivalent-outcomes | Requirement (Harness-equivalent outcomes) | Require equivalent review evidence despite provider-specific execution mechanics.
rule | rule:architecture:mutable-state-ownership | Rule (Mutable-state ownership) | Assign every mutable state file or registry to exactly one maintaining authority.
rule | rule:architecture:host-to-server-direction | Rule (Host-to-server direction) | Permit authoritative source to flow from the trusted host into the compute domain only.
rule | rule:architecture:server-results-are-data | Rule (Server results are data) | Treat every artifact returning from the server as untrusted data pending review.
proto | proto:architecture:returned-evidence-review | Protocol (Returned evidence review) | Sequence quarantine, textual inspection, local integration, and trusted verification.
req | req:architecture:quarantined-import | Requirement (Quarantined import) | Require returned source history to land in isolated references before integration.
inv | inv:architecture:trusted-final-gate | Invariant (Trusted final gate) | Keep the verdict of record on reviewed host state regardless of server-green evidence.
rule | rule:architecture:dynamic-facts-stay-in-registries | Rule (Dynamic facts stay in registries) | Keep rosters, budgets, identities, and toolchain versions out of normative specification prose.
rule | rule:architecture:stable-constraints-govern-registries | Rule (Stable constraints govern registries) | State the durable requirements that mutable registries and runbooks must satisfy.
rule | rule:architecture:external-contract-stability | Rule (External contract stability) | Hold streams, exit meanings, and final report lines stable across implementation changes.
proto | proto:architecture:internal-state-migration | Protocol (Internal state migration) | Permit internal state-shape change only through an explicit declared migration path.
req | req:architecture:migration-declaration | Requirement (Migration declaration) | Require compatibility scope, conversion, rollback, and evidence for every internal-state migration.
scenario | scenario:architecture:instruction-surface-contamination | Scenario (Instruction-surface contamination) | Specify detection and recovery when a rulebook reaches a worker or the wrong harness.
scenario | scenario:architecture:stale-machine-fact | Scenario (Stale machine fact) | Specify reconciliation when a charter or runbook drifts from governing machine facts.
verif | verif:architecture:authority-matrix | Verification (Authority matrix) | Recompute every governed fact against its owner, audience, and precedence layer.
gate | gate:architecture:architecture-conformance | Gate (Architecture conformance) | Block publication until every part respects the actor, authority, audience, and trust partition.
```

## Dispatch and supervision outline · `sec:assembly:dispatch-outline`

Part: `docs/spec/dispatch.md`. It owns worker selection, explicit dispatch declarations, read-back gating, callback-led supervision, degraded operation, recovery, and terminal dispatch outcomes.

```text
sec | sec:dispatch:scope | Scope | Delimit dispatch and supervision from worker execution and hook implementation.
sec | sec:dispatch:selection | Worker selection | Organize task weight, rosters, and Sonnet watcher exceptions.
sec | sec:dispatch:gated-dispatch | Gated dispatch | Organize declarations, read-back, correction, and proceed authorization.
sec | sec:dispatch:supervision | Supervision | Organize callbacks, heartbeat measurements, and stall response.
sec | sec:dispatch:owner-interface | Owner interface | Organize questions, commands, presentations, and transcript extraction addressed to the owner.
sec | sec:dispatch:degraded-operation | Degraded operation | Organize deliberate degradation, probing, recovery, and terminal failure.
def | def:dispatch:dispatch | Definition (Dispatch) | Define one bounded assignment of work to one selected worker context.
def | def:dispatch:worker-tier | Definition (Worker tier) | Define a roster position by capability and operating mode rather than by mutable model value.
term | term:dispatch:normal-mode | Terminology (Normal mode) | Name operation using the owner-approved primary capability roster.
term | term:dispatch:degraded-mode | Terminology (Degraded mode) | Name the recorded impairment state whose degraded roster names no producing tier; observation stays with the Sonnet watcher role.
term | term:dispatch:follower-task | Terminology (Sonnet watcher task) | Name auxiliary observation work that tracks a producing lane without owning its deliverable.
sig | sig:dispatch:dispatch-declaration | Signature (Dispatch declaration) | Fix the required model, reasoning depth, read-back policy, scope, and report fields of a brief.
tab | tab:dispatch:role-roster | Table (Role roster) | Map task classes to normal-tier and Sonnet watcher roles without embedding current model names.
rule | rule:dispatch:explicit-model | Rule (Explicit model) | Require every dispatch to state its selected model rather than inherit one.
rule | rule:dispatch:explicit-reasoning | Rule (Explicit reasoning depth) | Require every dispatch to state its intended reasoning depth.
rule | rule:dispatch:explicit-read-back | Rule (Explicit read-back policy) | Require every dispatch to state whether work is gated after the first restatement.
rule | rule:dispatch:task-weight-selection | Rule (Task-weight selection) | Select worker capability from the bounded bite's judgment and verification burden.
rule | rule:dispatch:follower-exception | Rule (Sonnet watcher exception) | Permit the Sonnet watcher role in normal operation only for non-deliverable tracking work.
req | req:dispatch:manufactured-bite | Requirement (Manufactured bite) | Require exact scope, files, constraints, verification, and report shape before launch.
proto | proto:dispatch:read-back-gate | Protocol (Read-back gate) | Sequence first-output restatement, audit, correction if needed, and explicit proceed.
scenario | scenario:dispatch:read-back-correction | Scenario (Read-back correction) | Split or promote a bite after the permitted correction still misses its contract.
rule | rule:dispatch:gated-tier-audit | Rule (Gated-tier audit) | Require diff review and independent claim recomputation for gated workers.
rule | rule:dispatch:no-background-task-chips | Rule (No background-task chips) | Route follow-up work into the project backlog instead of spawning untracked task chips.
listing | listing:dispatch:brief-opener | Listing (Brief opener) | Fix the first line of every brief that invokes the read-back gate.
conv | conv:dispatch:two-commit-tracks | Convention (Two commit tracks) | Separate ungated squash commits from a budget of gated named commits.
inv | inv:dispatch:callbacks-before-watchdog | Invariant (Callbacks before watchdog) | Bind lane results to their Sonnet watcher and loop letters to the independent inbox watcher; heartbeat wakeups check watchers only.
proto | proto:dispatch:inbox-watcher | Protocol (Loop inbox watcher) | Keep an inbox watcher active independently of heartbeat, with bounded blocking calls, held metadata and once-only hand-backs.
proto | proto:dispatch:heartbeat-supervision | Protocol (Heartbeat supervision) | Check only each live lane’s watcher for liveness, absolute UTC deadlines and complete duty coverage.
req | req:dispatch:progress-measurement | Requirement (Progress measurement) | Record source, size, time, and comparison basis for every liveness judgment.
scenario | scenario:dispatch:stalled-worker | Scenario (Stalled worker) | Reverify the worktree, resume promptly, and request small durable increments after no growth.
scenario | scenario:dispatch:log-eater-loss | Scenario (Sonnet watcher loss) | Resume and correct a live watcher by message; replace only a dead watcher after stopping its tool process, and report instruction-linked friction.
proto | proto:dispatch:log-eater-callback | Protocol (Sonnet watcher callback) | Assign every step and gate duty to the lane’s continuing Sonnet watcher, which owns waiting, relay and absolute UTC deadlines and hands each result back once.
rule | rule:dispatch:timing-led-decisions | Rule (Timing-led decisions) | Decide with measured durations, report civil instants as explicit UTC, and treat overruns or missing timings as findings.
rule | rule:dispatch:turn-end | Rule (Turn end) | End an orchestrator turn only at task completion or when blocked on the user.
proto | proto:dispatch:owner-questions | Protocol (Questions to the owner) | Shape an owner question in four parts so it is answered at a glance or safely left.
req | req:dispatch:owner-commands | Requirement (Owner commands) | Hand the owner fully qualified, self-verifying commands judged from pasted output.
rule | rule:dispatch:user-presentations | Rule (User presentations) | Present to the user as a standalone HTML file rather than a harness artifact.
rule | rule:dispatch:transcript-extraction | Rule (Transcript extraction) | Extract pasted chat bytes from the session transcript rather than retyping them.
proto | proto:dispatch:degraded-mode-entry | Protocol (Degraded-mode entry) | Record the failure, stamp degraded state, and choose a healthy disposition deliberately.
rule | rule:dispatch:within-vendor-degradation | Rule (Within-vendor degradation) | The impaired vendor's degraded roster names no producing tier; observation stays with the Sonnet watcher role.
rule | rule:dispatch:cross-vendor-normal | Rule (Cross-vendor normal tier) | Answer isolated impairment with the other vendor's normal tier rather than a smaller producer.
proto | proto:dispatch:normal-tier-probe | Protocol (Normal-tier probe) | Periodically retry the normal tier and clear degraded state on demonstrated recovery.
scenario | scenario:dispatch:terminal-worker-failure | Scenario (Terminal worker failure) | Stop retrying only at a defined terminal condition and preserve the evidence gathered.
verif | verif:dispatch:dispatch-record | Verification (Dispatch record) | Check that declarations, gate events, timings, callbacks, and terminal status agree.
gate | gate:dispatch:dispatch-completion | Gate (Dispatch completion) | Accept a dispatch only when its scoped deliverable and report contract are both satisfied.
```

## Hook state-machines outline · `sec:assembly:hooks-outline`

Part: `docs/spec/hooks.md`. It models both deployed hook machines as states, inputs, transitions, outputs, persistence, timing bounds, deduplication, exceptional paths, and fail-open behavior.

```text
rule | rule:hooks:letters-context | Rule (Letters context) | Define the stateless bounded inbox tail as the second notification route, without delivery receipts.
sec | sec:hooks:scope | Scope | Delimit hook behavior from orchestration policy and worker lifecycle.
sec | sec:hooks:shared-machine-contract | Shared machine contract | Organize graph representation, inputs, persistence, outputs, and safety posture.
sec | sec:hooks:orchestration-injection | Orchestration injection | Organize the top-level rulebook injection state machine.
sec | sec:hooks:heartbeat-guard | Heartbeat guard | Organize the stop-hook heartbeat state machine.
sec | sec:hooks:hook-evidence | Hook evidence | Organize transition, subprocess, persistence, and timing verification.
def | def:hooks:hook-machine | Definition (Hook machine) | Define a harness callback as a total state transition with a protocol-owned verdict.
sig | sig:hooks:hook-event | Signature (Hook event) | Name the common event payload, persisted state, emitted output, and elapsed-time fields.
def | def:hooks:hook-state-store | Definition (Hook state store) | Define per-session and per-project state whose ownership belongs to the hook implementation.
rule | rule:hooks:direct-state-graph | Rule (Direct state graph) | Require each hook machine to be represented directly as explicit graph nodes and edges.
inv | inv:hooks:fail-open-safety | Invariant (Fail-open safety) | Prevent malformed input, unreadable state, or internal failure from wedging the harness.
req | req:hooks:redacted-diagnostics | Requirement (Redacted diagnostics) | Keep persisted and emitted operational errors structured and free of classified values.
sig | sig:hooks:injection-input | Signature (Injection input) | Define accepted hook events, source classes, session identity, prompt identity, cwd, and transcript path.
sig | sig:hooks:scope-marker | Signature (Scope marker) | Define the digest and modification stamp that identify an injected rulebook edition.
diag | diag:hooks:injection-state-machine | Diagram (Injection state machine) | Display fresh, resumed, present, changed, disabled, refused, and fail-open transitions.
rule | rule:hooks:top-level-only | Rule (Top-level only) | Refuse injection into subagents or sidechain transcripts.
rule | rule:hooks:disable-precedence | Rule (Disable precedence) | Honor global and project disable state before reading or injecting the rulebook.
rule | rule:hooks:rulebook-size-bound | Rule (Rulebook size bound) | Refuse a rulebook exceeding the stable maximum before reading it into context.
inv | inv:hooks:exactly-once-in-context | Invariant (Exactly once in context) | Keep one current scope marker in a top-level session without repeat injection.
proto | proto:hooks:fresh-session-injection | Protocol (Fresh-session injection) | Read, snapshot, mark, persist, log, and emit the full rulebook on a fresh source.
proto | proto:hooks:resumed-session-reconciliation | Protocol (Resumed-session reconciliation) | Reinject only when state or the transcript lacks the current marker.
proto | proto:hooks:prompt-deduplication | Protocol (Prompt deduplication) | Bound remembered prompt identifiers and suppress repeat output for one prompt.
proto | proto:hooks:rulebook-change-notice | Protocol (Rulebook change notice) | Rotate snapshots and emit a diff instruction when content changes after injection.
req | req:hooks:atomic-state-write | Requirement (Atomic state write) | Replace complete temporary state so crashes cannot leave a torn session record.
req | req:hooks:snapshot-rotation | Requirement (Snapshot rotation) | Retain current and previous bytes needed for a named rulebook diff.
scenario | scenario:hooks:rulebook-refusal | Scenario (Rulebook refusal) | Log and allow when the rulebook is missing, unreadable, undecodable, or oversized.
scenario | scenario:hooks:injection-internal-error | Scenario (Injection internal error) | Log a redacted internal-error class, emit no protocol corruption, and allow.
verif | verif:hooks:injection-transitions | Verification (Injection transitions) | Exercise every event, source, marker, state, deduplication, change, and refusal edge.
sig | sig:hooks:stop-input | Signature (Stop input) | Define toggle state, transcript, session, stop-active flag, and evaluation time.
def | def:hooks:pending-wakeup | Definition (Pending wakeup) | Define pending status from the latest successfully completed structural scheduling call.
diag | diag:hooks:heartbeat-state-machine | Diagram (Heartbeat state machine) | Display off, fail-open, armed, prompt, and the complete exception family.
rule | rule:hooks:structural-wakeup-detection | Rule (Structural wakeup detection) | Derive armedness from call input, result success, transcript time, clamp, slack, and horizon.
rule | rule:hooks:per-project-heartbeat-toggle | Rule (Per-project heartbeat toggle) | Apply guard enforcement only while the current project's flag is present.
proto | proto:hooks:heartbeat-state-resolution | Protocol (Heartbeat state resolution) | Resolve violation status, armedness, and turn-local block count into exactly one state.
rule | rule:hooks:prompt-three-exits | Rule (Prompt three exits) | Allow only prompted rearm, explicit heartbeat-off, or bounded lapse from a prompt.
rule | rule:hooks:unprompted-arm-violation | Rule (Unprompted-arm violation) | Deliver one agent-visible correction per user turn for a successful premature arm.
rule | rule:hooks:turn-local-block-cap | Rule (Turn-local block cap) | Bound repeated blocks so the guard cannot trap a session indefinitely.
scenario | scenario:hooks:heartbeat-lapse | Scenario (Heartbeat lapse) | Allow after the cap, alarm the user, and reset the exception on the next real user turn.
scenario | scenario:hooks:transcript-flush-race | Scenario (Transcript flush race) | Retry once after a post-block stop before concluding that a prompted arm is absent.
scenario | scenario:hooks:heartbeat-fail-open | Scenario (Heartbeat fail-open) | Allow malformed stdin or an unreadable transcript without fabricating armed state.
verif | verif:hooks:heartbeat-transitions | Verification (Heartbeat transitions) | Cover every regular and exceptional state, verdict, persistence scope, and resolution path.
gate | gate:hooks:hook-conformance | Gate (Hook conformance) | Block replacement until graph and subprocess evidence match deployed behavior and safety.
```

## Worker-lane lifecycle outline · `sec:assembly:lanes-outline`

Part: `docs/spec/lanes.md`. It owns fresh launch, gated resume, work and verification steps, run evidence, budgets, offsets, watchers, stalls, runaways, completion markers, and terminal reports.

```text
sec | sec:lanes:scope | Scope | Delimit lane execution from dispatch selection and server execution.
sec | sec:lanes:launch-and-gate | Launch and gate | Organize fresh creation, first output, proceed, and resume.
sec | sec:lanes:work-and-verification | Work and verification | Organize work steps, verify rounds, corrections, and evidence.
sec | sec:lanes:observation-and-recovery | Observation and recovery | Organize event growth, capture offsets, diagnostic verdicts, stalls, and runaways.
sec | sec:lanes:completion | Completion | Organize step markers, reports, budgets, and terminal acceptance.
def | def:lanes:lane | Definition (Lane) | Define one durable dispatched Codex execution with a run directory and resumable thread.
def | def:lanes:run-directory | Definition (Run directory) | Define the durable evidence root for events, reports, messages, offsets, and step state.
sig | sig:lanes:event-stream | Signature (Event stream) | Define the append-only event record consumed by capture tools and Sonnet watchers.
def | def:lanes:lifecycle-step | Definition (Lifecycle step) | Define a launch, work, or verification step with one owning process and terminal record.
def | def:lanes:budget | Definition (Budget) | Define expected wall time plus tolerance for a lane or recurring step.
term | term:lanes:fresh-launch | Terminology (Fresh launch) | Name creation of a new run directory and thread from an audited brief.
term | term:lanes:gated-resume | Terminology (Gated resume) | Name continuation of the same thread after explicit proceed or verify feedback.
proto | proto:lanes:fresh-launch | Protocol (Fresh launch) | Create the run, record declarations, start the worker, and capture its first output.
proto | proto:lanes:read-back-resume | Protocol (Read-back resume) | Deliver proceed to the recorded thread only after the restatement passes audit.
req | req:lanes:read-back-evidence | Requirement (Read-back evidence) | Preserve the restatement and proceed event in the run evidence.
rule | rule:lanes:run-isolation | Rule (Run isolation) | Keep each lane's mutable evidence and execution state in its own run directory.
rule | rule:lanes:append-only-events | Rule (Append-only events) | Grow event evidence monotonically and never rewrite bytes already offered to capture consumers.
proto | proto:lanes:work-step | Protocol (Work step) | Resume the thread with scoped instructions and collect its report without changing the brief.
proto | proto:lanes:ready-for-verify | Protocol (Ready for verify) | End implementation work with the exact handoff that requests orchestrator-run verification.
proto | proto:lanes:verify-feedback | Protocol (Verify feedback) | Return the build-machine evidence tail to the same thread for bounded correction.
rule | rule:lanes:verify-round-accounting | Rule (Verify-round accounting) | Count every verify request and record what each non-green round found.
rule | rule:lanes:step-owned-marker | Rule (Step-owned marker) | Permit only the process owning a step to create that step's completion marker.
inv | inv:lanes:marker-after-evidence | Invariant (Marker after evidence) | Publish completion only after event, report, and last-message writes have settled.
term | term:lanes:wall-time-classification | Terminology (Wall-time classification) | Distinguish within-budget, over-budget, stalled, runaway, and terminal durations.
rule | rule:lanes:budget-overrun | Rule (Budget overrun) | Report elapsed time beyond budget as a finding rather than silently accepting it.
rule | rule:lanes:runaway-termination | Rule (Runaway termination) | Stop execution that exceeds its declared runaway bound while preserving evidence.
scenario | scenario:lanes:stalled-step | Scenario (Stalled step) | Confirm non-growth, classify the stall, and resume or replace according to step state.
scenario | scenario:lanes:missing-worktree-after-stall | Scenario (Missing worktree after stall) | Recreate an auto-cleaned empty worktree from the integration base before resuming.
proto | proto:lanes:watcher-probe | Protocol (Lane diagnostic probe) | Inspect event growth, marker state, process state, and report availability without consuming output.
spec | spec:lanes:watcher-verdicts | Specification (Watcher verdicts) | Define running, completed, failed, and stalled watcher meanings independently of prose.
def | def:lanes:feeder-offset | Definition (Capture offset) | Define the durable byte position from which the next capture delta begins.
proto | proto:lanes:feeder-delta | Protocol (Capture delta) | Emit bounded new event bytes and advance the offset only for accepted output.
proto | proto:lanes:feeder-completion | Protocol (Capture completion) | Emit terminal report bytes and optional last-message bytes after the lane settles.
rule | rule:lanes:log-eater-replacement | Rule (Sonnet watcher replacement) | Resume live watchers by message and replace only dead watchers after tool cleanup, preserving duties and evidence.
rule | rule:lanes:terminal-condition | Rule (Terminal condition) | End persistence only on verified completion, explicit user block, or defined unrecoverable failure.
spec | spec:lanes:final-lane-report | Specification (Final lane report) | Require scope result, deviations, verification rounds, findings, and per-step timings.
verif | verif:lanes:lifecycle-replay | Verification (Lifecycle replay) | Reconstruct state from one run directory and prove launch, resumes, offsets, and markers agree.
gate | gate:lanes:lane-completion | Gate (Lane completion) | Accept a lane only when the requested outcome and terminal evidence are both present.
```

## Server execution and trust outline · `sec:assembly:server-outline`

Part: `docs/spec/server.md`. It owns stable shared-instance constraints, account isolation, ephemeral recovery, toolchain and cache layout, server-first execution, hub transport, advisory evidence, space reporting, and reviewed return flow; mutable registry values remain outside the specification.

```text
sec | sec:server:scope | Scope | Delimit stable server execution rules from mutable registry facts and host deployment.
sec | sec:server:identity-and-isolation | Identity and isolation | Organize aliases, accounts, credentials, and management boundaries.
sec | sec:server:bootstrap-and-storage | Bootstrap and storage | Organize ephemeral recovery, toolchains, loop directories, caches, and disk management.
sec | sec:server:execution-and-reporting | Execution and reporting | Organize server-first runs, wrapper evidence, priority, budgets, and callbacks.
sec | sec:server:hub-and-trust | Hub and trust | Organize source transfer, returned data, quarantine, review, and trusted verdicts.
def | def:server:shared-instance | Definition (Shared instance) | Define a compute host whose resources and lifecycle are shared across isolated loops.
def | def:server:loop-account | Definition (Loop account) | Define the Unix identity and private mutable workspace assigned to one superloop.
def | def:server:server-registry | Definition (Server registry) | Define the mutable runbook that owns aliases, capabilities, restrictions, and current identities.
def | def:server:git-hub | Definition (Git hub) | Define the bare server repository used only as a branch transport boundary.
def | def:server:quarantined-reference | Definition (Quarantined reference) | Define a host-side ref namespace that cannot become trusted state without review.
rule | rule:server:alias-only-addressing | Rule (Alias-only addressing) | Keep raw network addresses and ports out of repository prose and command contracts.
rule | rule:server:management-account-boundary | Rule (Management-account boundary) | Reserve the privileged account for bootstrap and account administration.
inv | inv:server:per-loop-isolation | Invariant (Per-loop isolation) | Give every superloop its own account, home, work directory, cache, and credentials.
proto | proto:server:ephemeral-bootstrap | Protocol (Ephemeral bootstrap) | Restore accounts, keys, loop roots, shared tools, and hub state from trusted host inputs.
req | req:server:idempotent-bootstrap | Requirement (Idempotent bootstrap) | Permit safe reapplication after restart or partial setup without duplicating state.
rule | rule:server:host-is-restore-source | Rule (Host is restore source) | Treat the trusted host as the source of record for every ephemeral server replacement.
rule | rule:server:shared-toolchains-private-caches | Rule (Shared toolchains, private caches) | Share immutable toolchains while keeping package caches and build targets loop-owned.
rule | rule:server:disk-backed-workspace | Rule (Disk-backed workspace) | Place large work, temporary data, and caches under the assigned persistent-size workspace surface.
rule | rule:server:disposable-build-artifacts | Rule (Disposable build artifacts) | Permit removal of loop-owned targets while protecting shared tools and source evidence.
rule | rule:server:server-first-computation | Rule (Server-first computation) | Send routine builds, tests, and heavy checks to the compute domain.
rule | rule:server:minimum-build-priority | Rule (Minimum build priority) | Run batch build workloads at the lowest scheduling priority available in the domain.
rule | rule:server:lighter-node-placement | Rule (Lighter-node placement) | Place each launch on the lighter registered node by current load.
spec | spec:server:run-wrapper | Specification (Run wrapper) | Require every server command to relay child evidence and append the stable terminal report.
req | req:server:wall-and-space-reporting | Requirement (Wall and space reporting) | Record exit, elapsed wall time, temporary-space remainder, and workspace remainder.
rule | rule:server:gateway-served-iteration | Rule (Gateway-served iteration) | Run a Rust-iterating lane's server rounds through the registered lane gateway.
rule | rule:server:budgeted-server-run | Rule (Budgeted server run) | Give every recurring server action an expected duration and tolerance.
proto | proto:server:remote-callback | Protocol (Remote callback) | Launch detached work assigned to the lane's Sonnet watcher, which hands back completion, silence or the absolute UTC deadline.
scenario | scenario:server:silent-remote-job | Scenario (Silent remote job) | Classify a job as stalled after the declared interval without log movement and return evidence.
proto | proto:server:host-to-hub-flow | Protocol (Host-to-hub flow) | Push reviewed host source to the loop hub and update the isolated server clone.
proto | proto:server:hub-to-quarantine-flow | Protocol (Hub-to-quarantine flow) | Fetch server-authored commits into isolated host refs without executing them.
rule | rule:server:returned-material-is-data | Rule (Returned material is data) | Forbid execution, sourcing, or building of returned material before textual review.
proto | proto:server:return-review | Protocol (Return review) | Inspect diffs and executable build surfaces before integrating selected commits.
rule | rule:server:server-green-is-advisory | Rule (Server-green is advisory) | Treat a successful server run as evidence rather than the verdict of record.
verif | verif:server:server-evidence | Verification (Server evidence) | Check wrapper fields, space values, callback movement, hub refs, and review provenance.
gate | gate:server:trusted-host-verdict | Gate (Trusted-host verdict) | Require final verification over reviewed host state before release or deployment.
```

## Build and deployment topology outline · `sec:assembly:deployment-outline`

Part: `docs/spec/deployment.md`. It owns the agent execution environment, execution-domain selection, dedicated tool containers, minimum build priority, contention interpretation, routine toolchains and formatter resolution. Tool construction and installation contracts belong to (`[TOOLS-spec:deployment:tool-build-and-install-contracts]`).

```text
sec | sec:deployment:scope | Scope | Delimit agent execution environments and orchestrator build conduct from tool construction and installation.
sec | sec:deployment:build-domains | Build domains | Organize execution-domain selection, containers, priority and routine toolchains.
def | def:deployment:agent-container | Definition (Agent container) | Define the toolbox container in which an agent's shell runs on the trusted host.
rule | rule:deployment:build-where-executed | Rule (Build where executed) | Build server binaries on the server and host binaries in the trusted host domain.
rule | rule:deployment:dedicated-tool-containers | Rule (Dedicated tool containers) | Run a tool the host lacks in a registered dedicated toolbox, never on the host.
rule | rule:deployment:minimum-build-priority | Rule (Minimum build priority) | Place every compile and rebuilding gate in the lowest-priority scheduling class.
rem | rem:deployment:contention-slowdown | Remark (Contention slowdown) | Treat a build slowed by interactive contention as the priority rule working.
conv | conv:deployment:routine-toolchain | Convention (Routine toolchain) | Run routine Rust work on one designated toolchain and reserve stable runs for releases.
hint | hint:deployment:formatter-resolution | Hint (Formatter resolution) | Invoke the formatter binary form so the formatter on the path is the one that runs.
```

## Conformance and evidence outline · `sec:assembly:conformance-outline`

Part: `docs/spec/conformance.md`. It owns requirement-to-evidence links, label participation and resolution, owner reach, generic assembly freshness, whole-corpus measurement, burn-ratchet principles, server verification and trusted gates. Linter construction and verification contracts, including the historical census and frontier campaign, belong to (`[TOOLS-spec:conformance:linter-conformance]`).

```text
sec | sec:conformance:scope | Scope | Delimit conformance evidence from the operational requirements it evaluates.
sec | sec:conformance:calculus-and-ownership | Calculus and ownership | Organize participation, heads, mints, citations, owners, and reach.
sec | sec:conformance:assembly-and-shape | Assembly and shape | Organize membership, freshness, whole-corpus measurement, and division separation.
sec | sec:conformance:reports-and-ratchets | Reports and ratchets | Organize the burn-ratchet principle and point the report and register checks to the imported contracts.
sec | sec:conformance:trusted-gates | Trusted gates | Organize server verification, the historical frontier inventory, and release evidence.
def | def:conformance:conformance-claim | Definition (Conformance claim) | Define a normative statement paired with reproducible evidence and an owning gate.
def | def:conformance:trusted-evidence | Definition (Trusted evidence) | Define evidence produced or recomputed over reviewed authoritative source state.
term | term:conformance:green-check | Terminology (Green check) | Name a check whose declared contract passes without a failing finding.
sig | sig:conformance:requirement-evidence-link | Signature (Requirement-evidence link) | Name requirement, implementation surface, test, execution domain, result, and reviewer.
tab | tab:conformance:conformance-matrix | Table (Conformance matrix) | Map every normative environment to its evidence producer and trusted gate.
inv | inv:conformance:evidence-traceability | Invariant (Evidence traceability) | Require every passing claim to reach current source, test, result, and reviewer identity.
rule | rule:conformance:displayed-material-does-not-participate | Rule (Displayed material does not participate) | Exclude fenced blocks and displayed spans from minting and citation judgments.
req | req:conformance:head-validation | Requirement (Head validation) | Validate every participating authored head against its kind and exact surface form.
req | req:conformance:unique-mints | Requirement (Unique mints) | Require every authored label to mint exactly once within its owner.
req | req:conformance:citation-resolution | Requirement (Citation resolution) | Resolve every participating citation to one live mint in the permitted owner.
req | req:conformance:owner-reach | Requirement (Owner reach) | Admit cross-owner citations only across registered policy or manifest reach edges.
req | req:conformance:assembly-exact-membership | Requirement (Assembly exact membership) | List every accepted part exactly once in owner-approved order and no other file.
req | req:conformance:assembly-live-state | Requirement (Assembly live state) | Require removal of the draft marker only after all accepted parts exist.
req | req:conformance:assembly-freshness | Requirement (Assembly freshness) | Compare the committed publication to the exact generated concatenation.
rule | rule:conformance:generated-publication-nonparticipation | Rule (Generated publication nonparticipation) | Exclude assembled output so its copied heads do not mint twice.
req | req:conformance:whole-corpus-shape | Requirement (Whole-corpus shape) | Measure every participating authored document in the subscribed carrier without a benchmark set.
req | req:conformance:division-separation | Requirement (Division separation) | Measure divisions separately and exclude them from named-environment distributions.
def | def:conformance:burn-ratchet | Definition (Burn ratchet) | Define an exact legacy census that fails on both growth and stale registered counts.
proto | proto:conformance:server-verification-loop | Protocol (Server verification loop) | Run format, lint, and scoped tests on reviewed source and return the evidence tail for correction.
rule | rule:conformance:server-green-is-advisory | Rule (Server-green is advisory) | Prevent a successful server loop from substituting for the trusted release verdict.
gate | gate:conformance:trusted-release | Gate (Trusted release) | Require reviewed source, all adopted checks, server evidence, and final host verification.
gate | gate:conformance:specification-conformance | Gate (Specification conformance) | Require the seven-part generic publication and the applicable imported adoption contracts to satisfy their conformance conditions.
```
