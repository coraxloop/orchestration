# Concept proposal for the orchestration specification · `proposal:specconcept:orchestration-specification-concept`

The agent-side watching and waiting recipes retained below, including fresh-agent, never-resume, listener and session-side polling instructions, are superseded by (`proto:dispatch:log-eater-callback`) and (`proto:dispatch:heartbeat-supervision`); program interfaces, historical observations and quoted former instructions remain as recorded.

Status: PROPOSAL for corpus-owner review. This document proposes the shape of the specification; it is not the specification and makes no new operational ruling.

The document practices the calculus it proposes to extend. The label at each heading or environment head is that environment's mint; a parenthesized label in running text is a same-owner citation; material in fenced blocks and double-backtick spans is displayed without participating. Every internal label minted here has area `spec`; the title mint uses its document-genre kind and specification-concept area.

## Purpose and boundary · `sec:spec:purpose`

**Proposal (Review boundary)** · `proposal:spec:review-boundary`

The corpus owner should review a proposed subject, partition, vocabulary, and acceptance path before any specification prose is written. This opens the documentation programme deliberately deferred by (`dec:decisions:corpus-adoption-boundary`); it does not reopen the implemented label calculus, the output-mode decision, or the resolved build and deployment rulings. Acceptance authorizes a later specification campaign, not an implementation change.

## Subject of the specification · `sec:spec:subject`

**Definition (System subject)** · `def:spec:system-subject`

The system to be specified is the orchestration of dispatched worker lanes across the Claude Code and Codex harnesses, with routine computation delegated to a shared compute server. Its boundary includes the top-level orchestrator, the worker charters and read-back gates, lane launch/resume/watch/verify helpers, hook state machines, server wrapper and hub, command-output interfaces, trust boundary, and build/deploy path. It excludes the application work that a lane performs and the internals of either model provider.

**Invariant (Authority remains layered)** · `inv:spec:layered-authority`

The specification must preserve the deployed authority split. Machine facts and universal build constraints come from the global machine rules; orchestration policy comes from `ORCHESTRATION.md`; a worker receives its harness charter plus its brief; server facts and the lane wrapper contract come from `local/servers.md`; and executable behavior comes from the deployed helpers. The specification may reconcile these sources, but must not flatten them into one instruction audience or make a lower layer authoritative for a higher one.

**Invariant (Two harnesses, one evidence path)** · `inv:spec:two-harnesses-one-evidence-path`

Claude workers and Codex lanes have different launch and instruction surfaces, but both are dispatched by the same orchestration policy and return evidence to the same reviewing orchestrator. Server output is advisory data across a one-way host-to-server source flow; reviewed host state and the final trusted gate remain authoritative. This is the system-level meaning of the already achieved multi-superloop integration (`dec:decisions:multi-superloop-integration`).

## Proposed specification parts · `sec:spec:parts`

The following are candidate authored parts and candidate benchmark documents. Each paragraph states the part's scope and primary study sources. The final names are intentionally semantic rather than numbered; assembly order belongs to the manifest.

**Part (Architecture and authority)** · `part:spec:architecture`

Candidate `docs/spec/architecture.md` defines actors, trust domains, instruction audiences, the two harness boundaries, ownership of mutable state, and the host/server authority direction. Its primary sources are the deployed global machine rules, `ORCHESTRATION.md`, `local/servers.md`, the Codex worker charter, and the instruction-surface account in the Codex integration runbook.

**Part (Dispatch and supervision)** · `part:spec:dispatch`

Candidate `docs/spec/dispatch.md` specifies worker selection, explicit model and reasoning declarations, read-back gating, normal and degraded rosters, heartbeat supervision, stall recovery, log-eater replacement, and terminal conditions. Its primary sources are the worker-dispatch, degraded-mode, heartbeat, watchdog, and sub-harness sections of `ORCHESTRATION.md`, together with the measured lifecycle in the Codex integration runbook.

**Part (Hook state machines)** · `part:spec:hooks`

Candidate `docs/spec/hooks.md` specifies the orchestrator-scope injection machine and heartbeat-guard machine as states, inputs, transitions, outputs, persistence, deduplication, fail-open cases, and timing bounds. Its primary sources are the deployed `orchestrator.py` and `heartbeat-guard.py`, their rulebook context, the direct-petgraph ruling in the root manifest, and the corresponding backlog entries. The Python implementations are current behavior to model, not instructions to the specification author.

**Part (Worker-lane lifecycle)** · `part:spec:lanes`

Candidate `docs/spec/lanes.md` specifies fresh launch, gated resume, work and verification steps, run directories, event growth, step-owned completion markers, budget classification, stall/runaway handling, feeder offsets, and watcher verdicts. Its primary sources are `codex-lane`, `lane-feed.py`, `lane-watch`, `lane-verify`, the Codex integration runbook, and the worker charter's VERIFY protocol.

**Part (Server execution and trust)** · `part:spec:server`

