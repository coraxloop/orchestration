# Document-Title Labels · `rec:doctitles:document-title-labels`

**Status:** Decided

This record makes the document concept citable through its first structural level-one heading. It extends the existing label calculus structurally and leaves occurrence grammar, owner-scoped uniqueness, and citation reach unchanged.

## Title head · `sec:doctitles:title-head`

**Decision (A title carries an authored genre kind)** · `dec:doctitles:title-kind`

The first structural level-one heading is the source's sole Title head and carries exactly one authored mint. Its environment name is Document, while its kind names the document's genre from the locally declared effective relation. The checker derives neither kind, area, nor name from title spelling or location.

**Decision (Coverage follows a structural title)** · `dec:doctitles:coverage`

Every tracked Markdown source with a structural level-one heading participates, including README documents and generated registers. A source without such a heading is exempt; no synthetic title or mint is invented for it.

**Decision (Later level-one headings remain divisions)** · `dec:doctitles:first-heading`

Only the first structural level-one heading is a Title head. A later level-one heading is an ordinary division and carries a section mint under the same rules as any other structural heading.

## Citation and migration · `sec:doctitles:citation-and-migration`

**Decision (A title citation names the document concept)** · `dec:doctitles:citation-semantics`

A citation of a title mint asserts the continued existence of that document concept in the named owner. It asserts neither byte identity, current title spelling, current path, nor the complete set of nested heads.

**Decision (Targets precede replacements)** · `dec:doctitles:migration-order`

Migration establishes the target title mint before rewriting a locator or legacy record reference. The replacement must resolve under owner reach before the old form and its ratchet row are removed.

**Gate (Title participation)** · `gate:doctitles:participation`

The title migration is complete only when every tracked titled source is accounted, every participating title carries exactly one accepted genre-kind mint, later heads remain ordinary environments, and title citations resolve without duplicate generated authority.
