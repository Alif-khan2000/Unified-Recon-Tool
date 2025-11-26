import shutil
from urt.utils import run_subprocess

def nikto_scan(target: str) -> dict:
    """Run nikto scan for basic web vulns. Skip if binary missing."""
    if not shutil.which("nikto"):
        return {"status": "skipped (nikto missing)"}
    url = f"http://{target}"
    args = ["nikto", "-host", url, "-nointeractive", "-Cgidirs", "all", "-Display", "V"]
    result = run_subprocess(args, timeout=120)
    if result["returncode"] != 0:
        return {"status": "error", "stderr": result["stderr"]}
    # Nikto prints many findings as lines; extract basic info
    findings = []
    for line in result["stdout"].splitlines():
        if line.startswith("+") and not line.startswith("+ Target"):
            findings.append(line[2:].strip())
    return {"status": "ok", "findings": findings, "count": len(findings)}
