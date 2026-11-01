# Lane gateway outage recovery proposal · `proposal:gatewayrecovery:lane-gateway-outage-recovery`

The agent-side watching and waiting recipes retained below, including fresh-agent, never-resume, listener and session-side polling instructions, are superseded by (`proto:dispatch:log-eater-callback`) and (`proto:dispatch:heartbeat-supervision`); program interfaces, historical observations and quoted former instructions remain as recorded.

Status: RATIFIED and IMPLEMENTED — the three-lane split landed, the deployed gateway answers schema two, and the closing outage drill (2026-08-28) verified parking, crash detection, single relaunch with reconciliation, once-only execution of the original sequence, the deregistration guard, explicit abandonment, and clean shutdown end to end on the deployed binary. All five owner questions were resolved per the document's recommendations: expiry only by explicit abandon or lane closeout; the five-second heartbeat cadence with fifteen-second stale threshold; the narrow sequence-stable per-proposal projection; schema-two cutover by draining schema-one lanes where practical and explicitly rebriefing the remainder; deregistration refusing open proposals. This document is a recovery-semantics addendum to the ratified lane gateway design; the three-lane implementation split below governs the in-flight work.

## Purpose, evidence, and boundary · `sec:gatewayrecovery:purpose-evidence-and-boundary`

Backlog entry 22 records a roughly six-hour approval-path outage in which nine consecutive tier-three proposals each reached a registered 1,800-second timeout while the orchestrator was absent, after which the serve loop died and stopped consuming requests. The lane kept polling and retrying correctly; the gateway converted absence into destructive expiry, exposed no dependable daemon-health signal, and collapsed policy denial and unattended timeout into the same lane-visible verdict.

This proposal is a recovery-semantics addendum to the ratified mirror and three-tier gateway design. It preserves exact-argv approval, worker credential isolation, one-way host-to-server trust, gateway writes confined to `.lane/`, single-writer tracked trees, append-only audit evidence, and the final orchestrator gate of record.

The three required outcomes are durable proposal parking, observable and restartable serve-loop liveness, and proposal verdicts that tell a worker whether to stop, wait, or retry. The document intentionally mints no calculus labels and remains a carried but non-participating proposal under the repository's current adoption configuration.

The V2 friction queue remains out of scope. Two narrow overlaps are unavoidable and are named explicitly below: a sequence-stable per-proposal result file is required so durable status cannot be overwritten by unrelated traffic, and restart reconciliation must avoid replacing a recovered proposal status with a replay refusal. This proposal does not absorb quieter push, general sequence-addressed results, `.lane/` snapshot exclusion, cooldown timestamps, or verdict changes outside tier three.

## Durable proposal park · `sec:gatewayrecovery:durable-proposal-park`

Decision: `proposal_timeout_seconds` becomes an attention deadline, not a lifetime deadline. Reaching it changes an unresolved proposal from `pending` to `parked`, preserves the exact argv and reason, keeps approval and denial available under the original sequence, and never asks the worker to re-propose merely because the orchestrator was absent.

This intentionally reverses the current destructive path in `Gateway::expire_lane_proposals_locked` and `Gateway::timeout_proposal_locked`. A second unattended destruction timer would reproduce the outage at a larger interval, so no elapsed wall clock automatically changes `parked` to `expired`.

### State model and persistence · `sec:gatewayrecovery:state-model-and-persistence`

The authoritative states and transitions are:

|State|Meaning|Allowed next state|
|-----|-------|------------------|
|`pending`|The proposal is unresolved and still inside its registered attention window.|`approved`, `denied`, `parked`, or `expired`|
|`parked`|The attention window elapsed without an orchestrator verdict; the proposal remains open and executable.|`approved`, `denied`, or `expired`|
|`approved`|The orchestrator atomically claimed the exact argv for one execution.|Terminal|
|`denied`|The orchestrator made a policy decision not to execute the proposal.|Terminal|
|`expired`|The orchestrator explicitly abandoned the proposal because the lane stopped needing it or entered closeout.|Terminal|

