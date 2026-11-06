# Root-full server setup · `guide:rootserver:root-full-server-setup`

Reading order and parent: (`guide:docnav:documentation`).

This guide turns a fresh machine into a persistent, estate-controlled compute server without importing facts from any existing instance. Replace uppercase words such as `ACCOUNT`, `ALIAS`, `UID`, `TABLE`, and `PACKAGE` with values selected in the private server registry; never substitute endpoint coordinates into a repository document. The guide gives the safe order and acceptance probes, while the linked specifications remain authoritative.

## What a root-full server is · `sec:rootserver:what-a-root-full-server-is`

**What.** A root-full server is an estate-controlled persistent host whose root custody belongs to the owner. It supplies isolated accounts, policy-managed administration, durable local services, and replaceable compute surfaces. It is not a rented ephemeral pod: an ephemeral pod has no estate root custody, holds no on-box provider or owner secrets, and may disappear with all local state. It is also not the workstation: the workstation is the trusted host and source of record, while the server is an execution domain. Source and authority flow from host to server; everything that returns, including source commits, logs, reports, binaries, and suggested commands, is data until quarantined and reviewed. This boundary is defined by [server execution and trust](spec/server.md).

**Why.** Root custody makes operating-system isolation, rollback, kernel networking, and machine-local services possible, but it does not make server-produced material authoritative. Keeping the workstation as restore source makes loss or compromise of the server recoverable without trusting remnants from the failed machine.

**Recipe.** Before installation, create a private registry row with classification `root-full`, an owner, a proposed alias roster, and references to host-held bootstrap inputs. Keep the row private and leave endpoint fields unresolved until the access configuration is built. Accept the machine only if the owner controls the boot path, firmware choices, local console, storage, root-capable rescue path, and operating-system installation.

**Probe.** From a local console, prove that the owner can enter the explicit administrative domain and that a non-owner login cannot:

```bash
id -Z
sudo -n id -Z
```

The registry-selected administering session is confined and the second command reports `sysadm_t`; a loop or human staff account must fail noninteractive sudo. On the workstation, verify that the complete bootstrap inputs and reviewed source exist independently of the new server. Treat a missing host-held input as a failed root-full acceptance, not as permission to recover it from server state.

## Platform baseline · `sec:rootserver:platform-baseline`

**What.** Install the latest Fedora CoreOS stable release from the stable stream on disk, with SELinux enforcing and every login mapped to `staff_u`. Record the selected release and image identity in the private registry; the baseline names a stream, not a permanently pinned release. A provider pod stays on the provider's image: this baseline applies where the estate holds root. Put `/var`, `/var/home`, account homes, workspaces, caches, Cargo targets, and build temporaries on a disk-backed filesystem with sufficient headroom. A memory-backed temporary filesystem may hold small bounded control files only; builds, downloads, links, test data, and bulk transfers must use an account-owned disk-backed `TMPDIR`. The platform posture and its deliberate delta from defaults are explained in [the security posture](security-posture.md), and storage requirements are normative in [server execution and trust](spec/server.md) and [build and deployment topology](spec/deployment.md).

**Why.** Fedora CoreOS supplies the ostree image and SELinux substrate without a desktop stack, declarative first-boot provisioning through Ignition, a bootable deployment ledger, and automatic updates through Zincati inside a declared window. Keeping the installation file and versioned increments makes a reinstall reproducible. The confinement and rollback posture rests on ostree and SELinux rather than on a desktop image; UEFI installations retain the Secure Boot module gate. Disk-backed work avoids turning build volume into memory pressure, while home placement gives confined accounts the filesystem type they are already allowed to write.

**Recipe.** Prepare the installation through the CoreOS recipe (`guide:coreos:bare-metal-server-guides`), declare the Zincati window, and retain the reviewed Butane source and generated Ignition identity with the host-held bootstrap inputs. During installation, allocate persistent capacity to the filesystem containing `/var/home`; do not point account work at a memory-backed `/tmp`. After first boot, inspect rather than assume the storage class, create a private temporary directory for each working account, and persist its selection in that account's controlled environment:

```bash
getenforce
rpm-ostree status
findmnt -T /var/home
findmnt -T /tmp
sudo -u ACCOUNT install -d -m 700 /var/home/ACCOUNT/.cache/tmp
sudo -u ACCOUNT env TMPDIR=/var/home/ACCOUNT/.cache/tmp findmnt -T /var/home/ACCOUNT/.cache/tmp
```

Before changing SELinux policy, PAM, sudoers, login configuration, or any other lock-out-class surface, identify and pin the booted deployment:

```bash
sudo ostree admin status
sudo ostree admin pin DEPLOYMENT_INDEX
sudo ostree admin status
```

If Secure Boot is enabled and the server needs an out-of-tree kernel module, treat enrollment, signing, SELinux labeling, load ordering, and competing drivers as one gate. Create and enroll the machine-owner key before the first module build; make the enrollment secret console-safe; confirm the built module is signed; keep the exact signed module set under a root-owned `/var/lib/DRIVER-kmod/` path labeled `modules_object_t`; load it from a oneshot unit ordered after `local-fs.target` and, where graphical startup depends on it, before `graphical.target`; and blacklist any in-tree competitor in both kernel arguments and modprobe configuration. Refresh and re-probe the signed set after every kernel update. The measured constraints and failure modes are in [confined administration](confined-admin.md).

