# Changelog

Reading order and parent: (`guide:publicorchestration:orchestration`).

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.6] - 2026-11-17

### Added

- State the priority of sound architecture and good, refactored code over a full test bed, and have designs name focused tests, their commands and claims, deferred testing and continuing obligations (`prin:environment:testing-serves-the-product`), (`req:dispatch:design-names-focused-tests`). Review treats additional testing beyond the design's selection as backlog work without waiving product defects or adopted gates (`rule:conformance:review-beside-gates`), (`proto:conformance:server-verification-loop`).

## [0.1.5] - 2026-11-16

### Added

- The server part refuses exclusive access to a shared instance: no loop, gate, round or measurement holds the instance or a part of it while others wait, and an allocation that gives every loop the same standing is named as fairness (`rule:server:no-exclusive-access-to-a-shared-instance`). A gate queue is admitted only when it is not exclusive, with its wait counted in the gate's wall (`rule:server:a-gate-queue-is-not-exclusive-and-its-wait-is-in-the-gate-wall`), and fairness is an allocation that is declared, rehearsed and measured before any loop adopts it (`req:server:fairness-is-a-declared-rehearsed-and-measured-allocation`).

- The server part rejects a test whose verdict depends on wall time and repairs a red at a wall guard in the test, keeping a hang deadline far beyond any loaded run as the one exception (`rule:server:verdicts-do-not-rest-on-wall-time`). A time is a measurement read with the load beside it (`req:server:a-time-is-a-measurement-read-with-its-load`), two versions are compared in the order A, B, B, A in a focused analysis and never in a general gate (`rule:server:an-abba-comparison-is-a-focused-analysis`), and a gate is sized to the class of its change (`prin:server:proportion-comes-before-capacity`).

- Dispatch requires every requirement of a brief or a review brief to cite its governing label and treats one without a label as a proposal; a brief tightens a rule only explicitly, and a review judges against the governing rules and names uncited requirements (`rule:dispatch:briefs-cite-the-rules-they-state`).

### Changed

- The mail part retries a refused letter after a restart, an observed configuration change or a notification overflow, when its transient retry falls due, when a scan of its sender finds its source changed, and about hourly, in bounded batches; an unchanged refusal triggers no scan of its own (`rule:mail:refusal`).

- The gateway outage recovery proposal has one table separator row sized to its whole header cell, as the linter's formatter writes it; no cell, word or label changed (`proposal:gatewayrecovery:lane-gateway-outage-recovery`).

### Fixed

- The ownership declaration and the publication manifest own and classify the pack's generated provenance, `docs/public-pack-provenance.toml`, as an optional exact member, so a built pack's linter verdict passes; the manifest declares the existing unpublished-label register through `public.unpublished`, so cuts keep its audited generation route, and manifest readers built before that field refuse the tree (``prob:pack:pack-verify-burn-evidence-rule``).

## [0.1.4] - 2026-11-12

### Added

- Dispatch requires tree claims in briefs to be checked before sending and letters about worker files to state the governing boundary rather than a record shape (`rule:dispatch:brief-and-letter-claims`).

- Dispatch limits file confinement to existing mutations, keeps mechanism placement with the loop and requires workers to report duplication as a brief defect (`rule:dispatch:confinement-governs-mutations`).

- The architecture requires documentation reachability and parent return paths; generic directory indexes and upward references provide the authored navigation (`req:architecture:reachable-documentation`).

- The contributing guide gives slice workers the repository workflow, declaration rules, node verification forms and working-step report contract (`guide:contributing:orchestration`).

### Changed

- Configure reports whether it selected ordinary or public-pack lint mode, and the README states that a public consumer configures without a burn input (`sec:publicorchestration:checking-the-documents`).

- Dispatch names zero-offset civil timestamps among those refused by name, matching the hooks fixture boundary, and the hooks fixture matrix spells malformed-delay as one token (`rule:dispatch:timing-led-decisions`).

- The rulebook roadmap gives a topic hint for each of the eight specification parts and cites the architecture, dispatch, hooks and lanes part heads, within the hook's bound as the production renderer measures it (`preview:orch:which-part-to-read`).