The existing immutable proposal body remains at `<state>/proposals/<lane>/<seq>.json`; it continues to carry lane, sequence, exact argv, exact reason, intake timestamp, and registered attention timeout. A new create-once park marker at `<state>/proposal-parks/<lane>/<seq>.json` carries `schema`, `lane`, `seq`, `parked_unix_ms`, and `attention_timeout_seconds`. A proposal with no terminal resolution is `parked` when this marker exists and otherwise `pending`.

Terminal state remains create-once at `<state>/proposal-verdicts/<lane>/<seq>.json`. Its `ProposalVerdict.decision` is `approved`, `denied`, or `expired`; a newly emitted `expired` state also carries a `ProposalExpiryReason` of `abandoned` or `lane_closed` and the orchestrator's non-blank reason. The old `timed_out` decision is accepted only while decoding schema-one history, maps to decode-only `legacy_timeout`, and is never emitted by the recovery implementation.

The park marker is the authority for the nonterminal transition. `AuditEvent` gains `ProposalParked`, and startup reconciliation appends that event only when the marker has no matching lane-and-sequence event in the audit, then republishes the lane status. A crash after marker creation but before audit or result publication is therefore repaired without changing state or duplicating an audit transition.

The new `ProposalState` enum has `Pending`, `Parked`, `Approved`, `Denied`, and `Expired`; `ProposalPark` represents the park marker; `ProposalExpiryReason` has `Abandoned`, `LaneClosed`, and decode-only `LegacyTimeout`. `PendingProposal` gains `state: ProposalState` and optional `parked_unix_ms` so the existing public queue container can list both open states without a gratuitous type rename.

### Lane polling and orchestrator resume · `sec:gatewayrecovery:lane-polling-and-orchestrator-resume`

Proposal intake atomically publishes the initial status to both `.lane/result.json` and a new canonical `.lane/proposals/<seq>.json`. Every later proposal transition or approved execution republishes both files, but only the sequence-stable file is authoritative for a worker waiting on that proposal; unrelated push and run results may continue to replace `.lane/result.json` without erasing proposal status.

While parked, the canonical file has result schema two, `seq` equal to the original proposal sequence, `operation` equal to `propose`, `verdict` equal to `parked`, exit code zero, the registered `proposal_timeout_seconds`, and no refusal. Its `wall_millis` measures the transition publication rather than the total parked age. The exact schema and worker action table are specified under verdict distinguishability.

The worker must keep polling `.lane/proposals/<seq>.json` and must not create a duplicate proposal while it says `pending` or `parked`. It may continue unrelated push and registered-run traffic because neither open state owns the lane action lock. If the proposal blocks all useful work, the worker waits and reports the parked sequence honestly rather than consuming fresh sequences every attention interval.

When the orchestrator returns, `lane-gateway proposals` lists both pending and parked entries in lane-and-sequence order and includes their state, age, attention timeout, and park timestamp. `approve` and `deny` accept either open state, claim the existing immutable sequence through the terminal marker, and preserve the current exact-once and exact-reason behavior; no re-registration or worker retry is required.

On daemon restart, `Gateway::reconcile_open_proposals` runs before request polling. It scans immutable proposal bodies, park markers, terminal markers, and relevant audit records; creates any overdue park marker; repairs missing audit and canonical lane-status projections; and leaves every terminal proposal untouched. An already accepted request at or below the stored watermark is seeded into the serve loop's `seen` map rather than processed into a replay refusal, while a request above the watermark is consumed normally.

### Bounds and abandonment · `sec:gatewayrecovery:bounds-and-abandonment`

The lane's ordinary wall-budget clock continues while a proposal is pending or parked. Crossing the lane's soft reporting budget remains an over-budget finding and does not revoke an approved capability, matching the existing rule that a worker with continuing activity is allowed to finish; the gateway must not infer terminal authority from that clock.