**Probe.** `getenforce` prints `Enforcing`; `rpm-ostree status` identifies an immutable deployment and the intended rollback pin; `findmnt` shows that `/var/home` and each working `TMPDIR` are disk-backed; and an intentional file create as `ACCOUNT` succeeds below `/var/home/ACCOUNT` without relabeling a generic `/var` directory. Where the module gauntlet applies, `mokutil --sb-state`, `modinfo -F signer MODULE`, `matchpathcon /var/lib/DRIVER-kmod/MODULE_FILE`, `systemctl is-active DRIVER-kmod-load.service`, and a device-specific smoke test must all agree after reboot.

**Firmware and firewall.** Record whether the installed system boots legacy BIOS or UEFI and whether Secure Boot and a TPM are available; a capable board booted in BIOS mode is not a UEFI acceptance. On UEFI, retain the Secure Boot checks and module gauntlet above. A legacy-BIOS or no-TPM selection records its limits and the owner's encryption disposition without claiming those protections. The CoreOS example deliberately keeps that fictional hardware case (`obs:coreos:hardware`).

Use nftables as the host firewall with an explicit input policy, established traffic, loopback, ICMP, the selected DHCP reply paths and key-only SSH admitted; firewalld is inactive. Merge any selected WireGuard listener and application rules into that reviewed ruleset. Check the persistent configuration as well as the running rules, because a reload beginning with a flush removes undeclared tables (`setup:coreos:butane-firewall`).

## The account model · `sec:rootserver:the-account-model`

**What.** Establish one confined administering login, named by the private registry, before enabling remote entry. It holds the approved administrative group and elevates explicitly to `sysadm_r:sysadm_t`; there is no separate `owner` login and no unconfined administrator login. Its SSH admission is key-only. If console recovery needs a password, only this administering account holds one, kept in external owner custody and never admitted over SSH. Human staff and loop accounts are key-only, password-locked, non-administrative identities with separate homes, processes, credentials, caches and evidence. A headless compute node has no showcase account. The account and recovery roles are defined in (`proposal:serveraccounts:root-server-account-model`).

**Why.** A distinct uid makes each loop's storage, processes, keys, resource use and audit evidence attributable. Every login, including administration and console entry, maps to `staff_u`. Recovery from a policy that prevents the administrative transition uses the provider rescue path (`proto:coreos:rescue`), not a standing unconfined login. Confinement does not protect an account's data from that account or make an authorized administrator unable to change policy.

**Recipe.** Declare the administering and loop accounts from the registry in Ignition, with public-key placeholders filled only in the staging copy. Declare the default and explicit login mappings, the sudo transition and the reviewed container-role authorization in the same installation input. Activate them in a system-context identity unit ordered before sshd; validate sudoers and rebuild the login store before the first SSH session (`setup:coreos:first-boot-identity`). After policy utilities are available, inspect the effective mappings rather than assuming the default overrides an existing explicit entry:

```bash
sudo semanage login -l
id -Z
sudo -n id -Z
sudo visudo -cf /etc/sudoers.d/zz-admins
```

The administering login must report `staff_t`, and its sudo command must report `sysadm_t`. A loop login reports `staff_t` and has no sudo authorization. Refuse an unconfined mapping. Retain the provider recovery route until fresh key sessions prove both identities; do not rename uid 1000 or require a literal `owner` account to satisfy a bootstrap profile from a different platform.

For each human staff or loop account, choose a unique registry uid, create the home on `/var/home`, lock the password, map the login to `staff_u`, create `.ssh` and `correspondence`, and create `git` plus `loops` for loop accounts:

```bash
sudo useradd --uid UID --user-group --create-home --home-dir /var/home/ACCOUNT --shell /bin/bash ACCOUNT
sudo passwd -l ACCOUNT
sudo semanage login -a -s staff_u ACCOUNT
sudo install -d -m 700 -o ACCOUNT -g ACCOUNT /var/home/ACCOUNT/.ssh
sudo install -d -m 755 -o ACCOUNT -g ACCOUNT /var/home/ACCOUNT/correspondence
sudo install -d -m 750 -o LOOP -g LOOP /var/home/LOOP/git /var/home/LOOP/loops
sudo restorecon -RF /var/home/ACCOUNT
```

A superloop's existence is prior authorization for the standard loop-class account on each server. The loop supplies its public master and worker keys from its own custody; the owner performs the privileged creation and admission without seeking a new policy decision. GPU grants, extra identities, wheel, human onboarding, or any surface beyond the standard class still needs separate authority. Reconciliation must be idempotent: inspect the effective SELinux mapping, uid ownership, group membership, key fingerprints, modes, and home labels before changing them, and refuse a collision instead of reallocating silently.

A graphical showcase is a separately selected role, not a prerequisite for this headless baseline. If that role is selected, install the key-only SSH guard, PAM block against `su` and `sudo -u`, console auto-login, and network-management polkit denial before deleting its password for physical-console entry. Aggregate loop public keys into its `authorized_keys`; never create a showcase-wide private key. [The security posture](security-posture.md) explains why a connection-add action, rather than enabling an already enabled connection, is the valid NetworkManager authorization probe.

