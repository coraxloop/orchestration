# Post-install identities and host services · `guide:coreos:increments`

**Requirement (Increment contract)** · `req:coreos:increment-contract`

Each increment is a small idempotent shell script kept in git, with a header naming its running account, prerequisites and undo path. Apply it to the replica first, including a reboot, and then to the host. Copy it to a file and execute the file; the illustrated stdin failure is (`warn:coreos:ssh-stdin`). Preserve inputs across reboot on disk (`rule:server:disk-backed-workspace`), (`warn:coreos:temporary-inputs`). The evidence standard is (`req:server:idempotent-bootstrap`).

**Register (Increment order)** · `reg:coreos:increment-order`

1. Identities and SELinux (`sec:coreos:identities`).
2. Workspaces (`sec:coreos:workspaces`).
3. Restic backups (`sec:coreos:backups`).
4. PostgreSQL archiving and recovery (`sec:coreos:postgres`).
5. Object storage and analytics (`sec:coreos:datastores`).
6. NATS and Restate (`sec:coreos:messaging`).
7. Lingering user managers (`sec:coreos:user-managers`).
8. Slices and ceilings (`sec:coreos:ceilings`).
9. Unit supervision (`sec:coreos:supervision`).
10. Loopback guard (`sec:coreos:loopback`).
11. LLMNR off (`sec:coreos:llmnr`).
12. Update-window coordination (`sec:coreos:update-increment`).
13. Outbound tunnel (`sec:coreos:tunnel`).
14. KVM replica (`sec:coreos:replica`).
15. Watchdogs (`sec:coreos:watchdogs`).

## Identities and SELinux · `sec:coreos:identities`

**Remark (FCOS policy tooling difference)** · `rem:coreos:identity-tooling`

The administrative transition follows (`sec:rootserver:administering-under-confinement`); the reference FCOS image lacked `semanage`, so the local login store was edited and rebuilt with `semodule -B`. The listing records the first increment and its local policy workarounds, whose illustrated causes are in (`tab:coreos:fcos-frictions`). The estate’s rollback prerequisite remains (`sec:confinedadmin:pin-a-rollback-before-lock-out-class-surgery`).

**Listing (First identity increment)** · `listing:coreos:identity-increment`

```bash
LOCAL=/etc/selinux/targeted/active/seusers.local
for u in example-admin example-ops example-agent-1; do
  grep -q "^$u:" "$LOCAL" 2>/dev/null || echo "$u:staff_u:s0-s0:c0.c1023" >> "$LOCAL"
done
semodule -B

# admins elevate with an explicit role/type transition (the zz- prefix sorts after the distro file)
echo '%sudo ALL=(ALL) TYPE=sysadm_t ROLE=sysadm_r NOPASSWD: ALL' > /etc/sudoers.d/zz-admins
chmod 0440 /etc/sudoers.d/zz-admins && visudo -cf /etc/sudoers.d/zz-admins

# local CIL module (rules correspond to the illustrated FCOS frictions)
cat > /etc/selinux/local_fixes.cil <<'CIL'
(allow domain sshd_session_t (fifo_file (read write getattr ioctl append)))
(allow staff_sudo_t sysadm_t (process (getpgid)))
(allow staff_t user_tmp_t (service (start stop status reload)))
CIL
semodule -i /etc/selinux/local_fixes.cil

# rootless Quadlets wait 90 s for this target unless something pulls it in
systemctl add-wants multi-user.target network-online.target

# data layout, closed to staff accounts
install -d -m 0751 /var/lib/example               # 0751: workers can traverse to workspaces/ without listing
install -d -m 0750 /var/lib/example/prod /var/lib/example/releases
install -d -m 0755 /var/lib/example/workspaces
loginctl enable-linger example-ops
```

**Scenario (Identity acceptance after reboot)** · `scenario:coreos:identity-rehearsal`

In the fictional replica rehearsal the script takes 20 s, including a 15 s policy rebuild; reboot takes 30–40 s. Afterwards all accounts are `staff_u:staff_r:staff_t`, sudo reaches `sysadm_t` with output preserved over non-interactive SSH, and the agent has no sudo and receives `Permission denied` on `prod/`. A user Quadlet starts automatically after reboot under `staff_t` with its container in `container_t`. The example physical-host reboot takes 155 s and has zero SELinux denials since boot.

**Warning (Policy module replacement)** · `warn:coreos:module-replacement`

The module later gained the rpm-ostree connection rule and `name_bind` rules for two labelled development-backend port types. `semodule -i` replaces a module by name: reinstall the whole module, not only newly added rules (`tab:coreos:fcos-frictions`).

## Workspaces · `sec:coreos:workspaces`

