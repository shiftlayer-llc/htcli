"""
Chain information commands.
"""

import typer
from rich.console import Console
from ...utils.formatting import print_error, format_network_stats, format_account_info, format_epoch_info
from ...dependencies import get_client

app = typer.Typer(name="info", help="Chain information")
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
        # Use the proper RPC method according to documentation
        response = client.get_network_stats()

        if response.success:
            format_network_stats(response.data)
        else:
            print_error(f"Failed to get network stats: {response.message}")
            raise typer.Exit(1)
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
        # Use the balance method instead of get_account_info
        response = client.get_balance(address)

        if response.success:
            format_account_info(response.data)
        else:
            print_error(f"Failed to get account info: {response.message}")
            raise typer.Exit(1)
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
        # Use the proper RPC method according to documentation
        response = client.get_current_epoch()

        if response.success:
            format_epoch_info(response.data)
        else:
            print_error(f"Failed to get epoch info: {response.message}")
            raise typer.Exit(1)
    except Exception as e:
        print_error(f"Failed to get epoch info: {str(e)}")
        raise typer.Exit(1)
