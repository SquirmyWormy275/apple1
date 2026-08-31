# Apple-1 Field Library curriculum scaffold

This is the content map for an educational library intended for archival
storage on the project CF card. It is a writing brief, not a card image,
installer, or authorization to operate the Replica 1 Plus.

Each finished lesson should be useful in at least one off-device setting:

- **Read**: a short plain-text lesson for a visitor or learner.
- **Try**: a paper, whiteboard, or terminal exercise with a visible result.
- **Rehearse**: an optional run in the constrained emulator.
- **Live**: reserved for a separately approved, operator-led RAM-only session.

The fourth mode is deliberately not part of the default lesson path. Do not
equate an emulator result, a screen echo, or a file stored on the CF card with
proof that hardware, serial transport, or firmware is working.

## Library design rules

1. Make one claim at a time and distinguish historical fact, a model, and a
   hands-on exercise.
2. Put a visible result within the first three learner actions.
3. Keep source, expected result, and a plain-language explanation together.
4. Use upper-case printable ASCII for material intended for the Apple-1-sized
   display. Format host-generated display text with `format_for_apple1`.
5. Mark every runnable artifact `OFF-DEVICE`, `RAM-ONLY`, or `LIVE BY
   SEPARATE APPROVAL`.
6. Do not include firmware loading, EEPROM writing, CFFA1 modification,
   serial-port opening, or automated physical-device control in a lesson.

## Audience and session labels

| Label | Reader | Target time | What success looks like |
|---|---|---:|---|
| LOOK | Museum visitor or first-time learner | 5–10 min | Explains one idea in their own words |
| LEARN | Curious beginner | 20–40 min | Completes a guided exercise |
| BUILD | Beginner programmer | 45–90 min | Produces or changes a program in rehearsal |
| STUDY | Historian, educator, or advanced learner | 30–60 min | Compares evidence or explains a trade-off |

## Suggested card-facing menu

```text
APPLE-1 FIELD LIBRARY

1  START HERE
2  INSIDE A COMPUTER
3  THE WOZ MONITOR
4  6502 PROGRAMMING
5  BASIC AND ALGORITHMS
6  CREATIVE COMPUTING
7  HISTORY AND PRESERVATION
8  CHALLENGES AND PROJECTS
9  TEACHER AND AUTHOR NOTES
```

The actual card boot/menu mechanism is intentionally undecided. This outline
defines the educational catalog only.

## Lesson sequence

### 1. Start here

| ID | Working title | Level | Learner outcome | First visible result | Claude writing brief |
|---|---|---|---|---|---|
| S01 | What is an Apple-1? | LOOK | Separates a computer board, a monitor program, and a modern replica. | A three-part labeled diagram. | Tell the Apple-1 story without calling the Replica 1 Plus an original Apple-1. |
| S02 | A computer is not magic | LOOK | Describes input, processing, memory, and output. | Traces a key press to a displayed character in a conceptual diagram. | Use a friendly analogy, then replace it with the real technical terms. |
| S03 | Your first hex number | LEARN | Converts a small decimal number to hexadecimal. | Completes a 0–15 decimal/hex table. | Explain why programmers use base 16, with no assumed math background. |
| S04 | Facts, models, and evidence | STUDY | Knows why a manual or source archive is not proof of installed firmware. | Sorts three statements into fact, model, or claim needing evidence. | Connect careful computing to collectible preservation in plain language. |

### 2. Inside a computer

