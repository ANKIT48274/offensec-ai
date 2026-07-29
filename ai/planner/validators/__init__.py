"""Plan validation — scope enforcement, feasibility checks, and safety gates."""

from __future__ import annotations

from typing import Any


class PlanValidator:
    """Validates assessment plans against scope and constraints."""

    async def validate_scope(self, plan: list[dict[str, Any]], scope: dict[str, Any]) -> tuple[bool, list[str]]:
        violations = []
        allowed_techniques = set(scope.get("techniques", []))

        if allowed_techniques:
            for step in plan:
                for technique in step.get("techniques", []):
                    if technique not in allowed_techniques:
                        violations.append(f"Technique '{technique}' is outside allowed scope")

        is_valid = len(violations) == 0
        return is_valid, violations

    async def validate_dependencies(self, plan: list[dict[str, Any]]) -> tuple[bool, list[str]]:
        errors = []
        seen = set()

        for step in plan:
            for technique in step.get("techniques", []):
                if technique in seen:
                    errors.append(f"Duplicate technique: {technique}")
                seen.add(technique)

        return len(errors) == 0, errors
