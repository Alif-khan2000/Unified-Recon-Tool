import typer
from typing import Optional

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
    """Unified Recon Tool CLI entrypoint (skeleton)."""
    typer.echo(f"[URT] target={target} mode={mode} profile={profile} output={output} confirm={confirm} parallel={parallel}")
