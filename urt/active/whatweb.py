import shutil
from urt.utils import run_subprocess

def whatweb_scan(target: str) -> dict:
    """Fingerprint website using whatweb. Skip if binary missing."""
    if not shutil.which("whatweb"):
        return {"status": "skipped (whatweb missing)"}
    url = f"http://{target}"
    args = ["whatweb", url, "--no-errors"]
    result = run_subprocess(args, timeout=60)
    if result["returncode"] != 0:
        return {"status": "error", "stderr": result["stderr"]}
    # Parse plugins from WhatWeb's output (format: <url> [Plugins])
    lines = result["stdout"].splitlines()
    plugins = []
    if lines:
        parts = lines[-1].split("[", 1)
        if len(parts) > 1 and parts[1].endswith("]"):
            plugins = [x.strip() for x in parts[1][:-1].split(",")]
    return {"status": "ok", "plugins": plugins, "count": len(plugins)}
