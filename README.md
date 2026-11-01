# Orchestration · `guide:publicorchestration:orchestration`

Orchestration is the philosophy for running software loops with agent workers. This repository contains the rulebooks, environment kinds and labels, architecture decision records, guides, maps read by the install tooling, and instance templates under `docs/examples/`.

## Tools and documents · `sec:publicorchestration:tools-and-documents`

The companion repository `superloop-tools` implements the tooling that reads these documents' labels and maps. Orchestration supplies the rules and shapes; its instance templates show how to supply the values for a particular installation.

## Checking the documents · `sec:publicorchestration:checking-the-documents`

The linter from `superloop-tools` checks the label discipline: every label has one mint, every citation resolves, and document headings conform to their declared environment kinds. The repository's declarations also account for its files and check that the assembled specification agrees with its parts.

## Versioning · `sec:publicorchestration:versioning`

This is version 0.1.0. Before 1.0, backwards compatibility is explicitly excluded: every release may change the rules, labels, maps or template formats. Compatibility code for a pre-1.0 shape is a defect.

## Acknowledgements · `sec:publicorchestration:acknowledgements`

We thank the Torrust developers for the tooling that this philosophy grew beside.

## Licensing · `sec:publicorchestration:licensing`

Code and configuration are licensed under the GNU General Public License version 3 or any later version (`GPL-3.0-or-later`); see `LICENSE-CODE`. Documents are licensed under CC0 1.0 Universal (`CC0-1.0`); see `LICENSE-DOCS`. Third-party notices retain their own terms.
