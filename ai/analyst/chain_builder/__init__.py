"""Attack chain builder — constructs multi-step attack paths."""

from __future__ import annotations

from typing import Any


class AttackChainBuilder:
    """Builds multi-step attack chains from individual findings."""

    async def build_chains(
        self, findings: list[dict[str, Any]], paths: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        chains = []

        for path in paths:
            chain = {
                "source": path.get("source_target", ""),
                "destination": path.get("destination_target", ""),
                "technique": path.get("technique", ""),
                "technique_id": path.get("technique_id", ""),
                "prerequisites": path.get("prerequisites", []),
                "tools": path.get("tools", []),
                "related_findings": [],
            }

            for finding in findings:
                target = finding.get("target", "")
                if target == chain["destination"] or target == chain["source"]:
                    chain["related_findings"].append(
                        {
                            "id": finding.get("id", ""),
                            "title": finding.get("title", ""),
                            "severity": finding.get("severity", ""),
                        }
                    )

            chains.append(chain)

        return chains
