from typing import Dict, Any
import whois
from datetime import datetime

def whois_lookup(domain: str) -> Dict[str, Any]:
    try:
        w = whois.whois(domain)
        registrar = w.registrar
        creation_date = str(w.creation_date) if w.creation_date else None
        expiration_date = str(w.expiration_date) if w.expiration_date else None
        domain_age = None
        if w.creation_date:
            age = (datetime.utcnow() - w.creation_date if isinstance(w.creation_date, datetime) else 
                   datetime.utcnow() - w.creation_date[0])
            domain_age = age.days
        return {
            "registrar": registrar,
            "creation_date": creation_date,
            "expiration_date": expiration_date,
            "domain_age_days": domain_age
        }
    except Exception as e:
        return {"error": str(e)}
