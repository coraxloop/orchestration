# GPG keys and commit signing · `spec:signing:gpg-keys-and-commit-signing`

A signed commit binds a change to a key, and a key is only evidence when its custody is narrow, its lifetime is short, and its loss has a rehearsed answer. This document fixes how superloops hold OpenPGP keys and sign git history: one keyring per superloop, a certify-only root with a single signing subkey, one-year lifetimes rotated on time or on a new host, revocation certificates written before the root's private half is destroyed, and the signing half destroyed when the key ends. It extends the per-repository identity rule (`inv:environment:git-identity-per-repository`), which already refuses a machine-wide identity and any assumption that loops share a forge account; a signing key is the same kind of fact as an identity or a forge credential, so it follows the same per-loop discipline.

## One keyring per superloop · `sec:signing:one-keyring-per-superloop`

**Rule (No shared keyring)** · `rule:signing:no-shared-keyring`

Every superloop owns a separate OpenPGP home directory, mode `0700`, and never uses the machine default. The estate registers the directory shape in its environment rulebook alongside the per-loop forge configuration, because the two answer the same question: which loop is acting. Two superloops never share a key; a key names one loop on one host for one year. If a key is nevertheless present in two loops, for example after a loop is split, or because two loops publish to one upstream project under one maintainer identity and a second key would fragment that identity's history on the forge, each loop keeps its own copy inside its own directory: the key is established once by the procedure below and its signing subkey and certificates are carried into the other loop's keyring the way the migration procedure carries them. The directory itself is never shared, symlinked, or mounted into another loop, because a shared directory makes every signature ambiguous about which loop produced it and lets one loop's compromise revoke or exhaust the other's key.

**Rule (Only the superloop signs)** · `rule:signing:only-the-superloop-signs`

Lanes and workers never sign, in any loop and under any harness, and no brief or loop configuration makes an exception. A signature attests that a commit was reviewed and imported, which is the superloop's act: a lane clone or worktree is provisioned with `commit.gpgsign false`, a worker's commits ship unsigned, and the superloop signs each reviewed commit at import, verifying the patch rather than any lane signature. A signing key reachable from a lane sandbox is a credential exposure with nothing to attest, so a signing failure inside a lane is a stop to report, never a reason to copy a keyring or widen a sandbox root over one.

**Rule (Repository-local signing configuration)** · `rule:signing:repository-local-configuration`

Signing is configured in each repository the superloop commits in — its working clone and the checkouts it imports through — at provisioning, next to the local identity: the signing program is a wrapper inside the loop's keyring directory that exports that directory and executes the system `gpg`, the signing key is the signing subkey's fingerprint with the trailing `!` that pins the subkey, and commit and tag signing are enabled locally. Global git configuration carries no signing key and leaves signing off, so a repository that skipped its provisioning step produces an unsigned commit rather than a commit signed by the wrong loop. The wrapper lives inside the keyring directory so that the repository configuration names one path and the key selection cannot drift from the directory it belongs to.

Public keys are not secrets. Each loop exports its public key for the loops and reviewers that verify its history, and the loop's public key is registered with the forge through the loop's own forge configuration, an owner-run credential step. Verification needs only public material, so a verifier imports peers' public keys into its own keyring and never opens a peer's directory. Carrying a signing subkey into a second keyring is a private-key export, which a loop's own permission gate refuses by default; that handoff is an owner-run or owner-cleared step for each receiving loop, never a step one loop performs for another.

## Key shape · `sec:signing:key-shape`

**Definition (Loop signing key)** · `def:signing:loop-signing-key`

A loop signing key is an Ed25519 root key whose only capability is certify, carrying exactly one Ed25519 subkey whose only capability is sign. There is no encryption subkey and no authentication subkey: the loop encrypts nothing with this key and authenticates over SSH with separate keys, and every capability the key does not carry is a use a leaked key cannot be put to. The user identity is the repository's committer identity, so a forge that matches signature to committer marks the commit verified and a reader who checks the signature by hand sees the same name the commit carries.

The certify root exists to mint the subkey and to sign the revocation certificates; once those are written it has no further job. The signing subkey is the only private material that stays on the host, which is why it carries a single capability and a short life.

## Lifetime and rotation · `sec:signing:lifetime-and-rotation`

**Rule (One year, then a new key)** · `rule:signing:one-year-then-a-new-key`

Root and subkey both expire one year after creation. A key is rotated before it expires, and immediately when the loop moves to a new host. Rotation always produces a fresh root and subkey: the certify private key was destroyed after generation, so nothing can extend, re-sign, or add to the old key, and expiry is a hard stop rather than a reminder. The old key is revoked with a stored certificate, superseded when the rotation was planned, and its signing half is purged as the end-of-life rule requires.

**Rule (Private keys never migrate)** · `rule:signing:private-keys-never-migrate`

A private key is created on the host that uses it and dies there. Moving a loop to a new host means generating a new key on the new host and registering its public half; the old host's key is revoked and purged. Copying private material between machines multiplies the places it can leak from and makes a later compromise impossible to attribute to one host, while a fresh key costs one generation and one registration.

## Moving off a shared host keyring · `sec:signing:moving-off-a-shared-host-keyring`

**Procedure (Migrate loops that already publish under one identity)** · `alg:signing:migrate-loops-under-one-identity`

Loops that already publish under one committer identity whose key lives in the machine default keyring keep that identity's verified standing in history and on the forge by carrying the key across rather than starting fresh, and the sharing rule permits it because each loop ends up with its own copy in its own directory. Only the signing subkey moves; the certify half never enters a loop keyring.

