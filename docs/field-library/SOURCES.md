# Field Library shared source pool

Every lesson packet's `SOURCE-NOTES.md` cites into this file by key. Keeping one
pool means a claim is written down once, with its wording, and every lesson that
leans on it points at the same text.

Nothing in this file is a measurement of this project's Replica 1 Plus.

## Source keys

| Key | Source |
|---|---|
| OWAD | Owad, Tom. *Apple I Replica Creation: Back to the Garage.* Syngress. Project copy: `AppleIReplicaCreationTomOwad.pdf`. |
| WOZ-FWD | Wozniak, Steve. Foreword to OWAD, dated January 2005. First-person recollection, cited separately from the author's research. |
| BRIEL | Briel Computers. *Replica 1 Plus User Manual*, June 2014. Project copy: `Replica_One_Plus_Manual_-_June_2014.pdf`. |
| REPO | This repository, cited by path. |
| RUN | A run performed during authoring, recorded in `EMULATOR-RUNS.md`. |

Page numbers are the printed page numbers in the indexed text of those PDFs.
They have not been checked page by page against the local collection copies.
See "Open verification items" at the end.

---

## H. History and commerce

| ID | Claim | Source | Wording |
|---|---|---|---|
| H-PRICE | Retail price was $666.66 | OWAD ch. 1 p. 20; WOZ-FWD p. 18 | "The retail price of $666.66 wasn't much"; "I was into repeating digits so we priced it at $666.66 retail." |
| H-WHOLESALE | Byte Shop price was $500 each | WOZ-FWD p. 18 | "to sell fully-built and assembled computer boards for $500 each" |
| H-MADE | About two hundred were made | OWAD ch. 1 p. 20; BRIEL ch. 1 p. 6 | "Two hundred were made."; "200 boards were printed and most of them were assembled but not all of them." |
| H-SOLD | Wozniak recalls roughly 150 sold | WOZ-FWD p. 18 | "of which we sold maybe only 150" |
| H-BYTESHOP | The Byte Shop bought 100 | OWAD ch. 1 p. 20 | "The Byte Shop purchased 100 of these." |
| H-BARE | The price bought the bare board | OWAD ch. 1 p. 20 | "all that bought you was the circuit board" |
| H-SUPPLY | Buyer supplied keyboard, power supply, display | OWAD ch. 1 p. 20 | "It was up to the user to find a keyboard, power supply, and video monitor." |
| H-KBD-STD | Keyboard and display as standard I/O was the novelty | OWAD ch. 1 p. 20 | "the first computer of its kind to use a keyboard and monitor as standard input/output devices. Most competing systems, such as the Altair, used rows of lights and switches" |
| H-FOUNDED | Apple Computer Company started April 1976 | BRIEL ch. 1 p. 6 | "In April 1976, Steve Jobs and Steve Wozniak decided to start Apple Computer Company." |
| H-HOMEBREW | Woz distributed schematics and listings free at Homebrew | BRIEL ch. 1 p. 6; WOZ-FWD p. 18 | "Woz distributed schematics and source code listings ... at the Homebrew Computer Club"; "I passed out schematics and code listings freely at our club" |
| H-CASSETTE | Programs were hand-typed or loaded from audio cassette | OWAD ch. 1 p. 20 | "either by typing the machine code in by hand or by transferring the program from an audio cassette" |
| H-BASIC-TAPE | Apple BASIC was only available on cassette | OWAD ch. 1 p. 20 | "Apple BASIC was only available on cassette" |
| H-NINE | Nine programs sold on cassette at $5 each | OWAD ch. 1 p. 21 | "Nine programs were available on cassette: BASIC, Mastermind, Lunar Lander, Blackjack, Hamurabi, Mini-Startrek, 16K-Startrek, DisAssembler, and Extended Monitor. Apple sold these at just $5 each" |
| H-CLUB | Apple I Owners Club founded 1977 by Joe Torzewski | OWAD ch. 1 p. 25 | "In 1977, Joe Torzewski decided to found the Apple I Owners Club"; core of five, roughly 30 members |
| H-TORZEWSKI-16K | Torzewski upgraded his Apple I to 16 KB | OWAD ch. 7 p. 217 | "Joe Torzewski, who started the Apple I Owners Club in 1977, upgraded his Apple I to 16 KB." |
| H-ALTAIR | The Altair had only LEDs and switches | BRIEL ch. 1 p. 6 | "the only major computer out there was the Altair 8800 and that only came with LED's and switches" |
| H-RAM-COST | 8 KB of RAM was prohibitively expensive in 1976 | OWAD ch. 7 p. 217 | "Back in 1976, that 8 KB of RAM was prohibitively expensive." |

