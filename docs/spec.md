<!-- Assembled from docs/spec/ under docs/spec/assembly.md. Edit the parts, not this file. -->

# Architecture and authority · `spec:architecture:architecture-and-authority`

This part fixes the durable architecture of the orchestration system accepted by the corpus owner (`dec:decisions:spec-concept-accepted`). It specifies boundaries, authority, audiences, trust, and evidence flow; changing rosters, budgets, server identities, toolchain versions, and similar operating values remain in their owned registries. Every label minted here has area `architecture`.

## Purpose and boundary · `sec:architecture:purpose-and-boundary`

This division fixes where orchestration authority begins and ends. Interfaces at the boundary are governed even when the work or provider behind an interface is not.

**Definition (System subject)** · `def:architecture:system-subject`

The orchestration system is the coordinated whole that accepts corpus-owner policy, dispatches bounded work through provider harnesses, supervises the resulting worker contexts, delegates routine computation, receives evidence, reviews returned material, integrates accepted changes, and records trusted gate verdicts. It includes the top-level orchestrator, worker charters and briefs, harness launch and resume surfaces, hook and lane state, mutable operational registries, command contracts, the host/server transfer path, and the final review boundary. This definition specializes the accepted system subject (`def:spec:system-subject`).

The subject excludes the domain semantics and implementation of the application work assigned to a worker, and it excludes model-provider internals. Those excluded systems meet this specification only at observable boundaries: accepted instructions and inputs enter; events, edits, reports, statuses, and callbacks leave. A provider's internal behavior cannot amend an instruction, transfer authority, or create a trusted verdict.

## Actors and roles · `sec:architecture:actors-and-roles`

This division separates actors from the processes and machines that happen to realize them. A change of provider, executable, or server does not change a role's duties or enlarge its authority.

**Definition (Orchestrator)** · `def:architecture:orchestrator`

The orchestrator is the top-level coordinator acting under corpus-owner policy. It partitions work, selects a permitted harness and capability, constructs briefs, authorizes gated continuations, receives callbacks and reports, checks Sonnet watcher liveness, absolute UTC deadlines and duty coverage, and decides from their hand-backs, reviews diffs and evidence, integrates accepted material, and runs or commissions the final gates. It does not perform the lane's application work and does not treat a worker or compute result as its own verdict. Delegation changes who computes, not who reviews.

**Definition (Worker)** · `def:architecture:worker`

A worker is one dispatched execution context, not a model name or a permanent agent identity. Its authority exists only for the lifetime and scope of its dispatch. The matching harness charter supplies standing worker constraints, and the brief supplies the bounded task, allowed files or systems, required verification, and report contract. A resumed context remains the same worker only while the harness preserves its dispatch identity and instruction chain. The worker may produce edits and evidence; it may not orchestrate other work, expand its own scope, or issue the trusted final verdict.

**Definition (Harness)** · `def:architecture:harness`

A harness is the provider-specific boundary that creates or resumes a worker, delivers the authorized instruction chain, establishes tools and isolation, records events or a transcript, and publishes completion through its callback and report surfaces. The harness owns those transport mechanics, but it does not choose orchestration policy or reinterpret the brief. Provider behavior behind the boundary is observable only through the contract the harness exposes.

**Definition (Compute server)** · `def:architecture:compute-server`

A compute server is a replaceable, shared, and untrusted execution domain for routine builds, tests, gates, and other computation. It may hold isolated accounts, working clones, caches, toolchains, a source-transfer hub, and run wrappers. None of those holdings makes it a source of record. Server availability, capacity, identity, and installed versions are registry facts; the durable property is that loss or replacement of the domain cannot remove the trusted host's ability to restore inputs and judge results.

**Definition (Trusted host)** · `def:architecture:trusted-host`

The trusted host is the authority domain that holds reviewed source and governing records, receives returned material into isolation, performs textual review and local integration, and records final verification verdicts. Trust attaches to reviewed host state and its controlled procedures, not automatically to every byte resident on the machine. Server-originated data remains untrusted while stored on the host until the review protocol admits it.

**Terminology (Authority)** · `term:architecture:authority`

Authority is the recognized right to decide a defined class of facts and to maintain the record for that class. Access, write permission, computational ability, possession of a copy, and successful execution are capabilities, not authority. An actor can therefore produce or transport a value it has no right to ratify. Authority is always scoped by fact class, audience, and lifecycle; it is never inferred from which actor acted last.

**Terminology (Evidence)** · `term:architecture:evidence`

Evidence is reviewable output tied to a producer, input state, scope, time, and result, and capable of supporting or refuting a claim about execution. Transcripts, diffs, logs, reports, statuses, test output, and recomputed measurements can be evidence. Evidence does not issue a verdict merely by existing or by reporting success. It becomes trusted evidence only to the extent that the reviewing authority validates its provenance and relationship to the exact host state being judged.

**Signature (Actor roles)** · `sig:architecture:actor-roles`

Let the actor set contain the corpus owner, orchestrator, harness, worker, and compute server. The relation `owns(actor, fact-class)` assigns each governed decision class to one maintaining authority; `dispatches(orchestrator, worker, harness)` binds one worker to one harness and brief; and `produces(actor, evidence-class)` records provenance without implying authority. The trusted host is the domain in which the corpus owner and reviewing orchestrator exercise their authoritative roles.

One process may realize more than one role, and one role may move between processes, but neither fact changes these relations. In particular, a harness does not acquire orchestrator authority by launching a worker, and a server does not acquire reviewer authority by running a gate.

**Signature (Instruction surfaces)** · `sig:architecture:instruction-surfaces`

An instruction surface is a rule-bearing source together with its intended audience and fact class. The delivery relation is closed to the following classes:

- machine rules reach every session or derived charter surface they govern;
- the orchestration rulebook reaches only a user-initiated top-level orchestrator context;
- a harness charter chain reaches only workers launched by that matching harness;
- a dispatched brief or resume message reaches only its named worker and step;
- an operational runbook or registry is read on demand only by its authorized operator or orchestrator audience; and
- executable configuration reaches the invoked implementation and its callers through a declared contract, not as free-standing language-model instruction.

A provider-mandated repository-local worker file is part of the audited charter chain for that repository; it is not a new source of orchestration policy. Any delivery outside these pairs is instruction-surface contamination.

**Table (Actor responsibilities)** · `tab:architecture:actor-responsibilities`

The authoritative-output column is deliberately narrower than the evidence an actor can produce.

|Actor|Required duties|Prohibited duties|Authoritative output|
|-----|---------------|-----------------|--------------------|
|Corpus owner|Ratify the system boundary, normative policy, exceptions, and publication gates.|Let an implementation or successful run silently amend policy.|Owner decisions and accepted normative records.|
|Orchestrator|Dispatch, supervise, review, integrate, verify, and record the host verdict.|Perform lane application work or execute unreviewed returned source.|Scoped briefs, integration decisions, and trusted-host gate verdicts within owner policy.|
|Harness|Launch or resume the worker, deliver only its instruction chain, preserve events, and signal completion.|Select policy, broaden scope, or interpret provider success as correctness.|The protocol record of launch, events, callback, and termination; correctness remains for review.|
|Worker|Perform only the brief, preserve provenance, and return edits, evidence, timing, deviations, and a terminal report.|Orchestrate, self-authorize extra work, mutate another authority's state, or declare final acceptance.|Its scoped report of actions and observations, never the trusted verdict.|
|Compute server|Execute supplied computation in isolation and return bounded artifacts and run evidence.|Become the source of record, send instructions upstream, or bypass quarantine and host verification.|No architectural verdict; all outputs are data with server provenance.|

## Authority layers · `sec:architecture:authority-layers`

This division fixes precedence without flattening distinct fact classes into one master instruction file. A lower surface may specialize its assigned class; it may not take ownership of a higher or different class.

**Invariant (Layered authority)** · `inv:architecture:layered-authority`

The deployed separation among machine rules, orchestration policy, harness charters, briefs, runbooks, registries, and executable behavior is preserved, realizing the accepted invariant (`inv:spec:layered-authority`). Machine rules decide universal machine constraints. The specification parts decide dispatch and supervision policy under corpus-owner authority; the orchestrator-only rulebook delivers their location to an orchestrator session and originates no policy. A matching charter decides standing worker discipline, and a brief specializes one task within it. Runbooks and registries decide current operational values only in their owned class. Executables decide what the deployed implementation actually does, but an implementation that differs from its governing contract is defective rather than newly authoritative.

This is a typed precedence relation, not a total file order. When two surfaces speak to the same fact, the higher governing source wins; when they speak to different fact classes, both remain authoritative in their class. Copying a fact into a lower surface for delivery creates a synchronization obligation, not a second owner.

**Rule (Machine facts precede)** · `rule:architecture:machine-facts-precede`

A universal machine constraint precedes every charter, brief, runbook, registry, and executable configuration in every audience it governs. A lower surface may restate that constraint for delivery but may neither weaken it nor claim an exception. If the recorded machine fact and observed machine differ, the affected operation pauses at the safe boundary until the machine-fact authority reconciles the governing record; a worker may not choose between them.

**Rule (Orchestration policy owner)** · `rule:architecture:orchestration-policy-owner`

Dispatch selection, capability tiers, read-back policy, supervision cadence, callback use, degradation, and stall response belong to `docs/spec/dispatch.md` under corpus-owner authority. Integration practice belongs to `docs/spec/architecture.md` and `docs/spec/server.md`; gate ownership belongs to `docs/spec/conformance.md`. These specification parts carry the policy; the orchestrator-only rulebook delivers their location to an orchestrator session and originates none. A pointer that carried policy would create two carriers, while carrying the location instead of the text meets the injection hook's size bound. Worker charters, briefs, server runbooks, and helper code may implement or refer to those decisions but cannot originate them. Values that the policy deliberately delegates to a mutable roster remain owned registry data rather than becoming normative merely because the orchestrator reads them.

**Rule (Charter plus brief)** · `rule:architecture:charter-plus-brief`

A worker's complete authority is the intersection of its harness charter chain and its dispatched brief. The charter supplies standing boundaries and declares which of its rules a brief may specialize; the brief supplies the task, scope, permissions, verification bar, and report contract. Hard charter rules remain binding. Silence grants nothing, and a brief cannot grant orchestration authority, ownership of another actor's mutable state, or power to waive a machine rule. Resume input may narrow or continue the same dispatch but cannot silently create a new one.

