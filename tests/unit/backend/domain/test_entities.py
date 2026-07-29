"""Tests for domain entities."""

from backend.domain.entities import Assessment, Finding, Project, User
from backend.domain.value_objects import AssessmentStatus, Confidence, FindingStatus, Severity


class TestUser:
    def test_create_user(self):
        user = User(email="test@example.com", username="testuser", password_hash="hashed")
        assert user.email == "test@example.com"
        assert user.is_active is True
        assert user.is_superuser is False

    def test_to_dict(self):
        user = User(id="u1", email="a@b.com", username="a")
        data = user.to_dict()
        assert data["id"] == "u1"
        assert data["email"] == "a@b.com"


class TestProject:
    def test_create_project(self):
        project = Project(name="Test Project", description="Desc", owner_id="u1")
        assert project.name == "Test Project"
        assert project.is_archived is False

    def test_to_dict(self):
        p = Project(id="p1", name="P", owner_id="u1")
        data = p.to_dict()
        assert data["id"] == "p1"
        assert data["name"] == "P"


class TestAssessment:
    def test_initial_state(self):
        a = Assessment(name="Test", project_id="p1")
        assert a.status == AssessmentStatus.DRAFT

    def test_start(self):
        a = Assessment(name="Test", project_id="p1")
        a.start()
        assert a.status == AssessmentStatus.IN_PROGRESS
        assert a.started_at is not None

    def test_complete(self):
        a = Assessment(name="Test", project_id="p1")
        a.start()
        a.complete()
        assert a.status == AssessmentStatus.COMPLETED
        assert a.completed_at is not None

    def test_pause(self):
        a = Assessment(name="Test", project_id="p1")
        a.start()
        a.pause()
        assert a.status == AssessmentStatus.PAUSED


class TestFinding:
    def test_create_finding(self):
        f = Finding(
            assessment_id="a1",
            title="SQL Injection",
            severity=Severity.CRITICAL,
            confidence=Confidence.HIGH,
            target="192.168.1.1",
        )
        assert f.title == "SQL Injection"
        assert f.severity == Severity.CRITICAL
        assert f.status == FindingStatus.OPEN

    def test_to_dict(self):
        f = Finding(id="f1", assessment_id="a1", title="XSS")
        data = f.to_dict()
        assert data["id"] == "f1"
        assert data["title"] == "XSS"
        assert data["severity"] == "none"

    def test_with_evidence(self):
        f = Finding(
            assessment_id="a1",
            title="Test",
            evidence=[{"type": "command_output", "source": "nmap", "content": "output"}],
        )
        assert len(f.evidence) == 1
