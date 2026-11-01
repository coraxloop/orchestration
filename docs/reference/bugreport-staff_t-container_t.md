# Rootless podman unusable for confined SELinux users: `staff_r` not authorized for `spc_t`, breaking container process label computation · `rep:selinuxcontainers:confined-rootless-podman-failure`

## Summary · `sec:selinuxcontainers:summary`

On Fedora 44, a user mapped to the confined SELinux login `staff_u` (running as `staff_u:staff_r:staff_t:s0-s0:c0.c1023`) cannot run privileged rootless containers, and therefore cannot use Toolbx at all.

Podman itself transitions correctly into `container_runtime_t`. The failure occurs when the kernel computes the label for the container process: the computed type is `spc_t`, and the resulting context `staff_u:staff_r:spc_t:s0` is invalid, because the role `staff_r` is not authorized to hold the type `spc_t`. `security_compute_sid` therefore fails, the container's initial `execve(2)` returns `EACCES`, and — importantly — **no AVC denial is logged**, because nothing was denied; a valid context simply could not be constructed.

```
$ podman run --rm --privileged registry.fedoraproject.org/fedora-toolbox:44 true
{
  "msg": "exec container process `\/usr\/bin\/true`: Permission denied",
  "level": "error",
  "time": "2026-08-15T21:16:27.723021Z"
}
```

## Evidence · `sec:selinuxcontainers:evidence`

Four `SELINUX_ERR` records, all identical in shape; event identifiers and account mappings below are fixtures:

```
type=SELINUX_ERR msg=audit(0.000:1): op=security_compute_sid
  invalid_context="staff_u:staff_r:spc_t:s0"
  scontext=staff_u:staff_r:container_runtime_t:s0
  tcontext=system_u:object_r:container_file_t:s0:c1022,c1023 tclass=process
```

Corresponding records at `:2`, `:3`, and `:4`.

Notable points:

- `scontext` is `staff_u:staff_r:container_runtime_t:s0` — the `staff_t` -> `container_runtime_t` transition succeeds. The runtime is running normally.
- The failure is the *next* label computation, for `tclass=process`.
- There are **zero** AVC records from `container_runtime_t` or involving `spc_t`/`container_t` in the same capture. Searching for AVCs alone finds nothing and misleads the investigation.
- MCS is not the constraint: the user range `s0-s0:c0.c1023` spans the target's `c1022,c1023`.
- The invalid context differs from the source only in *type*, with user and role unchanged, pointing at a missing role-type authorization (`role staff_r types spc_t;`) rather than a missing allow rule.

## Environment · `sec:selinuxcontainers:environment`

|Component|Version|
|---------|-------|
|OS|Fedora 44 (pre-release), ostree-based (`/var/home` layout)|
|podman|`podman-5.8.4-1.fc44.x86_64`|
|crun|`crun-1.28-1.fc44.x86_64`|
|fuse-overlayfs|`fuse-overlayfs-1.17-1.fc44.x86_64`|
|container-selinux|`container-selinux-2.250.0-1.fc44.noarch`|
|selinux-policy|`selinux-policy-44.6-1.fc44.noarch`, `selinux-policy-targeted-44.6-1.fc44.noarch`|
|kernel|`7.1.8-200.fc44.x86_64` (at capture-completion 2026-08-28; the original failure was observed 2026-08-15)|
|SELinux mode|`Enforcing`|

```
$ id
uid=41001(ACCOUNT) gid=41001(ACCOUNT) groups=41001(ACCOUNT) context=staff_u:staff_r:staff_t:s0-s0:c0.c1023
```

SELinux login mapping: *(fill in: `sudo semanage login -l`)*

Role/type authorization (measured 2026-08-28 with setools 4.6.0 against the installed `policy.35`): `seinfo policy.35 --role_types spc_t` returns exactly `sysadm_r`, `system_r`, `unconfined_r` — `staff_r` is absent. `seinfo policy.35 --role_types container_t` returns `container_user_r`, `staff_r`, `sysadm_r`, `system_r`, `unconfined_r`, `user_r` — `staff_r` IS authorized for `container_t`.

## Steps to reproduce · `sec:selinuxcontainers:steps-to-reproduce`

1. Map a local user to the confined `staff_u` login: `sudo semanage login -m -s staff_u -r s0-s0:c0.c1023 <user>`
2. Log out and back in; confirm with `id -Z`.
3. Run a privileged rootless container: `podman run --rm --privileged registry.fedoraproject.org/fedora-toolbox:44 true`

