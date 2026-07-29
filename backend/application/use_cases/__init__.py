"""Use case orchestration for complex workflows."""

from __future__ import annotations

from typing import Any

from backend.application.dto import (
    AIPlanRequestDTO,
    AIPlanResponseDTO,
    AssessmentCreateDTO,
    AssessmentResponseDTO,
    FindingCreateDTO,
    FindingResponseDTO,
    ReportGenerateDTO,
)
from backend.application.services import AssessmentService, FindingService
from backend.domain.exceptions import EntityNotFoundError


class RunAssessmentUseCase:
    """Orchestrates the full assessment lifecycle."""

    def __init__(
        self,
        assessment_service: AssessmentService,
        finding_service: FindingService,
    ) -> None:
        self._assessment_service = assessment_service
        self._finding_service = finding_service

    async def execute(self, assessment_id: str, user_id: str) -> AssessmentResponseDTO:
        assessment = await self._assessment_service.start(assessment_id, user_id)
        return assessment


class GenerateReportUseCase:
    """Orchestrates report generation."""

    def __init__(
        self,
        finding_service: FindingService,
        report_generator: Any,
    ) -> None:
        self._finding_service = finding_service
        self._report_generator = report_generator

    async def execute(self, dto: ReportGenerateDTO) -> str:
        findings = await self._finding_service.list_by_assessment(dto.assessment_id, 1, 1000)
        report = await self._report_generator.generate(
            findings=[f.to_dict() for f in findings.data] if hasattr(findings, "data") else [],
            format=dto.format,
        )
        return report


class BulkFindingImportUseCase:
    """Imports findings from external tool output."""

    def __init__(
        self,
        finding_service: FindingService,
    ) -> None:
        self._finding_service = finding_service

    async def execute(
        self,
        assessment_id: str,
        findings_data: list[dict[str, Any]],
        user_id: str,
    ) -> list[FindingResponseDTO]:
        results = []
        for data in findings_data:
            dto = FindingCreateDTO(
                assessment_id=assessment_id,
                title=data.get("title", ""),
                description=data.get("description", ""),
                severity=data.get("severity", "medium"),
                confidence=data.get("confidence", "medium"),
                target=data.get("target"),
                evidence=data.get("evidence", []),
                references=data.get("references", []),
                owasp_id=data.get("owasp_id"),
                cwe_id=data.get("cwe_id"),
                cvss_score=data.get("cvss_score"),
                remediation=data.get("remediation"),
            )
            result = await self._finding_service.create(dto, user_id)
            results.append(result)
        return results
