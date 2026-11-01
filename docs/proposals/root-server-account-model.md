# Root-server account model · `proposal:serveraccounts:root-server-account-model`

Status: RATIFIED — every question this document raised was ruled by the owner, and the model was deployed on the estate's first root-capable server the same day. Live state, interim deviations, and the measured administration recipes live in the server registry and [confined-admin.md](../confined-admin.md); this document records the decided model.

## Purpose · `sec:serveraccounts:purpose`

A legacy shared-host deployment can lack real root: every loop works inside one unprivileged container, management is an outside actor, and the machine cannot express who owns it. A root-capable server changes the question from "how do we squeeze loops into one account" to "who owns the machine, who may rescue it, and who may merely use it." This model answers with four account classes, each defined by the single capability that justifies it.

## The four account classes · `sec:serveraccounts:the-four-account-classes`

### 1. `owner` — the machine owner · `sec:serveraccounts:1-owner-the-machine-owner`

Claude Code, registered under the estate's own account, is installed in a dedicated account holding wheel. This account owns the server: all maintenance — package updates, service changes, account creation, configuration — happens through this instance, so every administrative act lands in a session transcript and is reviewable the same way lane evidence is. The orchestration superloop holds the SSH key for this account, because machine maintenance is orchestration-estate work: other loops request changes, they do not make them.

The account authenticates by key only, and its `sudo` is passwordless: an agent holds no password to type, and the account's whole authentication story is possession of the key. Wheel membership rather than uid 0 keeps privileged acts explicit (`sudo` lines in the journal) instead of ambient.

### 2. `administrator` — the human rescue path · `sec:serveraccounts:2-administrator-the-human-rescue-path`

A human emergency account, also in wheel, for the cases automation cannot reach: the agent account wedged, the network path to it broken, a bad policy locking everyone else out. Three properties are deliberately unique to it:

- It is the only account in the system with a password. Everything else is key-only, so password attack surface exists exactly where console rescue requires it and nowhere else.
- It is the only account with an unconstrained SELinux context. Rescue must not be confineable by the very policy being rescued.
- It is not used for routine work. Routine use would erode both exceptions into normal-operations surface.

Its `sudo` requires the password: the human path keeps a second factor between a seized session and root, which costs a human seconds and costs an attacker the only password in the system.

Everyone else — including `owner` — runs in the `staff` SELinux context, and the system default for new users is `staff`. The unconfined context is then a measured exception held by one human account, not a default anyone inherits.

SELinux is enforcing from day one. A permissive bootstrap would mean the machine's first and most formative configuration work happens outside the regime everything afterward must live under, and the switch-on day inherits an unknown pile of latent denials; enforcing from the start makes every denial a bootstrap finding fixed at the moment it appears, and the rescue path for a policy mistake is exactly what `administrator` exists for.

A Fedora 44 reference deployment provides evidence of one known cost of `staff` confinement: a `staff_u` user cannot run rootless podman or Toolbx at all, because `staff_r` is not authorized for the container process types and the failure surfaces as a bare permission error with no AVC record ([archived bug report](../reference/bugreport-staff_t-container_t.md), with a local policy-module workaround granting `role staff_r types spc_t`). The module's scope is measured, not guessed: the tested policy already authorizes `staff_r` for `container_t`, so exactly the one `spc_t` authorization is missing, and the reference bootstrap ships it as a deliberate policy module rather than discovering the failure in production.

### 3. `public` — the shared showcase · `sec:serveraccounts:3-public-the-shared-showcase`

A passwordless account for presentations, kiosk displays, and anything meant to be seen: humans may view and interact with it freely. There is no shared key: every superloop's own key is added to this account's authorized keys by `owner`, so any loop can publish or update what the account shows while every SSH appearance remains attributable to exactly one loop's key, and revoking one loop touches nothing but its own line. Nothing secret and nothing privileged lives here — no wheel, staff context.