**Probe.** Open a fresh PAM session for every account and run `id -Z`; every login reports `staff_t`, including the administering account; no login reports `unconfined_t`. `getent group wheel` lists only the approved administrative classes, `passwd -S ACCOUNT` shows loop and staff passwords locked, and one loop account cannot list another loop's home. For the showcase, remote password authentication and switched-user entry fail, physical-console entry works as designed, and a NetworkManager connection-add attempt is denied.

## Administering under confinement · `sec:rootserver:administering-under-confinement`

**What.** Give the registry-selected administering account a sudo rule that changes both role and type; do not mistake uid zero inside `staff_t` for administration. Route rpm-ostree through a system-context transient unit, put loop data in policy-typed homes, explicitly authorize the confined role for the privileged container type when Toolbx is required, and keep the rollback deployment pinned through the observation window. These are measured recipes from [confined administration](confined-admin.md); the container failure evidence is preserved in [the confined-container bug report](reference/bugreport-staff_t-container_t.md).

**Why.** SELinux makes administrative capability a domain transition rather than a uid property. The separation prevents a seized confined session from acquiring ambient write access to system configuration and turns every privileged crossing into a narrow, journaled event.

**Recipe.** Install the mode `0440` sudoers drop-in through Ignition and the identity unit before sshd starts; validate it there and verify it from a fresh administering login. The rule names the approved administrative group, which only the administering login holds:

```text
%sudo ALL=(ALL) ROLE=sysadm_r TYPE=sysadm_t NOPASSWD: ALL
```

```bash
sudo visudo -cf /etc/sudoers.d/zz-admins
sudo -n id -Z
```

If the initial drop-in must be installed from an already confined administering session, request the transition explicitly with `sudo -r sysadm_r -t sysadm_t`; do not use plain sudo as a workaround. Stage image changes and apply them live as separate calls:

```bash
sudo systemd-run --wait --pipe --collect -- rpm-ostree install --idempotent PACKAGE
sudo systemd-run --wait --pipe --collect -- rpm-ostree apply-live
```

Exclude a package already supplied by the base image or deliberately use `--allow-inactive`; one inactive package can otherwise fail the batch. Keep account data under `/var/home/ACCOUNT`, where it inherits `user_home_t`, rather than relabeling an arbitrary `/var` workspace. For Toolbx and privileged rootless containers, install the narrow `staff_r` authorization for `spc_t`, then verify both ordinary and privileged cases; do not broaden it into an unrelated allow policy:

```bash
printf '%s\n' '(roletype staff_r spc_t)' | sudo tee /etc/selinux/staff_spc.cil >/dev/null
sudo semodule -i /etc/selinux/staff_spc.cil
podman run --rm CONTAINER true
podman run --rm --privileged CONTAINER true
toolbox create TOOLBOX
toolbox run -c TOOLBOX true
```

Flatpak is not part of this confined posture. Install development and showcase applications in rootless containers or Toolbx; expose a human-facing application only through a reviewed desktop file whose command enters the named toolbox.

**Probe.** In a fresh administering login, `id -Z` reports `staff_t` and `sudo -n id -Z` reports `sysadm_t`. A controlled plain-uid-zero process retained in `staff_t` cannot write `/etc`, while the explicit transition can perform a narrowly scoped administrative write. The rpm-ostree transient unit finishes successfully, home-local writes succeed without custom relabeling, ordinary Podman and Toolbx smoke tests exit zero, and `ostree admin status` still shows the known-good deployment pinned.

## Access · `sec:rootserver:access`

**What.** Permit SSH by public key only. Give every account on every server its own client alias, and keep addresses, transport ports, proxy details, and roaming endpoints exclusively in the access-controlled client SSH configuration. The public [fictional server registry](examples/servers.md) illustrates the naming discipline; the durable alias-only rule is in [server execution and trust](spec/server.md).

**Why.** Account-scoped aliases prevent command lines and retained evidence from leaking endpoint facts, while separate keys make every admission and revocation attributable. Key-only SSH also keeps the rescue password a console property instead of an internet-facing credential.

**Recipe.** After fresh-session key tests succeed for all required accounts, set `PasswordAuthentication no` and `KbdInteractiveAuthentication no` in a reviewed sshd drop-in, validate with `sshd -t`, reload rather than restart, and retain the tested console rescue path. Populate client configuration outside the pack. A template may use fictional aliases while the endpoint placeholders are filled only in the private client file:

```sshconfig
Host sagofink-root
    HostName ADDRESS
    Port PORT
    User ADMIN_ACCOUNT
    IdentityFile KEY_FILE
    IdentitiesOnly yes

Host mondreiher-analysis
    HostName ADDRESS
    Port PORT
    User ACCOUNT
    IdentityFile KEY_FILE
    IdentitiesOnly yes
```

The owner admits a verified public key without transporting a private key or consulting a forge account. Resolve the target account from the private registry, create its SSH directory with restrictive ownership, append only after fingerprint review, restore labels, and read back the installed public-key fingerprints:

