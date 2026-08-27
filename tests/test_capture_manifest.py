from __future__ import annotations

import pytest

from tools.capture_manifest import ManifestValidationError, validate_manifest


def valid_manifest() -> dict[str, object]:
    return {
        "target_identity": {
            "by_id": "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_00000000-if00-port0",
            "by_path": "/dev/serial/by-path/platform-xhci-hcd.0-usbv2-0:2:1.0-port0",
        },
        "timestamp_utc": "2026-08-27T00:00:00+00:00",
        "board_revision": "unverified",
        "power_source": "unverified",
        "usb_topology": "platform-xhci-hcd.0-usbv2-0:2:1.0-port0",
        "result": "INCONCLUSIVE",
    }


def test_valid_manifest_passes() -> None:
    validate_manifest(valid_manifest())


@pytest.mark.parametrize("field", ("target_identity", "timestamp_utc", "board_revision", "power_source", "usb_topology", "result"))
def test_manifest_rejects_missing_evidence(field: str) -> None:
    manifest = valid_manifest()
    manifest.pop(field)

    with pytest.raises(ManifestValidationError):
        validate_manifest(manifest)


def test_manifest_rejects_unknown_result_classification() -> None:
    manifest = valid_manifest()
    manifest["result"] = "maybe"

    with pytest.raises(ManifestValidationError):
        validate_manifest(manifest)
