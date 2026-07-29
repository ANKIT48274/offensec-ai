"""Plan scheduler — determines execution order and timing."""

from __future__ import annotations

from typing import Any


class PlanScheduler:
    """Schedules assessment plan steps based on dependencies and priorities."""

    def schedule(self, phases: list[dict[str, Any]]) -> list[dict[str, Any]]:
        schedule = []
        order = 0

        for phase in phases:
            for technique in phase.get("techniques", []):
                order += 1
                schedule.append(
                    {
                        "order": order,
                        "phase": phase.get("phase", ""),
                        "technique": technique,
                        "status": "pending",
                    }
                )

        return schedule
