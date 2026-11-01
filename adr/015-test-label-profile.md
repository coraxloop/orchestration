# The Test Label Profile · `rec:profiles:test-inventory-profile`

**Status:** Decided

This record instantiates the inventory-profile signature for Rust tests. The runtime catalogue and owner activations live in the declared surface; this record supplies the human derivation warrant.

## Test census · `sec:profiles:test-census`

**Convention (Owner prefixes)** · `conv:profiles:owner-prefixes`

Each workspace package derives its owner spelling from its crate name through the declared reconciliation rule, while repository policy has its separately declared root owner. Fixture corpora may invent prefixes only inside their own declared roots.

**Convention (Test profile)** · `conv:profiles:test-profile`

The profile covers every Rust function carrying a harness-recognized test attribute under a subscribed package's source and integration roots. Its kind is `test`; its area is `unit`, `crate`, or `integration` from structural home; its name replaces identifier underscores with hyphens; and its standard place is the function's final documentation line.

**Invariant (Test derivation is injective)** · `inv:profiles:test-injective`

Within one owner no two covered tests may derive the same full label or share an identifier that makes the standard-place evidence ambiguous. A collision reports every contributing asset.

**Gate (Test-profile conformance)** · `gate:profiles:test-conformance`

The profile passes only when the live census, derived labels, standard places, committed index subscription, and collision report agree for every subscribed owner.
