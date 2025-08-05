"""
Subnet management commands.
"""

import typer
from rich.console import Console
from typing import Optional
from ...utils.formatting import print_success, print_error, format_subnet_list, format_subnet_info
from ...dependencies import get_client

app = typer.Typer(name="manage", help="Subnet management commands")
console = Console()


@app.command()
def list(
    active_only: bool = typer.Option(False, "--active", "-a", help="Show only active subnets"),
    client = typer.Option(None, help="Client instance")
):
    """List all subnets."""
    # Get client if not provided
    if client is None:
        client = get_client()

    try:
        # Use the proper RPC method according to documentation
        response = client.get_subnets_data(active_only)

        if response.success:
            format_subnet_list(response.data.get("subnets", []))
        else:
            print_error(f"Failed to list subnets: {response.message}")
            raise typer.Exit(1)
    except Exception as e:
        print_error(f"Failed to list subnets: {str(e)}")
        raise typer.Exit(1)


@app.command()
def info(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    client = typer.Option(None, help="Client instance")
):
    """Get detailed subnet information."""
    # Get client if not provided
    if client is None:
        client = get_client()

    try:
        # Use the proper RPC method according to documentation
        response = client.get_subnet_data(subnet_id)

        if response.success:
            format_subnet_info(response.data.get("subnet_info", {}))
        else:
            print_error(f"Failed to get subnet info: {response.message}")
            raise typer.Exit(1)
    except Exception as e:
        print_error(f"Failed to get subnet info: {str(e)}")
        raise typer.Exit(1)
