from __future__ import annotations

import json
from pathlib import Path

import pytest

from neural1.benchmark import benchmark, benchmark_provider, benchmark_world_scaling, main
from neural1.core import Neural1Error
from neural1.models import FakeProvider


def test_installed_archive_reports_recorded_revision(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import importlib
    module = importlib.import_module("neural1.benchmark")
    package = tmp_path / "neural1"
    package.mkdir()
    monkeypatch.setattr(module, "__file__", str(package / "benchmark.py"))
    marker = tmp_path / ".neural1-revision"
    marker.write_text("a" * 40 + "\n")
    assert module.hardware_report(tmp_path)["revision"] == "a" * 40
    marker.write_text("unqualified-placeholder\n")
    assert module.hardware_report(tmp_path)["revision"] is None


def test_hardware_report_requires_absolute_new_output(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        main(["--hardware-report", "--output", "relative.json"])
    output = tmp_path / "native.json"
    assert main(["--hardware-report", "--output", str(output)]) == 0
    payload = json.loads(output.read_text())
    assert payload["hardware_report_only"]
    assert "world" not in payload
    assert "target identity not established" in payload["before"]["claim_scope"]
    with pytest.raises(SystemExit):
        main(["--hardware-report", "--output", str(output)])


def test_workloads_require_commissioned_storage(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        main(["--output", str(tmp_path / "workload.json")])
    assert not list(tmp_path.iterdir())


def test_benchmark_helper_bounds_and_provider_guard(tmp_path: Path) -> None:
    with pytest.raises(Neural1Error):
        benchmark(tmp_path, iterations=0)
    with pytest.raises(Neural1Error):
        benchmark_world_scaling(world_counts=(1000000,))
    with pytest.raises(Neural1Error):
        benchmark_provider(FakeProvider(), prompts=["x"] * 5)
    def stop() -> None:
        raise Neural1Error("resource stop")
    with pytest.raises(Neural1Error, match="resource stop"):
        benchmark_provider(FakeProvider(), prompts=["x"], check=stop)