**Setup (Shared workspace layout)** · `setup:coreos:workspace-layout`

The reference layout used root-only mode 0750 `prod` and `releases` below `/var/lib/example`, a mode 0751 parent allowing traversal without listing, and mode 0755 `workspaces`. Each `/var/lib/example/workspaces/<project>` used a shared group, setgid and a default ACL. Without that ACL, illustrated new files were 0644 and another group member could not write them. A shared clone also needed a `safe.directory` entry in each participating account’s global Git configuration to avoid dubious-ownership rejection.

**Warning (Owning a var_lib_t directory does not make it writable)** · `warn:coreos:workspace-labels`

`staff_t` could not write a `var_lib_t` directory even when the account owned it. The FCOS workaround assigned `user_home_t` persistently to worker workspaces by adding a local file-context entry, running `semodule -B` and then `restorecon`. The estate instead keeps loop data in homes (`sec:confinedadmin:the-filesystem-is-typed-loop-data-lives-in-homes`); this shared-project layout does not replace per-loop isolation (`inv:server:per-loop-isolation`).

## User managers · `sec:coreos:user-managers`

**Setup (Unprivileged account provisioning)** · `setup:coreos:user-provisioning`

Each agent, development and pilot-worker account receives `staff_u`, no sudo, separate subordinate UID/GID ranges, linger and a per-user slice ceiling inside the aggregate. The shared confinement model is (`sec:rootserver:the-account-model`); account-local service management and labels have additional illustrated FCOS constraints below.

**Observation (Pilot account acceptance)** · `obs:coreos:pilot-acceptance`

The fictional pilot worker reports `staff_t`, sudo requires a password, and access to `prod/` and other homes is denied. It can write its workspace and mount it in a container. A rootless container starts in 6 s including its image pull; its `CPUQuota=400%` permits four CPU equivalents. Replica reboot takes 25 s with zero AVC denials.

**Listing (Manage a user unit as its user)** · `listing:coreos:user-manager-command`

```
sudo -u <account> env XDG_RUNTIME_DIR=/run/user/<uid> \
  DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/<uid>/bus systemctl --user <verb> <unit>
```

**Warning (Cross-account manager access)** · `warn:coreos:manager-access`

Only (`listing:coreos:user-manager-command`) worked in the illustrated setup. `sudo -iu <account> systemctl --user` lacked a session bus; `systemctl --machine=<account>@.host --user` returned “Transport endpoint is not connected”. From `sysadm_t`, `list-unit-files`, `is-enabled` and `systemd-run` returned “Access denied”, while `show`, `start`, `stop`, `enable`, `list-units` and `daemon-reload` worked. Query the manager as its own user; to attach to another account’s tmux, use `machinectl shell <account>@`.

**Warning (User unit file labels)** · `warn:coreos:user-unit-labels`

Files written with `tee` into `~/.config/systemd/user` acquired `config_home_t`; the confined user could not relabel them and received “Access denied”. Run `restorecon` as root after writing those files.

## Slices and ceilings · `sec:coreos:ceilings`

**Scenario (Aggregate pressure before fractional ceilings)** · `scenario:coreos:aggregate-pressure`

In the fictional pressure scenario, a later fixed-ceiling configuration allows `user.slice` to reach 92 GiB on the 96 GiB machine without swap. A 90 GiB peak leaves insufficient headroom and the host stalls. The replacement script computes ceilings as fractions of capacity so it applies to both a 12 GiB replica and the physical host (`tab:coreos:slice-ceilings`). It is idempotent and applies live with `daemon-reload`, without reboot. The initial Butane values are preserved separately in (`obs:coreos:initial-ceiling`).

**Table (Revised reference ceilings)** · `tab:coreos:slice-ceilings`

|Slice|MemoryHigh / MemoryMax|CPUQuota|Notes|
|-----|----------------------|--------|-----|
|`user.slice` (aggregate)|60 % / 70 % of RAM|50 % of threads|leaves room for `production.slice` (`MemoryLow` 12G) and the kernel|
|heaviest example-dev account|40 % / 50 %|25 %|inner `MemoryLow` sized to its example stack|
|account running the KVM replicas|15 % / 20 %|10 %||
|other agent accounts|fixed, small (e.g. 4/6 GiB, 200 % CPU)|||

**Requirement (MemoryLow across the parent chain)** · `req:coreos:memory-low-chain`

Protection requires `MemoryLow` through `user.slice`, `user-<uid>.slice`, `user@<uid>.service` and the inner slice. A child’s low is capped by its parent; an isolated leaf value cannot supply the intended protection.

**Scenario (Build pressure isolated from a development stack)** · `scenario:coreos:heavy-slice`

