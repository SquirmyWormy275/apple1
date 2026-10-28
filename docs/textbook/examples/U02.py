from tools.apple1_basic import ROM_SHA256, run_session
from tools.textbook_support import ROOT

session = ROOT / "software/basic/CONVERT.session"
result = run_session(session.read_text(encoding="ascii").splitlines())
print("Interpreter SHA-256:", ROM_SHA256)
print(result.transcript, end="")
print("Stop:", result.stop)
print("NMOS 6502 instructions:", result.instructions)
print(f"LOMEM=${result.lomem:04X}; HIMEM=${result.himem:04X}")
assert "5 INCHES IS 12 CM" in result.transcript
assert "***" not in result.transcript
assert result.stop == "waiting-for-input"

program = (ROOT / "software/basic/CONVERT.bas").read_text().splitlines()
for value in ("0", "129", "130", "-1"):
    boundary = run_session([*program, "RUN", value])
    print("Input boundary:", value)
    print(boundary.transcript.split(">RUN\n", 1)[1], end="")
    assert "***" not in boundary.transcript
overflow = run_session(["PRINT 130*254/100"])
print("Unguarded intermediate overflow:")
print(overflow.transcript, end="")
assert "*** >32767 ERR" in overflow.transcript