Active parking is bounded by the registered lane lifecycle and an explicit trusted action, not by another absence-sensitive timer. The CLI gains `lane-gateway abandon LANE SEQ REASON`, which takes the lane lock, accepts pending or parked state, writes an orchestrator-authored `expired` terminal marker, audits it, and publishes an `expired` result. The worker cannot abandon through request JSON and therefore cannot erase approval evidence or manufacture a retryable terminal state.

`Gateway::deregister` must refuse with `GatewayError::OpenProposals` while any proposal is pending or parked. Closeout first abandons every open proposal with reason `lane closed`, then deregisters; immutable proposal, park, terminal, and audit records remain as lane-lifetime evidence for normal archival. This makes indefinite persistence during indefinite orchestrator absence a deliberate safety property while ensuring a consciously closed lane has no live queue entries.

The worker charter tells a lane that a desired abandonment is reported to the orchestrator; until the canonical file changes, the proposal is still open. This prevents local file deletion, a new sequence, or soft-budget expiry from being mistaken for cancellation.

### Implementation surface and tests · `sec:gatewayrecovery:implementation-surface-and-tests`

`packages/lane-gateway/src/types.rs` changes `VerdictDecision`, `ProposalVerdict`, `PendingProposal`, `OperationResult`, `ResultVerdict`, `RefusalRule`, and `AuditEvent`; adds `ProposalState`, `ProposalPark`, and `ProposalExpiryReason`; and retains legacy decoding for `timed_out` audit state without emitting it.

`packages/lane-gateway/src/proposal.rs` changes `Gateway::park_proposal`, `Gateway::proposals`, `Gateway::approve_proposal`, and `Gateway::deny_proposal`; renames `load_pending_proposal` to `load_open_proposal`, `proposal_expired` to `proposal_attention_elapsed`, `expire_lane_proposals_locked` to `park_due_lane_proposals_locked`, and `timeout_proposal_locked` to `park_due_proposal_locked`; and adds `Gateway::abandon_proposal`, `Gateway::reconcile_open_proposals`, `proposal_park_path`, and idempotent projection repair.

`packages/lane-gateway/src/serve.rs` changes `Gateway::serve` and `Gateway::serve_cycle` to reconcile before polling and call the park transition, changes `write_result` to write schema-two results, and adds `write_proposal_result` and `seed_seen_requests` for `.lane/proposals/<seq>.json` and restart replay suppression. `packages/lane-gateway/src/gateway.rs` changes `Gateway::deregister` and `Gateway::ensure_layout`, exposes `Gateway::request_watermark` to replay seeding, and extends `GatewayError`; `packages/lane-gateway/src/bin/lane-gateway.rs` adds the `abandon` action and parser; and `packages/lane-gateway/src/lib.rs` exports the new public types.

The implementation also updates `packages/lane-gateway/README.md`, `packages/lane-gateway/src/README.md`, and `packages/lane-gateway/src/bin/README.md` for the changed contract and test matrices, followed by the deployed copies of `docs/worker-charter.md` and `docs/integration.md` in the Codex repository during the documentation bite.

The exact gateway-state additions are `<state>/proposal-parks/<lane>/<seq>.json`; the exact worker-visible addition is `<worktree>/.lane/proposals/<seq>.json`; and the existing proposal body, terminal marker, audit JSONL, watermark, request, and current result files remain in use.

`packages/lane-gateway/src/tests.rs` must replace `proposal_timeout_refuses_and_fresh_sequence_reproposes` with `proposal_timeout_parks_without_terminal_resolution` and add `parked_proposal_survives_gateway_restart_and_is_approvable`, `proposal_queue_lists_pending_and_parked`, `per_proposal_status_survives_later_push_and_run_results`, `restart_repairs_park_projection_without_replay_refusal`, `explicit_abandon_expires_open_proposal`, `deregister_refuses_open_proposals`, and `legacy_timed_out_state_decodes_as_terminal_history`.