| ID | Working title | Level | Learner outcome | First visible result | Claude writing brief |
|---|---|---|---|---|---|
| C01 | The 6502 at work | LEARN | Names the CPU's job and the role of an instruction. | Decodes a simple `LDA` idea in English. | Avoid a full opcode table; teach fetch, decide, act. |
| C02 | Memory is a map | LEARN | Reads an address and explains a byte. | Locates `$0300`, `$0400`, and a conceptual display/keyboard area on a map. | State that the map is a learning model unless tied to cited machine documentation. |
| C03 | Binary, bits, and bytes | LEARN | Connects a binary pattern to one byte. | Builds an 8-bit value with a paper bit strip. | Include a short check-your-work answer. |
| C04 | Characters become numbers | LEARN | Explains character encoding and high-bit keyboard conventions. | Converts a typed `A` through a simple character example. | Keep any Apple-1-specific behavior accurately sourced and distinguish emulator conventions. |
| C05 | Instructions change state | BUILD | Predicts the effect of load, store, add, and branch. | Runs a four-instruction state trace on paper. | Use registers and memory cells as a compact worksheet, then supply an answer key. |

### 3. The Woz Monitor and debugging

| ID | Working title | Level | Learner outcome | First visible result | Claude writing brief |
|---|---|---|---|---|---|
| M01 | Meet the Monitor | LOOK | Explains what a monitor program is for. | Labels inspect, change, and run as three monitor jobs. | Present the monitor as a tiny toolset, not an operating system. |
| M02 | Addresses and byte entry | LEARN | Reads a hypothetical byte listing without entering it on hardware. | Marks the address and first three bytes in a sample listing. | Use a clearly fictional or emulator-only example unless a cited program is used. |
| M03 | A safe rehearsal loop | BUILD | Uses the repository emulator to rehearse a RAM-only program. | Obtains a reproducible emulator result. | Link to the emulator guide; state that it does not validate live hardware. |
| M04 | Debugging as observation | LEARN | Uses expected versus actual output to form one testable hypothesis. | Fills in a two-column observation sheet. | Teach "change one thing" and include an explicit STOP example. |
| M05 | Why `JMP $FF1F` matters | BUILD | Understands why the supplied programs return to Monitor warm entry. | Identifies the safe exit in a provided byte/source annotation. | Base the explanation on the existing RAM-only README; do not substitute `RTS`. |

### 4. Learn 6502 programming

| ID | Working title | Level | Learner outcome | First visible result | Claude writing brief |
|---|---|---|---|---|---|
| A01 | Read an instruction | LEARN | Reads mnemonic, operand, and intent. | Translates three instructions into English. | Start with immediate and absolute addressing only. |
| A02 | Variables in memory | BUILD | Stores and retrieves a value at a named address. | Completes a memory-before/memory-after table. | Explain the difference between a source label and a numeric address. |
| A03 | Counting and looping | BUILD | Predicts a loop and its stopping condition. | Traces a countdown. | Include one deliberate off-by-one puzzle. |
| A04 | Decisions and branches | BUILD | Uses a comparison to choose a path. | Solves a choose-the-message exercise. | Explain flags only as far as the lesson needs. |
| A05 | Keyboard to screen | BUILD | Explains the existing line-input program at a high level. | Annotates the input, store, echo, and return stages. | Use `line-input-0300.hex` only as RAM-only/emulator material. |
| A06 | Design a tiny utility | BUILD | Plans a useful one-purpose program before writing bytes. | Produces a one-page program design card. | Prompt for purpose, inputs, outputs, memory, exit, and test cases. |

### 5. BASIC, algorithms, and data

| ID | Working title | Level | Learner outcome | First visible result | Claude writing brief |
|---|---|---|---|---|---|
| B01 | From instructions to BASIC | LEARN | Contrasts assembly and BASIC without ranking them. | Matches a task to the more convenient language. | Use small pseudocode snippets if a runnable BASIC environment is not packaged. |
| B02 | Variables, input, and output | LEARN | Models a small calculator or quiz. | Completes a program flow diagram. | Keep the first program to one input and one result. |
| B03 | Algorithms: recipes for information | LEARN | Defines an algorithm and finds an ambiguity. | Rewrites an ambiguous sandwich or sorting recipe. | Tie the activity back to exact computer instructions. |
| B04 | Sorting by hand | LEARN | Explains why sorting takes repeated comparisons. | Sorts five cards with a trace sheet. | Introduce efficiency intuitively, not with asymptotic notation. |
| B05 | Data, files, and the CF card | STUDY | Distinguishes stored content, executable code, and a backup. | Classifies example files by purpose. | Do not assume a particular CFFA1 file system or boot workflow. |

