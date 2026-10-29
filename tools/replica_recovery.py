"""Verify, rebuild or print commands for the staged Replica firmware; never upload."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import shutil
import struct
import subprocess
import tarfile
from pathlib import Path

RELEASE = "110REV03-2026-10-28"
DEFAULT_PACKAGE = Path(__file__).resolve().parents[1] / "firmware" / "recovery" / RELEASE
ALIASES = {
    "fullduplex.spin": "FullDuplex.spin",
    "keyboard.spin": "Keyboard.spin",
    "aigeneric_driver.spin": "AiGeneric_Driver.spin",
    "Font_ATARI.spin": "Font_Atari.spin",
}
LOADER_VERSION = "v1.0-37-15-ga1b4cd8 (2026-10-28 staged recovery)"
CALL_FRAME = bytes.fromhex("fffff9fffffff9ff")


def image_report(binary: bytes, eeprom: bytes) -> dict[str, object]:
    if not 16 < len(binary) <= 32768 or len(binary) % 4 or len(eeprom) != 32768:
        raise ValueError("Invalid P1 image size/alignment")
    freq, mode, checksum, pbase, vbase, dbase, pcurr, dcurr = struct.unpack("<IBBHHHHH", binary[:16])
    if (freq, mode, pbase, vbase) != (80000000, 0x6F, 16, len(binary)):
        raise ValueError("Unexpected 110REV03 clock/header")
    if not (pbase <= pcurr < vbase <= dbase - 8 < dbase <= 32764 and dcurr == dbase + 4):
        raise ValueError("Invalid P1 code/data/stack pointers")
    padded = bytearray(32768)
    padded[:len(binary)] = binary
    padded[dbase - 8:dbase] = CALL_FRAME
    if sum(padded) % 256 or eeprom != bytes(padded):
        raise ValueError("P1 checksum, call frame or EEPROM padding mismatch")
    return {"program_bytes": len(binary), "eeprom_bytes": len(eeprom), "clock_hz": freq,
            "clock_mode": mode, "checksum_byte": checksum, "pbase": pbase, "vbase": vbase,
            "dbase": dbase, "pcurr": pcurr, "dcurr": dcurr, "image_format_valid": True,
            "hardware_qualified": False}


def verify_package(package: Path) -> dict[str, object]:
    package = package.resolve()
    root = package.parents[2]
    manifest = json.loads((package / "manifest.json").read_text())
    for name, entry in manifest["files"].items():
        path = (root / name).resolve()
        if not path.is_relative_to(root):
            raise ValueError(f"Path outside package checkout: {name}")
        data = path.read_bytes()
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise ValueError(f"Checksum/size mismatch: {name}")
    binary = (package / "images/replica-110REV03.binary").read_bytes()
    eeprom = (package / "images/replica-110REV03.eeprom").read_bytes()
    return {"verified_files": len(manifest["files"]), **image_report(binary, eeprom),
            "device_access": False}


def rebuild(package: Path, output: Path, cc: str = "gcc", cxx: str = "g++") -> dict[str, object]:
    package = package.resolve()
    verify_package(package)
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, SOURCE_DATE_EPOCH="1793145600")  # 2026-10-28 00:00 UTC
    commands: list[list[str]] = []

    def run(argv: list[str], cwd: Path, log: str) -> None:
        commands.append(argv)
        with (output / log).open("w") as stream:
            subprocess.run(argv, cwd=cwd, env=env, stdout=stream,  # noqa: S603 - pinned source, explicit build tool
                           stderr=subprocess.STDOUT, check=True)

    for name in ("OpenSpin", "PropLoader"):
        source = output / name
        source.mkdir()
        with tarfile.open(package / "sources" / f"{name}.tar.gz") as archive:
            archive.extractall(source, filter="data")
    run(["make", "-j2", f"CC={cc}", f"CXX={cxx}"], output / "OpenSpin", "openspin-build.log")
    compiler = output / "OpenSpin/build/openspin"
    run(["make", "-j2", "OS=linux", f"CC={cc}", f"CPP={cxx}", f"TOOLCC={cc}",
         f"SPINCMP={compiler}", f"VERSION={LOADER_VERSION}"], output / "PropLoader", "proploader-build.log")
    stage = output / "vendor-stage"
    stage.mkdir()
    vendor = package.parents[1] / "vendor/110REV03"
    for path in vendor.iterdir():
        if path.is_file():
            shutil.copy2(path, stage / path.name)
    for alias, original in ALIASES.items():
        (stage / alias).symlink_to(original)
    images = output / "images"
    images.mkdir()
    for flag, extension in (("-b", "binary"), ("-e", "eeprom")):
        dest = images / f"replica-110REV03.{extension}"
        run([str(compiler), flag, "-o", str(dest), "replica 110REV03.spin"], stage, f"compile-{extension}.log")
        if dest.read_bytes() != (package / "images" / dest.name).read_bytes():
            raise ValueError(f"Rebuild differs: {dest.name}")
    report = {"firmware_byte_identical": True, "device_access": False,
              "host_architecture": os.uname().machine, "cc": cc, "cxx": cxx,
              "source_date_epoch": env["SOURCE_DATE_EPOCH"], "commands": commands,
              **image_report((images / "replica-110REV03.binary").read_bytes(),
                             (images / "replica-110REV03.eeprom").read_bytes())}
    (output / "rebuild-report.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def load_commands(
    package: Path, by_id: str, by_path: str, mode: str, session_dir: Path | None = None,
) -> dict[str, object]:
    if not by_id.startswith("/dev/serial/by-id/") or not by_path.startswith("/dev/serial/by-path/"):
        raise ValueError("Supply both current /dev/serial/by-id and by-path names")
    if any(c in by_id + by_path for c in "\x00\n\r"):
        raise ValueError("Invalid port name")
    package = package.resolve()
    argv = [str(package / "bin/linux-x86_64/proploader"), "-I", str(package / "config"),
            "-b", "replica1", "-s", "-p", by_id, "-r", "-t"]
    if mode == "spare-eeprom":
        argv.append("-e")
    argv.append(str(package / "images/replica-110REV03.binary"))
    check = ("import pathlib,stat,sys; a=pathlib.Path(sys.argv[1]); b=pathlib.Path(sys.argv[2]); "
             "assert a.is_symlink() and b.is_symlink(); "
             "assert a.resolve(strict=True)==b.resolve(strict=True); "
             "assert stat.S_ISCHR(a.stat().st_mode); print('Identity paths match; port unopened')")
    session = session_dir or Path("out/replica-recovery/NEW-SESSION")
    recording = ["script", "-qef", "--log-out", str(session / f"{mode}.typescript"),
                 "--command", shlex.join(argv)]
    return {"mode": mode, "executed": False, "device_access": False,
            "binding_precheck": shlex.join(["python3", "-c", check, by_id, by_path]),
            "loader_argv": argv, "loader_command": shlex.join(argv),
            "recording_argv": recording, "recording_command": shlex.join(recording),
            "terminal_exit": "Escape; closing may discard a RAM trial if the board resets",
            "requires": "Reviewed physical setup/power/reset path; spare installed for EEPROM mode"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, default=DEFAULT_PACKAGE)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("verify")
    build = sub.add_parser("rebuild")
    build.add_argument("--out", type=Path, required=True)
    build.add_argument("--cc", default="gcc")
    build.add_argument("--cxx", default="g++")
    cmd = sub.add_parser("commands")
    cmd.add_argument("--by-id", required=True)
    cmd.add_argument("--by-path", required=True)
    cmd.add_argument("--mode", choices=("ram", "spare-eeprom"), default="ram")
    cmd.add_argument("--session-dir", type=Path)
    args = parser.parse_args()
    try:
        result = verify_package(args.package)
        if args.action == "rebuild":
            result = rebuild(args.package, args.out, args.cc, args.cxx)
        elif args.action == "commands":
            result = load_commands(args.package, args.by_id, args.by_path, args.mode, args.session_dir)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"Recovery preparation failed: {exc}\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