The binary tests in `packages/lane-gateway/src/bin/lane-gateway.rs` must extend `parses_tier_three_cli_surface` for `abandon` and prove that blank reasons and malformed lane/sequence shapes fail before state mutation. Every new test receives its derived label and a row in the appropriate source test matrix.

## Serve-loop liveness · `sec:gatewayrecovery:serve-loop-liveness`

Decision: a serve process is healthy only while it publishes a fresh process heartbeat, and every ordinary serve error or unwind panic is a reported process failure. Session supervision becomes a permanent per-tick contract rather than an outage-only suggestion.

### Heartbeat contract · `sec:gatewayrecovery:heartbeat-contract`

The fixed heartbeat path is `<state>/serve-heartbeat.json`, outside every worker worktree. `ServeConfig` gains `heartbeat_interval_millis`, defaulting to 5,000 and optionally set by positive integer environment variable `LANE_GATEWAY_HEARTBEAT_MILLIS`; three missed default intervals, or 15 seconds, is the runbook's stale threshold.

The heartbeat is strict JSON with independent schema one and fields `schema`, `pid`, `started_unix_ms`, `heartbeat_unix_ms`, `last_activity_unix_ms`, `process_state`, `activity`, and optional `lane` and `seq`. `process_state` is `running` or `stopped`; `activity` is `started`, `request_started`, `result_published`, `proposal_reconciled`, or `clean_shutdown`. No argv, proposal reason, remote, worktree path, command output, or credential-bearing value enters this file.

`last_activity_unix_ms` is initialized at process start, changes immediately before a request begins and after a result or proposal projection is published, and does not change for an idle scan. `heartbeat_unix_ms` changes on every cadence, so a live but idle daemon is distinguishable from a daemon that has not completed useful work.

A dedicated `ServeHeartbeatPublisher` thread writes before the first registration scan and then at every cadence, allowing the heartbeat to remain fresh while the synchronous serve loop waits on a long runner. Main-loop activity updates a shared typed snapshot; heartbeat-thread write or join failure is returned to the supervision boundary as a serve error rather than silently losing liveness.

Each heartbeat is serialized to a create-new sibling temporary file, synced, and atomically renamed over the fixed path. Clean shutdown writes one final `process_state: "stopped"` heartbeat with `activity: "clean_shutdown"` and returns zero; a crash leaves the last `running` heartbeat stale, which is itself actionable evidence.

### Loud crash contract · `sec:gatewayrecovery:loud-crash-contract`

The fixed latest-crash path is `<state>/serve-crash.json`. It is strict JSON with independent schema one and fields `schema`, `pid`, `started_unix_ms`, `failed_unix_ms`, `last_activity_unix_ms`, `failure_kind`, and `message`; `failure_kind` is exactly `error` or `panic`.

For an ordinary `GatewayError`, `message` is the existing safe `Display` string. For an unwind panic, it is the string payload when the payload is `String` or static string and otherwise the fixed text `non-string panic payload`; panic debug representations and request-controlled values are not serialized. A later crash atomically replaces the latest-crash file, while the append-only lane audits and external task transcript remain the historical evidence.

The public `Gateway::serve` becomes the supervision boundary: it starts heartbeat publication, invokes a private `serve_inner` inside `catch_unwind`, stops and joins the publisher, writes the crash report for either returned error or panic, and returns an error. The CLI's existing `Action::Serve` error path emits its machine diagnostic on standard error and returns `CommandExit::Failure`, so both cases exit nonzero.

Failure to write the crash report cannot turn the process green: the CLI emits the original serve failure plus the fixed diagnostic `serve crash report write failed` and still exits nonzero. An uncatchable process kill or machine loss cannot write a report; the stale or missing heartbeat is the required detection path for those cases.

A successful new start does not delete an older crash report. The `pid` and `started_unix_ms` in the fresh heartbeat let the probe determine that the report belongs to an earlier process generation, preserving evidence without declaring the replacement unhealthy.

