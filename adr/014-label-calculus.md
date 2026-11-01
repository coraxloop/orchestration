# A Calculus of Documentation and Source Labels · `rec:labels:calculus`

**Status:** Decided

This record defines the owner-scoped reference graph shared by Markdown and source documentation. Authored concepts mint at their heads, derived assets mint through declared profiles, and citations consume those mints without becoming a second source of authority.

## Syntax · `sec:labels:syntax`

**Language (Labels)** · `lang:labels:label-language`

A label is a colon-joined kind, area, and name. Kind and area are lowercase alphanumeric words; the name is one or more such words separated by hyphens. Prose uses a single backtick span for a mint, a parenthesized span for a same-owner citation, and a parenthesized bracketed prefix for an imported citation. Source comments use the corresponding acute-delimited forms.

**Grammar (Well-formed occurrences)** · `gram:labels:well-formed`

An occurrence participates only when its complete delimiter and label grammar parse in a scanned prose or documentation-comment region. Fenced blocks, doubled display delimiters, ordinary code strings, and fixture payloads outside scanned regions create no occurrence.

**Signature (Owners and partition)** · `sig:labels:owners`

Every participating source belongs to exactly one declared owner. A complete label is unique only within that owner; an imported citation names the target owner explicitly by its registered prefix.

**Signature (Inventory profiles)** · `sig:labels:profiles`

The profile signature lists each derived kind, its census, classification, name transformation, standard place, and collision rule. A profile may derive only the assets selected by its declared activation.

**Signature (Reserved kinds)** · `sig:labels:reserved-kinds`

Kinds assigned to machine-derived assets are reserved. Authored prose may cite their derived mints but may not mint those kinds as a substitute for the registered derivation.

## Warrants and citations · `sec:labels:warrants-and-citations`

**Inference rule (Authorship warrant)** · `inf:labels:authorship-warrant`

An authored mint is warranted by the owning corpus's durable choice to name the concept expressed at that head. Moving or retitling a concept preserves the mint when the concept remains; renaming a mint requires every citation to move in the same change.

**Inference rule (Same-owner citation)** · `inf:labels:same-owner-citation`

A parenthesized unqualified label resolves only to the unique mint of that label in the citing source's owner. It never searches another owner or guesses from an area name.

**Inference rule (Imported citation)** · `inf:labels:imported-citation`

A parenthesized bracketed prefix and label resolve only when the prefix is registered, the named owner mints the label exactly once, and the owner-reach policy permits the import.

**Judgment (Participation)** · `judg:labels:participation`

Only structurally recognized Markdown spans and documentation-comment spans participate. Displayed examples and fixture data remain inert unless a fixture explicitly declares and scans its own fictional corpus.

**Invariant (Unique mint)** · `inv:labels:unique-mint`

Within one owner, one complete label has exactly one mint. Duplicate source locations are a defect and neither is selected as authoritative.

**Invariant (Total resolution)** · `inv:labels:total-resolution`

Every participating citation resolves to exactly one mint under its owner form. An unresolved, ambiguous, self-qualified, malformed, or unreachable citation is a failing graph judgment.

**Meta-theorem (Warrant lapse)** · `metathm:labels:warrant-lapse`

When an authored concept is removed or a derived asset leaves its census, its mint lapses and every surviving citation becomes unresolved. The failure is therefore visible at each dependent claim rather than concealed by a stale register.

## Boundaries · `sec:labels:boundaries`

**Caveat (Owner coexistence)** · `cav:labels:coexistence`

Different owners may mint the same complete label without collision. The owner boundary is part of resolution even when prose omits it for a same-owner citation.

**Caveat (Labels are non-normative)** · `cav:labels:non-normativity`

A resolving citation establishes identity and reach, not truth, priority, or adoption. Normative force comes from the cited record's role and the corpus decision that admits it.

**Ansatz (Code-font delimiters identify labels)** · `ansatz:labels:code-font-delimiters`

Treating every code-formatted token as a label would turn examples, paths, identifiers, and fixture strings into accidental graph edges. Rejected: participation requires the exact occurrence grammar and scanned-region rule.

**Gate (Implementation)** · `gate:labels:implementation`

The calculus is implemented only when formation, head conformance, uniqueness, resolution, owner reach, profile derivation, and displayed-material exclusion are separate reproducible verdicts over one harvested graph.
