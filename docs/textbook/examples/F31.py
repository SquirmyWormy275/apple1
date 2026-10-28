from tools.capture_manifest import ManifestValidationError, validate_manifest

try:
    validate_manifest({"result": "PASS"})
    raise AssertionError("incomplete evidence must fail")
except ManifestValidationError as error:
    print("Incomplete PASS record refused:", str(error))
