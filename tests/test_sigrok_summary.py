from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from tools.sigrok_summary import sample_rate, summarize, write_json


def saved(path: Path, chunks: list[bytes], *, probes: str = "probe1=D0\nprobe2=D1\n", unitsize: int = 1,
          rate: str = "4 MHz", numbers: list[int] | None = None) -> Path:
    with ZipFile(path, "w") as archive:
        archive.writestr("version", "2")
        archive.writestr("metadata", "[global]\nsigrok version=test\n[device 1]\ncapturefile=logic-1\n"
                         f"unitsize={unitsize}\ntotal probes=8\ntotal analog=0\nsamplerate={rate}\n{probes}")
        for number, data in zip(numbers or range(1, len(chunks) + 1), chunks, strict=True):
            archive.writestr(f"logic-1-{number}", data)
    return path


def test_constant_high_and_disabled_bits(tmp_path: Path) -> None:
    # The unrecorded third bit toggles; it must not appear as an observed signal.
    result = summarize(saved(tmp_path / "constant.sr", [b"\x03\x07", b"\x07\x03"]), expected_samples=4)
    assert result["sample_count"] == 4
    assert result["duration_seconds"] == 0.000001
    assert len(result["enabled_channels"]) == 2
    for channel in result["enabled_channels"]:
        assert channel["high_samples"] == 4
        assert channel["low_samples"] == channel["transitions"] == 0


def test_sparse_probe_mapping_and_chunk_boundary_edges(tmp_path: Path) -> None:
    result = summarize(saved(tmp_path / "sparse.sr", [b"\x00\x00", b"\x04\x04", b"\x00"], probes="probe3=RESn\n"))
    channel, = result["enabled_channels"]
    assert channel == {"bit": 2, "label": "RESn", "high_samples": 2, "low_samples": 3,
                       "rising_edges": 1, "falling_edges": 1, "transitions": 2, "initial": 0, "final": 0}


def test_numeric_chunk_order(tmp_path: Path) -> None:
    chunks = [b"\x00"] * 9 + [b"\x01"] * 3
    result = summarize(saved(tmp_path / "order.sr", chunks, probes="probe1=D0\n"))
    assert result["enabled_channels"][0]["transitions"] == 1


def test_read_buffer_boundary(tmp_path: Path) -> None:
    result = summarize(saved(tmp_path / "large.sr", [b"\x00" * (1024 * 1024) + b"\x01"], probes="probe1=D0\n"))
    assert result["enabled_channels"][0]["rising_edges"] == 1


@pytest.mark.parametrize("kwargs", [{"unitsize": 2}, {"rate": "0 Hz"}, {"probes": "probe9=X\n"},
                                   {"probes": "probe1=X\nprobe2=X\n"}, {"probes": ""}, {"numbers": [1, 3]}])
def test_unsupported_or_inconsistent_metadata(tmp_path: Path, kwargs: dict) -> None:
    with pytest.raises(ValueError):
        summarize(saved(tmp_path / "invalid.sr", [b"\x00", b"\x01"], **kwargs))


def test_expected_count_and_empty_data(tmp_path: Path) -> None:
    path = saved(tmp_path / "capture.sr", [b"\x00"])
    with pytest.raises(ValueError, match="sample count mismatch"):
        summarize(path, expected_samples=2)
    with pytest.raises(ValueError, match="empty chunk"):
        summarize(saved(tmp_path / "empty.sr", [b""]))


def test_regular_file_only_and_no_overwrite(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="regular file"):
        summarize(tmp_path)
    target = tmp_path / "preserved.json"
    target.write_text("original")
    with pytest.raises(FileExistsError):
        write_json(target, {"replacement": True})
    assert target.read_text() == "original"


def test_sample_rate() -> None:
    assert sample_rate("4 MHz") == 4_000_000
    assert sample_rate("9600 Hz") == 9600
    with pytest.raises(ValueError):
        sample_rate("0.1 Hz")


@settings(max_examples=30)
@given(st.binary(min_size=2, max_size=100))
def test_counts_against_independent_bitwise_oracle(data: bytes) -> None:
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as temporary:
        result = summarize(saved(Path(temporary) / "oracle.sr", [data[:1], data[1:]]))
    for channel in result["enabled_channels"]:
        bits = [(value >> channel["bit"]) & 1 for value in data]
        assert channel["high_samples"] == sum(bits)
        assert channel["transitions"] == sum(a != b for a, b in zip(bits, bits[1:], strict=False))
        assert channel["initial"] == bits[0]
        assert channel["final"] == bits[-1]
