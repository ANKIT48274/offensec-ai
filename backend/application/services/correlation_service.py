"""Correlation service — gathers evidence and runs AI analysis."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.infrastructure.correlation.analyzer import correlate
from backend.infrastructure.persistence.postgres.models import (
    AICorrelationModel,
    AssetModel,
    AttackPathModel,
    NucleiResultModel,
)


class CorrelationService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def analyze(self, project_id: str) -> dict[str, Any]:
        assets = await self._get_assets(project_id)
        nuclei = await self._get_nuclei(project_id)
        scans = await self._get_scans(project_id)
        httpx_data = await self._get_httpx(project_id)

        result = correlate(assets, nuclei, scans, httpx_data)

        analysis_id = uuid4().hex
        model = AICorrelationModel(
            id=analysis_id,
            project_id=project_id,
            analysis_type="full_correlation",
            title="AI Security Correlation Analysis",
            summary=result.get("executive_summary", ""),
            severity=_severity_from_score(result.get("risk_score", 0)),
            risk_score=result.get("risk_score", 0),
            assets=[a.get("value", "") for a in assets],
            findings=list(result.get("top_risks", [])),
            attack_paths=result.get("attack_paths", []),
            recommendations=result.get("recommendations", []),
            raw_analysis=result,
        )
        self._session.add(model)

        for path in result.get("attack_paths", []):
            ap = AttackPathModel(
                id=uuid4().hex,
                project_id=project_id,
                source=path.get("source", "external"),
                destination=path.get("destination", ""),
                technique=path.get("technique", ""),
                score=path.get("score", 50),
                evidence=path.get("evidence", []),
            )
            self._session.add(ap)

        await self._session.commit()

        result["analysis_id"] = analysis_id
        return result

    async def get_report(self, project_id: str) -> dict[str, Any] | None:
        result = await self._session.execute(
            select(AICorrelationModel)
            .where(AICorrelationModel.project_id == project_id)
            .order_by(AICorrelationModel.created_at.desc())
            .limit(1)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return {
            "id": model.id,
            "analysis_type": model.analysis_type,
            "title": model.title,
            "summary": model.summary,
            "severity": model.severity,
            "risk_score": model.risk_score,
            "assets": model.assets or [],
            "findings": model.findings or [],
            "attack_paths": model.attack_paths or [],
            "recommendations": model.recommendations or [],
            "created_at": model.created_at.isoformat() if model.created_at else None,
        }

    async def get_attack_paths(self, project_id: str) -> list[dict[str, Any]]:
        result = await self._session.execute(
            select(AttackPathModel)
            .where(AttackPathModel.project_id == project_id)
            .order_by(AttackPathModel.score.desc())
        )
        return [
            {
                "id": m.id,
                "source": m.source,
                "destination": m.destination,
                "technique": m.technique,
                "score": m.score,
                "evidence": m.evidence or [],
            }
            for m in result.scalars().all()
        ]

    async def _get_assets(self, project_id: str) -> list[dict[str, Any]]:
        result = await self._session.execute(
            select(AssetModel).where(AssetModel.project_id == project_id)
        )
        return [_asset_dict(m) for m in result.scalars().all()]

    async def _get_nuclei(self, project_id: str) -> list[dict[str, Any]]:
        if not hasattr(NucleiResultModel, "__tablename__"):
            return []
        result = await self._session.execute(
            select(NucleiResultModel)
            .where(NucleiResultModel.project_id == project_id)
            .order_by(NucleiResultModel.created_at.desc())
            .limit(100)
        )
        return [
            {
                "template_id": m.template_id,
                "template_name": m.template_name,
                "severity": m.severity,
                "matched_url": m.matched_url,
                "target": m.target,
                "description": m.description,
                "cve_ids": m.cve_ids or [],
            }
            for m in result.scalars().all()
        ]

    async def _get_scans(self, project_id: str) -> list[dict[str, Any]]:
        return []

    async def _get_httpx(self, project_id: str) -> list[dict[str, Any]]:
        return []


def _asset_dict(m: AssetModel) -> dict[str, Any]:
    return {
        "id": m.id,
        "project_id": m.project_id,
        "asset_type": m.asset_type,
        "value": m.value,
        "ips": m.ips or [],
        "ports": m.ports or [],
        "technologies": m.technologies or [],
        "os_guesses": m.os_guesses or [],
        "label": m.label,
        "scan_count": m.scan_count,
    }


def _severity_from_score(score: int) -> str:
    if score >= 70:
        return "critical"
    if score >= 40:
        return "high"
    if score >= 20:
        return "medium"
    return "low"
