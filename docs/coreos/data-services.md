# Backups and production data services · `guide:coreos:data-services`

**Remark (Increment placement and evidence)** · `rem:coreos:data-context`

These fictional increments 3–6 in (`reg:coreos:increment-order`) follow (`req:coreos:increment-contract`). All timings and capacities are fixtures under (`conv:coreos:measurement-scope`). Example restores illustrate content recovery for the exercised engine and placement; they do not turn the same-host practice destination into offsite protection (`obs:coreos:backup-deployment-gap`).

## Restic backups · `sec:coreos:backups`

**Setup (Containerised restic and custody)** · `setup:coreos:restic-setup`

The reference wrapper ran pinned restic 0.18.1 in a container over SFTP. The machine generated its SSH key and repository passphrase and stored them under `/etc/example/backups/` with mode 0600. The box’s host key was pinned on first contact and thereafter enforced with `StrictHostKeyChecking yes`; compare the pinned key against the provider-published fingerprint. Each machine used its own repository path: a second machine pointed at a path already holding another machine’s repository, encrypted with a different passphrase, failed.

**Procedure (Backup service sequence)** · `alg:coreos:backup-sequence`

1. Run `backup --tag scheduled --exclude-file=... --exclude-caches /var/lib/example /etc` after the engine-native consistent backups.
2. Run `forget --keep-daily 7 --keep-weekly 4 --keep-monthly 3 --prune`.
3. Run `check`; a failed backup or check is an alarm (`alg:coreos:backup-repair`), not a successful timer occurrence.

**Observation (Backup timer evolution)** · `obs:coreos:backup-cadence`

The fictional timer begins daily with `Persistent=true` and a 10-minute random delay. Once PostgreSQL archives WAL, the cadence becomes every 20 minutes.

**Scenario (Build output filled the backup target)** · `scenario:coreos:backup-exclusions`

In the fictional capacity scenario, one snapshot is 48 GiB although production data is 300 MB: `target/`, `build/`, `node_modules/`, caches and worktrees dominate it. The target fills and backups fail for 12 hours. Excluding regenerable output reduces the snapshot to 1.5 GiB in 35 s, and pruning reclaims 45 GiB in 12 s. This illustrates the reason to separate disposable output from retained state (`rule:server:disposable-build-artifacts`).

**Setup (Backup target capacity monitoring)** · `setup:coreos:backup-capacity`

The fictional monitor queries free space over SFTP every 12 minutes, issues a notice below 24 GB and an alarm below 6 GB. An SFTP-only target has no shell: use SFTP batch-mode `df`, `ls` and `rm`, prefixing individual commands with `-` when one failure must not abort the rest of the batch. At a completely full target restic cannot even create its lock; `forget ... --prune --max-repack-size 0 --max-unused unlimited` illustrates recovery without temporary repacking room.

**Scenario (Practice backup and restore)** · `scenario:coreos:restic-rehearsal`

Against the fictional SFTP-only practice target in KVM, applying the increment takes 8 s; a full 1.5 GiB, 2000-file backup including prune and check takes 25 s; an incremental additional 64 MiB takes 5 s; full restore takes 20 s. SHA-256 matches for all 2000 restored files. The practice target rejects shell access with “This service allows sftp connections only.”

**Observation (Offsite deployment remained incomplete)** · `obs:coreos:backup-deployment-gap`

At the fictional reference state the separate-provider offsite target is planned, not yet used. Backups go to a practice VM on the same hardware and cannot protect against loss of that machine. The design calls for an offsite target (`prin:coreos:backups-and-window`), and the next host starts with a real one from day one (`reg:coreos:lessons`); the illustrated rehearsal is narrower than that requirement.

## PostgreSQL and WAL · `sec:coreos:postgres`

**Listing (PostgreSQL system Quadlet)** · `listing:coreos:postgres-quadlet`