### 6. Creative computing

| ID | Working title | Level | Learner outcome | First visible result | Claude writing brief |
|---|---|---|---|---|---|
| R01 | Pictures made of letters | LOOK | Makes a small ASCII picture within a fixed width. | Draws a 40-column banner. | Provide a printable 40-column grid and a design challenge. |
| R02 | Motion is many pictures | LEARN | Explains animation as a sequence of frames. | Designs three frames of a bouncing symbol. | Discuss timing conceptually; do not claim live timing behavior. |
| R03 | Generative patterns | BUILD | Uses a rule to create a text pattern. | Produces a number or character pattern. | Offer a pencil version and an optional host/emulator extension. |
| R04 | Interactive fiction | BUILD | Designs a room, choices, and state. | Writes a branching story map. | Make the learner's own world the focus, with a small test transcript. |
| R05 | Sound, rhythm, and code | STUDY | Explains how a program can represent timing and patterns. | Claps or plots a simple encoded rhythm. | Keep it conceptual unless a verified, compatible sound artifact is added later. |

### 7. History, preservation, and responsible computing

| ID | Working title | Level | Learner outcome | First visible result | Claude writing brief |
|---|---|---|---|---|---|
| H01 | The 1976 personal-computing moment | LOOK | Places the Apple-1 in a short timeline. | Orders five landmark events. | Cite primary or reputable historical sources for all dates and claims. |
| H02 | Original, replica, and reproduction | STUDY | Uses precise words for historically different objects. | Labels three hypothetical artifacts. | Be respectful of collectors; do not make authentication claims. |
| H03 | Why provenance matters | STUDY | Explains what a checksum and a source record can establish. | Creates a sample evidence-card entry. | Link to the collection-archive manifest and distinguish identity from authenticity. |
| H04 | Safe experimentation | LEARN | Identifies which actions are off-device, RAM-only, or approval-gated. | Completes a green/amber/red decision card. | Reuse the repository's safety boundaries exactly; no live procedure. |
| H05 | The future history you are making | LOOK | Treats notes, photos, and software versions as future historical material. | Writes a one-paragraph collection log entry. | End warmly: a careful hobbyist can be a good archivist. |
| H06 | The monitor that wasn't | STUDY | Separates Apple's 1976 display documentation from the VM-4209's later Apple-1 collector association. | Classifies three monitor claims as fact, later association, or unverified. | Use the display-history evidence ledger; teach how a later iconic pairing can be historically real without being an original factory bundle. |

### 8. Challenges and capstones

| ID | Working title | Level | Learner outcome | Evidence of completion | Claude writing brief |
|---|---|---|---|---|---|
| X01 | Hex scavenger hunt | LEARN | Finds and interprets values in a provided memory map. | Completed answer sheet. | Include hints and a separate answer page. |
| X02 | Fix the loop | BUILD | Corrects a small paper/emulator-only loop bug. | Before/after trace and explanation. | Make exactly one bug intentional. |
| X03 | Build a museum demo | BUILD | Combines a concept, demonstration, and explanation for a visitor. | Three-minute demonstration script. | Require an off-device fallback so it never depends on live hardware. |
| X04 | Curate a mini software exhibit | STUDY | Chooses, describes, and credits three artifacts. | Exhibit card set with sources. | Include rights/provenance prompts and a "what this does not prove" field. |
| X05 | Invent the next lesson | BUILD | Proposes an accurate, safe addition to the library. | Filled curriculum-author card. | Require learning objective, first result, sources, status label, and answer key plan. |

## Required lesson packet