**Rule (Audience separation)** · `rule:architecture:audience-separation`

Every instruction delivery mechanism must positively identify its audience before exposing content. The orchestrator rulebook is withheld from workers, subagents, and nonmatching harnesses; a worker charter is withheld from the orchestrator's policy surface and from workers of another harness; a brief is confined to its dispatch; and runbooks remain on-demand data rather than ambient prompt content. Hook filters, provider discovery rules, deployment copies, and repository-local instruction files must be audited as one delivery chain. A symlink, fallback discovery path, inherited prompt, or resume operation may not widen that chain.

## Harness boundaries · `sec:architecture:harness-boundaries`

This division preserves provider-specific mechanics while fixing the common architectural outcome: one dispatch returns reviewable evidence to one reviewing orchestrator.

**Invariant (Two harnesses, one evidence path)** · `inv:architecture:two-harnesses-one-evidence-path`

Claude worker contexts and Codex lanes retain distinct launch, instruction, resume, transcript, and completion mechanics, but both are dispatched under the same orchestration policy and return to the same reviewing orchestrator. No provider-specific success path terminates in acceptance outside that review. This preserves the accepted two-harness invariant (`inv:spec:two-harnesses-one-evidence-path`) and the achieved integration it describes (`dec:decisions:multi-superloop-integration`).

**Specification (Claude harness boundary)** · `spec:architecture:claude-harness-boundary`

The Claude harness launches a provider worker context from the top-level orchestrator and binds it to a brief and matching worker instruction chain. Machine-wide rules applicable to the context remain in force; the orchestrator-only rulebook is not delivered. The harness owns the provider worker identity, tool boundary, work context, event transcript, and completion callback. A transcript is retained as review and liveness evidence, while the harness callback is terminal transport evidence relayed by the lane's Sonnet watcher; the orchestrator session does not poll for it (`proto:dispatch:log-eater-callback`).

The callback must identify the dispatch and expose its terminal report and result location to the orchestrator. A provider-side completion, transcript message, or tool success is evidence only. Restarting or resuming a Claude context must preserve the brief and charter boundary or create a new dispatch; it cannot inherit orchestration instructions from the parent context.

**Specification (Codex harness boundary)** · `spec:architecture:codex-harness-boundary`

The Codex harness launches a headless lane at an explicit working root and isolation mode, records a persistent thread identity, and creates a lane-owned run directory for append-only events, step inputs, completion artifacts, and the terminal report. A continuation resumes that same thread through the lane driver and appends evidence to the same declared lifecycle; if identity or instruction continuity is unavailable, the continuation is a new dispatch.

The Codex instruction chain consists of the deployed worker-scoped `AGENTS.md`, any matching repository-local worker instructions that the harness necessarily discovers, and the dispatched brief or resume message. It must not discover the Claude machine rulebook or the orchestrator-only rulebook. Each step owns its completion marker and final report, while the run directory preserves earlier event evidence. The lane driver returns the terminal report and result location to the same orchestrator that dispatched the lane; the lane itself does not cross the trusted server boundary or run the final gate.

**Requirement (Harness-equivalent outcomes)** · `req:architecture:harness-equivalent-outcomes`

For equivalent briefs, both harnesses must yield evidence sufficient for the same review decision even though their event encodings and lifecycle mechanics differ. Each result must identify the dispatch, instruction scope, working state, produced changes, verification attempted, elapsed wall time, terminal status, deviations, and final report, and must preserve a transcript or event trail that explains those claims. Equivalence means equal reviewability and gate semantics, not byte-identical transcripts. A harness that cannot produce that evidence is unavailable for the dispatch rather than exempt from the gate.

## Trust and state · `sec:architecture:trust-and-state`

This division fixes where authority resides, how information crosses the compute boundary, and who maintains mutable state. Trust follows reviewed state and procedure, never machine identity or successful execution.

**Diagram (Trust domains)** · `diag:architecture:trust-domains`

The downward boundary arrow carries reviewed source and scoped inputs. The return arrow terminates in host quarantine and carries data, never authority.

```text
TRUSTED HOST / AUTHORITY DOMAIN
    Corpus owner
         |
         v
    Orchestrator / reviewer <------ evidence and reports ------+
         |                                                    |
         +---- brief ----> Claude harness context -------------+
         |
         +---- brief ----> Codex harness context --------------+
         |
         | reviewed source and scoped inputs
         v
================ HOST-TO-SERVER AUTHORITY BOUNDARY ================
         |
         v
    SHARED COMPUTE SERVER (UNTRUSTED)
         |
         | results, artifacts, and source history: DATA ONLY
         v
================ HOST QUARANTINE: NO EXECUTION =====================
    textual inspection --> local integration --> trusted verification
                                                       |
                                                       v
                                  Orchestrator / reviewer --> verdict
```

Information returns across the boundary, but authority does not. Only the trusted-host review path can promote selected returned data into reviewed source and then into a verdict.

**Rule (Mutable-state ownership)** · `rule:architecture:mutable-state-ownership`

Every mutable state file, registry, run directory, transcript, hook store, working reference, cache record, and deployed copy has exactly one maintaining authority. That authority defines the canonical location or derivation source, allowed writers, readers, schema, retention, update trigger, and recovery procedure. It may delegate writes to a process without transferring ownership. Readers and replicas do not become co-owners.

Where a deployed or generated copy exists, its source remains canonical and a declared reconciliation or deployment step proves correspondence. Two independently editable copies of one fact are forbidden. Ephemeral state must name the durable source from which it can be restored; state with no owner or recovery path is an architecture defect.

**Requirement (No-change claims name the state preserved)** · `req:architecture:no-change-claim-scope`

A command that claims to change nothing states exactly which entries remain unchanged, and its code preserves their content, names, kinds, modes, owners, groups, modification times and change times. Reading can advance an access time; the command suppresses that effect where its caller is permitted to do so and reports it for each affected entry where it cannot, so the claim describes the state it actually preserves.

**Rule (Act on the opened object)** · `rule:architecture:opened-object-identity`

A decision about a directory applies to the object opened for inspection. Once a directory is opened to classify it, every later check and operation uses that descriptor and does not reopen the path by name; reopening would allow a different object to receive the decision.

