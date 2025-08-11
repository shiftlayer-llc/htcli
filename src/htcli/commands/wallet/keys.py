"""
Wallet key management commands.
"""

import typer
from rich.console import Console
from typing import Optional
from ...utils.crypto import generate_keypair, import_keypair, list_keys, delete_keypair
from ...utils.validation import (
    validate_key_type,
    validate_password,
    validate_private_key,
    validate_wallet_name,
)
from ...utils.formatting import print_success, print_error, format_table

app = typer.Typer(name="keys", help="Wallet key management")
console = Console()


@app.command()
def generate(
    name: str = typer.Argument(..., help="Key name"),
    key_type: str = typer.Option(
        "sr25519", "--type", "-t", help="Key type (sr25519/ed25519)"
    ),
    password: Optional[str] = typer.Option(
        None, "--password", "-p", help="Key password"
    ),
):
    """Generate a new keypair."""
    # Validate inputs
    if not validate_wallet_name(name):
        print_error(
            "Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only."
        )
        raise typer.Exit(1)

    if not validate_key_type(key_type):
        print_error("Invalid key type. Use 'sr25519' or 'ed25519'.")
        raise typer.Exit(1)

    if password and not validate_password(password):
        print_error(
            "Invalid password. Must be at least 8 characters with letters and numbers."
        )
        raise typer.Exit(1)

    try:
        keypair = generate_keypair(name, key_type, password)
        print_success(f"Keypair '{name}' generated successfully!")
        console.print(f"Public Key: {keypair.public_key}")
        console.print(f"Address: {keypair.ss58_address}")
    except Exception as e:
        print_error(f"Failed to generate keypair: {str(e)}")
        raise typer.Exit(1)


@app.command()
def list():
    """List all available keys."""
    try:
        keys = list_keys()

        if keys:
            headers = ["Name", "Type", "Address"]
            rows = [[key.name, key.key_type, key.ss58_address] for key in keys]
            table = format_table(headers, rows, "Available Keys")
            console.print(table)
        else:
            console.print("No keys found.")

    except Exception as e:
        print_error(f"Failed to list keys: {str(e)}")
        raise typer.Exit(1)


@app.command()
def import_key(
    name: str = typer.Argument(..., help="Key name"),
    private_key: str = typer.Option(..., "--private-key", "-k", help="Private key"),
    key_type: str = typer.Option("sr25519", "--type", "-t", help="Key type"),
    password: Optional[str] = typer.Option(
        None, "--password", "-p", help="Key password"
    ),
):
    """Import an existing keypair."""
    # Validate inputs
    if not validate_wallet_name(name):
        print_error(
            "Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only."
        )
        raise typer.Exit(1)

    if not validate_private_key(private_key):
        print_error("Invalid private key format. Should be a 64-character hex string.")
        raise typer.Exit(1)

    if not validate_key_type(key_type):
        print_error("Invalid key type. Use 'sr25519' or 'ed25519'.")
        raise typer.Exit(1)

    if password and not validate_password(password):
        print_error(
            "Invalid password. Must be at least 8 characters with letters and numbers."
        )
        raise typer.Exit(1)

    try:
        keypair = import_keypair(name, private_key, key_type, password)
        print_success(f"Keypair '{name}' imported successfully!")
        console.print(f"Address: {keypair.ss58_address}")
    except Exception as e:
        print_error(f"Failed to import keypair: {str(e)}")
        raise typer.Exit(1)


@app.command()
def delete(
    name: str = typer.Argument(..., help="Key name"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Delete a keypair."""
    if not force:
        confirm = typer.confirm(f"Are you sure you want to delete keypair '{name}'?")
        if not confirm:
            console.print("Operation cancelled.")
            return

    try:
        delete_keypair(name)
        print_success(f"Keypair '{name}' deleted successfully!")
    except Exception as e:
        print_error(f"Failed to delete keypair: {str(e)}")
        raise typer.Exit(1)
