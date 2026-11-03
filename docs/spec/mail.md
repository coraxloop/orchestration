# Superloop mail system · `spec:mail:superloop-mail-system`

The superloop mail system is the single correspondence system for every loop and every worker on a host. It replaces the letters system, including its separate worker transport. This part owns mail identity, storage, delivery and notification; dispatch and instruction authority remain with (`rule:architecture:charter-plus-brief`) and (`rule:architecture:audience-separation`). Every label minted here has area `mail`.

## Domain and names · `sec:mail:domain-and-names`

**Definition (Letter)** · `def:mail:letter`

A letter is an uninterpreted finite byte string, including an empty string. Text encoding, headers, subject, line count, syntax and meaning impose no admission constraint. All metadata lives outside those bytes, in the filename and service records. Delivery preserves every byte; it neither decodes a body nor prepends an envelope. A regular file carries the letter; file-kind and publication checks protect transport, not content.

**Definition (Letter size constant)** · `def:mail:maximum-letter-bytes`

`MAX_LETTER_BYTES = 1048576` is the inclusive byte-size bound on one submitted letter. The service bounds its read to this value plus one byte and refuses overflow, including growth after a size observation. One MiB permits substantial correspondence while bounding a delivery's buffering and copy cost; larger artifacts travel by reference in a letter, without giving that reference authority. This is the only content limit.

**Definition (Address)** · `def:mail:address`

A loop address is its exact registered name, `LOOP`. A worker address is `LOOP+WORKER`, qualified by the loop that gave it birth. These names are case-sensitive ASCII tokens under (`lang:mail:names`); there are no aliases, implicit current-loop recipients, external addresses or path-valued recipients. Qualification separates loop names from worker names and lets different loops choose the same worker name without ambiguity. The sender address is derived from the registered outbox being serviced, never supplied by the body or an outgoing filename.

**Register (Identity name grammar)** · `reg:mail:identity-names`

This is the single normative name register cited by both the host loop registry validator and the mail grammar. Loop names and worker birth names use the same production: a nonempty sequence of lowercase ASCII letters, digits or hyphens whose first byte is a letter or digit, with no lexical length bound. A leading hyphen is excluded because every inbox and sent filename begins with an address, and ordinary `ls`, `cat` and `mv` would read such a name as an option. The registry and launcher validate this production without introducing a narrower mail-only name class.

```abnf
name = (%x61-7A / %x30-39) *(%x61-7A / %x30-39 / %x2D)
```

|Identity|Production|Consumer|
|--------|----------|--------|
|Loop name|`name`|Host loop registry and mail address resolver.|
|Worker birth name|`name`|Loop worker directory, birth launcher and mail address resolver.|

**Language (Mail names)** · `lang:mail:names`

The ABNF below fixes ASCII bytes, using numeric terminals for case-sensitive literals. `name` is imported exactly from (`reg:mail:identity-names`); `DIGIT` is defined here, and repetition and alternation have their ordinary ABNF meanings. `RECIPIENT` and `SENDER` both use `address`. A delivery instant has exactly the form `YYYY-MM-DDTHH:MM:SS.mmmZ`, with three fractional digits, uppercase `T` and trailing uppercase `Z`.

```abnf
DIGIT = %x30-39
lower = %x61-7A
loop = name
worker = name
address = loop [ %x2B worker ]
slug = 1*64(lower / DIGIT / %x2D)
letter-suffix = %x2E.6C.65.74.74.65.72
outgoing = address %x2E slug letter-suffix
incoming = address %x2E delivery letter-suffix
sent-name = address %x2E delivery letter-suffix
delivery = 4DIGIT %x2D 2DIGIT %x2D 2DIGIT %x54
           2DIGIT %x3A 2DIGIT %x3A 2DIGIT %x2E 3DIGIT %x5A
```

`delivery` additionally denotes a valid Gregorian UTC instant in years 0001 through 9999, hours 00 through 23, minutes and seconds 00 through 59, and milliseconds 000 through 999. Leap-second spelling is not used: delivery waits for a representable instant. Numeric ABNF permits parsing before calendar validation. Slugs sort by unsigned ASCII byte order, independent of locale; a sender uses fixed-width numeric prefixes when it wants numeric order. Names exclude dots, slashes and plus signs so the address and slug boundaries are unambiguous; the timestamp's dot belongs to the timestamp. No normalization or case folding occurs. Filesystem component and path limits are storage constraints, not a second name grammar: provisioning and submission must report an explicit unavailable endpoint or unrepresentable full filename when the backing filesystem cannot store a valid name. They must never truncate, hash, alias or silently reject it as lexically invalid; name alignment does not promise that a finite filesystem stores arbitrarily long components.

**Definition (Mail folder)** · `def:mail:folder`

All mail resides beneath the host's loops root `~/.var/loops`; `~` in this part always means the host home containing that root, never a loop's or box's home. A loop's folder is `~/.var/loops/LOOP/mail`; a worker's is `~/.var/loops/LOOP/workers/WORKER/mail`. Each folder contains exactly the five directories below. Service records are outside these folders. `draft` and `read` names have no mail grammar beyond the filesystem's single-component constraints.

