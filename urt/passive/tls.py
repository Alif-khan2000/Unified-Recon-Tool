import ssl
import socket
from typing import Dict, Any
from datetime import datetime

def tls_probe(domain: str, port: int = 443) -> Dict[str, Any]:
    result = {"CN": None, "SAN": [], "issuer": None, "days_until_expiry": None, "error": None}
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(7)
            s.connect((domain, port))
            cert = s.getpeercert()
            result["CN"] = cert.get("subject", [[("commonName", None)]])[0][0][1]
            result["issuer"] = cert.get("issuer", [[("commonName", None)]])[0][0][1]
            # SAN
            for ext in cert.get("subjectAltName", []):
                if ext[0] == "DNS":
                    result["SAN"].append(ext[1])
            # Expiry
            not_after = cert.get("notAfter")
            if not_after:
                expires = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                days = (expires - datetime.utcnow()).days
                result["days_until_expiry"] = days
    except Exception as e:
        result["error"] = str(e)
    return result
