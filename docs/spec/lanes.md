# Worker-lane lifecycle · `spec:lanes:worker-lane-lifecycle`

This part realizes the worker-lane lifecycle outline (`sec:assembly:lanes-outline`). It specifies the durable execution contract from creation of a Codex lane, through gated resumes, work and verification, to observation, recovery, and terminal evidence. Every label minted here has area `lanes`.

## Scope · `sec:lanes:scope`

This part governs execution after an orchestrator has manufactured and declared a dispatch: run creation, delivery to one resumable worker thread, step sequencing, event retention, wall-time classification, external verification handoffs, capture consumer offsets, recovery, and lane completion. The dispatch remains the unit of authorization (`def:dispatch:dispatch`), and its declaration remains the source of selection, scope, supervision policy, and report obligations (`sig:dispatch:dispatch-declaration`). A lane executes those decisions; it does not select a model, widen a brief, authorize its own resume, judge trusted completion, or choose a replacement worker.

This part assigns no byte grammar to terminal reports or worker-monitor documents. The Codex wrapper report remains governed by (`[TOOLS-spec:output:codex-lane-report]`), and raw capture consumer output remains governed by (`[TOOLS-spec:output:feeder-streams]`). Server-side verification execution is outside the lane: the lane records the request and returned evidence but neither acquires server authority nor treats server success as its own verdict.

**Definition (Lane)** · `def:lanes:lane`

A lane is one durable execution of one producing Codex worker within one dispatch. Its identity binds the dispatch identity, audited brief, harness thread identity, run directory, ordered lifecycle steps, event stream, and terminal report. A fresh process and its later resume processes are one lane only while they use the same run directory and resumable thread and preserve the original instruction chain and authority.

Process lifetime is shorter than lane lifetime. A work step may finish while the lane waits for verification, and a killed step may be resumed after its state is checked. Loss of the thread identity, instruction continuity, or authoritative run evidence ends that lane identity; reviewed work may seed a replacement dispatch, but the replacement is not another step of the old lane.

**Definition (Run directory)** · `def:lanes:run-directory`

A run directory is the lane-owned durable evidence root. It contains the original brief, each resume message, the append-only event stream, captured standard error, the current step's last-message file, the current step's completion report, capture consumer offset state, and enough ordered step records to distinguish launch, work, and verification resumes. Physical names may migrate, but their deployed compatibility roles are displayed here:

```text
brief.txt
step-{step-name}.txt
events.jsonl
stderr.txt
last-message.txt
run-report.txt
.feed-offset
```

`run-report.txt` is the live step marker: it is absent while that step runs and is published last. `last-message.txt` is result data, not a sufficient resume-step marker, because bytes from the preceding step may remain until the resumed child replaces them. An observer may read the directory, and a capture tool may maintain its own offset there, but neither may alter producer evidence. The location of the run root is deployment data; isolation and evidence roles are durable.

**Signature (Event stream)** · `sig:lanes:event-stream`

The event stream is an append-only byte sequence of newline-delimited harness events written from the worker process's JSON event output. Its execution record contains at least the thread-start event from which the resumable thread identity is obtained, worker messages, tool activity, and terminal events supplied by the harness. Provider-specific event members are data, not lane policy. Standard error and wrapper reports are separate evidence and must not be inserted into this stream.

For observation, the stable measurements are the source identity, byte size, sample time, and comparison with the immediately preceding sample. Line count, last complete record, and last event type may supplement a diagnostic but do not replace byte-growth evidence. Capture consumers consume the bytes through the owned capture tool contract; diagnostic probes inspect them without advancing a capture consumer's offset.

**Definition (Lifecycle step)** · `def:lanes:lifecycle-step`

A lifecycle step is one fresh-launch, work, or verification-resume execution owned by one wrapper process. It has a unique step name, persisted input, explicit UTC start instant, starting event offset, expected-duration budget, child process, terminal child status, elapsed wall time, classification, last message, and completion report. Steps in one lane are strictly ordered and must not overlap.

A step begins only after its input is durable and the preceding report has been retained under its preceding-step identity. Its live marker is then absent. It ends only after the child has terminated, event and diagnostic writes have closed, last-message state has settled, and the owning wrapper has published the step report. External build-machine work is evidence requested between steps, not a second process secretly sharing ownership of a lane step.

**Definition (Budget)** · `def:lanes:budget`