```bash
ssh OWNER_ALIAS 'sudo install -d -m 700 -o ACCOUNT -g ACCOUNT /var/home/ACCOUNT/.ssh'
ssh OWNER_ALIAS 'sudo tee -a /var/home/ACCOUNT/.ssh/authorized_keys >/dev/null' < PUBLIC_KEY_FILE
ssh OWNER_ALIAS 'sudo chown ACCOUNT:ACCOUNT /var/home/ACCOUNT/.ssh/authorized_keys && sudo chmod 600 /var/home/ACCOUNT/.ssh/authorized_keys && sudo restorecon -RF /var/home/ACCOUNT/.ssh'
ssh OWNER_ALIAS 'sudo ssh-keygen -lf /var/home/ACCOUNT/.ssh/authorized_keys'
```

Each superloop also creates a private client home for its workers. That home contains its own worker private key and a two-alias SSH configuration for that loop account on the two approved servers. Do not put a loop's server key in a shared client home. A generic layout is:

```text
CLIENT_HOME/
├── keys/
│   └── worker_ed25519
└── ssh_config
```

```sshconfig
Host ALIAS_ONE
    HostName ADDRESS_ONE
    Port PORT_ONE
    User LOOP
    IdentityFile CLIENT_HOME/keys/worker_ed25519
    IdentitiesOnly yes

Host ALIAS_TWO
    HostName ADDRESS_TWO
    Port PORT_TWO
    User LOOP
    IdentityFile CLIENT_HOME/keys/worker_ed25519
    IdentitiesOnly yes
```

Dispatch workers with `CODEX_HOME=CLIENT_HOME` and connect with `ssh -F CLIENT_HOME/ssh_config ALIAS COMMAND`. The worker key opens only that loop's own server account and is independently revocable from the loop's master key. No step assumes a forge login, credential helper, shared account, or network-access token.

**Probe.** `ssh -G ALIAS >/dev/null` exits zero without retaining its expanded output, then `ssh -F CLIENT_HOME/ssh_config ALIAS 'id -un; id -Z'` lands in the intended account and `staff_t`. A key admitted to one account cannot enter another account, removing the worker key leaves the master key usable, and `sshd -T` reports both password mechanisms disabled.

## The door · `sec:rootserver:the-door`

**What.** Select administration, application publication and recovery routes by the machine's role and record each disposition. A compute-only node may use its alias-scoped key-only SSH route and provider rescue without a local site tunnel or public application tunnel; that is an explicit role selection, not proof of either tunnel. An outbound application tunnel (`sec:coreos:tunnel`) publishes selected services and does not replace administrative access, per-account egress isolation or rescue. Where a site door is required, build it from two WireGuard layers: a root-owned provider uplink with a provider-side port forward, and the server's inbound site WireGuard listener reached through that forward. Give each tunneled loop account its own provider tunnel and route its uid through that tunnel; keep owner and rescue maintenance independent of loop egress. Produce a separately delivered roaming-client pack containing the client key, tunnel configuration, and the private endpoint coordinates. The network model is described in [per-account WireGuard routing](proposals/per-user-wireguard-routing.md).

**Why.** The provider forward gives inbound reachability without publishing the site's own address, and uid-based policy routing makes egress attributable without giving staff `NET_ADMIN`. Fail-closed routing prevents a tunnel outage from silently becoming direct egress.

**Recipe.** As owner, mint server tunnel keys on the server, store uplink configuration and provider credentials root-only, set `Table = off` in account tunnel configurations, and create explicit policy rules and tables. Keep loopback and approved site-local traffic on the main table, then add a default route for each account table and an nftables kill switch that rejects that uid's internet traffic unless it exits its assigned interface:

```bash
sudo ip rule add uidrange UID-UID lookup TABLE
sudo ip route add default dev WG_ACCOUNT table TABLE
sudo systemctl enable --now wg-quick@WG_ACCOUNT.service
sudo systemctl enable --now wg-quick@WG_SITE.service
sudo wg show
sudo ip rule show
sudo ip route show table TABLE
```

Register the uplink public key with a WireGuard VPN provider that supports port forwards, request the forward through the owning tunnel, validate that the returned allocation belongs to that tunnel, and bind the site listener to the assigned forwarded port in both runtime and persisted configuration. Never put provider tokens, tunnel private keys, endpoint coordinates, assigned ports, allocation identifiers, or expiry data in the pack. Store only references and current state in the private registry, and deliver roaming packs through an owner-controlled channel.

The standing self-heal design, not an assumption about deployment, is [provider-door self-healing](proposals/door-self-heal.md). A root-owned, non-overlapping timer should list the allocation through its own tunnel, distinguish an authenticated empty listing from transport or parsing failure, renew a missing or ageing grant, reconcile provider state with the runtime and persisted listener, and emit durable change notice without exposing its token. An independent external beacon must use ordinary site egress rather than the provider path.

