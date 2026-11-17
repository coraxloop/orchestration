# Backlog of the generic repository · `plan:genericbacklog:orchestration-backlog`

Reading order and parent: (`guide:docnav:documentation`).

This backlog holds the open work that a change to this repository discharges: the specification, the rulebooks, the generic documents, the examples and the kind registry, with the Meson layer and the linter declarations that carry them. It holds open work only, and every item keeps the label it was minted with for life: the kind of the label says what the item is, and the first word of its first paragraph says where the item stands.

## Priorities · `sec:genericbacklog:priorities`

**Register (Priorities)** · `reg:genericbacklog:priorities`

The estate this backlog serves is becoming one where every producing worker runs in a box and a loop's exception is an in-harness subagent of its own session, where slice workers read one contributing guide per repository and work under the slice form this repository's specification states, where a root-held server is installed from this repository's guides and the estate's kit, where every document this repository carries is installed on a host and reachable from the rulebook, and where every loop and every worker corresponds through one plain mail system whose specification this repository carries. The whole backlog is one slice, in the order below: the rule for producing workers and their exception first, the generic half of the removal of non-boxed worker support that leads the tools and estate registers after the Claude boxed workers; the contributing guide next, because the slice form's general brief points at it; then the root-full platform baseline, the CoreOS example's reconciliation and the build's installer name, because a second root-full server must be installable from the documents; then the documentation install and the documentation-graph requirement; then the mail specification's follow-ups and the to-do profile's rule for authored backlog heads, on which the tools backlog's linter half waits; then the rest. A slice worker reads this register first and reports what it will work on. The holdings column follows the priorities-register definition (`def:dispatch:priorities-register`).

|order|slice|rows|items, in order|depends on, and rows larger than one lane|held by|
|-----|-----|----|---------------|-----------------------------------------|-------|
|1|The whole generic backlog|8|(`prob:build:generic-install-map-carries-the-mail-part`), (`prob:build:generic-documentation-installs-under-the-package-doc-root`), (`prob:build:generic-documents-install-natively`), (`prob:build:render-test-checks-survive-optimised-python`), (`open:docs:rulebook-render-headroom-budget-or-raised-bound`), (`prob:docs:the-timing-evidence-rule-takes-the-controlled-clock-reading`), (`prob:docs:a-landing-that-changes-a-rule-of-the-specification-carries-its-changelog-line`), (`prob:dispatch:a-bar-on-a-tree-with-held-switches-is-run-again-on-the-landed-tree`)|Reading: the slice work section (`sec:dispatch:slice-work`) for the exception rule and the contributing guide, the notes register of the estate's first root-full deploy, read as a whole, for the platform rows, and the estate's documentation-install decision for the install rows, which also settles the native install's map question. Bar: at each tip the generic gate on the root-full node, with the lint in public-pack mode over the burn input, the projection, the formatter and the Meson layer. The tools backlog's ``prob:linter:authored-todo-head-in-backlog-documents`` waits on the to-do profile's rule; the roadmap's topic hints use the headroom under the render bound, so the bound is settled first. No row is larger than one lane.|lane r002g83, its two documentation install items, (`prob:build:generic-documentation-installs-under-the-package-doc-root`) and (`prob:build:generic-documents-install-natively`), wait on the estate gate's native-install predicate (``prob:gates:generic-gate-accepts-a-native-documentation-install`` in its backlog) and on the tools' index writer and provenance contract, held by lane r002g79 (``prob:build:installer-tree-targets-and-index-writer`` in the tools backlog); unheld: (`prob:build:generic-install-map-carries-the-mail-part`), (`prob:build:render-test-checks-survive-optimised-python`), (`open:docs:rulebook-render-headroom-budget-or-raised-bound`), (`prob:dispatch:a-bar-on-a-tree-with-held-switches-is-run-again-on-the-landed-tree`), (`prob:docs:the-timing-evidence-rule-takes-the-controlled-clock-reading`) and (`prob:docs:a-landing-that-changes-a-rule-of-the-specification-carries-its-changelog-line`)|

## Charter · `sec:genericbacklog:charter`

**Convention (Status grammar)** · `conv:genericbacklog:status-grammar`