## M. Memory, addresses, and the map

| ID | Claim | Source | Wording |
|---|---|---|---|
| M-64K | 64 KB of addressable space; 16-bit address bus | OWAD ch. 7 pp. 206, 216 | "The address bus is 16 bits wide, which means we have enough addresses for 65,536 (64 KB) unique locations"; "The Apple I has 64 KB of addressable space." |
| M-ROM | Monitor ROM is 256 bytes at `$FF00` to `$FFFF` | OWAD ch. 7 pp. 216, 224 | "The Monitor ROM, therefore, starts at $FF00 and ends at $FFFF." |
| M-RESET-VEC | The 6502 takes its start address from the top of memory at reset | OWAD ch. 7 p. 216 | "requires that a memory address be stored at addresses $FFFE and $FFFF ... When the 6502 is reset, it immediately loads the address ... into its program counter". See verification item V-3. |
| M-RAM-ORIG | Original: 4 KB at `$0000`-`$0FFF`, 4 KB at `$E000`-`$EFFF` | OWAD ch. 7 p. 217 | "Four kilobytes are for system and user access. These 4 KB are located at $000-$0FFF. The other 4 KB, which are intended for Apple's Integer BASIC, are located at $E000-$EFFF." |
| M-BASIC-RAM | On the original, `$E000`-`$EFFF` was RAM, so BASIC had to be reloaded every power-up | OWAD ch. 7 p. 217 | "Every time the original Apple I was powered up, the code for BASIC would have to be either loaded from cassette or typed in by hand." |
| M-STACK | The 6502 stack is `$0100`-`$01FF`, base `$01FF`, growing down | OWAD ch. 7 p. 216 | "The stack uses memory from $0100 to $01FF. $01FF is the base address. As data is pushed onto the stack, the stack grows towards $0100." |
| M-REPLICA-MAP | Replica I: 32 KB user space `$0000`-`$8000`; Integer BASIC in ROM at `$E000`-`$EFFF` | OWAD ch. 7 p. 218 | "The first 32 KB ($0000-$8000) are all dedicated to system and user space ... Instead of being in RAM, Integer BASIC is now in ROM." Describes the Replica I, not the Replica 1 Plus. See V-4. |
| M-PIA-RANGE | The PIA occupies `$D010`-`$D012` on the memory map | OWAD ch. 7 pp. 217, 218 (Figures 7.14, 7.15) | "$D010 - $D012 Keyboard In, Video Out" |

## P. Keyboard, display, and the PIA

