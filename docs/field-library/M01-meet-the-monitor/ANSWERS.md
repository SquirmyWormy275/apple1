# M01 Answer key

## Part A: name them

| # | Job | Example |
|---|---|---|
| 1 | Inspect: show what is at an address | `300` |
| 2 | Change: write a value to an address | `300: FF` |
| 3 | Run: start executing at an address | `300R` |

Accept "examine," "look," "read" for 1; "write," "poke," "set" for 2; "start,"
"execute," "go" for 3.

## Part B: read the command

| Typed | Job | Meaning |
|---|---|---|
| `300` | Inspect | Show the single byte at `$0300`. |
| `300.32F` | Inspect | Show the block from `$0300` to `$032F`, up to eight per line. |
| `300: FF` | Change | Write `$FF` at `$0300`. |
| `300: FF EE DD` | Change | Write `$FF`, `$EE`, `$DD` into `$0300`, `$0301`, `$0302`. |
| `300R` | Run | Jump to `$0300` and execute. |
| `E000R` | Run | Jump to `$E000`. On a replica with BASIC in ROM there, this enters BASIC. |

The last row is worth noting: `E000R` is not a special "start BASIC" command. It
is the ordinary run command aimed at the address BASIC happens to live at.

## Part C: the response that looks wrong

1. **They asked to write `$FF` into `$0300`.**
2. **`E1` is the value that was at `$0300` before the write.** It is the old
   contents, reported once.
3. **Because it looks like the machine is telling them the location still holds
   `E1`,** or refusing the change.
4. **Inspect it.** Type `300` and read what comes back. If it shows `FF`, the
   write worked. This is the three jobs doing exactly what they are for:
   inspect, change, inspect again.

## Part D: is it an operating system?

| Capability | Monitor? |
|---|---|
| Show the contents of an address | **Yes** |
| List what programs are stored | No |
| Stop a running program | No |
| Change a byte | **Yes** |
| Undo a change | No |
| Start a program at an address | **Yes** |
| Manage files | No |
| Tell you how much memory is free | No |

Three yeses out of eight, and the three are exactly the three jobs.

## Part E: the handover

A program must return control deliberately, because nothing will do it for them.
If a program runs off the end of its own instructions, the CPU does not notice
or stop. It carries on fetching whatever bytes come next and executing them as
instructions, which will be leftover data or unwritten memory. The behavior from
that point is undefined and the usual outcome is that the machine stops
responding and has to be reset.

This is why the programs in this repository end with an explicit jump back to
the Monitor.

## Part F: the tweezers question

No single right answer. Good ones capture that the Monitor is small, direct,
requires skill, and offers no protection: a scalpel, a pair of pliers on a live
circuit, a manual gearbox, a debugger with the program removed.

The thing tweezers misses is the **run** verb. Tweezers only manipulate; the
Monitor can also hand over control and step out of the way. An analogy that
captures inspect and change but not run is only two thirds right.

## README: Check your understanding

1. **Inspect, change, run.**
2. **Because it is not running once it has jumped.** "Run" transfers control
   permanently; the Monitor is not a supervisor sitting alongside the program,
   it is a program that stopped so another one could start.
3. **Any one of:** it manages no resources; it has no concept of a file; it
   cannot list, stop, or schedule anything; it provides no services to a running
   program. It is a small utility for reading and writing memory, and the
   comparison sets the wrong expectations about what it will do for you.
