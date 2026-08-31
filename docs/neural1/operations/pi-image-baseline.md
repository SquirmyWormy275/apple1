# Read-only Pi image baseline procedure

This procedure derives a software/BOM baseline from a preserved Pi image without modifying the image or the physical card.

## 1. Raw-image inspection

Run the repository tool directly against the raw image:

```bash
neural1-storage inspect-image /path/to/neural1-pi.img --sha256
```

This operation opens the image read-only and reports byte size, MBR signature validity, disk signature, partition entries, and (when requested) SHA-256.

Compare the result to the committed [preservation record](../preservation/pi-image-2026-08-30.md) and the private local checksum/metadata stored beside the image.

## 2. Read-only filesystem access

Filesystem inspection must use a read-only mapping. On Linux, a suitable operator-controlled sequence is:

```bash
sudo losetup --find --show --partscan --read-only /path/to/neural1-pi.img
```

Record the returned loop device, inspect its partitions, and mount only the desired partition(s) read-only. For an ext filesystem, use read-only options that prevent journal replay where supported by the host tooling. Do not use a writable loop mapping.

The repository deliberately does not automate privileged loop-device creation or mounting. Device identity and privilege boundaries must remain visible to the operator.

## 3. Software/BOM collection

Once the root filesystem is mounted read-only:

```bash
neural1-storage baseline-rootfs /mnt/neural1-root \
  --output /path/to/local/pi-rootfs-baseline.json
```

The baseline collector reads:

- `/etc/os-release`
- non-comment `/etc/fstab` entries
- hashes and sizes of Raspberry Pi boot configuration files when present
- enabled systemd units represented under `/etc/systemd/system/*.wants/`
- installed Debian package name/version/architecture records from `/var/lib/dpkg/status`

The output is local operational evidence. Review it before deciding whether any machine-specific values belong in the public repository.

## 4. Optional NEURAL1-specific archaeology

After the generic BOM exists, inspect the mounted root for the NEURAL1 checkout, model/runtime directories, Python environments, service unit definitions, caches, and paths referenced by configuration. Record findings in a local archaeology note first. Promote only non-sensitive, durable architecture facts into Git.

## 5. Unmount

Unmount filesystems and detach the read-only loop mapping when inspection is complete. The physical microSD does not need to be accessed for this procedure.
