from tools.apple1_basic import ROM_SHA256, run_session
from tools.textbook_support import ROOT

session = ROOT / "software/basic/HELLO.session"
result = run_session(session.read_text(encoding="ascii").splitlines())
print("Interpreter SHA-256:", ROM_SHA256)
print(result.transcript, end="")
print("Stop:", result.stop)
print("NMOS 6502 instructions:", result.instructions)
print(f"LOMEM=${result.lomem:04X}; HIMEM=${result.himem:04X}")
assert "HELLO TOM" in result.transcript
assert "***" not in result.transcript
assert result.stop == "waiting-for-input"

print("Prompt boundary: a supplied question mark plus INPUT's automatic one")
doubled = run_session(['10 DIM N$(20)', '20 INPUT "NAME?",N$', '30 PRINT N$', '40 END', 'RUN', 'TOM'])
print(doubled.transcript, end="")
assert "NAME??TOM" in doubled.transcript