### Probe and restart discipline · `sec:gatewayrecovery:probe-and-restart-discipline`

The orchestrator must keep the chained proposals waiter described in the current incident mitigation: it polls `lane-gateway proposals` about every 20 seconds for a bounded task lifetime, reports a nonempty queue by task callback, and is replaced immediately whenever the waiter exits. Scheduled orchestrator wakeups are not an approval transport.

On every orchestrator heartbeat tick, and on every waiter callback, the session checks the fixed shutdown flag first. If shutdown is requested, a stopped or absent daemon is expected and no relaunch occurs; otherwise the session reads the heartbeat, checks that `heartbeat_unix_ms` is no older than three configured cadences, and verifies that the recorded pid still names the tracked `lane-gateway serve` process.

A fresh running heartbeat and matching live pid are healthy. A missing heartbeat, stale heartbeat, stopped state without shutdown, dead pid, or completed background task is unhealthy; the session records the latest crash report and task exit, proves that no prior serve process remains, and relaunches immediately with the same state root, runner argv, poll interval, result-size limit, and heartbeat cadence.

If the recorded pid remains live but its heartbeat is stale, the session cancels that tracked background task, waits one heartbeat cadence for exit, and only then launches the replacement; it never starts two serve loops intentionally. The replacement must publish a fresh running heartbeat within one cadence, or the relaunch is reported as a loud repeated failure rather than retried in a blind loop.

Every replacement executes proposal reconciliation before reading request files, so proposals written or parked during the outage resume from gateway state and any request whose sequence is above the durable watermark is consumed. The chained waiter then observes the recovered queue without requiring a scheduled wakeup.

The diagnostic `lane already has an action in flight` from `approve`, `deny`, or `abandon` means exactly retry later. It is neither approval nor denial: the orchestrator waits for the current lane action to finish, reruns the same verdict command, and treats only a successful command plus the terminal marker as evidence that the verdict registered.

### Implementation surface and tests · `sec:gatewayrecovery:implementation-surface-and-tests-2`

`packages/lane-gateway/src/types.rs` adds `ServeHeartbeat`, `ServeProcessState`, `ServeActivity`, `ServeCrashReport`, and `ServeFailureKind`, each with strict fields and its own schema-one constant. `packages/lane-gateway/src/lib.rs` exports the health and crash types needed by the CLI and tests.

`packages/lane-gateway/src/serve.rs` changes `ServeConfig::for_gateway`, `ServeConfig::from_environment`, `ServeConfig::is_valid`, and the accessors for the new cadence; changes `Gateway::serve` into the supervision boundary; moves the current loop to `Gateway::serve_inner`; updates `Gateway::serve_cycle` to publish typed activity; and adds `ServeHeartbeatPublisher`, `supervise_serve`, `write_heartbeat`, `write_crash_report`, and `write_state_json_atomic`.

`packages/lane-gateway/src/gateway.rs` adds the fixed heartbeat and crash path helpers and the `GatewayError` variants `HeartbeatPublisherFailed`, `ServePanicked`, and `CrashReportWriteFailed`. `packages/lane-gateway/src/bin/lane-gateway.rs` keeps `Action::Serve` as the process exit boundary but changes it to preserve both the original failure and any crash-report failure diagnostic.

The exact new on-disk artifacts are `<state>/serve-heartbeat.json` and `<state>/serve-crash.json`; heartbeat temporary files are siblings named `.serve-heartbeat.<pid>.<sequence>.tmp` and are removed on failed publication. No file outside the state root or `.lane/` is written.

`packages/lane-gateway/src/tests.rs` adds `serve_writes_pid_and_last_activity_heartbeat`, `heartbeat_stays_fresh_during_long_runner`, `clean_shutdown_marks_heartbeat_stopped`, `serve_error_writes_crash_report`, `serve_panic_writes_crash_report`, `heartbeat_write_failure_is_fatal`, and `restart_consumes_request_written_while_serve_was_down`. The panic test exercises the private `supervise_serve` closure seam; it does not add a production panic switch.

