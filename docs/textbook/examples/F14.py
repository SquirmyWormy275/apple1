from tempfile import TemporaryDirectory

from neural1.models import FakeProvider
from neural1.runtime import ExperimentRuntime, RunManifest
from neural1.world import VirtualApple1World

with TemporaryDirectory() as d:
    runtime = ExperimentRuntime(d)
    world = VirtualApple1World()
    world.host_write(0x300, b"ABC")
    snapshot = runtime.snapshot(world)
    world.host_write(0x300, b"XYZ")
    restored = runtime.restore(snapshot)
    base = RunManifest.create("4k-mind", 7, FakeProvider().record, {"ram_budget": 4096})
    fork = runtime.fork(base, fork_point="snapshot", changed_factor="ram_budget", config={"ram_budget": 1024})
    print("Restored:", repr(restored.host_read(0x300, 3)))
    print("Fork names parent:", fork.parent_run_id == base.run_id)
    print("Changed factor:", fork.changed_factor)
    assert restored.host_read(0x300, 3) == b"ABC" and fork.run_id != base.run_id
