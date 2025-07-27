"""
Main CLI entry point for the Hypertensor CLI.
"""

import typer
from rich.console import Console
from pathlib import Path
from typing import Optional

from .commands.subnet import register, manage, nodes
from .commands.wallet import keys, staking
from .commands.chain import info, query
from .config import load_config
from .client import HypertensorClient
from .dependencies import set_client

app = typer.Typer(
    name="htcli",
    help="Hypertensor Blockchain CLI",
    add_completion=False,
    rich_markup_mode="rich"
)

console = Console()

# Global configuration
config = None


@app.callback()
def main(
    config_file: Optional[Path] = typer.Option(
        None, "--config", "-c", help="Configuration file path"
    ),
    endpoint: Optional[str] = typer.Option(
        None, "--endpoint", "-e", help="Blockchain endpoint"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    output_format: str = typer.Option("table", "--format", "-f", help="Output format (table/json/csv)")
):
    """Hypertensor Blockchain CLI - Manage subnets, wallets, and chain operations."""
    global config

    # Load configuration
    config = load_config(config_file)

    # Override endpoint if provided
    if endpoint:
        config.network.endpoint = endpoint

    # Initialize client
    client = HypertensorClient(config)
    set_client(client)

    # Set global options
    config.output.verbose = verbose
    config.output.format = output_format


# Include subnet command modules
app.add_typer(register.app, name="register", help="Subnet registration")
app.add_typer(manage.app, name="manage", help="Subnet management")
app.add_typer(nodes.app, name="nodes", help="Subnet node operations")

# Include wallet command modules
app.add_typer(keys.app, name="keys", help="Key management")
app.add_typer(staking.app, name="stake", help="Staking operations")

# Include chain command modules
app.add_typer(info.app, name="info", help="Chain information")
app.add_typer(query.app, name="query", help="Data queries")

if __name__ == "__main__":
    app()
