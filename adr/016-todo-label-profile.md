# The TODO Label Profile · `rec:todos:deficiency-notice-profile`

**Status:** Decided

This record instantiates the inventory-profile signature for deficiency notices. The declared policy selects owners and surfaces; this record fixes what the derived identity means.

## TODO identity · `sec:todos:identity`

**Signature (TODO kind extension)** · `sig:todos:kind-extension`

The local kind `todo` names a machine-derived deficiency notice and is reserved against authored minting. Its value is the notice identity, not the prose marker alone.

**Convention (TODO census)** · `conv:todos:census`

The census includes recognized TODO markers in scanned source comments. A marker in a string, generated target, displayed example, or unsubscribed owner is outside the production census.

**Convention (TODO profile)** · `conv:todos:profile`

A covered notice derives one owner-scoped label from its stable notice name and carries it at the declared standard place beside the notice. Moving the notice preserves its identity; changing its meaning requires an authored rename and citation update.

**Gate (TODO-profile conformance)** · `gate:todos:conformance`

The profile passes when every covered notice derives exactly one label, every derived label has one notice, and no authored source mints the reserved kind.