Every item opens with one of three statuses in bold, followed by the evidence for it, so a reader can triage by the first word and grep it: **OPEN** for work not started or whose remainder is unscheduled, with whatever part landed stated; **ACTIVE** for work a lane carries now; and **PARKED** for a deliberate deferral carrying its reason and revisit condition. A status changes when its evidence does, and the evidence that changed it is stated in the same paragraph; the earlier status and its text stay beneath. These are the open statuses of the estate backlog's grammar, ``conv:backlog:status-grammar``, whose closed statuses, DONE, CLOSED and SUPERSEDED, are the words of the estate's record documents; this repository does not import the estate's corpus, so the grammar is stated here rather than cited.

**Convention (Item kinds)** · `conv:genericbacklog:item-kinds`

An item's kind says what it is, and its status where it stands. A Problem (`prob`) is work assigned: a defect or a change, with its remedy where one is known; a Claim (`claim`) is a finding stated to be verified before it is relied on; an Open Problem or Open Question (`open`) is a design question whose answer is not yet known; a Question (`q`) asks a plain question of a named party; a Goal (`goal`) is a desideratum or a direction without one bounded piece of work; a Decision (`dec`) is a decided rule or form whose adoption or statement is still open; and a Record (`rec`) keeps a measurement or a piece of evidence until its revisit condition decides it. Existing work items retain their Problem identities permanently. The authored backlog profile (`conv:todos:authored-backlog`) admits new To-do heads on explicitly declared surfaces once the tools linter implements that admission; until then new work uses the supported Problem form. Profile adoption never renames an existing `prob` label.

**Convention (Intake and exit)** · `conv:genericbacklog:intake-and-exit`

New items come from letters to the loop and from review findings, sorted at intake into the backlog of the repository whose change discharges them; an item that a change to the tools repository discharges belongs to its backlog, ``plan:toolsbacklog:superloop-tools-backlog``, and one that an estate's operations discharge to that estate's backlog. An item that is met leaves this backlog: the loop's record of the landing names the commit that met it, and what the item established is folded into this repository's documentation rather than kept here as a closed entry. An item whose evidence names private details of an estate keeps those paragraphs in that estate's backlog and names the record that holds them.

**Convention (Working the backlog)** · `conv:genericbacklog:working-the-backlog`

Every worker of every loop receives clones of the bare repositories it needs in its workspace and makes its own checkouts; the loop pushes into and fetches from those bares, and a superloop keeps its own bares of record with mirror bares on the compute server, so that a hand-over is a repository rather than a prepared checkout and a clone on the node is a delta (`rule:dispatch:workers-clone-from-bare-repositories`).

This backlog is worked in slices (`sec:dispatch:slice-work`): the loop sets the priorities and submits rows to the backlog manager by letter; a slice worker, briefed with the workspace, the repository's contributing guide and a budget, reads the backlog with its priorities register, proposes a slice of twenty to thirty rows, or the whole backlog where it holds fewer, and stops; the loop answers that proposal and steers by letter afterwards, never before it. A slice worker never rebases, squashes, amends or force-pushes what it has pushed (`rule:dispatch:lane-branch-merge-in`): when the base branch moves it merges the base in, and a correction after a review is a fixup commit on top, so that a review in flight keeps its anchors and the worker keeps its own trail. The loop stages the lane branch on a review branch, `review/<topic>`, which the worker never touches (`proto:dispatch:review-branch-landing`): basic rebasing of the staged work is the loop's, advanced rebasing is the reviewer's, done on the review branch with its trivial fixups named in the review, and a correction beyond trivial returns to the worker as a fixup under the merge-in rule. The loop alone makes the commits of record, remade onto the development branch with its own identity and messages, gates them, and pushes the base back into the workspace bares.

Holdings follow the priorities-register definition (`def:dispatch:priorities-register`); selection among unheld items follows the slice protocol (`proto:dispatch:slice-dispatch`).

**Register (Areas)** · `reg:genericbacklog:areas`

An item's area is the subject of what must change to discharge it, and the sections of the open work follow the areas in this order; an item keeps the area and slug of its label for life, so an area shared with the other backlogs names the same subject there.

