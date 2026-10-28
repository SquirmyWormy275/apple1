import json

from neural1.models import OllamaHttpProvider


def opener(request, timeout):
    return json.dumps({"response": "0300: 2A", "prompt_eval_count": 7, "eval_count": 4}).encode()


r = OllamaHttpProvider("token-fixture", opener=opener).generate("Inspect byte", agent_id="A", seed=1)
print("Fixture prompt tokens:", r.prompt_tokens)
print("Fixture output tokens:", r.completion_tokens)
print("Response ASCII bytes:", len(r.text.encode("ascii")))
assert r.prompt_tokens == 7 and r.completion_tokens == 4
