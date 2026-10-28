from py65.devices.mpu6502 import MPU

memory = [0] * 65536
memory[0xFFFC:0xFFFE] = [0x00, 0x03]
memory[0xFFFE:0x10000] = [0x00, 0x04]
memory[0x300:0x303] = [0x00, 0xEA, 0xEA]  # BRK, padding, next instruction
memory[0x400] = 0x40  # RTI
mpu = MPU(memory=memory, pc=None)
print("Reset-vector PC:", f"{mpu.pc:04X}")
assert mpu.pc == 0x300
mpu.step()
print("After BRK: PC", f"{mpu.pc:04X}", "SP", f"{mpu.sp:02X}")
print("Stack return high/low:", f"{memory[0x1FF]:02X} {memory[0x1FE]:02X}")
assert mpu.pc == 0x400 and mpu.sp == 0xFC
assert memory[0x1FF:0x200] == [0x03] and memory[0x1FE] == 0x02
mpu.step()
print("After RTI: PC", f"{mpu.pc:04X}", "SP", f"{mpu.sp:02X}")
assert mpu.pc == 0x302 and mpu.sp == 0xFF
print("Direct Py65 CPU semantics: BRK uses IRQ/BRK vector and resumes at BRK+2 after RTI.")
print("The NEURAL1 world instead treats BRK as a stop marker before executing it.")
