# Illustrated FCOS frictions and workarounds · `guide:coreos:frictions`

**Observation (Reproduction scope)** · `obs:coreos:friction-scope`

The six failure mechanisms below are carried into the fictional example under (`conv:coreos:measurement-scope`). Public software versions and upstream issue references identify technical context, not a deployed node: the source cases span Podman 5.8.4–6.1.1 and selinux-policy 44.6. Upstream status is the recorded source observation, not a present-day issue-status claim. Reproduce the cases on the selected stable, `testing` and `next` releases and re-test local rules before each window (`rule:coreos:deployment-rules`).

**Table (Six FCOS frictions)** · `tab:coreos:fcos-frictions`

|Case|Friction|Streams|Workaround used|
|----|--------|-------|---------------|
|1|`sudo` over non-interactive SSH loses all output for `staff_u` users (exit 0, nothing printed). The SSH session pipes are labelled `sshd_session_t` (from the OpenSSH 10 `sshd-session` split), and the domains reached through sudo (`staff_sudo_t`, `sysadm_t`, `journalctl_t`, `load_policy_t`, `setfiles_t`) may not read or write them. The policy has the equivalent rule for the older `sshd_t`|stable, testing, next; not found upstream at the time|`(allow domain sshd_session_t (fifo_file (read write getattr ioctl append)))`. It mirrors the distro's `sshd_t` rule without `lock`. Re-check after each update with `sesearch` and drop it once upstream ships the fix. Alternatives: list the domains explicitly, or always use `ssh -tt`|
|2|A `staff_t` user cannot start or query its own Quadlet-generated units (generated into `/run/user/<uid>/systemd/generator/`, labelled `user_tmp_t`): "Access denied"|all three; known upstream: https://github.com/containers/podman/issues/24693|`(allow staff_t user_tmp_t (service (start stop status reload)))`. `podman run` and `systemd-run --user` work without it|
|3|The first start of any rootless Quadlet waits 90 s. `podman-user-wait-network-online.service` waits for the system `network-online.target`, which nothing pulls in on a default install. This is independent of SELinux: an unconfined control account hung the same way|all three; known upstream: https://github.com/containers/podman/issues/24796 and https://github.com/containers/podman/issues/24637|`systemctl add-wants multi-user.target network-online.target`; the Quadlet then starts in under 1 s|
|4|`rpm-ostree install` from `sysadm_t` fails: "Failed to connect to client transaction: Permission denied" (`connectto` on `install_t`)|stable|`(allow sysadm_t install_t (unix_stream_socket (connectto)))`, or `sudo -r unconfined_r -t unconfined_t rpm-ostree ...`|
|5|On shutdown, the `staff_t` user manager cannot signal the rootless network helper (`pasta_t`): `denied { signal sigkill }`. The container itself stops cleanly|stable|none needed so far; the helper dies with the session|
|6|`staff_t` cannot bind ports that carry their own label (illustrated denied: 3000, 3001, 8080, 8081, 9080, 9090, 9100; allowed: unlabelled ports such as 3002, 8300, 9081, 50051)|stable|either a narrow `name_bind` rule per port type, unreserved ports, or running the process in a container (`container_t`)|

**Remark (Estate rpm-ostree route differs)** · `rem:coreos:rpm-ostree-difference`

The table records the FCOS `connectto` allow rule and explicit unconfined invocation as illustrated alternatives. The estate recipe instead runs rpm-ostree through a system-context transient unit (`sec:confinedadmin:rpm-ostree-the-daemon-refuses-confined-dbus`). A historical workaround here does not broaden that estate administration path.

## Other illustrated traps · `sec:coreos:other-gotchas`

**Hint (Missing policy utilities)** · `hint:coreos:policy-utilities`

FCOS had neither `semanage` nor `setools`. Edit the local login and file-context stores and rebuild with `semodule -B` for the illustrated FCOS path; query policy with containerised setools against a copy of `/etc/selinux/targeted/policy/policy.*`. Workspace placement differs from the estate home-local recipe (`warn:coreos:workspace-labels`).

**Observation (Python layering)** · `obs:coreos:python-layering`

The fictional base image lacks Python. Small tools use bash and jq until python3 is needed; the example layers it and reboots. That layer-and-reboot practice differs from the estate’s illustrated apply-live route (`sec:confinedadmin:rpm-ostree-the-daemon-refuses-confined-dbus`).

**Warning (Temporary inputs disappear)** · `warn:coreos:temporary-inputs`

A replica reboot emptied `/tmp`, breaking increments that expected their inputs there. The repair copied inputs once into `/etc/example/sources/` and read them there. Disk-backed work is already required by (`rule:server:disk-backed-workspace`); this failure additionally demonstrates why a reboot-dependent input needs persistent placement.

**Warning (Relabelling shared trees and symlinks)** · `warn:coreos:volume-relabel`

`:Z` privately relabelled a shared clone, blocking another container or account with `lsetxattr operation not permitted`; it also relabelled a build tree while another container used it. `:z` did not follow the `releases/current` symlink, leaving its target `var_lib_t` and unreadable by a root container. Mount the real directory and account for shared use before choosing a private relabel.

**Warning (Rootful pasta networking)** · `warn:coreos:rootful-pasta`

Podman 5.8.7 rejected rootful pasta with “pasta networking is only supported for rootless mode”. The illustrated workaround used `Network=host` and made each service read its bind address from its environment to avoid stack collisions.

**Warning (Backup transport port label)** · `warn:coreos:backup-port-label`

Port 23 was `telnetd_port_t`; host-shell SSH to the backup box on that port was denied for `ssh_t`. The containerised backup was unaffected. Test its connectivity from that container with `--entrypoint ssh`, not only from the host shell.

**Warning (Non-interactive SSH input consumption)** · `warn:coreos:ssh-stdin`

`ausearch` without `--input-logs` reads stdin and can hang a remote test and its local SSH process. Use `ausearch --input-logs` with `</dev/null`. A first sudo on a remote line can also consume a script intended for a subsequent `sudo bash -s`; copy and execute a script file instead.

**Hint (Jump-host keys and login prompts)** · `hint:coreos:ssh-jump`

Command-line `-J` did not propagate `-i` to the jump host. Give the jump alias its own `IdentityFile` in SSH configuration and use `ProxyJump`, consistent with (`rule:server:alias-only-addressing`). Wait for the login prompt before pasting a command: a line sent before the prompt was lost to the login banner.

**Warning (Replica reboot path)** · `warn:coreos:replica-reboot`

Reboot replicas through their user unit, never by an in-guest reboot, because of the e1000 NIC hang in (`warn:coreos:replica-limits`). Prefer virtio disk and network and a QMP shutdown (`scenario:coreos:qmp-shutdown`).