The four failure classes are distinct: provider-side grant loss, scheduled grant expiry, a valid grant with a failed provider tunnel or listener path, and loss of the site's uplink. Diagnose them in evidence-preserving order: check the external beacon first; if the beacon is fresh, inspect the provider listing, self-heal journal, listener reconciliation, and external probe; if every co-sited beacon is silent while the receiver is healthy, investigate the shared site path; if the receiver is unhealthy, call the diagnosis degraded rather than blaming the site. Do not begin by changing the roaming client's routes or endpoint.

One repaired provider path is still one failure domain. Maintain a plurality of doors using different providers or mechanisms, with independently held credentials and documented selection rules, so loss of one provider, server, or route does not remove every recovery path.

**Probe.** For a selected site WireGuard door, from a genuinely roaming vantage bring up the client pack and require a fresh WireGuard handshake plus an application-level key-only SSH login through the site listener. On the server, confirm that traffic from `UID` uses only `WG_ACCOUNT`, that stopping the tunnel blocks external egress rather than sending it directly, and that owner maintenance remains reachable. Exercise each self-heal input as a fixture before activation, but call the live path accepted only after an external handshake. Finally, prove that at least one independent door remains usable while the primary door is deliberately unavailable.

## Toolchains, hubs, and lane surfaces · `sec:rootserver:toolchains-hubs-and-lane-surfaces`

**What.** Provide the registered routine Rust toolchain, normally nightly, as management-owned tools read-only to loops or as an account-owned installation; reserve stable and the declared minimum supported Rust version for release moments. Give every purpose a target directory under the loop's home, keep `TMPDIR` on disk, run all builds and rebuilding gates at the minimum scheduling priority, and maintain a per-loop bare Git hub plus disposable project and lane checkouts. These constraints come from [server execution and trust](spec/server.md) and [build and deployment topology](spec/deployment.md).

**Why.** Root-owned shared tools avoid duplicating a common compiler while private account state prevents caches and credentials from crossing boundaries (`rule:server:shared-toolchains-private-caches`). Purpose-specific targets preserve useful cache intelligence without mixing toolchains or profiles, and minimum priority keeps batch compilation from starving control and recovery services.

**Recipe.** On a compute node that supplies common C and Rust tools, declare the required development packages in the image layer and publish the system Rust installation under a root-owned prefix such as ``/usr/local/rustup``, with read-only wrappers under ``/usr/local/bin``. Keep the declared update unit and timer in the installation input; record each selected toolchain and its update provenance. Updates do not silently change a running lane's designated toolchain. Each account retains its own Cargo home and may use its registered home-local override. As the loop account, the home-local installation alternative and private work surfaces are:

```bash
rustup set profile minimal
rustup toolchain install nightly --component rustfmt --component clippy
rustup default nightly
install -d -m 700 "$HOME/.cache/tmp" "$HOME/.cache/cargo-target/DEVELOPMENT" "$HOME/.cache/cargo-target/GATES"
findmnt -T "$HOME/.cache/tmp"
```

Install stable or a declared MSRV toolchain only for a reviewed release check; do not silently change the development default. Create one bare transport hub and one disposable checkout per project or lane, all beneath the owning home:

```bash
git init --bare "$HOME/git/PROJECT.git"
git clone "$HOME/git/PROJECT.git" "$HOME/loops/PROJECT"
git clone "$HOME/git/PROJECT.git" "$HOME/loops/lanes/LANE"
install -d -m 700 "$HOME/.cache/cargo-target/LANE"
```

Provision each lane checkout with repository-local Git identity and a writable `.git` metadata path inside that lane's sandbox allowance. Push reviewed host source to a named disposable input ref, force the lane checkout to that exact object, remove residual state, and prove it clean before execution. Returned commits go only to a dedicated server ref that the workstation fetches into quarantine; neither the hub nor the checkout has integration authority.

Every run goes through the installed run-report wrapper. Set priority, temporary storage, and the purpose target before the first expensive child, and require the wrapper's terminal record to carry child status, elapsed wall time, free space on the system temporary surface, and free space on the loop workspace:

```bash
env TMPDIR="$HOME/.cache/tmp" CARGO_TARGET_DIR="$HOME/.cache/cargo-target/LANE" nice -n 19 RUN_WRAPPER COMMAND ARGUMENT
```

For a long job, allocate a unique run id, private append-only log and completion marker, and launch once under the wrapper. Assign the result, its evidence location and deadline to the lane's Sonnet watcher through (`proto:server:remote-callback`). It owns waiting, reports completion or silence and over-budget movement by hand-back, and retains the observation basis across duties. The session decides; it runs no workstation-side watching script. Resume a live watcher by message and replace only a dead one after its surviving tool process is stopped, never by relaunching the server job merely because its watcher died.

Teardown is part of the lane contract. At completion or abandonment, reconcile the Sonnet watcher's hand-back with the final marker and report, return selected source only through quarantine, remove the lane's disposable checkout and target directory under explicit lane-scoped cleanup authority, and leave the hub, credentials, other lanes, and retained evidence untouched.

**Probe.** As the loop account, `rustup show active-toolchain` reports nightly; stable or MSRV appears only in an explicit release command. `findmnt -T "$TMPDIR"` identifies disk-backed storage, `ps -o ni= -p PROCESS_ID` reports the minimum selected nice value for the build and its descendants, each target resolves below the same loop home, and another loop cannot read it. From the workstation, a pushed input object matches the clean lane checkout; the wrapper emits one correct terminal report on success and failure; the Sonnet watcher detects both completion and induced silence without duplicate execution; and a cleanup drill removes only the named lane surfaces.

