from tools.cffa1_model import blank_virtual_card
from tools.prodos import ProdosImage

machine = blank_virtual_card()
data = b"HELLO FROM A VIRTUAL CARD" + bytes([13])
machine.write_file("HELLO", data, file_type=4)
assert machine.read_file("HELLO") == data
image = ProdosImage(machine.memory.materialize())
assert image.read("/HELLO") == data
print("Actual CFFA1 ROM: format -> write -> read")
print("Independent ProDOS inventory:", image.inventory())
print("ATA blocks written:", machine.memory.writes)
print("Physical devices opened: 0")
