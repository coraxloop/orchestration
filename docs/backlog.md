# Backlog of the generic repository · `plan:genericbacklog:orchestration-backlog`

This backlog holds the open work that a change to this repository discharges: the specification, the rulebooks, the generic documents, the examples and the kind registry, with the Meson layer and the linter declarations that carry them. It holds open work only, and every item keeps the label it was minted with for life: the kind of the label says what the item is, and the first word of its first paragraph says where the item stands.

## Charter · `sec:genericbacklog:charter`

**Convention (Status grammar)** · `conv:genericbacklog:status-grammar`

Every item opens with one of three statuses in bold, followed by the evidence for it, so a reader can triage by the first word and grep it: **OPEN** for work not started or whose remainder is unscheduled, with whatever part landed stated; **ACTIVE** for work a lane carries now; and **PARKED** for a deliberate deferral carrying its reason and revisit condition. A status changes when its evidence does, and the evidence that changed it is stated in the same paragraph; the earlier status and its text stay beneath. These are the open statuses of the estate backlog's grammar, ``conv:backlog:status-grammar``, whose closed statuses, DONE, CLOSED and SUPERSEDED, are the words of the estate's record documents; this repository does not import the estate's corpus, so the grammar is stated here rather than cited.

**Convention (Item kinds)** · `conv:genericbacklog:item-kinds`

An item's kind says what it is, and its status where it stands. A Problem (`prob`) is work assigned: a defect or a change, with its remedy where one is known; a Claim (`claim`) is a finding stated to be verified before it is relied on; an Open Problem or Open Question (`open`) is a design question whose answer is not yet known; a Question (`q`) asks a plain question of a named party; a Goal (`goal`) is a desideratum or a direction without one bounded piece of work; a Decision (`dec`) is a decided rule or form whose adoption or statement is still open; and a Record (`rec`) keeps a measurement or a piece of evidence until its revisit condition decides it. Work items carry Problem rather than To-do because the kind registry reserves `todo` for the machine-derived deficiency notices of the to-do profile (`sig:todos:kind-extension`), so no authored head may mint it.

**Convention (Intake and exit)** · `conv:genericbacklog:intake-and-exit`

New items come from letters to the loop and from review findings, sorted at intake into the backlog of the repository whose change discharges them; an item that a change to the tools repository discharges belongs to its backlog, ``plan:toolsbacklog:superloop-tools-backlog``, and one that an estate's operations discharge to that estate's backlog. An item that is met leaves this backlog: the loop's record of the landing names the commit that met it, and what the item established is folded into this repository's documentation rather than kept here as a closed entry. An item whose evidence names private details of an estate keeps those paragraphs in that estate's backlog and names the record that holds them.

**Register (Areas)** · `reg:genericbacklog:areas`

An item's area is the subject of what must change to discharge it, and the sections of the open work follow the areas in this order; an item keeps the area and slug of its label for life, so an area shared with the other backlogs names the same subject there.

|area|subject|
|----|-------|
|`estate`|the division of documents between this repository and the others|
|`build`|this repository's Meson layer|
|`linter`|this repository's linter declarations and the values they name|
|`docs`|the specification, the rulebooks and the generic documents where the fix is prose|
|`dispatch`|the specification's dispatch and lanes parts: how a superloop gives its workers their repositories|

## Open work · `sec:genericbacklog:open-work`

### The division of documents · `sec:genericbacklog:open-estate`

**Problem (Architecture documents about how the tools are built stay generic while their records moved)** · `prob:estate:arch-documents-subject-survey`

**OPEN.** As recorded, and not yet checked against the tree, the generic architecture documents about how tools are built, installed and run stay in the generic repository while the records deciding them moved to the tools repository; what remains is a survey under the same subject test as the records' move, deciding whether those documents follow.

