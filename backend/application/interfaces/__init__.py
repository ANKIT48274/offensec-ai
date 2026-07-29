"""Port interfaces for dependency inversion in the application layer."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional, Protocol

from backend.application.dto import (
    AssessmentResponseDTO,
    FindingResponseDTO,
    PaginatedResponseDTO,
    ProjectResponseDTO,
    UserResponseDTO,
)


class UnitOfWork(Protocol):
    """Unit of work pattern for transaction management."""

    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
    async def close(self) -> None: ...


class PasswordHasher(Protocol):
    def hash(self, password: str) -> str: ...
    def verify(self, password: str, hashed: str) -> bool: ...


class TokenService(Protocol):
    def create_access_token(
        self, user_id: str, extra_claims: dict[str, Any] | None = None
    ) -> str: ...
    def create_refresh_token(self, user_id: str) -> str: ...
    def decode_token(self, token: str) -> dict[str, Any]: ...


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: dict[str, Any]) -> UserResponseDTO: ...
    @abstractmethod
    async def get_by_id(self, user_id: str) -> UserResponseDTO | None: ...
    @abstractmethod
    async def get_by_email(self, email: str) -> UserResponseDTO | None: ...
    @abstractmethod
    async def get_by_username(self, username: str) -> UserResponseDTO | None: ...
    @abstractmethod
    async def list(self, page: int, page_size: int) -> PaginatedResponseDTO: ...
    @abstractmethod
    async def update(self, user_id: str, data: dict[str, Any]) -> UserResponseDTO: ...
    @abstractmethod
    async def delete(self, user_id: str) -> None: ...


class ProjectRepository(ABC):
    @abstractmethod
    async def create(self, project: dict[str, Any]) -> ProjectResponseDTO: ...
    @abstractmethod
    async def get_by_id(self, project_id: str) -> ProjectResponseDTO | None: ...
    @abstractmethod
    async def list_by_owner(
        self, owner_id: str, page: int, page_size: int
    ) -> PaginatedResponseDTO: ...
    @abstractmethod
    async def update(self, project_id: str, data: dict[str, Any]) -> ProjectResponseDTO: ...
    @abstractmethod
    async def delete(self, project_id: str) -> None: ...


class AssessmentRepository(ABC):
    @abstractmethod
    async def create(self, assessment: dict[str, Any]) -> AssessmentResponseDTO: ...
    @abstractmethod
    async def get_by_id(self, assessment_id: str) -> AssessmentResponseDTO | None: ...
    @abstractmethod
    async def list_by_project(
        self, project_id: str, page: int, page_size: int
    ) -> PaginatedResponseDTO: ...
    @abstractmethod
    async def update(self, assessment_id: str, data: dict[str, Any]) -> AssessmentResponseDTO: ...
    @abstractmethod
    async def delete(self, assessment_id: str) -> None: ...


class FindingRepository(ABC):
    @abstractmethod
    async def create(self, finding: dict[str, Any]) -> FindingResponseDTO: ...
    @abstractmethod
    async def get_by_id(self, finding_id: str) -> FindingResponseDTO | None: ...
    @abstractmethod
    async def list_by_assessment(
        self, assessment_id: str, page: int, page_size: int
    ) -> PaginatedResponseDTO: ...
    @abstractmethod
    async def update(self, finding_id: str, data: dict[str, Any]) -> FindingResponseDTO: ...
    @abstractmethod
    async def delete(self, finding_id: str) -> None: ...


class EventBus(Protocol):
    """Publish domain events."""

    async def publish(self, event: Any) -> None: ...
    async def subscribe(self, event_type: type, handler: Any) -> None: ...


class AIClient(Protocol):
    """AI model client interface."""

    async def generate_plan(self, context: dict[str, Any]) -> dict[str, Any]: ...
    async def analyze_finding(self, evidence: list[dict[str, Any]]) -> dict[str, Any]: ...
    async def generate_report(self, data: dict[str, Any]) -> str: ...
    async def explain(self, topic: str, context: dict[str, Any]) -> str: ...


class ReportGenerator(Protocol):
    """Report generation interface."""

    async def generate(self, findings: list[dict[str, Any]], format: str) -> str: ...


class ScopeValidator(Protocol):
    """Scope validation interface."""

    async def validate_target(self, target: str, scope: dict[str, Any]) -> bool: ...
    async def validate_technique(self, technique: str, scope: dict[str, Any]) -> bool: ...


class AuditLogger(Protocol):
    """Audit logging interface."""

    async def log(
        self,
        actor_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        details: dict[str, Any] | None = None,
        ip_address: str | None = None,
    ) -> None: ...
