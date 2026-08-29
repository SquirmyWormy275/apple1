# S04 Answer key

## Part A: the three

| # | Answer | Reasoning |
|---|---|---|
| a | **M** | Published documentation of the design. True of the specification. Not a reading taken from this board. Dumping this machine's ROM and comparing would move it to F. |
| b | **C** | Having the vendor source establishes that the source exists. It does not establish that it was compiled, installed, or is still present. The repository's preservation dossier says the vendor source is candidate evidence, not the installed image. |
| c | **F** | Someone performed an action and recorded the observed result. It has an actor, a time, and an outcome. |

Note how little (c) claims. It does not say what broke or why. Narrowness is
what makes it a fact.

## Part B: ten more

| # | Answer | Why |
|---|---|---|
| 1 | **M** | Two published sources state it. It is a historical record, well attested, but it is documentation rather than something this project observed. Accept F from a learner who argues that a price in a period source is an observation; ask them who observed it. |
| 2 | **C** | "Works" is not defined and nothing has established it. This is the single most important item on the sheet. |
| 3 | **M** | It is what the manual specifies. A measured capture at that rate would move it. |
| 4 | **F** | A run was performed and the result recorded in `../EMULATOR-RUNS.md`. |
| 5 | **C** | Different object entirely. #4 does not carry across to hardware. |
| 6 | **M** | Documented design. |
| 7 | **F** | A dated observation from a specific host, recorded in `docs/hardware/plus-io-map.md`. |
| 8 | **C** | And a false one. The repository notes the value is non-unique. A claim can be wrong as well as unestablished. |
| 9 | **M** | Documented history. Note the shared pool records three different counts of three different things: made, sold, and bought by the Byte Shop. |
| 10 | **C** | And almost certainly false. Not the same class of object at all. |

The pair to sit with is **#4 and #5**. They differ by one word and by an entire
evidence gate.

## Part C: the same sentence, three ways

One set of answers. Others are acceptable if the bins are honest.

- **Fact:** "On 27 August, after power-on, the screen showed the expected
  garbage pattern, and I photographed it."
- **Model:** "The manual states that on power-up the display shows random
  characters until RESET is pressed."
- **Claim:** "The display works."

Notice the original sentence is the claim version. Short confident sentences
tend to land in the C bin.

## Part D: find the smuggled model

1. Fact: the board powered on and showed the garbage screen. **Model: "which
   means the video circuitry is healthy."** A garbage screen shows something is
   driving the display, not that the circuitry is healthy.
2. Fact: the source archive hashes correctly. **Model: "so the firmware is
   intact."** The hash establishes the file is unchanged. It says nothing about
   what is on the chip.
3. Fact: RESET produced a backslash. **Model: "so the Monitor ROM is the stock
   one."** A backslash shows something responded like a monitor. Any compatible
   image would do the same.

## Part E: sample evidence card

> **Claim:** This board's EEPROM contains `110REV03`.
> **Current bin:** C.
> **What exists now:** A copy of the vendor `110REV03` source in the repository,
> retained unmodified.
> **What would move it one bin:** A read-back of the installed EEPROM compared
> byte for byte against a build of that source, with both hashed.
> **Who would have to do that:** The operator, in a separately approved session,
> using a procedure that does not yet exist in this repository.

The last line is the one people skip. A claim with no one assigned to test it
stays a claim indefinitely.

## README: Check your understanding

1. **Model.** It is a specification. A capture showing bytes arriving intact at
   9600 baud on this cable and this board would move it toward fact, and would
   still only be a fact about that capture.
2. **As narrowly as possible: the byte sequence, executed by that emulator, on
   that host, produced that output.** It establishes something about the
   program's logic. It establishes nothing about any physical machine.
3. **Because a hash establishes file identity, not correspondence.** It proves
   the manual has not changed since it was hashed. Whether the manual describes
   the board next to it is a separate question that no hash can answer.
