# Probe-point evidence record

## Observations

- Analyzer GND was attached at the analyzer-side ground position adjacent to CH7, chosen to avoid the CH6-adjacent position that SparkFun warns may not be ground on some units.
- Board ground was the `GND` pin on the silkscreen-labelled four-pin USB INTERFACE header.
- CH0 was attached to the `TX-O` pin and CH1 to the `RX-I` pin on that same silkscreen-labelled header.
- The `3.3V` header pin was deliberately not probed because it is a supply rail.
- DTR and RTS were observed as unpopulated breakout pads; they are not routed through the installed four-conductor breakout-to-mainboard interconnect.
- No evidenced safe access point for Propeller `RESn` was established. It was not probed.
- No physical change was made to the board, breakout, analyzer, Pi, CFFA1, CF card, cabling, jumpers, switch position, or power topology.

## Evidence limits and inference

Point identification was based on visible breakout silkscreen and observations recorded during the session. The photos remain external and are not represented by an empty `photos/` directory. The observations support the identity of the two captured UART nets and the absence of wired DTR/RTS from the installed interconnect. They do not establish whether `RESn` transitioned or whether analog power or ground behavior occurred.
