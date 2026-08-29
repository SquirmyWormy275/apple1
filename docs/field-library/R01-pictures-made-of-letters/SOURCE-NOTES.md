# R01 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key |
|---|---|
| The video section is text only; it stores a character's ASCII code rather than pixels | P-VIDEO-TEXT |
| Only characters present in the video ROM can be displayed; no bitmapped graphics | P-VIDEO-ROM |
| Once a character is sent to the display it cannot be modified; it leaves by scrolling off or by clearing the display | P-VIDEO-WRITEONLY |
| The machine understands upper case only; PS/2 caps lock is on by default | R-UPPER |
| Display material is 40 columns of upper-case printable ASCII | E-WIDTH |
| Unsupported characters become a visible `?` rather than being silently dropped | E-SUBST |
| The formatter wraps rather than truncates at the width | REPO `tools/apple1_text.py`, `_wrap_line` |

## The 40 columns

**The 40-column figure comes from this repository, not from a cited Apple-1
display specification.** It is the default `width` in `tools/apple1_text.py` and
the rule stated in the curriculum. This is recorded in the shared pool as
**V-7**, and R01 depends on it more heavily than any other lesson.

No claim is made anywhere in this packet about how many *rows* an Apple-1 display
shows. The grid offers 12 rows as a working area and the design challenge caps at
12, both chosen as convenient rather than derived from any source. A reader should
not infer a screen height from either.

## The craft advice is not sourced

The guidance about letter widths, gap sizes, three weights, and when to use two
lines is craft judgement written for this lesson. It is not attributable to any
source and carries no Apple-1-specific claim. It is offered as advice and the
answer key marks the subjective parts as subjective, notably the weight ranking
in Part D, where reasonable people will disagree about the middle.

## The formatter answers

Part E's answers were derived from reading `tools/apple1_text.py`: it
upper-cases each character, replaces anything outside the printable seven-bit
range with `?`, and wraps at the width rather than truncating. The three worked
banners and the grid were checked against the formatter during authoring and pass
unchanged.

## Deliberate simplifications

1. **Which characters the Apple-1's video ROM actually contains is not stated.**
   P-VIDEO-ROM establishes that the set is limited, not what is in it. The lesson
   restricts itself to printable seven-bit ASCII, which is the repository's rule,
   and does not claim that every such character would display.
2. **Scrolling behavior is mentioned but not specified.** The lesson says a
   character leaves by scrolling off the top, which P-VIDEO-WRITEONLY supports,
   without describing how scrolling is triggered or how fast it is.
3. **No timing claim is made** about how a banner would appear.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-7 applies strongly.** The 40-column canvas is a repository convention, not
  a cited display specification.
- **V-24 (new).** The set of characters the Apple-1 video ROM can display is not
  established by any source in this project. This lesson restricts itself to
  printable ASCII on the repository's rule and does not claim all of it would
  render.
- **V-4 applies** to R-UPPER, which is from the Replica 1 Plus manual.
- **V-8 applies.** No banner here has been displayed on any machine.

## What this lesson does not establish

Nothing about this project's display. It authorizes no firmware load, EEPROM
write, CFFA1 write, serial-port open, or physical modification.
