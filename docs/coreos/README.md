# Bare-metal Fedora CoreOS server guides · `guide:coreos:bare-metal-server-guides`

**Remark (Scope and neighbouring setup)** · `rem:coreos:scope`

This set is an expressly fictional worked example: it describes the fictional node `example-node.example.invalid` under fictional names, addresses, account mappings, device identifiers and operating figures. It is not a record of a deployed estate. The example has 96 GiB of RAM and 24 CPU threads; its documentation addresses are `192.0.2.10` for the node and `198.51.100.20` for `example-backup.example.invalid`, with SSH aliases `example-node` and `example-backup`. The fictional accounts `example-admin`, `example-ops`, `example-dev`, `example-agent-1` and `example-worker` use UIDs 41010 through 41014 respectively; their private subordinate UID/GID ranges are assigned separately. The fictional system disk is `/dev/disk/by-id/nvme-EXAMPLE_SYSTEM_DISK`. Names and values must be selected and verified for an actual installation. The example complements (`guide:rootserver:root-full-server-setup`): common root-custody, confinement and execution-domain requirements remain there, while these guides illustrate FCOS installation, systemd service composition and recovery.

**Convention (Measurement scope)** · `conv:coreos:measurement-scope`

Every observation, timing, capacity and scenario result in this set is an illustrative fixture within the fictional example, not evidence that a deployment or measurement occurred. Public software names, protocol constants and failure mechanisms retain their technical meaning. The legacy BIOS, single-disk and no-TPM constraints are deliberate scenario assumptions because they explain the installation and recovery choices. Planned work remains planned within the scenario, following (`rule:conformance:unmeasured-claims`); it is not evidence of deployment. Actual operating selections and illustrated results belong in their owned registries or runbooks (`rule:architecture:dynamic-facts-stay-in-registries`).

**Observation (Fictional reference state)** · `obs:coreos:reference-state`

The fictional state uses a selected Fedora CoreOS release, kernel and Podman version, with SELinux enforcing, `/var` on XFS with `prjquota`, nftables active, firewalld inactive and the default `net.ipv4.ip_unprivileged_port_start=1024`. The example assumes one NVMe disk, legacy BIOS boot, no TPM and no disk encryption; installation uses `coreos-installer` from a fictional provider rescue system. Zincati uses a periodic Saturday window at 04:00 UTC for 45 minutes. The backup destination is initially a practice VM on this same hardware: a separate-provider offsite target and owner-held backup/database secret custody remain planned, not executed within the scenario (`obs:coreos:backup-deployment-gap`), (`obs:coreos:secret-custody-gap`).

**Register (Reading order)** · `reg:coreos:reading-order`

1. `README.md` — fictional scope, fixture vocabulary and reading order (`guide:coreos:bare-metal-server-guides`).
2. `design.md` — principles, systemd mechanisms and differences from the estate baseline (`guide:coreos:design`).
3. `boot.md` — hardware, deployment rules, reboot rehearsal and identity pinning (`guide:coreos:boot`).
4. `butane.md` — the installation file, block annotations and first-boot additions (`guide:coreos:butane`).
5. `increments.md` — identities, workspaces, user managers, ceilings, supervision, networking, replicas and watchdogs (`guide:coreos:increments`).
6. `data-services.md` — the backup increment and the database, datastore, messaging and durable-execution increments (`guide:coreos:data-services`).
7. `frictions.md` — illustrated FCOS frictions, workarounds and upstream references (`guide:coreos:frictions`).
8. `operations.md` — restore and rescue procedures, update coordination, monitoring and lessons (`guide:coreos:operations`).
