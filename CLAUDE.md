# Environment (applies to every project on this machine) · `spec:environment:global-project-environment`

**Preamble (Audience)** · `pref:environment:audience`

This file carries the rules every agent session on this machine needs, orchestrator or dispatched worker, top-level or subagent. Orchestration policy reaches top-level sessions separately, and a dispatched worker's brief and charter govern its task.

**Notation (Labels)** · `ntn:environment:labels`

A label has form ``kind:area:slug``: its kind names the statement's form, its area names the subject, and its slug identifies the statement within that kind and area. A mint appears once in the tree in single backticks after its heading; a citation appears in parentheses with single backticks; a plain mention uses double backticks. Find a rule by searching the tree for its label, including the mint and every citation, rather than paraphrasing it: a paraphrase drifts from the text it recalls, while a label stays fixed and the linter checks that each label is minted once and each citation resolves. The kinds a label may carry, each with its environment name and what it marks, form the kind registry (`rec:kinds:environment-kind-registry`), installed at `~/.local/share/orchestration/adr/011-environment-kinds.md`; a kind is taken from that registry by what the statement is, never coined for the occasion.

**Principle (Timeless on its merits)** · `prin:environment:timeless-on-its-merits`

Rules and internal documents are stated timelessly and on their merits. Git's author and date metadata are a change's provenance and its commit message states the engineering reason, so the text carries no dated rulings, which appear only in publicly shared documents or on explicit request; dates on measurements and events are data and stay. Every artifact an agent produces (rulebooks, documentation, code and comments, commit messages, backlog records, memory files) states what holds and why, as an engineering argument, never as a directive from a person: no verbatim rulings, no "the owner said", no "per the user". The test is whether the text stands for a reader who does not know who decided; a role stays nameable where it is a fact of the process, because that names who acts, not why the rule holds. A change that cannot be stated naturally on its merits lacks its reasoning, not its wording, and is raised with the user before it is written; the same holds for a memory or backlog record that only the one who asked for it could justify.

**Convention (Markdown runs)** · `conv:environment:markdown-runs`

A Markdown paragraph is one line, and so is each list item and table row; the viewer soft-wraps it. Prose is never hard-wrapped, a legacy-wrapped paragraph is reflowed when touched, and formatting is the toolchain's job rather than a hand-maintained artifact.

**Requirement (Wall time is measured and reported)** · `req:environment:wall-time-reported`

Every action reports its duration: tests, gates, builds, scripts and lanes, with per-step wall times in reports (a `time` prefix, lane timers, report contracts and `duration_ms` all count). An action that did not report how long it took is a process defect, reported as a finding and fixed in the harness or script, and a duration regression is a finding like any other regression.

**Requirement (Gate batteries report their resource deltas)** · `req:environment:gate-resource-deltas`

Every gate script samples the cgroup it runs in at the start and the end of each battery and of the whole gate (`cpu.stat` usage, user, system and throttled periods; the PSI averages and stall totals of `cpu.pressure`, `memory.pressure` and `io.pressure`; `memory.current` and `memory.peak` where present), prints the start sample, the end sample and the deltas beside the battery's wall time in the gate log and in its report, and prints the battery's own user and system CPU from process accounting on the same line, because a wall without its resource deltas cannot tell a slow candidate from a loaded node, and a duration regression needs its cause on the same line (`req:environment:wall-time-reported`). The samples name the cgroup's scope: on a cgroup shared by every session of a node the usage deltas are the node's load and the stall totals over the wall are the pressure figure, only a cgroup the gate entered for itself makes the cgroup deltas the gate's own, and the process-accounting figures are the gate's own in either case. A gate that prints a wall without its deltas, or cgroup figures without their scope, is a process defect, reported as a finding and fixed in the gate form.

**Invariant (Git identity is per repository)** · `inv:environment:git-identity-per-repository`

The machine carries no global git `user.name`, `user.email` or `user.signingkey`: every repository, and every lane clone at provisioning, sets its own local identity, and a commit that fails for a missing identity means that setup step was skipped, fixed by local configuration and never by a global. Forge credentials (`gh` state, tokens, deploy keys) are per-loop facts verified before use, never inherited from the environment, and no loop assumes it shares a forge account with another loop or with the owner. Signing keys are per loop, and each repository names its loop's signing subkey locally (`spec:signing:gpg-keys-and-commit-signing`).

**Rule (Private credential custody)** · `rule:environment:private-credential-custody`

The host's own uid owns no private credential: no gpg private key, ssh private key, forge token, Codex sign-in or Claude sign-in other than the host's own Claude desktop application. The only exceptions to keeping credentials off the host's uid are the public half of the server-provisioning key in the host's ssh directory and the owner's own desktop applications (Claude desktop, browser and editor). Every loop's private credential lives in that loop's private tier under the loop's uid and is reached only through the loop entry, because a host-owned credential is readable by every session and toolbox of the host. A credential found at the host's uid outside those exceptions is a finding naming its migration to the owning loop's private tier.

**Rule (AI attribution trailers)** · `rule:environment:ai-attribution-trailers`

An artifact an agent produces (a commit message, a letter, a post or a record) carries no AI attribution trailer by default: no `Co-Authored-By` naming a model and no "generated with" line. Its provenance is the repository's identity and the message's stated reason; a trailer names a tool rather than a fact of the change. A loop's explicitly stated policy in the loop's own documents may require or permit such a trailer, and only then does one appear.

**Warning (The angle-bracket c-h-a-r token)** · `warn:environment:five-character-token`

The token spelled angle bracket, the word c-h-a-r, angle bracket is kept out of every file saved to git, in code and prose alike, because chat transports substitute it with a role or account name: a pasted file containing it reads as code that cannot compile, and a reviewer correctly flags the artifact as self-refuting. In Rust, type inference (`let cs: Vec<_> = s.chars().collect()`) or a local `type` alias replaces the explicit generic; third-party text that contains it is quoted split or aliased.

**Procedure (Host tools build in the build toolbox)** · `alg:environment:host-tools-build-in-the-build-toolbox`

A tool is first looked for on the `PATH` of an existing toolbox and used directly when present. The host has no build route of its own: the SDK extensions its code editor's runtime carries serve the editor and are never used to build. A tool that executes on the host is built in the registered build toolbox on the distribution's packaged toolchain, package-scoped and `--release --locked`, at minimum priority, from the imported commit, with a provenance record naming the commit and the wall, because a binary cannot be reviewed as a text diff; every other tool the host lacks runs in a registered dedicated toolbox. Workers call a repository's registered prebuilt linter for its subcommands and never build it; rebuilding it after an import that touches it is the orchestrator's step.

{{overlay:sec:environment:build-toolbox-profile}}
{{overlay:sec:environment:temporary-storage-profile}}
