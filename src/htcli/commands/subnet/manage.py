"""
Subnet management commands.
"""

import typer
from rich.console import Console
from typing import Optional
from ...utils.formatting import print_error, create_subnet_table
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
        response = client.list_subnets(active_only=active_only)

        if response.data and response.data.get("subnets"):
            table = create_subnet_table(response.data["subnets"])
            console.print(table)

            if response.data.get("total_count"):
                console.print(f"\nTotal Subnets: {response.data['total_count']}")
                if active_only and response.data.get("active_count"):
                    console.print(f"Active Subnets: {response.data['active_count']}")
        else:
            console.print("No subnets found.")

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
        response = client.get_subnet_info(subnet_id)

        if response.data:
            from rich.panel import Panel
            info_text = f"""
Subnet ID: {subnet_id}
Path: {response.data.get('path', 'N/A')}
Status: {'Active' if response.data.get('activated', 0) > 0 else 'Inactive'}
Registration Cost: {response.data.get('registration_cost', 'N/A')}
Node Count: {response.data.get('node_count', 0)}
Total Stake: {response.data.get('total_stake', 0)}
Memory: {response.data.get('memory_mb', 0)} MB
Registration Blocks: {response.data.get('registration_blocks', 0)}
Entry Interval: {response.data.get('entry_interval', 0)}
            """
            console.print(Panel(info_text, title="Subnet Information"))
        else:
            console.print(f"Subnet {subnet_id} not found.")

    except Exception as e:
        print_error(f"Failed to get subnet info: {str(e)}")
        raise typer.Exit(1)