|Directory|Letter name|Use and transition|
|---------|-----------|------------------|
|`draft`|Unstructured|The actor composes bytes here, then closes the file and atomically renames it into its own `outbox` with a valid outgoing name.|
|`outbox`|`RECIPIENT.SLUG.letter`|Submission to the service; the actor does not modify a published letter while it is queued. The service moves it to the recipient's `inbox` and leaves a copy in the sender's `sent`.|
|`sent`|`RECIPIENT.DELIVERY.letter`|Service-published copy of the delivered bytes, readable by the sender.|
|`inbox`|`SENDER.DELIVERY.letter`|Service-published incoming bytes; the recipient reads them or moves the letter into its own `read`.|
|`read`|Unstructured|The recipient chooses a noncolliding name when moving a letter from `inbox`; this is the durable read history and the destination for migrated letters.|

**Invariant (Authority follows sender role)** · `inv:mail:data-not-authority`

Authority follows the sender's role, not the mail transport. A letter from a worker's own loop steers that worker at any moment of the run: it redirects, narrows, widens or corrects the task as the next step's brief, within (`rule:architecture:charter-plus-brief`). The sender must be established as that worker's principal through service delivery evidence, not merely claimed in a filename or body. Every other letter, including another loop's letter to the worker, another worker's letter and all loop-to-loop correspondence, is data, never authority. Neither kind bypasses a hard charter rule, grants a trusted verdict or automatically resumes a paused lane. Returned server material remains data under (`rule:architecture:server-results-are-data`).

**Protocol (Steering and resumed rounds)** · `proto:mail:round-transport`

The loop sends its steering letter through its own outbox to its worker's address. The service delivers it to the worker's inbox and assigns the delivery instant. The launcher learns the resulting inbox name from the service's delivery journal or the corresponding sent copy verified against that journal, binds it to this worker and step, and resumes the round with a prompt naming `/mail/inbox/SENDER.DELIVERY.letter` as the step's brief. The launcher's ordinary resume authorization remains required; an arrival notice is not a launch instruction. A running worker checks and reads its inbox between commands so its own loop can steer it within the round.

The launcher preserves the exact steering bytes as `step-<step>.txt` beside the round's brief before resume, for the watcher's evidence; it does not move or repurpose that evidence as a mailbox. The reservation replaces its legacy `letters` records with a `mail` delivery binding that records the sender, recipient, delivery instant, journal identity, delivered inbox name, step and evidence digest instead of selecting a legacy letter file. If the worker has already moved the named inbox file, the launcher does not guess another file or resume with a dangling brief: it reconciles the same delivery with the worker before resume or obtains a new steering delivery. A missing, mismatched or unverified delivery blocks that resume.

The round transport retires `send-letter`, `withdraw-letter` and `launch --round`'s legacy letter-file selection. Withdrawal before service acceptance uses the sender's outbox; a delivered instruction is corrected by a new steering letter, not erased. The legacy reservation `letters` schema is retired after its evidence is mapped to the `mail` delivery binding; no old-schema reader remains.

## Identity and directories · `sec:mail:identity-and-directories`

**Rule (Worker birth name)** · `rule:mail:worker-birth-name`

The creating loop assigns a `worker` name under (`lang:mail:names`) when it creates the worker's home, before the first harness process starts. The name is unique within that loop and stable for the worker's whole life, across process exits, rounds, provider resumes and box replacement that preserve worker identity. A replacement dispatch with a new worker gets a new name. Names are never reused: the loop retains retired entries, so delayed mail cannot reach a different worker. A name identifies a mailbox, not standing authority or a permanent agent role (`def:architecture:worker`).

**Definition (Loop configuration)** · `def:mail:loop-configuration`

The loop uid owns `ENTERED_HOME/.config/mail/loop.toml`, where `ENTERED_HOME` is the loop's private entered home, `~/.var/loops/LOOP/private` on the host. Thus its host path is `~/.var/loops/LOOP/private/.config/mail/loop.toml`, not a file beside host-owned box settings. This one TOML file declares its worker directory and the directed worker-to-worker whitelist. It is loop configuration, maintained by that loop and its trusted birth launcher, not a user-maintained or operations-maintained roster. Its mail schema is `mail.version = 1`; `workers` is an array of tables with exactly `name` and `state`, where state is `active` or `retired`; `mail.allow` is an array of tables with exactly `from` and `to`, each a worker birth name in this file. Other loop configuration may coexist outside these reserved keys. Empty arrays are explicit, duplicate worker names or duplicate edges are invalid, and unknown mail fields, dangling edges or nonconforming names invalidate the mail configuration. The following fictional shape permits one direction only:

```toml
workers = [
  { name = "producer-01", state = "active" },
  { name = "reviewer-01", state = "active" },
]

[mail]
version = 1
allow = [
  { from = "producer-01", to = "reviewer-01" },
]
```

The file and its configuration directory are owned by the loop uid; only that uid writes them, with the birth launcher operating through the loop entry. A named POSIX ACL grants the mail service's mapped uid read access on this one file and search-only access on the required ancestors, with no directory-list permission or access to sibling private files. The ACL mask must preserve those effective permissions. A per-file ACL is chosen over a shared group or default directory ACL because it does not expose other private material or grant access to future files. Before atomically replacing the configuration, the loop validates the full contents, sets the replacement inode's loop ownership and service read ACL, and verifies ancestor traversal; replacement must neither lose service access nor widen it. The service reads a fresh complete snapshot at each delivery decision and records its digest, never relying on a cached grant after replacement. Missing, unreadable, invalid or untrusted configuration refuses the affected worker delivery. Retirement is an atomic state change; birth names and retired entries are retained for the loop's lifetime. Recovery restores the loop-owned configuration from its backup and reconciles it with provisioned homes before delivery resumes; absence never means an empty permissive whitelist (`rule:architecture:stable-constraints-govern-registries`).

