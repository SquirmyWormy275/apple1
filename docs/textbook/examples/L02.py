parameters = 1_500_000_000
for bits in (16, 8, 4):
    nominal = parameters * bits // 8
    print(f"{bits:2d} bits: {nominal:,} nominal weight bytes ({nominal / 2**30:.3f} GiB)")
assert parameters * 4 // 8 == 750_000_000
print("Total runtime RAM: not established by this calculation")
