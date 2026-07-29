"""Tests for domain exceptions."""

from backend.domain.exceptions import (
    AssessmentStateError,
    AuthorizationError,
    DomainError,
    EntityNotFoundError,
    ScopeViolationError,
    ToolExecutionError,
    ValidationError,
)


class TestDomainError:
    def test_base_exception(self):
        e = DomainError("Something went wrong")
        assert str(e) == "Something went wrong"
        assert e.code == "DOMAIN_ERROR"

    def test_custom_code(self):
        e = DomainError("Custom error", code="CUSTOM")
        assert e.code == "CUSTOM"


class TestEntityNotFoundError:
    def test_message_format(self):
        e = EntityNotFoundError("User", "u123")
        assert "User" in str(e)
        assert "u123" in str(e)
        assert e.code == "ENTITY_NOT_FOUND"


class TestValidationError:
    def test_message_format(self):
        e = ValidationError("email", "invalid format")
        assert "email" in str(e)
        assert e.code == "VALIDATION_ERROR"


class TestScopeViolationError:
    def test_message_format(self):
        e = ScopeViolationError("10.0.0.1", "scope-1", "outside scope")
        assert "10.0.0.1" in str(e)
        assert e.code == "SCOPE_VIOLATION"


class TestAuthorizationError:
    def test_message_format(self):
        e = AuthorizationError("u1", "delete", "project/p1")
        assert "u1" in str(e)
        assert e.code == "AUTHORIZATION_ERROR"


class TestAssessmentStateError:
    def test_message_format(self):
        e = AssessmentStateError("a1", "draft", "in_progress")
        assert "a1" in str(e)
        assert "draft" in str(e)
        assert e.code == "ASSESSMENT_STATE_ERROR"


class TestToolExecutionError:
    def test_message_format(self):
        e = ToolExecutionError("nmap", 1, "error output")
        assert "nmap" in str(e)
        assert e.code == "TOOL_EXECUTION_ERROR"