generic `docs/arch/*` subject test (f07 round one, finding 5): the architecture documents whose subject is how tools are built, installed and run (lane-box-build, capability-door, key-custody, distribution-readiness, estate-layout) stay in the generic repository while the records deciding them moved to the tools repository (record 028 cites 66 generic labels, mostly there; lane-box-build cites record 033 thirty-six times through the import); a survey under the same subject test as the records move decides whether they follow

### The Meson layer · `sec:genericbacklog:open-build`

**Problem (The generic document layer's labels build record predates the deployed build-sync ledger contract)** · `prob:build:generic-layer-program-identity-under-ledger-contract`

**OPEN.** Measured on 2026-10-29 at 08:35Z: the generic repository's `meson.build`, since 8de937f (the documents-only layer), declares a `labels-record` custom target that calls `build-sync --record labels.toml --producer <linter> --domain server`, while the build-sync deployed to the node tools directory since the dependency-ledger inventories (tools 8e57926, ``entry:build:dependency-bite-version-line-and-ledger``) requires `--ledger`, `--source-root`, `--source-repository` and `--source-commit` and resolves the output's identity from exactly one ledger `program` row whose package, version and release group are checked against the source `meson.build`, which a documents-only layer does not declare. The generic gate on lane r002g03's candidate 44f2f4d7 went red at ninja step 6/7 with `missing_required_argument`, as the base f6052e07 would; the last green generic gate (r002f33, 2026-10-23, base b169374e) ran against the earlier build-sync, and the deploy note of the bite 6 commit (tools 14d6c41) names the document layers' `meson.build` lookups and their report and stamp arguments as a pending change that the layers never received. The unblocking change is r002g03's second commit, which drops the record target and keeps the export. What remains: the generic layer declares its program identity under the ledger contract, so that the label export carries a build record again, and its lookups move to the deployed names (`superloop-lint`, `superloop-pack`, `superloop-install`, and build-sync by its private directory option) in the same change; the instance layer's `meson.build` is checked for the same debt.

Measured on 2026-10-29 at 09:02Z, after generic main moved to 5743fe9a: the host's `~/.local/share/orchestration/labels.toml`, installed on 2026-10-23 by the build target of that time, has no map target any more and stays as a leftover until the record returns or the publisher removes the files the map no longer names; nothing reads it.

**Problem (The generic Meson layer configures without the burn input, so a public consumer can run it)** · `prob:build:burn-input-optional-for-the-public-tree`

**OPEN.** (r002g41 review 1 N4; taken into r002g41 fix round 2 as c09) the generic meson.build refused to configure without `-Dburn_input`, so a public consumer could not run the documents-only Meson layer; the option becomes optional with ordinary-mode lint targets without it. N5 (optional): the root README's install guidance, without estate paths, into a public document later.

**Problem (The generic configure step says which lint mode it selected)** · `prob:build:configure-says-which-lint-mode-it-selected`

**OPEN.** (r002g41 review 2 N1) since c09 (generic 8c121992) a `meson setup` without `-Dburn_input` silently selects ordinary lint mode, shown only as `"public_pack":false` in the report; the estate gate always passes the input, but a hand-run configure could get the weaker check unnoticed. Add a configure-time `message()` (or `warning()`) naming the selected mode when the input is empty.

### Linter declarations · `sec:genericbacklog:open-linter`

**Problem (The generic repository's public-pack policy names a values file that left it, so a bare linter check in its loop clone refuses)** · `prob:linter:generic-linter-burn-values`

**OPEN.** **OPEN 2026-10-03, found when a two-line rulebook fix was linted in the loop clone; the gates and the commit scripts compensate, the policy row is owed a home.** When the private partition left the generic repository (`80d45edc`), the burn-values document `local/linter/public-pack-burn.toml` went with it, but `.linter/policy-public-pack-values.toml` still names that path, so `orchestration-linter check --root .` in the loop clone refuses with `the burn-value document is absent` before checking anything. The gate form already substitutes the instance repository's `linter/public-pack-burn.toml` through `--public-pack --burn-input`, and the loop-clone commit scripts now lint the same way. The policy should name where the values live now, or declare the input as supplied by the caller, so that a bare check in any clone of the generic repository is clean or refuses for a reason of its own.

### Documents · `sec:genericbacklog:open-docs`

**Problem (the orchestrator rulebook render sits just under the hook's size bound)** · `prob:docs:rulebook-render-size-bound`

**OPEN.** The render sat 30 bytes under its 9,500-byte bound when this was recorded and has not been checked against the tree since; what remains is moving the generic register's long path register into the pointer form or raising the bound with a measured reason, and a generic gate that renders the instance shape so a breaking change is red before import.

the orchestrator rulebook render sits 30 bytes under its 9,500-byte bound (2026-10-21T23:05:09Z): the generic shape ORCHESTRATION.md grew 148 bytes at 870be3c2 (its line 53 names the tools publication homes) and rulebook-install refused the instance render (reason rendered_size) until the instance register lines were trimmed four times (rabe rulebooks/orchestration.md 4,464 to 4,356 bytes; render 9,470). The bound is the hook's (rule:hooks:rulebook-size-bound); the next sentence added to either shape breaks the render again. Proper fix: the generic rulebook's register moves its long path register into the pointer form (the layout of record names the folders), or the bound rises with a measured reason; and the generic gate renders the instance shape so a generic change that breaks the render is red before import.

**Problem (the dispatch rule on refused timestamps does not name the zero-offset form)** · `prob:docs:dispatch-rule-refuses-zero-offset-timestamps`

**OPEN.** The dispatch rule at `docs/spec/dispatch.md:232` still does not name the zero-offset form (`+00:00`) that the hooks fixture sentence pins since lane r002f37; what remains is one line naming zero-offset beside naive, local and nonzero-offset, committed with its regeneration, together with the stray space of "malformed- delay" at hooks.md:380.

`docs/spec/dispatch.md:232` (publication `docs/spec.md:526`) says "Naive, local and nonzero-offset civil timestamps are refused by name rather than assigned a zone" and does not name a zero-offset stamp without a Z (`+00:00`), the boundary the hooks fixture sentence now pins (lane r002f37); its earlier clause "only explicit UTC instants or declared epochs are parsed" may exclude it depending on how "explicit UTC" is read (review of r002f37, 2026-10-23). Fix: the dispatch rule names zero-offset beside naive, local and nonzero-offset, so the two parts agree; one line, one commit with its regeneration. Where: generic docs/spec/dispatch.md; with items ``entry:dispatch:utc-instants-everywhere`` and ``entry:docs:hooks-fixture-pins-zero-offset-timestamp``. Also: the token "malformed- delay" at hooks.md:380 (publication :1018) carries a stray space (`hooks.md:257` spells it `malformed-delay`); fix in the same step.

**Problem (The rulebook roadmap names what each specification part covers)** · `prob:docs:rulebook-roadmap-names-each-spec-part`

**OPEN.** GENERIC rulebook roadmap (r002g72 F1, 2026-11-02): the roadmap no longer lists what each spec part covers; four part labels (spec:dispatch:dispatch-and-supervision, spec:hooks:hook-state-machines, spec:lanes:worker-lane-lifecycle, spec:architecture:architecture-and-authority) are now cited nowhere in the generic tree (no uncited-mint linter check). ~500 B of headroom under the 9,500 B render bound could carry short topic hints back.

### Dispatch and lanes · `sec:genericbacklog:open-dispatch`

**Decision (Workers receive clones of the bare repositories they need and make their own checkouts)** · `dec:dispatch:workers-clone-from-bare-repositories`

**OPEN.** (2026-11-03) Workers of any loop get clones of the bare repositories they need in their workspace and make their own checkouts; the loop pushes into and fetches from those bares; superloops keep their own bares of record and mirror bares on the compute server for fast differential clones. To state in the generic specification (dispatch/lanes part), where the lane forms of each superloop then re-state their provisioning on bares.