**Protocol (Recipient resolution)** · `proto:mail:resolve`

1. Parse the exact address under (`lang:mail:names`). Resolve its loop only in the existing host superloop directory, `~/.config/loops/registry.toml`, whose registration authority and loop identities remain unchanged.
2. Derive `ENTERED_HOME/.config/mail/loop.toml` solely from the loop registry row's registered loop home and uid: the entered home is that loop home's `private` tier. Verify the file's loop ownership and service ACL through opened descriptors, never search host configuration directories or accept a worker-supplied path. For a qualified address, resolve its worker only in this file, requiring an active entry. A loop address needs no worker lookup. Derive the mail path from the registered names under (`def:mail:folder`), never from a body, symlink, search path, run directory or another address book.
3. Establish sender identity from the opened, provisioned outbox. For a worker sender, require its active birth entry and require that the recipient loop is its own superloop. A worker may send to that loop itself without a whitelist edge; any worker recipient additionally requires the exact directed `from`/`to` edge, including self-mail. A loop sender may address any registered loop or active worker.
4. Recheck that the selected registry snapshots and endpoint identities remain current at acceptance; serialize configuration updates against that decision or retry on replacement. A later revocation does not undo a delivery already accepted under the recorded snapshots.

These two directories are the only recipient resolution sources. Service journals can recover an accepted transaction but cannot register an address or supply a missing grant. Missing, ambiguous or invalid global registration fails closed for the affected resolution. No worker can relay outside its estate by naming another loop; a receiving loop's later decision to send new mail remains its own act.

**Rule (Ownership and confinement)** · `rule:mail:ownership`

The mail service runs as a dedicated subordinate uid in the host session's existing user namespace, distinct from every loop and worker uid. The host session's `superloop-mail.service` user unit enters that namespace and drops to the service uid through the existing identity-entry machinery. It neither allocates a host system account nor requires host root. Provisioning reserves the uid and mapped groups without overlap and gives the service access to registered mail trees, its private journal and the single-file configuration ACLs; it holds no loop credential and executes no letter.

The service owns each mailbox root, `inbox`, `sent` and delivered letter inodes. Each mailbox has an actor-specific mapped group, with no peer actor membership: the root is searchable but not writable by the actor, `inbox` and `sent` have group read, write and search permission, and delivered files have group read permission but no actor write permission. The actor owns `draft`, `outbox` and `read`; service ACLs permit claiming submissions and publishing refusal records. Ancestors and mount points cannot be replaced by that actor. Ordinary group-write directory permission lets the recipient move an inbox letter into its own `read`; by protocol that is the actor's only mutation of inbox or sent. Actors must not insert, rename within, remove from sent or alter letters there.

These modes isolate actors from each other's folders, but do not pretend that directory group write mechanically prevents an actor inserting or replacing an entry in its own folder. Provenance comes from the service's protected delivery journal: sender, recipient, delivery instant, size and digest must match, and an unrecorded or mismatched local entry is reported as `forged-local-entry`, never accepted as a delivery or a steering brief. Verification requires recorded inbox publication or its journaled rename witness, not merely an accepted or sent-only transaction. A consumer requiring sender authority obtains a journal verification from the service, scoped to its own address; the trusted launcher performs that check for resumed rounds and supplies the same verification for in-round steering. Verification returns delivery metadata and a verdict, not letter content or a second listing/reading interface. Filenames, modes, local sidecars and copies alone cannot establish the principal. The service never repairs a forgery by generating a delivery record for it.

Mandatory access control or a policy-enforcing filesystem view is optional hardening against local insertion, not a mailbox activation condition. The required boundary is separate subordinate identities, restricted mailbox mounts and journal-backed provenance, with opened-object checks under (`rule:architecture:opened-object-identity`). Identity collisions, peer access or an unprotected journal still block activation. Any stronger host policy must declare its privileged provisioning separately; it is not an implicit requirement of the user unit.

**Rule (Worker box mount)** · `rule:mail:box-mount`

The launcher mounts only that worker's mail folder read-write at `/mail` inside its box and identifies `/mail` in the worker's launch context. Read-write describes mount capability, not permission to write every directory: (`rule:mail:ownership`) still governs every operation. The box receives no ancestor bind, peer mailbox, loop mailbox, service state, configuration file, inherited descriptor or host escape that reaches another mail folder. Its namespace privileges cannot remount or bypass the host enforcement. The same worker gets the same folder on resume; a new worker receives a distinct folder and isolated identity. Ordinary `ls`, `cat` and `mv` operate on `/mail`; no mail-reading API or custom mailbox shell is required.

**Ansatz (Filesystem-only provenance)** · `ansatz:mail:discretionary-modes`

Rejected: treating a filename or discretionary mode as proof of service delivery. Group write needed for ordinary inbox extraction also permits local insertion; a sticky bit cannot supply provenance, and a read-only mount prevents extraction. Separate subordinate identities protect peers while a protected journal establishes provenance. Requiring a host system user, unrestricted root daemon or mandatory host policy would add privileged machinery without changing that provenance rule; optional hardening may supplement it.