## Mechanical services · `sec:rootserver:mechanical-services`

The server baseline uses timers for fixed observations and fixed actions. A timer must fail loudly when blind, remain bounded and non-overlapping, report elapsed work, and never ask an agent to reinterpret a deterministic condition.

**Correspondence pipeline. What.** Create `~/correspondence/` for every account and deploy the one-minute scanner from [infra/correspondence-watch](../infra/correspondence-watch/README.md). A file whose basename ends in `-admin-reply.md` is administrative output; otherwise a file owned by the home account is `from=user` and any other owner is `from=admin`. Quiet scans stay quiet.

**Correspondence pipeline. Why mechanical.** File enumeration, ownership comparison, hashing, cursor advance, and journal classification have exact answers. A model would add ambiguity without adding authority; judgment begins only after a correctly classified user event reaches its designated consumer.

**Correspondence pipeline. Recipe and deploy pointer.** Follow the reviewed install and ownership recipe in `infra/correspondence-watch/`, enable `correspondence-watch.timer`, and keep every folder owned by its account. Admin replies use the suffix convention or remain administratively owned so they do not wake the consumer as new user work.

**Correspondence pipeline. Probe.** `systemctl is-enabled correspondence-watch.timer` and `systemctl is-active correspondence-watch.timer` both succeed. Create one account-owned fixture and one administrative-reply fixture, run the service once, and inspect `journalctl -t correspondence-watch`; exactly one line is `from=user`, one is `from=admin`, each carries the expected relative path and digest, and a second unchanged scan emits no event.

**Hard memory floor. What.** Install earlyoom with an absolute `MemAvailable` floor of five GiB, configure swap pressure not to supersede that floor, protect the machine's spine such as init, SSH, network management, and WireGuard control processes with the avoid list, and retain periodic reports. This is the last-resort control beneath any human or future steward judgment.

**Hard memory floor. Why mechanical.** A lock-up can remove the time and access needed for deliberation. A fixed absolute floor and fixed protected process set must react predictably before the machine loses its control plane.

**Hard memory floor. Recipe and deploy pointer.** Layer `earlyoom` through the confined rpm-ostree route, stage then apply live, install a reviewed `/etc/default/earlyoom` configuration containing `-M 5242880 -s 100`, an explicit avoid expression for the control-plane process names selected during bootstrap, and hourly reporting, then enable `earlyoom.service`. The durable deployment artifact belongs under `infra/oom-guard/`; this pack revision does not yet contain that directory, so preserve the reviewed configuration and unit inputs in the host-held bootstrap set and do not copy bytes from a live server.

**Hard memory floor. Probe.** `systemctl is-enabled earlyoom.service` and `systemctl is-active earlyoom.service` both succeed; `systemctl show earlyoom.service -p ExecStart` or the service's startup journal shows the absolute floor, swap setting, avoid list, and reporting option; `/proc/meminfo` supplies the current `MemAvailable` reading; and `journalctl -u earlyoom.service` contains the startup line translating the absolute floor for this machine. Never validate by deliberately exhausting production memory.

**Per-staff Cargo cleanup. What.** Deploy one two-hour timer instance per approved confined staff account from [infra/cargo-clean](../infra/cargo-clean/README.md). It runs as that account, discovers Cargo workspaces and detached Cargo target markers below that account's home, and cleans only owned, proven build output. The explicit account list excludes the administering account and root.

**Per-staff Cargo cleanup. Why mechanical.** Ownership, Cargo marker pairs, path containment, idleness, and bytes reclaimed are deterministic. The timer prevents disposable build output from accumulating without granting a cross-account or root cleanup capability; its accepted cost is that a cleaned build is cold.

**Per-staff Cargo cleanup. Recipe and deploy pointer.** Follow `infra/cargo-clean/README.md`, install the script and template units as root, enable `cargo-clean@ACCOUNT.timer` for each reviewed account, and use the minimum-idle-hours drop-in only when the chosen cache policy calls for it. Never point an instance outside the selected account's home.

**Per-staff Cargo cleanup. Probe.** `systemctl list-timers 'cargo-clean@*'` lists exactly the approved accounts. Start one service instance and inspect its final `cargo-clean: run` journal line; it names the account-local root, target counts, failures, freed bytes, and duration. Symlink, foreign-owner, foreign-signature, and outside-home fixtures are reported as skips and survive unchanged.

A later resident steward would add policy-guided, attributable judgment for correspondence and resource arbitration, with bounded invocation and external oversight. It is not part of these mechanical controls and is not specified here; see [the resident-steward proposal](proposals/resident-steward.md) and the dormant deployment kit in [infra/steward](../infra/steward/README.md).

## Verification checklist · `sec:rootserver:verification-checklist`

Run these probes in order after setup and after any bootstrap replay. Stop at the first mismatch.

1. **Staff confinement.** `ssh -F CLIENT_HOME/ssh_config STAFF_ALIAS 'id -Z'` reports `staff_t`, and the account is absent from wheel. Any unconfined login fails acceptance.

