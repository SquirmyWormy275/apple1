# 2026-09-02 FT232R open analyzer packet

- Execution: `COMPLETE`
- Scientific result: `INCONCLUSIVE` as to root cause
- Packet: `COMPLETE_WITH_EXTERNAL_MEDIA`
- Portability: `NOT_SELF_CONTAINED_MEDIA`
- Live authority: `NONE`; the one controlled open is spent and must not be repeated under this record

The controlled no-transmit open reproduced display corruption. Across all 120,000,000 controlled-capture samples, TX-O and RX-I remained digitally high with zero threshold crossings. DTR and RTS are not routed through the installed four-conductor breakout-to-board interconnect. UART-data transitions and wired DTR/RTS control are therefore unsupported as the mechanism.

Propeller `RESn` was not probed. Analog rail, regulator, ground-reference, sub-threshold, and shared CFFA1 load behavior remain unresolved. The externally held display MOV files are hash-identified in `external-media-manifest.json` and documented in `display-video-record.md`; Codex did not inspect their bytes.
