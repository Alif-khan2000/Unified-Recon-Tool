import requests
from typing import Dict, Any, List

def http_probe(domain: str) -> Dict[str, Any]:
    url = f"http://{domain}"
    result: Dict[str, Any] = {
        "headers": {},
        "redirects": [],
        "cookies": [],
        "error": None,
    }
    try:
        r = requests.get(url, allow_redirects=True, timeout=7)
        result["headers"] = dict(r.headers)
        result["redirects"] = [h.url for h in r.history]
        cookies: List[dict] = []
        for c in r.cookies:
            cookies.append({
                "name": c.name,
                "httponly": c.has_nonstandard_attr('httponly'),
                "secure": c.secure,
                "expires": c.expires,
                "path": c.path
            })
        result["cookies"] = cookies
    except Exception as e:
        result["error"] = str(e)
    return result
