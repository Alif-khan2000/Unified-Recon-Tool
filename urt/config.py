# Recon framework config profiles/defaults
def PROFILES():
    return {
        "quick": ["dns", "whois", "http"],
        "full": ["dns", "whois", "http", "tls", "nmap", "gobuster", "nikto", "whatweb"],
        "web": ["http", "tls", "whatweb"],
        "osint": ["dns", "whois"]
    }

DEFAULT_PROFILE = "quick"
REPORT_DIR = "reports"