```ini
# /etc/containers/systemd/example-postgres.container (abridged)
[Container]
Image=<pinned postgres image>
Secret=example-pg-password,type=env,target=POSTGRES_PASSWORD
Volume=/var/lib/example/prod/postgres:/var/lib/postgresql:Z
Volume=/var/lib/example/prod/pg-wal-archive:/wal-archive:z
Volume=/var/lib/example/prod/pg-base:/base:z
PublishPort=<loopback-ip>:5432:5432   # IPv4 loopback only
Exec=postgres -c wal_level=replica -c archive_mode=on \
  -c "archive_command=test ! -f /wal-archive/%%f && cp %%p /wal-archive/%%f" -c archive_timeout=300
HealthCmd=pg_isready -U <user> -d <db>
[Service]
Slice=production.slice
Restart=always
RestartSec=5
TimeoutStartSec=180
[Install]
WantedBy=multi-user.target
```

**Setup (Database backup and secret paths)** · `setup:coreos:postgres-backup`

Generate the password on the machine with `openssl rand`, store it as a Podman secret and deliver it only to the service. Set data-directory ownership to the container image’s verified postgres UID rather than assuming a host account mapping. A daily `pg_basebackup -Ft -z -X stream` supplies self-contained base backups; the fictional retention keeps three locally and delegates longer retention to restic. Delete WAL only when it is older than the oldest retained base backup.

**Warning (Quadlet percent expansion)** · `warn:coreos:wal-percent`

Systemd expanded `%f` and `%p` before PostgreSQL saw them; archiving failed silently and the base backup waited 19 minutes. Write `%%f` and `%%p` in the Quadlet as in (`listing:coreos:postgres-quadlet`).

**Warning (Checkpoint WAL dependency)** · `warn:coreos:wal-checkpoint`

With `-X none`, the base backup depended on the checkpoint WAL still being archived. The rehearsal deleted that segment and recovery failed with “could not locate required checkpoint record”. Use `-X stream` for the self-contained base backup.

**Scenario (Point-in-time recovery)** · `scenario:coreos:postgres-pitr`

The fictional 50 s rehearsal loads 100k rows, takes a base backup, adds 20k rows, marks time T and adds 10k more. Backup to the SFTP target takes 5 s; restoring base plus WAL to a separate directory takes 2 s; recovery to T and promotion in a second container takes 2 s. The result contains exactly the 120k rows before T, and the vector index remains valid. The whole-run wall includes more than those individual transfer and recovery stages.

## Object storage and analytics · `sec:coreos:datastores`

**Setup (Native backups before restic)** · `setup:coreos:datastore-backups`

Both engines ran as system Quadlets under `production.slice`, pinned to the exact rehearsed patch-version image. Before restic, object storage supplied a metadata snapshot plus immutable data blocks; analytics supplied native `BACKUP ALL`, keeping two. The analytics container had `MemoryMax` with its internal memory limit below that ceiling.

**Scenario (Object and analytics restore)** · `scenario:coreos:datastore-rehearsal`

The fictional rehearsal backs up and restores 2000 objects and 2M rows into fresh instances in 30 s, verifying SHA-256 for objects and row count and sum for analytics.

**Warning (Secret mode and shell-free images)** · `warn:coreos:datastore-secrets`

Podman mounted secrets 0444 by default and some services rejected world-readable secrets; select `mode=0400`. Images without a shell require alternative configuration to be written on the host side.

## Messaging and durable execution · `sec:coreos:messaging`

**Setup (NATS and Restate)** · `setup:coreos:messaging-setup`

NATS core ran as a Quadlet without JetStream because the product did not use it; production NATS therefore retained no state and had no separate backup. Restate ran as a host-networked Quadlet and sent partition snapshots to an object-store bucket.

**Scenario (Cluster identity restoration)** · `scenario:coreos:restate-rehearsal`

In the fictional recovery scenario, a fresh Restate cluster rejects snapshots with “cluster fingerprint mismatch”: the cluster identity lives in the node metadata directory. The repair combines snapshots with a daily consistent data-directory copy while the service is stopped during maintenance, illustrated with 3 s downtime. Recovery rehearsal takes 20 s. Snapshots without the matching identity do not recover a lost machine.

**Warning (Stopped-service copy ordering)** · `warn:coreos:copy-ordering`

The copy unit needs `After=` rather than `Requires=` on the service. With `Requires=`, stopping the service cancelled the copy job itself. Stop the original before starting a restored identity (`rule:coreos:restore-identity`).
