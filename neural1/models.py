"""Model-provider abstraction; tests and demonstrations require no real model."""

from __future__ import annotations

import json
import subprocess
from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict, dataclass, field
from pathlib import Path
from time import perf_counter
from typing import Protocol
from urllib import error as urlerror
from urllib import request as urlrequest
from urllib.parse import urlparse

from .core import GenerationResult, ModelRecord, Neural1Error


class ModelProvider(Protocol):
    @property
    def record(self) -> ModelRecord: ...
    def generate(self, prompt: str, *, agent_id: str, seed: int) -> GenerationResult: ...


@dataclass
class FakeProvider:
    """Deterministic provider keyed by exact prompt, with a safe default."""

    responses: Mapping[str, str] = field(default_factory=dict)
    default: str = ""

    @property
    def record(self) -> ModelRecord:
        return ModelRecord(provider="fake", family="deterministic-fixture", name="fake-v1", version="1")

    def generate(self, prompt: str, *, agent_id: str, seed: int) -> GenerationResult:
        text = self.responses.get(prompt, self.default)
        return GenerationResult(text=text, provider_metadata={"agent_id": agent_id, "seed": seed})


@dataclass
class ReplayProvider:
    """Replays exact recorded responses and refuses unrecorded prompts."""

    responses: Mapping[tuple[str, str, int], GenerationResult]

    @property
    def record(self) -> ModelRecord:
        return ModelRecord(provider="replay", family="recorded", name="replay-v1", version="1")

    def generate(self, prompt: str, *, agent_id: str, seed: int) -> GenerationResult:
        try:
            return self.responses[(prompt, agent_id, seed)]
        except KeyError as error:
            raise Neural1Error("replay has no exact prompt/agent/seed record") from error


@dataclass
class OllamaHttpProvider:
    """Explicit localhost Ollama adapter with bounded HTTP requests."""

    model: str
    base_url: str = "http://127.0.0.1:11434"
    timeout_seconds: float = 120.0
    options: Mapping[str, object] = field(default_factory=dict)
    opener: Callable[[urlrequest.Request, float], bytes] | None = None

    def __post_init__(self) -> None:
        parsed = urlparse(self.base_url)
        if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
            raise Neural1Error("Ollama adapter permits explicit local HTTP endpoints only")
        if self.timeout_seconds <= 0:
            raise Neural1Error("Ollama timeout must be positive")

    @property
    def record(self) -> ModelRecord:
        return ModelRecord(provider="ollama-http", family=self.model.split(":", 1)[0], name=self.model, generation=dict(self.options))

    def generate(self, prompt: str, *, agent_id: str, seed: int) -> GenerationResult:
        body = json.dumps({"model": self.model, "prompt": prompt, "stream": False, "options": {**self.options, "seed": seed}}).encode("utf-8")
        request = urlrequest.Request(f"{self.base_url.rstrip('/')}/api/generate", body, {"Content-Type": "application/json"}, method="POST")  # noqa: S310 - base URL is validated as local HTTP
        start = perf_counter()
        try:
            raw = self.opener(request, self.timeout_seconds) if self.opener else self._open(request, self.timeout_seconds)
            payload = json.loads(raw)
        except (OSError, ValueError, KeyError, urlerror.URLError) as error:
            raise Neural1Error("Ollama request failed or returned invalid JSON") from error
        text = payload.get("response", "")
        if not isinstance(text, str) or not text.strip():
            raise Neural1Error("Ollama returned an empty response")
        latency = (perf_counter() - start) * 1000
        return GenerationResult(text, payload.get("prompt_eval_count"), payload.get("eval_count"), latency, {"agent_id": agent_id, "done_reason": payload.get("done_reason")})

    @staticmethod
    def _open(request: urlrequest.Request, timeout: float) -> bytes:
        with urlrequest.urlopen(request, timeout=timeout) as response:  # noqa: S310 - explicit localhost adapter; caller controls URL
            return response.read()


@dataclass
class LlamaCppProvider:
    """Bounded local-process adapter; never uses a shell."""

    executable: Path
    model_path: Path
    model_hash: str
    timeout_seconds: float = 120.0
    context_limit: int = 2048
    extra_args: Sequence[str] = ()
    runner: Callable[[list[str], float], tuple[str, str]] | None = None

    @property
    def record(self) -> ModelRecord:
        return ModelRecord(provider="llama.cpp", family="gguf", name=self.model_path.name, hash=self.model_hash, context_limit=self.context_limit, generation={"extra_args": list(self.extra_args)})

    def generate(self, prompt: str, *, agent_id: str, seed: int) -> GenerationResult:
        command = [str(self.executable), "-m", str(self.model_path), "-c", str(self.context_limit), "--seed", str(seed), "-p", prompt, *self.extra_args]
        start = perf_counter()
        try:
            stdout, stderr = self.runner(command, self.timeout_seconds) if self.runner else self._run(command, self.timeout_seconds)
        except (OSError, subprocess.SubprocessError) as error:
            raise Neural1Error("llama.cpp invocation failed") from error
        if not stdout.strip():
            raise Neural1Error("llama.cpp returned an empty response")
        return GenerationResult(stdout.strip(), latency_ms=(perf_counter() - start) * 1000, provider_metadata={"agent_id": agent_id, "stderr": stderr[-2000:]})

    @staticmethod
    def _run(command: list[str], timeout: float) -> tuple[str, str]:
        completed = subprocess.run(command, check=True, capture_output=True, text=True, timeout=timeout, shell=False)  # noqa: S603 - qualified local executable, shell disabled
        return completed.stdout, completed.stderr


class RecordingProvider:
    """Append exact prompt/result tuples so a run can later fail-closed replay."""

    def __init__(self, provider: ModelProvider, path: str | Path) -> None:
        self.provider = provider
        self.path = Path(path)

    @property
    def record(self) -> ModelRecord:
        return self.provider.record

    def generate(self, prompt: str, *, agent_id: str, seed: int) -> GenerationResult:
        try:
            result = self.provider.generate(prompt, agent_id=agent_id, seed=seed)
            record = {"prompt": prompt, "agent_id": agent_id, "seed": seed, "model": asdict(self.provider.record), "result": asdict(result), "error": None}
        except Exception as error:
            record = {"prompt": prompt, "agent_id": agent_id, "seed": seed, "model": asdict(self.provider.record), "result": None, "error": {"type": type(error).__name__, "message": str(error)}}
            self._append(record)
            raise
        self._append(record)
        return result

    def _append(self, record: Mapping[str, object]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=True, sort_keys=True) + "\n")

    @staticmethod
    def load_replay(path: str | Path) -> ReplayProvider:
        responses: dict[tuple[str, str, int], GenerationResult] = {}
        with Path(path).open(encoding="utf-8") as stream:
            for line in stream:
                record = json.loads(line)
                if record["error"] is None:
                    responses[(record["prompt"], record["agent_id"], record["seed"])] = GenerationResult(**record["result"])
        return ReplayProvider(responses)