In the fictional build-pressure scenario, a development backend stops responding for 45 minutes while compilers hold the shared slice at `MemoryHigh`: allocations force every process in the slice into reclaim. A dedicated inner `heavy.slice` with high 12 GiB, max 16 GiB and a one-heavy-job lock isolates that load. An oversized build then fails visibly with OOM inside its own slice instead of freezing the whole stack.

**Verification (Ceiling red and green rehearsal)** · `verif:coreos:ceiling-rehearsal`

On the replica, run N memory hogs in one account and compare host PSI, that slice’s `memory.events high` and another account’s login latency before and after the ceiling change. Require the intended failing case before and the intended protected case after; no numerical latency result is supplied for this check.

## Unit supervision · `sec:coreos:supervision`

**Observation (Invisible tunnel restart loop)** · `obs:coreos:tunnel-restart-loop`

In the fictional failure scenario, a tunnel unit restarts 600 times in 2 hours without connecting and without being noticed. Restart policy alone does not make the failure visible.

**Listing (User service failure and backoff drop-in)** · `listing:coreos:supervision-dropin`

The per-account file `~/.config/systemd/user/service.d/10-notify.conf` reaches every user service without root.

```ini
[Unit]
OnFailure=notify-failure@%n.service
StartLimitIntervalSec=0
[Service]
RestartSteps=8
RestartMaxDelaySec=240
```

**Requirement (Bounded non-recursive notification)** · `req:coreos:failure-notification`

`notify-failure@.service` writes one JSON line with time, account, unit, result and restart count to a state file and journals at `err` priority. It writes at most one line per unit per 10 minutes and only counts between notifications, and never copies potentially secret-bearing log lines. A same-named drop-in under `notify-failure@.service.d/` clears `OnFailure=` so the notifier cannot trigger itself.

**Scenario (Backoff preserves retries)** · `scenario:coreos:backoff`

In the fictional retry scenario, a start limit of 8 starts in 8 minutes with `RestartSec=4` leaves a repeatedly crashing unit failed within a minute; on a tunnel that would end recovery after a longer network outage. Increasing backoff replaces the start limit. With `RestartMode=normal`, `OnFailure` fires on every crash even when `Restart=` schedules another attempt.

**Verification (Failure notifier self-test)** · `verif:coreos:notifier-self-test`

A deliberately failing unit must produce exactly one notification in 40 s, keep retrying and spread its retries: 2–12 restarts rather than about 40. This check covers both visibility and continued recovery attempts.

**Precondition (Supervisor pre-mortem)** · `pre:coreos:supervisor-premortem`

Before installing a unit that runs agents, workers or builds whose processes it does not own, record inherited environment, `NOTIFY_SOCKET`, descriptors and cgroup; what a child can do with them; and behaviour at boot, clean exit, `kill -9`, requested stop and network loss.

**Scenario (Child notification inheritance)** · `scenario:coreos:notify-inheritance`

In the fictional supervision scenario, repeated crashes of a supervised session are traced to `NotifyAccess=all` with an inherited `NOTIFY_SOCKET`. The repair uses `NotifyAccess=main` and a real supervisor process, addressing the inheritance identified by (`pre:coreos:supervisor-premortem`).

## Loopback guard · `sec:coreos:loopback`

**Scenario (Unauthenticated local API isolation)** · `scenario:coreos:loopback-isolation`

An unprivileged account reached an unauthenticated durable-execution admin endpoint on loopback. The fix was an nftables output hook restricting the unauthenticated admin, ingress and message-bus ports to allowed socket UIDs. Afterward root and example-ops received HTTP 200 and other accounts could not connect; the table survived an nftables service reload. Services with their own passwords or keys were not in this guard.

**Listing (Loopback UID policy)** · `listing:coreos:loopback-policy`

```
table inet loopback-guard {
  set no_auth { type inet_service; elements = { <port>, <port>, ... } }
  set allowed { type uid; elements = { 0, 41011 } }
  chain out {
    type filter hook output priority filter; policy accept;
    # the original used two rules: IPv4 loopback /8 and ::1 as destination
    oifname "lo" tcp dport @no_auth meta skuid != @allowed counter reject with tcp reset
  }
}
```

**Requirement (Guard survives reload)** · `req:coreos:guard-persistence`

Store the guard under `/etc/nftables.d/` and include it from `/etc/sysconfig/nftables.conf`. Reload reads that complete file, whose `flush ruleset` discards separately loaded tables; a one-time successful load is insufficient.

## Disable LLMNR · `sec:coreos:llmnr`

**Observation (LLMNR listening surface)** · `obs:coreos:llmnr-listeners`