A new process-contract test `packages/lane-gateway/tests/serve_liveness.rs` adds `serve_error_exits_nonzero_with_crash_report`, and its new `packages/lane-gateway/tests/README.md` carries the derived integration-test label. `packages/lane-gateway/README.md`, `packages/lane-gateway/src/README.md`, and `packages/lane-gateway/src/bin/README.md` gain the heartbeat, crash, environment, restart, and test-matrix contract.

## Verdict distinguishability · `sec:gatewayrecovery:verdict-distinguishability`

Decision: proposal policy and proposal availability are different worker decisions and therefore receive different top-level result verdicts. A worker must not infer them from prose, elapsed time, exit code, or a nested refusal rule.

### Result schema and verdicts · `sec:gatewayrecovery:result-schema-and-verdicts`

`OperationResult` gains a required numeric `schema` field and worker-facing result schema becomes two. The exact `ResultVerdict` spellings are `success`, `pending`, `parked`, `denied`, `expired`, `over_budget`, and `refused`.

The proposal-specific meanings are:

|`verdict`|Terminal|Exit code|Required companion|Meaning|
|-|--------|---------|------------------|-------|
|`pending`|No|0|`proposal_timeout_seconds`|The proposal is open inside its attention window.|
|`parked`|No|0|`proposal_timeout_seconds`|The attention window elapsed, but the original proposal remains open.|
|`denied`|Yes|1|A `proposal_denied` refusal with the orchestrator reason.|The orchestrator rejected the command as policy.|
|`expired`|Yes|1|A `proposal_expired` refusal with `expiry_reason` and the orchestrator reason.|The proposal was explicitly abandoned or the lane closed.|

`refused` remains the verdict for request validation, run admission, runner failure, scope, budget, cooldown, and other non-proposal refusal paths. `success` and `over_budget` retain their current meanings for executed approved proposals, including the current rule that a tool's nonzero exit can accompany gateway-level `success`.

The exact parked projection, apart from its measured values, is:

```json
{"schema":2,"seq":17,"operation":"propose","exit_code":0,"wall_millis":1,"verdict":"parked","proposal_timeout_seconds":1800,"stdout":"","stderr":""}
```

The exact denied projection shape is:

```json
{"schema":2,"seq":17,"operation":"propose","exit_code":1,"wall_millis":1,"verdict":"denied","refusal":{"schema":2,"rule":"proposal_denied","message":"orchestrator denied the proposed command","seq":17,"reason":"outside lane scope"},"stdout":"","stderr":""}
```

The exact expired projection shape is:

```json
{"schema":2,"seq":17,"operation":"propose","exit_code":1,"wall_millis":1,"verdict":"expired","refusal":{"schema":2,"rule":"proposal_expired","message":"proposal was explicitly expired","seq":17,"reason":"lane chose a different approach","expiry_reason":"abandoned"},"stdout":"","stderr":""}
```

Optional fields absent from these examples remain omitted under the current serialization convention, and key order is not semantic. Both `.lane/result.json` and `.lane/proposals/<seq>.json` use the same `OperationResult` bytes when they publish the same transition.

### Worker guidance · `sec:gatewayrecovery:worker-guidance`

For `pending`, the worker waits through the stated attention window, may do unrelated push or registered-run work, and does not resubmit the argv. The status may become approved execution output, `denied`, `parked`, or `expired` under the same sequence.

For `parked`, the worker keeps polling the same `.lane/proposals/<seq>.json`, may continue unrelated work, and does not allocate a replacement sequence. Parking says the orchestrator has not decided; it is never evidence of denial.

For `denied`, the worker reads the reason and does not retry the same command or an equivalent argv under a fresh sequence. It changes approach, uses the pre-cleared roster, or proceeds to the final verify path; only new orchestrator direction can reopen the denied policy choice.

