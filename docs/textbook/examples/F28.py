from pathlib import Path

from neural1.models import LlamaCppProvider

seen = []


def runner(command, timeout):
    seen.append(command)
    print("Executable:", command[0])
    print("Arguments include a model path:", "-m" in command)
    print("Timeout is bounded:", timeout > 0)
    return "0300: 2A", ""


r = LlamaCppProvider(Path("llama-cli"), Path("fixture.gguf"), "a" * 64, runner=runner).generate("READ", agent_id="A", seed=7)
print("Synthetic response:", r.text)
assert r.text == "0300: 2A" and seen
