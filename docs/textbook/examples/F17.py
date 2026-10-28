from pathlib import Path
from tempfile import TemporaryDirectory

from neural1.storage_commissioning import inspect_image

with TemporaryDirectory() as d:
    p = Path(d) / "fixture.img"
    data = bytearray(4096)
    data[510:512] = b"\x55\xaa"
    data[450] = 0x0C
    data[454:458] = (1).to_bytes(4, "little")
    data[458:462] = (4).to_bytes(4, "little")
    p.write_bytes(data)
    r = inspect_image(p, include_sha256=True)
    print("Fixture bytes:", r.size_bytes)
    print("MBR signature valid:", r.mbr_signature_valid)
    print("First partition offset:", r.partitions[0].byte_offset)
    assert r.mbr_signature_valid and r.partitions[0].byte_offset == 512
