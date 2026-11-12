# Design and systemd orchestration · `guide:coreos:design`

Reading order and parent: (`guide:coreos:bare-metal-server-guides`).

**Principle (Reproducible host)** · `prin:coreos:reproducible-host`

A host is manageable when one installation file and versioned increments reproduce it, and everything running on it is supervised, bounded and backed up. FCOS supplies the immutable base; the reference setup layered only the few extra packages it needed, including tmux and python3, through rpm-ostree and rebooted to activate layers. Small idempotent scripts add post-install state. The installation listing is (`listing:coreos:butane-file`), and the increment contract is (`req:coreos:increment-contract`).

**Remark (Estate boundary and FCOS differences)** · `rem:coreos:estate-boundary`

This is the fictional recipe for the root-full Fedora CoreOS stable baseline (`sec:rootserver:platform-baseline`), under the root-custody and source-of-record boundary (`sec:rootserver:what-a-root-full-server-is`). Every login is confined; one registry-selected login administers through the explicit transition and provider rescue remains independent (`sec:rootserver:the-account-model`). Loop hubs, lanes and caches stay in homes; the labelled shared-project tree is optional application data, not an alternative loop layout (`sec:confinedadmin:the-filesystem-is-typed-loop-data-lives-in-homes`). The outbound application tunnel publishes selected services, while a site WireGuard door supplies a separately selected administration route; neither replaces provider rescue (`sec:rootserver:the-door`). The recipe uses nftables. Its fictional legacy BIOS and no-TPM hardware do not claim UEFI Secure Boot acceptance; firmware-specific probes follow the selected machine (`sec:rootserver:platform-baseline`).

**Remark (Execution and authority)** · `rem:coreos:execution-authority`

This fictional execution-server setup illustrates (`spec:server:server-execution-and-trust`) and (`spec:deployment:build-and-deployment-topology`). Routine checks follow (`rule:server:server-first-computation`); a service or rehearsal succeeding on a server does not change the source and review boundary (`rule:architecture:host-to-server-direction`), (`rule:architecture:server-results-are-data`). Fictional scenario results are explanatory fixtures under (`conv:coreos:measurement-scope`), not illustrated evidence under (`spec:conformance:conformance-and-evidence`) or authority to adopt the configuration.

## One service manager · `sec:coreos:one-service-manager`

**Principle (Systemd alone orchestrates)** · `prin:coreos:systemd-only`

Systemd is the only orchestrator in this setup: there is no Kubernetes or compose layer. Production containers are root-owned system Quadlets; development and agent stacks are rootless user Quadlets in unprivileged accounts. Systemd does not supply SELinux confinement, offsite storage or container network isolation: those come from the image policy, the backup destination, and Podman networks plus nftables respectively.

**Table (Mechanisms)** · `tab:coreos:mechanisms`

|Need|systemd mechanism|
|----|-----------------|
|Production services|System Quadlets in `/etc/containers/systemd/*.container` under a dedicated `production.slice`, with `Restart=`, healthchecks and `[Install]`|
|Development and agent workloads|each account's own `systemd --user` manager, user Quadlets, `loginctl enable-linger`|
|Resource ceilings|`user.slice` and per-user slices with `MemoryHigh`/`MemoryMax`/`CPUQuota`; `production.slice` with `MemoryLow` and `CPUWeight`|
|Periodic jobs (backups, watchdogs, cleanup)|`*.timer` + `*.service`, with `OnFailure=` pointing to a notifier|
|Secrets|Podman secrets for Quadlets; `LoadCredential=`/systemd-creds for plain units|
|Logs|journald; `journalctl -u` is the only log source|
|Host updates|Zincati with a fixed weekly window|

**Principle (Confinement and resource boundaries)** · `prin:coreos:confinement-and-ceilings`

The common staff-to-sysadm transition is described in (`sec:rootserver:administering-under-confinement`). Here every login account maps to `staff_u`, the single example-admin login elevates to `sysadm_r:sysadm_t` through sudo, and all other example accounts have no sudo. Aggregate and per-account slices bound workloads so one account does not consume the capacity reserved for production and the kernel; the illustrated failures and revised fractions are in (`scenario:coreos:aggregate-pressure`) and (`tab:coreos:slice-ceilings`).

**Principle (Backups and a known update window)** · `prin:coreos:backups-and-window`

The fictional design calls for offsite, encrypted restic backups over SFTP to a storage target every 20 minutes, preceded by each database’s consistent-backup method, and Zincati reboots within a known weekly slot. The example backup placement falls short of the offsite design (`obs:coreos:backup-deployment-gap`). The window and example update recovery are recorded in (`obs:coreos:reference-state`) and (`scenario:coreos:window-reboot`).

**Rule (Experimentation is operational work)** · `rule:coreos:experimentation`

An experimental server receives key-only access, a firewall, separate identities, offsite backups and secret handling that keeps secrets out of chat and tickets. The host's owner holds root custody and decides any explicit, named deferral. Disk encryption was the fictional host's recorded deferral (`obs:coreos:hardware`).