## Delivery service · `sec:mail:delivery-service`

**Definition (Service responsibility)** · `def:mail:service`

The program `superloop-mail` and its host-session user service unit `superloop-mail.service` have one mail job: deliver submitted bytes from outboxes into recipient inboxes with sender copies and attributable delivery records. They do not interpret correspondence, select work, resume workers or synthesize replies. One instance serializes delivery for the entire host loops root; a service-owned exclusive lock prevents a second writer. Administrative provisioning, storage enforcement and migration support this contract but do not become alternative correspondence transports.

**Rule (Delivery order and clock)** · `rule:mail:delivery-order`

The service takes a finite scan of registered outboxes, sorts senders by address byte order, and visits them round-robin, one candidate per sender per pass. Within each sender's scan it orders candidates by `(SLUG, RECIPIENT)` byte order, so recipient prefixes do not override the sender's chosen slug order. Identical recipient/slug names cannot coexist; publication refuses overwrite. New submissions join the next scan, not the front of an existing scan. A refused candidate is reported and skipped for that scan, so it cannot block later mail. There is no promised ordering between letters not yet published at scan time.

Only the service assigns `DELIVERY`, from the actual host UTC clock at millisecond precision. After any reserved delivery instant, it sleeps until a later millisecond tick before reserving another; if more letters wait, none bypasses that sleep. It persists the greatest reserved instant before publication and never reuses an instant, even across senders, refused transactions, service restart or clock rollback. If UTC is not strictly later than that watermark, it waits without delivering; it never invents a future timestamp. A rollback, unavailable clock or exhausted representable year is a recorded service condition. The discipline provides unique names and total delivery order, not a claim of simultaneous writes to two directories.

**Protocol (Delivery transaction)** · `proto:mail:deliver`

1. Select a candidate in (`rule:mail:delivery-order`), resolve and authorize under (`proto:mail:resolve`), and inspect it through opened directory descriptors. Refuse nonregular files, symlinks, multiply linked submissions, invalid names, unavailable endpoints or invalid ownership and cross-actor isolation. Never follow a submitted path outside its outbox.
2. Claim the outgoing entry exclusively and take a bounded copy into a service-owned immutable temporary file on the recipient inbox's filesystem. A sender closes writable descriptors before submission; detected mutation during copying refuses the submission. The service snapshot, not any retained sender descriptor, supplies all delivered bytes. Validate the inclusive size limit and digest, sync the file and its containing directory, and preserve the claimed source until completion or safe prepublication refusal.
3. At acceptance revalidate the registry snapshots, reserve and persist a fresh UTC delivery instant, and write and sync the journal record and journal directory before any publication. Record the source identity, sender, recipient, size, digest, configuration digests, exact private temporary name and opened filesystem identity, final sent and inbox names, and phase `accepted`. The private temporary is a publication witness: after this durable record, the service may remove that name only by the recorded atomic inbox rename or by the separately journaled discard protocol.
4. Link the journaled immutable temporary into the sender's `sent` when both filesystem support and the required sender/recipient read permissions permit sharing that inode, or copy its bytes to a journaled sender-side temporary, sync it and atomically rename it into `sent`. Both paths refuse overwrite and sync the sent directory. Persist phase `sent`. Then atomically rename the recipient-side journaled temporary to `SENDER.DELIVERY.letter` in `inbox`, on that same filesystem and without replacement, and sync both affected directories. Never implement inbox publication as copy-and-unlink or unlink-and-create; the disappearance of that temporary name must denote the one rename.
5. Persist phase `inbox`, clean up only the matching claimed source and refusal sidecar, and mark the transaction `complete`. A recipient may immediately move the inbox entry into `read` with ordinary `mv`, without a service callback. The source-to-inbox move is complete even if the source and recipient were on different filesystems: copying into the recipient-side private temporary precedes the one publication rename. A sent copy alone is not proof of inbox publication; the phase and publication witness decide it.

Each endpoint has a service-only `0700` staging directory outside its five-directory mail folder but under the loops root: `~/.var/loops/LOOP/.mail-staging` for a loop, or `~/.var/loops/LOOP/workers/WORKER/.mail-staging` for a worker. Provisioning must put that directory on the same filesystem as its endpoint's inbox and sent directories and protect its ancestors against actor replacement. Device identity is checked before publication. The service journals the exact temporary paths; it does not rediscover them by scanning another address directory. The backing filesystem must provide crash-consistent atomic rename and durable file and directory sync; an unsupported storage configuration refuses activation rather than weakening the witness.

**Invariant (Recovery preserves one delivery)** · `inv:mail:delivery-recovery`

Restart re-reads the protected journal before accepting new mail. For an `accepted` or `sent` transaction whose recipient temporary still exists with the recorded identity and digest, inbox publication has not happened: finish the sender copy if needed and perform the recorded rename exactly once. If that temporary is absent, and no durable discard decision exists, the journal's publication ordering proves the inbox rename occurred; mark inbox publication and finish source cleanup without recreating an inbox entry, even if the recipient already moved or removed it. The inbox pathname is never the recovery oracle. Recovery from phase `inbox` or `complete` likewise never republishes.

