# S01 Source notes

Every Apple-1-specific and historical claim in this lesson packet, with the
source it rests on. Following the preservation dossier's evidence rules, facts,
models, and claims still needing verification are recorded separately.

## Sources used

| Key | Source |
|---|---|
| OWAD | Owad, Tom. *Apple I Replica Creation: Back to the Garage.* Syngress. Copy held in the project collection as `AppleIReplicaCreationTomOwad.pdf`. |
| WOZ-FWD | Wozniak, Steve. Foreword to OWAD, dated January 2005. Cited separately because it is first-person recollection, not the author's research. |
| BRIEL | Briel Computers. *Replica 1 Plus User Manual*, June 2014. Copy held in the project collection as `Replica_One_Plus_Manual_-_June_2014.pdf`. |
| REPO | This repository's own documents, cited by path. |

Page numbers below are the printed page numbers appearing in the indexed text of
those PDFs. See "Claims still needing verification" for the limits of that.

## Claim-by-claim

### The board

| Claim in the lesson | Source | Basis |
|---|---|---|
| Retail price was $666.66 | OWAD ch. 1, p. 20; also WOZ-FWD p. 18 | "The retail price of $666.66 wasn't much." Wozniak: "I was into repeating digits so we priced it at $666.66 retail." Two independent statements in the same volume. |
| About two hundred were made | OWAD ch. 1, p. 20; BRIEL ch. 1, p. 6 | OWAD: "Two hundred were made." BRIEL: "200 boards were printed and most of them were assembled but not all of them." |
| The price bought the assembled board alone | OWAD ch. 1, p. 20 | "all that bought you was the circuit board" |
| The buyer supplied keyboard, power supply, and display | OWAD ch. 1, p. 20 | "It was up to the user to find a keyboard, power supply, and video monitor." |
| A keyboard and display were the normal way to use it, unlike the Altair | OWAD ch. 1, p. 20 | "The Apple I was the first computer of its kind to use a keyboard and monitor as standard input/output devices. Most competing systems, such as the Altair, used rows of lights and switches." |
| Apple Computer Company started in April 1976 | BRIEL ch. 1, p. 6 | "In April 1976, Steve Jobs and Steve Wozniak decided to start Apple Computer Company." Stated in the lesson only as background, not as a dated corporate record. |

### The monitor

| Claim in the lesson | Source | Basis |
|---|---|---|
| Wozniak named the program a "monitor" | WOZ-FWD p. 17 | "I saw that I could write a short program that monitored the keyboard for input to do what the old front panels had done. I called this program a monitor." |
| It is 256 bytes | WOZ-FWD p. 17; OWAD ch. 7, p. 224 | Wozniak: "It took 256 bytes, which was 2 PROM chips in 1975." OWAD: "256, bytes of addressable space, exactly the number we need for the Monitor ROM range of $FF00 to $FFFF." |
| It occupies `$FF00` to `$FFFF` | OWAD ch. 7, p. 224 | Same passage. |
| It runs after reset | BRIEL ch. 5, p. 20 | "simply power up your replica 1 ... press the reset button ... you will see a backslash and the cursor will drop below the backslash. You are now in the Woz monitor." Describes the replica; the lesson does not claim a measured reset behavior for this project's machine. |
| It does three things: show memory, change memory, run a program | BRIEL ch. 5, pp. 20 to 21 | "There are three basic functions to the Woz monitor": examine a range or one location; program a location; "start your program by entering the memory location that it starts at followed by R for run." |
| It is stored in ROM, which keeps its contents without power | OWAD ch. 7, p. 224 sidebar | "EPROMs and EEPROMs can be read an unlimited number of times." Read-only memory retaining contents is general computing background, not an Apple-1-specific claim. |

### The replica

| Claim in the lesson | Source | Basis |
|---|---|---|
| The Replica 1 Plus is a modern reproduction with its own user manual | BRIEL, title page and throughout | The manual is the product's own documentation, dated June 2014. |
| Its ROM holds BASIC, the Woz monitor, and an assembler | BRIEL ch. 5, p. 22 | "The replica 1 has 8K of EEPROM (ROM) space onboard. 4K is used for BASIC; 256 bytes are used for the Woz monitor. This leaves just under 4K ... occupied with a powerful assembler called Krusader." |
| A 1976 Apple-1 did not ship BASIC in ROM; BASIC came on cassette | OWAD ch. 1, pp. 20 to 21 | "Apple BASIC was only available on cassette." BASIC is listed among the nine cassette programs Apple sold. See verification note 3. |
| The replica uses an EEPROM rather than the original's PROM arrangement | OWAD ch. 7, p. 224 | "The Replica I uses an altenative chip for the ROM, a 28c64." Note: OWAD describes the earlier Replica I, not the Replica 1 Plus. The lesson does not name a part number for this reason. |

### Repository claims

| Claim in the lesson | Source |
|---|---|
| Display material is written to 40 columns in upper-case printable ASCII | REPO `docs/apple1-learning-library-curriculum.md`, library design rule 4; `tools/apple1_text.py` default `width = 40` |
| A manual or vendor source archive is not proof of an installed EEPROM image | REPO `docs/preservation-dossier.md`, "Current boundaries"; `docs/reference/README.md` |
| No firmware, EEPROM, CFFA1, serial, or physical action belongs in a lesson | REPO `docs/apple1-learning-library-curriculum.md`, library design rule 6; `docs/preservation-dossier.md` |

## Claims still needing verification

1. **Page numbers.** The citations above come from indexed text of the project
   PDFs, not from a page-by-page read of the local copies in
   `Manuals and Documentation/`. A reviewer should confirm each page number
   against the PDF before this packet goes on the card.
2. **Made versus sold.** OWAD ch. 1 says two hundred were made. WOZ-FWD p. 18
   says "we sold maybe only 150." These are compatible if some boards were made
   and not sold, but the lesson says only "about two hundred were made" and
   makes no claim about how many were sold. Do not let this drift into a
   sales figure without a better source.
3. **BASIC in ROM.** "Apple BASIC was only available on cassette" supports the
   lesson's statement that a 1976 Apple-1 did not ship BASIC in ROM, but the
   inference is the author's, not a direct statement. A citation from the
   Apple-1 Operation Manual or the Apple-1 BASIC Manual would settle it. Both
   are in the project collection and were not consulted for this packet.
4. **Manual edition and identity.** The project knowledge base indexes a file
   named `Replica_One_Plus_Manual__June_2014.pdf`; the local collection folder
   holds `Replica_One_Plus_Manual_-_June_2014.pdf`. These are presumed to be the
   same June 2014 edition, but the filenames differ and no SHA-256 comparison
   was run. `docs/collection-archive.md` requires the hash before a manual is
   treated as a fixed reference.
5. **This machine's ROM.** Every replica claim above describes what the 2014
   manual says the product contains. Nothing in this packet establishes what is
   installed on this project's board. Per `docs/preservation-dossier.md`, the
   vendor `110REV03` source is candidate evidence only.

## What no source here establishes

None of these sources, and no combination of them, shows that this project's
Replica 1 Plus powers on, displays text, or moves a byte over its serial port.
A manual describes a design. A book describes history. Neither is a measurement
of this machine.
