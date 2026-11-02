# Dispatch and supervision · `spec:dispatch:dispatch-and-supervision`

This part fixes the durable policy by which the orchestration system selects, authorizes, supervises, and closes worker assignments. It realizes the dispatch part accepted by the corpus owner (`dec:decisions:spec-concept-accepted`). Current roster membership, model and reasoning values, cadence intervals, and budget amounts remain owned registry data under (`rule:architecture:dynamic-facts-stay-in-registries`). This part instead fixes the constraints those values must satisfy and the evidence a dispatch must retain. Every label minted here has area `dispatch`.

## Scope · `sec:dispatch:scope`

Dispatch policy governs the decisions before, around, and after a bounded assignment. It does not govern how a worker performs its application work, how a provider reasons internally, or how a hook implements a callback or wakeup. Those boundaries may implement the policy but may not choose it.

**Definition (Dispatch)** · `def:dispatch:dispatch`

A dispatch is one bounded assignment of work to one selected worker context. It begins when the orchestrator (`def:architecture:orchestrator`) binds a unique dispatch identity, a complete brief, a selected harness, resolved capability values, and evidence endpoints to a worker (`def:architecture:worker`). It ends only when that assignment has a recorded terminal outcome. A conversation, provider request, model value, worktree, or resume message alone is not a dispatch.

One dispatch has one scope and one report contract. A resume remains in that dispatch only while the harness (`def:architecture:harness`) preserves the worker identity, instruction chain, working state, and evidence trail. Loss of any required continuity creates a replacement dispatch with a new identity; it may reuse reviewed work but may not inherit authorization implicitly. The worker's authority remains the charter-and-brief intersection fixed by (`rule:architecture:charter-plus-brief`).

## Worker selection · `sec:dispatch:selection`

Selection begins with the bounded task, not with an available model. The orchestrator classifies the task, resolves an approved role through a fresh roster, and records the concrete values chosen for this dispatch.

**Definition (Worker tier)** · `def:dispatch:worker-tier`

A worker tier is a roster position defined by an operating mode, capability envelope, task classes, gate posture, and failover relationship. It is not a model name. A tier may resolve to different provider, harness, model, or reasoning values as its owned roster changes, but every resolved dispatch must remain within the tier's durable capability and audit constraints.

The corpus owner, through orchestration policy, owns the tier meanings (`rule:architecture:orchestration-policy-owner`). The roster owner maintains their current realizations and must satisfy the ownership, freshness, validation, and missing-data requirements of (`rule:architecture:stable-constraints-govern-registries`). An absent, stale, or ambiguous roster entry makes that tier unavailable; it never licenses an inherited default.

**Terminology (Normal mode)** · `term:dispatch:normal-mode`

Normal mode is operation using the owner-approved primary capability roster while the selected provider path is not in recorded impairment. Producing work in normal mode uses the `normal-tier heavy` role. Normal describes the approved selection path, not the eventual quality or success of a worker, and it cannot be inferred from a model identifier alone.

Normal-mode health is scoped to the affected provider path. One provider can remain in normal operation while another is in degraded mode, provided the selection and impairment records identify that distinction.

**Terminology (Degraded mode)** · `term:dispatch:degraded-mode`

Degraded mode is deliberate, recorded operation after failure or overload of a normal-tier provider path. It begins only through the degraded-entry protocol (`proto:dispatch:degraded-mode-entry`). The impaired vendor's degraded roster names no producing tier; observation stays with the Sonnet watcher role. Producing work moves to an explicitly permitted healthy path, is split to fit one, or pauses. Continuing on a healthy path does not rename it as the impaired path's replacement and does not itself prove recovery.

Degradation is a state with an owner, scope, cause, start time, and most recent normal-tier attempt. Merely observing a difficult task, attaching a Sonnet watcher, or exceeding a task budget does not enter degraded mode.

**Terminology (Sonnet watcher task)** · `term:dispatch:follower-task`

A Sonnet watcher performs auxiliary observation for a lane across its dispatches. It consumes declared evidence and relays reports, but does not own the producer's deliverable, mutate its work, accept verification, authorize a resume, or issue a gate verdict. Sonnet is the watcher role; its concrete model version remains a roster value, and no fallback watcher model is permitted. Its instructions name the lane, its duties, their evidence sources and absolute UTC deadlines, so a replacement can reconstruct the observation state.

A Sonnet watcher's output is supervision evidence only. Losing that output can reduce visibility, but cannot change the producing worker's authority or turn the Sonnet watcher into a producer.

**Signature (Dispatch declaration)** · `sig:dispatch:dispatch-declaration`

Before launch, the orchestrator must create a declaration containing every field below. Together these fields specialize one worker's authority and make the result reviewable across either harness, as required by (`req:architecture:harness-equivalent-outcomes`).

