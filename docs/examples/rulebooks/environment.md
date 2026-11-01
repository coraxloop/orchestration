## Build toolbox profile · `sec:environment:build-toolbox-profile`

**Listing (Build-toolbox recipe)** · `listing:environment:build-toolbox-recipe`

The fictional build box is `sagofink-build`. Its recipe pins `PATH` and keeps the cargo home and one target directory per purpose below `/srv/example/example-user/cache/build-box/`:

```bash
example-host-run sagofink-build sh -c 'export PATH=/usr/bin:/bin TMPDIR=/srv/example/example-user/tmp CARGO_HOME=/srv/example/example-user/cache/build-box/cargo CARGO_TARGET_DIR=/srv/example/example-user/cache/build-box/<purpose>; cd <checkout> && example-low-priority cargo build -p <package> --release --locked'
```

## Temporary storage profile · `sec:environment:temporary-storage-profile`

**Setting (Temporary root)** · `setup:environment:temporary-root`

`TMPDIR` is `/srv/example/example-user/tmp`, disk-backed with ample free space, and is exported inside every container command and every stdin-fed script; the fictional `/tmp` is memory-backed and never holds a build or a large file.
