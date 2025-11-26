import shutil
import os
from urt.utils import run_subprocess

def gobuster_scan(target: str) -> dict:
    """Run gobuster dir scan if gobuster binary and a wordlist are present."""
    if not shutil.which("gobuster"):
        return {"status": "skipped (gobuster missing)"}
    wordlist = "/usr/share/wordlists/dirb/common.txt"
    if not os.path.isfile(wordlist):
        return {"status": "skipped (wordlist missing)", "wordlist": wordlist}
    url = f"http://{target}"
    args = ["gobuster", "dir", "-u", url, "-w", wordlist, "-q", "-r"]
    result = run_subprocess(args, timeout=120)
    if result["returncode"] != 0:
        return {"status": "error", "stderr": result["stderr"]}
    found = []
    # Parse the output: gobuster -q prints lines like /admin (Status: 301)
    for line in result["stdout"].splitlines():
        if line.startswith("/"):
            path = line.split()[0]
            found.append(path)
    return {"status": "ok", "found": found, "count": len(found)}
