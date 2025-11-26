import pytest
from urt.passive import whois

class DummyWhois:
    registrar = 'TestRegistrar'
    creation_date = None
    expiration_date = None

def test_whois_lookup(monkeypatch):
    def fake_whois(domain):
        c = DummyWhois()
        c.creation_date = __import__('datetime').datetime(2020, 1, 1)
        c.expiration_date = __import__('datetime').datetime(2030, 1, 1)
        return c
    monkeypatch.setattr('whois.whois', fake_whois)
    results = whois.whois_lookup('example.com')
    assert results['registrar'] == 'TestRegistrar'
    assert results['creation_date'].startswith('2020')
    assert results['expiration_date'].startswith('2030')
