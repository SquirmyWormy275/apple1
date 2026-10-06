# Wooden enclosure — current design reference (R04)

**Current revision: R04. Locked as the project enclosure design reference by Alex on October 5, 2026.**

Use this record and the [R04 drawing](Apple1_Wooden_Enclosure_R04.pdf) for the wooden enclosure. Earlier R01–R03 drawings and conflicting chat descriptions are superseded. Future design changes must update this record and the drawing together in a new revision; do not silently substitute different geometry.

The keyboard deck **slopes upward away from the user, then meets a flat rear monitor shelf at the same height**. The transition changes angle from inclined to horizontal, with a flush joint. Sanyo VM-4209 rests directly on the level shelf.

This locks the design baseline. It does not change the documented component uncertainties into measured fit evidence or release the remaining assembly details for fabrication.

## Dimensions

All dimensions are millimetres. These are proposed project design dimensions, not recovered dimensions of a historical Apple-1 case.

| Item | R04 design |
|---|---|
| Overall footprint | 460 wide × 560 deep |
| Front keyboard deck, horizontal run | 210 |
| Flat rear shelf depth | 350 |
| Front deck surface height | 135 above exterior bottom |
| Deck/shelf transition | Depth 210 from front; surface height 180 |
| Rear shelf surface height | 180, level through rear edge |
| Keyboard deck rise / angle | 45 over 210; approximately 12.09° |
| Side walls / shelf | 18 thick |
| Keyboard deck | 18 thick, measured normal to its surface |
| Removable bottom | 12 thick |
| Clear interior width | 424 |
| Optional raised side trim | 8 above deck; additional to surface heights |
| Feet | Additional to quoted heights; selection not fixed |
| Sanyo planning footprint | 230 wide × 285 deep, within depth 235–520 |
| Keyboard PCB reference | 298.45 × 139.7; conditional on actual keyboard variant |

Mount the keyboard parallel to the front incline. The woodworker already holds the physical keyboard: transfer the aperture, brackets and keycap clearance from that assembly. The PCB reference rectangle is not a routing template. Wood species, finish and joinery remain unspecified.

The 18 mm sloping deck and flat shelf undersides must be joined without obstructing the interior; the drawing shows their intersecting underside planes. The shelf must have suitable structural support for the monitor, with supports outside the card zone.

## CFFA1 and CompactFlash clearance

Keep the complete upright CFFA1 plus inserted CF card beneath the **flat shelf**. The drawing marks depth 430–540 from the front as the card zone. Keep the motherboard horizontal and limit the complete mounting rise, including any baseplate, to 10.

| Stack item | Allocated height |
|---|---:|
| Motherboard mounts, including any baseplate | 10 |
| Motherboard PCB | 2 |
| Slot connector | 20 |
| Entire CFFA1 PCB | 65 |
| Entire CF card length above adapter | 37 |
| **Total conservative allocation** | **134** |
| Interior: 180 shelf height − 18 shelf − 12 bottom | **150** |
| **Remaining allocated clearance** | **16** |

The entire adapter is counted above the entire connector, and the entire CF card above the entire adapter. Installed parts overlap, so this allocation deliberately double-counts those overlaps. Keep rails, screws, cables and supports out of the clearance zone. Each millimetre of mounting rise beyond the allocated 10 reduces the gap by one millimetre.

The CFFA1 PCB allowance comes from a manufacturer Rev D photograph: approximately 18 pixels per 3.9624 mm contact pitch and approximately 242 pixels of PCB height imply about 53.3 mm. Treat this as a 53–55 mm estimate, enlarged to 65 for this budget. This is **not a manufacturer-certified dimensional bound**. Recovered project records identify CFFA1 but do not establish the actual unit revision or measured installed height. Retailer shipping-size fields are not board dimensions.

CompactFlash manufacturer dimensions give length 36.40 ± 0.15; this design rounds up to 37 and counts that entire length above the adapter. The connector allowance is 20; EDAC 305/355 housing height is 11.94. Motherboard thickness and mounting values are design allowances.

