import shutil
from urt.utils import run_subprocess
import xml.etree.ElementTree as ET

def nmap_scan(target: str) -> dict:
    """Run nmap against target. Parse summary from XML. Skip if nmap is missing."""
    if not shutil.which("nmap"):
        return {"status": "skipped (nmap missing)"}
    args = ["nmap", "-A", "-oX", "-", target]
    result = run_subprocess(args, timeout=120)
    if result["returncode"] != 0:
        return {"status": "error", "stderr": result["stderr"]}
    out = result["stdout"]
    try:
        # Parse the XML result for an overview
        root = ET.fromstring(out)
        ports = []
        for port in root.findall('.//port'):
            proto = port.get('protocol')
            num = port.get('portid')
            state = port.find('state').get('state') if port.find('state') is not None else ''
            name = ''
            if port.find('service') is not None:
                name = port.find('service').get('name', '')
            ports.append({"port": num, "protocol": proto, "state": state, "service": name})
        return {"status": "ok", "ports": ports}
    except Exception as e:
        return {"status": "ok-raw", "raw": out, "parse_error": str(e)}
