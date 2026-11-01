# Recovery, updates and operating lessons · `guide:coreos:operations`

**Remark (Operating scope)** · `rem:coreos:operations-context`

Operations use the fictional reference-state limits in (`conv:coreos:measurement-scope`) and the monitoring mechanisms in (`sec:coreos:watchdogs`). The estate’s source-of-record recovery model remains (`sec:rootserver:recovery`), (`rule:server:host-is-restore-source`); the procedures here illustrate engine restores, provider rescue and FCOS update recovery.

## Backup rehearsals · `sec:coreos:backup-operations`

**Procedure (Check and repair the backup chain)** · `alg:coreos:backup-repair`

Run restic `check` after every backup and treat failure as an alarm. In the illustrated unclean-VM-shutdown incident, `check` found a corrupted snapshot. `repair index` alone did not repair it; recovery removed the bad snapshot file over SFTP, then ran `check`, `prune` and a fresh backup. Preserve the failed-backup observation before clearing unit failures (`warn:coreos:watchdog-order`).

**Verification (Restore into separate engine instances)** · `verif:coreos:restore-rehearsal`

For each engine, restore the backup-target copy into a separate instance and compare content with checksums, row counts and sums or message counts as applicable. Recorded walls and checks are (`scenario:coreos:restic-rehearsal`), (`scenario:coreos:postgres-pitr`), (`scenario:coreos:datastore-rehearsal`) and (`scenario:coreos:restate-rehearsal`). Those runs used the practice target; a true offsite end-to-end rehearsal still depends on completing (`obs:coreos:backup-deployment-gap`).

**Rule (One restored identity at a time)** · `rule:coreos:restore-identity`

In a disaster rehearsal, stop the original before starting the restored copy. One rehearsal briefly ran both copies with the same identity against the same bucket.

**Observation (Owner secret custody remained planned)** · `obs:coreos:secret-custody-gap`

At the fictional reference state, transferring the repository passphrase and database admin passwords into the owner’s custody through a channel other than chat remains planned, not executed. The on-machine files in (`setup:coreos:restic-setup`) do not complete that recovery-custody step. Choose the offsite passphrase’s recovery location before it is needed.

## Provider rescue · `sec:coreos:rescue-operations`

**Protocol (Rescue procedure)** · `proto:coreos:rescue`

1. Activate rescue in the provider panel with the intended SSH public key selected and verify that confirmation shows it. If activation is password-only, deactivate and reactivate with the key; never paste the rescue password.
2. Trigger the boot, using hardware reset for an unresponsive machine and respecting (`warn:coreos:power-button`).
3. Measure ping and SSH-port reachability at a selected interval, 12 s in the fictional example, against the illustrated threshold (`obs:coreos:reboot-alarm`).
4. Verify the rescue host key against the panel value and log in by key using a dedicated `known_hosts` file. Where the panel supplies no host key, use the recorded hardware identifiers as the limited cross-check in (`alg:coreos:pin-identity`) and pass no secret through that session.
5. For a broken installed system, boot the NVMe in QEMU with `-snapshot` and inspect the serial console.
6. `systemctl reboot` from rescue returns to the installed disk. Rescue activation is consumed by one boot; reactivate it before reboot if another rescue boot is required.

## Update coordination · `sec:coreos:update-operations`

**Scenario (First scheduled update reboot)** · `scenario:coreos:window-reboot`

In the fictional first update window, the kernel changes to the next selected release. `reboot.target` is reached about 60 s after reboot starts and the new boot arrives about 160 s later; the outage is under 4 minutes. Both stacks, all production services and supervised sessions return automatically. One session unit needs its 4 s `Restart=`. A 6-minute URL probe misses the outage, so that probe interval alone does not measure availability through the reboot.

**Procedure (Prepare each update window)** · `alg:coreos:prepare-update`

Run the `testing` and `next` replicas against local workarounds and required host functions (`rule:coreos:deployment-rules`), and use `sesearch` to check whether upstream policy now covers the SSH-session FIFO rule in (`tab:coreos:fcos-frictions`). Schedule consistent data copies and base backups ahead of the window (`setup:coreos:pre-window-maintenance`) and verify automatic service recovery.

**Observation (Loaded startup timeout)** · `obs:coreos:startup-timeout`

In the fictional load scenario, units starting soon after boot need a larger first-start timeout: it rises from 45 s to 150 s within 8 minutes of boot. This is an illustrative adjustment, not a universal timeout.

## Monitoring and lessons · `sec:coreos:monitoring-and-lessons`

**Register (Monitoring inventory)** · `reg:coreos:monitoring`

- Failed units excluding transient healthchecks, restart counts and OnFailure notifications (`req:coreos:failure-notification`).
- Age of successful backup, restic check result and backup-target free space (`setup:coreos:backup-capacity`).
- Production CPU and memory PSI, host memory PSI and each user slice’s `memory.events high` against its ceiling (`setup:coreos:load-watchdog`), (`verif:coreos:ceiling-rehearsal`).
- Disk usage at the fictional 65/80/95% thresholds (`setup:coreos:root-watchdog`).
- Tunnel public-route status and latency, tunnel connections and restart counts (`rule:coreos:tunnel-ingress`).
- SELinux denials since boot with `ausearch --input-logs -m avc -ts boot`, using closed stdin for remote invocation (`warn:coreos:ssh-stdin`).

**Requirement (Actionable alerts)** · `req:coreos:actionable-alerts`

An alert states what is happening, who is consuming the resource and what action is available. Send only owner-actionable conditions to the phone and other notices to the shared file (`setup:coreos:load-watchdog`); do not mistake an unread file alarm for notification (`warn:coreos:watchdog-order`).

**Register (Lessons to carry into the next host)** · `reg:coreos:lessons`

1. Rehearse the initial KVM boot, measure the board reboot and install serial-console arguments before the first physical reboot (`alg:coreos:reboot-rehearsal`).
2. Include overwrite flags and every host-level increment in Butane or first-boot execution so reinstall reproduces the host (`reg:coreos:first-boot-additions`).
3. Use a genuinely offsite target from day one, exclude rebuildable output, monitor free space and rehearse restoration (`obs:coreos:backup-deployment-gap`), (`scenario:coreos:backup-exclusions`).
4. Decide encryption before buying hardware: select suitable UEFI/TPM hardware or record the owner’s explicit deferral (`obs:coreos:hardware`).
5. Compute ceilings from machine fractions, protect the complete MemoryLow chain and isolate heavy builds (`tab:coreos:slice-ceilings`), (`req:coreos:memory-low-chain`), (`scenario:coreos:heavy-slice`).
6. Install OnFailure with backoff before each account’s first service and deliver actionable alarms to a read channel (`listing:coreos:supervision-dropin`), (`req:coreos:actionable-alerts`).
7. Avoid labelled SELinux application ports unless narrowly authorised or containerised; bind services to loopback and guard unauthenticated local APIs by UID (`tab:coreos:fcos-frictions`), (`listing:coreos:loopback-policy`).
8. Use virtio disk/network and a lingering user Quadlet with clean QMP shutdown for replicas (`warn:coreos:replica-limits`), (`scenario:coreos:qmp-shutdown`).
9. Keep reboot-dependent inputs out of `/tmp`, execute transferred script files, and close audit-query stdin (`warn:coreos:temporary-inputs`), (`warn:coreos:ssh-stdin`).
10. Draft upstream reproductions when adding workarounds and re-test on `testing` and `next` before each update window (`rule:coreos:deployment-rules`).