A budget is a positive expected wall duration plus a nonnegative tolerance for one lane step or one recurring lifecycle action. Their sum is the effective reporting threshold passed to the wrapper and recorded as its `budget` value. The start and end boundaries must be declared, use one monotonic elapsed-time basis, and be applied consistently to repeated steps.

Expected durations, tolerances, and the resulting threshold amounts are dispatch and registry data, not constants in this specification (`rule:architecture:dynamic-facts-stay-in-registries`). Their durable meaning is fixed: crossing the effective threshold creates an over-budget finding; it does not by itself authorize a signal, a failure verdict, or abandonment.

## Launch and gate · `sec:lanes:launch-and-gate`

This division governs creation of an isolated run, the read-back result, and an authorized continuation in the same worker thread. The audit and authority decision remain those of the dispatch read-back gate (`proto:dispatch:read-back-gate`).

**Terminology (Fresh launch)** · `term:lanes:fresh-launch`

A fresh launch creates a previously absent run directory and a new harness thread from the complete audited brief. It has no resume thread or existing run argument. Its first worker output is the declared read-back, not task work, whenever the dispatch is gated. Reusing a directory, copying a prior thread identity, or omitting the brief is not fresh launch.

The deployed directory name combines a UTC creation stamp and a declared lane name beneath absolute `LANE_RUNS_ROOT` when set, or beneath `runs` below the parent of the binary's directory when unset; a binary in `~/.local/bin` therefore defaults to `~/.local/runs`, and an empty or relative override is a usage error. That convention does not weaken the identity rule: the allocator must prevent a same-name, same-stamp collision and must refuse rather than merge with a directory already owned by another lane.

**Terminology (Gated resume)** · `term:lanes:gated-resume`

A gated resume continues the same harness thread in the same run directory after an explicit authorization event. The first work resume carries the recorded `PROCEED`; later resumes carry verification evidence or another instruction already permitted by the original brief. The resume message may clarify or narrow work but cannot amend the declaration, add files, relax a hard rule, or substitute silence for authorization.

Resume requires both the thread identity from the run's thread-start event and the existing run directory. A missing or mismatched member is a continuity failure, not permission to guess, use the most recent thread, or create a fresh run under the old identity.

**Protocol (Fresh launch)** · `proto:lanes:fresh-launch`

Fresh launch proceeds in this order:

1. Validate one complete prompt, a positive effective budget, working root, sandbox, lane name, and every explicit harness value copied from the dispatch declaration. Allocate a run path that is not already owned.
2. Create the isolated run directory and durably write the exact prompt to the original-brief record before starting the child.
3. Construct a fresh JSON-event execution with the declared working root and sandbox, the declared model and effort controls when applicable, and the run's last-message path. Do not supply a resume identity.
4. Start the child with the saved brief as its input. Append its event output to the event stream and its diagnostics to the separate standard-error record while the wrapper's monitor measures the live step.
5. Record the thread identity from the thread-start event and capture the first nonempty worker message. For a gated dispatch, require the process to stop after that read-back rather than proceeding into task actions.
6. Wait for the child, settle its files, classify its status and wall time, and publish the step-owned wrapper report last. Return the same process status required by the report contract.

Argument or allocation failure stops before child creation and cannot create a lane claimed as launched. The wrapper's terminal line and stored copy use the existing output contract (`[TOOLS-spec:output:codex-lane-report]`).

**Protocol (Read-back resume)** · `proto:lanes:read-back-resume`

Read-back resume proceeds in this order:

1. Retain the exact first output, its event boundary, the launch-step report, and the orchestrator's field-by-field audit. Resolve the same thread identity and run directory from that evidence.
2. Require an explicit, recorded `PROCEED` authorized under (`proto:dispatch:read-back-gate`). If the audit failed, is absent, or names another dispatch, do not resume.
3. Give the resume a unique step name, preserve the preceding step's report, and durably write the exact proceed message to that step's input record. Remove the shared live-step report only after its preceding bytes have been retained.
4. Start a resume execution with the same working root, sandbox, declared harness values, thread identity, and run directory. Append new events and diagnostics; do not replace the original brief or prior event bytes.
5. Monitor the step from its own starting event offset, collect its result, and publish its report according to the ordinary step completion order.

The next lifecycle step belongs to the same lane and run directory. Once its driver has established the new step, message the lane's existing Sonnet watcher with the step identity, evidence location and absolute UTC deadline; a boxed round's active directory is a capture target, not a new watcher identity.

**Requirement (Read-back evidence)** · `req:lanes:read-back-evidence`

