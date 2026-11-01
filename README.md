# Orchestration · `guide:publicorchestration:orchestration`

Orchestration is a philosophy for running software loops with agent workers. This repository contains rulebooks, a specification, architecture decision records, guides and instance templates: a shared vocabulary for assigning work, reviewing evidence and preserving decisions.

## Rulebooks and instances · `sec:publicorchestration:rulebooks-and-instances`

A rulebook states an agent's responsibilities, boundaries and working practices. The generic shapes in [CLAUDE.md](CLAUDE.md) and [ORCHESTRATION.md](ORCHESTRATION.md) leave explicit overlay slots for the values of an instance. This separates reusable rules from the environment in which they apply.

The fictional [instance templates](docs/examples/README.md) illustrate those overlays, installation maps and supporting records. Their [instance contract](docs/examples/instance-contract.toml) names the required and optional files. The [specification](docs/spec.md) explains how the parts fit together, and the [decision records](adr/) preserve the reasons behind the design.

## Tools and documents · `sec:publicorchestration:tools-and-documents`

The companion repository [superloop-tools](https://github.com/coraxloop/superloop-tools) implements the tooling that reads these documents' labels and maps. Orchestration supplies the rules and shapes; its instance templates show how to supply the values for a particular installation.

## Checking the documents · `sec:publicorchestration:checking-the-documents`

The linter from `superloop-tools` checks the label discipline: every label has one mint, every citation resolves, and document headings conform to their declared environment kinds. The repository's declarations also account for its files and check that the assembled specification agrees with its parts.

## Versioning · `sec:publicorchestration:versioning`

Minor releases introduce big new features; patch releases cover everything else, including corrections and documentation changes. There is no 1.0 release planned. Backwards compatibility is explicitly excluded: every release may change the rules, labels, maps or template formats. Compatibility code for an earlier shape is a defect. The [changelog](CHANGELOG.md) records each release.

## Acknowledgements · `sec:publicorchestration:acknowledgements`

We thank the Torrust developers for the tooling that this philosophy grew beside.

## Licensing · `sec:publicorchestration:licensing`

Code and configuration are licensed under the GNU General Public License version 3 or any later version (`GPL-3.0-or-later`); see `LICENSE-CODE`. Documents are licensed under CC0 1.0 Universal (`CC0-1.0`); see `LICENSE-DOCS`. Third-party notices retain their own terms.
