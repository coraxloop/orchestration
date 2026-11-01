# Butane installation configuration · `guide:coreos:butane`

**Remark (Listing scope)** · `rem:coreos:butane-scope`

The listing is a fictional installation configuration under (`conv:coreos:measurement-scope`), not a validated deployment artifact. Select actual keys, disk, release and resource limits, then validate with `butane --strict` and rehearse the generated Ignition before installing. It is the example baseline, not the complete later state: subsequent additions are identified in (`reg:coreos:first-boot-additions`), and the fixed ceilings are superseded by (`tab:coreos:slice-ceilings`). Installation order and the overwrite failure are in (`guide:coreos:boot`).

**Listing (Installation Butane)** · `listing:coreos:butane-file`

```yaml
# Fedora CoreOS stable, single NVMe, legacy BIOS boot, no disk encryption.
# Public keys only. Validate with `butane --strict` before generating Ignition.
variant: fcos
version: 1.5.0
passwd:
  users:
    - name: example-admin                 # the owner: wheel + sudo
      uid: 41010
      groups: [wheel, sudo]
      ssh_authorized_keys:
        - <owner public key>
    - name: example-ops                   # operations account: wheel + sudo
      uid: 41011
      groups: [wheel, sudo]
      ssh_authorized_keys:
        - <example-ops public key>
    - name: example-agent-1               # unprivileged automation account: no sudo
      uid: 41013
      ssh_authorized_keys:
        - <agent public key>
storage:
  files:
    - path: /etc/hostname
      overwrite: true             # REQUIRED: without it Ignition fails at boot (rehearsed overwrite failure)
      mode: 0644
      contents:
        inline: example-node.example.invalid
    - path: /etc/ssh/sshd_config.d/10-local.conf
      overwrite: true
      mode: 0600
      contents:
        inline: |
          PermitRootLogin no
          PasswordAuthentication no
          KbdInteractiveAuthentication no
          AllowUsers example-admin example-ops example-agent-1
    - path: /etc/zincati/config.d/55-updates-strategy.toml
      overwrite: true
      mode: 0644
      contents:
        inline: |
          [updates]
          strategy = "periodic"
          [updates.periodic]
          time_zone = "UTC"
          [[updates.periodic.window]]
          days = ["Sat"]
          start_time = "04:00"
          length_minutes = 45
    - path: /etc/sysconfig/nftables.conf
      overwrite: true
      mode: 0600
      contents:
        inline: |
          flush ruleset
          table inet host {
            chain input {
              type filter hook input priority 0; policy drop;
              ct state established,related accept
              iif lo accept
              meta l4proto { icmp, ipv6-icmp } accept
              tcp dport 22 accept
            }
          }
    - path: /etc/systemd/system/user.slice.d/10-staff-ceiling.conf
      overwrite: true
      mode: 0644
      contents:
        inline: |
          # aggregate ceiling for every login account (example-dev, staging, agents)
          [Slice]
          MemoryHigh=32G
          MemoryMax=48G
          CPUQuota=800%
    - path: /etc/systemd/system/production.slice
      overwrite: true
      mode: 0644
      contents:
        inline: |
          [Unit]
          Description=Production services
          [Slice]
          MemoryLow=12G
          CPUWeight=300
    - path: /var/lib/systemd/linger/example-agent-1   # linger: the user manager runs without a login
      mode: 0644
systemd:
  units:
    - name: nftables.service
      enabled: true
```

## Block annotations · `sec:coreos:butane-blocks`

**Setup (Login accounts)** · `setup:coreos:butane-users`

`passwd.users` declares three key-only accounts: `example-admin` and `example-ops` in `wheel` and `sudo`, and `example-agent-1` in neither. The replica has these same accounts and no `core` account. Hours were once lost trying to log in to a replica as `core`; replicas use the declared role names. This differs from the account roster in (`sec:rootserver:the-account-model`).

**Requirement (Overwrite content-bearing files)** · `req:coreos:overwrite`

Every file supplying content needs `overwrite: true`, including files FCOS already ships such as `/etc/hostname`. The boot failure and correction are recorded in (`scenario:coreos:blind-reboot`); a successful translation alone does not discharge (`verif:coreos:boot-acceptance`).

**Setup (SSH admission)** · `setup:coreos:butane-ssh`

The sshd drop-in disables root, password and keyboard-interactive logins and supplies an explicit `AllowUsers`. The key-only access rationale and acceptance path remain in (`sec:rootserver:access`); the FCOS-specific follow-up is to add each new account to this allow-list or a later drop-in.

**Setup (Periodic updates)** · `setup:coreos:butane-zincati`

The fictional Zincati periodic strategy selects UTC and one Saturday 04:00 window lasting 45 minutes. Select the time zone and schedule for an actual deployment; the example update recovery is (`scenario:coreos:window-reboot`).

**Setup (Input firewall)** · `setup:coreos:butane-firewall`

The nftables input policy drops traffic except established/related traffic, loopback, ICMP and SSH. firewalld remains inactive. Because the configuration begins with `flush ruleset`, additional tables must be included from this file to survive `nftables.service` reload (`req:coreos:guard-persistence`).

**Observation (Initial aggregate ceiling)** · `obs:coreos:initial-ceiling`

The initial fictional `user.slice` ceiling in the listing is `MemoryHigh=32G`, `MemoryMax=48G` and `CPUQuota=800%`. On the 24-thread example machine, the quota limits a session to eight CPU equivalents. Later ceiling changes are recorded separately in (`scenario:coreos:aggregate-pressure`) and (`tab:coreos:slice-ceilings`).

**Setup (Production protection)** · `setup:coreos:butane-production`

`production.slice` gives the fictional production workload `MemoryLow=12G` and `CPUWeight=300`; production Quadlets select `Slice=production.slice`. MemoryLow protects against reclaim and CPUWeight favours production under contention. Protection across nested user slices requires the complete parent chain (`req:coreos:memory-low-chain`).

**Setup (Linger and firewall activation)** · `setup:coreos:butane-linger`

The empty `/var/lib/systemd/linger/example-agent-1` file enables that account’s user manager without login. The `systemd.units` entry enables `nftables.service`. Other account managers are added in (`sec:coreos:user-managers`).

**Register (Reinstall completeness additions)** · `reg:coreos:first-boot-additions`

- Add `/etc/systemd/resolved.conf.d/10-no-llmnr.conf` with `[Resolve]` and `LLMNR=no` (`alg:coreos:disable-llmnr`).
- Add the `multi-user.target.wants` entry pulling in `network-online.target` (`tab:coreos:fcos-frictions`).
- Preserve `seusers.local`, sudoers and the complete local CIL module; activate the policy through a first-boot script because it requires `semodule` at runtime (`listing:coreos:identity-increment`).
- Fold the revised ceilings and other host-level increments into Butane or a first-boot unit so reinstalling reproduces the post-install state (`tab:coreos:slice-ceilings`).

**Listing (Translation and installation)** · `listing:coreos:install-command`

```
butane --strict host.bu > host.ign
coreos-installer install /dev/disk/by-id/nvme-EXAMPLE_SYSTEM_DISK --ignition-file host.ign \
  --append-karg console=ttyS0,115200n8 --append-karg console=tty0
```

**Observation (Installation result)** · `obs:coreos:installation-result`

The example acceptance result has a passing Fedora GPG signature check, SSH returning at 160 s after the physical reboot, the system `running` with zero failed units, SELinux enforcing and nftables, sshd and Zincati active. These are fictional results under (`conv:coreos:measurement-scope`), not a substitute for an actual host’s acceptance probes.