Claude should create one folder or linked packet per finished lesson containing:

```text
NN-title/
  README.md              # learner-facing lesson
  ACTIVITY.md            # worksheet, puzzle, or rehearsal instructions
  ANSWERS.md             # educator/learner answer key
  SOURCE-NOTES.md        # citations and historical/technical claim notes
  assets/                # diagrams, plain-text samples, or verified programs
  STATUS.md              # OFF-DEVICE / RAM-ONLY / LIVE BY SEPARATE APPROVAL
```

If a lesson has no runnable artifact, say so directly. If it does, its status
file must name the exact file, expected result, known limitations, and the
recovery/stop condition that applies.

## Authoring template for Claude

Use this outline verbatim for each lesson. Fill every bracketed field before
marking the lesson ready for review.

```markdown
# [ID] [Lesson title]

**Audience:** [LOOK / LEARN / BUILD / STUDY]
**Time:** [minutes]
**Status:** [OFF-DEVICE / RAM-ONLY / LIVE BY SEPARATE APPROVAL]
**Prerequisites:** [none or named lesson IDs]

## You will learn

By the end, you can [observable learner action].

## Why this matters

[Two or three plain-language sentences.]

## First result

[The visible result reached in three learner actions or fewer.]

## What you need

[Paper, a browser, the repository emulator, or other explicitly safe tools.]

## Activity

1. [Action]
2. [Action]
3. [Visible result]

## Explain what happened

[Accurate explanation, with new terms defined on first use.]

## Try a variation

[One bounded extension activity.]

## Check your understanding

1. [Question]
2. [Question]
3. [Question]

## Answer key

[Answers or link to ANSWERS.md.]

## Sources and boundaries

- [Source for each Apple-1-specific or historical claim.]
- [What this lesson does not prove or authorize.]
```

## Claude writing handoff

Use the following prompt when starting a content-writing pass. Write lesson
packets only; do not modify firmware, open serial hardware, create a CF image,
or claim that an off-device result proves the live Replica 1 Plus works.

```text
Read docs/apple1-learning-library-curriculum.md, docs/apple1-software-library.md,
docs/emulator-demo-guide.md, docs/preservation-dossier.md, and
software/ram-only/README.md before writing.

You are creating learner-facing content for the Apple-1 Field Library. Start
with the requested lesson ID or the next unfinished lesson in the curriculum.
Create the required lesson packet (README.md, ACTIVITY.md, ANSWERS.md,
SOURCE-NOTES.md, assets/, and STATUS.md) and follow the authoring template
exactly.

Use only sourced historical and Apple-1-specific claims. Make the first visible
result happen in three learner actions or fewer. Give every question an answer
key. Label runnable material OFF-DEVICE or RAM-ONLY unless a separate written
approval explicitly authorizes a live session. An emulator result, display
echo, manual, or candidate firmware source does not prove live hardware,
serial, or installed-firmware behavior.

Do not create a firmware load, EEPROM write, CFFA1 write, serial-port action,
or physical procedure. At the end, report the files created, sources used,
claims that still need verification, and the exact checks you ran.
```

## Review gate before adding a lesson to the card catalog

- [ ] Every technical and historical claim has a source note.
- [ ] The first visible result arrives in three actions or fewer.
- [ ] The stated mode matches the actual artifact.
- [ ] A learner can finish without opening a physical serial port or changing hardware.
- [ ] Any program has a deterministic expected result and an answer key.
- [ ] Unsupported display characters and line-width assumptions are handled deliberately.
- [ ] The lesson says what it does **not** establish about the live machine.

## Repository links

- [Field Library lesson packets](field-library/README.md) - the written lessons,
  with a catalog index and the register of open verification items
- [RAM-only software library](apple1-software-library.md)
- [Emulator and demo preparation](emulator-demo-guide.md)
- [Collection archive manifest](collection-archive.md)
- [Preservation dossier](preservation-dossier.md)
