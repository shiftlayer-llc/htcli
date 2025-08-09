"""
Flattened wallet commands - 3-level hierarchy.
"""

import typer
from rich.console import Console
from typing import Optional
from ..utils.crypto import generate_keypair, import_keypair, list_keys as list_keys_util, delete_keypair
from ..utils.validation import (
    validate_key_type, validate_password, validate_private_key,
    validate_wallet_name, validate_address, validate_tensor_stake_amount
)
from ..utils.formatting import (
    print_success, print_error, format_table, format_stake_info
)
from ..models.requests import StakeAddRequest, StakeRemoveRequest
from ..dependencies import get_client

app = typer.Typer(name="wallet", help="Wallet operations")
console = Console()


@app.command()
def generate_key(
    name: str = typer.Option(..., "--name", "-n", help="Key name"),
    key_type: str = typer.Option("sr25519", "--type", "-t", help="Key type (sr25519/ed25519)"),
    password: Optional[str] = typer.Option(None, "--password", "-p", help="Key password"),
    show_guidance: bool = typer.Option(True, "--guidance/--no-guidance", help="Show comprehensive guidance")
):
    """Generate a new keypair with comprehensive guidance."""
    # Validate inputs
    if not validate_wallet_name(name):
        print_error("Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only.")
        raise typer.Exit(1)

    if not validate_key_type(key_type):
        print_error("Invalid key type. Use 'sr25519' or 'ed25519'.")
        raise typer.Exit(1)

    if password and not validate_password(password):
        print_error("Invalid password. Must be at least 8 characters with letters and numbers.")
        raise typer.Exit(1)

    try:
        keypair_info = generate_keypair(name, key_type, password)
        print_success("✅ Key generated successfully!")

        # Display key information
        console.print(f"Name: {keypair_info.name}")
        console.print(f"Type: {keypair_info.key_type}")
        console.print(f"Public Key: {keypair_info.public_key}")
        console.print(f"SS58 Address: {keypair_info.ss58_address}")
    except Exception as e:
        print_error(f"Failed to generate key: {str(e)}")
        raise typer.Exit(1)


@app.command()
def import_key(
    name: str = typer.Option(..., "--name", "-n", help="Key name"),
    private_key: str = typer.Option(..., "--private-key", "-k", help="Private key (64-character hex)"),
    key_type: str = typer.Option("sr25519", "--type", "-t", help="Key type (sr25519/ed25519)"),
    password: Optional[str] = typer.Option(None, "--password", "-p", help="Key password"),
    show_guidance: bool = typer.Option(True, "--guidance/--no-guidance", help="Show comprehensive guidance")
):
    """Import a keypair from private key with comprehensive guidance."""
    # Validate inputs
    if not validate_wallet_name(name):
        print_error("Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only.")
        raise typer.Exit(1)

    if not validate_private_key(private_key):
        print_error("Invalid private key format. Should be a 64-character hex string.")
        raise typer.Exit(1)

    if not validate_key_type(key_type):
        print_error("Invalid key type. Use 'sr25519' or 'ed25519'.")
        raise typer.Exit(1)

    if password and not validate_password(password):
        print_error("Invalid password. Must be at least 8 characters with letters and numbers.")
        raise typer.Exit(1)

    try:
        keypair_info = import_keypair(name, private_key, key_type, password)
        print_success("✅ Key imported successfully!")

        # Display key information
        console.print(f"Name: {keypair_info.name}")
        console.print(f"Type: {keypair_info.key_type}")
        console.print(f"Public Key: {keypair_info.public_key}")
        console.print(f"SS58 Address: {keypair_info.ss58_address}")
    except Exception as e:
        print_error(f"Failed to import key: {str(e)}")
        raise typer.Exit(1)