1. Run the normal checks on the host keyring while its certify half is still present: verify the shape, and write the four revocation certificates, because this is the last moment a certificate can be produced.
2. Export the signing subkey alone with `gpg --export-secret-subkeys '<subkey fingerprint>!'` and import it into each receiving loop's keyring through that loop's wrapper; copy the four certificates into each keyring's `revocations/` at mode `0600`. A secret listing in the receiving keyring must show `sec#` for the root and an ordinary `ssb` for the subkey.
3. Configure each receiving repository as the establishment procedure requires, make a signed commit, and verify it.
4. Only after every receiving loop has signed and verified through its own keyring, export the public key for the record and remove the machine default keyring entirely. Its removal is the purge of the certify private key and of the last ambient copy of the subkey, so that no signature can again be produced without naming a loop.

The carried key keeps its original expiry. Each receiving loop rotates to a key of its own at that expiry by the ordinary rule, or at once when the expiry is near, and purges the carried private half then.

## Generation, verification, revocation certificates, purge · `sec:signing:generation-and-purge`

**Procedure (Establish a loop signing key)** · `alg:signing:establish-a-loop-signing-key`

The sequence is run by the loop that will own the key, inside its own keyring directory, and reported step by step with wall time. The key carries no passphrase: an unattended agent would have to supply the passphrase itself, so it would protect nothing, and the directory mode, the single capability, and the one-year life are the controls instead.

1. Create the keyring directory at mode `0700` and, inside it, a `bin/gpg` wrapper that exports the directory as the OpenPGP home and executes the system `gpg` with its arguments. Everything below runs through that wrapper.
2. Generate the certify-only root: `gpg --quick-generate-key '<committer identity>' ed25519 cert 1y`. Record the root fingerprint.
3. Add the signing subkey: `gpg --quick-add-key <root fingerprint> ed25519 sign 1y`. Record the subkey fingerprint.
4. Verify the shape: the secret listing shows one `sec` with capability `[C]`, one `ssb` with capability `[S]`, and both expiries one year out. Sign a test message with the subkey and verify it.
5. Write four revocation certificates, one for each reason OpenPGP defines, into `revocations/` inside the keyring directory at mode `0600`, named by root fingerprint and reason: `0` no reason given, `1` key compromised, `2` key superseded, `3` key no longer used. Each is produced with `gpg --gen-revoke <root fingerprint>` answered through the command file descriptor (`--no-tty --command-fd 0`, never `--batch`, which suppresses the questions and writes nothing), and each is checked by listing its packets: a key-revocation signature of class `0x20` carrying the intended reason. Four certificates exist because the reason is part of what a revocation tells a verifier, and once the certify key is gone no new reason can be written. The certificate gpg writes on its own into `openpgp-revocs.d` at generation stays where it is; it is not one of the four, which are named by reason and verified.
6. Only when four certificates have been verified that way, purge the certify private key: list keygrips with `gpg --with-keygrip -K`, delete the root keygrip's file from `private-keys-v1.d/`, and confirm that the secret listing now shows `sec#` for the root and an ordinary `ssb` for the subkey. Sign and verify again to prove the subkey still works without the root.
7. Configure the repository: local `gpg.program` pointing at the wrapper, local `user.signingkey` set to the subkey fingerprint with `!`, local `commit.gpgsign` and `tag.gpgsign` true. Make a signed commit and verify it with `git verify-commit`.
8. Export the public key, register it with the forge under the loop's own forge configuration, and record the root and subkey fingerprints, creation and expiry dates, and the host in the loop's registry.

**Invariant (Certify key absent after establishment)** · `inv:signing:certify-key-absent-after-establishment`

From the end of the procedure until the key's end of life, the loop's keyring holds the signing subkey's private half and no certify private key. A keyring found with a live certify half after establishment is a finding: the key is re-established from step 5, and if the revocation certificates cannot be located it is rotated.

## After expiry or revocation · `sec:signing:after-expiry-or-revocation`

**Rule (Purge the signing subkey at end of life)** · `rule:signing:purge-the-signing-subkey-at-end-of-life`

When the key expires, or when a revocation certificate is published for it, the signing subkey's private half is deleted from `private-keys-v1.d/` the same way the certify half was, and the deletion is verified by a secret listing that shows no private material for the key. The public key, the revocation certificates, and the registry record stay, because signatures already in history are verified against the public key and a reader must be able to see when and why the key ended. A private key that has no future use only has a future misuse.

Revocation is used, rather than waiting for expiry, whenever the host is retired or rebuilt, whenever the loop is moved, and whenever compromise is suspected; the stored certificate for the matching reason is imported into the keyring and published to the forge and to every verifier that holds the public key.

## Conformance · `sec:signing:conformance`

A loop's signing setup conforms when every line below holds, and each is checkable from a secret listing, a directory listing, and the repository's local configuration without reading private material:

- the keyring is the loop's own directory at mode `0700`, and the repository's `gpg.program` is the wrapper inside it;
- the secret listing shows `sec#` for a certify-only root and exactly one `ssb` with capability `[S]`, both expiring within one year of creation;
- `revocations/` holds four certificates for the root, one per reason, at mode `0600`;
- `user.signingkey` names the signing subkey with `!`, and commit and tag signing are enabled locally while global configuration leaves them off;
- the public key is registered with the forge under the loop's own forge configuration, and the latest commit verifies;
- no other loop's private material is present, and no private material for an expired or revoked key remains.