- A template-suite test renders the rulebook through the production renderer over the fictional instance, or over an instance checkout named by `rulebook_instance_root`, under the hook's 9,500-byte bound and asserts the named refusal below it; the roadmap names its documentation folders in pointer form (`sec:contributing:verification`).

- The to-do profile admits authored To-do heads on explicitly declared backlog surfaces, with disjoint source and authored censuses, collision refusals and permanent existing Problem identities (`conv:todos:authored-backlog`).

- Mail distinguishes permanent worker birth names from reusable numeric uids, releasing a uid only after durable retirement and custody transfer (`rule:mail:worker-uid-lifetime`).

- Mail defines the per-record serialized journal limit and distinguishes unavailable endpoints from unsafe storage, preserving pending accepted transactions (`def:mail:retention-constants`), (`rule:mail:refusal`).

- The generic build uses deployed command names and an explicit private helper directory, restores the label export's ledger-backed build record and installation, and tests record identity and named refusals (`sec:publicorchestration:build-identity`).

- The CoreOS recipe and root-full requirements share one confined administering login, home-local loop work and explicit route and firmware choices; first-boot policy, deployment probes and recovery distinguish recorded results from unperformed acceptance (`sec:rootserver:the-account-model`), (`reg:rootserver:recorded-fcos-probe-basis`).

- Root-full servers use the latest Fedora CoreOS stable release on the stable stream with confined logins, declarative installation and a declared update window; dated Silverblue measurements retain their historical scope (`sec:rootserver:platform-baseline`).

- The priorities register defines its holdings column: each holding lane with the whole row, an item range or labels, the unheld rest of a row held in part and none for an unheld row, reported by the loop and recorded by the backlog manager; slice selection takes unheld items (`def:dispatch:priorities-register`).

- Producing workers run in boxes; work requiring an exception uses an in-harness subagent of the loop's session and records the friction (`rule:dispatch:producing-workers-run-in-boxes`).

## [0.1.3] - 2026-11-05

### Added

- The superloop mail system replaces letters with opaque file delivery for loops and stably named workers, loop-owned routing and whitelists, notice-only hooks, a one-time migration and a tools conformance register (`spec:mail:superloop-mail-system`).

### Changed

- The rulebook's tone, manners and attention paragraphs and its roadmap are tightened so the instance render stays within its size bound (`preview:orch:which-part-to-read`).

## [0.1.2] - 2026-11-02

### Changed

- Citations to retired tools documents now use public contracts or self-contained historical descriptions, and the TOOLS snapshot is refreshed to the imported public-contract export.

- The public introduction is now the root README, with rulebook and instance-template orientation and the release cadence; every repository file is included in the public source set.

- The generic label export now locates the public introduction's labels at the root README and drops the replaced overview's labels; the declared empty unpublished-label register keeps source checks and public cuts on the same label surface.

## [0.1.1] - 2026-11-01

### Added

- The instance templates under `docs/examples/` are declared as a nested corpus in `.linter/owners.toml`, so the linter checks them as their own repository and reports their evidence instead of dropping it.

### Changed

- `public-set.toml` names the repository in its `[public]` table, which the publishing tool uses as the public tag title.

## [0.1.0] - 2026-11-01

### Added

- First public source cut from a cleaned tip, with independent Git history and a declared publication set.
- Generic rulebooks and the orchestration specification for running software loops with agent workers.
- Environment kinds, label discipline, architecture decision records and operational guides.
- Installation maps and fictional instance templates under `docs/examples/`.
- GPL-3.0-or-later code and configuration and CC0-1.0 documents, with no backwards compatibility before 1.0.

[Unreleased]: https://github.com/coraxloop/orchestration/compare/v0.1.6...HEAD
[0.1.6]: https://github.com/coraxloop/orchestration/compare/v0.1.5...v0.1.6
[0.1.5]: https://github.com/coraxloop/orchestration/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/coraxloop/orchestration/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/coraxloop/orchestration/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/coraxloop/orchestration/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/coraxloop/orchestration/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/coraxloop/orchestration/releases/tag/v0.1.0