`ss` showed systemd-resolved listening on 5355 for TCP and UDP over IPv4 and IPv6 on all interfaces. The input firewall already blocked external access; disabling LLMNR removed the listeners themselves.

**Procedure (Disable and verify LLMNR)** · `alg:coreos:disable-llmnr`

Write `[Resolve]` and `LLMNR=no` into `/etc/systemd/resolved.conf.d/10-no-llmnr.conf`, run `restorecon`, restart systemd-resolved, verify that nothing listens on 5355 and that `getent hosts <public name>` still resolves. Delete the drop-in to undo it. Preserve the setting in Butane (`reg:coreos:first-boot-additions`).

## Coordinate the update window · `sec:coreos:update-increment`

**Setup (Pre-window maintenance)** · `setup:coreos:pre-window-maintenance`

The fictional Butane window is (`setup:coreos:butane-zincati`). The example schedule places the stopped-service copy at 02:00 and the database base backup at 02:15 UTC, ahead of the 04:00 window. Coordinate long-running jobs with that window and make services return without manual login (`scenario:coreos:window-reboot`).

## Outbound application tunnel · `sec:coreos:tunnel`

**Setup (Loopback services and outbound access)** · `setup:coreos:outbound-tunnel`

Only SSH on 22 was reachable from outside; application services bound to loopback. Public webhooks and staging web access used an outbound `cloudflared` tunnel as an unprivileged user unit, with an access gateway in front of web UIs. This is distinct from the estate WireGuard door (`sec:rootserver:the-door`).

**Rule (Review tunnel ingress and restarts)** · `rule:coreos:tunnel-ingress`

Keep ingress rules in the repository and compare them with the provider panel: the reference setup found one stale panel rule. Apply (`req:coreos:failure-notification`) and inspect restart counts; an externally plausible tunnel state did not reveal the restart loop (`obs:coreos:tunnel-restart-loop`).

## Persistent rehearsal replica · `sec:coreos:replica`

**Setup (Replica container and access)** · `setup:coreos:replica-setup`

The fictional example-ops account runs the replica inside rootless Podman with `/dev/kvm` passed through, as a lingering user Quadlet. It uses the same FCOS metal image and Butane file on a 24 GB virtual disk; illustrative installation takes 45 s. Guest SSH is published only on host loopback and reached using ProxyJump through example-admin. Files move with `scp`; the replica shares no disk with the host. On-demand `testing` and `next` replicas use qcow2 images and Ignition through `fw_cfg`.

**Warning (Replica fidelity limits)** · `warn:coreos:replica-limits`

An emulated NVMe disk can fail to boot under the selected QEMU version without console output, so the fictional replica uses virtio. The scenario includes an emulated NIC hanging after an in-guest reboot with “Detected Tx Unit Hang”; restart through the replica unit, budget 35 s in this example, and prefer virtio-net. QEMU user networking does not reproduce the provider network or board POST time. A 12 GiB, 4-vCPU replica cannot run the example’s large build; size rehearsals for their workload.

**Scenario (Clean QMP shutdown)** · `scenario:coreos:qmp-shutdown`

In the fictional backup scenario, a hard-killed VM holding a backup target corrupts a restic snapshot. `ExecStop` is changed to send QMP `system_powerdown` and wait up to 120 s. The first wait uses unavailable `pgrep` and exits immediately; the second breaks the QMP request through shell quoting; the third moves the request into a small script and shuts down cleanly in 3 s.

## Watchdogs · `sec:coreos:watchdogs`

**Setup (Root state watchdog)** · `setup:coreos:root-watchdog`

A fictional root timer every 12 minutes checks failed units, timers, last successful backup age against 50 minutes, disk thresholds 65/80/95%, memory, production health and backup-target free space. It writes the result into a state JSON file; backup-target-specific thresholds are (`setup:coreos:backup-capacity`).

**Setup (Owner-action load watchdog)** · `setup:coreos:load-watchdog`

A fictional user watchdog every 4 minutes reads that state and PSI. It sends phone alerts for production CPU `some avg10 > 8%`, production memory `full avg10 > 8%`, host memory pressure above 25% unless one account is contending only with itself inside its own ceiling, or a new state-file alarm. It sends one alert on onset and one each 20 minutes while persistent, and “recovered” only after an alert has been sent. Other notices go to a shared file for sessions to read.

**Warning (Preserve alarms before clearing failures)** · `warn:coreos:watchdog-order`

Exclude Podman transient healthcheck units by name: the example has startup failures that cause false alarms. Run the watchdog before `reset-failed`; clearing failures first can produce “all fine” despite a failed backup. In the fictional incident a backup target hangs for 8 hours while its alarm remains unread in a file, motivating the phone channel. An unread record is not an effective alert.
