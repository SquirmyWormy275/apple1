import json

from neural1.models import OllamaHttpProvider

seen = []


def opener(request, timeout):
    payload = json.loads(request.data)
    seen.append(payload)
    print("Endpoint:", request.full_url)
    print("Model:", payload["model"], "seed:", payload["options"]["seed"])
    return json.dumps({"response": "0300: 2A", "prompt_eval_count": 3, "eval_count": 2}).encode()


r = OllamaHttpProvider("teaching-fixture", opener=opener).generate("READ", agent_id="A", seed=7)
print("Synthetic response:", r.text, "tokens:", r.completion_tokens)
assert r.completion_tokens == 2 and seen[0]["options"]["seed"] == 7
