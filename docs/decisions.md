# Public decisions · `reg:decisions:governing-rulings`

This register collects durable decisions that govern the reusable orchestration system. Each entry states the rule that remains in force, its rationale, and the earlier posture it replaces.

**Decision (Specification concept accepted)** · `dec:decisions:spec-concept-accepted`

The specification programme uses the proposed root-level carrier and eight-part partition; the generic assembly carries seven of those parts (`conv:assembly:assembly`), and the command and output part, the tool build and install contracts and the linter conformance contracts are specified by the tools repository (`[TOOLS-spec:outputspec:command-and-output-contracts]`), (`[TOOLS-spec:deployment:tool-build-and-install-contracts]`), (`[TOOLS-spec:conformance:linter-conformance]`). Architecture, output, and conformance form the initial benchmark band; the remaining parts enter after the first shape report. Mutable operating facts remain in registries and runbooks constrained by stable requirements. External streams, exit meanings, and final report lines remain byte-stable, while internal state files may change through declared migrations. Anti-vacuity floors derive from a committed census rather than inherited fixed bounds.

This structure makes conformance measurable without freezing changing deployment data into normative prose. It supersedes the concept proposal's pending status and resolves its carrier, partition, benchmark, mutable-fact, compatibility, and anti-vacuity alternatives.

**Decision (Build and deployment topology)** · `dec:decisions:build-deployment-topology`

Routine development and self-contained testing run in the shared compute domain, and binaries used there are built there. A trusted host builds only an installable host artifact from a fixed, reviewed milestone tag as part of installation; that admitted release build is outside the routine host compile ceiling. Installation copies the resulting outputs into the harness-owned target tree.

Building in the execution domain keeps executable artifacts from crossing the evidence boundary, while the narrow tagged host exception preserves host trust and reproducibility. This supersedes routine host compilation, importing server-built executables for host use, and installing host artifacts built from untagged state.

**Decision (Release cadence is milestones)** · `dec:decisions:release-cadence`

Releases advance by reviewed milestones. The milestone tag exists and resolves to the reviewed commit before configuration, compilation, or installation begins, and the trusted host never builds an untagged candidate.

Tag-first release identity makes every admitted artifact traceable to stable reviewed source. This supersedes rolling branch-tip releases, untagged host builds, and attempts to validate an earlier build by tagging it afterward.

**Decision (No shell)** · `dec:decisions:no-shell`

Maintained helper behavior is implemented in Rust, while maintained build and installation orchestration is expressed in Meson. A shell program may remain as migration evidence or a behavioral reference, but no released build, verification, installation, hook, lane, or wrapper path delegates maintained behavior to it.

Rust and Meson make argument handling, failure semantics, evidence, and installation structure explicit and testable. This supersedes maintained shell helpers, including shell trampolines around otherwise conforming commands.

**Decision (Meson installs)** · `dec:decisions:meson-installs`

Installation runs through Meson from a reviewed milestone tag. The install path preserves content-sensitive copies, verified backups of outgoing bytes, declared permissions, and unchanged modification times for unchanged content; when stock Meson operations cannot prove those properties, Meson invokes a typed Rust installation primitive using the declared target map.

Those guarantees preserve reproducible deployment and the modification-time signal consumed by change detection. This supersedes ad hoc shell copy loops while retaining their required content, backup, permission, and timestamp semantics.

**Decision (Multi-superloop integration is achieved)** · `dec:decisions:multi-superloop-integration`

Distinct worker harnesses are integrated through one orchestration policy and one reviewing evidence path even though their launch, instruction, resume, transcript, and completion mechanics differ. The coordination rulebook carries rosters, gates, degraded operation, server operations, and heartbeat policy; refinements land there.

Integration is an operational property of shared dispatch, supervision, evidence, and final review rather than uniform provider mechanics. This supersedes treating multi-harness integration as an unstarted design campaign or requiring a separate integration document.

**Decision (Lane verification is Rust)** · `dec:decisions:lane-verify-rust`

Lane verification is a maintained Rust tool. Its former shell implementation remains only a behavioral reference, and the ratified lane and output contracts govern wherever the two differ.

The Rust implementation provides typed argument and process boundaries, deterministic status mapping, controlled evidence output, and fixture-backed verification while satisfying the no-shell architecture. This supersedes both the assessment of whether to port the verifier and the shell verifier as the maintained implementation.

**Decision (Corpus-adoption boundary)** · `dec:decisions:corpus-adoption-boundary`

Adoption of the label calculus separates mechanical migration from semantic documentation work. The mechanical phase establishes committed burn-register ratchets and converts the existing programme plan to the label calculus; specification and broader document-conformance work proceed as separately reviewed campaigns.

Keeping those phases distinct prevents a syntax-and-inventory migration from silently changing normative meaning. This supersedes any reading of mechanical adoption as authorization for a simultaneous specification or corpus-wide conformance rewrite.

**Decision (Signing keys are per-loop, sign-only, and one year)** · `dec:decisions:signing-keys-per-loop`

Every superloop signs its git history with its own OpenPGP key held in its own keyring directory: a certify-only root with one sign-only subkey, both expiring after one year, rotated on time and on any new host, with four revocation certificates written before the certify private key is purged and the signing private key purged at end of life. Signing configuration is repository-local, and global git configuration carries no signing key (`spec:signing:gpg-keys-and-commit-signing`).

A key narrow in capability, custody, and lifetime is evidence of which loop acted; a machine-wide key is only evidence that the machine acted. This supersedes the earlier posture in which a global `user.signingkey` remained after the global identity was removed.
