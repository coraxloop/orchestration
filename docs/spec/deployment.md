# Build and deployment topology · `spec:deployment:build-and-deployment-topology`

This part specifies the agent execution environment and the orchestrator's selection of execution domains, containers, scheduling priority and routine toolchains (`sec:assembly:deployment-outline`). Tool construction, installation, managed-copy semantics and deployment evidence belong to (`[TOOLS-spec:deployment:tool-build-and-install-contracts]`). Every label minted here has area `deployment`.

## Scope · `sec:deployment:scope`

This part owns the agent container, execution-domain selection, dedicated tool containers, minimum build priority, interpretation of contention, routine toolchain selection and formatter resolution. Implementation languages, build and install mechanisms, cache and storage contracts, milestone admission, target mappings, copy and backup behavior, and deployment evidence are specified by (`[TOOLS-spec:deployment:tool-build-and-install-contracts]`).

It does not own a helper's externally visible behavior, the hook transition system, or operation of the compute server. A replacement preserves its public bytes and statuses under (`rule:architecture:external-contract-stability`), and the rulebook target preserves the input transition required by (`proto:hooks:rulebook-change-notice`). Server connection, wrapper, callback, and lifecycle behavior remains governed by the server part; this part cites that part only to select and constrain a build domain.

**Definition (Agent container)** · `def:deployment:agent-container`

The agent container is the toolbox container in which an agent's shell runs on the trusted host; it is not the host shell. Host tools and the container engine are not on its path: a host command runs through the host escape, and a project's own containers run on the host's engine, reached through the same escape. Project directories are bind-mounted into those containers, so files are edited at their host paths and only execution passes through the container; a project's own documents name its container, mount point and ports. The container's name, image and escape command are machine-registry values under (`rule:architecture:dynamic-facts-stay-in-registries`).

## Build domains · `sec:deployment:build-domains`

This division governs execution-domain selection, dedicated containers, scheduling priority and routine toolchains. The tool build and install contracts supply the cache and temporary-storage requirements (`[TOOLS-spec:deployment:tool-build-and-install-contracts]`); compute-server operation remains with the server part.

**Rule (Build where executed)** · `rule:deployment:build-where-executed`

An executable shall be built in the execution domain in which its installed or deployed copy will run: server helpers on the server, and trusted-host helpers on the trusted host. Data-only targets are copied from the tagged tree and do not acquire a build domain. The trusted host builds every host-executed binary from a clean checkout of the tools repository at the tagged commit. The generic and instance repositories install only copies and renders of tracked files, so neither acquires a build domain. Their installs run on the trusted host with the deployed tools from clean tagged checkouts at minimum priority and with a disk-backed temporary root; exact paths remain registry data. Each build domain uses one Meson build directory and one Cargo target directory per purpose, with its own package cache and toolchain selection (`[TOOLS-rule:buildcontracts:build-provenance]`).

An artifact crossing a domain boundary is data for inspection, not an executable candidate. A helper whose execution domain changes must follow the execution-domain rebuild protocol (`[TOOLS-proto:deployment:execution-domain-rebuild]`); copying the old binary or renaming its directory is insufficient.

**Rule (Dedicated tool containers)** · `rule:deployment:dedicated-tool-containers`

A tool the host lacks runs in a registered dedicated toolbox, entered through the host escape with the disk-backed temporary root and the project directory explicit. A tool absent from every toolbox is installed into a new dedicated toolbox, never onto the host and never into the agent container (`def:deployment:agent-container`), which stays as provisioned. A new toolbox receives the disk-backed temporary-root profile before first use, and after a toolbox is created or changed its inventory is refreshed from the host's container listing, which is the inventory of record.

**Rule (Minimum build priority)** · `rule:deployment:minimum-build-priority`

Every compile, link, code-generation action, and gate that may rebuild shall start in the lowest-priority scheduling class available in its execution domain, and all expensive descendants shall inherit that class. This applies to server development builds, tagged host builds, and the vendored-checker exception. Priority is established before the first expensive child and its effective class is captured in evidence.

The semantic minimum is a durable constraint; the scheduler name, wrapper, slice, weights, and other mechanism are current machine-registry values. If the selected domain cannot establish or demonstrate the minimum, the build fails before expensive work. Server-side enforcement remains governed by (`rule:server:minimum-build-priority`).

**Remark (Contention slowdown)** · `rem:deployment:contention-slowdown`

Idle scheduling bites only under contention: on an idle machine a minimum-priority build still receives the whole processor. A build slowed by interactive use is therefore the priority rule working as intended; its report notes the contention, and the slower wall is not a regression finding.

**Convention (Routine toolchain)** · `conv:deployment:routine-toolchain`

Routine Rust development, meaning every routine build, test, gate, and formatter run, uses one designated routine toolchain, which is nightly unless a project records another designation with its reason in its own documents; every routine run reuses that designation, so toolchains never alternate between routine runs. Stable and minimum-supported-version runs are not development toolchains: they are reserved for tags, releases, and other significant verification moments, alongside the full multi-toolchain sweeps, and never serve a routine lane or a per-merge gate. Formatter and lint configurations may use nightly-only keys, because the nightly formatter is the formatter of record and a stable run's silent fallback is no verdict.

**Hint (Formatter resolution)** · `hint:deployment:formatter-resolution`

`cargo fmt` resolves through the cargo home's `bin` shims before `PATH`, so inside a toolbox it can run a different rustfmt than the one on `PATH`. Recipes therefore invoke the binary form `cargo-fmt`, which resolves the formatter on `PATH` deterministically.
