# Unified Recon Tool (URT)

**Professional, CLI-first Reconnaissance Framework**  
_Python 3.10+, modular, robust, and ethical_

---

## Features
- Passive & Active Recon modules
- Modern CLI (Typer)
- Profile-driven or ad-hoc module selection
- Parallel scanning option (future)
- Automated JSON/HTML reporting
- Dependency checking & auto-skip for missing binaries
- Modular, extensible, and fully documented
- **Ethics warning**: Only scan authorized targets! Misuse may be illegal.

## Installation
```
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
```

---

## Usage

### General CLI Pattern
```
python main.py <target> [OPTIONS]
```

### Required Arguments
- `<target>`: Domain name or IP address to scan.

### Main Options
- `-m`, `--mode`: Recon mode. Choices: `passive`, `active`, `all`. Default: `passive`.
- `-o`, `--output`: Output report file (default: reports/<target>/recon.json)
- `-p`, `--profile`: Run a module profile. Choices: `quick`, `full`, `web`, `osint` (future: custom).
- `--confirm`: Show recon plan and require confirmation (future).
- `--parallel`: Scan modules in parallel (stub, future).

### Example Commands
**Passive scan:**
```
python main.py example.com -m passive -o reports/example.com/recon.json
```
**Active scan:**
```
python main.py 192.168.1.6 -m active  -o reports/metasploitable/recon.json
```
**Profile (future, toggles a set of modules):**
```
python main.py target.com -p full
```

---

## Module Functionalities

### Passive Recon (`-m passive`):
- **dns**: Lookup all standard records (A, AAAA, MX, NS, TXT, PTR, CNAME, SOA); attempts zone transfer (AXFR) on all detected NS records. Uses `dnspython`.
- **whois**: Extract domain registrar, creation and expiry dates, calculates domain age. Uses `python-whois`.
- **http**: Fetches HTTP headers, tracks redirect chains, lists cookies and security-related flags. Uses `requests`.
- **tls**: Pulls X.509 certificate info (CN, SAN, Issuer, days until expiry). Uses Python's `ssl`.

### Active Recon (`-m active`):
- **nmap**: Full version/enumeration scan (`nmap -A`) with XML parsing. Requires `nmap` binary.
- **gobuster**: Directory brute-force (`gobuster dir`), uses wordlist `/usr/share/wordlists/dirb/common.txt` by default. Requires `gobuster` and the wordlist.
- **nikto**: Web vulnerability scan. Reports found issues. Requires `nikto`.
- **whatweb**: Web fingerprinting/tech detection. Reports detected plugins. Requires `whatweb`.
- *If a required binary or wordlist is missing, the tool is skipped and noted in the report with status info.*

---

## Output & Reporting
- Output: JSON report at the specified path (default: reports/<target>/recon.json)
- Example report keys:
    - `dns`, `whois`, `http`, `tls`, `nmap`, `gobuster`, `nikto`, `whatweb`
- Each key contains:
    - `status`: "ok" if module ran successfully; "skipped (reason)" or "error" otherwise
    - Module-specific data (e.g., open ports, hosts, plugins, findings, records)
- HTML report support planned (`urt/reporting/html_report.py`, Jinja2 template)

---

## Dependency & Binary Checking
- `scripts/check_deps.sh`: Checks for required binaries (nmap, gobuster, nikto, whatweb)
- Missing tools or wordlists are noted directly in JSON output.
- All modules return JSON-serializable results. No run-ever exceptions by missing binaries.

---

## Contributing, Testing & CI
- Unit tests (with mock) in `tests/`; run using `pytest`
- Lint with `flake8`
- GitHub Actions (CI): Lint + test on push/pull-request

---

## ETHICS WARNING
**URT is for use on authorized systems only. Scanning without permission is strictly prohibited and may constitute illegal activity.**
