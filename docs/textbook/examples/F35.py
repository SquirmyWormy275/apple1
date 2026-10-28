from tools.firmware_behavior import QueueFullStop, SingleWriterQueue

queue = SingleWriterQueue(capacity=2)
queue.enqueue("ps2", b"A")
queue.enqueue("serial", b"B")
try:
    queue.enqueue("serial", b"C")
    raise AssertionError("overflow must stop")
except QueueFullStop:
    print("Overflow: STOP")
print("First:", queue.service_one())
print("Second:", queue.service_one())
assert queue.service_one() is None
print("Installed firmware changed: False")
