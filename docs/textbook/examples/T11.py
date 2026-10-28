from tools.apple1_emulator import Apple1RamHarness
from tools.textbook_support import ROOT

harness = Apple1RamHarness.from_program_file(ROOT / "software/ram-only/line-input-0300.hex")
for count, expected_length, expected_steps in [(0, 1, 10), (1, 2, 20), (127, 128, 1280), (128, 128, 1282)]:
    r = harness.run_keyboard_line("A" * count + "\r")
    print(f"Ordinary characters={count}; emitted={len(r.screen_text)}; CR emitted={r.screen_text.endswith(chr(13))}; instructions={r.instructions}")
    assert len(r.screen_text) == expected_length and r.instructions == expected_steps and r.returned_to_monitor
    assert r.screen_text.endswith("\r") is (count < 128)
print("At 128 ordinary characters, the Y=$80 exit occurs before reading the supplied Return.")
print("For n<=127: setup 1 + ordinary passes 10*n + CR pass 8 + final JMP 1 = 10*(n+1).")
