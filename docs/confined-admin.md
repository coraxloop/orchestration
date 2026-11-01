# Administering a confined SELinux server · `guide:confinedadmin:confined-selinux-administration`

Everything here was measured during the 2026-08-28 bootstrap of a reference root-capable confined deployment running Fedora Silverblue 44, with SELinux enforcing and every account mapped to `staff_u` except the human rescue account. The account model this serves is [root-server-account-model.md](proposals/root-server-account-model.md); the argued case for the overall posture — what the platform's defaults provide, which surface the universal confinement moves, and why few deliberate actions carry it — is [security-posture.md](security-posture.md); the container-policy evidence is the [archived bug report](reference/bugreport-staff_t-container_t.md). Each section states the failure as observed, the cause, and the working recipe.

## Root is not admin: the sudo domain transition · `sec:confinedadmin:root-is-not-admin-the-sudo-domain-transition`

Under a confined login, `sudo` grants uid 0 but keeps the process in the confined domain, and `staff_t` — root or not — cannot write `/etc`: the initial drop-in attempt failed with `tee: /etc/sudoers.d/...: Permission denied` under a successful sudo. Administrative capability is the *domain*, not the uid. The working sudoers form bakes the transition in, so every privileged act lands in `sysadm_t` and is recorded as an explicit transition; `ACCOUNT` stands for the confined administrator account:

```
ACCOUNT ALL=(ALL) ROLE=sysadm_r TYPE=sysadm_t NOPASSWD: ALL
```

Installing that first drop-in is a chicken-and-egg: it must be written by an unconfined actor (the rescue account) or by requesting the transition explicitly — `sudo -r sysadm_r -t sysadm_t tee ...` — which is the designed staff-to-sysadm path and worked live.

## rpm-ostree: the daemon refuses confined DBus · `sec:confinedadmin:rpm-ostree-the-daemon-refuses-confined-dbus`

`rpm-ostree` calls from a `sysadm_t` sudo fail with `Failed to connect to client transaction: Permission denied` — the daemon rejects the confined client. Route every call through a system-context transient unit:

```
sudo systemd-run --wait --pipe --collect -- rpm-ostree install --idempotent <pkgs>
```

Two further edges, both measured: inline `install --apply-live` fails even via the transient unit, while staging first and then running a bare `rpm-ostree apply-live` succeeds (1.8 s, no reboot); and a package already provided by the base image fails the *entire* batch (`--idempotent` does not cover it) — exclude it or pass `--allow-inactive`.

## The filesystem is typed: loop data lives in homes · `sec:confinedadmin:the-filesystem-is-typed-loop-data-lives-in-homes`

A directory chowned to a confined user under `/var` is still unwritable: `/var/workspace/...` carries `var_t`, and `staff_t` writes `user_home_t`, not `var_t`. Do not reach for `semanage fcontext` first — put per-account data where the policy already wants it: the account's home. Per-account git hubs and working areas therefore belong below their respective account homes, which keeps ownership boundaries identical to account boundaries.

## Containers: one missing role authorization · `sec:confinedadmin:containers-one-missing-role-authorization`

The confined role can run ordinary rootless containers (`container_t` is role-authorized for `staff_r`) but not privileged or label-disabled ones (`spc_t` is not), and Toolbx creates privileged containers — so Toolbx is entirely broken while plain `podman run` works, failing with a bare `EACCES` and *no AVC record* (only `SELINUX_ERR` in the audit log; see the archived report). The fix is one authorization, installable with no compiler toolchain:

```
echo "(roletype staff_r spc_t)" > staff_spc.cil
sudo semodule -i staff_spc.cil
```

Verified end to end on two Fedora 44 installations: after the module, privileged podman and `toolbox create`/`run` all exit 0 for the confined user.

## Flatpak does not survive confinement; apps ship via toolbox · `sec:confinedadmin:flatpak-does-not-survive-confinement-apps-ship-via-toolbox`

Flatpak applications do not work under `staff` confinement; the reference deployment's stock apps were removed outright. This supports a portable delivery rule: software installs into a toolbox, and anything a human should launch gets a desktop file in `~/.local/share/applications/` whose `Exec` runs `toolbox run -c <toolbox> <command>`. The desktop-file set is then the reviewable inventory of what a seat exposes.

