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

from .core import GenerationResult, ModelRecord, Neural1Error, sha256_bytes


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
    api: str = "generate"
    keep_alive: str | int | float | None = None
    format: str | None = None
    model_hash: str = "UNAVAILABLE"
    quantization: str = "UNAVAILABLE"
    context_limit: int | None = None
    model_family: str | None = None

    def __post_init__(self) -> None:
        parsed = urlparse(self.base_url)
        if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
            raise Neural1Error("Ollama adapter permits explicit local HTTP endpoints only")
        if self.timeout_seconds <= 0:
            raise Neural1Error("Ollama timeout must be positive")
        if self.api not in {"generate", "chat"}:
            raise Neural1Error("Ollama api must be explicitly generate or chat")
        if self.format is not None and self.format != "json":
            raise Neural1Error("Ollama format must be json or unset")
        if isinstance(self.keep_alive, bool) or (self.keep_alive is not None and not isinstance(self.keep_alive, str | int | float)):
            raise Neural1Error("Ollama keep_alive must be a duration string or number")
        if any(key in self.options for key in ("api", "base_url", "keep_alive", "timeout_seconds", "format")):
            raise Neural1Error("Ollama transport settings must not be generation options")
        if self.model_hash != "UNAVAILABLE" and (len(self.model_hash) != 64 or any(value not in "0123456789abcdefABCDEF" for value in self.model_hash)):
            raise Neural1Error("Ollama qualified model hash must be a SHA-256 manifest digest")
        if self.context_limit is not None:
            if self.context_limit <= 0:
                raise Neural1Error("Ollama context limit must be positive")
            self.options = {"num_ctx": self.context_limit, **self.options}
            if self.options["num_ctx"] != self.context_limit:
                raise Neural1Error("Ollama recorded context limit differs from requested num_ctx")

    @property
    def record(self) -> ModelRecord:
        generation = {**self.options, "api": self.api, "base_url": self.base_url, "timeout_seconds": self.timeout_seconds}
        if self.format is not None:
            generation["format"] = self.format
        if self.keep_alive is not None:
            generation["keep_alive"] = self.keep_alive
        if self.model_hash != "UNAVAILABLE":
            generation["hash_kind"] = "ollama-manifest; not the GGUF weight blob"
        return ModelRecord(provider="ollama-http", family=self.model_family or self.model.split(":", 1)[0], name=self.model, hash=self.model_hash, quantization=self.quantization, context_limit=self.context_limit, generation=generation)

    def generate(self, prompt: str, *, agent_id: str, seed: int) -> GenerationResult:
        body_fields: dict[str, object] = {"model": self.model, "stream": False, "options": {**self.options, "seed": seed}}
        if self.api == "chat":
            body_fields["messages"] = [{"role": "user", "content": prompt}]
        else:
            body_fields["prompt"] = prompt
        if self.format is not None:
            body_fields["format"] = self.format
        if self.keep_alive is not None:
            body_fields["keep_alive"] = self.keep_alive
        body = json.dumps(body_fields).encode("utf-8")
        endpoint = f"{self.base_url.rstrip('/')}/api/{self.api}"
        request = urlrequest.Request(endpoint, body, {"Content-Type": "application/json"}, method="POST")  # noqa: S310 - base URL is validated as local HTTP
        start = perf_counter()
        try:
            raw = self.opener(request, self.timeout_seconds) if self.opener else self._open(request, self.timeout_seconds)
            raw_text = raw.decode("utf-8")
            payload = json.loads(raw_text)
        except (OSError, ValueError, KeyError, urlerror.URLError) as error:
            raise Neural1Error("Ollama request failed or returned invalid JSON") from error
        if not isinstance(payload, dict):
            raise Neural1Error("Ollama returned a non-object response")
        if self.api == "chat":
            message = payload.get("message")
            if not isinstance(message, dict):
                raise Neural1Error("Ollama chat returned no assistant message")
            text = message.get("content", "")
        else:
            text = payload.get("response", "")
        if not isinstance(text, str) or not text.strip():
            raise Neural1Error("Ollama returned an empty response")
        latency = (perf_counter() - start) * 1000
        metadata = {"agent_id": agent_id, "seed": seed, "api": self.api, "format": self.format, "endpoint": endpoint, "done_reason": payload.get("done_reason"), "response_payload": payload, "raw_response_utf8": raw_text, "raw_response_sha256": sha256_bytes(raw)}
        return GenerationResult(text, payload.get("prompt_eval_count"), payload.get("eval_count"), latency, metadata)

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
