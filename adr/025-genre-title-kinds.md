# Genre Kinds for Document Titles · `rec:titlekinds:genre-title-kinds`

**Status:** Decided

This record fixes the genre vocabulary used by title mints in this corpus. The vocabulary is declaration data rather than a checker constant: Title recognition asks only that a mint exists and ordinary head validation asks whether Document is catalogued with the authored kind.

## Vocabulary · `sec:titlekinds:vocabulary`

**Definition (Participating title genres)** · `def:titlekinds:genre-kinds`

The participating corpus currently uses seven document genres.

|Kind|Genre|Use|
|----|-----|---|
|`rec`|Record|A durable decision and its consequences.|
|`rep`|Report|Findings, audits, incident evidence, and reviews.|
|`reg`|Register|A maintained list or assembly manifest.|
|`proposal`|Proposal|A recommendation or design awaiting adoption.|
|`spec`|Specification|Normative meaning, requirements, or interface shape.|
|`plan`|Plan|An ordered course of work, including a backlog.|
|`guide`|Guide|Orientation and operating instructions, including README material.|

The corresponding Document pairs are declared in `.linter/environments.toml`. Plan, Backlog, Guide, Readme, and Manual remain local extension names where the base registry has no matching genre row.

**Decision (A title kind names genre)** · `dec:titlekinds:genre-split`

A Title mint's first segment says what kind of document it names. The area states the document's conceptual home and the name is the owner's durable authored identity; neither segment repeats collection membership.

**Rule (Reserved kinds are excluded)** · `rule:titlekinds:reserved-excluded`

A title never mints a reserved machine-derived kind. A document about a test, constant, package, or API remains a record, report, register, proposal, specification, plan, or guide according to its documentary role.

## Declaration and change · `sec:titlekinds:declaration-and-change`

**Decision (No checker-owned title-kind set)** · `dec:titlekinds:no-set`

The checker contains no special list of title kinds. The effective environment relation supplies Document pairs, and the ordinary catalogue verdict rejects an undeclared pair.

**Convention (Genre changes are semantic renames)** · `conv:titlekinds:genre-change`

Changing a document's genre changes the kind segment of its title label and therefore requires every citation to be updated in the same change. Moving the file without changing the document concept changes no label.

**Gate (Genre census)** · `gate:titlekinds:census`

The declared Document pairs and the live title ledger must agree as sets: every live genre is declared, every title carries one genre, and any declared genre with no live document is explained rather than inferred as participation.