| ID | Claim | Source | Wording |
|---|---|---|---|
| P-KBD | `$D010` holds the keyboard character; `$D011` is its control register | OWAD ch. 7 pp. 228, 231 | "the keyboard register is at $D010 and the keyboard control register is at $D011. The processor checks for the flag at $D011. When it sees it, the processor goes to $D010 and loads the character." |
| P-DSP | `$D012` is the display register; `$D013` its control register | OWAD ch. 7 p. 228 (Table 7.5) | "DSP Display Register ... $D012"; "DSPCR Display Control Register ... $D013" |
| P-DSP-BUSY | Before sending a character the processor checks bit 7 of `$D012` and waits for it to go low | OWAD ch. 7 p. 231 | "the processor checks bit 7 at memory location $D012. If this bit is high ... The processor waits until the bit goes low" |
| P-KBD-7BIT | A keypress puts a seven-bit ASCII value on the keyboard data lines, with a strobe pulse | OWAD ch. 7 p. 232 | "that character's seven-bit ASCII value is placed on the keyboard's data lines. A pulse on the strobe line indicates the data is ready." |
| P-HIGHBIT | In the Monitor, a keyboard byte is expected to have bit 7 set | BRIEL Appendix C p. 30 | "FF2E: AD 10 D0 LDA KBD Load character. B7 should be '1'." |
| P-DDR | On reset the Monitor configures the 6821; the video port is output except the highest bit, used as Data Available | OWAD ch. 7 p. 226 | "On reset, both ports default to being inputs and the keyboard port is left untouched. The video port is set to output except for the highest bit, which is used as the 'Data Available' line." |
| P-VIDEO-TEXT | The video section is text only and stores a character's ASCII code, not pixels | OWAD ch. 7 p. 234 | "The Apple I's video section is text only. Instead of storing each individual pixel for a character, it stores the character's ASCII code." |
| P-VIDEO-ROM | Only characters present in the video ROM can be displayed; no bitmapped graphics | OWAD ch. 7 p. 234 | "Only the characters stored in that ROM can be displayed on screen. Thus, no bitmapped graphics can be displayed." |
| P-VIDEO-WRITEONLY | Once a character is on the display it cannot be modified; it scrolls off or the display is cleared | OWAD ch. 7 p. 234 | "once a character is sent to the display, it cannot be modified. It's there until you enter enough lines that it scrolls off the top of the screen, or until you manually clear the entire display. In this way, the function of the video is very similar to a typewriter or Teletype." |
| P-PROPELLER | On the Replica I TE a Parallax Propeller handles video and keyboard and provides the serial interface | OWAD ch. 7 p. 234 sidebar | "a Parallax Propeller microcontroller now handles both. The Propeller also provides a serial interface. The video section of the Propeller sends data to both the video port and serial interface, while the keyboard section listens for data from both the keyboard and serial interface." Describes the Replica I TE. See V-4. |

## R. The replica as documented by its manual

| ID | Claim | Source | Wording |
|---|---|---|---|
| R-RESET | Power on shows a garbage screen; RESET gives a backslash and drops the cursor | BRIEL ch. 3 p. 11 | "a screen of garbage should appear ... Press RESET on the board and your replica will respond with a backslash '\' and the cursor will drop to the next line." |
| R-CURSOR | The cursor is a blinking `@` | BRIEL ch. 3 p. 11 | "The cursor is a blinking '@' symbol just like the original Apple 1 computer." |
| R-UPPER | Only upper-case characters are understood | BRIEL ch. 3 p. 11 | "The apple 1 only understands uppercase characters so does the replica 1." |
| R-KBD-PORTS | PS/2 or Apple II ASCII keyboard | BRIEL ch. 3 p. 11 | "You have two choices for keyboards; PS/2 PC style keyboard or an ASCII keyboard." |
| R-MON-3 | The Woz monitor has three basic functions: examine, program, run | BRIEL ch. 5 pp. 20 to 21 | "There are three basic functions to the Woz monitor." |
| R-MON-SYNTAX | `300[RETURN]` examines; `300.32F` examines a block; `300:FF` writes; `300R` runs | BRIEL ch. 5 pp. 20 to 21 | Worked examples in the chapter. |
| R-MON-8 | A block examine prints up to 8 locations per line | BRIEL ch. 5 p. 20 | "The replica will display the memory contents up to 8 locations per line" |
| R-ROM-SPLIT | 8 KB EEPROM: 4 KB BASIC, 256 bytes Woz monitor, just under 4 KB Krusader | BRIEL ch. 5 p. 22 | "The replica 1 has 8K of EEPROM (ROM) space onboard. 4K is used for BASIC; 256 bytes are used for the Woz monitor. This leaves just under 4K" |
| R-BASIC-ENTRY | `E000R` enters BASIC; prompt is `>` | BRIEL ch. 5 p. 21 | "type in: E000R [RETURN] ... The prompt for BASIC is '>'." |
| R-KRUSADER | `F000R` enters the Krusader assembler by Ken Wessen | BRIEL ch. 5 pp. 22, 26 | "To start Krusader, type in 'F000R'" |
| R-ROMSEL | A ROM select jumper switches to an Applesoft lite with prompt `]` | BRIEL ch. 5 p. 22 | "Place the jumper on the ROM select with the power switch in the off position ... the prompt is now a ']'." |
| R-SERIAL | 9600 baud, 8 data bits, one stop bit, no parity, no flow control | REPO `docs/reference/README.md` (summarizing BRIEL) | Recorded in the repository reference note. |

