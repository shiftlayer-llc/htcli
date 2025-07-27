"""
Subnet node operations commands.
"""

import typer
from rich.console import Console
from typing import Optional
from ...models.requests import SubnetNodeAddRequest
from ...utils.validation import validate_peer_id, validate_address
from ...utils.formatting import print_success, print_error, create_node_table
from ...dependencies import get_client

app = typer.Typer(name="nodes", help="Subnet node operations")
console = Console()


@app.command()
def add(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    peer_id: str = typer.Argument(..., help="Peer ID"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey account"),
    client = typer.Option(None, help="Client instance")
):
    """Add a node to a subnet."""
    # Get client if not provided
    if client is None:
        client = get_client()

    # Validate inputs
    if not validate_peer_id(peer_id):
        print_error("Invalid peer ID format. Should be a valid MultiHash.")
        raise typer.Exit(1)

    if not validate_address(hotkey):
        print_error("Invalid hotkey address format.")
        raise typer.Exit(1)

    try:
        request = SubnetNodeAddRequest(
            subnet_id=subnet_id,
            peer_id=peer_id,
            hotkey=hotkey
        )

        response = client.add_subnet_node(request)
        print_success(f"Node added to subnet {subnet_id} successfully!")
        console.print(f"Transaction: {response.transaction_hash}")
    except Exception as e:
        print_error(f"Failed to add node: {str(e)}")
        raise typer.Exit(1)


@app.command()
def list(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    client = typer.Option(None, help="Client instance")
):
    """List nodes in a subnet."""
    # Get client if not provided
    if client is None:
        client = get_client()

    try:
        response = client.get_subnet_nodes(subnet_id)

        if response.data and response.data.get("nodes"):
            table = create_node_table(response.data["nodes"], subnet_id)
            console.print(table)

            if response.data.get("total_nodes"):
                console.print(f"\nTotal Nodes: {response.data['total_nodes']}")
                if response.data.get("total_stake"):
                    from ...utils.formatting import format_balance
                    console.print(f"Total Stake: {format_balance(response.data['total_stake'])}")
        else:
            console.print(f"No nodes found in subnet {subnet_id}.")

    except Exception as e:
        print_error(f"Failed to list nodes: {str(e)}")
        raise typer.Exit(1)
