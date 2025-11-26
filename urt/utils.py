import socket
import subprocess
from typing import Any, List, Optional
from rich.console import Console

console = Console()

def safe_resolve(domain: str, record_type: str = "A") -> Optional[List[str]]:
    """Safely resolve DNS for the given domain and record type."""
    import dns.resolver
    try:
        answers = dns.resolver.resolve(domain, record_type, raise_on_no_answer=False)
        return [r.to_text() for r in answers]
    except Exception as e:
        console.print(f"[yellow]DNS resolve error for {domain} ({record_type}): {e}")
        return None

def run_subprocess(args: List[str], timeout: int = 30) -> dict[str, Any]:
    """Run a subprocess and capture output, returning dict with code, stdout, stderr."""
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return {
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr
        }
    except Exception as e:
        console.print(f"[yellow]Subprocess error: {e}")
        return {"returncode": -1, "stdout": "", "stderr": str(e)}
