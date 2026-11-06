# Changelog

Reading order and parent: (`guide:publicorchestration:orchestration`).

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- The architecture requires documentation reachability and parent return paths; generic directory indexes and upward references provide the authored navigation (`req:architecture:reachable-documentation`).

- The contributing guide gives slice workers the repository workflow, declaration rules, node verification forms and working-step report contract (`guide:contributing:orchestration`).

### Changed

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

[Unreleased]: https://github.com/coraxloop/orchestration/compare/v0.1.3...HEAD
[0.1.3]: https://github.com/coraxloop/orchestration/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/coraxloop/orchestration/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/coraxloop/orchestration/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/coraxloop/orchestration/releases/tag/v0.1.0
