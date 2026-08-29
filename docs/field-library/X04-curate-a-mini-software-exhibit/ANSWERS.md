# X04 Answer key

Curation has no single right answer. Below is a worked set and the criteria for
judging a learner's.

## Worked set

**Chosen: artifacts 1, 4, and 5.** The byte list, the vendor source archive, and
the recorded emulator runs.

**Why these three:** together they make one argument, that software evidence and
hardware evidence are different things. Artifact 1 is a program someone wrote.
Artifact 5 shows it behaving correctly in a model. Artifact 4 is the thing that
looks like it should close the loop and does not.

### Card for artifact 1

| Field | Content |
|---|---|
| 1. Title | Twenty-six bytes that read a line of typing |
| 2. What it is | A hand-entered 6502 program that collects typed characters into memory, echoes each one, and returns to the Monitor. |
| 3. Why it is here | It is the smallest complete useful program in the collection: input, storage, output, and a clean exit in 26 bytes. |
| 4. Where it came from | Retained from confirmed learning exercises recorded in the project handover. |
| 5. Who made it, who says so | Not recorded. The repository describes it as retained from the handover and does not name an author. |
| 6. Rights | Not recorded. Origin within the project handover; whether it derives from published material is unknown. Would need to ask whoever compiled the handover. |
| 7. Status | RAM-ONLY, no live-run authority. |
| 8. What it shows | That a useful interactive program fits in 26 bytes. |
| 9. **What it does not prove** | That this program has ever run on this project's board, that the board can read a keypress, or that the Monitor routine it calls is present on that machine. |

### Card for artifact 4

| Field | Content |
|---|---|
| 1. Title | The firmware source that may or may not be what is installed |
| 2. What it is | A vendor source archive for the `110REV03` Propeller firmware, retained unmodified. |
| 3. Why it is here | Because it is the artifact most likely to be mistaken for proof of something it does not prove. |
| 4. Where it came from | The vendor. Exact retrieval route and date not recorded in this library. |
| 5. Who made it, who says so | The vendor, per the archive itself. |
| 6. Rights | **Unresolved.** It is somebody's source code. Whether it may be displayed or copied is not recorded anywhere in this project and would need the vendor's terms. |
| 7. Status | OFF-DEVICE as an object to read. Any use beyond reading is red. |
| 8. What it shows | What one candidate firmware version's source contains. |
| 9. **What it does not prove** | That it was compiled, that a build of it was installed, or that it is what is on this board's EEPROM now. The repository classifies it as candidate evidence, not the installed image. |

### Card for artifact 5

| Field | Content |
|---|---|
| 1. Title | Nine runs that prove nothing about the machine |
| 2. What it is | Recorded executions of the repository's byte lists in a ROM-free software harness, with their inputs and outputs. |
| 3. Why it is here | To show what software evidence looks like, and exactly where it stops. |
| 4. Where it came from | Produced during authoring of this library, on an ordinary computer. |
| 5. Who made it, who says so | This library, recorded in `../EMULATOR-RUNS.md` with the harness named. |
| 6. Rights | The repository's own material. |
| 7. Status | OFF-DEVICE. |
| 8. What it shows | That the byte sequences behave as described, reproducibly. |
| 9. **What it does not prove** | Anything about hardware. The harness emulates no Propeller, no serial hardware, and no ROM image. A successful run does not waive a hardware evidence gate. |

**The set's argument:** three artifacts, and the one in the middle is the trap. A
visitor who reads all three cards should come away understanding why the project
still does not know what is on its own EEPROM.

## Acceptance criteria

**Part A.** Three artifacts, each with a distinct reason. Two that do the same job
is a fault.

**Part B.** All nine fields on all three cards. Field 9 filled on every card. Any
card missing field 9 is unfinished, as the template says.

**Part C.** The difference between a bad and a good title is usually accuracy plus
one interesting fact. "Apple-1 program" is bad twice: it is inaccurate, since
these are replica-era artifacts, and it is dull.

**Part D.** **No blank cells.** A cell the learner cannot fill must say what they
would find out and from whom. This is the field most often left blank and the
exercise refuses to allow it.

**Part E.** Eight entries. See below.

**Part F.** A stated argument, and identification of the complicating artifact. A
set where all three agree is weaker and the learner should say what they would
add.

**Part G.** A plausible wrong conclusion for each, and an honest answer about
whether the card prevents it. "Yes" for all three is usually optimistic.

## Part E: field 9 for all eight

| # | Does not prove |
|---|---|
| 1 | That it has run on this board, or that the board reads a keypress. |
| 2 | The same, and note it does not return to the Monitor on its own. |
| 3 | That this listing matches the ROM installed on this board. It is a manual's reprint of a documented design. |
| 4 | That it was compiled, installed, or is present now. Candidate evidence only. |
| 5 | Anything about hardware. |
| 6 | That the manual describes this board, or that this scan matches the vendor's original. The project also holds an unresolved filename discrepancy for this manual. |
| 7 | That its descriptions apply to the Replica 1 Plus. It documents the original Apple-1 and the earlier Replica I and Replica I TE. |
| 8 | That any lesson has been reviewed against the curriculum's review gate, or that its cited page numbers have been checked against the local copies. |

Item 8 is the uncomfortable one, and it belongs on the list. This library's own
lessons carry unverified page numbers and unclosed verification items, recorded in
their source notes. An exhibit that included them without field 9 would be doing
exactly what the field exists to prevent.

## Part H: the missing artifact

The obvious answer: **a read-back of this board's installed EEPROM**, hashed and
compared against a build of the vendor source.

**What would have to happen:** a procedure that does not currently exist, an
operator decision, and an approval this project has not granted. EEPROM action is
excluded from ordinary development work.

**Is anyone permitted to make it?** Not under any document this library has seen.
That is the honest answer, and it is why artifact 4's card says what it says.

## Try a variation: field 9 first

Writing field 9 first tends to change the selection. Artifacts whose limits are
hard to state clearly are usually artifacts you have not thought about carefully,
and artifacts whose "does not prove" is long and specific tend to be the
interesting ones.

## README: Check your understanding

1. **Because three is enough to make a point and few enough that each must earn
   its place.** Five becomes a survey, and in a survey a weak item hides.
2. **It answers field 4, where it came from, and only partially.** It does **not**
   answer field 6, rights and permission. A location is not a permission, and
   conflating them is how material ends up displayed without anyone having asked.
3. **Because an exhibit that shows a program without saying whether anyone may
   run it answers the question by omission, and answers it wrongly.** A visitor
   reasonably assumes that something on display can be demonstrated. The label is
   where you say otherwise.
