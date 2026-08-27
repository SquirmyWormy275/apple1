# Replica 1 Plus I/O evidence map

## Confirmed host-side identity

Captured on 2026-08-27 from the connected Raspberry Pi `apple1`:

| Field | Observed value |
|---|---|
| Host account | `squirmywormy275` (member of `dialout`) |
| Device node | `/dev/ttyUSB0` |
| Stable name for this setup | `/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_00000000-if00-port0` |
| Physical USB topology | `/dev/serial/by-path/platform-xhci-hcd.0-usbv2-0:2:1.0-port0` |
| USB device | FTDI FT232R USB UART (`0403:6001`) |
| Kernel driver | `ftdi_sio` |
| USB serial value | `00000000` |

The USB serial value is non-unique. The eventual serial owner must bind both
the recorded by-id path and by-path topology, and fail closed if either changes.

## Unverified board signals

The following remain measurement targets, not wiring instructions: Propeller
P30/P31, Propeller reset, FT232 transmit, CA1, CA2, and the 6821 data bus.
Do not attach a direct CA2-to-Propeller wire: CA2 can be 5 V and Propeller GPIO
is 3.3 V.
