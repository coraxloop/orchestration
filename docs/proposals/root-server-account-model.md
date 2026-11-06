# Root-server account model · `proposal:serveraccounts:root-server-account-model`

Status: RATIFIED in its four-class form for the Silverblue deployment, and amended for the root-full FCOS baseline to the model that baseline's first deploy measured: one confined administering login, no separate owner or unconfined administrator login, and independent provider rescue. The earlier Silverblue account split is historical evidence, not the current provisioning recipe. Live identities and key custody stay in the private registry; the setup recipe is (`sec:rootserver:the-account-model`).

## Purpose · `sec:serveraccounts:purpose`

A legacy shared-host deployment can lack real root: every loop works inside one unprivileged container, management is an outside actor, and the machine cannot express who owns it. A root-capable server changes the question from "how do we squeeze loops into one account" to "who owns the machine, who may rescue it, and who may merely use it." This model separates the administering login, independent recovery, optional presentation and unprivileged loop roles without creating a second administrative login.

## Account roles and recovery · `sec:serveraccounts:the-four-account-classes`

### 1. The confined administering login · `sec:serveraccounts:1-owner-the-machine-owner`

One registry-selected account administers the host. Its login maps to `staff_u`; its approved sudo group crosses explicitly to `sysadm_r:sysadm_t`. Maintenance runs under the estate's authority with a retained transcript and journal evidence. Other loops request privileged changes rather than acquiring this account's key. The account name is a registry value, not a requirement to create a literal `owner` login.

SSH authentication is key-only. The reviewed sudo rule permits the explicit transition without an interactive password so that authorized maintenance can run noninteractively. This is root-equivalent administrative authority, not confinement of what an authorized administrator can change. A console password, where required by the recovery arrangement, stays in external owner custody and does not enable SSH password authentication.

### 2. Independent recovery, not another login · `sec:serveraccounts:2-administrator-the-human-rescue-path`

Every installed-system login is confined, including console administration; no unconfined rescue account is provisioned. A network failure may leave the same administering login usable at the console. A policy failure that blocks its transition requires the independent provider rescue path (`proto:coreos:rescue`), with the rescue key and host identity checked before access. Keep this route proven before depending on a reboot or policy change.

Declare the default and explicit staff mappings, sudoers and required local modules in the installation input. Rebuild the login store and validate sudoers in the first-boot identity unit before sshd, so confinement holds from the first session (`setup:coreos:first-boot-identity`). SELinux remains enforcing throughout; a failed identity setup is not repaired by admitting an unconfined routine login.

The 2026-08-28 Fedora 44 container evidence remains scoped to the missing role authorization: ordinary rootless `container_t` containers worked, while privileged or label-disabled `spc_t` containers and Toolbx were refused. The documented `staff_r` authorization for `spc_t` is retained in the first-boot input and probed from a confined loop login (`sec:confinedadmin:containers-one-missing-role-authorization`).

### 3. `public` — the shared showcase · `sec:serveraccounts:3-public-the-shared-showcase`

This optional graphical role is absent from a headless compute node. Where separately selected, it is a passwordless account for presentations, kiosk displays, and anything meant to be seen: humans may view and interact with it freely. There is no shared key: every superloop's own key is added to this account's authorized keys by the administering account, so any loop can publish or update what the account shows while every SSH appearance remains attributable to exactly one loop's key, and revoking one loop touches nothing but its own line. Nothing secret and nothing privileged lives here — no wheel, staff context.

Exactly two entry paths exist, and `su` into `public` is not one of them: a human at the physical console logs in without a password, and everything else arrives over key-only SSH. Passwordless login is therefore bound to physical presence — the property that makes it safe — and never becomes a remote door. Blocking `su` (and `sudo -u public`) keeps every appearance of the account attributable to one of the two sanctioned paths; a switched-user session would let any local account wear the showcase identity without its key, turning the least-privileged account into an unattributed lateral hop.

Applications reach this account the way they reach every human seat on the estate: the server runs its software through podman and toolbox, so an app a loop wants to present is installed in a container and linked out by a desktop file whose `Exec` runs it inside its toolbox. What the console session offers a human is exactly the set of desktop files the loops have published — an app without one is agent-reachable only, which makes the desktop-file set the reviewable inventory of everything the showcase exposes. The archived rootless-podman constraint above applies here with force: `public` is a confined `staff` account expected to run containers, so the bootstrap's role-type authorization module is a prerequisite for the showcase working at all.

### 4. Per-superloop accounts — the workers · `sec:serveraccounts:4-per-superloop-accounts-the-workers`

Each superloop generates its own SSH key, and the administering account admits it to that loop's account; admission to a separately selected showcase is an additional role, not a compute-node prerequisite. Separate uids keep loop evidence, budgets, and disk attributable, and a leaked key exposes one loop, not the estate — revocation also removes any separately authorized showcase admission. These accounts hold no wheel and no passwords; their compute discipline (nice batch builds, per-loop workspaces, TMPDIR) carries over from the existing bootstrap unchanged.

## Custody summary · `sec:serveraccounts:custody-summary`

|Role|Administrative group|Password|SELinux|Key custody|
|----|--------------------|--------|-------|-----------|
|Administering login|yes|console only if selected; SSH key-only|staff, explicit sudo to sysadm|estate operator; console credential in owner custody|
|Provider rescue|outside the installed login model|provider procedure|independent recovery environment|owner-controlled rescue key and verified provider identity|
|Optional showcase|no|physical-console entry only|staff|separate loop keys admitted by the administering account|
|Loop or staff login|no|locked|staff|that account's own custody|

## What changes against the current model · `sec:serveraccounts:what-changes-against-the-current-model`

In a legacy shared-host model, a provider-controlled, management-only account can sit outside the deployment's trust story; in the root-capable model, the machine owner is an agent account whose acts land in transcripts. Account bootstrap consequently moves from being pushed by a root actor on a management host to the registry-selected confined administering account executing it in place. Reference-deployment evidence shows that an existing registry convention (a bird name in the server's local language, aliases in `~/.ssh/config`, and no raw addresses in documents) can remain unchanged, while stable per-loop key filenames outlive individual servers and carry over as-is.

## Rollback before surgery: pin the ostree deployment · `sec:serveraccounts:rollback-before-surgery-pin-the-ostree-deployment`

On an ostree-based system the machine keeps a bootable ledger of prior deployments, and that ledger is the cheapest insurance the platform offers: before any serious change to the parts of the system that can lock everyone out — SELinux policy modules or booleans, PAM stacks, sudoers, the login and getty configuration — pin the current known-good deployment so it survives the automatic pruning that would otherwise drop it. A confined SELinux server makes this doubly warranted, because the failure mode of policy surgery is exactly the loss of the access needed to undo it: a bad module can wedge every account at once, and the installed console login is subject to that same policy, so provider rescue remains independent of it. A pinned deployment turns that class of mistake from a reinstall into a reboot into the previous entry.

The mechanism is `sudo ostree admin pin <index>` (equivalently `rpm-ostree` deployment pinning) on the running deployment before the change, and unpinning once the new state has been exercised long enough to trust — pins are removed deliberately, not left to accumulate, so the ledger stays short and its meaning stays legible. The measured administration recipes this pinning protects live in [confined-admin.md](../confined-admin.md).

## Open questions for the owner · `sec:serveraccounts:open-questions-for-the-owner`

None — every question raised by this document has been ruled on. Provisioning follows the root-full recipe and records its acceptance separately; a ratified model is not a live acceptance result.
