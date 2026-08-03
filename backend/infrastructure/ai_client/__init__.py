"""AI model client abstraction for multiple providers."""

from __future__ import annotations

import os
from typing import Any

import httpx


class AIProviderError(Exception):
    """Raised when the AI provider returns an error."""


class BaseAIClient:
    """Abstract base for AI model clients."""

    async def generate_plan(self, context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    async def analyze_finding(self, evidence: list[dict[str, Any]]) -> dict[str, Any]:
        raise NotImplementedError

    async def generate_report(self, data: dict[str, Any]) -> str:
        raise NotImplementedError

    async def explain(self, topic: str, context: dict[str, Any]) -> str:
        raise NotImplementedError


class LocalAIClient(BaseAIClient):
    """Client for local model inference via the ai-runner service."""

    def __init__(self, base_url: str = "http://ai-runner:8001") -> None:
        self._base_url = base_url
        self._client = httpx.AsyncClient(timeout=120.0)

    async def generate_plan(self, context: dict[str, Any]) -> dict[str, Any]:
        response = await self._client.post(
            f"{self._base_url}/v1/plan",
            json=context,
        )
        response.raise_for_status()
        return response.json()

    async def analyze_finding(self, evidence: list[dict[str, Any]]) -> dict[str, Any]:
        response = await self._client.post(
            f"{self._base_url}/v1/analyze",
            json={"evidence": evidence},
        )
        response.raise_for_status()
        return response.json()

    async def generate_report(self, data: dict[str, Any]) -> str:
        response = await self._client.post(
            f"{self._base_url}/v1/report",
            json=data,
        )
        response.raise_for_status()
        return response.text

    async def explain(self, topic: str, context: dict[str, Any]) -> str:
        response = await self._client.post(
            f"{self._base_url}/v1/explain",
            json={"topic": topic, "context": context},
        )
        response.raise_for_status()
        return response.text

    async def close(self) -> None:
        await self._client.aclose()


class OpenAICompatibleClient(BaseAIClient):
    """Client for OpenAI-compatible APIs."""

    def __init__(self) -> None:
        self._api_key = os.environ.get("OPENAI_API_KEY", "")
        self._base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self._model = os.environ.get("OPENAI_MODEL", "gpt-4o")
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=120.0,
            headers={"Authorization": f"Bearer {self._api_key}"},
        )

    async def _chat_completion(
        self, messages: list[dict[str, str]], response_format: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "model": self._model,
            "messages": messages,
            "temperature": 0.1,
        }
        if response_format:
            body["response_format"] = response_format

        response = await self._client.post("/chat/completions", json=body)
        response.raise_for_status()
        return response.json()

    async def generate_plan(self, context: dict[str, Any]) -> dict[str, Any]:
        messages = [
            {
                "role": "system",
                "content": "You are a penetration testing planning assistant. Generate a structured assessment plan.",
            },
            {"role": "user", "content": str(context)},
        ]
        result = await self._chat_completion(messages)
        return {"plan": result["choices"][0]["message"]["content"]}

    async def analyze_finding(self, evidence: list[dict[str, Any]]) -> dict[str, Any]:
        messages = [
            {
                "role": "system",
                "content": "Analyze the following security evidence and produce structured findings.",
            },
            {"role": "user", "content": str(evidence)},
        ]
        result = await self._chat_completion(messages)
        return {"analysis": result["choices"][0]["message"]["content"]}

    async def generate_report(self, data: dict[str, Any]) -> str:
        messages = [
            {
                "role": "system",
                "content": "Generate a professional penetration testing report from the provided findings.",
            },
            {"role": "user", "content": str(data)},
        ]
        result = await self._chat_completion(messages)
        return result["choices"][0]["message"]["content"]

    async def explain(self, topic: str, context: dict[str, Any]) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are a security education assistant. Explain the following topic in context.",
            },
            {"role": "user", "content": f"Topic: {topic}\nContext: {context}"},
        ]
        result = await self._chat_completion(messages)
        return result["choices"][0]["message"]["content"]

    async def close(self) -> None:
        await self._client.aclose()


