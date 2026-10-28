from tools.apple1_basic import ROM_SHA256, run_session
from tools.textbook_support import ROOT

session = ROOT / "software/basic/PATTERN.session"
result = run_session(session.read_text(encoding="ascii").splitlines())
print("Interpreter SHA-256:", ROM_SHA256)
print(result.transcript, end="")
print("Stop:", result.stop)
print("NMOS 6502 instructions:", result.instructions)
print(f"LOMEM=${result.lomem:04X}; HIMEM=${result.himem:04X}")
assert "******" in result.transcript
assert result.transcript.split(">RUN\n", 1)[1].split("\n\n>", 1)[0].splitlines() == ["*" * n for n in range(1, 7)]
assert result.stop == "waiting-for-input"