|Field|Required content|
|-----|----------------|
|Identity|Unique dispatch identity, producing or Sonnet watcher role, selected harness, and fresh or resumed lifecycle status.|
|Task|One objective, task class, expected deliverable or Sonnet watcher outcome, and completion condition.|
|Scope|Exact allowed files or systems, allowed mutations and commands, excluded surfaces, authoritative starting state, and working root.|
|Selection|Operating mode, worker tier, exact resolved model value, exact reasoning depth, roster edition or observation time, and the evidence used to judge availability.|
|Read-back|Required restatement fields and either `gated` or `audit-first`; for `gated`, the channel by which explicit proceed authorization will arrive.|
|Constraints|Applicable hard rules, permissions, forbidden actions, ambiguity resolutions, checkpoint policy, and terminal conditions.|
|Supervision|Completion callback, transcript or event source, heartbeat policy, progress basis, budget, tolerance, and stall or runaway response.|
|Verification|Checkable verification bar, execution authority, required commands or recomputations, and treatment of failures or unavailable tooling.|
|Report|Exact report shape, required evidence, per-step wall times, deviations, open questions, verification rounds, and terminal status.|

The declaration must carry the concrete operating values selected for the run without turning them into specification constants. If any required field is unknown, the dispatch is not launchable. Harness-specific terminal report bytes remain governed by their owning output contract, including (`[TOOLS-proto:output:run-report-line]`); the brief fixes the report content it needs, not a competing transport grammar.

**Table (Role roster)** · `tab:dispatch:role-roster`

The following mapping fixes role selection while leaving current model values to the two owned rosters. Producing, design and review work defaults to a Codex lane on the normal roster's current general model; a thread already in flight on another backend may continue there, but its continuity does not change the default for new work. A task moved between rows must be reclassified and redeclared before launch.

|Task class|Normal operation|Operation after normal-path impairment|Binding condition|
|----------|----------------|--------------------------------------|-----------------|
|Cross-file judgment, adoption, verification, or deep design|`normal-tier heavy`|A healthy other-provider `normal-tier heavy`, or split or defer|Splitting must produce bites the receiving normal tier carries whole; no producing role below `normal-tier heavy` exists to receive the remainder.|
|Bounded design or implementation bite|`normal-tier heavy`|A healthy other-provider `normal-tier heavy`, or defer|The bite is exact, the receiving provider path is healthy and authorized, and the dispatch is gated.|
|Mechanical exact-shape sweep|`normal-tier heavy`|A healthy other-provider `normal-tier heavy`, or defer|Inputs and output shape are closed, verification is deterministic, the receiving path is healthy, and the dispatch is gated.|
|Auxiliary tracking, backlog consumption, watching, or bounded health observation|Sonnet watcher|Sonnet watcher; missing coverage is a dispatch defect|The task owns no producing deliverable and cannot substitute for review or verification.|

Both operation columns name roles, not products. At action time the orchestrator resolves the selected role through the current roster and copies the resulting values into the dispatch declaration (`sig:dispatch:dispatch-declaration`).

**Rule (Explicit model)** · `rule:dispatch:explicit-model`

Every dispatch must state the exact selected model value in its brief and record the roster edition or observation from which that value was resolved. No command default, configuration default, previous lane, provider default, or resume context may supply it implicitly. Before accepting work, the orchestrator must compare the declared value with launch evidence from the harness.

If the harness cannot select or report the declared value, launch stops. A substitution requires an amended declaration and a new authorization event; silent fallback is a dispatch defect even when its output appears correct.

**Rule (Explicit reasoning depth)** · `rule:dispatch:explicit-reasoning`

Every dispatch must state its intended reasoning depth. Where the harness has an effort control, the brief names the exact resolved setting and launch evidence must agree. Where no such control exists, the brief states the observable reasoning obligation, such as mechanical reproduction, comparison with a named source, or independent recomputation of review claims from the tree. Neither form may be inherited from a prior dispatch or ambient configuration.

A later promotion, correction, or provider change restates the depth and its rationale. Resuming a context cannot silently weaken or strengthen it.

**Rule (Explicit read-back policy)** · `rule:dispatch:explicit-read-back`

Every dispatch must require a first-output restatement and must state whether work is `gated` after that restatement. Under `gated`, the worker stops until the orchestrator sends explicit proceed authorization. Under `audit-first`, an approved ungated normal role may continue after the restatement while the orchestrator audits it at the first Sonnet watcher hand-back. Silence is not `audit-first`, and roster or harness convention cannot choose the policy by implication.

All producing work dispatched under a recorded impairment and every role declared gated by its roster use `gated`. A Sonnet watcher still receives an explicit read-back policy even though it owns no deliverable.

**Rule (Task-weight selection)** · `rule:dispatch:task-weight-selection`