2. **Administrative transition.** From a fresh administering login, `id -Z` reports `staff_t` and `sudo -n id -Z` reports `sysadm_t`; a controlled plain sudo path that stays in `staff_t` cannot write `/etc`. The administering console login is also confined; there is no unconfined login exception. Verify provider rescue separately from the installed policy.

3. **Alias resolution without endpoint exposure.** `ssh -G ALIAS >/dev/null` and a harmless `ssh ALIAS true` both exit zero. Store neither expanded configuration nor verbose transport output in the report; retained evidence contains only `ALIAS` and status.

4. **Selected door.** For a selected site WireGuard door, from a network outside the site, the roaming pack records a fresh WireGuard handshake and completes a key-only SSH login. A local provider listing or listener socket alone is not an end-to-end result. For a compute-only SSH route, prove the registered key login and independent rescue disposition instead; record an omitted application tunnel as not selected.

5. **Loop isolation.** As `LOOP_A`, attempts to list or read `/var/home/LOOP_B`, its `.ssh`, cache, target, hub, and workspace fail. Ownership and SELinux agree; a discretionary-permission failure alone is not used to excuse a wrong label.

6. **Toolchain and hub reachability.** As each loop, nightly Rust, rustfmt, and clippy resolve; the loop can fetch its bare hub and force a clean disposable checkout to the declared object; other loops cannot write that hub or checkout; and the workstation can reach it by alias without exposing coordinates.

7. **Timers active.** `systemctl is-active correspondence-watch.timer`, every reviewed `cargo-clean@ACCOUNT.timer`, and every enabled door self-check or beacon timer return `active`. A design that is not yet deployed is recorded as absent rather than reported green.

8. **Memory-floor evidence.** `systemctl is-active earlyoom.service` succeeds and the latest startup journal line names the configured absolute five-GiB floor, the swap-independent setting, and the protected control-plane set.

9. **CoreOS deployment and packages.** `rpm-ostree status` names the selected stable deployment and requested layered packages; distinguish the booted image from a staged layered image and an apply-live filesystem. `ostree admin status` identifies the actual booted index before pinning it; never assume index zero is booted. Probe the required programs with `rpm -q PACKAGE` and their harmless version commands. After a controlled reboot, verify that the intended layered deployment is booted and the known-good rollback remains pinned.

10. **First boot and updates.** Ignition runs in the initramfs of the first boot, so read its records there with `journalctl -b BOOT --identifier=ignition --all`, where `BOOT` is the first boot listed by `journalctl --list-boots`; then read `systemctl status identity-increment.service` and the identity unit journal. Require completed provisioning and successful policy activation; classify warnings from their effect rather than accepting every log error or rejecting a known benign partition re-read alone. `systemctl is-active zincati.service` must succeed after layering; read its journal and the declared periodic strategy/window under ``/etc/zincati/config.d``. An active unit alone does not prove the intended window or a successful scheduled update.

11. **Firewall, firmware and boot time.** `systemctl is-active nftables.service sshd.service`, `sudo nft list ruleset`, `getenforce` and `systemctl --failed --no-legend` must agree with the selected configuration. Record ``/sys/firmware/efi`` presence, the selected Secure Boot probes where applicable, and TPM availability without treating an absent device as a passing security feature. Measure reboot command, observed down, ping and verified installed-system SSH separately; distinguish rescue SSH by host key. Set the alarm from that board's recorded wall and margin (`obs:coreos:reboot-alarm`).

12. **Node gate and confinement frictions.** Run the repository's complete gate on the node with its declared tools and record the terminal result and resource deltas. From an unprivileged confined login, test ordinary rootless Podman, a label-disabled or privileged container, and Toolbx creation, execution and a home write. Read both AVC and SELinux error records with `ausearch --input-logs -m AVC,USER_AVC,SELINUX_ERR -ts boot </dev/null`; retain a denial as a finding before deciding whether it is an expected probe effect or a missing authorization.

Record each expected result, exit status and wall duration in the private acceptance record. An omitted role-specific service is named with its disposition; a skipped applicable probe is a blocking finding, never an implicit pass. These are deployment instructions checked against the recorded basis below, not a fresh live acceptance.

**Register (Recorded FCOS probe basis)** · `reg:rootserver:recorded-fcos-probe-basis`

The first root-full FCOS deploy notes, recorded on 2026-11-05, supply the following anonymized evidence. They were read through their final amendments: the intermediate two-account and unconfined-admin forms were superseded. This register preserves the distinction between observed results, a refusal and an unperformed check; the fictional CoreOS set retains its own fixture figures.

