from tools.apple1_basic import ROM_SHA256, run_session
from tools.textbook_support import ROOT

session = ROOT / "software/basic/SORT.session"
result = run_session(session.read_text(encoding="ascii").splitlines())
print("Interpreter SHA-256:", ROM_SHA256)
print(result.transcript, end="")
print("Stop:", result.stop)
print("NMOS 6502 instructions:", result.instructions)
print(f"LOMEM=${result.lomem:04X}; HIMEM=${result.himem:04X}")
assert "COMPARISONS 16 SWAPS 7" in result.transcript
assert "***" not in result.transcript
assert result.stop == "waiting-for-input"

boundary = run_session(["DIM A(5)", "A(0)=1"])
print("One-based array boundary:")
print(boundary.transcript, end="")
assert "*** RANGE ERR" in boundary.transcript
