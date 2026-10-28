from neural1.family_runner import evaluate_family
from neural1.world import VirtualApple1World

result = evaluate_family("1976-multiverse", VirtualApple1World(), [])
print("Status:", result["status"])
print("Passed:", result["passed"])
assert result["status"] == "EVALUATED" and not result["passed"]
print("Missing historical values were not estimated.")
