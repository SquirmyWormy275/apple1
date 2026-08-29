# H03 Status

**Mode: OFF-DEVICE**

No runnable artifact. Record-keeping on paper.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/evidence-card.txt` | Ten-field record card, 40 columns | No |

No hashing tool is invoked by any step of this lesson and no file in the project
is modified. The learner fills in a card by hand.

## Expected result

One filled evidence card including field 10. Part B has determinate answers:
three of seven questions are answerable by a hash, and all three are identity
questions. Parts D, F, and G are keyed.

The intended insight in Part D is that the tidier of the two cards is the less
truthful one.

## Known limitations

- **Card fields 9 and 10 are this library's addition** to the repository's
  documented record requirements, not existing project practice (V-30).
- How SHA-256 works is not explained, and no claim is made about its
  cryptographic properties beyond the identity property the repository already
  relies on.
- Manifest self-integrity remains unaddressed, here as in B05 (V-23).
- The worked example, the manual filename discrepancy, is left unresolved (V-6).

## Stop condition

Not applicable. No device interaction, no file modification, no tool invocation.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification.

**This packet authenticates nothing.** It makes no claim about the originality,
condition, or value of any object, and it resolves none of this project's open
provenance items.
