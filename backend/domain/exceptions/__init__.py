"""Domain layer exceptions for OffenSec AI."""


class DomainError(Exception):
    """Base exception for all domain errors."""

    def __init__(self, message: str, code: str | None = None) -> None:
        self.message = message
        self.code = code or "DOMAIN_ERROR"
        super().__init__(self.message)


class EntityNotFoundError(DomainError):
    """Raised when a requested entity does not exist."""

    def __init__(self, entity_type: str, entity_id: str) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(
            message=f"{entity_type} with id {entity_id} not found.",
            code="ENTITY_NOT_FOUND",
        )


class EntityAlreadyExistsError(DomainError):
    """Raised when attempting to create a duplicate entity."""

    def __init__(self, entity_type: str, identifier: str) -> None:
        self.entity_type = entity_type
        self.identifier = identifier
        super().__init__(
            message=f"{entity_type} with identifier '{identifier}' already exists.",
            code="ENTITY_ALREADY_EXISTS",
        )


class ValidationError(DomainError):
    """Raised when domain validation fails."""

    def __init__(self, field: str, reason: str) -> None:
        self.field = field
        self.reason = reason
        super().__init__(
            message=f"Validation failed for '{field}': {reason}",
            code="VALIDATION_ERROR",
        )


class ScopeViolationError(DomainError):
    """Raised when an operation exceeds the defined assessment scope."""

    def __init__(self, target: str, scope_id: str, reason: str) -> None:
        self.target = target
        self.scope_id = scope_id
        self.reason = reason
        super().__init__(
            message=f"Scope violation: target '{target}' is outside scope '{scope_id}': {reason}",
            code="SCOPE_VIOLATION",
        )


class AuthorizationError(DomainError):
    """Raised when a user lacks permission for an operation."""

    def __init__(self, user_id: str, action: str, resource: str) -> None:
        self.user_id = user_id
        self.action = action
        self.resource = resource
        super().__init__(
            message=f"User '{user_id}' not authorized to {action} on {resource}.",
            code="AUTHORIZATION_ERROR",
        )


class AssessmentStateError(DomainError):
    """Raised when an operation is invalid for the current assessment state."""

    def __init__(self, assessment_id: str, current_state: str, expected_state: str) -> None:
        self.assessment_id = assessment_id
        self.current_state = current_state
        self.expected_state = expected_state
        super().__init__(
            message=f"Assessment '{assessment_id}' is in state '{current_state}', expected '{expected_state}'.",
            code="ASSESSMENT_STATE_ERROR",
        )


class ConfigurationError(DomainError):
    """Raised when system configuration is invalid."""

    def __init__(self, key: str, reason: str) -> None:
        self.key = key
        self.reason = reason
        super().__init__(
            message=f"Configuration error for '{key}': {reason}",
            code="CONFIGURATION_ERROR",
        )


class ToolExecutionError(DomainError):
    """Raised when an external security tool fails."""

    def __init__(self, tool: str, exit_code: int, stderr: str) -> None:
        self.tool = tool
        self.exit_code = exit_code
        self.stderr = stderr
        super().__init__(
            message=f"Tool '{tool}' exited with code {exit_code}: {stderr[:500]}",
            code="TOOL_EXECUTION_ERROR",
        )
