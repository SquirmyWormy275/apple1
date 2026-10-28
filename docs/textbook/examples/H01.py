events = [(1977, "Apple I Owners Club"), (1976, "Apple Computer Company"), (1975, "Altair era")]
ordered = sorted(events)
for year, event in ordered:
    print(year, event)
assert [year for year, event in ordered] == [1975, 1976, 1977]
