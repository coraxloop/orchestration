# Backlog of the generic repository · `plan:genericbacklog:orchestration-backlog`

This backlog holds the open work that a change to this repository discharges: the specification, the rulebooks, the generic documents, the examples and the kind registry, with the Meson layer and the linter declarations that carry them. It holds open work only, and every item keeps the label it was minted with for life: the kind of the label says what the item is, and the first word of its first paragraph says where the item stands.

## Priorities · `sec:genericbacklog:priorities`

**Register (Priorities)** · `reg:genericbacklog:priorities`

The estate this backlog serves is becoming one where every loop and every worker corresponds through one plain mail system, whose specification this repository carries, where workers are handed bare repositories and make their own checkouts, a rule the dispatch part of the specification is to state, and where the documents say what holds while the backlogs say what is still to do. The whole backlog is one slice, in the order below: the mail specification's follow-ups first as rows for them arrive, then the bare-repository rule, then the to-do profile's rule for authored backlog heads, on which the tools backlog's linter half waits, then the rest. A slice worker reads this register first and reports what it will work on.

|order|slice|rows|items, in order|depends on, and rows larger than one lane|
|-----|-----|----|---------------|-----------------------------------------|
|1|The whole generic backlog|11|(`open:mail:per-record-maximum-and-unavailable-endpoint-code`), (`open:mail:worker-uid-lifetime-stated`), (`dec:dispatch:workers-clone-from-bare-repositories`), (`prob:docs:todo-profile-admits-authored-backlog-heads`), (`prob:docs:rulebook-render-size-bound`), (`prob:docs:rulebook-roadmap-names-each-spec-part`), (`prob:docs:dispatch-rule-refuses-zero-offset-timestamps`), (`prob:build:generic-layer-program-identity-under-ledger-contract`), (`prob:build:burn-input-optional-for-the-public-tree`), (`prob:build:configure-says-which-lint-mode-it-selected`), (`prob:build:generic-documents-install-natively`)|The tools backlog's ``prob:linter:authored-todo-head-in-backlog-documents`` waits on the to-do profile's rule; the roadmap's topic hints use the headroom under the render bound, so the bound is settled first. No row is larger than one lane.|

## Charter · `sec:genericbacklog:charter`

**Convention (Status grammar)** · `conv:genericbacklog:status-grammar`

Every item opens with one of three statuses in bold, followed by the evidence for it, so a reader can triage by the first word and grep it: **OPEN** for work not started or whose remainder is unscheduled, with whatever part landed stated; **ACTIVE** for work a lane carries now; and **PARKED** for a deliberate deferral carrying its reason and revisit condition. A status changes when its evidence does, and the evidence that changed it is stated in the same paragraph; the earlier status and its text stay beneath. These are the open statuses of the estate backlog's grammar, ``conv:backlog:status-grammar``, whose closed statuses, DONE, CLOSED and SUPERSEDED, are the words of the estate's record documents; this repository does not import the estate's corpus, so the grammar is stated here rather than cited.

**Convention (Item kinds)** · `conv:genericbacklog:item-kinds`

An item's kind says what it is, and its status where it stands. A Problem (`prob`) is work assigned: a defect or a change, with its remedy where one is known; a Claim (`claim`) is a finding stated to be verified before it is relied on; an Open Problem or Open Question (`open`) is a design question whose answer is not yet known; a Question (`q`) asks a plain question of a named party; a Goal (`goal`) is a desideratum or a direction without one bounded piece of work; a Decision (`dec`) is a decided rule or form whose adoption or statement is still open; and a Record (`rec`) keeps a measurement or a piece of evidence until its revisit condition decides it. Work items carry Problem rather than To-do because the kind registry reserves `todo` for the machine-derived deficiency notices of the to-do profile (`sig:todos:kind-extension`), so no authored head may mint it.

**Convention (Intake and exit)** · `conv:genericbacklog:intake-and-exit`

New items come from letters to the loop and from review findings, sorted at intake into the backlog of the repository whose change discharges them; an item that a change to the tools repository discharges belongs to its backlog, ``plan:toolsbacklog:superloop-tools-backlog``, and one that an estate's operations discharge to that estate's backlog. An item that is met leaves this backlog: the loop's record of the landing names the commit that met it, and what the item established is folded into this repository's documentation rather than kept here as a closed entry. An item whose evidence names private details of an estate keeps those paragraphs in that estate's backlog and names the record that holds them.

**Convention (Working the backlog)** · `conv:genericbacklog:working-the-backlog`

Every worker of every loop receives clones of the bare repositories it needs in its workspace and makes its own checkouts; the loop pushes into and fetches from those bares, and a superloop keeps its own bares of record with mirror bares on the compute server, so that a hand-over is a repository rather than a prepared checkout and a clone on the node is a delta.

