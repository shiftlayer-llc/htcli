"""
Chain information commands.
"""

import typer
from rich.console import Console
from typing import Optional
from ...utils.formatting import print_error, create_network_stats_panel, create_account_info_panel, create_epoch_info_panel
from ...dependencies import get_client

app = typer.Typer(name="info", help="Chain information commands")
console = Console()


@app.command()
def network(
    client = typer.Option(None, help="Client instance")
):
    """Get network statistics."""
    # Get client if not provided
    if client is None:
        client = get_client()

    try:
        response = client.get_network_stats()

        if response.data:
            panel = create_network_stats_panel(response.data)
            console.print(panel)
        else:
            console.print("No network statistics available.")

    except Exception as e:
        print_error(f"Failed to get network stats: {str(e)}")
        raise typer.Exit(1)


@app.command()
def account(
    address: str = typer.Argument(..., help="Account address"),
    client = typer.Option(None, help="Client instance")
):
    """Get account information."""
    # Get client if not provided
    if client is None:
        client = get_client()

    try:
        response = client.get_account_info(address)

        if response.data:
            panel = create_account_info_panel(response.data, address)
            console.print(panel)
        else:
            console.print(f"Account {address} not found.")

    except Exception as e:
        print_error(f"Failed to get account info: {str(e)}")
        raise typer.Exit(1)


@app.command()
def epoch(
    client = typer.Option(None, help="Client instance")
):
    """Get current epoch information."""
    # Get client if not provided
    if client is None:
        client = get_client()

    try:
        response = client.get_current_epoch()

        if response.data:
            panel = create_epoch_info_panel(response.data)
            console.print(panel)
        else:
            console.print("No epoch information available.")

    except Exception as e:
        print_error(f"Failed to get epoch info: {str(e)}")
        raise typer.Exit(1)