## Pin a rollback before lock-out-class surgery · `sec:confinedadmin:pin-a-rollback-before-lock-out-class-surgery`

On an ostree system every serious change to something that can lock all accounts out — SELinux modules or booleans, PAM stacks, sudoers, login/getty — is preceded by pinning the current known-good deployment, so the automatic pruning cannot drop the bootable state you would roll back to. The failure mode of policy surgery is losing the access needed to undo it, and even the rescue account only helps on a machine that still boots the policy it was reached under; a pin turns that from a reinstall into a reboot into the prior entry.

```
sudo ostree admin status          # identify the running (*) deployment index
sudo ostree admin pin <index>     # pin it before the change
# ... perform the SELinux / PAM / sudoers change, exercise it ...
sudo ostree admin pin --unpin <index>   # once the new state is trusted
```

Unpin deliberately after the change has proven itself — pins are rollback insurance, not accumulated history, and a short deployment ledger stays legible. Note that `/etc` and `/var` persist across deployments as a three-way merge, so a rolled-back boot restores the image and package layer but not necessarily hand-edited config under `/etc`; keep the actual policy-module and drop-in artifacts in the repo (as here) so the config half is reproducible too.

## Codex workers reach the server through a per-superloop CODEX_HOME · `sec:confinedadmin:codex-workers-reach-the-server-through-a-per-superloop-codex-home`

Codex workers may hold a real key when accessing a confined server, but the key is per-superloop and self-provisioned, because `~/.codex` is one home shared by every superloop session on the host — a server key placed there would hand every superloop's workers one identity. Each superloop instead runs its lanes under its own `CODEX_HOME` (a separate harness home is the precedent) holding its own `ssh_config` and key, and each superloop provisions its own; this is not done centrally.

The account a superloop's workers land in is that superloop's own confined staff account on the server — the compute environment the superloop shares with its workers. The worker key is a dedicated key admitted to that account alongside the superloop's master key, so it revokes independently, and it is named per-loop (`<loop>-codex_ed25519`, matching the `superloop-<loop>` master convention — the loop, not the server, is the identity axis).

Provisioning is the superloop's own responsibility and involves no human credential step: the worker key opens only the loop's own account — access the superloop already holds through its master key — so wiring it expands nothing. The measured shape (a separate harness home is the precedent; `auth.json` and the charter symlink back to the shared home so logins and charter deploys reach every loop home automatically):

```
# 1. generate a worker key (host side) and admit its PUBLIC half to the
#    superloop's own server account (via owner):
ssh-keygen -t ed25519 -N '' -C '<loop>-codex-worker' -f ~/.ssh/<loop>-codex_ed25519
cat ~/.ssh/<loop>-codex_ed25519.pub | ssh mondreiher-root \
  'sudo tee -a /var/home/<loop>/.ssh/authorized_keys >/dev/null'
# 2. create the per-superloop CODEX_HOME:
install -d -m 700 ~/.codex-<loop>/keys
install -m 600 ~/.ssh/<loop>-codex_ed25519 ~/.codex-<loop>/keys/mondreiher_ed25519
ln -s ~/.codex/auth.json ~/.codex-<loop>/auth.json
ln -s ~/.codex/AGENTS.md ~/.codex-<loop>/AGENTS.md
# ssh_config: Host mondreiher-analysis -> User <loop>, IdentityFile that key,
#   IdentitiesOnly yes; config.toml: lane model defaults plus
#   [sandbox_workspace_write] network_access = true
# 3. dispatch lanes with CODEX_HOME=~/.codex-<loop>
```

The boundary the layout enforces: a superloop's server key never leaves its own `CODEX_HOME` — copying it into another loop's home or into the shared `~/.codex` would hand one loop's identity to every loop's workers, which defeats the isolation and is never done.

## Secure Boot + akmods + ostree: the kernel-module gauntlet · `sec:confinedadmin:secure-boot-akmods-ostree-the-kernel-module-gauntlet`