The run evidence must preserve the original brief, complete first restatement, thread identity, launch event range, launch report, audit result, authorization identity, exact proceed message, and their ordering and times. When the harness's last-message file is empty because a trailing empty message replaced it, the recorder must retain the last nonempty worker message from the event stream rather than treating the read-back as absent or inventing text.

Because resume reuses the live report pathname, the preceding report must be archived under its step identity before removal. A copy held only in transient chat or process output is insufficient for run-directory replay. Read-back evidence shows uptake and authorization; it does not prove that later work is correct.

**Rule (Run isolation)** · `rule:lanes:run-isolation`

Each lane must have one run directory that no other producing lane or concurrent step uses. The fresh allocator must establish absence or exclusive ownership before writing, every resume must resolve that same directory, and at most one producer wrapper may be live there. Step names must be unique within the lane so saving a later input cannot overwrite an earlier one.

Sonnet watchers and diagnostic probes are read-only. A capture tool may write only its declared offset state. Orchestrator retention may add immutable step-index evidence but may not edit the brief, event stream, message, diagnostic, or report bytes attributed to a producer. A collision, concurrent producer, or cross-lane artifact is an evidence-integrity failure and blocks resume until isolated.

**Rule (Append-only events)** · `rule:lanes:append-only-events`

Every resume appends its JSON event bytes to the existing event stream. No step, watcher, capture consumer, cleanup action, or recovery may truncate, reorder, replace, normalize, or rewrite a byte already made available to an observer. The starting byte size for each step is retained so old backlog cannot be counted as new step progress.

A smaller, replaced, missing, or identity-changed event source is evidence loss, not a zero-growth sample. The supervisor must preserve the observation, stop offset advancement, and resolve continuity before applying a stall or completion rule.

## Work and verification · `sec:lanes:work-and-verification`

This division sequences authorized task work, the worker-to-verifier handoff, returned evidence, correction resumes, and step completion markers. It does not grant a lane authority to run an unavailable toolchain or to judge its own output.

**Protocol (Work step)** · `proto:lanes:work-step`

A work step proceeds in this order:

1. Reverify the lane identity, run directory, thread identity, working root, current worktree state, and the authorization for this message. The first work step additionally requires read-back evidence (`req:lanes:read-back-evidence`).
2. Preserve the preceding step's marker and report, write a uniquely named step input, remove the shared live marker, and sample the event stream's starting size.
3. Resume the same thread with only instructions permitted by the original brief. A correction may resolve how to meet the brief but may not silently change scope, verification, or report shape.
4. Append events and diagnostics while the step owner monitors budget, progress, stall, and runaway conditions. The Sonnet watcher may observe but cannot direct or mutate the work.
5. Wait for natural completion or a protocol-authorized kill, settle all evidence, write the step report last, and deliver the worker result and wrapper report to the orchestrator.

A failed work step retains its partial edits and evidence for review. It is not automatically retried, accepted, or converted into a new brief.

**Protocol (Ready for verify)** · `proto:lanes:ready-for-verify`

The verification handoff proceeds in this order:

1. Complete the scoped edits and every verification action the worker is authorized and equipped to perform. Record any unavailable, failed, or skipped action as a finding.

2. Settle the worktree and give concise handoff notes without claiming a trusted or final verdict.

3. End the work turn with this exact final nonempty line:

   ```text
   READY FOR VERIFY
   ```

4. Let the work step terminate normally so its event range, last message, elapsed time, and wrapper report are retained before external verification begins.

5. Treat the handoff as a request for the authority named in the brief to run the declared checks. Do not continue editing until verification evidence is returned through an authorized resume.

The handoff is neither the final lane report nor evidence that the checks ran. A misspelled, embedded, or nonterminal phrase does not request a round.

**Protocol (Verify feedback)** · `proto:lanes:verify-feedback`

Verification feedback proceeds in this order:

1. Bind the request to the reviewed worktree state and run exactly the commands or independent recomputations named by the brief. When execution is delegated to the server loop, preserve its source identity and advisory result under (`proto:conformance:server-verification-loop`).
2. Retain the complete verifier status and report, including the stable lane-verifier report governed by (`[TOOLS-spec:output:lane-verify-report]`), and select a sufficient evidence tail for correction without changing its meaning.
3. Resume the same lane thread with the round number, overall status, exact failing findings or green result, and the evidence tail. Preserve the request and response as one round record.
4. On a non-green result, correct only within the original scope, record what the round found, and perform the ready-for-verify protocol again. An infrastructure failure is non-green evidence, not permission to declare the source correct.
5. On a green result, reconcile it with the exact current worktree. If no edit followed the verified snapshot, resume the lane to write its final report; otherwise request another round over the changed state.

