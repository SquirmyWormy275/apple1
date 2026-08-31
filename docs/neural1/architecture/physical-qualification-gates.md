# Physical qualification gates

The evaluator is pure data logic and cannot enumerate or open hardware. It
requires every gate: explicit supersession of the FT232R STOP, named-artifact
review, prepared Reset recovery, electrical measurement coverage, verified
exclusive output boundary, and recorded operator approval. Missing any gate
keeps serial open, transmit, firmware/EEPROM/CFFA1 writes, GPIO control, and
generated-program execution prohibited.

Current result is **NOT READY** because the STOP has not been superseded. This
software gate does not itself authorize a live action even when fields become
true; the controlling repository protocol and human approval still apply.
