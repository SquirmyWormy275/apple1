from tools.apple1_basic import ROM_SHA256, run_session
from tools.textbook_support import ROOT

session = ROOT / "software/basic/QUIZ.session"
result = run_session(session.read_text(encoding="ascii").splitlines())
print("Interpreter SHA-256:", ROM_SHA256)
print(result.transcript, end="")
print("Stop:", result.stop)
print("NMOS 6502 instructions:", result.instructions)
print(f"LOMEM=${result.lomem:04X}; HIMEM=${result.himem:04X}")
assert "CORRECT: 42" in result.transcript
assert "***" not in result.transcript
assert result.stop == "waiting-for-input"

source = (ROOT / "software/basic/QUIZ.bas").read_text().splitlines()
wrong = run_session([*source, "RUN", "41"])
print("Nonmatching answer:")
print(wrong.transcript.split(">RUN\n", 1)[1], end="")
assert "TRY AGAIN: 2*16+10" in wrong.transcript
