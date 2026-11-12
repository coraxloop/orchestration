# Fictional instance repository · `guide:examples:instance`

The enclosing source collection is the [generic documentation guide](../README.md); this fixture keeps its own owner and fictional import snapshot.

This is a fictional instance repository for the `alpha` loop, uid 2001, launched from the `dev/alpha` face. It follows version 1 of the instance contract in `instance-contract.toml`; every name, host, session and fingerprint in this tree is a fixture to replace before use.

The generic repository supplies the rulebook shapes and rules, while this instance supplies its server registry, overlays, install maps, backlog, permission records, signing record and public-pack burn values. The optional `orchestration-owned-archive-passphrase.txt` is named by the contract but has no template and is absent from this tree because a sample passphrase could be mistaken for a usable record.

The `.linter/` directory checks this tree as its own corpus. Its imported `ORCHESTRATION` registry is a small fictional snapshot for exercising the import format; an actual instance replaces it with the generic repository's published export. The snapshot's fictional review-boundary rule (`[ORCHESTRATION-rule:fictional:review-boundary]`) is cited here so the check resolves an imported citation. The generic repository's legacy tag, scenario, division, section and record reference families deliberately cover these templates through their `docs/` prose surfaces.

## Reading order · `sec:examples:reading-order`

|Read in order|Label|
|-------------|-----|
|[Example server registry](servers.md)|(`reg:exampleservers:fictional-server-registry`)|
|[Fictional signing record](signing.md)||
|[Example rulebooks](rulebooks/README.md)|(`guide:examples:rulebooks`)|
|[Example permission records](permissions/README.md)|(`guide:examples:permissions`)|
|[Example plans](plans/README.md)|(`guide:examples:plans`)|
|[Example pack records](pack/README.md)|(`guide:examples:pack`)|
|[Example infrastructure](infra/README.md)|(`guide:examples:infrastructure`)|
