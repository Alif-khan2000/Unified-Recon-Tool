import pytest
from urt.passive import tls as tls_mod

class DummySock:
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def settimeout(self, to): pass
    def connect(self, tup): pass
    def getpeercert(self):
        return {
            'subject': [[('commonName', 'test.local')]],
            'issuer': [[('commonName', 'TestCA')]],
            'subjectAltName': [('DNS', 'example.com')],
            'notAfter': 'Dec 31 23:59:59 2099 GMT'
        }
def test_tls_probe(monkeypatch):
    monkeypatch.setattr('ssl.create_default_context', lambda: type('X', (), {'wrap_socket': lambda self, sock, server_hostname: DummySock() })() )
    result = tls_mod.tls_probe('example.com')
    assert result['CN'] == 'test.local'
    assert result['issuer'] == 'TestCA'
    assert 'example.com' in result['SAN']
    assert result['days_until_expiry'] > 0
