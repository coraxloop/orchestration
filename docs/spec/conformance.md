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
