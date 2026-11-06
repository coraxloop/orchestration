# The TODO Label Profile · `rec:todos:deficiency-notice-profile`

Reading order and parent: (`reg:records:philosophy-records`).

**Status:** Decided

This record instantiates the inventory-profile signature for source deficiency notices and states beside it the admission of authored backlog tasks, whose identities are assigned rather than derived. The declared policy selects owners and surfaces; this record fixes the identities and keeps the two censuses disjoint.

## TODO identity · `sec:todos:identity`

**Signature (TODO kind extension)** · `sig:todos:kind-extension`

The local kind `todo` names either a machine-derived source deficiency notice or an authored backlog task in the declared backlog profile (`conv:todos:authored-backlog`). Outside that profile it is reserved against authored minting. Its value identifies the notice or task, not the prose marker alone.

**Convention (TODO census)** · `conv:todos:census`

The census includes recognized TODO markers in scanned source comments. A marker in a string, generated target, displayed example, or unsubscribed owner is outside the production census.

**Convention (TODO profile)** · `conv:todos:profile`

A covered notice derives one owner-scoped label from its stable notice name and carries it at the declared standard place beside the notice. Moving the notice preserves its identity. A replacement with a different meaning receives a new identity; an existing identity is never renamed or reused for that replacement.

**Convention (Authored backlog profile)** · `conv:todos:authored-backlog`

An owner explicitly declares each backlog document covered by the authored profile. In that surface an authored To-do head mints one owner-scoped `todo` label at the standard label position; its first paragraph states its current status. The author assigns a stable task identity, rather than deriving it from a source comment or its current wording. Authored heads outside those declared surfaces are refused. A source-comment marker in a backlog example remains outside the source census. A declared backlog head is counted only by the authored census.

The two profiles share the identity namespace: duplicate labels within or across their censuses are refused. Existing labels, including backlog `prob` identities, remain permanent and retain their citations; admitting new authored To-do heads does not rename existing Problems. A repository mints authored To-do heads only where its linter enforces this admission.

**Gate (TODO-profile conformance)** · `gate:todos:conformance`

The profile passes when every covered source notice derives exactly one label, every derived label has one notice, every admitted authored head mints exactly one label in its declared backlog surface, and no label belongs to more than one notice or task. It refuses authored minting outside the declared backlog profile and duplicate labels within or across the two censuses. Source notices and authored heads are checked by their respective censuses.
