from tools.apple1_basic import ROM, resume_session
from tools.cffa1_model import blank_virtual_card
from tools.prodos import ProdosImage
from tools.textbook_support import ROOT

machine = blank_virtual_card()
machine.save_basic("HELLO", (ROOT / "software/basic/HELLO.bas").read_text())
image = ProdosImage(machine.memory.materialize())
entry = image.entries["/HELLO"]
assert entry.file_type == 0xF1
assert image.read("/HELLO").startswith(b"A1" + bytes([0]))
machine.memory[0x4A:0x100] = [0] * 182
machine.memory[0x800:0x1000] = [0] * 2048
machine.memory[0xE000:0xF000] = ROM.read_bytes()
machine.api(0x26, name="HELLO")
result = resume_session(machine.memory, ["RUN", "TOM"])
print("Saved type:", f"{entry.file_type:02X}", "bytes:", entry.size)
print("Program RAM and BASIC state cleared before LoadBASICFile")
print(result.transcript, end="")
assert "HELLO TOM" in result.transcript and "***" not in result.transcript
assert result.stop == "waiting-for-input"