**Rule (Shared judgement keeps each command's walk)** · `rule:architecture:shared-judgement-keeps-walk`

Where a reporting command and an acting command must agree, they share a pure judgement from observed facts to the action that would follow. Each command keeps its own walk through what it observes or acts on, including its calls, order and stopping points, call for call when the judgement is extracted; sharing that walk would change a command's observable contract even when its decision is the same.

**Requirement (Executable settings have trusted writers)** · `req:architecture:executable-settings-trust`

A file that names programs to execute is trusted only after its opened descriptor proves its owner and mode and the containing directory's owner and mode are read from the opened directory descriptor through which the file was opened, before parsing. The authority of a command path cannot exceed the authority of whoever can alter the file or replace it through its directory (`rule:architecture:opened-object-identity`).

**Rule (Value shape and origin are separate)** · `rule:architecture:value-shape-and-origin`

A value's form says nothing about who supplied it. A program validates both form and origin when a value arrives through a channel others can write, such as a browsing context's name, an environment variable or a file beside a target. If origin cannot be established, the program does nothing with the value or acts only within a declared boundary where a wrong value is harmless, and states which boundary applies.

**Rule (Inspection does not run subject-named programs)** · `rule:architecture:inspection-does-not-run-subject-programs`

A program inspecting what another identity controls runs no program that the inspected thing can name. A repository can name filters, hooks, file-system monitors, pagers, credential and transport helpers, and programs in included configuration; disabling a list of settings misses the next naming route, so the inspector reads needed facts from the files that state them or does without.

**Requirement (Child output and lifetime are bounded)** · `req:architecture:bounded-child-result`

Every program that runs a child bounds both output streams as they are read and enforces a time limit. Crossing either stream cap or the time limit ends and reaps the child before a result is published; checking collected output only after a child exits cannot bound memory or lifetime. The requirement applies in the host and compute domains alike.

**Rule (Inspecting commands fix helpers and child environments)** · `rule:architecture:fixed-loop-report-helpers`

A report about a loop is produced where that loop's programs are reachable. Its launcher, every program in the scaffold that brings the reporting command into place, and every helper through the last one are named by fixed system paths that the loop cannot replace; the environment handed down carries no executable search path the loop can write. Letting the inspected loop replace any program along that chain lets the subject change the reporter and invalidates the evidence (`term:architecture:evidence`). A fixed path establishes which program starts, but not what it loads: a command inspecting untrusted material clears each child's environment and adds only variables that child needs, each named with its reason and none taken from what is inspected.

**Requirement (System-program links have trusted writers)** · `req:architecture:system-program-chain-trust`

A checker that claims a candidate is a system-owned program resolves its link chain to the final target within a bound, inspecting each link without following it. The target, every link on the way and every directory holding one are owned by the system administrator and writable by no other account. This establishes only that another account cannot change those objects inside the checker's own user namespace; a familiar path or regular-file check alone establishes less.

**Rule (Host-to-server direction)** · `rule:architecture:host-to-server-direction`

Authoritative source, configuration, credentials selected for use, and scoped job inputs originate in the trusted-host domain and may flow into the compute domain through an authenticated, reviewable transfer. No server-side working copy, branch, cache, tool installation, or generated file can become the authoritative source by being newer or by completing a successful run. A server may return source history, but that return is data governed by the review protocol, not a reverse authority flow.

**Rule (Server results are data)** · `rule:architecture:server-results-are-data`

Every byte returning from a compute server is untrusted data: logs, reports, statuses, binaries, archives, generated source, commits, patches, build scripts, macros, and metadata alike. Human-readable text is not an instruction to the orchestrator, and a green report is not permission to integrate. No returned executable material may be run, sourced, imported as configuration, or built before textual review establishes what would execute and the trusted path admits it.

**Protocol (Returned evidence review)** · `proto:architecture:returned-evidence-review`

Returned evidence is handled in this order:

1. receive artifacts and source history into a host-side quarantine that cannot alter authoritative working state;
2. bind the return to its dispatched inputs and inspect provenance, changed paths, and the complete textual diff without executing returned material;
3. reject the return or explicitly select reviewed changes and integrate them into a clean local host state;
4. run the required trusted verification against exactly that integrated state, recomputing security- or release-critical claims where needed; and
5. record the review decision, verification evidence, and final host verdict.

Any failed or indeterminate step stops promotion. Evidence may be retained to explain the failure, but later steps may not infer success from an earlier server status.

**Requirement (Quarantined import)** · `req:architecture:quarantined-import`

Returned source history must first land in isolated host references or an equivalent non-executing namespace. Import must not update the current branch, index, working tree, trusted tag, deployment source, or executable search path. The quarantined identity and its provenance remain stable during review, and integration is a separate explicit operation naming the reviewed commits or changes. A transport that can update authoritative state as a side effect does not satisfy this requirement.

**Invariant (Trusted final gate)** · `inv:architecture:trusted-final-gate`

The verdict of record is always issued over reviewed host state by the reviewing orchestrator under corpus-owner policy. Server-green evidence, worker confidence, a provider completion state, and an earlier verification snapshot remain advisory until the final gate establishes that they correspond to the exact state being accepted. If server and host results disagree, the host verdict controls and the disagreement is retained as a finding. Moving computation between domains never moves this gate.

**Rule (Dynamic facts stay in registries)** · `rule:architecture:dynamic-facts-stay-in-registries`

Current worker rosters, model values, reasoning settings, measured budgets, cadences, server identities, addresses, capacities, account inventories, installed toolchain versions, and similar fast-changing values stay in their owned policy registries or runbooks. Normative prose may classify such values and constrain their use, but may not freeze the current entries. This applies the mutable-facts ruling recorded with concept acceptance (`dec:decisions:spec-concept-accepted`).

**Rule (Stable constraints govern registries)** · `rule:architecture:stable-constraints-govern-registries`

Every mutable registry must identify its maintaining authority, intended audience, canonical storage, schema, freshness test, allowed update procedure, validation or reconciliation method, security classification, and degraded or missing-data behavior. Entries are read at the time of action and the selected values are captured in execution evidence. A registry may change a choice within those constraints; it may not create an exception to machine rules, audience separation, trust direction, or the trusted final gate. Stale or unowned entries fail closed for the action whose safety depends on them.

**Rule (External contract stability)** · `rule:architecture:external-contract-stability`

Externally consumed stream assignments, framing bytes, exit meanings, and terminal report lines remain byte-stable across ports, refactors, wrapper changes, and provider upgrades. In particular, an implementation must preserve the ordered final-report forms owned by the command contract (`[TOOLS-proto:output:run-report-line]`). Internal convenience is not grounds to change a caller's parser or the semantics on which orchestration branches. Replacing an external contract requires a separate owner-ratified compatibility decision; it is not an internal-state migration.

**Protocol (Internal state migration)** · `proto:architecture:internal-state-migration`

An owner may change a private state-file or run-directory shape only after classifying every affected field as internal and declaring a migration. The owner first records the old and new shapes and all readers and writers, then provides conversion or a bounded dual-read path, preserves a recoverable old state, verifies equivalent externally visible outcomes, deploys the cutover atomically, and removes compatibility support only after the declared window and evidence are complete. A failed cutover restores the prior producer and state together; partial forward migration is not a recovery state.

**Requirement (Migration declaration)** · `req:architecture:migration-declaration`

Before any producer writes a new internal shape, its declaration must name the maintaining authority, affected stores and processes, compatibility scope, old-to-new conversion, treatment of in-flight and missing state, atomicity boundary, backup and rollback procedure, cutover and retirement conditions, and evidence that external contracts and outcomes are unchanged. It must also state why the changed fields are internal. An undeclared shape change, a one-way conversion with no recoverable rollback, or evidence measured against different source state blocks deployment.

## Architecture evidence · `sec:architecture:architecture-evidence`

This division makes violations observable and recovery testable. Architecture conformance is established from current sources and deployed surfaces, not from the prose's assertion that they agree.

**Scenario (Instruction-surface contamination)** · `scenario:architecture:instruction-surface-contamination`

Contamination is detected when a worker receives orchestration-only phrases or scope markers, a harness discovers the other harness's charter, a transcript shows an undeclared instruction source, or an audience audit cannot account for every delivered rule. The worker reports the scope failure and follows only the uncontaminated machine rules, matching charter, and brief needed to stop safely. Its output from the contaminated context is retained as untrusted evidence and is not integrated on confidence alone.

Recovery preserves the transcript, disables the faulty delivery path, and repairs the owning hook, discovery configuration, repository instruction file, or deployed copy. The orchestrator audits all sibling contexts for the same path, starts a clean context with the intended instruction chain, and repeats the affected read-back or work. Resuming a context whose prompt still contains the contaminating surface is not recovery. Integration and publication remain blocked until the clean rerun and audience audit agree.

**Scenario (Stale machine fact)** · `scenario:architecture:stale-machine-fact`

Staleness is detected when a charter, brief template, runbook, registry, or deployed helper contradicts the governing machine-rule record, or when an audited live constraint shows that the governing record itself needs owner reconciliation. The affected action stops before unsafe execution. No lower surface chooses the convenient value or edits around the conflict.

The machine-fact authority first validates the live constraint and, if needed, updates the governing record. The owners of every derived charter, runbook, template, configuration, and deployed copy then reconcile their surfaces in precedence order and audit other audiences for the same stale fact. Contexts that already consumed the stale value are restarted or explicitly refreshed, and their affected evidence is rerun. Recovery completes only when the governing fact, all required deliveries, and a fresh execution observation agree.

**Verification (Authority matrix)** · `verif:architecture:authority-matrix`

Verification discovers every rule-bearing source, delivery mechanism, mutable store, executable contract, and verdict path, then recomputes a row for each governed fact. It does not trust copied documentation as the inventory. Each row must contain the fact class, sole maintaining authority, canonical source, intended audience, delivery path, applicable higher-precedence source, mutable replicas, evidence producer, and trusted verifier.

|Fact class|Sole authority|Permitted audience|Required check|
|----------|--------------|------------------|--------------|
|Universal machine constraint|Machine-rule authority|Every governed session or synchronized charter surface|Lower copies equal the current governing record and declare no exception.|
|Dispatch and supervision policy|Corpus owner through `docs/spec/dispatch.md`, `docs/spec/architecture.md`, `docs/spec/server.md`, and `docs/spec/conformance.md`|Top-level orchestrator|The orchestrator-only rulebook delivers the parts' location; no worker or runbook surface originates the policy.|
|Standing worker discipline|Matching harness-charter owner|Workers of that harness|Discovery contains only the audited charter chain and obeys machine rules.|
|One assignment|Dispatching orchestrator|One named worker and step|Brief scope is within the charter and every continuation preserves identity.|
|Mutable operational value|Named registry or runbook owner|Authorized on-demand readers|Freshness, validation, and stable normative constraints all hold.|
|Runtime behavior|Owning executable contract|Invoking harness and callers|Observed streams, statuses, state ownership, and reports conform; differences are findings.|
|Acceptance verdict|Reviewing orchestrator on trusted-host state|Gate and publication consumers|Quarantine, review, integration, and verification all refer to the exact accepted state.|

The verification passes only if every fact has exactly one owner, every delivery reaches only its intended audience, copied facts reconcile to their canonical source, both harnesses terminate at the same reviewer, no server return bypasses quarantine, every dynamic value remains in an owned registry, and every state-shape change has a complete migration declaration. The two contamination scenarios must be exercised far enough to demonstrate detection, safe stop, repair, clean-context recovery, and renewed evidence.

**Gate (Architecture conformance)** · `gate:architecture:architecture-conformance`

Specification publication is blocked until the authority-matrix verification (`verif:architecture:authority-matrix`) has no unresolved row and every part uses the actor, authority, audience, harness, trust, and state meanings fixed here. In particular, no part may grant a worker orchestration authority, grant a server source or verdict authority, deliver a rulebook to the wrong audience, leave mutable state without one owner, embed current registry values as normative facts, bypass quarantined review, weaken the trusted final gate, or migrate an external contract as internal state.

The gate also requires evidence for both failure scenarios, equivalent review outcomes from both harness boundaries, stable external command contracts, and a trusted verdict over the exact reviewed publication source. A server-green run or clean prose check is necessary evidence where applicable, but neither substitutes for this host-side architecture verdict.

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

**Rule (Letters context)** · `rule:hooks:letters-context`

At SessionStart, UserPromptSubmit and Stop, the letters hook resolves the loop from the working-directory project and reads its inbox through `enter-loop LOOP -- letters list`. It accepts the current five-field metadata shape with a quoted decoded subject and renders a stateless tail over `new/` and `cur/`, newest first. The header carries the full unread count; each row names the letter, sender, posting instant and unread status. Feedback is bounded by eight entries and 4096 UTF-8 bytes including heading and omission text, within the composed twenty-line ceiling. It has no per-turn delivery receipts; old receipt files have no effect. Read history alone cannot cause a letters block, while unread-letter composition and heartbeat counters retain their behavior. The entry deadline is five seconds; failures fail open. The loop inbox watcher's hand-back is the notification route of record (`proto:dispatch:inbox-watcher`), this tail is the second route, and the inbox directory is the durable record. The session compares names and ignores known ones.

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

# Server execution and trust · `spec:server:server-execution-and-trust`

This part fixes the durable constraints for shared server execution and the review path by which its results return to trusted host state. It realizes the server outline (`sec:assembly:server-outline`) and refines the architectural trust direction without freezing mutable operating facts. Current aliases, identities, capacities, versions, storage selections, and authentication material remain registry data, as required by (`rule:architecture:dynamic-facts-stay-in-registries`). Every label minted here has area `server`.

## Scope · `sec:server:scope`

This division separates stable server constraints from the facts needed to operate a particular shared instance. It governs isolation, restoration, storage classes, execution evidence, source transport, and returned-material review. It does not choose an instance, allocate a current identity, pin a toolchain version, describe a provider, or govern installation and deployment on the trusted host.

**Definition (Shared instance)** · `def:server:shared-instance`

A shared instance is a replaceable compute host whose resource pool and lifecycle are shared by two or more isolated superloops. Sharing permits management-owned tools and transport infrastructure, but it does not permit one loop to read, write, signal, impersonate, or account for another loop's private state. The instance is an execution domain, never a source of record; loss of all instance-local state is an expected recovery case.

**Definition (Loop account)** · `def:server:loop-account`

A loop account is the operating-system security principal and private mutable workspace assigned to exactly one superloop. It owns that loop's home state, work tree, temporary data, package cache, build targets, process set, and authentication material. Its current system identity and storage placement are registry facts. Reusing one loop account for another superloop, or allowing a superloop to conduct routine work through a management identity, violates this definition.

**Definition (Server registry)** · `def:server:server-registry`

The server registry is the mutable, access-controlled runbook maintained by the orchestrator for server selection and recovery. It owns the current alias roster; observed capabilities and restrictions with audit freshness; loop and management account allocations; references to host-held authentication and bootstrap inputs; storage, toolchain, and hub selections; and the recovery notes needed to replace an instance. It records references and classifications rather than publishing secret material.

Every action reads the registry at action time and captures the selected alias, relevant capability claims, and audit freshness in its evidence. A missing owner, stale safety-critical observation, ambiguous account mapping, or unresolved restriction fails closed for the affected action. Registry changes may select new values, but may not weaken any invariant in this part.

**Definition (Git hub)** · `def:server:git-hub`

A Git hub is a management-owned bare repository on the shared instance used only to transport explicitly named source objects between the trusted host and one loop's disposable clone. It has no authoritative branch, working tree, build step, content-triggered hook, or integration authority. Each loop has a distinct hub boundary. Possession, recency, or successful verification of an object in the hub cannot promote that object to reviewed host state.

**Definition (Quarantined reference)** · `def:server:quarantined-reference`

A quarantined reference is a host-side reference in a non-executing namespace that names returned source without updating an authoritative branch, tag, staging state, working tree, deployment input, or executable search surface. Its object identity, originating run, input identity, and transport provenance remain fixed for the duration of review. Promotion requires a separate, explicit selection from this reference through the return-review protocol (`proto:server:return-review`).

## Operations profile · `sec:server:operations-profile`

**Definition (Operations profile)** · `def:server:operations-profile`

One loop holds the operations profile for provisioning, server administration and sharing resources among loops. It serves the other loops by keeping their compute, accounts, tools and working doors available and answering reported friction. One holder lets each other loop concentrate on its engineering instead of duplicating shared operations.

**Rule (Arbitration gives no holder precedence)** · `rule:server:operations-arbitration`

The holder arbitrates when loops contend for a resource. It measures who holds what, since when and what is waiting before deciding, gives the reason with its decision, and tells the waiting loop how long it must wait. It prefers adding capacity or re-timing work to refusal, and its own lanes gain no precedence from holding the profile; an arbiter that also serves is trusted only while it takes no advantage.

**Requirement (Measure held resources for arbitration)** · `req:server:contention-measurement`

Contention concerns what is held without sharing or can fill: a GPU is pinned to one holder, and memory and storage fill, while the kernel ordinarily shares processor cores among runnable work. Arbitration measures, in order, each GPU's holder and duration, memory in use with its largest holders, and free space per volume; load average does not answer those questions. An idle holder is asked to release before another loop is made to wait (`rule:server:operations-arbitration`).

**Rule (Fresh-server handover grants root actions)** · `rule:server:fresh-server-root-handover`

Root actions on a compute server belong to the holder of the operations profile after a person hands over a fresh server; that handover is the grant. The holder reads and records freshness at handover before touching server state. If the server holds anything the system did not put there, it stops before touching any of it, reports what it found to the person, and proceeds only on that person's answer, because no report can give back data that was not the system's (`def:server:operations-profile`).

**Rule (Hotfix debt against a held loop)** · `rule:server:hotfix-debt-against-a-held-loop`

When a loop is blocked on a defect in a shared tool, the holder weighs the wall the loop loses against what the full engineering process would add before choosing the route, and the decision names the loop's waiting time. A hotfix is the smallest change that unblocks the loop: one review round, then its own deploy the moment its gate is green, never batched behind sibling lanes, because a hold-and-rename costs milliseconds while a batched deploy holds the loop for every sibling's rounds. A hotfix is a debt: the proper fix follows as its own lane and replaces the hotfix outright, with no compatibility path kept for the hotfix's shape, and every finding the review makes beyond the minimum is recorded as a backlog item the same day (`def:server:operations-profile`). The decision is the holder's arbitration of a shared tool and carries the same measured reason (`rule:server:operations-arbitration`).

**Requirement (Waiting time is measured and read)** · `req:server:waiting-time-measured`

The holder keeps each loop's waiting time as a measured number in its state, from the letter that reported the block to the completion that lifts it, and reads it at every ordering decision, as arbitration reads holders and durations (`rule:server:operations-arbitration`). Having the number is the floor; the question asked of it is what the time costs, and a decision that cannot say what a loop's hour buys has not been made. A wait is placed on the event it awaits, a barrier such as a hand-back, a socket accept, a child's exit or a file's appearance, and a deadline only bounds that wait: a deadline over a sleep-poll measures nothing but the poll and turns a hang into a late failure, so it is no wait of record and no deadline of record.

## Identity and isolation · `sec:server:identity-and-isolation`

This division constrains how connection aliases, management privilege, loop accounts, and authentication boundaries compose on a shared instance. The registry supplies current selections; these rules determine whether those selections are admissible.

**Rule (Alias-only addressing)** · `rule:server:alias-only-addressing`

Repository prose, command contracts, automation inputs, retained reports, and operator instructions shall identify a server only by a registered connection alias. Raw network addresses and transport ports belong solely to the access-controlled client configuration that resolves those aliases. A command shall accept an alias as one indivisible argument and shall not construct, parse, print, or persist endpoint literals.

Before a server action starts, the caller shall prove that the selected alias exists in the current registry and resolves through the owned client configuration. Evidence that exposes an endpoint literal is rejected for retention and handled at that configuration boundary; it is not copied into a repository record or terminal report.

**Rule (Management-account boundary)** · `rule:server:management-account-boundary`

The privileged management account is reserved for reconciling loop accounts, installing or updating shared immutable tools, maintaining shared storage surfaces and hubs, and repairing bootstrap-owned permissions. It shall not run routine builds, tests, worker commands, or source edits, and it shall not hold a loop's private cache or mutable work tree. Management activity uses its own alias and authentication boundary and records the affected management-owned objects.

Loop accounts shall neither acquire management privilege nor modify another loop's account, hub, tools, or private surfaces. A bootstrap action may place loop-owned inputs on behalf of a loop, but ownership and permissions must be reconciled before routine work begins.

**Invariant (Per-loop isolation)** · `inv:server:per-loop-isolation`

At every runnable state, each superloop has exactly one loop account and a distinct home, work directory, temporary area, package cache, build-target area, process boundary, hub, and authentication set. Only that account and the management account acting within bootstrap may write its private surfaces. Shared toolchains are read-only to loop accounts; shared capacity does not make cache entries, environment state, logs, or credentials cross-readable.

Isolation is checked after bootstrap and before accepting work. Any ambiguous ownership, shared mutable cache, inherited credential, writable shared tool, or cross-loop access blocks the affected accounts until bootstrap restores the declared ownership and a fresh isolation check passes.

## Bootstrap and storage · `sec:server:bootstrap-and-storage`

This division makes loss and partial setup recoverable while preserving per-loop ownership. It classifies toolchains, workspaces, caches, and build artifacts by mutability and cleanup authority rather than by current paths or sizes.

**Protocol (Ephemeral bootstrap)** · `proto:server:ephemeral-bootstrap`

An empty, restarted, or partially configured shared instance is restored in this order:

1. Read the current registry on the trusted host, validate its owner and freshness, select only a registered management alias, and stop if a required restriction or input is unresolved.
2. Transfer the trusted bootstrap program, execution wrapper, and declared account, authentication, storage, tool, and hub inputs through the management boundary; instance-local remnants are not accepted as inputs.
3. Invoke the transferred wrapper around bootstrap, then reconcile each loop account, private home, loop workspace, authentication set, and ownership boundary, creating only missing state and correcting drift.
4. Reconcile management-owned immutable toolchains, disk accounting helpers, and bare hubs; then make shared tools read-only to loop accounts.
5. Establish each loop's disk-backed temporary area, private package cache, private build targets, and disposable clone, and verify that environment selection cannot fall back to a constrained system temporary surface.
6. Repopulate each hub from reviewed host source, force each disposable clone to its declared input object, remove residual work-tree state, and prove that the resulting clone is clean.
7. Audit account isolation, management separation, tool ownership, workspace selection, wrapper reporting, and hub object identity. Admit routine work only when every check passes and the bootstrap evidence names the registry revision used.

**Requirement (Idempotent bootstrap)** · `req:server:idempotent-bootstrap`

Bootstrap shall reconcile declared state rather than append presumed-missing state. Reapplying the same trusted inputs after success or interruption must not allocate a second account, duplicate authentication material, fork a hub, create another cache owner, change a reviewed object identity, or broaden a permission. Already-correct objects are left semantically unchanged; drifted objects are repaired to the declared owner, mode, and content.

Each step records completion only after its postcondition is true. Failure leaves enough step evidence for a later invocation to re-evaluate the same postcondition safely. Destructive replacement of loop evidence or reviewed source is never an implicit consequence of retry; it requires separately recorded cleanup authority.

**Rule (Cross-loop probes only read)** · `rule:server:cross-loop-probes-only-read`

A probe of another loop uses commands that only read its state. The superloop runs a command that prepares a home only for that command's own loop name, because preparation mutates the subject and cannot be treated as observation of a peer. It records a cross-loop finding for authorized repair through the affected loop's operation.

**Rule (Host is restore source)** · `rule:server:host-is-restore-source`

The trusted host is the source of record for bootstrap logic, account and authentication declarations, reviewed source, hub input objects, and the registry facts used to recreate an ephemeral instance. Surviving server state may be inspected as untrusted recovery evidence but shall not override those inputs. This is the operational restore consequence of the one-way authority rule (`rule:architecture:host-to-server-direction`).

Material that exists only on a failed or retiring instance is either discardable or must first return through quarantine and review. A replacement instance is not considered recovered until it can be bootstrapped from host-held inputs without depending on its predecessor.

**Rule (Shared toolchains, private caches)** · `rule:server:shared-toolchains-private-caches`

Management may install one immutable toolchain set for compatible loops to read and execute. Loop accounts shall not update it, place extensions in it, or select an unregistered version. Tool selection and update provenance are registry and bootstrap evidence.

Every package cache, build target, incremental state store, and generated dependency state is owned privately by one loop account under its assigned workspace. No cache key, lock, writable directory, or environment fallback may redirect a loop into another loop's state or into the shared toolchain store.

**Rule (Disk-backed workspace)** · `rule:server:disk-backed-workspace`

Large source work, temporary data, downloads, package caches, build targets, logs, and generated artifacts shall reside on the loop's assigned disk-backed workspace surface. The system temporary surface is reserved for small bounded control data and shall not receive a build or bulk transfer. Disk-backed describes placement and capacity behavior, not durability across instance replacement.

Before a large action, the wrapper or caller verifies that the assigned workspace is mounted as declared, is owned by the loop account, and has the required run-specific margin. Missing placement, fallback to the system temporary surface, or insufficient margin prevents launch and is reported as evidence.

**Rule (Disposable build artifacts)** · `rule:server:disposable-build-artifacts`

Loop-owned build targets and regenerable temporary artifacts may be removed at campaign boundaries or to recover workspace margin. Cleanup must resolve one loop and one artifact class before deletion, exclude source objects, hubs, shared tools, authentication material, run reports, and retained review evidence, and record what class was reclaimed.

When space falls below a run's declared margin, new heavy work stops, current usage is measured, and only authorized disposable classes are reclaimed. Space is measured again before work resumes. If the margin remains insufficient, the run returns the measurements and waits for a storage-policy decision rather than widening cleanup scope.

## Execution and reporting · `sec:server:execution-and-reporting`

This division sends routine computation to the compute domain while making priority, time, space, progress, and completion observable to the reviewing orchestrator.

**Rule (Server-first computation)** · `rule:server:server-first-computation`

Routine development builds, tests, documentation checks, linters, and other heavy or recurring computation shall run on a shared instance. Binaries used in that domain are built there. Trusted-host release and installation work remains governed by the accepted topology decision (`dec:decisions:build-deployment-topology`); it is not an implied exception for routine development computation.

Moving a command to the server changes only its execution location. Reviewed source still flows from the trusted host, returned bytes remain data, and the final verdict remains host-owned.

**Rule (Minimum build priority)** · `rule:server:minimum-build-priority`

Batch build workloads and all descendants shall run at the lowest scheduling priority available in the compute domain. Priority is established before the first expensive child starts and is captured in run evidence. A worker may not raise its own batch priority to improve elapsed time.

If the requested minimum cannot be established or inherited, the wrapper shall fail before the batch workload and report that condition. Management and callback control operations may use the minimum responsiveness needed to maintain the instance, but they may not perform build work outside the batch priority boundary.

**Rule (Lighter-node placement)** · `rule:server:lighter-node-placement`

Before a launch, the caller reads the current load of every compute node registered for its loop and places the run on the lighter one, recording both readings in the run's evidence. The node list and the load reader are registry data (`def:server:server-registry`); the placement rule is durable.

**Specification (Run wrapper)** · `spec:server:run-wrapper`

Every server command runs beneath the server wrapper. The wrapper starts the child without reinterpreting repository content as command text, relays and drains all child evidence, preserves the child's declared status unless the wrapper itself fails, measures elapsed wall time and both required storage surfaces, and publishes one terminal report as its last authored line.

The exact stream, field order, field meanings, status relation, and terminal line shape are owned by (`[TOOLS-spec:output:server-wrapper-report]`). This part adds no alternate report form. Signal, launch, measurement, and relay failures must still terminate through that contract with the wrapper's truthful status rather than a fabricated child success.

**Requirement (Wall and space reporting)** · `req:server:wall-and-space-reporting`

Each completed or failed server run records the returned status, elapsed wall duration, remaining capacity on the system temporary surface, and remaining capacity on the assigned workspace surface. Measurements are taken at the wrapper boundary after child output is drained, are bound to the same run identity, and remain present on non-success paths.

An unavailable, stale, malformed, or wrong-surface measurement is a wrapper failure, not an unknown value that may be omitted or guessed. The terminal report contract is the evidence for completion, duration, and space (`[TOOLS-req:output:result-after-exit]`).

**Rule (Gateway-served iteration)** · `rule:server:gateway-served-iteration`

A lane that iterates on Rust is registered with the lane gateway, which the orchestrator serves, and runs its server rounds through that gateway under the runbook's protocol, so its rounds are pre-cleared commands with recorded output, status, and wall rather than ad hoc remote shells.

**Rule (Budgeted server run)** · `rule:server:budgeted-server-run`

Before each recurring server action starts, its dispatch records an expected wall duration, a tolerated excess, the evidence used to choose them, and the authority that may extend or stop the action. These values are run data, not constants in this specification. A run without a declared expectation and tolerance is not eligible for unattended waiting.

Budget expiry and stalled progress are distinct observations. Continued log movement after the tolerated duration produces an over-budget callback and a continue-or-stop decision; it does not silently revise the budget. Lack of movement is handled by the silent-job scenario (`scenario:server:silent-remote-job`). Actual wall duration is retained even when the job is stopped or the wrapper fails.

**Protocol (Remote callback)** · `proto:server:remote-callback`

Detached server work returns control through this sequence:

1. Allocate a run identity, private append-only log, and completion marker in the loop workspace, and record the expected duration, tolerance, movement interval, and silence threshold.
2. Launch the job beneath the run wrapper so that it atomically publishes the completion marker only after child evidence and the terminal report are durable.
3. Before yielding, assign the duty to the lane's Sonnet watcher, bound to the registered alias, run identity, evidence location and absolute UTC deadline. A step or gate without that watcher is a dispatch defect, corrected by handing it the duty; no session-side waiter substitutes for it.
4. The watcher observes completion and log movement through the runbook's bounded calls. For a gate it polls the declared output for progress, total and exit lines until the gate exit line appears; on completion it relays the final evidence once by hand-back, on silence or the absolute UTC deadline it reports the missing evidence, and on budget excess with movement it reports an over-budget observation without inventing completion.
5. The session reconciles the hand-back with the run identity and decides. Resume a live watcher by message; only a dead watcher is replaced, after stopping its surviving tool process and recovering retained observation state, without relaunching the server job or duplicating a terminal delivery (`scenario:dispatch:log-eater-loss`).

**Scenario (Silent remote job)** · `scenario:server:silent-remote-job`

Detection occurs when the completion marker is absent and the watched log has not advanced for the entire declared silence threshold. The Sonnet watcher classifies the observation as stalled, captures the run identity, threshold, last log position and movement time, marker state, and bounded final log evidence, and returns that evidence to the orchestrator. Silence is not reported as success and is not proof that the remote process exited.

Recovery first reconnects through the registered alias and reconciles the marker, log, wrapper process, and available run evidence. A completed job is reported once; a live but blocked job remains stalled for an explicit continue-or-terminate decision; a lost job is relaunched only after the prior identity is proved incapable of later completion. A live Sonnet watcher is corrected by message; a dead one is replaced from retained observation state after its surviving tool process is stopped, never by starting a second copy of the job.

## Hub and trust · `sec:server:hub-and-trust`

This division operationalizes the one-way authority boundary. Reviewed source moves to a disposable compute clone; source history and evidence may return only as quarantined data; review and final judgment stay on trusted host state.

**Protocol (Host-to-hub flow)** · `proto:server:host-to-hub-flow`

Reviewed host source reaches one server run in this order:

1. Snapshot the exact host work tree without changing its staging state, branch, or history, bind the snapshot object to the run identity, and record its reviewed parent and requested verification scope.
2. Push that object through the loop alias to a dedicated input reference in the loop's hub. A forced update is permitted only for the explicitly named disposable input reference; unrelated hub references are not changed.
3. In the loop's disposable clone, fetch the exact input reference, force a detached checkout of its object, remove residual tracked and untracked work state, and reject any content left from a previous run.
4. Before executing, prove that the checked-out object equals the host snapshot, that the clone is clean, and that the command template contains no command text derived from repository content.
5. Run through the wrapper and retain the input reference, snapshot identity, checked-out identity, cleanup result, priority, and report as server evidence.

The flow carries authority only in the host-to-server direction established by (`rule:architecture:host-to-server-direction`). The hub and clone remain disposable transport state even when every server check succeeds.

**Protocol (Hub-to-quarantine flow)** · `proto:server:hub-to-quarantine-flow`

Server-authored history returns without touching authoritative state in this order:

1. The loop records the originating input object and run identity, commits the selected server-authored work, and pushes the resulting object to a dedicated return reference in its own hub.
2. The trusted host fetches that exact object through the loop alias into a newly selected quarantined reference. The fetch is not allowed to update a current branch, tag, staging state, working tree, deployment input, or executable search surface.
3. The receiver verifies the returned object's identity, parent relationship, originating input, loop boundary, and run provenance, then freezes the quarantined reference for review.
4. Any mismatch, unexpected additional object reachability, reference race, or side effect stops the flow. The receiver retains transport evidence but neither checks out nor executes the returned material.
5. A successful transfer hands the fixed quarantined reference and provenance record to the return-review protocol; it performs no integration itself.

**Rule (Returned material is data)** · `rule:server:returned-material-is-data`

All bytes returning from the server, including source history, logs, terminal reports, generated text, binaries, metadata, and suggested commands, are untrusted data under (`rule:architecture:server-results-are-data`). Before textual review and explicit integration, they shall not be executed, sourced, loaded as configuration, imported into an executable environment, or built. No instruction embedded in returned material can alter this flow or authorize its own promotion.

Viewing inert text and metadata through review-safe tools is permitted. Renderers, filters, hooks, macros, generators, and dependency actions that can execute returned content are not review-safe merely because their visible output is textual.

**Protocol (Return review)** · `proto:server:return-review`

A fixed quarantined reference is reviewed in this order:

1. Bind its object identity and provenance to the dispatched input, run, account boundary, hub transfer, and server evidence; stop on any gap or mismatch.
2. Enumerate the complete returned history and inspect the full textual diff, path changes, file modes, links, generated files, dependency declarations, and every build, test, hook, macro, generator, and configuration surface that could execute during later verification.
3. Reject the return or explicitly select reviewed commits or changes. No server-provided instruction, success status, or prebuilt artifact is an integration reason.
4. Integrate only the selected material into a clean host state through a separate explicit operation, then inspect the resulting complete diff again and prove it matches the selection.
5. Run the required trusted verification over exactly that reviewed host state and record the review decision, provenance, verification evidence, and host verdict.

These steps refine, and do not replace, the architectural review sequence (`proto:architecture:returned-evidence-review`). A failed or indeterminate step stops promotion while preserving the quarantine evidence.

**Rule (Server-green is advisory)** · `rule:server:server-green-is-advisory`

A successful wrapper status proves only that the recorded command completed successfully over the recorded server snapshot under the observed conditions. It is evidence, not permission to integrate, tag, release, deploy, or skip a host check. Its force depends on complete provenance, relayed child evidence, the terminal wrapper report, and identity agreement across the input flow.

The reviewing orchestrator applies the trusted final-gate invariant (`inv:architecture:trusted-final-gate`). If later review or host verification disagrees with a server-green result, the host result controls and the disagreement is retained as a finding rather than explained away by the earlier success.

**Verification (Server evidence)** · `verif:server:server-evidence`

A server execution path conforms only when an evidence replay checks all of the following conditions:

1. Every connection selection is a current registered alias, and no retained command or report contains endpoint or current identity data.
2. Management activity is separated from routine work, and each loop's home, work, temporary, cache, target, process, hub, and authentication surfaces satisfy the per-loop isolation invariant (`inv:server:per-loop-isolation`).
3. Bootstrap succeeds from trusted host inputs on empty state and, when applied again, produces no duplicate allocation, broadened permission, or changed source identity.
4. Shared toolchains are management-owned and immutable to loops; caches and targets are private; large work uses the assigned disk-backed surface; and cleanup touches only declared disposable classes.
5. A success child, a failing child, and a wrapper-side failure each preserve child evidence and satisfy the stream, field-order, status, measurement, and terminal-line contract in (`[TOOLS-spec:output:server-wrapper-report]`). Both space values identify the required surfaces, are current at completion, and agree with an independent measurement.
6. Batch descendants run at the domain's minimum priority, and the evidence records the expected duration, tolerance, actual wall duration, movement, and any budget decision.
7. Callback trials return completion after movement and return stalled after induced silence without duplicating the job or callback. Replacing a dead watcher resumes from retained observation state.
8. Hub replay proves the pushed input object, forced detached checkout, clean disposable clone, returned object, frozen quarantined reference, complete textual review, selected integration, and final reviewed-host state form one provenance chain.

Missing evidence, an unchecked condition, an unexpected side effect, or an identity mismatch fails this verification. A green server command cannot be used to fill the gap.

**Gate (Trusted-host verdict)** · `gate:server:trusted-host-verdict`

Release or deployment may proceed only when the reviewing orchestrator checks all gate conditions:

1. The candidate is the exact clean host state produced by explicit integration from a fixed quarantine.
2. The complete return and every executable surface were textually reviewed.
3. Input, hub, run, return, selection, and candidate identities form an unbroken provenance chain.
4. The required final verification ran over that exact candidate.
5. No failure, indeterminate check, or server-to-host disagreement remains unresolved.

The verdict is recorded on reviewed host state in accordance with (`inv:architecture:trusted-final-gate`). Server reports remain attached as advisory evidence and cannot satisfy a missing gate condition. If any condition cannot be proved, the gate is closed and no release or deployment authority is issued.

# Build and deployment topology · `spec:deployment:build-and-deployment-topology`

This part specifies the agent execution environment and the orchestrator's selection of execution domains, containers, scheduling priority and routine toolchains (`sec:assembly:deployment-outline`). Tool construction, installation, managed-copy semantics and deployment evidence belong to (`[TOOLS-spec:deployment:tool-build-and-install-contracts]`). Every label minted here has area `deployment`.

## Scope · `sec:deployment:scope`

This part owns the agent container, execution-domain selection, dedicated tool containers, minimum build priority, interpretation of contention, routine toolchain selection and formatter resolution. Implementation languages, build and install mechanisms, cache and storage contracts, milestone admission, target mappings, copy and backup behavior, and deployment evidence are specified by (`[TOOLS-spec:deployment:tool-build-and-install-contracts]`).

It does not own a helper's externally visible behavior, the hook transition system, or operation of the compute server. A replacement preserves its public bytes and statuses under (`rule:architecture:external-contract-stability`), and the rulebook target preserves the input transition required by (`proto:hooks:rulebook-change-notice`). Server connection, wrapper, callback, and lifecycle behavior remains governed by the server part; this part cites that part only to select and constrain a build domain.

**Definition (Agent container)** · `def:deployment:agent-container`

The agent container is the toolbox container in which an agent's shell runs on the trusted host; it is not the host shell. Host tools and the container engine are not on its path: a host command runs through the host escape, and a project's own containers run on the host's engine, reached through the same escape. Project directories are bind-mounted into those containers, so files are edited at their host paths and only execution passes through the container; a project's own documents name its container, mount point and ports. The container's name, image and escape command are machine-registry values under (`rule:architecture:dynamic-facts-stay-in-registries`).

## Build domains · `sec:deployment:build-domains`

This division governs execution-domain selection, dedicated containers, scheduling priority and routine toolchains. The tool build and install contracts supply the cache and temporary-storage requirements (`[TOOLS-spec:deployment:tool-build-and-install-contracts]`); compute-server operation remains with the server part.

**Rule (Build where executed)** · `rule:deployment:build-where-executed`

An executable shall be built in the execution domain in which its installed or deployed copy will run: server helpers on the server, and trusted-host helpers on the trusted host. Data-only targets are copied from the tagged tree and do not acquire a build domain. The trusted host builds every host-executed binary from a clean checkout of the tools repository at the tagged commit. The generic and instance repositories install only copies and renders of tracked files, so neither acquires a build domain. Their installs run on the trusted host with the deployed tools from clean tagged checkouts at minimum priority and with a disk-backed temporary root; exact paths remain registry data. Each build domain uses one Meson build directory and one Cargo target directory per purpose, with its own package cache and toolchain selection (`[TOOLS-rule:buildcontracts:build-provenance]`).

An artifact crossing a domain boundary is data for inspection, not an executable candidate. A helper whose execution domain changes must follow the execution-domain rebuild protocol (`[TOOLS-proto:deployment:execution-domain-rebuild]`); copying the old binary or renaming its directory is insufficient.

**Rule (Dedicated tool containers)** · `rule:deployment:dedicated-tool-containers`

A tool the host lacks runs in a registered dedicated toolbox, entered through the host escape with the disk-backed temporary root and the project directory explicit. A tool absent from every toolbox is installed into a new dedicated toolbox, never onto the host and never into the agent container (`def:deployment:agent-container`), which stays as provisioned. A new toolbox receives the disk-backed temporary-root profile before first use, and after a toolbox is created or changed its inventory is refreshed from the host's container listing, which is the inventory of record.

**Rule (Minimum build priority)** · `rule:deployment:minimum-build-priority`

Every compile, link, code-generation action, and gate that may rebuild shall start in the lowest-priority scheduling class available in its execution domain, and all expensive descendants shall inherit that class. This applies to server development builds, tagged host builds, and the vendored-checker exception. Priority is established before the first expensive child and its effective class is captured in evidence.

The semantic minimum is a durable constraint; the scheduler name, wrapper, slice, weights, and other mechanism are current machine-registry values. If the selected domain cannot establish or demonstrate the minimum, the build fails before expensive work. Server-side enforcement remains governed by (`rule:server:minimum-build-priority`).

**Remark (Contention slowdown)** · `rem:deployment:contention-slowdown`

Idle scheduling bites only under contention: on an idle machine a minimum-priority build still receives the whole processor. A build slowed by interactive use is therefore the priority rule working as intended; its report notes the contention, and the slower wall is not a regression finding.

**Convention (Routine toolchain)** · `conv:deployment:routine-toolchain`

Routine Rust development, meaning every routine build, test, gate, and formatter run, uses one designated routine toolchain, which is nightly unless a project records another designation with its reason in its own documents; every routine run reuses that designation, so toolchains never alternate between routine runs. Stable and minimum-supported-version runs are not development toolchains: they are reserved for tags, releases, and other significant verification moments, alongside the full multi-toolchain sweeps, and never serve a routine lane or a per-merge gate. Formatter and lint configurations may use nightly-only keys, because the nightly formatter is the formatter of record and a stable run's silent fallback is no verdict.

**Hint (Formatter resolution)** · `hint:deployment:formatter-resolution`

`cargo fmt` resolves through the cargo home's `bin` shims before `PATH`, so inside a toolbox it can run a different rustfmt than the one on `PATH`. Recipes therefore invoke the binary form `cargo-fmt`, which resolves the formatter on `PATH` deterministically.

# Conformance and evidence · `spec:conformance:conformance-and-evidence`

This part governs the connection between normative claims and reproducible evidence, the standing of the participating corpus, the generic specification assembly, and trusted verification (`sec:assembly:conformance-outline`). Linter construction and verification contracts belong to the tools specification (`[TOOLS-spec:conformance:linter-conformance]`); its census and frontier campaign are historical adoption evidence, not measurements of this repository. Every label minted here has area `conformance`.

## Scope · `sec:conformance:scope`

Conformance evaluates the requirements owned by this and the other parts. It does not replace those requirements, choose mutable operating values, or make advisory measurements normative. Its durable subjects are the evidence link, the calculus and owner partition, assembly freshness, whole-corpus measurement, the burn-ratchet principle, the server evidence loop, and the two trusted gates. The test census, graph and shape recomputation, and burn and projection checks are specified by (`[TOOLS-spec:conformance:linter-conformance]`).

**Definition (Conformance claim)** · `def:conformance:conformance-claim`

A conformance claim is a normative statement for which one can identify a reproducible evidence producer and the gate that owns the decision. The claim is passing only when its declared evidence is produced from the source state being judged, reports the required result, and is reviewed at that gate. Prose, an implementation, or a successful command standing alone is not a conformance claim.

**Definition (Trusted evidence)** · `def:conformance:trusted-evidence`

Trusted evidence is evidence in the architectural sense (`term:architecture:evidence`) that a reviewer has produced or recomputed over the exact reviewed authoritative source state and has bound to its scope and result. Server logs, worker reports, generated files, and statuses arrive as candidate evidence. They become trusted only after provenance and source-state identity are checked; successful remote execution never transfers verdict authority, as required by (`inv:architecture:trusted-final-gate`).

**Rule (Unmeasured claims identify their limit)** · `rule:conformance:unmeasured-claims`

A document that states an expected result without a confirming measurement marks the result as not measured in that document. An expectation cannot be promoted to evidence by a later reader's inference; the missing measurement remains visible where the claim is used (`def:conformance:trusted-evidence`).

**Rule (Rules beside compliant material; bites prove inventories)** · `rule:conformance:rule-and-inventory-evidence`

A rule is minted only beside material that obeys it; otherwise its neighbouring example teaches a conflicting rule. The document states known cases without claiming an exhaustive command inventory for programs whose sources can change. Each bite that renames or merges a program derives that program's current command inventory from source and proves the rule against it, so a stale list cannot stand in for the changed program's evidence.

**Terminology (Green check)** · `term:conformance:green-check`

A green check is a declared judging check that completed over its entire scope, returned the status its contract assigns to success, and produced no finding of failing severity. A skipped, filtered, aborted, or unreviewed run is not green. An informational command can complete successfully, but its status does not make the conditions in its advisory listings green.

**Requirement (Failed-test output remains in the gate log)** · `req:conformance:failed-test-output-retained`

A gate retains the output of every test that failed in its log. A failure that does not repeat can be diagnosed only from what the failed test said; its name and the line where it panicked do not preserve its message.

**Rule (Checks are predicates)** · `rule:conformance:checks-are-predicates`

A check is a predicate whose exit status says whether its requirement is met: an unmet requirement makes the command fail, so a caller need not judge its output to know the answer. Reading, searching and listing observe rather than check; a tool whose default success status ignores its own warnings is invoked in a mode that fails on those warnings before its result is used as a check.

**Rule (Ordering and timing evidence)** · `rule:conformance:ordering-and-timing-evidence`

An ordering test asserts order through the program's own events rather than elapsed time. A time bound that is part of the contract is scaled by measurements from the gate's node; a timing failure in an untouched package supplies no causal claim about the candidate without further evidence. A gate's evidence carries, beside each battery's wall time, the cgroup samples with their scope named, the gate's own user and system CPU from process accounting, and the deltas (`req:environment:gate-resource-deltas`), so that a reader of the record alone can tell a slow candidate from a loaded node, and a wall without its deltas is a process defect of the gate form rather than evidence about the candidate.

**Rule (Green gates answer declared checks)** · `rule:conformance:review-beside-gates`

A green gate answers only its declared automated assertions. Review separately reads the construction and trust assumptions of manifest removal, opened-object identity, reported places, executable settings, child capture, plan forms, measurement marks and fixed helpers, because those assumptions can escape the automated checks (`[TOOLS-req:deployment:reversible-manifest-removal]`), (`rule:architecture:opened-object-identity`), (`[TOOLS-req:output:report-path-validity]`), (`req:architecture:executable-settings-trust`), (`req:architecture:bounded-child-result`), (`[TOOLS-req:output:plan-forms-agree]`), (`rule:conformance:unmeasured-claims`), (`rule:architecture:fixed-loop-report-helpers`).

**Requirement (Browser changes name a browser-path test)** · `req:conformance:browser-path-test`

A lane that changes what a browser does names a test that exercises the rendered pages through the browser path, or states that no such test exists yet. Reading a rendered page can reveal faults that static or component checks miss, so repeated review findings on the browser path call for that test rather than another assertion about unrendered source.

**Rule (Review findings converge by reach and fix kind)** · `rule:conformance:review-finding-classes`

Review findings are sorted by whom they reach: a person harmed or misled in ordinary use, a reader slowed, or nobody. Each fix states its kind so one design can resolve several findings and review rounds converge.

**Rule (Reproduce a doubtful finding without the candidate)** · `rule:conformance:reproduce-doubtful-finding`

When reading leaves doubt whether a fault can occur, the reviewer builds the smallest disposable case under the reviewer's scratch directory and shows the occurrence without running the candidate. The reproduction settles whether the fault is possible; argument from the unrun candidate's apparent intent cannot overturn that evidence.

**Signature (Requirement-evidence link)** · `sig:conformance:requirement-evidence-link`

Every passing conformance claim carries six fields: the requirement being judged; the implementation surface that realizes it; the test or deterministic recomputation that examines that surface; the execution domain in which it ran; the result, including source-state identity and terminal status; and the reviewer who accepted or rejected the result. A missing, ambiguous, stale, or unenumerated field breaks the link rather than yielding partial evidence. One producer may support multiple claims only through a complete link for each.

**Table (Conformance matrix)** · `tab:conformance:conformance-matrix`

Displayed local labels in the first column are row keys, not occurrences; imported citations identify contracts in the tools specification (`[TOOLS-spec:conformance:linter-conformance]`). The matrix retains the evidence producers and gates of the adoption campaign, including its historical census and frontier conditions. “Trusted release” means the ordinary release verdict; “specification conformance” means the campaign-closing gate, which also depends on the trusted release verdict.

|Environment|Evidence producer or recomputation|Owning trusted gate|
|-----------|----------------------------------|-------------------|
|``def:conformance:conformance-claim``|Prose/head analysis and matrix completeness|``gate:conformance:trusted-release``|
|``def:conformance:trusted-evidence``|Source-state and reviewer binding in the final verification record|``gate:conformance:trusted-release``|
|``term:conformance:green-check``|Declared command status, scope, and failing-finding count|``gate:conformance:trusted-release``|
|(`[TOOLS-term:conformance:frontier-test]`)|Frontier inventory and unfiltered corpus-test execution|``gate:conformance:specification-conformance``|
|``sig:conformance:requirement-evidence-link``|Final evidence-record field validation|``gate:conformance:trusted-release``|
|``tab:conformance:conformance-matrix``|Outline-to-head and row-to-head bijection check|``gate:conformance:specification-conformance``|
|``inv:conformance:evidence-traceability``|Requirement-evidence link traversal|``gate:conformance:trusted-release``|
|``rule:conformance:displayed-material-does-not-participate``|Markdown participation fixtures and repository prose analysis|``gate:conformance:specification-conformance``|
|``req:conformance:head-validation``|Repository prose verification|``gate:conformance:specification-conformance``|
|``req:conformance:unique-mints``|Repository prose and derived-profile collision passes|``gate:conformance:specification-conformance``|
|``req:conformance:citation-resolution``|Seeded two-pass repository prose analysis|``gate:conformance:specification-conformance``|
|``req:conformance:owner-reach``|Manifest-derived layer pass and reach-register reconciliation|``gate:conformance:trusted-release``|
|(`[TOOLS-req:conformance:current-owner-prefixes]`)|Workspace discovery and owner-register reconciliation|``gate:conformance:trusted-release``|
|(`[TOOLS-req:conformance:carrier-completeness]`)|Carrier traversal and assembly-target exclusion check|``gate:conformance:specification-conformance``|
|(`[TOOLS-req:conformance:source-owner-retargeting]`)|Current-path, owner, shape-scope, and fixture audit|``gate:conformance:specification-conformance``|
|(`[TOOLS-req:conformance:test-profile-adoption]`)|Test census, classification, derivation, and standard-place pass|``gate:conformance:trusted-release``|
|(`[TOOLS-req:conformance:one-mint-per-covered-test]`)|Covered-versus-derived count equality and collision pass|``gate:conformance:specification-conformance``|
|(`[TOOLS-req:conformance:test-derivation-injectivity]`)|Per-owner identifier and full-label collision analysis|``gate:conformance:trusted-release``|
|(`[TOOLS-req:conformance:census-totality]`)|Workspace AST census and parse-failure inventory|``gate:conformance:trusted-release``|
|(`[TOOLS-rule:conformance:census-derived-floor]`)|Live census comparison with the committed census table|``gate:conformance:specification-conformance``|
|(`[TOOLS-tab:conformance:test-census]`)|Member, source-root, attribute, package, and area recount|``gate:conformance:specification-conformance``|
|(`[TOOLS-verif:conformance:live-and-dead-test-citations]`)|Four-outcome resolver fixture over a current covered asset|``gate:conformance:specification-conformance``|
|``req:conformance:assembly-exact-membership``|Bidirectional manifest/directory membership verification|``gate:conformance:specification-conformance``|
|``req:conformance:assembly-live-state``|Dormant, draft, and live state report|``gate:conformance:specification-conformance``|
|``req:conformance:assembly-freshness``|Exact generated-byte comparison|``gate:conformance:specification-conformance``|
|``rule:conformance:generated-publication-nonparticipation``|Adoption exclusion and duplicate-mint analysis|``gate:conformance:specification-conformance``|
|``req:conformance:whole-corpus-shape``|Participating-carrier and measured-document reconciliation|``gate:conformance:specification-conformance``|
|``req:conformance:division-separation``|Named-versus-division shape partitions|``gate:conformance:specification-conformance``|
|(`[TOOLS-req:conformance:shape-distributions]`)|Nearest-rank shape recomputation|``gate:conformance:specification-conformance``|
|(`[TOOLS-verif:conformance:shape-report]`)|Informational shape command plus independent arithmetic checks|``gate:conformance:specification-conformance``|
|(`[TOOLS-req:conformance:graph-resolution-space]`)|Seeded prose-and-code graph construction|``gate:conformance:trusted-release``|
|(`[TOOLS-req:conformance:graph-no-dangling]`)|Resolution findings and graph endpoint traversal|``gate:conformance:trusted-release``|
|(`[TOOLS-req:conformance:graph-hubs]`)|In-degree ranking and partition arithmetic|``gate:conformance:specification-conformance``|
|(`[TOOLS-verif:conformance:graph-report]`)|Informational graph command over the check's analysis|``gate:conformance:specification-conformance``|
|``def:conformance:burn-ratchet``|Growth and stale-entry fixture|``gate:conformance:trusted-release``|
|(`[TOOLS-req:conformance:burn-register-freshness]`)|Six live censuses compared with six committed registers|``gate:conformance:trusted-release``|
|(`[TOOLS-req:conformance:projection-freshness]`)|In-memory regeneration and byte comparison|``gate:conformance:trusted-release``|
|(`[TOOLS-rule:conformance:informational-reports-do-not-judge]`)|Subprocess status and stream-contract tests|``gate:conformance:trusted-release``|
|(`[TOOLS-verif:conformance:repository-prose]`)|Fully seeded repository prose analysis|``gate:conformance:specification-conformance``|
|(`[TOOLS-verif:conformance:repository-census]`)|Live package/area census and committed-floor comparison|``gate:conformance:specification-conformance``|
|(`[TOOLS-verif:conformance:repository-assembly]`)|Read-only assembly verification|``gate:conformance:specification-conformance``|
|(`[TOOLS-verif:conformance:repository-check]`)|Complete adopted linter check|``gate:conformance:trusted-release``|
|``proto:conformance:server-verification-loop``|Server transcript with command, status, timing, and tail|``gate:conformance:trusted-release``|
|``rule:conformance:server-green-is-advisory``|Final-host rerun and source-state match|``gate:conformance:trusted-release``|
|(`[TOOLS-tab:conformance:frontier-ownership]`)|Eight-row frontier inventory audit|``gate:conformance:specification-conformance``|
|(`[TOOLS-verif:conformance:eight-frontier-tests]`)|Unfiltered execution of the eight mapped tests|``gate:conformance:specification-conformance``|
|(`[TOOLS-inv:conformance:existing-greens-remain-green]`)|Full corpus suite with frontier results separated|``gate:conformance:specification-conformance``|
|``gate:conformance:trusted-release``|Reviewer-issued final-host verification record|``gate:conformance:trusted-release``|
|``gate:conformance:specification-conformance``|All-part, publication, frontier, and release aggregation|``gate:conformance:specification-conformance``|

**Invariant (Evidence traceability)** · `inv:conformance:evidence-traceability`

Every claim reported as passing must traverse one complete requirement-evidence link to current authoritative source, the implementation surface inspected, an executable test or deterministic recomputation, its complete terminal status and finding set, and an identified reviewer. The source identity at the beginning and end of that traversal must be the same. A result from a different revision, an unexplained skipped check, a hand-copied summary, or an anonymous approval is a broken trace and blocks the owning gate.

## Calculus and ownership · `sec:conformance:calculus-and-ownership`

This division specifies the participating corpus and the owner-aware reference graph. Linter adoption and source-owner retargeting are specified by (`[TOOLS-spec:conformance:linter-conformance]`); their historical campaign records do not establish the standing of a different source state.

**Rule (Displayed material does not participate)** · `rule:conformance:displayed-material-does-not-participate`

An occurrence inside a fenced block or a doubled-delimiter displayed span mints nothing, cites nothing, creates no import, and is excluded from head and resolution judgments. Participating single-delimiter spans retain their mint or citation meaning. Outline records therefore remain inert under (`conv:assembly:displayed-outline`), and examples may exhibit a label without creating evidence for or against it.

**Requirement (Head validation)** · `req:conformance:head-validation`

In every participating authored document that mints at least one label, each heading below the publication title and each bold environment head must pair with exactly one mint in its own block or sanctioned naming block. Each pair must validate against the adopted kind registry after presentation reduction. A mintless head, headless mint, uncatalogued name, wrong kind, or authored use of a reserved derived kind is a failing finding.

**Requirement (Unique mints)** · `req:conformance:unique-mints`

Within an owner, every authored label must mint exactly once across the complete carrier, including all part files, and every derived label must be unique under its profile. The harvest must report both locations of an authored duplicate; the profile must report every colliding asset. Generated publication copies and generated regions are not a second authority and may not enter the mint registry.

**Requirement (Citation resolution)** · `req:conformance:citation-resolution`

All code-side mints are seeded, all participating prose mints are harvested, and only then are prose and code citations resolved. An unqualified citation must reach exactly one mint in its own owner and must use the parenthesized citation form. A cross-owner citation must additionally bracket one registered prefix with its label and reach one mint in that owner. An unresolved, unregistered, self-qualified or non-parenthesized citation is a failing finding at its source location, and so is the bracket-free cross-owner form: another owner's label cited in the unqualified parenthesized form, which reaches no mint of its own owner and names no prefix. A prefix-label pair written in a code span without its import brackets is not that form but a near miss, warned with the repair that adds the brackets, since one named repair turns it into a well-formed import.

**Requirement (Owner reach)** · `req:conformance:owner-reach`

Resolution does not by itself authorize an import. Package-to-package imports must follow one direct workspace-path dependency derived from the current member manifests, without transitive closure, as fixed by (`[TOOLS-rule:lintcontracts:ownership]`). Every package may cite repository policy upward. Repository-level policy may import no package-owned head, even when the linter crate depends on that package. The derived graph and its committed reach register must agree in both directions.

## Assembly and shape · `sec:conformance:assembly-and-shape`

Assembly turns the authored part set into one publication; shape measures the authored corpus without turning size into a verdict. Both are derived from current carrier state.

**Requirement (Assembly exact membership)** · `req:conformance:assembly-exact-membership`

The root specification manifest must list each of the seven accepted part files exactly once, in owner-approved order, and no other file, as required by (`conv:assembly:assembly`). Each row must name one adjacent Markdown file, not a nested path, the manifest itself, or a duplicate. Verification runs both ways: every row must have a readable part and every Markdown part beside the manifest must have one row. Missing and unlisted parts are findings, and duplicate mints across parts are reported against the authored parts.

**Requirement (Assembly live state)** · `req:conformance:assembly-live-state`

An absent adopted parts directory is dormant only before its rewrite begins. A present manifest carrying the exact draft marker remains draft: membership is still checked, no freshness verdict is formed, and a write is refused. The marker may be removed only after every accepted part exists and membership is clean. Specification release requires the single adopted assembly to be present, non-dormant, non-draft, and verified.

**Requirement (Assembly freshness)** · `req:conformance:assembly-freshness`

For a live assembly, regenerate the publication from the listed part bytes in manifest order using the adopted provenance header and final-line-feed recipe, then compare the complete generated byte string with the committed publication. A missing publication or any byte difference is stale. Read-only verification writes nothing; regeneration may repair staleness but cannot repair missing, invalid, duplicated, or unlisted membership.

**Rule (Generated publication nonparticipation)** · `rule:conformance:generated-publication-nonparticipation`

The part files are the authored and participating sources. The assembled publication is their generated copy and must be excluded from participation, head validation, minting, citation harvesting, shape measurement, and owner imports. External citations continue to resolve to the mint in the owning part. If the publication enters the carrier as participating prose, every copied mint is a duplicate and the gate must fail rather than suppress those findings.

**Requirement (Whole-corpus shape)** · `req:conformance:whole-corpus-shape`

The shape report measures every participating authored Markdown document in the subscribed carrier that contributes a validated environment, with ownership and generated-document exclusion taken from the same accepted plan as the repository check. It selects no configured benchmark set, does not treat a remembered source-corpus path as a standard, and compares the corpus with nothing.

**Requirement (Division separation)** · `req:conformance:division-separation`

Shape measurement must retain every validated division in document and division distributions while excluding divisions from the named-environment word and citation distributions. An environment extends from its head to the next environment head, the next heading of any level, or end of document. Front matter belongs to the document and to no environment. Thus a short organizational heading cannot lower the measurements applied to definitions, requirements, and other named environments.

## Reports and ratchets · `sec:conformance:reports-and-ratchets`

The graph and shape views are review instruments. Burn registers and generated projections are exact checks. Their implementation and verification contracts belong to (`[TOOLS-spec:conformance:linter-conformance]`); an informational listing does not acquire a verdict.

**Definition (Burn ratchet)** · `def:conformance:burn-ratchet`

A burn ratchet is a declared legacy or inventory-remainder family, its exact recognizer and surfaces, and a committed per-file count register. Verification fails when a live file contains more occurrences than registered and when a registered file or count outlives occurrences that have disappeared. Per-file exactness prevents a decrease in one file from paying for growth in another; the stale direction makes the register describe the current corpus rather than an obsolete ceiling.

## Trusted gates · `sec:conformance:trusted-gates`

Server execution supplies correction evidence; authority remains with the reviewed host state. The frontier inventory (`[TOOLS-tab:conformance:frontier-ownership]`) refines the original red-test map (`tab:spec:red-test-map`) as historical adoption evidence; its recorded red or green conditions do not measure this repository.

**Protocol (Server verification loop)** · `proto:conformance:server-verification-loop`

After a worker has completed scoped edits, it yields `READY FOR VERIFY`. The orchestrator identifies the reviewed source state and sends that state to the compute server, where the declared loop runs formatting, linting, and the brief's scoped package and integration tests without silently filtering tests. The returned record identifies source state, commands, scope, statuses, elapsed times, and an evidence tail sufficient to diagnose every failure. A failing round is returned to the same worker for a scoped correction; the cycle repeats and every round is retained until the server loop is green or the task is reported unresolved.

**Rule (Server-green is advisory)** · `rule:conformance:server-green-is-advisory`

A green server loop proves only that the recorded commands passed over the state the server received. It cannot approve source, replace review, establish that returned bytes equal the reviewed host state, or issue the release verdict. The trusted host must inspect the diff, reconcile provenance, and run or commission the final verification over the exact reviewed state, preserving the trusted-final-gate invariant (`inv:architecture:trusted-final-gate`).

**Gate (Trusted release)** · `gate:conformance:trusted-release`

A release is blocked unless all of the following are true over one exact source state: the source and governing records were reviewed; every required requirement-evidence link is complete; all adopted judging checks and scoped tests ran without a failing finding or unexplained skip; formatting and linting passed; generated projections, burn registers, owner declarations, and any live assembly are current; server evidence identifies the same input and is retained; the returned diff and artifacts were quarantined and reviewed; and the trusted host's final verification passed without any intervening unreviewed change. Missing evidence, state mismatch, command failure, status disagreement, unreviewed generation, or absent reviewer blocks. Server success, an informational status, or a worker's report cannot override a blocker.

**Gate (Specification conformance)** · `gate:conformance:specification-conformance`

The specification campaign is blocked until the trusted-release gate passes and all applicable campaign conditions are simultaneously true. The seven generic part files must exist, participate, and match their manifest outlines head for head; the manifest must list exactly those parts in its declared order and be non-draft; and the generated publication must be byte-fresh and nonparticipating. Linter adoption conditions are specified by (`[TOOLS-spec:conformance:linter-conformance]`), including current owner prefixes, carrier completeness, census and floor reconciliation, projections, burn registers, and graph and shape arithmetic. The historical eight-test frontier is judged against its recorded conditions (`[TOOLS-verif:conformance:eight-frontier-tests]`), with preservation of existing greens (`[TOOLS-inv:conformance:existing-greens-remain-green]`); its census and frontier state are adoption evidence, not a claim about this repository's test population. Any missing part or head, extra head, stale artifact or register, unresolved citation, unmet applicable adoption condition, regression, skipped required check, or untrusted final evidence blocks closure.