Candidate `docs/spec/server.md` specifies account isolation, ephemeral bootstrap, shared toolchains, per-loop work and cache locations, the git-hub flow, server-first computation, run-wrapper evidence, space reporting, and the rule that returned server material is data until reviewed. Its primary sources are `local/servers.md`, the server-operations and trust-boundary sections of `ORCHESTRATION.md`, `lane-verify`, and the global build-priority and toolchain rules.

**Part (Command and output contracts)** · `part:spec:output`

The original candidate `docs/spec/output.md` specifies the four sanctioned modes, stream ownership, exit classes, redaction, panic behavior, feeder framing, and the exact final-report forms used by lanes and the server wrapper. It also maps every helper to one mode. The public output specification defines the helper mode assignments and final-report forms (`[TOOLS-tab:output:binary-mode-map]`) and (`[TOOLS-proto:output:run-report-line]`), checked against the current helper scripts and the `cli-common`, `execwrap`, and `linter` package READMEs.

**Part (Build and deployment topology)** · `part:spec:deployment`

Candidate `docs/spec/deployment.md` specifies Rust-or-Meson implementation, server development builds, milestone-tag host builds, build priority and cache placement, content-diffed installs, mtime preservation, and rebuilding helpers in their execution domain. Its primary sources are the pre-design research, the root manifest, the global machine rules, and the backlog decisions on topology, no-shell implementation, Meson installs, milestone cadence, and the Rust `lane-verify` port (`dec:decisions:build-deployment-topology`), (`dec:decisions:no-shell`), (`dec:decisions:meson-installs`), (`dec:decisions:release-cadence`), and (`dec:decisions:lane-verify-rust`).

**Part (Conformance and evidence)** · `part:spec:conformance`

Candidate `docs/spec/conformance.md` specifies requirement-to-test evidence, label participation, owner reach, assembly freshness, benchmark selection, burn ratchets, server verification, and trusted release gates. Its primary sources are the corpus gauntlet, the linter command contract, the label and head readers, the layer-owner graph, the burn registers, the command-output verification gate (`[TOOLS-gate:output:output-conformance]`), and the Codex VERIFY loop.

## Proposed label vocabulary · `sec:spec:label-vocabulary`

**Convention (Area vocabulary)** · `conv:spec:area-vocabulary`

This concept uses area `spec`. The final parts should use the stable conceptual homes `architecture`, `dispatch`, `hooks`, `lanes`, `server`, `output`, `deployment`, and `conformance`, matching the partition above. Areas remain owner-local and never imply ownership. A requirement keeps the area of the concept it governs even when its implementation moves between binaries.

**Convention (Mint families)** · `conv:spec:mint-families`

The final corpus should mint `sec` for document divisions; `def`, `term`, and `sig` for actors, data, and state vocabularies; `spec`, `req`, `rule`, and `inv` for normative behavior; `proto`, `judg`, and `scenario` for sequences, transitions, and exceptional paths; `tab` and `diag` for exact mappings and graphs; `gate` and `verif` for acceptance evidence; `dec` only for owner-ratified choices; and `open` for questions not yet decided. These kinds retain the distinct meanings fixed by (`inv:kinds:distinctness`) and every head must validate through (`judg:kinds:head-validation`).

**Rule (Authored and derived mints)** · `rule:spec:authored-and-derived-mints`

Specification authors mint normative prose environments, not identities for code merely because the prose names a binary, script, event, setting, or test. Asset-family mints remain derived and require an adopted profile and warrant; until such a profile exists, a helper's contract is headed as a Specification, Protocol, Rule, or Requirement. Repository-policy prose uses same-owner citations and imports no package-owned head, following (`[TOOLS-rule:lintcontracts:ownership]`); package implementation documents may cite root policy upward under the owner graph.

## Deferred corpus-test frontier · `sec:spec:corpus-frontier`

**Table (Red-test map)** · `tab:spec:red-test-map`

The vendoring baseline records twenty-seven green corpus tests and the following eight deliberately red tests. The green condition below is the work that must exist before each red test may be changed from frontier evidence into a gate.

