# Butane installation configuration · `guide:coreos:butane`

Reading order and parent: (`guide:coreos:bare-metal-server-guides`).

**Remark (Listing scope)** · `rem:coreos:butane-scope`

The listing is a fictional installation configuration under (`conv:coreos:measurement-scope`), not a validated deployment artifact. Select actual keys, disk, release and resource limits, then validate with `butane --strict` and rehearse the generated Ignition before installing. It includes the first-login confinement boundary; role-specific service additions and later state are identified in (`reg:coreos:first-boot-additions`), and the fixed ceilings are superseded by (`tab:coreos:slice-ceilings`). Installation order and the overwrite failure are in (`guide:coreos:boot`).

**Listing (Installation Butane)** · `listing:coreos:butane-file`

```yaml
# Fedora CoreOS stable, single NVMe, legacy BIOS boot, no disk encryption.
# Public keys only. Validate with `butane --strict` before generating Ignition.
variant: fcos
version: 1.5.0
passwd:
  users:
    - name: example-admin                 # the single confined administering login
      uid: 41010
      password_hash: "<console password hash supplied only at staging>"
      groups: [wheel, sudo]
      ssh_authorized_keys:
        - <owner public key>
    - name: example-ops                   # unprivileged service account
      uid: 41011
      ssh_authorized_keys:
        - <example-ops public key>
    - name: example-agent-1               # unprivileged automation account: no sudo
      uid: 41013
      ssh_authorized_keys:
        - <agent public key>
storage:
  files:
    - path: /etc/selinux/targeted/active/seusers.local
      overwrite: true
      mode: 0644
      contents:
        inline: |
          __default__:staff_u:s0-s0:c0.c1023
          core:staff_u:s0-s0:c0.c1023
          example-admin:staff_u:s0-s0:c0.c1023
          example-ops:staff_u:s0-s0:c0.c1023
          example-agent-1:staff_u:s0-s0:c0.c1023
    - path: /etc/sudoers.d/zz-admins
      overwrite: true
      mode: 0440
      contents:
        inline: |
          %sudo ALL=(ALL) TYPE=sysadm_t ROLE=sysadm_r NOPASSWD: ALL
    - path: /etc/selinux/local_fixes.cil
      overwrite: true
      mode: 0644
      contents:
        inline: |
          (allow domain sshd_session_t (fifo_file (read write getattr ioctl append)))
    - path: /etc/selinux/staff_spc.cil
      overwrite: true
      mode: 0644
      contents:
        inline: |
          (roletype staff_r spc_t)
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
              udp sport 67 udp dport 68 accept  # DHCPv4 replies where DHCP is selected
              udp sport 547 udp dport 546 accept  # DHCPv6 replies where selected
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
    - name: identity-increment.service
      enabled: true
      contents: |
        [Unit]
        Description=Activate confined identities and reviewed modules before SSH
        DefaultDependencies=no
        After=local-fs.target systemd-tmpfiles-setup.service
        Before=sshd.service
        ConditionPathExists=!/var/lib/identity-increment.stamp
        [Service]
        Type=oneshot
        RemainAfterExit=yes
        ExecStart=/usr/sbin/semodule -i /etc/selinux/local_fixes.cil
        ExecStart=/usr/sbin/semodule -i /etc/selinux/staff_spc.cil
        ExecStart=/usr/sbin/semodule -B
        ExecStart=/usr/sbin/visudo -cf /etc/sudoers.d/zz-admins
        ExecStart=/bin/touch /var/lib/identity-increment.stamp
        [Install]
        RequiredBy=sshd.service
        WantedBy=multi-user.target
```

## Block annotations · `sec:coreos:butane-blocks`

**Setup (Login accounts)** · `setup:coreos:butane-users`

The administering login is `example-admin`, the only declared account in the administrative groups; `example-ops` and `example-agent-1` have no sudo. SSH is key-only for all three. The optional console-password placeholder is filled outside Git, never with a public fixture credential. The replica uses the same role names and admits no key for the image's default `core` account; the explicit `core` mapping still prevents an inherited unconfined mapping. This instantiates (`sec:rootserver:the-account-model`) without a separate owner or unconfined rescue login.

**Setup (Confinement before the first login)** · `setup:coreos:first-boot-identity`

The identity unit installs the reviewed SSH-session FIFO fix and the container-role authorization, rebuilds the login store and validates sudoers before sshd. Its required dependency prevents a failed activation from being treated as a usable SSH setup; the stamp is written only after success. Preserve the independent rescue path while rehearsing this boundary. The FIFO rule addresses the recorded noninteractive-output denial; the other illustrated service and process rules are not copied without a reproduced need (`tab:coreos:fcos-frictions`). A later policy change uses a separately recorded increment and a pinned deployment, not deletion of the first-boot stamp as a substitute for review.

