"""Tests for domain value objects."""

import pytest

from backend.domain.exceptions import ValidationError
from backend.domain.value_objects import (
    CIDR,
    URL,
    AttackPath,
    Credential,
    Hostname,
    IPAddress,
    Port,
    ScopeDefinition,
    Severity,
)


class TestSeverity:
    def test_score_mapping(self):
        assert Severity.NONE.score == 0
        assert Severity.LOW.score == 1
        assert Severity.MEDIUM.score == 2
        assert Severity.HIGH.score == 3
        assert Severity.CRITICAL.score == 4

    def test_from_cvss(self):
        assert Severity.from_cvss(0.0) == Severity.NONE
        assert Severity.from_cvss(3.9) == Severity.LOW
        assert Severity.from_cvss(6.9) == Severity.MEDIUM
        assert Severity.from_cvss(8.9) == Severity.HIGH
        assert Severity.from_cvss(10.0) == Severity.CRITICAL


class TestIPAddress:
    def test_valid_ipv4(self):
        ip = IPAddress("192.168.1.1")
        assert ip.version == 4

    def test_valid_ipv6(self):
        ip = IPAddress("::1")
        assert ip.version == 6

    def test_invalid_ip(self):
        with pytest.raises(ValidationError):
            IPAddress("not_an_ip")

    def test_private_detection(self):
        assert IPAddress("10.0.0.1").is_private is True
        assert IPAddress("8.8.8.8").is_private is False


class TestCIDR:
    def test_valid_cidr(self):
        cidr = CIDR("192.168.1.0/24")
        assert cidr.contains(IPAddress("192.168.1.50"))

    def test_excludes_outside_range(self):
        cidr = CIDR("192.168.1.0/24")
        assert not cidr.contains(IPAddress("10.0.0.1"))

    def test_invalid_cidr(self):
        with pytest.raises(ValidationError):
            CIDR("invalid")


class TestPort:
    def test_valid_port(self):
        p = Port(80)
        assert p.number == 80

    def test_port_too_low(self):
        with pytest.raises(ValidationError):
            Port(0)

    def test_port_too_high(self):
        with pytest.raises(ValidationError):
            Port(65536)

    def test_invalid_protocol(self):
        with pytest.raises(ValidationError):
            Port(80, protocol="icmp")


class TestHostname:
    def test_valid_hostname(self):
        h = Hostname("example.com")
        assert h.value == "example.com"

    def test_invalid_hostname(self):
        with pytest.raises(ValidationError):
            Hostname("not_a_hostname_!")


class TestURL:
    def test_valid_url(self):
        u = URL("https://example.com/path")
        assert u.hostname == "example.com"

    def test_invalid_url(self):
        with pytest.raises(ValidationError):
            URL("not_a_url")


class TestCredential:
    def test_valid_credential(self):
        c = Credential(username="admin", password="secret")
        assert c.username == "admin"

    def test_empty_credential(self):
        with pytest.raises(ValidationError):
            Credential()


class TestScopeDefinition:
    def test_includes_target(self):
        scope = ScopeDefinition(targets=["192.168.1.1"])
        assert scope.includes("192.168.1.1") is True

    def test_excludes_target(self):
        scope = ScopeDefinition(targets=["192.168.1.1"], excluded_targets=["192.168.1.1"])
        assert scope.includes("192.168.1.1") is False


class TestAttackPath:
    def test_to_dict(self):
        path = AttackPath(source_target="host1", destination_target="host2", technique="SMB")
        data = path.to_dict()
        assert data["source_target"] == "host1"
        assert data["technique"] == "SMB"
