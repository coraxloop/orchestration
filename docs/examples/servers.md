# Example server registry · `reg:exampleservers:fictional-server-registry`

This is a complete example of the instance repository's `servers.md` document. Every server and fact below is fictional; no endpoint, port, credential, or expiry value describes a live system.

## Alias discipline · `sec:exampleservers:alias-discipline`

Server names are locally meaningful bird names represented in ASCII. Repository prose uses `<bird>-<account>` aliases and `<bird>-root` for management, while addresses and transport details live only in the operator's SSH configuration.

## Server registry · `sec:exampleservers:server-registry`

|Name|Location|Specs|Restrictions|
|----|--------|-----|------------|
|`sagofink`|fictional island laboratory|fictional four-core host, ample memory, solid-state storage, immutable operating system|Persistent build host. Aliases include `sagofink-root`, `sagofink-orchestration`, and `sagofink-public`; all access is key-only and account-scoped.|
|`mondreiher`|fictional mountain observatory|fictional twelve-core host, accelerator, redundant storage, enforcing mandatory access control|Persistent accelerator host. Aliases include `mondreiher-root`, `mondreiher-analysis`, and `mondreiher-public`; the showcase account has no administrative authority.|
