"""Evidence correlator — links related findings across different sources."""

from __future__ import annotations

from typing import Any


class EvidenceCorrelator:
    """Correlates evidence from multiple sources to build unified findings."""

    async def correlate(self, evidence_set: list[dict[str, Any]]) -> list[dict[str, Any]]:
        correlated = []
        grouped: dict[str, list[dict[str, Any]]] = {}

        for evidence in evidence_set:
            target = evidence.get("target", "unknown")
            if target not in grouped:
                grouped[target] = []
            grouped[target].append(evidence)

        for target, items in grouped.items():
            services = [i.get("service", "") for i in items if i.get("service")]
            ports = [i.get("port") for i in items if i.get("port")]
            vulnerabilities = [i for i in items if i.get("type") == "vulnerability"]

            correlated.append(
                {
                    "target": target,
                    "services": list(set(services)),
                    "ports": sorted(set(ports)),
                    "vulnerability_count": len(vulnerabilities),
                    "confidence": min(1.0, len(items) * 0.1 + 0.3),
                }
            )

        return correlated
