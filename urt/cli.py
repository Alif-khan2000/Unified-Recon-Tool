import typer
from typing import Optional
from urt.reporting.json_report import save_json_report

app = typer.Typer()

@app.command()
def main(
    target: str = typer.Argument(..., help="Target domain or IP"),
    mode: str = typer.Option("passive", "-m", help="Recon mode: passive/active/all"),
    profile: str = typer.Option(None, "-p", help="Recon profile: quick/full/web/osint"),
    output: Optional[str] = typer.Option(None, "-o", help="Output JSON report path"),
    confirm: bool = typer.Option(False, "--confirm", help="Confirm target and settings"),
    parallel: bool = typer.Option(False, "--parallel", help="Run modules in parallel")
):
    """Unified Recon Tool CLI entrypoint."""
    results = {}
    if mode == "passive":
        from urt.passive import dns, whois, http, tls
        results["dns"] = dns.dns_lookup(target)
        results["whois"] = whois.whois_lookup(target)
        results["http"] = http.http_probe(target)
        results["tls"] = tls.tls_probe(target)
        save_json_report(results, target, output)
        typer.echo(f"[URT] Passive recon complete. Report saved to {output or f'reports/{target}/recon.json'}")
    else:
        typer.echo(f"[URT] Mode '{mode}' not implemented yet.")
