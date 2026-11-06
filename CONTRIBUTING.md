# Contributing to orchestration · `guide:contributing:orchestration`

This is the first reading for a slice worker in the generic repository. The public introduction (`guide:publicorchestration:orchestration`) describes the repository's purpose; the backlog (`plan:genericbacklog:orchestration-backlog`) and its priorities register (`reg:genericbacklog:priorities`) order its open work. The worker charter and the working letter supply the lane's scope, compute route, budget and gate commands; this guide states the repository's practices without embedding an estate's private values.

## Select and work a slice · `sec:contributing:slice-work`

Clone the supplied workspace bare into a checkout of your own, start your lane branch from the base named by the brief, and push only the lane branch to the workspace bare and the compute mirror explicitly named by the working letter (`rule:dispatch:workers-clone-from-bare-repositories`). A producing worker follows the boxed execution rule and its reported in-harness exception (`rule:dispatch:producing-workers-run-in-boxes`). Never sign a worker commit or touch a signing key: the loop makes the reviewed commits of record.

Read each item's first status paragraph together with the priorities register, including dependencies, reading, verification bar and holdings. Select unheld work. Propose twenty to thirty rows, or the whole backlog when it holds fewer, and stop for the working letter (`proto:dispatch:slice-dispatch`). For each row report its label and repository, order and reason, intended commit or coherent pair, files, tests, wall estimate and contradictions with the tree. Name dependencies on another lane rather than taking its held work.

Make each commit of an authorized working step a named Conventional Commit with a body explaining why, and pass the letter's bar at its tip before shipping. A pushed slice branch is never rebased, squashed, amended or force-pushed: merge a moved base into it and append review corrections as fixup commits (`rule:dispatch:lane-branch-merge-in`). The single-bite lane's squash-and-fold convention does not apply. The loop owns the review branch and remakes the reviewed work on the base; a worker never edits the review branch (`proto:dispatch:review-branch-landing`).

## Text and declarations · `sec:contributing:text-and-declarations`

State rules timelessly; keep dated measurements in records and release history. Write each prose paragraph on one physical line. Keep public examples fictional and keep credentials, private addresses and estate-specific values out of this repository. Backwards compatibility is excluded by the repository's versioning policy (`sec:publicorchestration:versioning`).

Headings and named environments mint labels of their declared kind; each label has one mint and keeps its identity. A same-owner citation is a parenthesized backtick label, as in (`req:dispatch:contributing-guide`). A cross-repository citation includes the imported owner inside brackets, as in (`[TOOLS-spec:outputspec:command-and-output-contracts]`); its target must exist in the declared import snapshot. Do not turn an imported label into a local mint. Use double-backtick mentions for file paths or displayed label syntax in prose, such as ``docs/spec/dispatch.md``; they do not participate as citations. Never write the token made by joining a less-than sign, the four letters c h a r and a greater-than sign in a tracked file, including a fixture or example.

Declare every new tracked file in the appropriate inventory reached from ``meson.build``, give it an owner partition in ``.linter/owners.toml`` and classify it in ``public-set.toml``. A new root guide belongs in the root inventory, prose checks and export inputs, not just in a directory. Add a route from an existing reader-facing document. The fictional examples are a separate nested owner: their declarations and instance contract must remain consistent.

Edit authored specification parts under ``docs/spec`` and regenerate the committed publication ``docs/spec.md`` with the linter's assembly command; never hand-edit the generated copy. Keep source declarations, owner partitions, import snapshots, projections and generated publications consistent in the same commit. A change to the imported tools corpus follows its published export rather than inventing a label absent from that export.

## Verification on the named compute node · `sec:contributing:verification`

Use the compute node, tool paths, temporary root and gate form in the working letter. Do not build or run checks in a worker sandbox that the charter reserves for editing. Run the repository's node gate chain over each candidate: root lint in public-pack mode with the externally held burn input, format and projection checks, assembly and census, the Meson lint and template suites, and staged installation twice to prove the second pass changes no file. The gate's conditional Cargo and bootstrap checks apply only when their source trees exist; report an absent branch as inapplicable, not as a test passed. A code-class letter requires the whole bar it names.

The following forms name the linter operations; ``LINTER``, ``BURN_INPUT`` and ``BUILDDIR`` are supplied by the working letter. The burn input stays outside the checkout: pass its path to the linter, never print or copy its contents.

```sh
"$LINTER" --public-pack --burn-input "$BURN_INPUT" check --root .
"$LINTER" --public-pack --burn-input "$BURN_INPUT" project --root .
"$LINTER" fmt --check .
"$LINTER" assemble --root . --write
meson setup -Ddomain=server -Dburn_input="$BURN_INPUT" "$BUILDDIR" .
ninja -C "$BUILDDIR"
meson test -C "$BUILDDIR" --suite lint --suite template --print-errorlogs
git diff --check
```

Before importing a generic shape into an instance, configure with ``-Drulebook_instance_root=/path/to/instance-checkout`` and run the template suite. The render-bound test invokes the production renderer with that instance's render target, reports the UTF-8 byte length and verifies the named `rendered_size` refusal one byte below the render without publishing overlay contents. An empty option checks the fictional instance only and is not evidence for a real instance. The bound is the hook's 9,500 bytes (`rule:hooks:rulebook-size-bound`).

The assembly write precedes the final checks and commit. Keep staged installs in the letter's temporary root, not in a live prefix. If the deployed tools refuse a shape they predate, report the exact mismatch; do not add compatibility aliases or change an unrelated build contract to hide it. For a base failure, retain the same-test base and tip results; for a load retry, retain the rerun evidence and use the letter's classification rule.

## Close and report · `sec:contributing:close-and-report`

A completed item leaves the backlog and its priorities row in the same commit that meets it; adjust the count and preserve the remaining items' order. Put its met claim under Unreleased in ``CHANGELOG.md``, citing the lasting rule or guide rather than the removed backlog mint. An already-met item needs evidence of the check that proves it, not a second implementation. The loop owns the release stamp and the manager's allocation of holdings.

End each working step with one section per named commit: full hash, repository, subject, files and line counts; a table of check commands, wall seconds and results; the start and wait form of every server round; the items closed and their backlog or changelog locations; deviations or NONE; and the ready or blocked word required by the letter (`proto:dispatch:slice-dispatch`). Time substantive commands and distinguish editing, transport and node work. A detached round retains its PID, log and end marker and is awaited in the foreground until that marker; after a lost wait, reconnect to the same round instead of starting it again.
