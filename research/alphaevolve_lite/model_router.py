"""Remote-only Qwen/vLLM router for Phase 4 child dry runs."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


class ModelRouterError(RuntimeError):
    """Raised when the remote vLLM endpoint is unavailable or invalid."""


@dataclass(frozen=True)
class ModelEndpoint:
    role: str
    served_model_name: str
    base_url: str
    api_key_env: str = "AE_VLLM_API_KEY"

    @property
    def health_url(self) -> str:
        return self.base_url.removesuffix("/v1") + "/health"

    @property
    def models_url(self) -> str:
        return self.base_url.rstrip("/") + "/models"

    @property
    def chat_url(self) -> str:
        return self.base_url.rstrip("/") + "/chat/completions"


ENDPOINTS = {
    "fast_generator": ModelEndpoint(
        role="fast_generator",
        served_model_name="qwen35-9b-fast",
        base_url="http://127.0.0.1:8001/v1",
    ),
    "critic_repair": ModelEndpoint(
        role="critic_repair",
        served_model_name="qwen35-9b-fast",
        base_url="http://127.0.0.1:8001/v1",
    ),
}

DEFAULT_MAX_COMPLETION_TOKENS = 8192


def _read_url(url: str, *, api_key: str | None = None, payload: dict[str, Any] | None = None) -> tuple[int, str]:
    headers = {"User-Agent": "alphaevolve-lite-model-router"}
    data = None
    method = "GET"
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
        method = "POST"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            return int(response.status), response.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        raise ModelRouterError(
            "Qwen/vLLM endpoint is not reachable. Open a dedicated remote terminal or tmux pane, "
            "launch the required vLLM server, keep it running, and verify /health plus /v1/models before retrying. "
            f"Original error: {exc}"
        ) from exc


def get_endpoint(role: str) -> ModelEndpoint:
    try:
        return ENDPOINTS[role]
    except KeyError as exc:
        allowed = ", ".join(sorted(ENDPOINTS))
        raise ModelRouterError(f"unsupported model role {role!r}; allowed: {allowed}") from exc


def require_api_key(endpoint: ModelEndpoint) -> str:
    api_key = os.environ.get(endpoint.api_key_env)
    if not api_key:
        raise ModelRouterError(
            f"{endpoint.api_key_env} is not set. Set it only in the remote shell or private scheduler environment."
        )
    return api_key


def verify_endpoint(endpoint: ModelEndpoint) -> dict[str, Any]:
    """Verify health and served model before a Qwen call."""

    api_key = require_api_key(endpoint)
    health_status, health_body = _read_url(endpoint.health_url)
    model_status, model_body = _read_url(endpoint.models_url, api_key=api_key)
    try:
        model_payload = json.loads(model_body)
    except json.JSONDecodeError as exc:
        raise ModelRouterError(f"model list response is not JSON: {model_body[:200]}") from exc
    served_ids = [item.get("id") for item in model_payload.get("data", []) if isinstance(item, dict)]
    if endpoint.served_model_name not in served_ids:
        raise ModelRouterError(
            f"served model {endpoint.served_model_name!r} not found in /v1/models: {served_ids}"
        )
    return {
        "health_status": health_status,
        "health_body": health_body,
        "model_status": model_status,
        "served_model_name": endpoint.served_model_name,
        "served_ids": served_ids,
    }


def chat_completion(
    *,
    role: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.2,
    max_tokens: int = DEFAULT_MAX_COMPLETION_TOKENS,
    verify: bool = True,
) -> dict[str, Any]:
    """Call remote vLLM OpenAI-compatible chat completions."""

    endpoint = get_endpoint(role)
    api_key = require_api_key(endpoint)
    endpoint_status = verify_endpoint(endpoint) if verify else {}
    payload = {
        "model": endpoint.served_model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        # This is a direct HTTP client, not the OpenAI SDK. vLLM expects these
        # extra OpenAI-compatible fields at the top level of the JSON body.
        "chat_template_kwargs": {"enable_thinking": False},
        "top_p": 0.95,
    }
    status, body = _read_url(endpoint.chat_url, api_key=api_key, payload=payload)
    try:
        response = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ModelRouterError(f"chat response is not JSON: {body[:500]}") from exc
    choices = response.get("choices") or []
    if not choices:
        raise ModelRouterError(f"chat response had no choices: {body[:500]}")
    message = choices[0].get("message", {}) if isinstance(choices[0], dict) else {}
    content = message.get("content")
    reasoning = message.get("reasoning") or message.get("reasoning_content") or ""
    content_was_null = content is None
    if content is None:
        content = ""
    return {
        "status": status,
        "content": content,
        "content_was_null": content_was_null,
        "reasoning_length": len(reasoning) if isinstance(reasoning, str) else 0,
        "raw_response": response,
        "endpoint_status": endpoint_status,
        "role": role,
        "served_model_name": endpoint.served_model_name,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }


__all__ = [
    "DEFAULT_MAX_COMPLETION_TOKENS",
    "ModelEndpoint",
    "ModelRouterError",
    "chat_completion",
    "verify_endpoint",
]
