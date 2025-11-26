from urt.utils import safe_resolve
import dns.query
import dns.zone
from typing import Dict, Any

def dns_lookup(domain: str) -> Dict[str, Any]:
    """Perform DNS lookups for various record types and attempt AXFR."""
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "PTR", "CNAME", "SOA"]
    results = {}
    for rtype in record_types:
        res = safe_resolve(domain, rtype)
        results[rtype] = res if res is not None else []

    # Attempt AXFR (zone transfer) for each NS
    axfr_results = []
    ns_records = results.get("NS", [])
    for ns in ns_records:
        try:
            zone = dns.zone.from_xfr(dns.query.xfr(ns, domain, timeout=7))
            axfr_data = {n.to_text(): [r.to_text() for r in zone[n].rdatasets[0]] for n in zone.nodes.keys()}
            axfr_results.append({"server": ns, "zone": axfr_data})
        except Exception as e:
            axfr_results.append({"server": ns, "zone": None, "error": str(e)})
    results["AXFR"] = axfr_results
    return results
