"""
Wallet staking operations.
"""

import typer
from rich.console import Console
from typing import Optional
from ...models.requests import StakeAddRequest, StakeRemoveRequest
from ...utils.validation import validate_address, validate_amount
from ...utils.formatting import print_success, print_error, format_stake_info
from ...dependencies import get_client

app = typer.Typer(name="stake", help="Staking operations")
console = Console()


@app.command()
def add(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    node_id: int = typer.Argument(..., help="Node ID"),
    amount: float = typer.Argument(..., help="Stake amount in TENSOR"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey account address"),
    client = typer.Option(None, help="Client instance")
):
    """Add stake to a subnet node."""
    # Get client if not provided
    if client is None:
        client = get_client()

    # Validate inputs
    if not validate_address(hotkey):
        print_error("Invalid hotkey address format.")
        raise typer.Exit(1)

    if not validate_amount(amount):
        print_error("Invalid stake amount. Must be a positive number.")
        raise typer.Exit(1)

    try:
        # Convert amount to smallest unit (assuming 12 decimals)
        stake_amount = int(amount * 1e12)

        request = StakeAddRequest(
            subnet_id=subnet_id,
            node_id=node_id,
            hotkey=hotkey,
            stake_to_be_added=stake_amount
        )

        # Use the proper RPC method according to documentation
        response = client.add_to_stake(request)

        if response.success:
            print_success(f"Added {amount} stake to subnet {subnet_id} successfully!")
            if response.transaction_hash:
                console.print(f"Transaction: {response.transaction_hash}")
        else:
            print_error(f"Failed to add stake: {response.message}")
            raise typer.Exit(1)
    except Exception as e:
        print_error(f"Failed to add stake: {str(e)}")
        raise typer.Exit(1)


@app.command()
def remove(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    amount: float = typer.Argument(..., help="Stake amount to remove in TENSOR"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey account address"),
    client = typer.Option(None, help="Client instance")
):
    """Remove stake from a subnet."""
    # Get client if not provided
    if client is None:
        client = get_client()

    # Validate inputs
    if not validate_address(hotkey):
        print_error("Invalid hotkey address format.")
        raise typer.Exit(1)

    if not validate_amount(amount):
        print_error("Invalid stake amount. Must be a positive number.")
        raise typer.Exit(1)

    try:
        # Convert amount to smallest unit (assuming 12 decimals)
        stake_amount = int(amount * 1e12)

        request = StakeRemoveRequest(
            subnet_id=subnet_id,
            hotkey=hotkey,
            stake_to_be_removed=stake_amount
        )

        # Use the proper RPC method according to documentation
        response = client.remove_stake(request)

        if response.success:
            print_success(f"Removed {amount} stake from subnet {subnet_id} successfully!")
            if response.transaction_hash:
                console.print(f"Transaction: {response.transaction_hash}")
        else:
            print_error(f"Failed to remove stake: {response.message}")
            raise typer.Exit(1)
    except Exception as e:
        print_error(f"Failed to remove stake: {str(e)}")
        raise typer.Exit(1)


@app.command()
def info(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey account address"),
    client = typer.Option(None, help="Client instance")
):
    """Get stake information for an account."""
    # Get client if not provided
    if client is None:
        client = get_client()

    # Validate inputs
    if not validate_address(hotkey):
        print_error("Invalid hotkey address format.")
        raise typer.Exit(1)

    try:
        # Use the proper RPC method according to documentation
        response = client.get_account_subnet_stake(hotkey, subnet_id)

        if response.success:
            format_stake_info(response.data)
        else:
            print_error(f"Failed to get stake info: {response.message}")
            raise typer.Exit(1)
    except Exception as e:
        print_error(f"Failed to get stake info: {str(e)}")
        raise typer.Exit(1)
