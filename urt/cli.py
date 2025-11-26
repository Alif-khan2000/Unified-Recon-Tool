import typer
from typing import Optional
from urt.reporting.json_report import save_json_report
from urt.reporting.html_report import save_html_report
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()

@app.command()
def main(
    target: str = typer.Argument(..., help="Target domain or IP"),
    mode: str = typer.Option("passive", "-m", help="Recon mode: passive/active/all"),
    profile: str = typer.Option(None, "-p", help="Recon profile: quick/full/web/osint"),
    output: Optional[str] = typer.Option(None, "-o", help="Output JSON report path"),
    confirm: bool = typer.Option(False, "--confirm", help="Confirm target and settings"),
    parallel: bool = typer.Option(False, "--parallel", help="Run modules in parallel"),
    verbose: bool = typer.Option(False, "--verbose", help="Verbose output in terminal")
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
        html_path = save_html_report(results, target)
        typer.echo(f"[URT] Passive recon complete. Reports saved to {output or f'reports/{target}/recon.json'} and {html_path}")
    elif mode == "active":
        from urt.active import nmap_wrapper, gobuster, nikto, whatweb
        results["nmap"] = nmap_wrapper.nmap_scan(target)
        results["gobuster"] = gobuster.gobuster_scan(target)
        results["nikto"] = nikto.nikto_scan(target)
        results["whatweb"] = whatweb.whatweb_scan(target)
        save_json_report(results, target, output)
        html_path = save_html_report(results, target)
        if all(str(r.get('status', ''))[:7] == 'skipped' for r in results.values()):
            typer.echo(f"[URT] All active modules skipped (binaries missing or not implemented). Reports saved to {output or f'reports/{target}/recon.json'} and {html_path}")
        else:
            typer.echo(f"[URT] Active recon complete. Reports saved to {output or f'reports/{target}/recon.json'} and {html_path}")
    else:
        typer.echo(f"[URT] Mode '{mode}' not implemented yet.")

    if verbose:
        console.rule("[bold cyan]Recon Results")
        for module, res in results.items():
            if module == "nmap" and res.get("ports"):
                table = Table(title="Nmap Open Ports/Services")
                table.add_column("Port")
                table.add_column("Proto")
                table.add_column("Service")
                table.add_column("Status")
                for port in res["ports"]:
                    table.add_row(str(port["port"]), port["protocol"], port["service"], port["state"])
                console.print(table)
            elif module == "gobuster" and res.get("found"):
                table = Table(title="Gobuster Found Paths")
                table.add_column("Path")
                for path in res["found"]:
                    table.add_row(path)
                console.print(table)
            elif module == "nikto" and res.get("findings"):
                table = Table(title="Nikto Vulnerabilities")
                table.add_column("Finding")
                for f in res["findings"]:
                    table.add_row(f)
                console.print(table)
            elif module == "whatweb" and res.get("plugins"):
                table = Table(title="WhatWeb Plugins")
                table.add_column("Plugin/Tech")
                for p in res["plugins"]:
                    table.add_row(p)
                console.print(table)
            elif module == "dns" and (res.get("A") or res.get("MX") or res.get("NS")):
                table = Table(title="DNS Records")
                table.add_column("Type")
                table.add_column("Value")
                for rtype in ["A", "AAAA", "MX", "NS", "TXT", "PTR", "CNAME", "SOA"]:
                    if res.get(rtype):
                        table.add_row(rtype, str(res[rtype]))
                console.print(table)
            elif module == "whois" and res.get("registrar"):
                table = Table(title="Whois Info")
                table.add_column("Registrar")
                table.add_column("Created")
                table.add_column("Expires")
                table.add_column("Domain Age (d)")
                table.add_row(str(res.get("registrar")), str(res.get("creation_date")), str(res.get("expiration_date")), str(res.get("domain_age_days")))
                console.print(table)
            elif module == "tls" and res.get("CN"):
                table = Table(title="TLS Cert Info")
                table.add_column("CN")
                table.add_column("Issuer")
                table.add_column("SAN")
                table.add_column("Days till Expiry")
                table.add_row(str(res.get("CN")), str(res.get("issuer")), ", ".join(res.get("SAN", [])), str(res.get("days_until_expiry")))
                console.print(table)
            else:
                console.print(f"[bold yellow]{module.capitalize()}:[/bold yellow] ", res)