## W. The Woz Monitor listing

Source for all of these: BRIEL Appendix C, pp. 30 and following, which reprints
the Monitor listing with labels.

| ID | Claim | Wording |
|---|---|---|
| W-FF00 | `$FF00` is RESET, and it begins `CLD` | "FF00: D8 RESET CLD Clear decimal arithmetic mode." |
| W-FF1F | `$FF1F` is the label `GETLINE` | "FF1F: A9 8D GETLINE LDA #$8D CR." |
| W-FFEF | `$FFEF` is the label `ECHO`, called with `JSR` | "FF1C: 20 EF FF JSR ECHO Output it." |
| W-CR | Carriage return is `$8D` in Monitor terms, that is `$0D` with bit 7 set | "LDA #$8D CR." with P-HIGHBIT |
| W-RUNCMD | `R` runs a user program | "FF55: C9 D2 CMP #$D2 'R'? FF57: F0 3B BEQ RUN Yes. Run user program." |
| W-MODES | The Monitor tracks three modes: `$00` examine, `$7B` store, `$AE` block examine | "FF41: 85 2B SETMODE STA MODE $00=XAM $7B=STOR $AE=BLOK XAM" |

## A. ASCII, hex, and binary

| ID | Claim | Source | Wording |
|---|---|---|---|
| A-ASCII | ASCII assigns decimal 0 to 127; one byte per character | OWAD Appendix E p. 266 | "uses 1 byte to correspond to each of 128 different letters ... Only the decimal values 0 through 127 are assigned, which is half of the space available in a byte." |
| A-ASCII-1968 | Many control characters are holdovers from the 1968 specification | OWAD Appendix E p. 266 | "holdovers from the original specification created in 1968" |
| A-HEX | Two hex characters represent one byte; hex is prefixed `0x` or `$` | OWAD Appendix E p. 266 | "Two hex characters can represent 8 bits (a byte). ... Hex characters are sometimes prefixed with 0x or $" |
| A-TABLE | Decimal, binary, hex equivalence table | OWAD Appendix E p. 267 (Table E.1) | 0 to 15, then 16, 31, 32, 63, 127, 255. |
| A-CHART | Full ASCII chart with `CR` = 13 = `$0D`, space = 32 = `$20`, `A` = 65 = `$41` | OWAD Appendix A p. 237 and Appendix E p. 268 (Table E.2) | Reprinted chart. |

## B. Apple I BASIC

| ID | Claim | Source | Wording |
|---|---|---|---|
| B-INTEGER | Apple I BASIC supports integers only | OWAD ch. 5 p. 132 | "Apple I BASIC only supports integers; so, if you perform division, you'll get results like this: >PRINT 38/9 gives 4" |
| B-MOD | `MOD` gives the remainder | OWAD ch. 5 p. 132 | ">PRINT 38 MOD 9 gives 2" |
| B-VARNAMES | Integer variables are a letter or a letter and a digit; strings end in `$` | OWAD ch. 5 p. 130 | "An integer may be named with a letter or a letter and a digit (for example, A, N, A1, B8). A character string must be named with a letter and a dollar sign" |
| B-DIM | Strings must be dimensioned; maximum length 255 | OWAD ch. 5 p. 130 | "BASIC needs to be told how many bytes to allocate to a string ... The maximum string length is 255 characters (or bytes)." |
| B-INPUT-Q | `INPUT` always adds a question mark and it cannot be turned off | OWAD ch. 5 p. 131 | "A question mark is automatically inserted after each INPUT statement. Unfortunately, there is no way to turn it off." |
| B-COLON | A colon puts two statements on one line | OWAD ch. 5 p. 130 | "A colon ( : ) is used to place two instructions on the same line" |
| B-IMMEDIATE | Arithmetic works directly from the command line without a program | OWAD ch. 5 p. 131 | ">PRINT 8+3 gives 11" |

