"""Off-device integrity and command-planning checks for the recovery bundle."""
import shlex
from pathlib import Path

import pytest

from tools.replica_recovery import DEFAULT_PACKAGE, image_report, load_commands, verify_package


def test_staged_images_and_source_tool_checksums() -> None:
    report = verify_package(DEFAULT_PACKAGE)
    assert report["image_format_valid"] is True
    assert report["hardware_qualified"] is False
    assert report["device_access"] is False
    assert (report["program_bytes"], report["eeprom_bytes"]) == (6992, 32768)


@pytest.mark.parametrize("target,offset", [("binary", 100), ("eeprom", 20000)])
def test_changed_program_or_eeprom_padding_is_rejected(target: str, offset: int) -> None:
    binary = bytearray((DEFAULT_PACKAGE / "images/replica-110REV03.binary").read_bytes())
    eeprom = bytearray((DEFAULT_PACKAGE / "images/replica-110REV03.eeprom").read_bytes())
    (binary if target == "binary" else eeprom)[offset] ^= 1
    with pytest.raises(ValueError):
        image_report(bytes(binary), bytes(eeprom))


def test_truncated_program_is_rejected() -> None:
    binary = (DEFAULT_PACKAGE / "images/replica-110REV03.binary").read_bytes()
    eeprom = (DEFAULT_PACKAGE / "images/replica-110REV03.eeprom").read_bytes()
    with pytest.raises(ValueError):
        image_report(binary[:-4], eeprom)


@pytest.mark.parametrize("mode", ["ram", "spare-eeprom"])
def test_commands_are_explicit_print_only_and_keep_one_connection(mode: str, tmp_path: Path) -> None:
    by_id = "/dev/serial/by-id/test ' ; dollar$()"
    by_path = "/dev/serial/by-path/test"
    report = load_commands(DEFAULT_PACKAGE, by_id, by_path, mode, tmp_path)
    argv = report["loader_argv"]
    assert isinstance(argv, list)
    assert shlex.split(str(report["loader_command"])) == argv
    assert argv[argv.index("-p") + 1] == by_id
    assert "-s" in argv and "-t" in argv and "-r" in argv
    assert ("-e" in argv) == (mode == "spare-eeprom")
    assert str(argv[-1]).endswith(".binary")
    assert report["executed"] is False and report["device_access"] is False
    recording = shlex.split(str(report["recording_command"]))
    assert recording[-1] == report["loader_command"]
    assert str(tmp_path / f"{mode}.typescript") in recording
    assert by_path in str(report["binding_precheck"])


def test_port_autoselection_is_not_planned() -> None:
    with pytest.raises(ValueError):
        load_commands(DEFAULT_PACKAGE, "/dev/ttyUSB0", "/dev/ttyUSB0", "ram")


def test_profile_preserves_candidate_clock_and_uses_rom_dtr() -> None:
    text = (DEFAULT_PACKAGE / "config/replica1.cfg").read_text()
    assert "loader: rom" in text and "reset: dtr" in text
    assert "clkfreq: 80000000" in text and "clkmode: 0x6f" in text
    assert "loader-baud-rate: 115200" in text and "baud-rate: 9600" in text
