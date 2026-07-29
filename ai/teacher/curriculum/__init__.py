"""Curriculum manager — structures learning paths for skill development."""

from __future__ import annotations

from typing import Any


class CurriculumManager:
    def __init__(self) -> None:
        self._curricula = {
            "beginner": [
                {"topic": "port_scanning", "difficulty": 1},
                {"topic": "web_enumeration", "difficulty": 1},
                {"topic": "service_fingerprinting", "difficulty": 1},
                {"topic": "password_testing", "difficulty": 2},
                {"topic": "xss_detection", "difficulty": 2},
            ],
            "intermediate": [
                {"topic": "sql_injection", "difficulty": 3},
                {"topic": "privilege_escalation_linux", "difficulty": 3},
                {"topic": "active_directory_enumeration", "difficulty": 3},
                {"topic": "kerberos_attacks", "difficulty": 4},
                {"topic": "api_security_testing", "difficulty": 4},
            ],
            "advanced": [
                {"topic": "chain_exploitation", "difficulty": 5},
                {"topic": "domain_dominance", "difficulty": 5},
                {"topic": "evasion_techniques", "difficulty": 5},
            ],
        }

    def get_curriculum(self, level: str) -> list[dict[str, Any]]:
        return self._curricula.get(level, self._curricula["beginner"])

    def get_next_topics(self, completed: list[str], level: str) -> list[str]:
        curriculum = self.get_curriculum(level)
        return [t["topic"] for t in curriculum if t["topic"] not in completed]