No returned log tail broadens worker authority. A requested change outside scope goes back to dispatch for a new or amended authorization.

**Rule (Verify-round accounting)** · `rule:lanes:verify-round-accounting`

Every accepted `READY FOR VERIFY` request increments the lane's round count, including a request that exposes verifier infrastructure failure. For each round, retain its ordinal, request time, exact source identity, requested checks, execution authority, command statuses, terminal reports, evidence tail, elapsed time, result, findings, and any correction that followed.

The final report states the total and says what every non-green round found. Retries are new requests and therefore new rounds; coalescing attempts, discarding a failed round, or counting only the final green result is nonconforming. A result over a different source state cannot close the round for this lane.

**Rule (Step-owned marker)** · `rule:lanes:step-owned-marker`

Only the wrapper process that owns the current lifecycle step may remove the preceding shared marker at step start and publish the current step's `run-report.txt` at step end. The worker child supplies events and its last message but does not declare wrapper completion. A Sonnet watcher, capture tool, capture consumer, or recovery routine must never manufacture, truncate, delete, or repair the marker.

Marker existence denotes completion of the current step, not completion of the whole lane. On resume, prior reports remain immutable under their step identities while the shared marker is re-armed by absence. An old last-message file or an old report copied outside that live pathname cannot serve as the new marker.

**Invariant (Marker after evidence)** · `inv:lanes:marker-after-evidence`

The step owner publishes its completion marker only after the child has been waited, all event and diagnostic descriptors have closed, the final-message write has settled, elapsed wall time and child status are known, and the full terminal report has been formed. Publication must make the complete report visible as one settled file state; existence of an empty or partial report is not completion.

After publication, producer-authored bytes for that step do not change. A capture tool or diagnostic probe that observes the marker can therefore read the report and optional last message without racing later producer writes. Any report published early, in place while still being written, or before event closure fails this invariant even if a later read obtains complete bytes.

## Observation and recovery · `sec:lanes:observation-and-recovery`

This division owns execution-level measurements and recovery mechanics. The dispatch supervisor decides which declared response to authorize; the lane supplies classifications and preserves the evidence on which that decision rests.

**Terminology (Wall-time classification)** · `term:lanes:wall-time-classification`

Wall-time classification combines child status, effective reporting budget, event growth, and monitor action. A naturally successful step at or below its threshold is `ok`; one naturally successful above it is `OVER-BUDGET`; a nonzero natural child exit is `FAILED`, except that a nonzero natural exit whose own transcript region carries a rejected `rate_limit_event` is `RATE-LIMITED`, because the provider refused the dispatch and the step attempted no work; a monitor kill for proven no-growth is `STALLED-KILLED`; and a monitor kill at the absolute duration backstop is `RUNAWAY-KILLED`. A nonzero natural exit after budget remains `FAILED`, while the independent over-budget finding remains visible from wall and budget.

A monitor kill classifies the child it stopped, and the kill verdicts speak only for a child that was still working. Where the step's own event region already ends in the backend's terminal result event, that child published its finish and then fell idle, so its step is classified by that result on the same terms as a natural exit — the successful classifications above, judged against the measured awake wall, or `FAILED` when the result reports an error — and its evidence records that a finished child was reaped rather than that work stalled. The stop is unchanged, because a process that is still there is still stopped by the owner that started it. Silence past a bound proves that no bytes arrived; it never proves that no result did, and a step reported as killed sends its reader to a recovery that nothing needs.

The elapsed time every one of those comparisons reads, and the `wall` the report carries, is time the host was awake: the monotonic basis of (`def:lanes:budget`), which stops while the host is suspended. Host suspension is therefore not a classification at all. It moves no bound, ends no step, and cannot expire the no-growth window, because a frozen child had no interval in which to grow anything and holds its whole remaining budget when the host wakes. Seconds the host slept are reported as the separate `suspend_gap` measurement of (`[TOOLS-spec:output:codex-lane-report]`), beside the verdict the step earned.

The current declared protocol constants are:

```text
LANE_STALL_WINDOW = 120 seconds
LANE_RUNAWAY_MULT = 4
absolute runaway bound = 4 × effective reporting budget
LANE_SUSPEND_GAP_THRESHOLD = 2 seconds
```

