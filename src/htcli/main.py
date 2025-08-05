"""
Main CLI entry point for the Hypertensor CLI.
"""

import typer
from rich.console import Console
from pathlib import Path
from typing import Optional

from .commands.subnet import app as subnet_app
from .commands.wallet import app as wallet_app
from .commands.chain import app as chain_app
from .config import load_config
from .client import HypertensorClient
from .dependencies import set_client

app = typer.Typer(
    name="htcli",
    help="Hypertensor Blockchain CLI",
    add_completion=True,
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


# Include the three main command groups
app.add_typer(subnet_app, name="subnet", help="Subnet operations")
app.add_typer(wallet_app, name="wallet", help="Wallet operations")
app.add_typer(chain_app, name="chain", help="Chain operations")

if __name__ == "__main__":
    app()
