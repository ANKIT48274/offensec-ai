"""Skill assessor — evaluates user proficiency based on assessment actions."""

from __future__ import annotations

from typing import Any


class SkillAssessor:
    def assess(self, actions: list[dict[str, Any]]) -> dict[str, Any]:
        if not actions:
            return {"level": "beginner", "score": 0, "strengths": [], "weaknesses": []}
        completed = sum(1 for a in actions if a.get("status") == "completed")
        successful = sum(1 for a in actions if a.get("result") == "success")
        accuracy = successful / max(completed, 1)
        if accuracy < 0.3:
            level = "beginner"
        elif accuracy < 0.6:
            level = "intermediate"
        else:
            level = "advanced"
        return {"level": level, "score": accuracy, "completed": completed, "successful": successful, "strengths": [], "weaknesses": []}