@app.command()
def list_keys(
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """List all stored keys."""
    try:
        keys = list_keys_util()
        if not keys:
            console.print("No keys found.")
            return

        if format_type == "json":
            console.print_json(data=keys)
        else:
            # Create table
            headers = ["Name", "Type", "Address"]
            rows = []
            for key_info in keys:
                rows.append([
                    key_info.get("name", "N/A"),
                    key_info.get("key_type", "N/A"),
                    key_info.get("ss58_address", "N/A")
                ])

            table = format_table(headers, rows, "Stored Keys")
            console.print(table)
    except Exception as e:
        print_error(f"Failed to list keys: {str(e)}")
        raise typer.Exit(1)


@app.command()
def delete_key(
    name: str = typer.Option(..., "--name", "-n", help="Key name to delete"),
    confirm: bool = typer.Option(False, "--confirm", "-y", help="Skip confirmation prompt"),
    show_guidance: bool = typer.Option(True, "--guidance/--no-guidance", help="Show comprehensive guidance")
):
    """Delete a stored key with comprehensive guidance."""
    if not validate_wallet_name(name):
        print_error("Invalid wallet name.")
        raise typer.Exit(1)

    # Confirmation prompt
    if not confirm:
        delete_confirm = typer.confirm(f"Are you sure you want to delete key '{name}'?")
        if not delete_confirm:
            console.print("Operation cancelled.")
            return

    try:
        success = delete_keypair(name)
        if success:
            print_success(f"✅ Key '{name}' deleted successfully!")
        else:
            print_error(f"Key '{name}' not found.")
    except Exception as e:
        print_error(f"Failed to delete key: {str(e)}")
        raise typer.Exit(1)


@app.command()
def add_stake(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(..., "--node-id", "-n", help="Node ID"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey address"),
    amount: int = typer.Option(..., "--amount", "-a", help="Stake amount (in smallest unit)"),
    key_name: Optional[str] = typer.Option(None, "--key-name", "-k", help="Key name for signing")
):
    """Add stake to a subnet node."""
    client = get_client()

    # Validate inputs
    if not validate_address(hotkey):
        print_error("Invalid hotkey address format.")
        raise typer.Exit(1)

    if amount <= 0:
        print_error("Stake amount must be positive.")
        raise typer.Exit(1)

    try:
        request = StakeAddRequest(
            subnet_id=subnet_id,
            node_id=node_id,
            hotkey=hotkey,
            stake_to_be_added=amount
        )

        # Get keypair for signing if provided
        keypair = None
        if key_name:
            # TODO: Load keypair from storage
            pass

        response = client.add_to_stake(request, keypair)
        print_success(f"✅ Added {amount} stake to subnet {subnet_id} successfully!")
        console.print(f"Transaction: {response.transaction_hash}")
        if response.block_number:
            console.print(f"Block: #{response.block_number}")
    except Exception as e:
        print_error(f"Failed to add stake: {str(e)}")
        raise typer.Exit(1)


@app.command()
def remove_stake(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey address"),
    amount: int = typer.Option(..., "--amount", "-a", help="Stake amount to remove"),
    key_name: Optional[str] = typer.Option(None, "--key-name", "-k", help="Key name for signing")
):
    """Remove stake from a subnet node."""
    client = get_client()

    # Validate inputs
    if not validate_address(hotkey):
        print_error("Invalid hotkey address format.")
        raise typer.Exit(1)

    if amount <= 0:
        print_error("Stake amount must be positive.")
        raise typer.Exit(1)

    try:
        request = StakeRemoveRequest(
            subnet_id=subnet_id,
            hotkey=hotkey,
            stake_to_be_removed=amount
        )

        # Get keypair for signing if provided
        keypair = None
        if key_name:
            # TODO: Load keypair from storage
            pass

        response = client.remove_stake(request, keypair)
        print_success(f"✅ Removed {amount} stake from subnet {subnet_id} successfully!")
        console.print(f"Transaction: {response.transaction_hash}")
        if response.block_number:
            console.print(f"Block: #{response.block_number}")
    except Exception as e:
        print_error(f"Failed to remove stake: {str(e)}")
        raise typer.Exit(1)


@app.command()
def stake_info(
    address: str = typer.Option(..., "--address", "-a", help="Account address"),
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """Get stake information for an account."""
    client = get_client()

    # Validate inputs
    if not validate_address(address):
        print_error("Invalid address format.")
        raise typer.Exit(1)

    try:
        response = client.get_account_subnet_stake(address, subnet_id)
        if response.success:
            stake_data = response.data
            if format_type == "json":
                console.print_json(data=stake_data)
            else:
                format_stake_info(stake_data)
        else:
            print_error(f"Failed to retrieve stake info: {response.message}")
    except Exception as e:
        print_error(f"Failed to get stake info: {str(e)}")
        raise typer.Exit(1)


@app.command()
def claim_unbondings(
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey address"),
    key_name: Optional[str] = typer.Option(None, "--key-name", "-k", help="Key name for signing")
):
    """Claim unbonded stake."""
    client = get_client()

    # Validate inputs
    if not validate_address(hotkey):
        print_error("Invalid hotkey address format.")
        raise typer.Exit(1)

    try:
        # Get keypair for signing if provided
        keypair = None
        if key_name:
            # TODO: Load keypair from storage
            pass

        response = client.claim_unbondings(keypair)
        print_success("✅ Unbonded stake claimed successfully!")
        console.print(f"Transaction: {response.transaction_hash}")
        if response.block_number:
            console.print(f"Block: #{response.block_number}")
    except Exception as e:
        print_error(f"Failed to claim unbondings: {str(e)}")
        raise typer.Exit(1)