Only a transaction whose recipient temporary still exists can be discarded before publication. First journal and sync phase `discarded` with its reason and the recoverable source disposition; only then remove temporary artifacts and any matching incomplete sender copy, leaving or restoring the exact source in the sender's outbox with a refusal reason. If source restoration cannot be made without overwrite, keep the protected payload and the transaction pending for repair. A crash during discard resumes discard rather than interpreting the now-absent temporary as publication. An unjournaled temporary is unpublished and can be reclaimed after its source is reconciled; it is never delivered on inference.

Recovery relies on the service being the only writer of its journal and staging and on the declared crash-consistent filesystem. A mismatched temporary, corrupt journal or failed durability guarantee stops the affected transaction for reconciliation; it is not permission to guess. The same reserved instant is retained across all retries, and neither an actor's ordinary inbox move nor a missing inbox entry requires coordination with the service.

**Definition (Service records)** · `def:mail:records`

The service solely maintains `~/.var/loops/.mail-service/`, outside all actor mail folders and invisible to worker boxes. Its `state.toml` stores schema version 1 and the greatest reserved delivery instant. Its `deliveries/DELIVERY.toml` records schema version 1, sender and recipient addresses, original outgoing name, byte length, SHA-256 digest, global-registry and applicable loop-configuration digests, acceptance instant, source identity, sent and inbox names, exact temporary paths and filesystem identities, phase (`accepted`, `sent`, `inbox`, `complete`, `discarded`), terminal completion instant when present, and any pending error or discard disposition. Acceptance instant equals `DELIVERY`; phase transitions are durable atomic record replacements. Private endpoint `.mail-staging` directories hold the journaled payloads on their publication filesystems under (`proto:mail:deliver`); this state root holds the service lock and their records. These records are delivery metadata, never letter contents or an additional address directory.

Delivery records and private payloads follow the bounded retention classes in (`rule:mail:retention`); only the fixed-size watermark and current summary checkpoint persist for the loops root's lifetime. Backups preserve journal, checkpoint, watermark and mail trees as a coordinated set. Restore reconciles pending phases and compaction before service start and must not lower the watermark or discard evidence of publication. Missing or corrupt recovery state stops delivery for reconciliation; intentional compaction is recognized only through its durable checkpoint. Actors receive only verification or refusal information scoped to their own address; administration can inspect the private journal without becoming its writer (`rule:architecture:mutable-state-ownership`).

**Definition (Retention constants)** · `def:mail:retention-constants`

`JOURNAL_HISTORY_SECONDS = 2592000` retains full terminal records for thirty days before ordinary compaction. `JOURNAL_MAX_BYTES = 268435456` caps the aggregate service journal, checkpoints and record-replacement scratch at 256 MiB. `STAGING_MAX_BYTES = 67108864` caps the aggregate private payload staging across all endpoint filesystems at 64 MiB, including claimed originals and any independent sent-copy temporary. `PRUNE_INTERVAL_SECONDS = 3600` bounds the service's interval between retention passes to one hour while running. `SUMMARY_MAX_BYTES = 4096` caps the current cumulative summary checkpoint at 4 KiB. These are byte and elapsed-second constants, not per-loop tuning values; hard-link aliases count once for payload accounting, and independently copied bytes count separately.

**Rule (Bounded records and staging retention)** · `rule:mail:retention`

The mail service alone prunes its records and private staging, at startup, before capacity admission and at least once per pruning interval. Full `complete` or `discarded` records become eligible after the history interval, but a pending transaction, an unresolved refusal/source-restoration disposition, an active reservation reference or an extant inbox entry of an active endpoint pins its individual record for recovery and provenance. A sender's `sent` copy does not pin its record, because it is the sender's own history and never a steering brief; an unrecorded `sent` entry whose delivery instant is not later than the checkpoint's greatest compacted instant is reported as `compacted-history`, not `forged-local-entry`. A retired worker's inbox entries stop pinning when its retirement is recorded, because no round can be steered through them. A recipient's read-history copy can outlive that pin; after compaction it is historical data, not independently verifiable steering evidence. Pruning must not turn a live inbox entry of an active endpoint into an apparently forged one. The terminal age is measured from a persisted completion instant; uncertain or backward wall time postpones age-based pruning.

Eligible terminal records are folded in deterministic compaction order, sorting the eligible set by delivery instant on each pass, into a cumulative SHA-256 digest chain, recording the previous chain head, the exact removed record digest, cumulative count and greatest reserved instant. One bounded current checkpoint replaces the preceding checkpoint; a chain of summary files is not retained. Compaction journals its next record and new checkpoint before deleting that record, syncs the checkpoint and deletion, and recovers interruption without incorporating a record twice. The summary proves an aggregate history commitment, not an individual sender attestation. The watermark is never pruned or lowered, and verification never invents individual evidence from a summary.

After terminal cleanup is durable, its payload temporaries are removed in that operation; startup recovery reaps leftovers. Unjournaled temporaries are removed only after reconciliation proves them unpublished and the source recoverable. A pending payload is never deleted merely because it is old. Before claiming a source or reserving an instant, the service reserves capacity for the full transaction's maximum private payload copies and journal/compaction scratch within both caps. If pruning cannot free capacity because evidence is pinned or deliveries remain pending, it refuses new acceptance with `service-capacity` and leaves outgoing letters with reasons. It does not evict necessary evidence or consume extra space hoping to recover later. Because retained sent copies and retired workers' inboxes pin nothing, these hard caps bound only abnormal accumulation, such as an active endpoint leaving its inbox unread or staying unavailable; the deliberate tradeoff is backpressure until safe cleanup or repair releases the pinned capacity.

