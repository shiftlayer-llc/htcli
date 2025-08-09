"""
Subnet registration commands.
"""

import typer
from rich.console import Console
from ...models.requests import SubnetRegisterRequest
from ...utils.validation import (
    validate_subnet_path,
    validate_memory_mb,
    validate_registration_blocks,
    validate_entry_interval
)
from ...utils.formatting import print_success, print_error
from ...dependencies import get_client

app = typer.Typer(name="register", help="Subnet registration commands")
console = Console()


@app.command()
def create(
    path: str = typer.Argument(..., help="Subnet path"),
    memory_mb: int = typer.Option(..., "--memory", "-m", help="Memory requirement in MB"),
    registration_blocks: int = typer.Option(..., "--blocks", "-b", help="Registration period in blocks"),
    entry_interval: int = typer.Option(..., "--interval", "-i", help="Entry interval in blocks"),
    client = typer.Option(None, help="Client instance")
):
    """Register a new subnet."""
    # Get client if not provided
    if client is None:
        client = get_client()

    # Validate inputs
    if not validate_subnet_path(path):
        print_error("Invalid subnet path. Use alphanumeric characters, hyphens, and underscores only.")
        raise typer.Exit(1)

    if not validate_memory_mb(memory_mb):
        print_error("Invalid memory requirement. Must be between 1 and 100000 MB.")
        raise typer.Exit(1)

    if not validate_registration_blocks(registration_blocks):
        print_error("Invalid registration blocks. Must be between 1 and 1000000 blocks.")
        raise typer.Exit(1)

    if not validate_entry_interval(entry_interval):
        print_error("Invalid entry interval. Must be between 1 and 100000 blocks.")
        raise typer.Exit(1)

    try:
        request = SubnetRegisterRequest(
            path=path,
            memory_mb=memory_mb,
            registration_blocks=registration_blocks,
            entry_interval=entry_interval
        )

        response = client.register_subnet(request)
        print_success("Subnet registered successfully!")
        console.print(f"Transaction: {response.transaction_hash}")
    except Exception as e:
        print_error(f"Failed to register subnet: {str(e)}")
        raise typer.Exit(1)


@app.command()
def activate(
    subnet_id: int = typer.Argument(..., help="Subnet ID to activate"),
    client = typer.Option(None, help="Client instance")
):
    """Activate a registered subnet."""
    # Get client if not provided
    if client is None:
        client = get_client()

    try:
        response = client.activate_subnet(subnet_id)
        print_success(f"Subnet {subnet_id} activated successfully!")
        console.print(f"Transaction: {response.transaction_hash}")
    except Exception as e:
        print_error(f"Failed to activate subnet: {str(e)}")
        raise typer.Exit(1)
