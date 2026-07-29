"""Application service implementations."""

from __future__ import annotations

from datetime import UTC, datetime, timezone
from typing import Any

from backend.application.dto import (
    AIPlanRequestDTO,
    AIPlanResponseDTO,
    AssessmentCreateDTO,
    AssessmentResponseDTO,
    FindingCreateDTO,
    FindingResponseDTO,
    PaginatedResponseDTO,
    ProjectCreateDTO,
    ProjectResponseDTO,
    ProjectUpdateDTO,
    ReportGenerateDTO,
    UserRegisterDTO,
    UserResponseDTO,
)
from backend.application.interfaces import (
    AIClient,
    AssessmentRepository,
    AuditLogger,
    EventBus,
    FindingRepository,
    PasswordHasher,
    ProjectRepository,
    ReportGenerator,
    ScopeValidator,
    TokenService,
    UnitOfWork,
    UserRepository,
)
from backend.domain.entities import Assessment, Finding, Project, User
from backend.domain.events import (
    AssessmentCompleted,
    AssessmentStarted,
    FindingCreated,
    ProjectCreated,
)
from backend.domain.exceptions import (
    AssessmentStateError,
    AuthorizationError,
    EntityNotFoundError,
)
from backend.domain.value_objects import AssessmentStatus, Confidence, FindingStatus, Severity


class UserService:
    def __init__(
        self,
        user_repo: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
        audit_logger: AuditLogger,
        event_bus: EventBus,
    ) -> None:
        self._user_repo = user_repo
        self._password_hasher = password_hasher
        self._token_service = token_service
        self._audit_logger = audit_logger
        self._event_bus = event_bus

    async def register(self, dto: UserRegisterDTO, ip: str | None = None) -> UserResponseDTO:
        existing = await self._user_repo.get_by_email(dto.email)
        if existing:
            from backend.domain.exceptions import EntityAlreadyExistsError

            raise EntityAlreadyExistsError("User", dto.email)

        password_hash = self._password_hasher.hash(dto.password)
        user = User(email=dto.email, username=dto.username, password_hash=password_hash)
        result = await self._user_repo.create(user.to_dict())
        await self._audit_logger.log(
            actor_id=result.id,
            action="user.register",
            resource_type="user",
            resource_id=result.id,
            details={"email": result.email},
            ip_address=ip,
        )
        return result

    async def get_by_id(self, user_id: str) -> UserResponseDTO:
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            from backend.domain.exceptions import EntityNotFoundError

            raise EntityNotFoundError("User", user_id)
        return user

    async def authenticate(
        self, email: str, password: str, ip: str | None = None
    ) -> tuple[str, str]:
        user = await self._user_repo.get_by_email(email)
        if not user:
            raise AuthorizationError("unknown", "login", f"user {email}")
        if not self._password_hasher.verify(password, user.password_hash):
            raise AuthorizationError(user.id, "login", f"user {email}")

        await self._user_repo.update(user.id, {"last_login_at": datetime.now(UTC)})
        access = self._token_service.create_access_token(user.id)
        refresh = self._token_service.create_refresh_token(user.id)
        await self._audit_logger.log(
            actor_id=user.id,
            action="user.login",
            resource_type="user",
            resource_id=user.id,
            ip_address=ip,
        )
        return access, refresh, user.id


class ProjectService:
    def __init__(
        self,
        project_repo: ProjectRepository,
        audit_logger: AuditLogger,
        event_bus: EventBus,
    ) -> None:
        self._project_repo = project_repo
        self._audit_logger = audit_logger
        self._event_bus = event_bus

    async def create(self, dto: ProjectCreateDTO, owner_id: str) -> ProjectResponseDTO:
        project = Project(name=dto.name, description=dto.description, owner_id=owner_id)
        result = await self._project_repo.create(project.to_dict())
        await self._event_bus.publish(
            ProjectCreated(project_id=result.id, name=result.name, owner_id=owner_id)
        )
        return result

    async def get_by_id(self, project_id: str, user_id: str) -> ProjectResponseDTO:
        project = await self._project_repo.get_by_id(project_id)
        if not project:
            raise EntityNotFoundError("Project", project_id)
        if project.owner_id != user_id:
            raise AuthorizationError(user_id, "view", f"project/{project_id}")
        return project

    async def list_by_user(self, user_id: str, page: int, page_size: int) -> PaginatedResponseDTO:
        return await self._project_repo.list_by_owner(user_id, page, page_size)

    async def update(
        self, project_id: str, dto: ProjectUpdateDTO, user_id: str
    ) -> ProjectResponseDTO:
        existing = await self._project_repo.get_by_id(project_id)
        if not existing:
            raise EntityNotFoundError("Project", project_id)
        if existing.owner_id != user_id:
            raise AuthorizationError(user_id, "update", f"project/{project_id}")
        data = dto.model_dump(exclude_none=True)
        return await self._project_repo.update(project_id, data)

    async def delete(self, project_id: str, user_id: str) -> None:
        existing = await self._project_repo.get_by_id(project_id)
        if not existing:
            raise EntityNotFoundError("Project", project_id)
        if existing.owner_id != user_id:
            raise AuthorizationError(user_id, "delete", f"project/{project_id}")
        await self._project_repo.delete(project_id)