The orchestrator must weight a manufactured bite by ambiguity, breadth of state, number and coupling of files, authority sensitivity, amount of design judgment, adversarial risk, verification burden, and cost of recovery. It then selects a role whose demonstrated capability covers the highest burden, not a role chosen merely because it is idle or inexpensive.

When the available role is too small, the orchestrator must split the bite, promote it, cross to an approved healthy normal tier, or defer it. It may not hide a capability mismatch by loosening verification or leaving design choices open for the worker.

**Rule (Sonnet watcher exception)** · `rule:dispatch:follower-exception`

The recorded `follower` role, fulfilled by the Sonnet watcher, is permitted during normal operation only for Sonnet watcher tasks (`term:dispatch:follower-task`). This is the sole normal-mode exception that permits the approved small observation role outside the producing normal-tier roster. The brief must make the Sonnet watcher read-only with respect to the producer and must name its parent dispatch, input backlog, reporting channel, and replacement behavior.

If a task authors a deliverable, edits shared state, decides correctness, or owns a verification result, it is producing work and the exception does not apply. Relabelling such work as summarization is prohibited.

## Gated dispatch · `sec:dispatch:gated-dispatch`

Gating turns a complete declaration into explicit authorization. A worker's confidence, availability, or correct guess does not replace the orchestrator's audit of scope and instruction uptake.

**Requirement (Manufactured bite)** · `req:dispatch:manufactured-bite`

Before launch, every producing assignment must be manufactured into one independently reviewable bite. Its brief names the exact objective, deliverable, files or systems, starting state, allowed and forbidden actions, hard constraints, resolved design choices, verification bar, failure treatment, and final report shape. It also identifies what is deliberately out of scope. A material design question may be delegated only with bounded options and decision criteria; an unbounded question means the bite is not ready.

If the bite cannot be stated that precisely, the orchestrator must split or promote it before launch. When a disposable Git worktree can be reclaimed after a stall, the brief must explicitly grant and order an early first scoped commit before exploratory work and must name the target worktree and base. A non-Git execution context with the same loss risk must name an equivalent durable checkpoint. A worker charter's default prohibition cannot be bypassed by supervision shorthand.

**Requirement (Public constructors enter the brief and gate)** · `req:dispatch:public-constructor-scope`

When a bite extends a public structure, its brief names the constructors of that structure across the workspace, and its verification bar compiles and lints the whole workspace. A package-only gate can pass while a constructor elsewhere no longer builds, so the public shape is part of the change's scope (`req:dispatch:manufactured-bite`).

**Protocol (Read-back gate)** · `proto:dispatch:read-back-gate`

The read-back sequence is:

1. The orchestrator launches the worker with the complete declaration (`sig:dispatch:dispatch-declaration`) and records whether the dispatch is `gated` or `audit-first`.
2. Before any task action, the worker emits one first output containing only its restatement of scope, hard rules, verification bar, report contract, and ambiguities. A gated worker then stops.
3. The orchestrator compares the restatement field by field with the brief, charter boundary, and manufactured bite (`req:dispatch:manufactured-bite`).
4. If the restatement is faithful, the orchestrator records the audit. For a gated dispatch it then sends an explicit `PROCEED` through the same harness identity; only receipt of that event authorizes work. An audit-first worker needs no proceed event but its audit must occur at the first Sonnet watcher hand-back.
5. If the first restatement misses the contract, the orchestrator stops or suspends work, sends one correction, and requires a corrected restatement. No correction may broaden the original authority silently.
6. The orchestrator audits the corrected restatement and either authorizes it or applies the correction-failure scenario (`scenario:dispatch:read-back-correction`). Every restatement, correction, audit, and proceed event is retained with ordering and time evidence.

Any gated task action before the recorded proceed event is unauthorized even if the later result matches the brief.

**Scenario (Read-back correction)** · `scenario:dispatch:read-back-correction`

A read-back miss is detected when the worker omits, alters, or contradicts any scope boundary, hard rule, verification obligation, report field, or material ambiguity, or when it acts before authorization. On the first miss, the orchestrator preserves the transcript, halts further task work, states one precise correction, and requires another restatement. Premature edits are isolated and reviewed as unauthorized evidence; they do not earn proceed.

Exactly one correction is permitted. If the corrected restatement still misses the contract, the original dispatch terminates without work authority. The orchestrator then splits the bite into simpler declarations or promotes it to a role capable of holding the complete contract. Repeated clarification, silent acceptance of the miss, or continuation in the same misunderstood context is not recovery.

**Rule (Gated-tier audit)** · `rule:dispatch:gated-tier-audit`

Before integrating or accepting gated work, the orchestrator must inspect the actual complete diff or artifact against the declared starting state and must independently recompute at least one substantive worker claim from its primary source. A report summary, Sonnet watcher summary, test tail, or worker assertion cannot substitute for either check. The recomputation must identify its input, method, result, and reviewer.

