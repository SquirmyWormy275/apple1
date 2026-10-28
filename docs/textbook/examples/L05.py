from tools.textbook_support import emit

record = {
    "tag": "example:latest",
    "manifest_digest": "a" * 64,
    "weight_digest": "b" * 64,
    "quantization": "teaching example",
    "evidence": "SYNTHETIC",
}
emit(record)
assert record["manifest_digest"] != record["weight_digest"]
