import pytest
from urt.passive import dns

@pytest.fixture
def mock_dns(monkeypatch):
    class DummyAns:
        def to_text(self):
            return "1.2.3.4"
    def fake_resolve(domain, record_type, **kwargs):
        return [DummyAns()]
    monkeypatch.setattr("dns.resolver.resolve", fake_resolve)
    yield

def test_dns_lookup_A(mock_dns):
    res = dns.dns_lookup("example.com")
    assert "A" in res
    assert any(r == "1.2.3.4" for r in res["A"])