For `expired`, the original sequence is terminal and must not be reused. If the lane is still registered and the command remains necessary, the worker may submit a fresh sequence after accounting for the abandonment reason; a `lane_closed` expiry instead directs it to stop gateway work and report.

For `refused`, the worker continues to follow the typed refusal rule: retry only rules whose contract says retry later, never retry blind, and treat run-cap exhaustion as direction to final verify. The out-of-band CLI diagnostic `lane already has an action in flight` remains orchestrator-facing retry-later state and never becomes a lane proposal verdict.

### Compatibility and versioning · `sec:gatewayrecovery:compatibility-and-versioning`

Result schema two is an intentional breaking change because adding required `schema` and new enum values would be rejected by strict schema-one decoders. Request JSON remains schema one with exactly the existing `push`, `run`, and `propose` shapes, and registration TOML remains schema one; neither worker authority nor the three-tier command boundary changes.

`types.rs` splits the current shared result constant into explicit `REGISTRATION_SCHEMA = 1`, `REQUEST_SCHEMA = 1`, `PROPOSAL_STATE_SCHEMA = 1`, `SERVE_HEALTH_SCHEMA = 1`, `RESULT_SCHEMA = 2`, and `AUDIT_SCHEMA = 2`. New `OperationResult`, `Refusal`, `ProposalQueue`, and audit records emit the appropriate schema; `OperationResult.schema` deserializes an absent field as legacy schema one but every constructor writes two, and the audit reader accepts both audit schemas because an append-only lane log may contain records from before and after deployment.

Existing schema-one immutable proposal bodies and terminal markers remain readable. An unresolved old body becomes pending or parked from its age during reconciliation; an existing schema-one `timed_out` terminal marker remains terminal history and is mapped to expired-with-legacy-timeout for display, never revived automatically, because the outage lane may already have submitted and resolved replacement sequences.

Old `.lane/result.json` files are disposable projections and receive no migration. The first result from the new binary overwrites them with schema two, while each open proposal receives a schema-two canonical file during reconciliation.

Deployment must not mix a schema-two gateway with a worker brief that only understands generic `TIMED-OUT`. The rollout order is binary and state-reader compatibility first, then worker charter and runbook in the same maintenance window, then fresh or explicitly rebriefed registrations; an in-flight schema-one lane is drained or resumed with the new guidance before the new daemon serves it.

### Implementation surface and tests · `sec:gatewayrecovery:implementation-surface-and-tests-3`

`packages/lane-gateway/src/types.rs` adds `OperationResult.schema`, the `Parked`, `Denied`, and `Expired` `ResultVerdict` variants, `RefusalRule::ProposalExpired`, and `Refusal.expiry_reason`; stops emitting `ProposalTimedOut`; and separates request, registration, proposal-state, health, result, and audit schema constants. Every `OperationResult` constructor is changed to set schema two.

`packages/lane-gateway/src/proposal.rs` publishes `pending`, `parked`, `denied`, and `expired` through distinct constructors and keeps approved execution on `success`, `over_budget`, or a typed non-policy `refused`. `packages/lane-gateway/src/serve.rs::write_result` and `write_proposal_result` reject an in-memory result whose schema is not two before touching a worker file.

`packages/lane-gateway/src/gateway.rs::audit_consumption` and the proposal reconciliation reader accept schema-one and schema-two audit records while writers emit schema two. `packages/lane-gateway/src/lib.rs` exports the changed enums, and the package and source READMEs document schema two without changing request examples.

`packages/lane-gateway/src/tests.rs` adds `proposal_result_verdicts_are_distinct`, `schema_two_proposal_result_json_is_exact`, `denied_verdict_is_not_retryable_timeout`, `expired_verdict_allows_fresh_sequence_when_lane_remains_open`, `parked_verdict_keeps_original_sequence_open`, `schema_one_audit_and_proposal_state_remain_readable`, and `write_result_rejects_wrong_in_memory_schema`. Existing proposal tests change their top-level verdict assertions from `Refused` to `Denied` or `Expired` only where the proposal outcome requires it.