class AssessmentService:
    def __init__(
        self,
        assessment_repo: AssessmentRepository,
        scope_validator: ScopeValidator,
        audit_logger: AuditLogger,
        event_bus: EventBus,
    ) -> None:
        self._assessment_repo = assessment_repo
        self._scope_validator = scope_validator
        self._audit_logger = audit_logger
        self._event_bus = event_bus

    async def create(self, dto: AssessmentCreateDTO, user_id: str) -> AssessmentResponseDTO:
        assessment = Assessment(
            project_id=dto.project_id,
            name=dto.name,
            scope={"targets": dto.targets, **(dto.scope or {})},
            started_by=user_id,
        )
        result = await self._assessment_repo.create(assessment.to_dict())
        return result

    async def get_by_id(self, assessment_id: str, user_id: str) -> AssessmentResponseDTO:
        assessment = await self._assessment_repo.get_by_id(assessment_id)
        if not assessment:
            raise EntityNotFoundError("Assessment", assessment_id)
        return assessment

    async def list_by_project(
        self, project_id: str, page: int, page_size: int
    ) -> PaginatedResponseDTO:
        return await self._assessment_repo.list_by_project(project_id, page, page_size)

    async def start(self, assessment_id: str, user_id: str) -> AssessmentResponseDTO:
        assessment = await self._assessment_repo.get_by_id(assessment_id)
        if not assessment:
            raise EntityNotFoundError("Assessment", assessment_id)

        domain = Assessment(
            id=assessment.id,
            project_id=assessment.project_id,
            name=assessment.name,
            status=AssessmentStatus(assessment.status),
            started_by=assessment.started_by,
        )
        domain.start()
        result = await self._assessment_repo.update(assessment_id, domain.to_dict())
        await self._event_bus.publish(
            AssessmentStarted(
                assessment_id=assessment_id,
                project_id=assessment.project_id,
                scope_id="",
                started_by=user_id,
            )
        )
        return result

    async def complete(self, assessment_id: str, user_id: str) -> AssessmentResponseDTO:
        assessment = await self._assessment_repo.get_by_id(assessment_id)
        if not assessment:
            raise EntityNotFoundError("Assessment", assessment_id)

        domain = Assessment(
            id=assessment.id,
            project_id=assessment.project_id,
            name=assessment.name,
            status=AssessmentStatus(assessment.status),
            started_by=assessment.started_by,
        )
        domain.complete()
        result = await self._assessment_repo.update(assessment_id, domain.to_dict())
        await self._event_bus.publish(
            AssessmentCompleted(
                assessment_id=assessment_id,
                project_id=assessment.project_id,
                finding_count=0,
                critical_count=0,
            )
        )
        return result


class FindingService:
    def __init__(
        self,
        finding_repo: FindingRepository,
        ai_client: AIClient,
        audit_logger: AuditLogger,
        event_bus: EventBus,
    ) -> None:
        self._finding_repo = finding_repo
        self._ai_client = ai_client
        self._audit_logger = audit_logger
        self._event_bus = event_bus

    async def create(self, dto: FindingCreateDTO, user_id: str) -> FindingResponseDTO:
        severity = Severity(dto.severity) if dto.severity else Severity.MEDIUM
        confidence = Confidence(dto.confidence) if dto.confidence else Confidence.MEDIUM

        finding = Finding(
            assessment_id=dto.assessment_id,
            title=dto.title,
            description=dto.description,
            severity=severity,
            confidence=confidence,
            target=dto.target or "",
            evidence=dto.evidence,
            references=dto.references,
            owasp_id=dto.owasp_id,
            cwe_id=dto.cwe_id,
            cvss_score=dto.cvss_score,
            remediation=dto.remediation,
            created_by=user_id,
        )
        result = await self._finding_repo.create(finding.to_dict())
        await self._event_bus.publish(
            FindingCreated(
                finding_id=result.id,
                assessment_id=result.assessment_id,
                title=result.title,
                severity=result.severity,
                target=result.target or "",
            )
        )
        return result

    async def get_by_id(self, finding_id: str) -> FindingResponseDTO:
        finding = await self._finding_repo.get_by_id(finding_id)
        if not finding:
            raise EntityNotFoundError("Finding", finding_id)
        return finding

    async def list_by_assessment(
        self, assessment_id: str, page: int, page_size: int
    ) -> PaginatedResponseDTO:
        return await self._finding_repo.list_by_assessment(assessment_id, page, page_size)