`LANE_SUSPEND_GAP_THRESHOLD` is the tolerance at or below which the two clocks' divergence is not a suspension: each is read as whole seconds a moment apart, so either reading can be short by almost a second, and a divergence of two seconds or less is that sampling jitter rather than time the host spent away. At or below the tolerance the reported gap is zero and the `wall + suspend_gap` identity above holds to within it; above the tolerance the gap is reported as measured.

Every conforming lane monitor must apply that no-growth window and runaway multiple. They are load-bearing protocol constants, not per-lane budget or registry values. An environment compatibility control may expose their names, but selecting another value changes this protocol and requires owner-ratified specification and verification rather than an ordinary registry edit. Monitor sampling may detect a crossed strict bound at its next declared probe; it may not change the bound's meaning.

**Rule (Budget overrun)** · `rule:lanes:budget-overrun`

Crossing the effective budget creates a wall-time finding immediately. If event bytes continue to grow, the wrapper must let the step run toward its natural terminal condition, subject only to a separately proven stall or the absolute runaway bound. An approved gateway run of the step's registered lane, with its verdict present, no audited result, and time remaining inside its proposal timeout, or an audited roster `request` of that registered lane with neither a `result` nor a `refusal` for its sequence and time remaining inside the command's registered wall budget, is progress under the same stall window. It must not signal the child merely because wall time exceeds the budget.

At natural success the wrapper classifies the step `OVER-BUDGET` while returning successful status as required by (`[TOOLS-spec:output:codex-lane-report]`). At natural failure or a later kill, the more specific terminal classification governs the verdict, but the report and lane findings still disclose the overrun. Increasing a budget after start or omitting the finding is prohibited.

**Rule (Runaway termination)** · `rule:lanes:runaway-termination`

At the first monitor probe where elapsed wall time is strictly greater than four times the step's effective reporting budget, the step owner must stop a still-running child unless the same probe has already established the more specific stalled condition. The monitor records the sampled time, bound, process identity, last event size and growth time, last-await instant when the step was credited, signal action, wait status, and `RUNAWAY-KILLED` classification.

Runaway termination preserves the run directory and all bytes already written. It is an absolute safety backstop even when events continue growing; it does not authorize deletion, acceptance of partial work, or a blind retry. Any resume or replacement follows the declared dispatch terminal policy after worktree and continuity review.

**Scenario (Stalled step)** · `scenario:lanes:stalled-step`

Detection requires both conditions at one monitor probe: elapsed wall time is strictly greater than the effective budget, and neither the append-only event size nor a credited approved gateway run nor a credited roster `request` of the step's registered lane has supplied progress for strictly more than the declared 120-second stall window. The starting event size and each growth sample belong to the current step, so historical bytes from an earlier resume cannot reset its clock. Wall time alone, quiet standard error, an old last message, or capture consumer silence does not prove a stall.

Detection proves silence, which is not by itself an ending. Before the classification is chosen the owner reads the step's own event region: a region already ending in the backend's terminal result event belongs to a child that published its finish and then idled — a step measured 125 seconds past its own result on a 2,400-second budget was stopped and filed as a stall, which sent its reader to a resume the step did not need — and that child is stopped exactly as this scenario stops one, while the verdict, the status, and the evidence record the finish it reached (`term:lanes:wall-time-classification`). `STALLED-KILLED` is reserved for a child whose events stopped growing while it was still meant to be working, and recovery below applies only to that case, because a step that reached its own result had nothing interrupted.

On detection of that case, the owner records the two size/time bases and the last-await instant when the step was credited, classifies the step `STALLED-KILLED`, stops and waits for the child, and publishes terminal step evidence without deleting the worktree or run directory. Recovery then reverifies the declared worktree, base, diff, durable checkpoints, run identity, and resumable thread. If continuity remains intact, the orchestrator may authorize a resume that begins with re-verification and requests small durable increments. Otherwise it creates a replacement dispatch under the supervision scenario (`scenario:dispatch:stalled-worker`).

**Scenario (Missing worktree after stall)** · `scenario:lanes:missing-worktree-after-stall`

This condition is detected when post-stall re-verification finds that the declared disposable worktree path is absent or has been auto-cleaned, rather than merely unchanged. The recovery record compares the missing path, exact integration-base identity from the original declaration, retained run evidence, and any durable scoped checkpoint. An unrelated existing checkout or a path with an unverified base is not a substitute.

