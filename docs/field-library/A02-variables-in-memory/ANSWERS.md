# A02 Answer key

## Part A: the before-and-after table

| After | A | `$0400` | `$0401` |
|---|---|---|---|
| Start | `?` | `?` | `?` |
| `0300` `LDA #$48` | `$48` | `?` | `?` |
| `0302` `STA $0400` | `$48` | `$48` | `?` |
| `0305` `LDA #$49` | `$49` | `$48` | `?` |
| `0307` `STA $0401` | `$49` | `$48` | `$49` |
| `030A` `JMP $FF1F` | `$49` | `$48` | `$49` |

`$48` is `H` and `$49` is `I`, so the program writes `HI` into the buffer.

Note that `$0401` stays unknown until something writes to it. A learner who put
`$00` there has invented a fact, exactly as in C05.

## Part B: the indexed version

| After | A | Y | `$0400` | `$0401` |
|---|---|---|---|---|
| `0304` `STA $0400,Y` | `$48` | `$00` | `$48` | `?` |
| `0307` `INY` | `$48` | `$01` | `$48` | `?` |
| `030A` `STA $0400,Y` | `$49` | `$01` | `$48` | `$49` |

**Same final memory state as Part A.** Both leave `$48` at `$0400` and `$49` at
`$0401`. The difference is that the second version used one store instruction
twice rather than two different store instructions, and the second version would
extend to a hundred values without gaining a single new instruction.

## Part C: what does it write where

| Instruction | Y | Address |
|---|---:|---|
| `STA $0400,Y` | 0 | `$0400` |
| `STA $0400,Y` | 1 | `$0401` |
| `STA $0400,Y` | 16 | `$0410` |
| `STA $0400,Y` | 255 | `$04FF` |
| `STA $0500,Y` | 3 | `$0503` |

## Part D: label or address

| # | Item | Which |
|---|---|---|
| 1 | `$FF1F` | Address |
| 2 | `GETLINE` | Label |
| 3 | `$0400` | Address |
| 4 | `ECHO` | Label |
| 5 | `NOTCR` | Label |

**Addresses appear in the bytes. Labels do not.** `JMP $FF1F` assembles to
`4C 1F FF`, and the `1F FF` is the address. Nothing anywhere in the byte list
spells `GETLINE`. Delete every label from a listing and the program is
unchanged; delete an address and it is broken.

## Part E: read it back

One correct answer:

```text
0300  A9 5A     LDA #$5A      ; 'Z'
0302  8D 02 04  STA $0402
0305  AE 02 04  LDX $0402
0308  4C 1F FF  JMP $FF1F
```

Trace: A becomes `$5A`; `$0402` becomes `$5A`; X becomes `$5A`; control leaves.
Three places hold `$5A` at the end.

Accept an indexed version, or one using `LDY`/`STY`. Reject anything using
`STA #`.

## Part F: the collision

1. **`$0300` to `$0319`.** 26 bytes from `$0300`.
2. **`$0310` is inside the program.** Writing a buffer there overwrites the
   program's own instructions while it is running.
3. **Almost anything.** The program might work for a few characters and then
   behave strangely, or jump somewhere meaningless, or stop responding, because
   the bytes it is about to execute have been replaced with text. The symptom
   would look nothing like "the buffer is in the wrong place," which is what
   makes this class of bug expensive.
4. **Two safe choices, with reasons:** `$0400`, which is a full 256 bytes past
   the start and comfortably clear of a 26-byte program; or `$0320`, which is
   just past the program's last byte at `$0319` and is safe *for this program at
   this length*. The first is safer because it survives the program growing.

## Part G: count the instructions saved

Without indexing, ten values need ten `LDA #` and ten `STA` with ten different
addresses: **20 instructions**, and every address written out by hand.

With indexing, ten values need `LDY #$00` once, then ten `LDA #` and ten
`STA $0400,Y` and nine or ten `INY`: **around 30 instructions** for a
straight-line version, which is *worse*.

This is the honest answer and it is the point of the exercise. Indexing does not
pay off for a fixed list written out longhand. It pays off when the values come
from somewhere else and the code becomes a **loop**: read, store, increment,
repeat, which is four or five instructions total regardless of how many values
arrive.

A learner who notices that straight-line indexing is worse has understood
something real. A03 supplies the missing half.

## Try a variation

Y holds one byte, so its highest value is 255, and the highest address reachable
is `$0400` plus 255 = **`$04FF`**.

The next `INY` wraps Y to `$00`, so the following store goes back to `$0400` and
overwrites the first character. Nothing warns you. This is why a program that
collects input needs to decide what happens when the buffer is full, and why the
repository's own firmware behavior model treats a full queue as a recorded stop
rather than a silent discard.

## README: Check your understanding

1. **It stores A into `$0405`.** Base `$0400` plus index 5.
2. **Because it would reset the position on every pass**, so every character
   would be written to `$0400` and each would overwrite the last. Initialization
   belongs where it happens once.
3. **An instruction byte.** `LOOP` is a name in the listing and occupies no
   memory. What is at `$0302` is whatever opcode that line assembles to.
