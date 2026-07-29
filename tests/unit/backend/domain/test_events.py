"""Tests for domain events."""

from backend.domain.events import (
    AssessmentCompleted,
    AssessmentStarted,
    DomainEvent,
    EventPriority,
    FindingCreated,
    ProjectCreated,
    ScopeViolationDetected,
)


class TestDomainEvent:
    def test_base_event(self):
        e = DomainEvent()
        assert e.event_id is not None
        assert e.version == 1

    def test_to_dict_contains_event_type(self):
        e = DomainEvent()
        data = e.to_dict()
        assert "event_type" in data
        assert data["version"] == 1


class TestProjectCreated:
    def test_event_data(self):
        e = ProjectCreated(project_id="p1", name="Test", owner_id="u1")
        assert e.project_id == "p1"
        data = e.to_dict()
        assert data["project_id"] == "p1"
        assert data["name"] == "Test"


class TestAssessmentStarted:
    def test_event_data(self):
        e = AssessmentStarted(assessment_id="a1", project_id="p1", scope_id="s1", started_by="u1")
        data = e.to_dict()
        assert data["assessment_id"] == "a1"


class TestAssessmentCompleted:
    def test_event_data(self):
        e = AssessmentCompleted(assessment_id="a1", project_id="p1", finding_count=5, critical_count=1)
        data = e.to_dict()
        assert data["finding_count"] == 5


class TestFindingCreated:
    def test_event_data(self):
        e = FindingCreated(finding_id="f1", assessment_id="a1", title="SQLi", severity="critical", target="host")
        assert e.priority == EventPriority.HIGH


class TestScopeViolationDetected:
    def test_critical_priority(self):
        e = ScopeViolationDetected(scope_id="s1", target="10.0.0.1", reason="outside", attempted_by="u1")
        assert e.priority == EventPriority.CRITICAL
