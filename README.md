# Orchestration · `guide:publicorchestration:orchestration`

Orchestration is a philosophy for running software loops with agent workers. This repository contains rulebooks, a specification, architecture decision records, guides and instance templates: a shared vocabulary for assigning work, reviewing evidence and preserving decisions.

## Rulebooks and instances · `sec:publicorchestration:rulebooks-and-instances`

A rulebook states an agent's responsibilities, boundaries and working practices. The generic shapes in [CLAUDE.md](CLAUDE.md) and [ORCHESTRATION.md](ORCHESTRATION.md) leave explicit overlay slots for the values of an instance. This separates reusable rules from the environment in which they apply.

The fictional [instance templates](docs/examples/README.md) illustrate those overlays, installation maps and supporting records. Their [instance contract](docs/examples/instance-contract.toml) names the required and optional files. The [specification](docs/spec.md) explains how the parts fit together, and the [decision records](adr/) preserve the reasons behind the design.

## Tools and documents · `sec:publicorchestration:tools-and-documents`

The companion repository [superloop-tools](https://github.com/coraxloop/superloop-tools) implements the tooling that reads these documents' labels and maps. Orchestration supplies the rules and shapes; its instance templates show how to supply the values for a particular installation.

Slice workers start with the contributing guide (`guide:contributing:orchestration`), then read the backlog and its priorities register.

## Checking the documents · `sec:publicorchestration:checking-the-documents`

The linter from `superloop-tools` checks the label discipline: every label has one mint, every citation resolves, and document headings conform to their declared environment kinds. The repository's declarations also account for its files and check that the assembled specification agrees with its parts.

## Build identity · `sec:publicorchestration:build-identity`

Meson uses the deployed `superloop-lint` and `superloop-install` commands, with `git` for the source commit and `python3` for the record contract test. Supply `-Dtools_private_dir=PATH` for the directory containing the private `build-sync` helper; the default is the configured prefix and libexec directory followed by `superloop`. The build has no pack invocation; publication uses `superloop-pack` separately. The fictional instance Meson layer declares no program targets or helper lookups.

The label export has exactly one configured program row in ``dependency-ledger.jsonl``. Its non-Cargo version authority is ``meson.build``'s script roster, using the build-sync shell form for generated output: package and release group `orchestration`, identity ``share/orchestration/labels.toml``, and the project's release version. The record beside ``labels.toml`` binds its digest, producer version, execution domain and source commit to that identity. A new commit or checkout reconfigures the build through Git's HEAD and branch ref, so the record names the checked-out commit. The install map consumes the export and verifies its record; staged installation permits a domain mismatch and reports it, while live installation enforces the declared server domain.

The Meson lint suite tests the built export's record, repeated-record stability and named refusals for absent, duplicate and inconsistent identities. Invalid identity tests assert the diagnostic text as well as failure and absence of a record. The instance estate's separate build must declare its own generated identities when it produces them.

## Versioning · `sec:publicorchestration:versioning`

Minor releases introduce big new features; patch releases cover everything else, including corrections and documentation changes. There is no 1.0 release planned. Backwards compatibility is explicitly excluded: every release may change the rules, labels, maps or template formats. Compatibility code for an earlier shape is a defect. The [changelog](CHANGELOG.md) records each release.

## Acknowledgements · `sec:publicorchestration:acknowledgements`

We thank the Torrust developers for the tooling that this philosophy grew beside.

## Licensing · `sec:publicorchestration:licensing`

Code and configuration are licensed under the GNU General Public License version 3 or any later version (`GPL-3.0-or-later`); see `LICENSE-CODE`. Documents are licensed under CC0 1.0 Universal (`CC0-1.0`); see `LICENSE-DOCS`. Third-party notices retain their own terms.