For CF service: shut down, remove power, lift off the Sanyo, unscrew and remove the flat shelf, then withdraw the card through the open rear bay. Use screws and threaded inserts for shelf access. The 16 mm closed-shelf gap is not card-withdrawal access.

## Assembly allocation and remaining fitting work

The width allocation is 230 for motherboard/card, 20 gap, 160 for NEURAL1, and 14 spare. These are planning zones, not verified installed envelopes. Orient/place the motherboard so the entire upright card envelope occupies the marked shelf zone; mainboard outline and holes still require fitting.

The historical NEURAL1 tray proposal is 160 × 125 with a 35 flange. Rev A was withdrawn. Corrected tray geometry and installed assembly size remain unresolved. Do not fabricate the withdrawn tray solely because its planning envelope appears here.

Remaining fitting/construction items are the actual keyboard aperture and brackets, motherboard placement and holes, corrected NEURAL1 tray, connector openings and ventilation, and shelf support strength. Preserve monitor ventilation space behind the monitor cabinet and room for the PL-259 connector and cable bend; the case rear edge is not itself the ventilation clearance.

## Source basis and artifact identity

The profile follows Alex's explicit correction on October 5: the keyboard slopes up, flattens out, and meets a shelf. The previously supplied enclosure photographs are visual references, not dimensional drawings. R04 supersedes the stepped R02 and full-length-incline R03 interpretations.

The repository PDF contains the **unchanged first three pages** of the approved four-page R04 brief: side profile, plan and clearance calculation. The fourth page's external reference photographs are omitted from the repository copy under the existing [heritage-art boundary](../../repository/architecture.md#art-and-heritage-references); their evidence and source links are recorded here. Drawing geometry and fit allowances are unchanged.

- Repository PDF SHA-256: `0f46b092bb7d466e223e3eca33bb9596932c3db1e8ecaf8da7099c17d486b2cb`
- Original four-page R04 brief SHA-256: `d54884b1abc9acbb5f018c876ce40ba13bc5bca13d2f29b1ed372efa84d46410`
- Repository PDF size: 28823 bytes; three pages.
- Authority class: project-approved design baseline / derived documentation, with conditional engineering reconstruction. This is not measured physical qualification.

Primary source references retained from the enclosure research:

- [R&D Automation CFFA1 product and Rev D photograph](https://dreher.net/?s=projects/CFforApple1&c=projects/CFforApple1/main.php)
- [CFFA1 Manual 1.1, installed geometry and PCB outline](https://dreher.net/projects/CFforApple1/downloads/CFFA1_Manual_1.1.pdf)
- [Apple-1 expansion documentation, 44-pin 0.156-inch pitch](https://apple1notes.com/wp-content/uploads/2020/07/Apple-1-Expansion-Documentation.pdf)
- [EDAC connector dimensions](https://edac.net/products/card-edge-connectors/110)
- [SanDisk CompactFlash manual, revision 10.1, table 2-5](https://retrocmp.de/hardware/cf-dom/sandisk.pdf)
- [Schlaepfer Datanetics PCB dimensions](https://github.com/schlae/replica-datanetics)
- [Original Datanetics bracket reference](https://www.willegal.net/appleii/apple1-datanetics.htm)
- [Henry Ford Sanyo VM-4209 specimen and ventilation label](https://www.thehenryford.org/collections/explore/artifact/400080)
- [Archived Sanyo service manual](https://archive.org/details/manual_VM4209_SM_SANYO_EN)

The Sanyo museum specimen is 228.6 wide × 260.35 deep × 266.7 high; the archived 220 V / 50 Hz manual gives approximately 220 wide × 285 deep × 255 high. R04 uses a 230 × 285 planning footprint, not a measurement of Alex's monitor. The museum label specifies at least 50.8 behind the monitor cabinet; allow additional connector and cable space.