The audit also reconciles allowed paths, verification scope, deviations, and terminal status with the declaration. A discrepancy returns for scoped correction or rejects the dispatch; it is never absorbed merely because an automated gate is green.

**Rule (Review the brief's design)** · `rule:dispatch:brief-design-review`

A requested design is a claim subject to the same review as a worker's implementation. If the design prescribed by the brief is itself at fault, the review states that fault and returns its correction to the brief's author; passing tests or faithful execution do not transfer the design fault to the worker.

**Rule (Briefs bound shared implementation)** · `rule:dispatch:briefs-bound-shared-implementation`

A brief that asks two things to share an implementation names the exact judgement or component to share and the behavior each must keep separate. Saying only “one implementation” can make a shared walk alter one command's calls, order or stopping behavior and cost a correction round, even when the common judgement was right (`rule:architecture:shared-judgement-keeps-walk`).

**Rule (No background-task chips)** · `rule:dispatch:no-background-task-chips`

The orchestrator and workers must not create detached, untracked task chips for follow-up work. A newly discovered item outside the current bite is recorded in the owning project backlog with its evidence, scope, dependency, and disposition, then considered later as a separately declared dispatch. Workers may not spawn sub-workers to pursue it.

An in-scope correction may remain in the current dispatch, but a distinct deliverable, owner, or authority boundary requires a new one. A stray task chip is dismissed only after the orchestrator confirms that its durable backlog record exists.

**Listing (Brief opener)** · `listing:dispatch:brief-opener`

Every brief opens with this line, so that the read-back gate (`proto:dispatch:read-back-gate`) is the first instruction the worker meets:

```text
FIRST TURN: read-back ONLY — restate scope, hard rules, verification bar, report contract, ambiguities, then STOP. Work begins only after PROCEED.
```

**Convention (Two commit tracks)** · `conv:dispatch:two-commit-tracks`

Commits run on two tracks because progress tracking and a readable history pull apart. Frequent `squash:` commits carry no gate expectation and keep a dead lane's work visible; a brief states a small budget of named commits, each a meaningful step in Conventional Commits form with a body stating why, and each passing the gate. Squash commits are folded into their named commit before the ship that ends a step, so candidates are reviewed and imported as named commits only.

## Supervision · `sec:dispatch:supervision`

The Sonnet watcher is the only watcher. One Sonnet watcher belongs to each lane: it is spawned at the lane's first dispatch and resumed by message with every later duty. A lane's steps share its run directory, so one watcher per lane and one per run directory are the same rule. A boxed duty's message names its active round directory without changing the watcher's lane identity. The lane's watcher holds every watching duty: read-backs, investigations, work, fix rounds, review rounds, closes and gates. It owns the waiting, the relay of the step's report or gate's exit line, and the absolute UTC deadline; the session owns the decision when the hand-back arrives.

**Invariant (Callbacks before watchdog)** · `inv:dispatch:callbacks-before-watchdog`

Every result the orchestrator awaits is a duty of its lane's Sonnet watcher before launch, bound to the lane identity, evidence source and absolute UTC deadline. A watching script on the session's side is a bug in any form, including a background loop over gate output, a foreground poll of step output, or a session-side poll of the letters inbox; the loop's own inbox watcher supplies its callback independently of the lane watchers. A session that waits on what a watcher does is not at its desk. A step or gate without a watcher is a dispatch defect, corrected by handing the duty to that lane's Sonnet watcher.

The heartbeat wakeup exists only to check that each live lane's Sonnet watcher is alive, within its absolute UTC deadline and holding every watching duty. Hand-backs carry the results; neither a scheduled wakeup nor a separate listener replaces the watcher.

**Definition (Letters)** · `def:dispatch:letters`

Letters are the estate's single correspondence system because one durable, named form, each letter attributable to the loop that sent it, serves peers and workers alike. A loop writes letters through its own entry (`rule:oper:owner-and-operations`). The two directions have different authority.

Loop to loop, a letter reaches the receiving loop's durable inbox through the loop entry. A peer's letter is data, never authority: the receiving loop reads it, answers it and acts on it at its own judgement. The inbox watcher (`proto:dispatch:inbox-watcher`) brings correspondence to the loop's desk.

Loop to worker, a letter steers an existing run. Whenever the loop sees reason to redirect, narrow, widen or correct a worker's task, it writes a letter; supervision is not limited to the dispatch brief and final review. The letter may be written at any moment of the run, before or after any round, not only at a step boundary planned in advance; delivery is at the worker's next round, which the loop launches. Steering by letter keeps the loop at its desk while the worker retains its context. The worker treats the letter as its next step's brief, within the charter-and-brief authority boundary (`rule:architecture:charter-plus-brief`).

The loop places the letter with `superloop-lane send-letter LOOP RUN --step STEP --letter FILE` and delivers it at the worker's next round with `superloop-lane launch LOOP RUN --round STEP`. The launcher saves the text beside that round's brief as the step letter. The worker's reply returns as that step's outbox reply, `outbox/STEP.md`, under (`[TOOLS-rule:workercontracts:letters-and-retention]`).

**Protocol (Loop inbox watcher)** · `proto:dispatch:inbox-watcher`

Every loop starts or resumes one Sonnet inbox watcher at session start, including while heartbeat is off. It waits on bounded blocking single-result follow calls through the loop entry, immediately relaunching after a quiet timeout. Its exact metadata hand-back re-invokes the session and is the primary notification. The session reads and answers letters, then resumes that watcher by message; only the owner authorizes resuming paused lanes. HOLD names sender and subject-word classes; the watcher keeps held lines in order and excludes observed names on each call. An unheld hand-back appends and drains the held list; RELEASE returns its remaining lines once and clears the hold. Retained context provides once-only hand-back, never a duplicate message. A dead watcher is replaced with inbox reconstruction after its surviving tool is stopped. The prompt-and-stop hook tail is the second route and the inbox directory is the record. The runbook pins the prompt, call limit, replacement absolute UTC deadlines and friction procedure; this loop duty is independent of producing dispatches.

**Protocol (Heartbeat supervision)** · `proto:dispatch:heartbeat-supervision`

At each heartbeat wakeup, the orchestrator checks the watchers as follows:

1. Load the live-lane inventory and each lane's assigned watcher, duties and absolute UTC deadlines.
2. Check that each live lane has its Sonnet watcher and that the watcher is alive.
3. Check that the watcher is within each assigned absolute UTC deadline and holds every step and gate duty; missing coverage is a dispatch defect, corrected by assigning the duty.
4. Correct a live watcher by message against its instructions; replace only a dead watcher under (`scenario:dispatch:log-eater-loss`).
5. Record the watcher check and any instruction-linked friction; do not poll lane output, gate output or the letters inbox.
6. Leave result review and continuation decisions to the hand-back path; the wakeup is not another completion transport.
7. Re-arm according to the owned cadence while watcher checking remains required; the wakeup has no other duty.

Every live-worker policy must have a cadence and every dispatch must have an expected-duration budget plus tolerance. The values come from owned registry data, but must be positive, measured from declared boundaries, frequent enough to detect silence before the selected terminal backstop, and less frequent in idle supervision than while workers are live. A budget overrun is a recorded finding, not a kill switch: a worker whose evidence continues to grow runs to its declared terminal condition unless a separate safety or runaway backstop fires.

**Requirement (Progress measurement)** · `req:dispatch:progress-measurement`

Every liveness judgment delivered by the Sonnet watcher must record the dispatch identity, harness, evidence source and source identity, current size or monotonic offset, observation time, prior size or offset, prior time, computed change, callback state, completion state, selected cadence and threshold basis, budget state, resulting classification, and action taken. A statement such as “still working” without that comparison is not a measurement.

A missing, replaced, truncated, or regressed source is a distinct evidence failure and must not be reported as ordinary no-growth. The Sonnet watcher reports the evidence for the orchestrator to resolve whether the worker moved, the worktree vanished, or the harness lost continuity. Measurements and their comparison bases remain attached to the dispatch record through terminal review.

**Scenario (Stalled worker)** · `scenario:dispatch:stalled-worker`

A worker is presumed stalled when a valid Sonnet watcher observation shows no growth against the immediately prior recorded basis, when the declared watcher returns its stalled outcome, or when a completion callback remains silent past its declared evidence-movement rule. The presumption is recorded with the two measurements; it is not inferred from elapsed wall time alone. Source loss or regression is classified separately under the progress requirement (`req:dispatch:progress-measurement`).

Recovery begins promptly by re-verifying the declared worktree, base identity, current diff, and durable checkpoints before any resume message. If an unchanged disposable worktree was reclaimed, the orchestrator recreates it from the declaration's integration base and never substitutes an unrelated checkout. It then resumes the same worker only if identity and instruction continuity remain intact; otherwise it creates a replacement dispatch.

The resume message opens with worktree re-verification and requests small, durable increments. **Commit-before-explore** applies to every cleanup-prone Git worktree: the brief grants commit authority and the worker records an early scoped commit before further exploration so a later cleanup cannot erase all progress. A context whose higher charter forbids commits must not be put on that lifecycle unless the declaration names another durable persistence path before launch. Repeated stalls follow the predeclared terminal policy, and every recovered diff remains subject to normal review.

**Protocol (External interruption resumes one thread)** · `proto:dispatch:external-interruption-resume`

When a step ends because an external service is at capacity or the host slept, continuation uses the same thread while its identity and work evidence remain intact. The next message says that the interruption was external and that the work did not cause it, asks for what remains from the interrupted step together with what is new, and requests one report covering both; splitting the continuation would lose the shared evidence trail (`def:dispatch:dispatch`).

**Scenario (Sonnet watcher loss)** · `scenario:dispatch:log-eater-loss`

Resume a live watcher by message. Correct strange behavior, missing evidence or an instruction it cannot follow by comparing the hand-back with its instructions; these are frictions, not proof that its Agent session must be discarded. Compare strange behavior and friction with the watcher's instructions. Its hand-back names the instruction, the obstacle and the evidence. Every loop reports watcher frictions to the orchestration loop as findings, so watcher prompts and documents are corrected from measured friction, never guesses.

Replace only a dead watcher, with a fresh Sonnet watcher for the same lane, after stopping its surviving tool process; an abandoned background call must not wake the old Agent beside its replacement. Preserve the lane's duty and absolute UTC deadline assignments and the retained evidence needed to reconstruct its observation state. Reset only failed capture-consumption state when replay is needed, make any truncation explicit and recover the retained backlog before claiming continuity. A missing watcher is a dispatch defect, never permission for direct session-side watching; a healthy producer is not restarted because its watcher died.

**Protocol (Sonnet watcher callback)** · `proto:dispatch:log-eater-callback`

The Sonnet watcher serves its lane through this protocol:

1. Spawn the lane's watcher at first dispatch with the lane identity and complete instructions; resume it by message with every later step or gate duty and its absolute UTC deadline.
2. For a step, use the capture tool's bounded foreground calls; for a gate, use the runbook's pinned gate-output poll until its exit line appears. The watcher owns these waits, never the orchestrator session, and reports a missed absolute UTC deadline without inventing completion.
3. Relay the verified step report or gate exit line once by hand-back on the current turn, including resumed turns, never also by message. Completion of a duty does not retire the lane's watcher; the session decides the next action and messages the watcher with any further duty.
4. Compare strange behavior and friction with the instructions under (`scenario:dispatch:log-eater-loss`); each loop reports the instruction-linked evidence to the orchestration loop. The heartbeat checks only watcher liveness, absolute UTC deadlines and complete duty coverage under (`proto:dispatch:heartbeat-supervision`).

**Rule (Timing-led decisions)** · `rule:dispatch:timing-led-decisions`

Workers measure and report; the orchestrator decides with the numbers. It cites the last measured duration before starting expensive work, defines a budget for every recurring action, and treats an overrun or a missing timing as a finding. Verification is scoped to the content that changed, and full surfaces run at batch or merge boundaries. An instant identifies one point on the UTC timeline; elapsed durations and boot-clock readings do not. Every civil instant is reported as a calendar-valid `YYYY-MM-DDTHH:MM:SS[.fraction]Z`, as prose explicitly labelled UTC, or as a machine epoch field with its unit and origin documented. Every duration states its unit. Current civil time is read with `date -u +%Y-%m-%dT%H:%M:%SZ`; only explicit UTC instants or declared epochs are parsed. Naive, local and nonzero-offset civil timestamps are refused by name rather than assigned a zone. Every watcher deadline is an absolute UTC instant.

**Rule (Turn end)** · `rule:dispatch:turn-end`

An orchestrator turn ends only when its task is complete or it is blocked on the user. A harness message that there is nothing more to do in the turn ends nothing while work remains in flight.

## Owner interface · `sec:dispatch:owner-interface`

This division fixes how the orchestrator addresses the owner and how owner-facing material is shaped, so that an answer, a command, or a presentation can be judged from what the owner actually sees.

**Rule (The owner's desk receives visible choices)** · `rule:dispatch:owner-desk-boundary`

A question reaches the owner's desk only within the owner's three responsibilities (`rule:oper:owner-and-operations`) or for an act the documents keep as a person's own, such as a permanent deletion of data that may be the only copy (`rule:dispatch:host-removal-authority`), and when a person using the system would notice the difference: a name the person types, who acts, what the person is asked to do, or what is granted. A question also blocks: the asker's work waits for the answer, so a question is asked only for a problem that blocks everything else, and every other uncertainty is carried as a stated assumption that the work proceeds under and the report raises for correction. Reconciliation of a settled choice with the documents, the construction that carries it, and a private program's name are engineering matters the orchestrator settles with workers and reviewers and reports in one line. A person's attention is the scarcest shared resource, and asking that person to manage machinery by hand defeats the service the system provides.

**Protocol (Questions to the owner)** · `proto:dispatch:owner-questions`

A question that needs the owner's answer, and only that, has four parts in this order:

1. **In one breath**: the ask in one sentence.
2. **Analogy**: the same choice in familiar terms.
3. **Desk view**: what each answer changes, concretely.
4. **If it sits**: what happens unanswered, and the default taken.

The form lets the question be answered at a glance or safely left.

**Requirement (Reported commands and owner deletion)** · `req:dispatch:owner-commands`

A command run by the superloop for an operation granted by a loop row is fully qualified and self-verifying: absolute paths, nothing taken from the current directory, variables, or aliases, steps chained on success, and a final check that prints one verification token. Its output is retained in the operation report; a command that cannot be judged from that report is refused. A command prepared for a person's irreversible deletion outside reproducible places has the same form, but its check and apply belong to the person because the data may be the only copy (`rule:dispatch:host-removal-authority`).

A script prepared for a person's permanent deletion outside reproducible places has separate check and apply modes; the person runs the check first, and each precondition is tested in isolation before apply can destroy data. A pipeline under `pipefail` whose producer ends early may fail because the consumer closed the pipe, so that pipeline cannot serve as proof that the precondition failed. Destruction there remains the person's act because the bytes may be the only copy (`rule:dispatch:host-removal-authority`).

**Rule (Removal authority follows the place)** · `rule:dispatch:host-removal-authority`

The superloop may remove for good only in the cache directory of the account it runs as and on transient compute servers where a loop acts as an unprivileged account. There it confirms each named path resolves inside that place, uses no greater privilege than that account has, and reports the removal as a repeatable loop-row operation: those places hold only what can be made again. Everywhere else it moves what it removes to a recoverable place, the desktop trash on a host, and reports the recovery route; because the data may be the only copy, it prepares any permanent deletion as a script for a person, with a check mode run before an apply mode and each precondition tested in isolation (`req:dispatch:owner-commands`).

**Rule (User presentations)** · `rule:dispatch:user-presentations`

A presentation for the user is a standalone HTML file under `~/Downloads`; the orchestrator never publishes one as a harness artifact.

**Requirement (Local files remain readable presentations)** · `req:dispatch:local-file-reading-aid`

A reader who keeps exported pages as files and opens them from disk receives an ordinary reading path. Because a browser gives each local file its own origin, a page whose script reads across frames either provides a path that works for local files or says in words what the script would have shown. The reading aid makes no decision and reveals no value beyond the already exported page, which permits the weaker evidence of that fallback.

**Rule (Transcript extraction)** · `rule:dispatch:transcript-extraction`

Pasted chat is never transcribed by hand: its exact bytes are extracted from the registered session transcript with a small script, because a retyped copy can differ in bytes the reader cannot see.

## Degraded operation · `sec:dispatch:degraded-operation`

Degradation is an explicit recovery state, not an opportunistic model switch. It preserves the failed path's evidence, constrains fallback selection, and keeps probing for a demonstrated return to normal capability.

**Protocol (Degraded-mode entry)** · `proto:dispatch:degraded-mode-entry`

The orchestrator enters degraded mode in this order:

1. Detect a launch, API, capacity, overload, or provider-health failure on a declared normal-tier path and distinguish it from a task-specific worker failure or an invalid brief.
2. Preserve the error class, affected dispatch, provider and harness scope, observation time, last known success, and evidence supporting the impairment judgment.
3. Write the owned degraded-state record before fallback launch, including `degraded since`, `last normal attempt`, reason, affected scope, and the roster edition used for recovery.
4. Choose the disposition. When the impairment is isolated, dispatch the producing work to a healthy other-provider normal tier; otherwise split it into bites that tier carries, defer it, or pause it until the probe protocol clears the impairment. No smaller producing role substitutes for the impaired tier.
5. Create a new explicit dispatch for the chosen path, re-resolving model, reasoning, read-back, scope, callback, budget, verification, and report fields. Never reuse a failed context as an undeclared fallback.
6. Assign the wait until the next normal-tier attempt and its absolute UTC deadline to the relevant lane's Sonnet watcher under the owned probe cadence; on its hand-back the session launches the recovery probe. The watcher never launches a probe. Record whether work continued, moved, or paused.

Entry is incomplete until both the degradation stamp and a deliberate disposition exist. A fallback launched first and documented afterward is an unrecorded substitution.

**Rule (Within-vendor degradation)** · `rule:dispatch:within-vendor-degradation`

An impaired vendor's degraded roster names no producing tier; observation stays with the Sonnet watcher role (`term:dispatch:follower-task`). The predicate is roster position rather than model size: a producing role outside the approved normal roster costs more than it saves, because the review bar was never sized for it. Its work is reviewed by a normal-tier dispatch either way, so the reviewer outweighs the producer, and its characteristic failure is plausible work that misses a cross-file fact, which no automated gate tail detects. A normal-roster role carried for mechanical work is inside that bar and is not what this rule excludes.

The orchestrator therefore answers impairment by crossing producing work to a permitted healthy normal tier (`rule:dispatch:cross-vendor-normal`), splitting the work into bites that tier carries, or pausing it until recovery. The watcher role remains Sonnet, with its concrete model version resolved from the roster; impairment does not authorize another watcher model or direct session-side watching.

**Rule (Cross-vendor normal tier)** · `rule:dispatch:cross-vendor-normal`

Crossing is the ordinary answer to isolated impairment. The orchestrator dispatches the producing work to another provider's approved normal tier when evidence isolates the impairment to one provider path and the other path is healthy, authorized, and capable of equivalent review evidence. The new dispatch uses that provider's matching harness and charter and repeats every explicit declaration and gate; no instruction context crosses provider boundaries implicitly.

Using the healthy provider does not clear or conceal the impaired provider's degraded state. Cross-vendor normal operation is forbidden when the failure is systemic, the task depends on a missing provider-specific capability, or the other path cannot satisfy the verification and report contract. Work that cannot cross waits for the impaired path's recovery; it is never re-aimed at a smaller producing role.

**Protocol (Normal-tier probe)** · `proto:dispatch:normal-tier-probe`

Recovery probing proceeds as follows:

1. The Sonnet watcher holds the wait until the next attempt and its absolute UTC deadline at the registry-owned cadence; on its hand-back the session selects each degraded provider path whose next attempt is due. The cadence must be bounded by the recovery objective while avoiding probe load that worsens the impairment.
2. The session, never the watcher, launches a bounded, low-risk probe against the exact normal-tier harness path with explicit selection and completion evidence. A production dispatch is not silently repurposed as a probe.
3. Record start and finish times, provider response, event movement, callback, report, expected outcome, and the roster observation used.
4. Clear degraded state only when the probe demonstrates successful launch, execution, evidence flow, and completion on that normal path. Record the recovery time before routing later work back to the primary roster.
5. On failure or indeterminate evidence, retain degraded state, update the `last normal attempt` field and its evidence, and schedule the next attempt without disturbing healthy fallback work.

A response that merely accepts a request, a fallback success, or an unverified production result does not demonstrate normal-tier recovery.

**Scenario (Terminal worker failure)** · `scenario:dispatch:terminal-worker-failure`

Terminal failure is detected only when a condition declared before the attempt is met: an authority or safety boundary forbids continuation; instruction or work-state continuity cannot be restored; every permitted role and provider disposition is unavailable or unsuitable; an owned retry or runaway backstop is exhausted; the task is cancelled by its authority; or the required evidence can no longer be produced. Ordinary provider impairment enters degraded mode, and budget overrun with continuing evidence growth remains a timing finding rather than terminal failure.

On terminal detection, the orchestrator stops new launches and resumes for that dispatch, records the exact condition and time, and preserves the brief, roster observation, errors, transcripts or events, callbacks, heartbeat measurements, worktree identity, complete diff, checkpoints, degraded-state transitions, probes, and reports. It marks the deliverable incomplete unless the completion gate independently passes. Remaining work is returned to the backlog or escalated under its owner; any later attempt is a new dispatch, not an erased retry history.

**Verification (Dispatch record)** · `verif:dispatch:dispatch-record`

Verification reconstructs a dispatch from its evidence rather than trusting its summary:

1. Recompute the task class and role from the manufactured bite and the roster observation, then confirm that model, reasoning depth, read-back policy, budget, cadence, and terminal controls were explicit before launch.
2. Compare the declaration with harness launch evidence and prove that the selected identity, model, effort, working root, charter boundary, and callback agree.
3. Order every restatement, audit, correction, and proceed event; prove that there was no more than one correction and no gated task action before proceed.
4. Compare the starting state, complete diff or Sonnet watcher output, checkpoints, verification evidence, and report with the declared scope and constraints.
5. Recompute callback handling, progress deltas, wall times, budget findings, stall responses, degraded transitions, fallback selections, and probe outcomes from their underlying records.
6. Reconcile the final callback, process status, terminal report, retained evidence, and claimed dispatch outcome. For gated work, also verify the full-diff review and independent claim recomputation (`rule:dispatch:gated-tier-audit`).

The record passes only when every required field exists, ordering is possible, all measured values have a source and comparison basis, and no declaration, event, diff, report, or status contradicts another. The evidence meaning is the one fixed by (`term:architecture:evidence`); worker confidence cannot fill a missing record.

**Gate (Dispatch completion)** · `gate:dispatch:dispatch-completion`

A producing dispatch is accepted only when its declaration was authorized, its read-back policy was satisfied, the complete scoped deliverable exists, the verification bar passes over that deliverable, every deviation and timing finding is adjudicated, the terminal callback and status agree, and the exact report contract is fulfilled. Gated work additionally requires the diff and claim audit (`rule:dispatch:gated-tier-audit`). Deliverable without report, report without deliverable, partial scope, unauthorized extra work, or a green status over different state blocks completion.

A Sonnet watcher may close only its declared observation assignment and report; its closure never satisfies the producing dispatch's deliverable or gate. A successful degraded dispatch does not clear degraded mode without the probe protocol (`proto:dispatch:normal-tier-probe`). This is a dispatch-level gate, not the release verdict: accepted work remains subject to reviewed-host integration and the trusted final gate (`inv:architecture:trusted-final-gate`).