## Expected behaviour · `sec:selinuxcontainers:expected-behaviour`

The container runs and exits 0, as it does for a user in `unconfined_t`.

## Actual behaviour · `sec:selinuxcontainers:actual-behaviour`

`exec container process '/usr/bin/true': Permission denied`, exit 1, with the `SELINUX_ERR` record above and no accompanying AVC.

## Scope · `sec:selinuxcontainers:scope`

`--privileged` and `--security-opt label=disable` both select `spc_t` and both fail. Whether unprivileged containers using `container_t` are equally affected depends on whether `staff_r` is authorized for `container_t`:

```
podman run --rm --security-opt label=type:container_t \
  registry.fedoraproject.org/fedora-toolbox:44 true; echo "rc=$?"
```

Static answer (seinfo 4.6.0 against installed policy.35): `staff_r` is authorized for `container_t` but not `spc_t`, so unprivileged containers under the default label are expected to work and the failure is specific to `spc_t` selection — `--privileged` and `label=disable`. Toolbx creates privileged containers, which is why Toolbx is entirely broken while plain `podman run` succeeds.

Runtime confirmation (2026-08-28, second Fedora 44 machine — Silverblue, `staff_u` login, Enforcing): `podman run --rm registry.fedoraproject.org/fedora-toolbox:44 true` exits 0; adding `--privileged` exits 1 with the reported error. The scope is therefore confirmed on two installations: only `spc_t`-selecting containers are affected.

## Ruled out · `sec:selinuxcontainers:ruled-out`

- **MCS categories** — user range spans the target categories.
- **Filesystem permissions / mount options** — storage on btrfs at `/var/home/<user>/.local/share/containers/storage`, no `noexec`, ownership correct under `podman unshare`.
- **UID/GID mapping** — ``ACCOUNT:100000:65536`` in both `/etc/subuid` and `/etc/subgid`; expected rootless `uid_map`.
- **Runtime setup** — `podman --log-level=debug` shows overlay mounted, netns created, pasta configured, OCI spec written, conmon and crun launched, container created, started, and cleanly torn down. Only the container's own `execve` fails.
- **Container labelling** — reproduces with `--security-opt label=disable`, which selects `spc_t` rather than removing SELinux from the path.

## Impact · `sec:selinuxcontainers:impact`

Toolbx is entirely unusable for confined users. On ostree-based Fedora variants, where layering packages onto the host is discouraged, Toolbx is the primary supported route to development tooling, so this is a hard block rather than an inconvenience.

The user-visible symptom is badly misleading:

```
$ toolbox enter
Error: failed to bind /etc/machine-id to /run/host/etc/machine-id
```

The entry point never executed, so the bind never happened — but the message sends users to investigate `/etc/machine-id`, bind mounts, and storage drivers. Combined with the absence of any AVC, this is very difficult to diagnose: every layer reports success, standard SELinux troubleshooting finds nothing, and only `SELINUX_ERR` records reveal the cause.

## Local workaround · `sec:selinuxcontainers:local-workaround`

Verified end-to-end 2026-08-28 on the second Fedora 44 machine (Silverblue, `staff_u`, Enforcing): after `semodule -i` of the one-line CIL equivalent (`(roletype staff_r spc_t)`), `podman run --privileged` exits 0 and `toolbox create` + `toolbox run` succeed for the confined user. The CIL form needs no compiler toolchain:

```
echo "(roletype staff_r spc_t)" > staff_spc.cil
sudo semodule -i staff_spc.cil
```

```
module staff_spc 1.0;
require {
    role staff_r;
    type spc_t;
}
role staff_r types spc_t;
```

```
checkmodule -M -m -o staff_spc.mod staff_spc.te
semodule_package -o staff_spc.pp -m staff_spc.mod
sudo semodule -i staff_spc.pp
```

## Questions for maintainers · `sec:selinuxcontainers:questions-for-maintainers`

1. Is rootless podman from a confined user domain such as `staff_t` intended to be supported? If so, `container-selinux` appears to be missing role-type authorizations (`role staff_r types spc_t;`, and possibly `container_t`) for confined user roles.
2. If it is not supported, could that be documented? The failure mode gives no usable signal.
3. Could podman or crun surface `security_compute_sid` failures more clearly? A bare `EACCES` from `execve` with no AVC is close to undiagnosable without knowing to look for `SELINUX_ERR` specifically.

## Notes · `sec:selinuxcontainers:notes`

- Not yet established whether this is a regression from an earlier Fedora release. If a prior release worked in the same configuration, please add that.