Enabling an out-of-tree kernel module (measured in the reference deployment with an NVIDIA driver) crosses three systems whose failure modes compound. The working delivery, after 4 measured dead ends: the locally signed `.ko.xz` set lives under `/var/lib/<name>-kmod/` labeled `modules_object_t` (`semanage fcontext` — insmod from `var_lib_t` is a bare EACCES), loaded by a oneshot unit ordered `After=local-fs.target` and `Before=graphical.target` (`/var` is not mounted at `systemd-modules-load` time on ostree, and a display manager starting before the GPU module settles stalls the seat), with the in-tree competitor blacklisted via both kargs and modprobe.d (a driver that owns the card makes the new module fail with "No such device", not anything informative).

The dead ends, each measured so nobody walks them again:

1. **akmods builds before the signing key exists** when packages and `kmodgenca` land in one pass — the initial build is unsigned and gets delivered anyway. Create and enroll the MOK before package installation, or force a rebuild after (`akmods --force` produces a signed RPM once `/etc/pki/akmods` keys exist).
2. **akmods cannot install its own product on an image-based host** — its installer wants dnf/yum, absent by design. The built RPM sits in `/var/cache/akmods/`.
3. **rpm-ostree layering cannot deliver a same-NEVRA content fix**: the package cache is keyed by NEVRA (`ostree refs` under `rpmostree/pkg/`), so uninstall + reinstall of an identically-versioned RPM silently serves the stale first import; and even after deleting the ref, the import transformed module bytes (three distinct live hashes from one constant RPM). Kernel modules that must be byte-exact do not travel through layering — hence `/var/lib` + insmod.
4. **MOK enrollment passwords are typed on a US console layout** regardless of the system keymap — a password containing layout-sensitive characters fails at the blue screen with no diagnosis. Digits only.

Container access afterward: the CDI spec (`nvidia-ctk cdi generate`) plus `--device nvidia.com/gpu=all` works rootless, but SELinux labels the device nodes `xserver_misc_device_t`, which `container_t` cannot use — GPU containers add `--security-opt label=disable` (standard practice); privileged toolboxes run `spc_t` and are exempt. Standing cost: every kernel update orphans the signed set — refresh is `akmods --force`, extract the new RPM into `/var/lib/<name>-kmod/`, `restorecon`, reboot.

## Working defaults · `sec:confinedadmin:working-defaults`

- Fresh accounts inherit the confined default (`__default__` mapped to `staff_u`); verify with `id -Z` at first login rather than assuming.
- Key-only accounts stay locked (`passwd -l`), never empty (`passwd -d`): an empty password is a press-Enter console login, a locked one only disables password authentication while keys keep working.
- Verify the passwordless-sudo path from a fresh session *before* locking a password you might still need.
- A sudo rule that permits only `systemd-run` is root-equivalent, not a narrower door: the transient unit it starts is arbitrary, `-S` is a root shell, and property and uid flags plus package scriptlets defeat any pinning of arguments. The `ROLE=sysadm_r TYPE=sysadm_t` on the rule is attribution, an explicit transition in the audit trail, not containment: a transient unit runs in the service manager's context whatever the caller's role.
- Wheel membership gates uid 0; the role is a separate per-user list. `staff_u` carries `sysadm_r` (reachable without sudo through `newrole -r sysadm_r`, which re-authenticates and keeps the uid), `unconfined_u` does not, so a group rule `%wheel ALL=(ALL:ALL) ROLE=sysadm_r TYPE=sysadm_t ALL` yields an invalid context for an unconfined rescue account and sudo refuses rather than falling back; that account needs its own plain line below the group line, since the last matching line wins. uid 0 inside `staff_t` still bypasses DAC, so a plain sudo from any wheel member reads every mode-700 home on the box.
- `NOPASSWD` lets any process running as the account cross, which is the case for a sudo authenticated by an agent-held key or a hardware token over one that stores a password; dropping the tag is done with a usable credential in hand and a `PASSWD:` probe line on a harmless command below the main rule, checked from a second session before the rule is narrowed.
- journald's forward secure sealing is never enabled (`journalctl --setup-keys` is not run) and a passing `journalctl --verify` is never cited as evidence: the verification key is the sealing seed, so whoever can verify can also re-seal a doctored journal, silently and for every past epoch, and the seal then vouches for the forgery. Journal integrity is built above journald, as an off-box replica in another trust domain and an asymmetric signature over a digest, which the security posture document states.