The public listing is a fictional recipe requiring strict translation and replica acceptance, not a claim that these exact bytes were deployed. Compare the configured modules and first-login results with (`reg:rootserver:recorded-fcos-probe-basis`); the recorded deployment establishes the mechanism and the denial, while this recipe's complete acceptance belongs to its next deployment.

**Requirement (Overwrite content-bearing files)** · `req:coreos:overwrite`

Every file supplying content needs `overwrite: true`, including files FCOS already ships such as `/etc/hostname`. The boot failure and correction are recorded in (`scenario:coreos:blind-reboot`); a successful translation alone does not discharge (`verif:coreos:boot-acceptance`).

**Setup (SSH admission)** · `setup:coreos:butane-ssh`

The sshd drop-in disables root, password and keyboard-interactive logins and supplies an explicit `AllowUsers`. The key-only access rationale and acceptance path remain in (`sec:rootserver:access`); the FCOS-specific follow-up is to add each new account to this allow-list or a later drop-in.

**Setup (Periodic updates)** · `setup:coreos:butane-zincati`

The fictional Zincati periodic strategy selects UTC and one Saturday 04:00 window lasting 45 minutes. Select the time zone and schedule for an actual deployment; the example update recovery is (`scenario:coreos:window-reboot`).

**Setup (Input firewall)** · `setup:coreos:butane-firewall`

The nftables input policy drops traffic except established/related traffic, loopback, ICMP, selected DHCP replies and SSH. firewalld remains inactive. Because the configuration begins with `flush ruleset`, additional tables must be included from this file to survive `nftables.service` reload (`req:coreos:guard-persistence`).

**Observation (Initial aggregate ceiling)** · `obs:coreos:initial-ceiling`

The initial fictional `user.slice` ceiling in the listing is `MemoryHigh=32G`, `MemoryMax=48G` and `CPUQuota=800%`. On the 24-thread example machine, the quota limits a session to eight CPU equivalents. Later ceiling changes are recorded separately in (`scenario:coreos:aggregate-pressure`) and (`tab:coreos:slice-ceilings`).

**Setup (Production protection)** · `setup:coreos:butane-production`

`production.slice` gives the fictional production workload `MemoryLow=12G` and `CPUWeight=300`; production Quadlets select `Slice=production.slice`. MemoryLow protects against reclaim and CPUWeight favours production under contention. Protection across nested user slices requires the complete parent chain (`req:coreos:memory-low-chain`).

**Setup (Linger and firewall activation)** · `setup:coreos:butane-linger`

The empty `/var/lib/systemd/linger/example-agent-1` file enables that account’s user manager without login. The `systemd.units` entry enables `nftables.service`. Other account managers are added in (`sec:coreos:user-managers`).

**Register (Reinstall completeness additions)** · `reg:coreos:first-boot-additions`

- Add `/etc/systemd/resolved.conf.d/10-no-llmnr.conf` with `[Resolve]` and `LLMNR=no` (`alg:coreos:disable-llmnr`).
- Add the `multi-user.target.wants` entry pulling in `network-online.target` (`tab:coreos:fcos-frictions`).
- Preserve the login store, sudoers, SSH FIFO fix, container-role module and identity unit from (`setup:coreos:first-boot-identity`); later identity increments keep that same boundary (`listing:coreos:identity-increment`).
- Declare the required package layer and its system-context first-boot unit before Zincati, checking the live and staged deployment states separately (`obs:coreos:python-layering`).
- Declare loop accounts from the registry with home-local hubs and workspaces at mode 0750, private temporary roots and lingering managers; a compute-only role omits production services, backups and an application tunnel with the omission recorded (`sec:rootserver:the-door`).
- Fold the revised ceilings and other host-level increments into Butane or a first-boot unit so reinstalling reproduces the post-install state (`tab:coreos:slice-ceilings`).

**Listing (Translation and installation)** · `listing:coreos:install-command`

```
butane --strict host.bu > host.ign
coreos-installer install /dev/disk/by-id/nvme-EXAMPLE_SYSTEM_DISK --ignition-file host.ign \
  --append-karg console=ttyS0,115200n8 --append-karg console=tty0
```

**Observation (Installation result)** · `obs:coreos:installation-result`

The example acceptance result has a passing Fedora GPG signature check, SSH returning at 160 s after the physical reboot, the system `running` with zero failed units, SELinux enforcing and nftables, sshd and Zincati active. These are fictional results under (`conv:coreos:measurement-scope`), not a substitute for an actual host’s acceptance probes.
