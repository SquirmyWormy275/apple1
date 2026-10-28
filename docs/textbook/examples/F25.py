from pathlib import Path
from tempfile import TemporaryDirectory

from neural1.deployment import verify_storage

with TemporaryDirectory() as d:
    path = Path(d) / "not-an-ssd"
    path.mkdir()
    try:
        verify_storage(path, "TEXTBOOK-NOT-A-REAL-UUID")
        raise AssertionError("ordinary directory must be refused")
    except (ValueError, OSError) as error:
        print("Ordinary directory refused:", type(error).__name__)
    assert list(path.iterdir()) == []
    print("Fallback files created: 0")
