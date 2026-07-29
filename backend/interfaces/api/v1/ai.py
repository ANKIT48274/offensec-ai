"""AI agent API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from backend.application.dto import AIPlanRequestDTO
from backend.infrastructure.ai_client import BaseAIClient, create_ai_client
from backend.interfaces.api.responses import error_response, success_response

router = APIRouter()


async def get_ai_client() -> BaseAIClient:
    return create_ai_client()


@router.post("/plan")
async def generate_plan(
    body: AIPlanRequestDTO,
    ai_client: BaseAIClient = Depends(get_ai_client),
) -> Any:
    try:
        plan = await ai_client.generate_plan(body.context)
        return success_response(plan)
    except Exception as e:
        return error_response(str(e), code="AI_PLAN_ERROR")


@router.post("/analyze")
async def analyze_evidence(
    evidence: list[dict[str, Any]],
    ai_client: BaseAIClient = Depends(get_ai_client),
) -> Any:
    try:
        analysis = await ai_client.analyze_finding(evidence)
        return success_response(analysis)
    except Exception as e:
        return error_response(str(e), code="AI_ANALYSIS_ERROR")


@router.post("/explain")
async def explain_topic(
    topic: str,
    context: dict[str, Any] | None = None,
    ai_client: BaseAIClient = Depends(get_ai_client),
) -> Any:
    if context is None:
        context = {}
    try:
        explanation = await ai_client.explain(topic, context)
        return success_response({"explanation": explanation})
    except Exception as e:
        return error_response(str(e), code="AI_EXPLAIN_ERROR")
