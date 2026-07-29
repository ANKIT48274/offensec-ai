"""Dashboard API routes — risk overview, charts, and trends."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.infrastructure.auth_deps import get_current_user_id
from backend.infrastructure.di import get_db_session
from backend.infrastructure.persistence.postgres.models import (
    AssetModel,
    AttackPathModel,
    FindingModel,
    NucleiResultModel,
    ScanJobModel,
)
from backend.interfaces.api.responses import success_response

router = APIRouter()


@router.get("/overview")
async def dashboard_overview(
    project_id: str = Query(""),
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    counts = {
        "total_findings": 0, "critical": 0, "high": 0, "medium": 0, "low": 0,
        "total_assets": 0, "total_scans": 0, "attack_paths": 0, "risk_score": 0,
    }

    if project_id:
        f_res = await session.execute(
            select(func.count(FindingModel.id), FindingModel.severity)
            .where(FindingModel.assessment_id == project_id)  # simplified — in real impl would join project
            .group_by(FindingModel.severity)
        )
        for count, sev in f_res:
            counts[sev] = count

        a_res = await session.execute(select(func.count(AssetModel.id)).where(AssetModel.project_id == project_id))
        counts["total_assets"] = a_res.scalar() or 0

        s_res = await session.execute(select(func.count(ScanJobModel.id)).where(ScanJobModel.project_id == project_id))
        counts["total_scans"] = s_res.scalar() or 0

        ap_res = await session.execute(select(func.count(AttackPathModel.id)).where(AttackPathModel.project_id == project_id))
        counts["attack_paths"] = ap_res.scalar() or 0

    n_res = await session.execute(select(func.count(NucleiResultModel.id)).where(NucleiResultModel.severity == "critical"))
    counts["critical"] += n_res.scalar() or 0
    h_res = await session.execute(select(func.count(NucleiResultModel.id)).where(NucleiResultModel.severity == "high"))
    counts["high"] += h_res.scalar() or 0

    counts["total_findings"] = counts["critical"] + counts["high"] + counts["medium"] + counts["low"]

    risk = 0
    if counts["critical"] > 0:
        risk += 40
    if counts["high"] > 3:
        risk += 20
    risk = min(risk + counts["medium"] * 3 + counts["low"] * 1, 100)
    counts["risk_score"] = risk

    return success_response(counts)


@router.get("/findings-trend")
async def findings_trend(
    project_id: str = Query(""),
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    return success_response({"trend": "up", "period": "30d", "change": 0})


@router.get("/asset-graph")
async def asset_graph(
    project_id: str = Query(""),
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    return success_response({"nodes": [], "edges": []})