class FallbackAIClient(BaseAIClient):
    """LocalAI client with a rules-based offline fallback.

    Uses the `correlate()` rules engine so the platform stays fully
    functional (per the README promise) even when the ai-runner service
    is not deployed or is temporarily unreachable.
    """

    def __init__(self, base_url: str = "http://ai-runner:8001") -> None:
        self._local = LocalAIClient(base_url=base_url)
        from backend.infrastructure.correlation.analyzer import correlate

        self._correlate = correlate

    async def generate_plan(self, context: dict[str, Any]) -> dict[str, Any]:
        try:
            return await self._local.generate_plan(context)
        except Exception:
            return {
                "plan": _rules_based_plan(context),
                "fallback": True,
            }

    async def analyze_finding(self, evidence: list[dict[str, Any]]) -> dict[str, Any]:
        try:
            return await self._local.analyze_finding(evidence)
        except Exception:
            return self._rules_analyze(evidence)

    async def generate_report(self, data: dict[str, Any]) -> str:
        try:
            return await self._local.generate_report(data)
        except Exception:
            return _rules_based_report(data)

    async def explain(self, topic: str, context: dict[str, Any]) -> str:
        try:
            return await self._local.explain(topic, context)
        except Exception:
            return (
                f"# {topic}\n\n"
                f"**Context:** {context}\n\n"
                "_Offline analysis: a full LLM explanation requires the ai-runner "
                "service. Findings are ranked by the rules-based correlation engine._"
            )

    def _rules_analyze(self, evidence: list[dict[str, Any]]) -> dict[str, Any]:
        """Structured analysis using the rules-based correlation engine."""
        assets = [e for e in evidence if e.get("type") == "asset"]
        nuclei = [e for e in evidence if e.get("type") == "nuclei" or e.get("template_id")]
        scans = [e for e in evidence if e.get("type") == "scan"]
        httpx_data = [e for e in evidence if e.get("type") == "httpx"]

        if not assets and not nuclei and not scans and not httpx_data:
            assets = evidence

        result = self._correlate(
            assets=assets, nuclei=nuclei, scans=scans, httpx_data=httpx_data
        )
        result["fallback"] = True
        return result

    async def close(self) -> None:
        await self._local.close()


def _rules_based_plan(context: dict[str, Any]) -> str:
    """Generate a simple methodology plan from assessment context."""
    target = context.get("target") or context.get("targets") or "target"
    scope = context.get("scope", "")
    lines = [
        f"# Assessment Plan — {target}",
        "",
        "## Phase 1: Reconnaissance",
        "- Run nmap port scan (-sV -sC) to identify open services",
        "- Enumerate subdomains and DNS records",
        "",
        "## Phase 2: Service Probing",
        "- Probe web services with httpx (tech detection, TLS)",
        "- Crawl endpoints with katana",
        "",
        "## Phase 3: Vulnerability Scanning",
        "- Run nuclei templates against exposed services",
        "- Fuzz directories with ffuf",
        "",
        "## Phase 4: Analysis",
        "- Correlate findings and rank risks (0-100)",
        "- Map to OWASP Top 10 / MITRE ATT&CK",
    ]
    if scope:
        lines.insert(3, f"- In-scope: {scope}")
    return "\n".join(lines)


def _rules_based_report(data: dict[str, Any]) -> str:
    """Render a markdown report from findings without an external LLM."""
    from backend.infrastructure.reporting import MarkdownReportGenerator
    import asyncio

    findings = data.get("findings", []) if isinstance(data, dict) else []
    assessment = data.get("assessment") if isinstance(data, dict) else None
    gen = MarkdownReportGenerator()
    return asyncio.run(gen.generate(findings=findings, assessment=assessment))


def create_ai_client() -> BaseAIClient:
    """Factory to create the appropriate AI client based on configuration."""
    provider = os.environ.get("AI_MODEL_PROVIDER", "local")

    if provider == "openai":
        return OpenAICompatibleClient()

    base_url = os.environ.get("AI_MODEL_BASE_URL", "http://ai-runner:8001")
    return FallbackAIClient(base_url=base_url)
