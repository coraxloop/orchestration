# Hardware and installation rehearsal · `guide:coreos:boot`

**Remark (Measurement context)** · `rem:coreos:boot-context`

Hardware and reboot results are fictional fixtures under (`conv:coreos:measurement-scope`). The installation configuration is (`guide:coreos:butane`); ongoing recovery is (`proto:coreos:rescue`).

## Hardware and recovery access · `sec:coreos:hardware-and-recovery`

**Observation (Hardware constraints)** · `obs:coreos:hardware`

The board had legacy BIOS and no TPM, excluding TPM2-bound Clevis/LUKS encryption for that hardware. The owner deferred disk encryption. One NVMe disk supplied storage without RAID; losing that disk loses the local machine state. Encryption must be decided before installation and hardware selection: retrofitting it into this setup entails reinstalling. Offsite recovery therefore matters independently of whether this host can reboot.

**Setup (Provider rescue environment)** · `setup:coreos:rescue-environment`

The provider's rescue environment was network-booted Debian running in RAM. Activation in the provider panel applied only to the next boot. Installation from it used `coreos-installer` against the NVMe with an Ignition file (`listing:coreos:install-command`).

**Warning (Installation destroys the selected disk)** · `warn:coreos:destructive-install`

`coreos-installer install /dev/disk/by-id/nvme-EXAMPLE_SYSTEM_DISK --ignition-file <file>.ign` wipes the selected disk. The disk-snapshot rehearsal follows installation; it is not a pre-install non-destructive step (`alg:coreos:reboot-rehearsal`).

**Precondition (Out-of-band recovery before reboot)** · `pre:coreos:out-of-band`

Before depending on a reboot, prove rescue activation, hardware reset and any provider console path. The recovery procedure is (`proto:coreos:rescue`).

**Warning (Power-button menu)** · `warn:coreos:power-button`

The illustrated provider menu distinguished automatic hardware reset from a long power-button press: a long press powered the machine off and left it off, requiring a short press to start it again. Use the reset option for an unresponsive machine rather than assuming a long press reboots it.

**Observation (Firmware dominates reboot)** · `obs:coreos:firmware-overhead`

In the fictional timing example, `systemd-analyze` reports about 24 s: 8 s kernel, 6 s initrd and 10 s userspace. A full reboot takes about 150 s; shutdown and firmware POST account for most of the difference.

## Deployment process · `sec:coreos:deployment-process`

**Rule (Six deployment rules)** · `rule:coreos:deployment-rules`

1. Apply the experimental-host discipline (`rule:coreos:experimentation`).
2. Apply every host change first to a KVM replica with the same image, configuration and boot mode; verify it including a reboot before touching the physical host. This includes installation, Ignition, boot, networking, firewall, system units and updates.
3. Measure the board's reboot and verify recovery access and serial logging before relying on the reboot; choose the alarm from evidence (`rule:dispatch:timing-led-decisions`), (`req:environment:wall-time-reported`), (`alg:coreos:reboot-rehearsal`).
4. Keep process rules in repository documentation, not only in memory or a session.
5. Test confined identities, Quadlets, firewall, boot and updates on FCOS `testing` and `next` replicas at setup, when adding a workaround and before each update window, so the probes show whether a workaround is still needed and whether an update is about to break a function the server depends on. Search upstream for reproduced friction; draft an evidence-bearing reproduction if it is not reported, and retire workarounds when the probes show they are unnecessary.
6. The operator adapts stack variables, account Quadlets, gate recipes, paths and ports within the existing configuration scope, then applies, measures, records and reports the result. The owner decides root changes, secret handling, transfers off the machine and user-visible outages; routine adaptation does not extend that authority.

**Scenario (Blind first reboot)** · `scenario:coreos:blind-reboot`

The first installation reboot had no serial console, illustrated baseline or successful configuration boot. The host did not return, and a guessed 15-minute threshold could not distinguish slow boot from failure. Booting the installed disk inside QEMU from rescue later exposed a pre-existing `/etc/hostname` with Ignition overwrite disabled (`listing:coreos:ignition-failure`). The machine had entered emergency mode without networking or SSH. Adding `overwrite: true` to each content-bearing file repaired this failure; `butane --strict` alone had not detected it.

**Listing (Ignition failure)** · `listing:coreos:ignition-failure`

```
Ignition failed: failed to create files: error creating /sysroot/etc/hostname:
A file exists there already and overwrite is false
```

**Procedure (Rehearse before the physical reboot)** · `alg:coreos:reboot-rehearsal`

1. While the disk is still empty, activate rescue and measure a rescue-to-rescue reboot until ping and SSH return. Use that baseline plus a fixed margin initially; the installed-system measurement refines the operating alarm (`obs:coreos:reboot-alarm`).
2. Prove rescue activation and hardware reset, and obtain a provider console if available.
3. In rescue, boot a disposable FCOS image in QEMU/KVM with the intended Ignition file and the board's illustrated BIOS or UEFI mode. Log serial output; require completed Ignition, key login, SSH through the firewall and a successful VM reboot (`verif:coreos:boot-acceptance`).
4. Install the NVMe with the serial-console arguments in (`listing:coreos:install-command`). This is the destructive boundary; the preceding three steps do not erase the physical disk.
5. Before rebooting the board, boot the installed NVMe in QEMU with `-snapshot` so the rehearsal's first-boot changes are not written back. Inspect bootloader, serial output, embedded configuration checksum and networking.
6. Reboot the physical board with a watcher measuring against the selected alarm and the rescue return path established. Retain the physical reboot result separately from the VM result.

**Observation (Rescue and VM rehearsal timings)** · `obs:coreos:rehearsal-timings`

In the fictional rehearsal, rescue-to-rescue ping returns at 20 s and SSH at 40 s. A 24 GB virtual disk, an image file attached through a loop mount, installs in 45 s, reaches SSH on first boot in 30 s and reboots in 25 s. It reports `running` and zero failed units. The installed disk snapshot boot in QEMU has the same embedded-config checksum as the rehearsal and reaches SSH at 60 s.

**Table (Physical reboot observations)** · `tab:coreos:reboot-times`

|Reboot|Time to SSH|
|------|-----------|
|First boot after install (with Ignition)|160 s|
|Normal reboot|150 s|
|Reboot after the identity/SELinux increment|155 s|
|Reboot with all production services enabled|165 s|
|Later reboots (from the last shutdown log line to sshd listening)|145–160 s|

**Observation (Operating alarm threshold)** · `obs:coreos:reboot-alarm`

The fictional host uses 300 s without SSH as its operating alarm, twice its illustrative normal reboot. Beyond that interval the recovery action is to activate rescue and inspect the serial console. This installed-system threshold is distinct from the initial rescue baseline; select an actual operating threshold from measurements on the target board.

**Verification (Boot acceptance)** · `verif:coreos:boot-acceptance`

Require completed Ignition, key login to the configured accounts, firewall-permitted SSH, a returning VM reboot, `systemctl is-system-running` reporting `running` and zero failed units. The example installation also requires SELinux enforcing and nftables, sshd and Zincati active; its fixture first SSH is at 160 s (`obs:coreos:installation-result`).

**Procedure (Pin identity at verified first login)** · `alg:coreos:pin-identity`

After the first verified login, retain the SSH host-key fingerprint and the NVMe serial, board serial, system UUID and NIC MAC in the private record. Rescue confirmation sometimes omitted a host key; the hardware identifiers serve as a machine cross-check in that case. No secret passes through such a session. Keep that fallback distinct from the pinned host-key path in (`proto:coreos:rescue`).
