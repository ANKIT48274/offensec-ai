"""Tests for asset merge logic."""


def _merge_ports(existing: list[dict], incoming: list[dict]) -> list[dict]:
    seen = {(p.get("port"), p.get("protocol")) for p in existing}
    merged = list(existing)
    for p in incoming:
        key = (p.get("port"), p.get("protocol"))
        if key not in seen:
            seen.add(key)
            merged.append(p)
    return merged


class TestMergePorts:
    def test_empty_lists(self):
        assert _merge_ports([], []) == []

    def test_new_ports_added(self):
        result = _merge_ports([], [{"port": "80", "protocol": "tcp"}])
        assert len(result) == 1
        assert result[0]["port"] == "80"

    def test_duplicate_not_added(self):
        existing = [{"port": "80", "protocol": "tcp"}]
        result = _merge_ports(existing, [{"port": "80", "protocol": "tcp"}])
        assert len(result) == 1

    def test_different_ports_merged(self):
        result = _merge_ports(
            [{"port": "80", "protocol": "tcp"}],
            [{"port": "443", "protocol": "tcp"}],
        )
        assert len(result) == 2

    def test_different_protocols(self):
        result = _merge_ports(
            [{"port": "53", "protocol": "tcp"}],
            [{"port": "53", "protocol": "udp"}],
        )
        assert len(result) == 2