**Rule (Visible refusal)** · `rule:mail:refusal`

A pre-acceptance refusal leaves the letter unchanged at its outgoing name and atomically publishes a service-owned sidecar in the same outbox named `FILENAME.reason.toml`. The sidecar carries `version = 1`, the exact filename, its observed byte length and digest when safely readable, a stable `code`, a UTF-8 explanatory `reason`, and the UTC observation instant. Reason text describes transport only and never quotes the body. Codes distinguish `invalid-name`, `invalid-file`, `oversize`, `unknown-recipient`, `retired-worker`, `outside-estate`, `not-whitelisted`, `invalid-directory`, `unsafe-storage`, `changed-source`, `io-failure` and `service-capacity`. An accepted transaction blocked during publication projects `pending-delivery` with its reserved instant; its claimed source cannot be withdrawn or edited. The journal remains authoritative if projection itself fails, and the unit reports that failure for repair.

Sidecars are reserved service entries, never candidates; the service recognizes them by protected provenance as well as suffix, so a sender cannot hide an invalid letter by choosing the suffix. An invalid filename's sidecar uses `refusal-HEX.reason.toml` instead when the name is not UTF-8 or appending the suffix exceeds the filesystem name limit; `HEX` is SHA-256 of the raw filename bytes, and that sidecar records those bytes as hexadecimal. Sidecars cannot overwrite sender entries. A conflicting entry or unsafe outbox is a visible service failure in the unit log until repaired; no delivery proceeds on that candidate. Actors may read service-owned sidecars but cannot edit their bytes; a locally replaced sidecar has no service provenance and cannot change the protected refusal record.

An actor withdraws a refused letter by moving it to `draft`, corrects its name or bytes, and resubmits by atomic rename. The service removes a stale sidecar when its bound source is withdrawn or changes, and retries refused candidates on the next scan with fresh directory snapshots; a repaired whitelist can therefore admit unchanged queued mail. Notifications or logging failures do not turn refusal into success. A reason beside the retained letter avoids a bounce letter, which could itself require delivery or loop forever.

## Notice, waiting and cutover · `sec:mail:notice-and-cutover`

**Rule (Loop notice)** · `rule:mail:notice`

At the existing SessionStart, UserPromptSubmit and Stop hook positions, a nonempty loop inbox produces exactly one line, `You've got mail.`, and an empty inbox produces no mail context. The hook reads directory presence only, never letter bodies, subjects, sender lists, timestamps, counts or old envelope records. It preserves the five-second entry deadline, fail-open behavior and other hook composition bounds. It keeps no delivery receipt; repeated notice while mail remains is harmless. Read history alone never triggers it (`rule:hooks:letters-context`).

**Protocol (Inbox watcher)** · `proto:mail:watch`

Each loop starts or resumes its Sonnet inbox watcher at session start, independently of heartbeat and lane watchers. It arms inotify on that loop's `inbox` before listing it, then waits for arrival events; a re-list after wakeup, overflow or watch replacement reconciles the actual directory so events are hints, not delivery records. Where inotify is unavailable, an ordinary listing at the runbook's bounded waiting interval supplies the fallback. Worker watchers may use the same filesystem means on their own mount. Listing, `cat` and moving into `read` are the complete reading interface; no metadata-list or follow command is retained.

The loop watcher hands back only `You've got mail.` and returns to waiting when resumed by the session. It may remember observed names in its own context to suppress repeated wakeups, but replacement reconstructs from inbox and may repeat a notice. A notice conveys neither content nor authority; the receiving actor lists and reads at its own judgement. A dead watch is stopped before replacement. Watchers do not filter subjects or maintain HOLD/RELEASE queues, and no observation automatically resumes a paused lane (`proto:dispatch:inbox-watcher`).

**Protocol (One-time migration)** · `proto:mail:migration`

The migration command `superloop-mail migrate` replaces the old letters storage once, with no dual reader or compatibility transport. The maintaining loops and trusted provisioner inventory every old loop inbox (`new/` and `cur/`), each box home's `.local/inbox` and `.local/outbox`, together with all old producers, hooks and watchers. Each legacy letter file is treated as opaque bytes, including any old envelope bytes; the command moves it into the corresponding actor's `read` under its old basename. It neither parses nor strips an old record form. Pending legacy outgoing letters become history too, never automatic new submissions. Existing workers receive stable names and entries before this mapping is made. The worker-side stores being replaced are the box homes' `.local/inbox` and `.local/outbox`, not run directories: `step-<step>.txt` and the round's brief remain driver-owned watcher evidence at their original paths and are excluded from the migration manifest's move set.

Cutover stops old writers and readers and keeps the new service stopped, takes a recoverable backup, and records an exact source-to-destination manifest with lengths and digests. Missing optional stores are recorded as absent; a missing expected store blocks cutover. Equal old basenames from distinct sources go into separate unstructured provenance subdirectories of `read`, preserving every old basename and every byte without overwrite or deduplication. The manifest records those subdirectories and their source stores. New queued mail is withheld until verification establishes that every inventoried letter has moved and its bytes match. Migration is restartable from the manifest and moves an already verified item only once.

