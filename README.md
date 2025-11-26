# Unified Recon Tool (URT)

**Professional, CLI-first Reconnaissance Framework**  
_Python 3.10+, modular, robust, and ethical_

---

## Features
- Passive & Active Recon modules
- Modern CLI (Typer)
- Parallel or profile-driven enumeration
- Templated reporting (JSON/HTML)
- Built-in dependency checking, rich output, and progress bars
- *Ethics warning*: **Only scan authorized targets! Misuse may be illegal.**

## Installation
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
```

## Usage Example
```bash
python main.py example.com -m passive -o reports/example.com/recon.json
```

## Module Overview
- `dns`: DNS records (A, AAAA, MX, NS, TXT, PTR, CNAME, SOA), AXFR attempt
- `whois`: Registrar, creation/expiry, domain age
- `http`: Headers, redirects, cookie flags
- `tls`: CN, SAN, issuer, expiry days
- *Active Modules*: nmap, nikto, gobuster, whatweb (auto-skip if missing)

## Reporting
- JSON and HTML output under `reports/<target>/`

## Contributing / Testing
- See `tests/`, run `pytest`
- Lint via `flake8`
- CI: All PRs tested

---

## ETHICS WARNING
**URT is for use on authorized systems *only*. Scanning without permission is strictly prohibited and may constitute illegal activity.**
