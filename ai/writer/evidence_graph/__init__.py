"""Evidence graph — maps relationships between findings, targets, and evidence."""

from __future__ import annotations

from typing import Any


class EvidenceGraph:
    """Builds a directed graph of evidence relationships."""

    def build(self, findings: list[dict[str, Any]]) -> dict[str, Any]:
        nodes = []
        edges = []
        seen_targets: set[str] = set()

        for finding in findings:
            target = finding.get("target", "")
            node_id = finding.get("id", "")

            nodes.append(
                {
                    "id": node_id,
                    "type": "finding",
                    "label": finding.get("title", ""),
                    "severity": finding.get("severity", ""),
                }
            )

            if target and target not in seen_targets:
                seen_targets.add(target)
                nodes.append({"id": target, "type": "target", "label": target})
                edges.append({"source": node_id, "target": target, "relation": "affects"})

        return {"nodes": nodes, "edges": edges}
