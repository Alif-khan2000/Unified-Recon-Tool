import pytest
from urt.passive import http as http_mod

class DummyResp:
    headers = {'Server': 'nginx'}
    history = []
    cookies = []

def test_http_probe(monkeypatch):
    def fake_get(url, allow_redirects=True, timeout=7):
        return DummyResp()
    monkeypatch.setattr('requests.get', fake_get)
    out = http_mod.http_probe('example.com')
    assert out['headers']['Server'] == 'nginx'