## E. Repository facts

| ID | Claim | Source |
|---|---|---|
| E-WIDTH | Display text is written to 40 columns of upper-case printable ASCII | REPO `docs/apple1-learning-library-curriculum.md` rule 4; `tools/apple1_text.py` default `width = 40` |
| E-SUBST | Unsupported characters become a visible `?`, never a silent drop | REPO `tools/apple1_text.py` docstring |
| E-RAMONLY | The `.hex` files are address-free byte lists for entry at the address in the filename | REPO `software/ram-only/README.md` |
| E-EXIT | Exit via `JMP $FF1F`, not `RTS`, because the Monitor's `R` leaves no return address on the stack | REPO `software/ram-only/README.md` |
| E-NOPROOF | A manual, a vendor source archive, or a display echo is not proof of installed firmware or serial transport | REPO `docs/preservation-dossier.md`; `docs/apple1-software-library.md`; `docs/reference/README.md` |
| E-STOP | On unexpected output, reset to the Monitor prompt, record `STOP`, and start nothing else | REPO `docs/apple1-software-library.md`; `docs/preservation-dossier.md` |
| E-FT232-STOP | Opening the FT232R from the host has already produced a display-garbling `STOP` result | REPO `docs/preservation-dossier.md`, "Current boundaries" |
| E-EMU-SCOPE | The repository emulator is ROM-free, models only the keyboard registers and Monitor ECHO and warm entry, and emulates no Propeller or serial hardware | REPO `tools/apple1_emulator.py` docstring |
| E-110REV03 | The vendor `110REV03` source is immutable candidate evidence, not the installed EEPROM image | REPO `docs/preservation-dossier.md` |

## Open verification items

- **V-1. Page numbers.** Taken from indexed PDF text, not a page-by-page read of
  the local collection copies. Confirm before any packet goes on the card.
- **V-2. Made versus sold.** H-MADE, H-SOLD, and H-BYTESHOP are three different
  counts of three different things. Lessons must not merge them into one number.
- **V-3. Reset vector typo.** OWAD p. 216 states `$FFFE` and `$FFFF` correctly in
  one sentence and then writes "$FFEF and $FFFF" in the next. The first is
  correct for the 6502. Lessons cite the concept, not the typo.
- **V-4. Which replica.** OWAD describes the Replica I and the Replica I TE.
  BRIEL documents the Replica 1 Plus. These are different products. A claim
  sourced to OWAD must not be stated as a fact about the Plus.
- **V-5. BASIC in ROM on the original.** H-BASIC-TAPE and M-BASIC-RAM together
  support "a 1976 Apple-1 did not have BASIC in ROM," but the inference is the
  author's. A citation from the Apple-1 Operation Manual would settle it.
- **V-6. Manual identity.** The knowledge base indexes
  `Replica_One_Plus_Manual__June_2014.pdf`; the collection folder holds
  `Replica_One_Plus_Manual_-_June_2014.pdf`. Presumed the same June 2014
  edition. No SHA-256 comparison has been run, which
  `docs/collection-archive.md` requires.
- **V-7. Display geometry.** The 40-column width used throughout this library
  comes from the repository's own rule and tooling, not from a cited Apple-1
  display specification. A line count per screen is nowhere cited and is not
  claimed by any lesson.
- **V-8. This machine.** Nothing in this pool describes the state of this
  project's board, its installed EEPROM, or its serial path.
