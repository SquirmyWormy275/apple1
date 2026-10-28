; RAM-only paged reader, NMOS 6502, load/run at $1000.
; FIRST_LO/FIRST_HI are supplied by tools.build_cf_library.
; Page record: previous pointer, next pointer, NUL-terminated display bytes.
; Uses $F8-$FB, the normal stack, keyboard registers and Monitor ECHO only.
; No CFFA API calls, disk writes, ROM writes, or serial operations.
START:
    CLD
    LDA #FIRST_LO
    STA $F8
    LDA #FIRST_HI
    STA $F9
SHOW:
    CLC
    LDA $F8
    ADC #$04
    STA $FA
    LDA $F9
    ADC #$00
    STA $FB
PRINT:
    LDY #$00
    LDA ($FA),Y
    BEQ WAIT
    ORA #$80
    JSR $FFEF
    INC $FA
    BNE PRINT
    INC $FB
    JMP PRINT
WAIT:
    LDA $D011
    BPL WAIT
    LDA $D010
    AND #$7F
    CMP #$51
    BEQ QUIT
    CMP #$42
    BEQ BACK
    LDY #$02
    JMP SELECT
BACK:
    LDY #$00
SELECT:
    LDA ($F8),Y
    TAX
    INY
    LDA ($F8),Y
    STA $F9
    STX $F8
    LDA $F8
    ORA $F9
    BEQ QUIT
    JMP SHOW
QUIT:
    JMP $FF1F
