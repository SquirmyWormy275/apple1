from tools.textbook_support import emit

proposal = {
    "objective": "predict the byte at $0400 after LDA/STA",
    "result": "$2A",
    "check": "compare prediction with virtual readback",
    "mode": "VIRTUAL_EXECUTION",
}
emit(proposal)
assert all(proposal.values())