|area|subject|
|----|-------|
|`mail`|the mail specification's follow-ups: its constants, refusal codes and the questions its implementation lanes raise|
|`estate`|the division of documents between this repository and the others|
|`build`|this repository's Meson layer|
|`linter`|this repository's linter declarations and the values they name|
|`docs`|the specification, the rulebooks and the generic documents where the fix is prose|
|`dispatch`|the specification's dispatch and lanes parts: how a superloop gives its workers their repositories|
|`servers`|the root-full server guides and the CoreOS worked example: the platform baseline, the account model, the verification checklist and the recovery|

## Open work · `sec:genericbacklog:open-work`

### The mail specification · `sec:genericbacklog:open-mail`

### The division of documents · `sec:genericbacklog:open-estate`

### The Meson layer · `sec:genericbacklog:open-build`

**Problem (The generic repository installs its documents by Meson's native rules and retires its install map)** · `prob:build:generic-documents-install-natively`

**OPEN.** (2026-11-03) This repository's part of the tools' native install, ``prob:build:native-meson-install`` in the tools backlog: bite 5, the generic repository a documents-only install by Meson's own rules, and its half of bite 8, its install map's removal. Measured at development e8b83958: the layer is documents-only, but its install still runs the tools' install primitive over the generic install map as an install script, so the documents install by map rather than by Meson's native rules.

**Problem (The generic repository installs its documentation under the package documentation root)** · `prob:build:generic-documentation-installs-under-the-package-doc-root`

**OPEN.** (2026-11-05, a slice of the documentation-install set, whose lead is the estate's decision that each repository installs its complete documentation set as a package does) The install map ``maps/generic-map.toml`` gains one `tree` target from the repository root to ``~/.local/share/doc/orchestration/``, including ``README.md``, ``CHANGELOG.md``, ``ORCHESTRATION.md``, ``CLAUDE.md``, ``adr/**`` and ``docs/**`` (the specification, the CoreOS guides, the proposals, the reference, the examples, the decisions and the guides); the program-read copies stay as `copy` targets under ``~/.local/share/orchestration/`` (the specification, the rulebook shape, ``CLAUDE.md``, ``labels.toml`` and the examples), and the human-read specification parts and ADRs under that root are removed with no compatibility copy. The document route re-renders, and its provenance records the removal.

Measured on 2026-11-05 at main d574ea8: the map copies the specification parts, one ADR, the commit-signing document, the two rulebooks and the fictional examples and nothing else, so the CoreOS guides (eight, 68 KB), the root-full server setup (36 KB), the confined-administration guide, the security posture, the decisions, the harness user channels, the reference and the proposals are declared in ``docs/meson.build`` with no copy target and absent from the host, where a session asked about the server design walks past them; a host script publishes them under the documentation root as a hotfix until this lands. The rulebook's reading roadmap (`preview:orch:which-part-to-read`) points at the documentation root and its package indexes in the same change, and the instance register's line naming the server guides is the estate's half.

This form meets the native install (`prob:build:generic-documents-install-natively`) head-on: that item retires the install map, while this one makes the map the documentation's declaration, so the estate's decision settles which form carries the documentation and the other item follows it.

**Problem (The generic install carries the mail part to the host's specification root)** · `prob:build:generic-install-map-carries-the-mail-part`

**OPEN.** (2026-11-06, from the review of lane r002g83's mail-part rows) The base install map, ``maps/generic-map.toml``, has no target for ``docs/spec/mail.md``, so the host's specification root carries no mail part while the rulebook's reading roadmap (`preview:orch:which-part-to-read`) lists mail among the parts (`spec:mail:superloop-mail-system`); the hotfix publication under the documentation root is complete, and the map is not. The map gains the part's target, or the native install that retires the map installs it from the generated inventory, so that every part the roadmap names is installed where the roadmap points.

(2026-11-11, read on a host while checking where a newly landed dispatch rule is installed) The map still has no target for ``docs/spec/mail.md``, so the installed specification under the share root has no mail part beside it while the rendered rulebook's roadmap names it among the parts beside the specification, and the complete documentation root has it. The copy targets also follow the `main` branch, last refreshed on 2026-11-03, so a rule landed on `development`, such as (`rule:dispatch:letters-carry-communication`), reaches the installed specification only at the next release and the documentation root at the next documentation publish. The map gains the mail part, and the rulebook's pointer names whichever root is current.

**Problem (The render test's checks survive optimised Python)** · `prob:build:render-test-checks-survive-optimised-python`

**OPEN.** (2026-11-06, from the review of lane r002g83's render rows) The render test, ``tests/test_rulebook_render.py``, relies on bare `assert` statements, so under `PYTHONOPTIMIZE` it runs no check at all and passes; its checks raise an explicit failure or run under a test runner that keeps them, so that the render's size gate holds in every interpreter mode.

### Linter declarations · `sec:genericbacklog:open-linter`

### Documents · `sec:genericbacklog:open-docs`

**Open Question (Whether the rulebook render keeps a measured headroom budget or the hook's bound rises)** · `open:docs:rulebook-render-headroom-budget-or-raised-bound`

**OPEN.** (2026-11-06, measured by the render test and by lane r002g83) The rendered instance stands at 9,465 of the hook's 9,500 bytes (`rule:hooks:rulebook-size-bound`) after the roadmap's topic hints and again after the mail operating form: 35 bytes of headroom, less than one overlay sentence, so the next sentence of either shape breaks the render. Two forms answer it, and the choice is the rulebook's owner's: a measured budget, in which the render test fails below a declared minimum headroom such as 100 bytes while the hook keeps 9,500, so that a change approaching the bound is red before it lands; or a raised hook bound with a measured reason, the render's cost in the session's context against what the added bytes carry.

**Problem (The timing evidence rule takes the controlled-clock reading)** · `prob:docs:the-timing-evidence-rule-takes-the-controlled-clock-reading`

**OPEN.** (2026-11-17, from the testing-policy design note, fb019819, its part G3) The timing evidence rule says that a time bound that is part of the contract is scaled by measurements from the gate's node (`rule:conformance:ordering-and-timing-evidence`), which conflicts with the newer server rule that no verdict rests on wall time (`rule:server:verdicts-do-not-rest-on-wall-time`). The note's part G3 replaces only the rule's body: a contract about time is exercised through a controlled clock at the production boundary; measurements on a shared instance are reported with their load and do not become a general gate's wall-time verdict; an untouched source file alone does not prove that a failure is unrelated to a change; and failure disposition follows the product's adopted gate, test repair beyond the accepted change belonging to separately scoped backlog work (`prin:environment:testing-serves-the-product`). It is no reason to abolish deadline contracts: a product that needs real-time acceptance changes the server rule explicitly for its scope and names the measurement's conditions.

**Problem (A landing that changes a rule of the specification carries its changelog line)** · `prob:docs:a-landing-that-changes-a-rule-of-the-specification-carries-its-changelog-line`

**OPEN.** (2026-11-16, found at a release) Four landings changed rules of the specification, the server part twice, the mail part and the dispatch part, each with a compatibility line in its commit and no changelog entry, and nothing refused them; the entries were written at the release from the commit bodies. A reader of the release notes is told what changed only if the entry exists, so the design question is who tells that reader: the linter knows which labels a commit mints or amends and could ask for a changelog line citing each, or the landing form could ask for it.

### Dispatch and lanes · `sec:genericbacklog:open-dispatch`

**Problem (A worker's bar on a tree that carries held switches runs again on the landed tree before the next review stacks)** · `prob:dispatch:a-bar-on-a-tree-with-held-switches-is-run-again-on-the-landed-tree`

**OPEN.** (2026-11-08, from a gate after a review landing) A worker whose branch carried held switches, which the landing leaves out, passed its bar on that branch, while three of the tests it touched went red at the first gate of the landed tree, which the review's caveat had named as that tree's first run. A branch with held switches tests a tree other than the landing, so the review's caveat that the gate is the landed tree's first run is the signal to gate that tree before the next review stacks on it, or the worker reruns its bar on the landed tree before claiming it; the gate at the landed tip (`proto:dispatch:review-branch-landing`) is then a confirmation rather than the first measurement.

### The root-full servers · `sec:genericbacklog:open-servers`