Recovery recreates the worktree at the declared location from that exact integration base, reapplies only reviewed durable lane state, and then repeats the diff and continuity checks before resume. If cleanup risk requires an early commit, that authority and checkpoint order must have been explicit in the manufactured bite (`req:dispatch:manufactured-bite`); otherwise the declaration must name another durable path. Missing uncheckpointed work is reported as loss and cannot be reconstructed by guesswork.

**Protocol (Lane diagnostic probe)** · `proto:lanes:watcher-probe`

A `lane-watch` diagnostic probe proceeds in this order:

1. Validate the run directory and load the explicitly selected observation threshold. Identify the live step and obtain its independently supervised process state without signalling, waiting for, or consuming its output.
2. Check the live completion marker first. If it exists, read the settled stored lane report and classify its lane verdict; terminal report evidence takes precedence over event freshness.
3. If no report exists, inspect event-source existence and identity, current byte size, modification time, line count, and last complete event type. Compare size and time with the preceding recorded probe when deciding growth.
4. If the event source is missing, return stalled with unknown age and no last event. If it exists and its age is below the selected threshold, return running with the current diagnostics. If its age reaches the threshold without byte growth, sample the producer tree's liveness before choosing running or stalled. The age this step reads is awake time wherever the step's own monitor publishes it in the run directory's `.monitor` record, the driver named by the lock is alive, and the reader's own boot clock is readable and not behind the record's, and the modification-time-derived age in every other case, so seconds the host spent suspended are not counted against a producer that was frozen with it. The diagnostic may compare the modification-time-derived age first and consult the record only once that age reaches the threshold, since the awake age never exceeds it.
5. Reconcile process state: a terminated producer without a settled report is failed/incomplete evidence, not running; an unavailable process observation remains unknown and cannot manufacture a failed verdict.
6. Leave every producer file and capture tool offset unchanged, and return the diagnostic process status owned by its output contract.

**Rule (Producer liveness contradicts stall)** · `rule:lanes:producer-liveness-contradicts-stall`

For an existing event source at or beyond the watcher threshold, an established TCP connection owned by the locked driver's producer tree or movement in that tree's `rchar` plus `wchar` counters across the one-second sample is independent producer-liveness evidence and requires `running`; a missing lock, dead driver PID, unreadable process evidence, no established connection, and no I/O movement cannot contradict the stalled event evidence. The threshold this rule tests is reached on awake time wherever a live step's own monitor publishes it in the `.monitor` record and the reader's own boot clock is readable and not behind the record's, so a suspended host never brings a healthy step to this rule at all, and on the modification-time-derived age in every other case, where liveness evidence remains the only admitted contradiction.

**Specification (Watcher verdicts)** · `spec:lanes:watcher-verdicts`

The semantic `lane-watch` diagnostic verdicts are exhaustive and disjoint for one successful probe:

|Verdict|Checkable meaning|
|-------|-----------------|
|`running`|The current step has no completion report, its event source has the expected identity, and either its age — awake time wherever a live step's own monitor publishes it in the `.monitor` record and the reader's own boot clock is readable and not behind the record's, and the modification-time-derived age in every other case — is below the selected threshold with no contradictory terminated-process evidence or producer liveness is independently shown by an established TCP connection or I/O movement in the producer tree (`rule:lanes:producer-liveness-contradicts-stall`); observation completed successfully.|
|`completed`|A settled current-step report exists and encodes natural lane success, including success with an over-budget finding.|
|`failed`|A settled report encodes natural failure or a protocol kill, or independently confirmed producer termination lacks the required settled report.|
|`stalled`|No completion report exists, producer termination has not been independently confirmed, event evidence is absent or has shown no growth through the selected diagnostic threshold on the age that governs it — awake time wherever a live step's own monitor publishes it in the `.monitor` record and the reader's own boot clock is readable and not behind the record's, and the modification-time-derived age in every other case — and no established TCP connection or I/O movement in the producer tree contradicts that stall (`rule:lanes:producer-liveness-contradicts-stall`).|

`completed` and `failed` describe the observed lane step, not the diagnostic's own success. Relaying a failed lane report can therefore be a successful observation. The `lane-watch` diagnostic reserves process status 42 exclusively for its `stalled` result and uses status 0 for a successful running or terminal observation, as governed by (`[TOOLS-rule:output:lane-watch-stalled-status]`). Diagnostic usage or runtime failure is not one of the four lane verdicts and must not be disguised as `failed`.

**Definition (Capture offset)** · `def:lanes:feeder-offset`