Exactly two entry paths exist, and `su` into `public` is not one of them: a human at the physical console logs in without a password, and everything else arrives over key-only SSH. Passwordless login is therefore bound to physical presence — the property that makes it safe — and never becomes a remote door. Blocking `su` (and `sudo -u public`) keeps every appearance of the account attributable to one of the two sanctioned paths; a switched-user session would let any local account wear the showcase identity without its key, turning the least-privileged account into an unattributed lateral hop.

Applications reach this account the way they reach every human seat on the estate: the server runs its software through podman and toolbox, so an app a loop wants to present is installed in a container and linked out by a desktop file whose `Exec` runs it inside its toolbox. What the console session offers a human is exactly the set of desktop files the loops have published — an app without one is agent-reachable only, which makes the desktop-file set the reviewable inventory of everything the showcase exposes. The archived rootless-podman constraint above applies here with force: `public` is a confined `staff` account expected to run containers, so the bootstrap's role-type authorization module is a prerequisite for the showcase working at all.

### 4. Per-superloop accounts — the workers · `sec:serveraccounts:4-per-superloop-accounts-the-workers`

Each superloop generates its own SSH key, and `owner` installs that one key into two authorized-keys files: the loop's own account and `public`. Separate uids keep loop evidence, budgets, and disk attributable, and a leaked key exposes one loop, not the estate — the same single-key revocation also closes that loop's `public` access. These accounts hold no wheel and no passwords; their compute discipline (nice batch builds, per-loop workspaces, TMPDIR) carries over from the existing bootstrap unchanged.

## Custody summary · `sec:serveraccounts:custody-summary`

|Account|Wheel|Password|SELinux|Key custody|
|-------|-----|--------|-------|-----------|
|`owner`|yes|none|staff|machine operator|
|`administrator`|yes|the only one|unconstrained (only one)|human owner|
|`public`|no|none|staff|no key of its own; every loop's key admitted by `owner`|
|`<loop>` (one per superloop)|no|none|staff|that loop alone|

## What changes against the current model · `sec:serveraccounts:what-changes-against-the-current-model`

In a legacy shared-host model, a provider-controlled, management-only account can sit outside the deployment's trust story; in the root-capable model, the machine owner is an agent account whose acts land in transcripts. Account bootstrap consequently moves from being pushed by a root actor on a management host to the `owner` account executing it in place. Reference-deployment evidence shows that an existing registry convention (a bird name in the server's local language, aliases in `~/.ssh/config`, and no raw addresses in documents) can remain unchanged, while stable per-loop key filenames outlive individual servers and carry over as-is.

## Rollback before surgery: pin the ostree deployment · `sec:serveraccounts:rollback-before-surgery-pin-the-ostree-deployment`

On an ostree-based system the machine keeps a bootable ledger of prior deployments, and that ledger is the cheapest insurance the platform offers: before any serious change to the parts of the system that can lock everyone out — SELinux policy modules or booleans, PAM stacks, sudoers, the login and getty configuration — pin the current known-good deployment so it survives the automatic pruning that would otherwise drop it. A confined SELinux server makes this doubly warranted, because the failure mode of policy surgery is exactly the loss of the access needed to undo it: a bad module can wedge every account at once, and even the `administrator` rescue path is only as good as a machine that still boots the policy it was reached under. A pinned deployment turns that class of mistake from a reinstall into a reboot into the previous entry.

The mechanism is `sudo ostree admin pin <index>` (equivalently `rpm-ostree` deployment pinning) on the running deployment before the change, and unpinning once the new state has been exercised long enough to trust — pins are removed deliberately, not left to accumulate, so the ledger stays short and its meaning stays legible. The measured administration recipes this pinning protects live in [confined-admin.md](../confined-admin.md).

## Open questions for the owner · `sec:serveraccounts:open-questions-for-the-owner`

None — every question raised by this document has been ruled on. The model is ready to fold into the server registry and the bootstrap when the server arrives.
