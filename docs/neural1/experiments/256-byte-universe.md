# 256-BYTE UNIVERSE

Candidates must be exactly 256 bytes and pass separately named functional
tests. Correctness, human usability, machine-agent usability, size, and recovery
are separate score families. During blinded generation the WozMon implementation
and bytes are excluded; agents receive only requirements such as inspect,
deposit, run, keyboard/display compatibility, and budget. WozMon comparison
occurs only after reveal. The 16x16 genome renderer maps byte ranges to stable
glyph classes and makes no semantic claim about function.

The bounded console starting task uses a 256-byte executable candidate at
0200–02FF. Its acceptance evaluator rejects CPU instruction fetches, reads and
writes outside that region, except the explicitly declared NMOS call-stack page
0100–01FF and read-only Monitor ECHO service at FFEF; FF1F is a stop sentinel.
It cannot expand code or data into the surrounding 4K world to pass. These
external architectural resources are recorded in the result; the preset does
not claim that the entire machine, stack and Monitor services occupy 256 bytes.