A capture tool offset is the durable nonnegative byte position in `events.jsonl` from which that capture consumer's next unread range begins. The current compatibility file is `.feed-offset`, containing one ASCII decimal integer and line feed. A missing, unreadable, malformed, or negative value recovers to zero; a value beyond a regressed source is an evidence-continuity failure rather than proof that no events remain.

The offset belongs to one capture consumer consumption history, not to the producer or to all observers. Its accepted value advances to a sampled event size only after the complete corresponding delta frame has been written and flushed. When a cap intentionally selects only the newest suffix, advancing to that size records that older unread bytes were skipped for this capture consumer; the frame's truncation evidence must not be suppressed.

The compatibility pathname supports one active `worker-monitor` consumption history per run directory. Concurrent capture consumers must not share it; independent program consumers need independently owned offset state without changing producer bytes or tool semantics. This program boundary does not permit a second Sonnet watcher: one watcher per lane and one per shared run directory are the same rule.

**Protocol (Capture delta)** · `proto:lanes:feeder-delta`

Delta emission proceeds in this order:

1. Read the capture consumer offset using the declared recovery-to-zero rule and sample the current event-source identity and byte size.
2. If size is not greater than offset, emit no delta; check completion and, if still live, wait for a later source change or the bounded wait's expiry without changing the offset, publishing the state alone when the wait expires.
3. If unread bytes fit the nonnegative configured cap, select the complete range from offset to sampled size. Otherwise select the cap-sized suffix ending at sampled size and mark that selection truncated.
4. Emit and flush exactly one delta frame under (`[TOOLS-spec:output:feeder-streams]`). A complete successful flush is `worker-monitor`'s acceptance boundary.
5. Only after that boundary, replace the capture consumer offset with the sampled size and exit successfully. On an incomplete relay, retain the prior offset so the next invocation starts from the last accepted boundary.

`worker-monitor` does not parse, redact, re-encode, or add separators to event payload. Those are byte-contract matters owned by the cited output specification.

**Protocol (Capture completion)** · `proto:lanes:feeder-completion`

Completion emission proceeds in this order:

1. Read the current offset and event size. If unread event bytes exist, emit one delta first and leave completion for a later invocation.
2. When no delta is due, test the current step's settled report marker. If it is absent, wait without output or offset mutation.
3. If the marker exists, read the complete current-step report and determine whether a last-message file exists. Do not infer completion from the last-message file alone.
4. Emit and flush exactly one finished frame containing the report and the optional last-message payload under (`[TOOLS-spec:output:feeder-streams]`), then exit successfully.
5. Complete the named step's observation duty after that record. A later lifecycle step gets a newly armed marker and a message to the same live Sonnet watcher after the driver establishes that step; it does not get a fresh Agent merely because the previous duty finished.

Completion frames describe the current lifecycle step. Whole-lane acceptance requires the separate lane-completion gate.

**Rule (Sonnet watcher replacement)** · `rule:lanes:log-eater-replacement`

The Sonnet watcher is the only watcher. One Sonnet watcher belongs to each lane: it is spawned at the lane's first dispatch and resumed by message with every later duty. A lane's steps share its run directory, so one watcher per lane and one per run directory are the same rule. A boxed duty's message names its active round directory without changing the watcher's lane identity. The lane's watcher holds every watching duty: read-backs, investigations, work, fix rounds, review rounds, closes and gates. It owns the waiting, the relay of the step's report or gate's exit line, and the absolute UTC deadline; the session owns the decision when the hand-back arrives. The step capture is supplied by `worker-monitor`; gate duties use the runbook's gate-output recipe. Neither the capture tool nor the `lane-watch` diagnostic is another agent.

Resume and correct a live watcher by message against its instructions. Replace only a dead watcher after stopping any surviving tool process, preserving the lane's duties and absolute UTC deadlines and reconstructing observation from retained evidence under (`scenario:dispatch:log-eater-loss`). The replacement must recover any truncated backlog before claiming continuity. Missing coverage is a dispatch defect corrected by assigning the duty, never by direct session-side watching. Compare strange behavior and friction with the watcher's instructions. Its hand-back names the instruction, the obstacle and the evidence. Every loop reports watcher frictions to the orchestration loop as findings, so watcher prompts and documents are corrected from measured friction, never guesses.

**Rule (Terminal condition)** · `rule:lanes:terminal-condition`

The execution-and-recovery loop ends only on one of three recorded conditions: the requested outcome has passed its declared verification and completion gate; the user has explicitly blocked the authority or input required to continue; or the dispatch's predeclared unrecoverable-failure condition has been demonstrated with retained evidence. Each condition names the deciding authority, source state, time, and disposition of partial work.

