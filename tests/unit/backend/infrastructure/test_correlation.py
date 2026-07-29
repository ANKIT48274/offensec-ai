"""Tests for AI correlation engine."""

from backend.infrastructure.correlation.analyzer import (
    correlate,
    _analyze_attack_surface,
    _find_critical_assets,
    _rank_risks,
    _build_attack_paths,
    _detect_outdated,
    _detect_weak_protocols,
    _detect_exposed_services,
    _extract_tech_stack,
)


class TestAttackSurface:
    def test_empty(self):
        result = _analyze_attack_surface([])
        assert result["total_hosts"] == 0
        assert result["score"] == 10

    def test_counts_ports(self):
        assets = [{"ports": [{"port": "80", "state": "open"}, {"port": "443", "state": "open"}]}]
        result = _analyze_attack_surface(assets)
        assert result["total_ports"] == 2

    def test_high_risk_adds_score(self):
        assets = [{"ports": [{"port": "23", "state": "open"}]}]
        result = _analyze_attack_surface(assets)
        assert result["score"] > 10


class TestCriticalAssets:
    def test_no_critical(self):
        assert _find_critical_assets([], []) == []

    def test_nuclei_critical_found(self):
        assets = [{"value": "http://test.local", "asset_type": "url"}]
        nuclei = [{"severity": "critical", "matched_url": "http://test.local"}]
        result = _find_critical_assets(assets, nuclei)
        assert len(result) == 1
        assert "Critical vulnerability" in result[0]["reason"]

    def test_high_risk_port_found(self):
        assets = [{"value": "10.0.0.1", "ports": [{"port": "23"}]}]
        result = _find_critical_assets(assets, [])
        assert len(result) == 1


class TestRankRisks:
    def test_critical_first(self):
        nuclei = [{"severity": "low", "template_id": "low1"}, {"severity": "critical", "template_id": "crit1"}]
        result = _rank_risks(nuclei, [])
        assert len(result) == 2
        assert result[0]["severity"] == "critical"

    def test_empty_returns_empty(self):
        assert _rank_risks([], []) == []


class TestAttackPaths:
    def test_critical_creates_path(self):
        nuclei = [{"severity": "critical", "template_id": "RCE", "matched_url": "http://host", "template_name": "RCE", "description": "desc"}]
        result = _build_attack_paths([], nuclei)
        assert len(result) >= 1

    def test_low_does_not_create_path(self):
        nuclei = [{"severity": "low", "template_id": "info"}]
        result = _build_attack_paths([], nuclei)
        assert len(result) == 0


class TestDetectOutdated:
    def test_detects_openssh_7(self):
        assets = [{"ports": [{"service": "OpenSSH_7.9"}]}]
        result = _detect_outdated(assets, [])
        assert len(result) >= 1

    def test_detects_old_apache(self):
        httpx = [{"server": "Apache/2.4.6", "url": "http://test"}]
        result = _detect_outdated([], httpx)
        assert len(result) >= 1

    def test_modern_not_detected(self):
        httpx = [{"server": "nginx/1.26", "url": "http://test"}]
        result = _detect_outdated([], httpx)
        assert len(result) == 0


class TestDetectWeakProtocols:
    def test_ftp_detected(self):
        assets = [{"value": "10.0.0.1", "ports": [{"port": "21", "service": "ftp"}]}]
        result = _detect_weak_protocols(assets)
        assert len(result) == 1
        assert "ftp" in result[0]

    def test_ssh_not_weak(self):
        assets = [{"value": "10.0.0.1", "ports": [{"port": "22", "service": "ssh"}]}]
        result = _detect_weak_protocols(assets)
        assert len(result) == 0


class TestExposedServices:
    def test_smb_detected(self):
        assets = [{"value": "10.0.0.1", "ports": [{"port": "445", "service": "smb"}]}]
        result = _detect_exposed_services(assets)
        assert len(result) == 1

    def test_multiple_exposed(self):
        assets = [{"value": "10.0.0.1", "ports": [{"port": "445"}, {"port": "3389"}]}]
        result = _detect_exposed_services(assets)
        assert len(result) == 2


class TestTechStack:
    def test_returns_unique(self):
        assets = [{"technologies": ["React", "Node.js"]}, {"technologies": ["React", "Python"]}]
        result = _extract_tech_stack(assets)
        assert len(result) == 3

    def test_empty(self):
        assert _extract_tech_stack([]) == []


class TestCorrelate:
    def test_returns_dict_with_keys(self):
        result = correlate([], [], [], [])
        assert "executive_summary" in result
        assert "attack_surface" in result
        assert "top_risks" in result
        assert "recommendations" in result
        assert "risk_score" in result

    def test_risk_score_is_bounded(self):
        result = correlate([], [], [], [])
        assert 0 <= result["risk_score"] <= 100

    def test_recommendations_not_empty(self):
        result = correlate([], [], [], [])
        assert len(result["recommendations"]) > 0

    def test_nuclei_creates_recommendations(self):
        nuclei = [{"severity": "critical", "template_id": "RCE"}]
        result = correlate([], nuclei, [], [])
        critical_recs = [r for r in result["recommendations"] if "critical" in r.lower()]
        assert len(critical_recs) >= 1
