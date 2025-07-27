"""
Staking operations commands.
"""

import typer
from rich.console import Console
from typing import Optional
from ...models.requests import StakeAddRequest, StakeRemoveRequest
from ...utils.validation import validate_amount, validate_address
from ...utils.formatting import print_success, print_error, create_stake_info_panel
from ...dependencies import get_client

app = typer.Typer(name="staking", help="Staking operations")
console = Console()


@app.command()
def add(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    node_id: int = typer.Argument(..., help="Subnet node ID"),
    amount: str = typer.Argument(..., help="Stake amount"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey account"),
    client = typer.Option(None, help="Client instance")
):
    """Add stake to a subnet node."""
    # Get client if not provided
    if client is None:
        client = get_client()

    # Validate inputs
    if not validate_amount(amount):
        print_error("Invalid stake amount. Must be a positive number.")
        raise typer.Exit(1)

    if not validate_address(hotkey):
        print_error("Invalid hotkey address format.")
        raise typer.Exit(1)

    try:
        # Convert amount to smallest unit
        amount_int = int(float(amount) * 1e9)  # Assuming 9 decimal places

        request = StakeAddRequest(
            subnet_id=subnet_id,
            subnet_node_id=node_id,
            hotkey=hotkey,
            stake_to_be_added=amount_int
        )

        response = client.add_stake(request)
        print_success(f"Added {amount} stake to subnet {subnet_id} successfully!")
        console.print(f"Transaction: {response.transaction_hash}")
    except Exception as e:
        print_error(f"Failed to add stake: {str(e)}")
        raise typer.Exit(1)


@app.command()
def remove(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    amount: str = typer.Argument(..., help="Stake amount to remove"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey account"),
    client = typer.Option(None, help="Client instance")
):
    """Remove stake from a subnet."""
    # Get client if not provided
    if client is None:
        client = get_client()

    # Validate inputs
    if not validate_amount(amount):
        print_error("Invalid stake amount. Must be a positive number.")
        raise typer.Exit(1)

    if not validate_address(hotkey):
        print_error("Invalid hotkey address format.")
        raise typer.Exit(1)

    try:
        amount_int = int(float(amount) * 1e9)

        request = StakeRemoveRequest(
            subnet_id=subnet_id,
            hotkey=hotkey,
            stake_to_be_removed=amount_int
        )

        response = client.remove_stake(request)
        print_success(f"Removed {amount} stake from subnet {subnet_id} successfully!")
        console.print(f"Transaction: {response.transaction_hash}")
    except Exception as e:
        print_error(f"Failed to remove stake: {str(e)}")
        raise typer.Exit(1)


@app.command()
def info(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey account"),
    client = typer.Option(None, help="Client instance")
):
    """Get stake information."""
    # Get client if not provided
    if client is None:
        client = get_client()

    try:
        response = client.get_stake_info(subnet_id, hotkey)

        if response.data:
            panel = create_stake_info_panel(response.data, subnet_id, hotkey)
            console.print(panel)
        else:
            console.print(f"No stake found for hotkey {hotkey} in subnet {subnet_id}.")

    except Exception as e:
        print_error(f"Failed to get stake info: {str(e)}")
        raise typer.Exit(1)