Budget overrun, one stalled or failed step, Sonnet watcher loss, missing auxiliary summary, and a non-green verification round are not terminal by themselves. Neither repeated blind retries nor indefinite persistence is allowed: recovery continues only through authorized resumes or replacement dispatches and stops at the declared terminal policy.

## Completion · `sec:lanes:completion`

This division fixes the worker's final report, replay evidence, and the lane gate. Wrapper report bytes remain an output concern; lane acceptance remains an orchestrator decision.

**Specification (Final lane report)** · `spec:lanes:final-lane-report`

Every terminal lane, whether successful, blocked, or unrecoverably failed, must produce or have assembled a final report containing these fields:

|Field|Required evidence|
|-----|-----------------|
|Scope result|Each requested deliverable and completion condition, with its resulting path or state and an explicit terminal status.|
|Deviations|Every action, artifact, failure, skip, or scope conflict that differed from the brief, or the explicit value `NONE`.|
|Verification|Every authorized local check and external round, exact statuses, source identity, round count, and what each non-green round found.|
|Findings|Unresolved defects, output-contract disagreement, evidence loss, budget overrun, stall, runaway, unavailable tool, and material open question, or `NONE` for each empty class.|
|Timings|Wall time for launch/read-back, every work and correction step, every verification request, final reporting, and each separately timed substantive action required by the brief.|
|Evidence|Run identity, thread identity, run directory, terminal step report, and references to retained diff, event, verifier, and gate evidence.|

The worker authors the report when continuity permits; otherwise the orchestrator assembles it from retained evidence and marks the missing worker report as a deviation. `READY FOR VERIFY`, a Sonnet watcher recap, and the wrapper's `RUN-REPORT` line are not substitutes. Transport of the wrapper line remains governed by (`[TOOLS-spec:output:codex-lane-report]`).

**Verification (Lifecycle replay)** · `verif:lanes:lifecycle-replay`

Starting from the one run directory and its immutable step index, verification must perform these checks:

1. Inventory one original brief, one append-only event stream, all uniquely named resume inputs, every step report, the current marker state, message records, capture tool-offset history, and terminal report; reject a missing, overwritten, or cross-lane artifact.
2. Recover one thread identity from launch and confirm every resume uses it, every step has a nonoverlapping input/event/report interval, and event sizes never regress across recorded boundaries.
3. Reconstruct the read-back, audit, and proceed ordering and reject any task event before authorization.
4. Recount every ready-for-verify request, bind it to returned verifier evidence and the exact source state, and obtain the final report's stated round count and bounce history independently.
5. Replay each accepted capture tool transition from its prior offset, sampled size, cap, and frame result; confirm no offset advanced after incomplete output and no completion preceded unread delta evidence.
6. Confirm for every step that the marker followed settled events and message, the stored report agrees with child status and elapsed time, wall-time classification used the declared budget and protocol constants, and any stall or runaway action has its required measurements.
7. Recompute the terminal condition and final-report fields from this evidence and compare them with the claimed lane outcome.

Chat-only copies, current-state-only offsets, and a shared report overwritten without a step archive cannot satisfy replay. Their absence is a verification finding rather than permission to infer the missing history.

**Gate (Lane completion)** · `gate:lanes:lane-completion`

The orchestrator may accept a lane only when all applicable conditions below are simultaneously true:

1. The exact requested outcome exists in the allowed scope, no unauthorized mutation remains, and the original completion condition is met.
2. Read-back and proceed evidence is complete, every lifecycle step has one settled report and status, and lifecycle replay passes without unexplained loss or overlap.
3. Every required verification ran over the exact accepted source state, its terminal status is green, and round accounting agrees with the final lane report.
4. Wrapper, Sonnet watcher, diagnostic, capture tool, and verifier evidence has internally consistent statuses and obeys its owning output contract, including the agent-text status agreement (`[TOOLS-req:output:agent-text-status-agreement]`).
5. Every over-budget, failed, stalled, runaway, skipped, unavailable, or divergent condition is disclosed and either recovered or resolved by the declared terminal authority.
6. The final lane report is complete, its per-step timings agree with wrapper evidence, and the dispatch completion gate also passes (`gate:dispatch:dispatch-completion`).

A worker assertion, growing event stream, successful Sonnet watcher observation, server-green result, or `ok` wrapper line cannot waive any condition. A successful over-budget step may pass once its finding is disclosed; missing terminal evidence cannot.
