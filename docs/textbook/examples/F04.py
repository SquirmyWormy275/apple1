from pathlib import Path
from tempfile import TemporaryDirectory

from neural1.qualification import qualify_registry
from neural1.registry import ModelRegistry, RegisteredModel

registry = ModelRegistry()
registry.add(
    RegisteredModel(
        "fake", "fixture", "test", "fake", "fake-v1", "0", "NONE", 512, "fixture", "TEST-ONLY", {"default": "0200: 00", "max_tokens": 8}
    )
)
with TemporaryDirectory() as d:
    path = Path(d) / "registry.json"
    registry.save(path)
    result = qualify_registry(path, Path(d) / "qualification.json")
    print("Qualified fixture:", result["qualified"])
    print("Repeated response identical:", result["results"][0]["repeat_identical"])
    assert result["qualified"] and result["results"][0]["repeat_identical"]
