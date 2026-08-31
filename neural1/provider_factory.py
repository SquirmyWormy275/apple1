"""Construct qualified providers from backend-independent registry records."""

from __future__ import annotations

from pathlib import Path

from .core import Neural1Error
from .models import FakeProvider, LlamaCppProvider, ModelProvider, OllamaHttpProvider, RecordingProvider
from .registry import RegisteredModel


def provider_for(model: RegisteredModel, *, record_path: str | Path | None = None) -> ModelProvider:
    settings = dict(model.generation_defaults)
    if model.backend == "fake":
        provider: ModelProvider = FakeProvider(default=str(settings.get("default", "")))
    elif model.backend == "ollama":
        max_tokens = settings.pop("max_tokens", None)
        if max_tokens is not None:
            settings["num_predict"] = int(max_tokens)
        provider = OllamaHttpProvider(model.backend_name, timeout_seconds=float(settings.pop("timeout_seconds", 120)), options=settings)
    elif model.backend == "llama.cpp":
        executable = settings.pop("executable", None)
        model_path = settings.pop("model_path", None)
        if not executable or not model_path:
            raise Neural1Error("llama.cpp registry record requires executable and model_path")
        extra_args = tuple(str(value) for value in settings.pop("extra_args", ()))
        max_tokens = settings.pop("max_tokens", None)
        if max_tokens is not None:
            extra_args = (*extra_args, "-n", str(int(max_tokens)))
        provider = LlamaCppProvider(Path(str(executable)), Path(str(model_path)), model.digest, timeout_seconds=float(settings.pop("timeout_seconds", 120)), context_limit=model.context_limit, extra_args=extra_args)
    else:
        raise Neural1Error(f"provider factory cannot instantiate backend: {model.backend}")
    return RecordingProvider(provider, record_path) if record_path else provider