The activation boundary is the whole inventoried host mail estate: verified folders, worker directory, identity isolation, service and notice-only hooks become active together while all old transports remain disabled. Failure before activation restores the old state and processes together from backup; after new delivery begins, recovery uses the mail journal and a reviewed reconciliation rather than resurrecting old readers. Retain migration manifest and backup until inventory verification and rollback review are complete. Remove old metadata parsers, metadata-list/follow interfaces, the old worker mailbox transport and old hook rendering; continue writing `step-<step>.txt` and the round brief under (`proto:mail:round-transport`); backups are inert data, never a compatibility read path. This is an explicit replacement of correspondence behavior, not a claim of unchanged external command compatibility (`rule:architecture:external-contract-stability`) (`req:architecture:migration-declaration`).

## Implementation contract · `sec:mail:implementation-contract`

**Requirement (Delivery core and user unit)** · `req:mail:service-and-unit`

One delivery-core lane supplies `superloop-mail` and its host-session user unit under (`def:mail:service`). It owns subordinate identity entry, the exclusive writer lock, opaque bounded submission, two-directory resolution, fresh whitelist and estate decisions, `(SLUG, RECIPIENT)` scheduling, UTC millisecond admission and visible refusal. It uses the journal and publication interfaces required below rather than implementing a separate persistence path. Evidence covers empty and binary letters, the inclusive byte bound, sender ordering across recipients, directed whitelist outcomes, cross-estate refusal, invalid files, source mutation and capacity refusal. This obligation does not absorb records/recovery/retention or inbox-publication implementation.

**Requirement (Loop mail at birth)** · `req:mail:loop-birth`

Loop-home provisioning must create the five directories at `~/.var/loops/LOOP/mail` and establish (`rule:mail:ownership`) before a registered loop becomes mail-active. Through the loop entry it must create `ENTERED_HOME/.config/mail/loop.toml` with the file-only service read ACL and ancestor search ACLs under (`def:mail:loop-configuration`), using `workers = []` and an empty `mail.allow` array at schema version 1 when no configuration exists, preserve valid existing configuration on retry, and never silently reset workers or grants. Loop-home's root ensure and verification steps must preserve those named ACL entries and an ACL mask that keeps their effective permissions; a mode correction that resets the mask is a provisioning defect. Evidence must show exact paths, identity separation, idempotent creation without loss of queued or read mail, ACL survival across a repeated ensure, and refusal to activate a partial or cross-actor-accessible folder (`def:mail:loop-configuration`).

**Requirement (Worker birth in the lane launcher)** · `req:mail:worker-birth`

The lane launcher, and every other worker-creating harness, must assign and durably reserve the unique birth name, create `~/.var/loops/LOOP/workers/WORKER/mail` with all five directories and its isolated identity, and publish the active worker entry in the loop's configuration before launching the worker. Birth and retirement serialize with configuration replacement; a failed birth reserves its name without exposing an active incomplete endpoint. Resume preserves the name, folder and address; replacement allocates a new name and retirement retains the old entry. Evidence must cover concurrent allocation, interrupted birth, resume, replacement and nonreuse, with whitelist changes remaining solely loop-owned (`rule:mail:worker-birth-name`) (`proto:mail:resolve`).

**Requirement (Confined box mount)** · `req:mail:box-mount`

The box launcher must establish the read-write `/mail` mount and the subordinate-identity boundary under (`rule:mail:box-mount`) before exposing the worker's tools. Evidence must demonstrate listing, binary reading, draft publication and inbox-to-read moves with ordinary file tools, together with denial of writes to service-owned letter bytes, ancestor replacement, peer-folder access and remount escape. It must also demonstrate that local insertion allowed by directory modes gains no provenance and is reported as forged against the journal; optional mandatory hardening is not required to pass. If those checks cannot be established, launch fails rather than running with a broader bind mount (`rule:mail:ownership`).

**Requirement (Notice and ordinary waiting)** · `req:mail:notice-and-wait`

The hooks must emit exactly the one-line notice at the existing event positions and preserve deadline and fail-open behavior under (`rule:mail:notice`) and (`rule:hooks:letters-context`). The loop watcher must use ordinary inbox observation under (`proto:mail:watch`), including inotify arming before listing, overflow reconciliation, listing fallback and replacement. Evidence must show that neither hook nor watcher parses or relays letter bytes or metadata, an empty inbox with nonempty read history yields no notice, arrival between watch arming and listing is found, and a notice grants no resume authority.

**Requirement (Migration command)** · `req:mail:migration-command`

The tools repository supplies `superloop-mail migrate` under (`proto:mail:migration`) as one byte-migration lane, consuming entry and round retirement evidence under (`req:mail:legacy-entry-retirement`) and (`req:mail:round-transport`) before activation. Evidence must inventory every old loop store and each box home's `.local/inbox` and `.local/outbox`, explicitly excluding driver `step-<step>.txt` and round-brief evidence, prove exact byte and basename preservation including duplicate basenames, show interrupted conversion resumes without duplication, demonstrate rollback before activation, and verify that activation leaves no legacy metadata reader, follow interface, hook tail or legacy worker mailbox transport reachable, while proving that driver step evidence remains in place and continues to be written. Existing workers must have their birth names and mailbox mappings before conversion, and unverified or missing expected source state must block activation.

