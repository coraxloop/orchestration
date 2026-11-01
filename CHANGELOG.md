# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/coraxloop/orchestration/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/coraxloop/orchestration/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/coraxloop/orchestration/releases/tag/v0.1.0
