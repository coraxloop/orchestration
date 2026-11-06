# Backlog of the generic repository · `plan:genericbacklog:orchestration-backlog`

Reading order and parent: (`guide:docnav:documentation`).

This backlog holds the open work that a change to this repository discharges: the specification, the rulebooks, the generic documents, the examples and the kind registry, with the Meson layer and the linter declarations that carry them. It holds open work only, and every item keeps the label it was minted with for life: the kind of the label says what the item is, and the first word of its first paragraph says where the item stands.

## Priorities · `sec:genericbacklog:priorities`

**Register (Priorities)** · `reg:genericbacklog:priorities`

The estate this backlog serves is becoming one where every producing worker runs in a box and a loop's exception is an in-harness subagent of its own session, where slice workers read one contributing guide per repository and work under the slice form this repository's specification states, where a root-held server is installed from this repository's guides and the estate's kit, where every document this repository carries is installed on a host and reachable from the rulebook, and where every loop and every worker corresponds through one plain mail system whose specification this repository carries. The whole backlog is one slice, in the order below: the rule for producing workers and their exception first, the generic half of the removal of non-boxed worker support that leads the tools and estate registers after the Claude boxed workers; the contributing guide next, because the slice form's general brief points at it; then the root-full platform baseline, the CoreOS example's reconciliation and the build's installer name, because a second root-full server must be installable from the documents; then the documentation install and the documentation-graph requirement; then the mail specification's follow-ups and the to-do profile's rule for authored backlog heads, on which the tools backlog's linter half waits; then the rest. A slice worker reads this register first and reports what it will work on. The holdings column follows the priorities-register definition (`def:dispatch:priorities-register`).

|order|slice|rows|items, in order|depends on, and rows larger than one lane|held by|
|-----|-----|----|---------------|-----------------------------------------|-------|
|1|The whole generic backlog|4|(`prob:build:generic-documentation-installs-under-the-package-doc-root`), (`prob:build:generic-documents-install-natively`), (`prob:build:burn-input-optional-for-the-public-tree`), (`prob:build:configure-says-which-lint-mode-it-selected`)|Reading: the slice work section (`sec:dispatch:slice-work`) for the exception rule and the contributing guide, the notes register of the estate's first root-full deploy, read as a whole, for the platform rows, and the estate's documentation-install decision for the install rows, which also settles the native install's map question. Bar: at each tip the generic gate on the root-full node, with the lint in public-pack mode over the burn input, the projection, the formatter and the Meson layer. The tools backlog's ``prob:linter:authored-todo-head-in-backlog-documents`` waits on the to-do profile's rule; the roadmap's topic hints use the headroom under the render bound, so the bound is settled first. No row is larger than one lane.|lane r002g83, the whole row|

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

**Problem (The generic Meson layer configures without the burn input, so a public consumer can run it)** · `prob:build:burn-input-optional-for-the-public-tree`

**OPEN.** (r002g41 review 1 N4; taken into r002g41 fix round 2 as c09) the generic meson.build refused to configure without `-Dburn_input`, so a public consumer could not run the documents-only Meson layer; the option becomes optional with ordinary-mode lint targets without it. N5 (optional): the root README's install guidance, without estate paths, into a public document later.

**Problem (The generic configure step says which lint mode it selected)** · `prob:build:configure-says-which-lint-mode-it-selected`

**OPEN.** (r002g41 review 2 N1) since c09 (generic 8c121992) a `meson setup` without `-Dburn_input` silently selects ordinary lint mode, shown only as `"public_pack":false` in the report; the estate gate always passes the input, but a hand-run configure could get the weaker check unnoticed. Add a configure-time `message()` (or `warning()`) naming the selected mode when the input is empty.

**Problem (The generic repository installs its documents by Meson's native rules and retires its install map)** · `prob:build:generic-documents-install-natively`

**OPEN.** (2026-11-03) This repository's part of the tools' native install, ``prob:build:native-meson-install`` in the tools backlog: bite 5, the generic repository a documents-only install by Meson's own rules, and its half of bite 8, its install map's removal. Measured at development e8b83958: the layer is documents-only, but its install still runs the tools' install primitive over the generic install map as an install script, so the documents install by map rather than by Meson's native rules.

**Problem (The generic repository installs its documentation under the package documentation root)** · `prob:build:generic-documentation-installs-under-the-package-doc-root`

**OPEN.** (2026-11-05, a slice of the documentation-install set, whose lead is the estate's decision that each repository installs its complete documentation set as a package does) The install map ``maps/generic-map.toml`` gains one `tree` target from the repository root to ``~/.local/share/doc/orchestration/``, including ``README.md``, ``CHANGELOG.md``, ``ORCHESTRATION.md``, ``CLAUDE.md``, ``adr/**`` and ``docs/**`` (the specification, the CoreOS guides, the proposals, the reference, the examples, the decisions and the guides); the program-read copies stay as `copy` targets under ``~/.local/share/orchestration/`` (the specification, the rulebook shape, ``CLAUDE.md``, ``labels.toml`` and the examples), and the human-read specification parts and ADRs under that root are removed with no compatibility copy. The document route re-renders, and its provenance records the removal.

Measured on 2026-11-05 at main d574ea8: the map copies the specification parts, one ADR, the commit-signing document, the two rulebooks and the fictional examples and nothing else, so the CoreOS guides (eight, 68 KB), the root-full server setup (36 KB), the confined-administration guide, the security posture, the decisions, the harness user channels, the reference and the proposals are declared in ``docs/meson.build`` with no copy target and absent from the host, where a session asked about the server design walks past them; a host script publishes them under the documentation root as a hotfix until this lands. The rulebook's reading roadmap (`preview:orch:which-part-to-read`) points at the documentation root and its package indexes in the same change, and the instance register's line naming the server guides is the estate's half.

This form meets the native install (`prob:build:generic-documents-install-natively`) head-on: that item retires the install map, while this one makes the map the documentation's declaration, so the estate's decision settles which form carries the documentation and the other item follows it.

### Linter declarations · `sec:genericbacklog:open-linter`

### Documents · `sec:genericbacklog:open-docs`

### Dispatch and lanes · `sec:genericbacklog:open-dispatch`

### The root-full servers · `sec:genericbacklog:open-servers`
