"""
Flattened wallet commands - 3-level hierarchy.
"""

import typer
from rich.console import Console
from typing import Optional
from ..utils.crypto import (
    generate_keypair,
    import_keypair,
    list_keys as list_keys_util,
    delete_keypair,
)
from ..utils.validation import (
    validate_key_type,
    validate_password,
    validate_private_key,
    validate_wallet_name,
)
from ..utils.formatting import print_success, print_error, format_table

app = typer.Typer(name="wallet", help="Wallet operations")
console = Console()


@app.command()
def generate_key(
    name: str = typer.Option(..., "--name", "-n", help="Key name"),
    key_type: str = typer.Option(
        "sr25519", "--type", "-t", help="Key type (sr25519/ed25519)"
    ),
    password: Optional[str] = typer.Option(
        None, "--password", "-p", help="Key password"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Generate a new keypair with comprehensive guidance."""
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
    private_key: str = typer.Option(
        ..., "--private-key", "-k", help="Private key (64-character hex)"
    ),
    key_type: str = typer.Option(
        "sr25519", "--type", "-t", help="Key type (sr25519/ed25519)"
    ),
    password: Optional[str] = typer.Option(
        None, "--password", "-p", help="Key password"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Import a keypair from private key with comprehensive guidance."""
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
    format_type: str = typer.Option(
        "table", "--format", "-f", help="Output format (table/json)"
    )
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
                rows.append(
                    [
                        key_info.get("name", "N/A"),
                        key_info.get("key_type", "N/A"),
                        key_info.get("ss58_address", "N/A"),
                    ]
                )

            table = format_table(headers, rows, "Stored Keys")
            console.print(table)
    except Exception as e:
        print_error(f"Failed to list keys: {str(e)}")
        raise typer.Exit(1)


@app.command()
def status(
    format_type: str = typer.Option(
        "table", "--format", "-f", help="Output format (table/json)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Show your blockchain identity and key status."""
    from rich.panel import Panel
    from rich.table import Table
    from ..utils.ownership import get_user_addresses, get_ownership_summary

    if show_guidance:
        guidance_panel = Panel(
            "[bold cyan]🔐 Blockchain Identity Status[/bold cyan]\n\n"
            "This command shows your blockchain identity and key status:\n"
            "• [bold]Stored Keys[/bold]: Your private/public keypairs\n"
            "• [bold]Addresses[/bold]: Your blockchain addresses (SS58 format)\n"
            "• [bold]Identity[/bold]: Your presence on the Hypertensor network\n"
            "• [bold]Capabilities[/bold]: What you can do with your keys\n\n"
            "[yellow]💡 Tip:[/yellow] Your private keys are your identity on the blockchain.\n"
            "Keep them secure and never share them with anyone!",
            title="[bold yellow]🔑 Key Status Guide[/bold yellow]",
            border_style="yellow",
        )
        console.print(guidance_panel)
        console.print()

    try:
        # Get user addresses and summary
        user_addresses = get_user_addresses()
        summary = get_ownership_summary(user_addresses)

        if not user_addresses:
            console.print(
                Panel(
                    "[bold red]❌ No Keys Found[/bold red]\n\n"
                    "You don't have any keys stored yet. To get started:\n\n"
                    "1. [cyan]Generate a new key:[/cyan]\n"
                    "   htcli wallet generate-key --name my-wallet\n\n"
                    "2. [cyan]Import existing key:[/cyan]\n"
                    "   htcli wallet import-key --name my-wallet --private-key <key>\n\n"
                    "3. [cyan]Check your identity:[/cyan]\n"
                    "   htcli wallet status",
                    title="[bold red]🔑 No Blockchain Identity[/bold red]",
                    border_style="red",
                )
            )
            return

        # Create identity summary
        identity_panel = Panel(
            f"[bold green]✅ Blockchain Identity Active[/bold green]\n\n"
            f"• [bold]Keys Found:[/bold] {len(user_addresses)}\n"
            f"• [bold]Addresses:[/bold] {len(user_addresses)}\n"
            f"• [bold]Network:[/bold] Hypertensor\n"
            f"• [bold]Status:[/bold] Ready for operations",
            title="[bold green]🔐 Your Blockchain Identity[/bold green]",
            border_style="green",
        )
        console.print(identity_panel)
        console.print()

        # Create detailed key table
        table = Table(
            title="[bold cyan]Your Keys & Addresses[/bold cyan]",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Key Name", style="cyan", no_wrap=True)
        table.add_column("Address (SS58)", style="green")
        table.add_column("Type", style="yellow")
        table.add_column("Status", style="white")

        for key_name, address in user_addresses:
            table.add_row(
                key_name,
                address,
                "sr25519",  # We can enhance this to show actual type
                "✅ Active",
            )

        console.print(table)
        console.print()

        # Show capabilities
        capabilities_panel = Panel(
            "[bold blue]🚀 What You Can Do:[/bold blue]\n\n"
            "✅ [green]Sign transactions[/green] (staking, subnet operations)\n"
            "✅ [green]Own assets[/green] (subnets, nodes, stakes)\n"
            "✅ [green]Filter results[/green] (use --mine flag)\n"
            "✅ [green]Earn rewards[/green] (staking rewards)\n"
            "✅ [green]Participate in governance[/green] (voting, proposals)\n\n"
            "[yellow]💡 Next Steps:[/yellow]\n"
            "• Check your balance: htcli chain balance --address <your-address>\n"
            "• View your assets: htcli --mine subnet list\n"
            "• Start staking: htcli stake add --subnet-id 1 --amount 100 --key-name <key-name>",
            title="[bold blue]🎯 Your Capabilities[/bold blue]",
            border_style="blue",
        )
        console.print(capabilities_panel)

    except Exception as e:
        print_error(f"Failed to get wallet status: {str(e)}")
        raise typer.Exit(1)


@app.command()
def delete_key(
    name: str = typer.Option(..., "--name", "-n", help="Key name to delete"),
    confirm: bool = typer.Option(
        False, "--confirm", "-y", help="Skip confirmation prompt"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
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