|Currently-red test|Proposed part or parts|What must exist before it can go green|
|------------------|----------------------|--------------------------------------|
|`the_repository_prose_is_in_good_standing`|(`part:spec:architecture`), (`part:spec:output`), and (`part:spec:conformance`)|All authored parts are carried and head-valid; every root and code citation names a current mint under the current owner partition; vendored source-owner references are retargeted; and the complete seeded prose analysis has no finding.|
|`the_repository_seeds_one_mint_for_every_covered_test`|(`part:spec:conformance`)|The current workspace's test profile is adopted end to end, every covered test derives exactly one mint without collision, and the source-workspace anti-vacuity threshold is replaced by an owner-ratified threshold for this workspace while authored prose remains the smaller registry.|
|`a_document_citing_a_live_test_resolves_and_a_dead_one_does_not`|(`part:spec:architecture`) and (`part:spec:conformance`)|The fixture selects a covered test from a current workspace package rather than a package absent from the workspace, uses that package's registered owner prefix for the cross-owner case, and proves live, dead, imported, and unwarranted-mint outcomes against the current census.|
|`the_repository_graph_report_is_sane`|all content parts, governed by (`part:spec:conformance`)|The completed parts and current code commentary form one resolution space with no dangling citation; current owner prefixes and manifest reach edges replace vendored ones; the graph retains cited and legitimately orphaned mints; and its requested hub list is populated and ranked.|
|`the_assembly_of_the_specification_is_live_and_fresh`|all eight parts and (`part:spec:conformance`)|The adopted assembly is retargeted to the accepted root parts directory and publication, its manifest lists every part exactly once in owner-approved order, the draft marker is absent, and the committed publication is the exact generated concatenation.|
|`the_repository_shape_report_is_sane`|all eight candidate benchmark parts and (`part:spec:conformance`)|The benchmark register names present current-workspace documents instead of absent source-corpus ADRs; every candidate is carried; together they contain a non-vacuous body of more than one hundred named environments; divisions remain separately measured; and the real outlier list is nonempty and ranked.|
|`the_repository_census_covers_every_test_function`|(`part:spec:conformance`)|The census ranges over all current members, classifies every discovered test into `unit`, `crate`, or `integration`, derives every label, and uses a current-workspace anti-vacuity floor instead of the source repository's four-thousand-test expectation. Any remaining parse exception is either removed or explicitly owned.|
|`the_repository_check_is_clean`|all parts, governed by (`part:spec:conformance`)|Every covered test carries its exact derived label; the prose, owner graph, edition register, burn registers, projections, and live specification assembly are current; the check has no finding; and its old four-thousand-label floor is replaced by the accepted current-corpus floor.|

No fixture-only test needs specification prose to pass. The campaign must keep those twenty-seven existing greens green while it discharges the eight rows; the table is a dependency map, not permission to weaken fixture contracts.

## Publication and benchmark shape · `sec:spec:publication`

**Proposal (Assembly and benchmarks)** · `proposal:spec:assembly-and-benchmarks`

The candidate paths and displayed layout record the original proposal; the live generic assembly has seven parts (`conv:assembly:assembly`), and the output contract is published at `~/.local/share/superloop-tools/docs/spec/output.md` (`[TOOLS-spec:outputspec:command-and-output-contracts]`).

Subject to the owner's answers below, the authored carrier should be the eight part files plus one manifest, while `docs/spec.md` is the committed generated, non-participating publication. The manifest declares order and exact membership; filename prefixes must not carry order implicitly. The eight part files are the initial benchmark candidates, while the manifest and generated publication are excluded from the band.

```text
docs/spec/assembly.md
docs/spec/architecture.md
docs/spec/dispatch.md
docs/spec/hooks.md
docs/spec/lanes.md
docs/spec/server.md
docs/spec/output.md
docs/spec/deployment.md
docs/spec/conformance.md
docs/spec.md
```

This arrangement reuses the linter's already-tested assembly lifecycle: dormant before the directory exists, draft while the marker stands, and live only when exact freshness binds. The present concept remains outside that assembly and is retired or retained as design history when the owner accepts the final publication.

## Open questions for the corpus owner · `sec:spec:owner-questions`

**Open Question (Canonical carrier)** · `open:spec:canonical-carrier`

Should the accepted assembly use the proposed root paths `docs/spec/` and `docs/spec.md`, making repository-wide ownership explicit, or another root location chosen before the linter's adopted assembly constants are retargeted?

**Open Question (Part boundaries)** · `open:spec:part-boundaries`

Are the eight proposed parts the right review-sized benchmark documents, or should dispatch and lane lifecycle, or architecture and server trust, be combined before prose is authored?

**Open Question (Benchmark admission)** · `open:spec:benchmark-admission`

Should every accepted part enter the benchmark band immediately, or should a smaller owner-approved subset establish the band after a first shape report and adversarial review?

**Open Question (Mutable facts)** · `open:spec:mutable-facts`

Which rapidly changing facts belong normatively in the specification: model rosters, measured budgets, server identities, and installed toolchain versions; and which should remain registry or runbook data constrained only by stable requirements?

**Open Question (Compatibility surface)** · `open:spec:compatibility-surface`

Must the Rust ports preserve every current state-file and run-directory byte shape, or may the specification define explicit migrations for selected formats while holding external streams, exit meanings, and final reports stable?

**Open Question (Anti-vacuity floors)** · `open:spec:anti-vacuity-floors`

Should the repository-facing corpus tests use fixed lower bounds calibrated to this workspace, or bounds derived from a committed census so growth remains measured without inheriting the vendored source repository's scale?

## Owner-review gate · `sec:spec:owner-review`

**Gate (Concept acceptance)** · `gate:spec:concept-acceptance`

The specification campaign remains blocked until the corpus owner accepts or amends the subject boundary, the part list, the label vocabulary, the assembly location, the benchmark policy, and each open question above. Once accepted, the first implementation step is an outline manifest that maps every future head to one part; only then should part prose, linter adoption data, corpus-test retargeting, assembly publication, and the final conformance gate proceed.