|Probe or instruction|Recorded result|Limit carried into the recipe|
|--------------------|---------------|-----------------------------|
|First-login staff mapping and sudo transition|The replica's first session was confined; sudo reached sysadm. The final input mapped every login to staff and created no separate owner or unconfined administrator.|A fresh installed-system session is required; a login-store file alone is not acceptance.|
|Identity unit and SSH output|The replica reproduced the SSH-session FIFO denial for sudo and journal output; installing the FIFO rule restored the route, and the rule was folded into the pre-sshd identity unit.|The other illustrated service/process allow rules did not reproduce and were not copied.|
|Container role authorization|A loop's ordinary rootless container worked, but Toolbx and label-disabled containers failed with an invalid `staff_u:staff_r:spc_t` context. After the module, Toolbx creation, execution and a home write passed; a label-disabled run passed.|The final module belongs in the first-boot file set; no fresh run is claimed here.|
|Ignition and layers|Ignition completed despite eight partition re-read error lines in the mirrored-disk rehearsal. The three initial runtime packages were live at 60–65 s uptime; the layered deployment remained staged until reboot.|Inspect completion and live/staged/booted state separately; the warning count is evidence of that disk layout, not a universal allowance.|
|Physical reboot and alarm|First boot: down at 26 s, ping at 160 s, installed SSH at 165 s after the reboot command (139 s down-to-SSH). The later layered reboot: down at 22 s, SSH at 100 s (78 s down-to-SSH).|The initial 300 s alarm was provisional. These walls do not replace a new board's measurement, and no scheduled-update window was measured by these reboots.|
|Firmware and firewall|The board is UEFI-capable but booted legacy BIOS, with no ``/sys/firmware/efi`` and no TPM device. On the replica and the board SELinux was enforcing, nftables and sshd were active and no unit had failed.|No Secure Boot, module-gauntlet or TPM check ran on this platform; a UEFI installation's firmware acceptance remains unperformed.|
|Rollback pin|The pristine booted deployment was index 1 while the layered candidate was staged at index 0; the pristine entry was pinned before reboot.|Read status before selecting the index. Image rollback does not restore every mutable configuration file.|
|Recovery and replica limits|The owner waived the rescue-to-rescue, reset and console proof before installation. The physical-disk snapshot boot was skipped because mirror resync into RAM-backed overlays would exhaust rescue memory.|Those checks remain unproven; a documented waiver is not a successful rescue drill. Use disk-backed bounded rehearsal storage.|
|Bootstrap and homes|The older kit stopped at its preflight requiring `owner`; nothing after that refusal was tested by the kit. Accounts were provisioned from declarations with home-local hubs/workspaces and lingering managers.|Do not claim full kit convergence or reuse its uid-1000 rename/showcase assumptions for this model.|
|System tools and administration route|The confined rpm-ostree client was refused; the system-context transient-unit route worked. Later increments installed common development packages and a root-owned system Rust toolchain. A system-unit log directed into a user home was refused.|Keep system logs under ``/var/log`` or in the journal and loop caches private; a system tool does not authorize shared mutable account state.|
|Gate and application-role boundary|The estate node gate passed in 118.6 s. Subsequent repository gates exposed a missing external program and version-sensitive fixtures. Production services, their backups and the outbound application tunnel were not selected for the compute role.|A gate is evidence for its measured tree and toolchain; it does not prove unselected service or recovery paths.|

## Recovery · `sec:rootserver:recovery`

**What.** Keep one private registry row for the new server. It records the owner and classification; alias roster; current capability and restriction audit with freshness; account classes, uid allocations, and key-reference custody; storage, temporary, toolchain, target, hub, and wrapper selections; door and routing inventory including private endpoint and grant state; enabled mechanical services; rollback-pin status; bootstrap source identity; and replacement notes. The row references secret material but never embeds it, and it never ships in the public pack. Registry scope and failure-closed behavior are defined in [server execution and trust](spec/server.md).

**Why.** Recovery needs current selections but must not turn a public guide into an instance inventory. The server is replaceable; the trusted host holds bootstrap logic, reviewed source, account declarations, public keys, secret references, client packs, and the evidence needed to reproduce it.

**Recipe.** Keep the known-good ostree deployment pinned through every lock-out-class change and a deliberate observation window. If routine SSH fails, try the same confined administering identity at the console. If policy prevents its transition, use the provider rescue protocol (`proto:coreos:rescue`) and inspect the installed system through the console or a bounded replica. Verify the rescue host key independently; a one-boot activation is consumed when rescue boots and must be renewed for another rescue boot. Repair only the reviewed configuration or select the pinned deployment. Remember that `/etc` and `/var` persist across deployment changes, so restore reviewed configuration bytes explicitly rather than assuming an image rollback reverses them.

For replacement, start with an empty host and the private registry row, validate ownership and freshness, install the platform baseline, restore the confined administering login and the independent provider rescue path, transfer the reviewed bootstrap program and declared inputs from the workstation, and reconcile accounts, access, storage, toolchains, hubs, doors, and services in this guide's order. Repopulate hubs only from reviewed workstation source, force disposable checkouts to declared objects, and run the complete verification checklist. Surviving bytes from the old server remain untrusted recovery evidence; material that must be kept first returns through quarantine and review.

**Probe.** Perform a dry-run bootstrap against the converged machine and require no duplicate account, key, hub, route, timer, or permission broadening. Exercise the provider rescue path and confirm the rollback entry is selectable before unpinning it. Finally, prove from a clean staging environment that host-held inputs alone can recreate a loop account, its alias-scoped access, disk-backed surfaces, exact hub input object, wrapper report, and timers without reading the predecessor server.