**Requirement (Round transport over mail)** · `req:mail:round-transport`

The lane driver must implement (`proto:mail:round-transport`) as one round-transport change: resolve the service-assigned delivery name, verify its principal and worker binding, name the delivered inbox file in the resume prompt, preserve exact `step-<step>.txt` watcher evidence and replace the reservation's `letters` records with the `mail` delivery binding. Evidence must cover own-loop steering during a run and on resume, peer mail remaining data, a moved or unverified inbox file blocking resume, and absence of `send-letter`, `withdraw-letter` and legacy `launch --round` letter-file readers after cutover.

**Requirement (Registry and mail name alignment)** · `req:mail:name-alignment`

The registry validator, worker allocator and mail parser must cite (`reg:mail:identity-names`) as their shared contract and admit exactly its production for loop and worker names. One alignment lane must demonstrate parity for digit-leading names, the refusal of hyphen-leading names by all three consumers, names longer than 48 bytes, empty names and excluded bytes, without an independent mail-only length or prefix restriction. It must distinguish lexical validity from a reported backing-filesystem failure when a complete path or filename cannot be represented (`lang:mail:names`).

**Requirement (Records recovery and retention)** · `req:mail:records-recovery-retention`

One persistence lane owns the journal schema, protected provenance verification, durable watermark, recovery/discard decisions, capacity accounting and bounded compaction under (`def:mail:records`), (`inv:mail:delivery-recovery`) and (`rule:mail:retention`). It consumes the publication witness supplied by (`req:mail:inbox-publication`). Evidence covers restart and clock rollback, unrecorded local entries, exact metadata and digest verification, discard interrupted at each durable boundary, pinned records at both capacity limits, age-based eligibility, checkpoint recovery without duplicate folding and preservation of the watermark. It must not remove needed payloads or attest a summary as an individual record.

**Requirement (Journaled inbox publication)** · `req:mail:inbox-publication`

One filesystem-publication lane implements (`proto:mail:deliver`) behind the persistence interface: service-only endpoint staging, same-filesystem checks, file and journal sync before publication, sent link with valid read permissions for both actors or a separately permissioned synced copy, one atomic no-replace inbox rename and directory sync. It reports the durable witness needed by (`inv:mail:delivery-recovery`). Evidence interrupts every publication boundary and moves the inbox file to read before the next journal update, proving that an absent journaled temporary does not cause redelivery; a surviving temporary must permit safe completion. Unsupported durability, mismatched filesystem identity and a destination collision must fail without overwrite or copy-and-unlink fallback.

**Requirement (Legacy loop entry retirement)** · `req:mail:legacy-entry-retirement`

One loop-entry lane removes loop-home's `letters` command family and the `letters`, `letters-private` and `letters-group` reserved-word branches. It removes their metadata-list/follow parsers and compatibility dispatch, then applies the ordinary entry grammar to those tokens with no mail-specific interception. Evidence derives the entry command inventory, proves the removed handlers and reserved-word matches are absent, and verifies unrelated loop entry behavior. Round commands and reservation records belong to (`req:mail:round-transport`); byte migration belongs to (`req:mail:migration-command`).

**Register (Tools conformance)** · `reg:mail:tools-conformance`

Each row is one independently reviewable implementation lane with one owning boundary and its own evidence; dependencies are consumed through their cited contracts, not duplicated. Each row names one requirement the tools repository can cite; its evidence must bind the implementation revision and observed outcome under (`sig:conformance:requirement-evidence-link`). These are implementation obligations, not a claim that the tools already implement them.

|Requirement|Tools surface|Contract and acceptance evidence|
|-----------|-------------|--------------------------------|
|(`req:mail:service-and-unit`)|Delivery core and user unit|Subordinate identity entry, submission, routing, scheduling and refusal.|
|(`req:mail:loop-birth`)|Loop-home provisioner|Five mail directories and initial loop configuration at loop birth.|
|(`req:mail:worker-birth`)|Lane launcher and other worker creators|Stable birth names, worker directories, lifecycle and loop-owned whitelist.|
|(`req:mail:box-mount`)|Box launcher and subordinate identity isolation|Only the worker's read-write mail mount, with journal-verified service publication and peer isolation.|
|(`req:mail:notice-and-wait`)|Hooks and inbox watcher|One-line arrival notice and ordinary filesystem waiting and reading.|
|(`req:mail:migration-command`)|Migration command and transport retirement|One-time byte-preserving move to read history, verified cutover and no legacy reader.|
|(`req:mail:round-transport`)|Lane driver and reservation records|Steering over mail with retained step evidence and retired round letter commands.|
|(`req:mail:name-alignment`)|Registry, worker allocator and address parser|One shared name grammar, with storage failures reported separately.|
|(`req:mail:records-recovery-retention`)|Journal and recovery module|Protected records, provenance, restart, discard, bounded retention and backpressure.|
|(`req:mail:inbox-publication`)|Filesystem publication adapter|Journal-before-rename ordering and recovery independent of inbox survival.|
|(`req:mail:legacy-entry-retirement`)|Loop-home entry parser|Retire legacy letters commands, reserved words and metadata interfaces.|