This backlog is worked in slices: the loop sets the priorities and submits rows to the backlog manager by letter; a slice worker reads the backlog with its priorities register, takes a large slice of thirty rows or more and reports what it will work on; the loop steers it by mail, cherry-picks its commits into review branches for review workers, and alone makes the commits of record, squashed and remade with its own messages after an importable review.

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

## Open work · `sec:genericbacklog:open-work`

### The mail specification · `sec:genericbacklog:open-mail`

**Open Question (Whether the mail specification declares its per-record maximum, and which refusal code names an unavailable endpoint)** · `open:mail:per-record-maximum-and-unavailable-endpoint-code`

**OPEN.** (2026-11-03 09:05Z, from the review of lane r002g76's c02, F5) The specification declares the journal and staging bounds as constants but not the per-record maximum, which the implementation sets at 65,536 bytes to size the reserved scratch: the specification declares it, or states that it is an implementation constant.

(from the review of lane r002g76's c01, F3) The refusal-code list has no code for an unavailable endpoint, with unsafe-storage and io-failure as the candidates; the delivery core reports the gap until the specification names one. Both parts are answered in the mail specification (`spec:mail:superloop-mail-system`), the first beside its retention constants (`def:mail:retention-constants`), the second in its visible-refusal rule (`rule:mail:refusal`).

**Open Question (Whether the mail specification states a worker uid's lifetime)** · `open:mail:worker-uid-lifetime-stated`

**OPEN.** (2026-11-03 15:55Z, from lane r002g76's c06 review K1) Worker uids are recycled at retirement after custody transfer, while the specification states only that worker birth names are never reused (`rule:mail:worker-birth-name`); whether it states the uid's lifetime explicitly is open, and the tools' retirement operation lands meanwhile (``prob:mail:worker-run-retirement-recycles-the-uid`` in the tools backlog).

### The division of documents · `sec:genericbacklog:open-estate`

### The Meson layer · `sec:genericbacklog:open-build`

**Problem (The generic document layer's labels build record predates the deployed build-sync ledger contract)** · `prob:build:generic-layer-program-identity-under-ledger-contract`

**OPEN.** Measured on 2026-10-29 at 08:35Z: the generic repository's `meson.build`, since 8de937f (the documents-only layer), declares a `labels-record` custom target that calls `build-sync --record labels.toml --producer <linter> --domain server`, while the build-sync deployed to the node tools directory since the dependency-ledger inventories (tools 8e57926, ``entry:build:dependency-bite-version-line-and-ledger``) requires `--ledger`, `--source-root`, `--source-repository` and `--source-commit` and resolves the output's identity from exactly one ledger `program` row whose package, version and release group are checked against the source `meson.build`, which a documents-only layer does not declare. The generic gate on lane r002g03's candidate 44f2f4d7 went red at ninja step 6/7 with `missing_required_argument`, as the base f6052e07 would; the last green generic gate (r002f33, 2026-10-23, base b169374e) ran against the earlier build-sync, and the deploy note of the bite 6 commit (tools 14d6c41) names the document layers' `meson.build` lookups and their report and stamp arguments as a pending change that the layers never received. The unblocking change is r002g03's second commit, which drops the record target and keeps the export. What remains: the generic layer declares its program identity under the ledger contract, so that the label export carries a build record again, and its lookups move to the deployed names (`superloop-lint`, `superloop-pack`, `superloop-install`, and build-sync by its private directory option) in the same change; the instance layer's `meson.build` is checked for the same debt.

Measured on 2026-10-29 at 09:02Z, after generic main moved to 5743fe9a: the host's `~/.local/share/orchestration/labels.toml`, installed on 2026-10-23 by the build target of that time, has no map target any more and stays as a leftover until the record returns or the publisher removes the files the map no longer names; nothing reads it.

**Problem (The generic Meson layer configures without the burn input, so a public consumer can run it)** · `prob:build:burn-input-optional-for-the-public-tree`

**OPEN.** (r002g41 review 1 N4; taken into r002g41 fix round 2 as c09) the generic meson.build refused to configure without `-Dburn_input`, so a public consumer could not run the documents-only Meson layer; the option becomes optional with ordinary-mode lint targets without it. N5 (optional): the root README's install guidance, without estate paths, into a public document later.

**Problem (The generic configure step says which lint mode it selected)** · `prob:build:configure-says-which-lint-mode-it-selected`

**OPEN.** (r002g41 review 2 N1) since c09 (generic 8c121992) a `meson setup` without `-Dburn_input` silently selects ordinary lint mode, shown only as `"public_pack":false` in the report; the estate gate always passes the input, but a hand-run configure could get the weaker check unnoticed. Add a configure-time `message()` (or `warning()`) naming the selected mode when the input is empty.

**Problem (The generic repository installs its documents by Meson's native rules and retires its install map)** · `prob:build:generic-documents-install-natively`

**OPEN.** (2026-11-03) This repository's part of the tools' native install, ``prob:build:native-meson-install`` in the tools backlog: bite 5, the generic repository a documents-only install by Meson's own rules, and its half of bite 8, its install map's removal. Measured at development e8b83958: the layer is documents-only, but its install still runs the tools' install primitive over the generic install map as an install script, so the documents install by map rather than by Meson's native rules.

### Linter declarations · `sec:genericbacklog:open-linter`

### Documents · `sec:genericbacklog:open-docs`

**Problem (the orchestrator rulebook render sits just under the hook's size bound)** · `prob:docs:rulebook-render-size-bound`

**OPEN.** The render sat 30 bytes under its 9,500-byte bound when this was recorded and has not been checked against the tree since; what remains is moving the generic register's long path register into the pointer form or raising the bound with a measured reason, and a generic gate that renders the instance shape so a breaking change is red before import.

the orchestrator rulebook render sits 30 bytes under its 9,500-byte bound (2026-10-21T23:05:09Z): the generic shape ORCHESTRATION.md grew 148 bytes at 870be3c2 (its line 53 names the tools publication homes) and rulebook-install refused the instance render (reason rendered_size) until the instance register lines were trimmed four times (rabe rulebooks/orchestration.md 4,464 to 4,356 bytes; render 9,470). The bound is the hook's (rule:hooks:rulebook-size-bound); the next sentence added to either shape breaks the render again. Proper fix: the generic rulebook's register moves its long path register into the pointer form (the layout of record names the folders), or the bound rises with a measured reason; and the generic gate renders the instance shape so a generic change that breaks the render is red before import.

**Problem (the dispatch rule on refused timestamps does not name the zero-offset form)** · `prob:docs:dispatch-rule-refuses-zero-offset-timestamps`

**OPEN.** The dispatch rule at `docs/spec/dispatch.md:232` still does not name the zero-offset form (`+00:00`) that the hooks fixture sentence pins since lane r002f37; what remains is one line naming zero-offset beside naive, local and nonzero-offset, committed with its regeneration, together with the stray space of "malformed- delay" at hooks.md:380.

`docs/spec/dispatch.md:232` (publication `docs/spec.md:526`) says "Naive, local and nonzero-offset civil timestamps are refused by name rather than assigned a zone" and does not name a zero-offset stamp without a Z (`+00:00`), the boundary the hooks fixture sentence now pins (lane r002f37); its earlier clause "only explicit UTC instants or declared epochs are parsed" may exclude it depending on how "explicit UTC" is read (review of r002f37, 2026-10-23). Fix: the dispatch rule names zero-offset beside naive, local and nonzero-offset, so the two parts agree; one line, one commit with its regeneration. Where: generic docs/spec/dispatch.md; with items ``entry:dispatch:utc-instants-everywhere`` and ``entry:docs:hooks-fixture-pins-zero-offset-timestamp``. Also: the token "malformed- delay" at hooks.md:380 (publication :1018) carries a stray space (`hooks.md:257` spells it `malformed-delay`); fix in the same step.

**Problem (The rulebook roadmap names what each specification part covers)** · `prob:docs:rulebook-roadmap-names-each-spec-part`

**OPEN.** GENERIC rulebook roadmap (r002g72 F1, 2026-11-02): the roadmap no longer lists what each spec part covers; four part labels (spec:dispatch:dispatch-and-supervision, spec:hooks:hook-state-machines, spec:lanes:worker-lane-lifecycle, spec:architecture:architecture-and-authority) are now cited nowhere in the generic tree (no uncited-mint linter check). ~500 B of headroom under the 9,500 B render bound could carry short topic hints back.

**Problem (The to-do profile admits an authored To-do head in backlog documents)** · `prob:docs:todo-profile-admits-authored-backlog-heads`

**OPEN.** (lane bkm01 step 1, 2026-11-03) an authored To-do head is refused by the linter in all three repositories because the registry reserves `todo` for the to-do profile's derived notices; the backlogs carry `prob` (Problem) for work meanwhile. Decide: admit an authored To-do head in backlog documents (ADR-016 + the linter), then rename by one transform.

The rule half is this repository's: the to-do profile (`rec:todos:deficiency-notice-profile`) and its kind extension (`sig:todos:kind-extension`) reserve `todo` for machine-derived notices, so a backlog document needs a stated profile under which an authored To-do head is admitted; the linter's half follows in the tools backlog as ``prob:linter:authored-todo-head-in-backlog-documents``.

### Dispatch and lanes · `sec:genericbacklog:open-dispatch`

**Decision (Workers receive clones of the bare repositories they need and make their own checkouts)** · `dec:dispatch:workers-clone-from-bare-repositories`

**OPEN.** (2026-11-03) Workers of any loop get clones of the bare repositories they need in their workspace and make their own checkouts; the loop pushes into and fetches from those bares; superloops keep their own bares of record and mirror bares on the compute server for fast differential clones. To state in the generic specification (dispatch/lanes part), where the lane forms of each superloop then re-state their provisioning on bares.
