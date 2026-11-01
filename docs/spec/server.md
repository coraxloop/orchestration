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
