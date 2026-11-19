# Estate operations · `spec:oper:estate-operations`

Reading order and parent: (`guide:publicorchestration:orchestration`).

This document states the operations profile's work, the matters of estate operations that come to a person and each loop's own custody. Its policy belongs to the orchestration corpus (`rule:architecture:orchestration-policy-owner`); dispatch reaches it through (`rule:dispatch:owner-desk-boundary`). An instance places its paths and the profile holder's instructions in that loop's face, so the general contract carries no machine-specific locations.

**Rule (Owner and operations)** · `rule:oper:owner-and-operations`

The matters of estate operations that come to the owner are enumerated in (`reg:oper:owner-desk-list`); each loop asks directly for its own login, registration and identity. Engineering questions are settled with workers and reviewers and reported in one line. The operations profile holds estate operations: compute nodes with root, accounts, units, kernel settings of record and cleanup, deploys and their holds, the door's host steps, and the loops' frictions and findings. It announces a first-time change before acting and reports after. Server freshness, data-removal authority, review and the adopted deployment gates still apply (`rule:server:fresh-server-root-handover`), (`rule:dispatch:host-removal-authority`), (`inv:architecture:trusted-final-gate`). A loop's own keys, records, letters and requests remain that loop's work (`rule:oper:loop-owner-inputs`).

An operations matter that goes unanswered was not the owner's to answer: the session withdraws the unnecessary question and proceeds under the existing grant; no session adds an owner gate to an operations matter that the list or an existing person's-own rule does not carry. Silence neither expands nor retracts a grant. A missing grant, an unresolved nonfresh-server finding or a real gate failure still stops the affected action; privilege, unfamiliarity and an unanswered unnecessary question do not create another stop.

**Register (The owner's desk)** · `reg:oper:owner-desk-list`

This list is the operations profile's own focus: it names the matters of estate operations that come to the person who owns the estate, so that operations settles every other one itself and keeps its own questions off that person's desk. It does not bound what a loop brings to its owner about its own work, its product and its decisions, which that loop asks under (`rule:dispatch:owner-desk-boundary`); each loop asks directly for its own login, registration and identity, never through the operations loop.

1. API logins: new vendor and forge logins, choosing a different account, token refresh that needs the person, and any copy of a sign-in from one loop to another; a loop's fallback among sign-ins already provisioned for it remains its own act (`rule:oper:loop-owner-inputs`).
2. A loop's registration: its row in the loops file, including its existence, uid, launch directory, runs root and door floor; moving the floor toward less strictness changes that file (`rule:oper:loop-owner-inputs`).
3. A loop's identity: its email address and forge account (`rule:oper:loop-owner-inputs`).
4. The host harness that supervises the sessions: registering a hook for a new concept, its permission and settings files, and the person's own global instruction file (`rule:oper:host-harness-authority`).
5. Server handover: the person's one-sentence handover of a fresh server grants root operations; a server holding anything the estate did not put there stops operations for the person's answer before it is touched (`rule:server:fresh-server-root-handover`).
6. Policy set by word: what the system is for a person, including the degree of confidence preferred before a product ships (`rule:architecture:orchestration-policy-owner`).

The existing rules that reserve acts to a person remain binding, including permanent deletion of data that may be the only copy (`rule:dispatch:host-removal-authority`); this list does not grant that deletion.

**Rule (A loop's owner-managed inputs)** · `rule:oper:loop-owner-inputs`

The person performs new vendor and forge logins, chooses a different account and performs any transfer of a sign-in between loops, because these acts grant access outside the loop's existing provision. At a usage limit the loop may probe its own already-provisioned backup sign-ins from private probe copies and install the first usable one as its canonical sign-in without another owner question or printing sign-in bytes. Preparing a home, deriving that loop's worker or door credential, operating an installed renewal protocol and selecting that fallback carry the existing provision; they authorize neither a new login nor a different-account choice nor a copy from another loop. An expired or unusable sign-in that needs the person is requested directly by its loop.

The person maintains the loops file: a row grants the loop's existence, uid, launch directory, runs root and door floor. Provisioning carries out that row without another owner question. A less-strict floor requires the file to change; a conversation cannot substitute for the row. A loop may choose a stricter effective mode and return within its registered floor under the door's existing rules.

The person chooses the loop's email address and forge account. The loop makes its own keys, signing records, letters and requests in its own entry; those records are not the owner-maintained registration row (`alg:signing:establish-a-loop-signing-key`). A grant of identity is not custody of the loop's private keys.

**Rule (Host-harness authority)** · `rule:oper:host-harness-authority`

The person controls the host harness that supervises the sessions: a hook for a new concept, its permission and settings files, and the person's own global instruction file. A new concept grants a new kind of decision or event to the session's tools and therefore needs the person's grant. A reviewed repository text is not permission to install it in that person's instruction file.

Maintaining an already granted host-hook concept is an operations task: adapter renames, corrected paths and reply formats preserve the grant. The superloop announces a first-time change, retains the former settings for rollback, reports the edit and proves the expected event; this delegation does not grant another permission or concept. The holder of each affected session restarts it when required. Worker-harness hooks and derived worker settings belong to the prepared lane home under its loop's registration, not to a new host-session grant (`rule:oper:loop-owner-inputs`).

**Rule (A face keeps its history)** · `rule:oper:face-history`

Every loop's face, the launch directory holding its instruction file and the harness's state, is a Git repository whose bare of record lies in that loop's own home. The loop establishes and maintains both; changes to the instruction file have a history and a stated reason because every session reads them. The harness's state directory stays untracked through the repository's local exclude file because its state and settings belong to the harness rather than the loop's instruction history. The face's repository is readable without traversing the private bare; it is not a linked worktree or an object store dependent on that bare, because sharing that dependency would expose private objects or leave the session unable to read its own history.

A face tracks only its instruction file and CONTRIBUTING (`req:dispatch:contributing-guide`), so product sources and generated state cannot obscure changes to the instructions every session reads. Product sources, builds, tests and linter configuration belong in their product repositories, where their implementation and verification rules are reviewed together. Only the loop's own session changes and signs the face's history under its identity; a worker lane never works there because a brief cannot grant authority to change the orchestration instructions it runs under (`rule:architecture:charter-plus-brief`). Instruction changes come from reviewed source documents and point to what can be read there rather than restating it, because a delivery copy must not become a second policy owner (`rule:architecture:orchestration-policy-owner`). Their commit bodies state the reason for the change.

The route by which commits reach the bare is the loop's choice. The face repository remains usable and its history stays in the loop's custody; this grants neither publication of private history nor placement of credentials in the face. The instance records its locations.