The process-contract test reads the on-disk JSON rather than round-tripping only through the same Rust type, and the documentation bite changes the exact worker guidance in the Codex `docs/worker-charter.md` and the orchestrator decision table in `docs/integration.md`.

## V2 friction-queue overlap · `sec:gatewayrecovery:v2-friction-queue-overlap`

The first necessary overlap is `.lane/proposals/<seq>.json`. It is sequence-stable only for proposal lifecycle and exists because the single current result slot can be overwritten by a later push or run while the original proposal remains open; general per-sequence push and run results remain V2 work.

The second necessary overlap is restart seeding from the durable watermark. It suppresses only the stale current request already accepted before a daemon restart, preventing a replay refusal from overwriting recovered status; it does not redesign request publication, add a queue, or implement general result-sequence validation.

The third necessary overlap is semantic top-level verdicts, limited to `parked`, `denied`, and `expired` for tier-three recovery. All other refusal classes keep `refused`, so the broader V2 semantic-verdict campaign remains separate.

Quieter push, general sequence-addressed result files, `.lane/` snapshot exclusion, and cooldown timestamps are not implemented here. In particular, the new canonical proposal files continue to enter a gateway snapshot under current behavior; that known transport noise is called out rather than silently fixed and remains owned by V2.

## Proposed implementation bite split · `sec:gatewayrecovery:proposed-implementation-bite-split`

Use three sequential implementation lanes because the state/result work and heartbeat work both touch `types.rs`, `serve.rs`, and `tests.rs`, while the deployed documentation must describe the final combined behavior rather than an intermediate schema.

Lane one, proposal recovery and verdicts: implement the park marker, open-state reconciliation, explicit abandon, deregistration guard, canonical per-proposal projection, result schema two, legacy state and audit readers, CLI surface, unit tests, and the package/source matrices. Its acceptance test kills and recreates a `Gateway` around a parked proposal, approves the original sequence once, and observes distinct parked, denied, and expired bytes.

Lane two, serve liveness: start from lane one's imported state; implement heartbeat publication during idle and long-running actions, supervised error and panic reporting, nonzero process behavior, restart-safe reconciliation entry, unit and process tests, and the package liveness documentation. Its acceptance test covers clean shutdown, returned error, caught panic, stale generation evidence, and a request written while the daemon is absent.

Lane three, deployment contract: after both code lanes are green and imported, update the Codex worker charter and integration runbook, rebuild and deploy the gateway through the normal reusable-tool path, re-register or rebrief any live lane, and run an orchestrator-observed outage drill covering chained proposal notification, serve death detection, immediate single-process relaunch, parked-sequence approval, and retry-later handling for a busy lane. The final trusted gate remains orchestrator-owned.

## Owner questions · `sec:gatewayrecovery:owner-questions`

1. Ratify explicit abandon and lane closeout as the only transitions to `expired`, with the soft lane budget continuing to report overrun but never destroying a parked proposal; this proposal recommends yes because another automatic lifetime repeats the measured failure mode.

2. Ratify the five-second heartbeat cadence and fifteen-second stale threshold; this proposal recommends yes as a small fixed-state write rate with far lower frequency than the existing 500-millisecond polling while detecting death within one orchestrator probe.

3. Ratify the narrow sequence-stable `.lane/proposals/<seq>.json` overlap while leaving general sequence-addressed results and `.lane/` snapshot exclusion to V2; this proposal recommends yes because later push and run traffic otherwise destroys the lane's only durable view of an open proposal.

4. Choose the schema-two cutover policy: drain all schema-one lanes before deployment, or rebrief them in place after the compatible reader lands; this proposal recommends draining when practical and explicitly rebriefing the few remaining lanes rather than supporting dual worker result writers.

5. Ratify `deregister` refusing open proposals rather than silently bulk-expiring them; this proposal recommends refusal because each abandonment then carries a reviewed, non-blank reason in the terminal marker and audit.
