"""
Flattened wallet commands - 3-level hierarchy.
"""

from typing import Optional

import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm

from ..utils.crypto import delete_keypair, generate_coldkey_pair, generate_hotkey_pair, generate_keypair, import_keypair
from ..utils.crypto import list_keys as list_keys_util
from ..utils.formatting import format_table, print_error, print_success
from ..utils.ownership import get_ownership_summary, get_user_addresses
from ..utils.validation import (validate_key_type, validate_password,
                                validate_private_key, validate_wallet_name)

app = typer.Typer(name="wallet", help="Wallet operations")
console = Console()


def prompt_for_missing_args(name: Optional[str] = None, owner_address: Optional[str] = None,
                           key_type: Optional[str] = None, password: Optional[str] = None,
                           show_guidance: Optional[bool] = None) -> tuple[str, str, str, Optional[str], bool]:
    """Interactive prompt for missing arguments."""

    # Prompt for name if missing
    if not name:
        while True:
            name = Prompt.ask("Enter hotkey name", default="my-hotkey")
            if validate_wallet_name(name):
                break
            print_error("Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only.")

    # Prompt for owner address if missing
    if not owner_address:
        while True:
            owner_address = Prompt.ask("Enter coldkey address that owns this hotkey")
            if owner_address.startswith("5"):
                break
            print_error("Owner address must be a valid SS58 address starting with '5'")

    # Prompt for key type if missing
    if not key_type:
        key_type = Prompt.ask("Enter key type", choices=["sr25519", "ed25519"], default="sr25519")

    # Prompt for password (optional)
    if password is None:
        use_password = Confirm.ask("Do you want to set a password for this hotkey?", default=False)
        if use_password:
            while True:
                password = Prompt.ask("Enter password (min 8 chars, letters + numbers)", password=True)
                if validate_password(password):
                    break
                print_error("Invalid password. Must be at least 8 characters with letters and numbers.")
        else:
            password = None

    # Prompt for guidance (optional)
    if show_guidance is None:
        show_guidance = Confirm.ask("Show comprehensive guidance?", default=True)

    return name, owner_address, key_type, password, show_guidance


@app.command()
def generate_hotkey(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Hotkey name"),
    owner_address: Optional[str] = typer.Option(None, "--owner", "-o", help="Coldkey address that owns this hotkey"),
    key_type: str = typer.Option(
        "sr25519", "--type", "-t", help="Key type (sr25519/ed25519)"
    ),
    password: Optional[str] = typer.Option(
        None, "--password", "-p", help="Key password"
    ),
    show_guidance: Optional[bool] = typer.Option(
        None, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Generate a new hotkey with comprehensive guidance."""

    # Interactive prompting for missing arguments
    name, owner_address, key_type, password, show_guidance = prompt_for_missing_args(
        name, owner_address, key_type, password, show_guidance
    )

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

    # Validate owner address format
    if not owner_address.startswith("5"):
        print_error("Owner address must be a valid SS58 address starting with '5'")
        raise typer.Exit(1)

    try:
        keypair_info = generate_hotkey_pair(name, owner_address, key_type, password)
        print_success("✅ Hotkey generated successfully!")

        # Display key information
        console.print(f"Name: {keypair_info.name}")
        console.print(f"Type: {keypair_info.key_type}")
        console.print(f"Public Key: {keypair_info.public_key}")
        console.print(f"SS58 Address: {keypair_info.ss58_address}")
        console.print(f"Owner: {keypair_info.owner_address}")

        if show_guidance:
            from rich.panel import Panel
            guidance_panel = Panel(
                f"[bold cyan]🔑 Hotkey Generated Successfully[/bold cyan]\n\n"
                f"[bold]Hotkey Details:[/bold]\n"
                f"• Name: {name}\n"
                f"• Address: {keypair_info.ss58_address}\n"
                f"• Owner: {owner_address}\n\n"
                f"[bold]What is a Hotkey?[/bold]\n"
                f"• Used for operational tasks (consensus, validation)\n"
                f"• Owned by your coldkey for security\n"
                f"• Can be kept online for frequent operations\n"
                f"• Cannot transfer funds directly\n\n"
                f"[bold]Usage Examples:[/bold]\n"
                f"• Register node: htcli node register --hotkey {keypair_info.ss58_address}\n"
                f"• Update hotkey: htcli wallet update-hotkey --old-hotkey {keypair_info.ss58_address}\n\n"
                f"[yellow]💡 Security Tip:[/yellow] Keep your coldkey secure, hotkey can be rotated if compromised",
                title="Hotkey Generation Complete",
                border_style="green",
            )
            console.print(guidance_panel)

    except Exception as e:
        print_error(f"Failed to generate hotkey: {str(e)}")
        raise typer.Exit(1)


def prompt_for_coldkey_args(name: Optional[str] = None, key_type: Optional[str] = None,
                           password: Optional[str] = None, show_guidance: Optional[bool] = None) -> tuple[str, str, Optional[str], bool]:
    """Interactive prompt for coldkey arguments."""

    # Prompt for name if missing
    if not name:
        while True:
            name = Prompt.ask("Enter coldkey name", default="my-coldkey")
            if validate_wallet_name(name):
                break
            print_error("Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only.")

    # Prompt for key type if missing
    if not key_type:
        key_type = Prompt.ask("Enter key type", choices=["sr25519", "ed25519"], default="sr25519")

    # Prompt for password (optional)
    if password is None:
        use_password = Confirm.ask("Do you want to set a password for this coldkey?", default=False)
        if use_password:
            while True:
                password = Prompt.ask("Enter password (min 8 chars, letters + numbers)", password=True)
                if validate_password(password):
                    break
                print_error("Invalid password. Must be at least 8 characters with letters and numbers.")
        else:
            password = None

    # Prompt for guidance (optional)
    if show_guidance is None:
        show_guidance = Confirm.ask("Show comprehensive guidance?", default=True)

    return name, key_type, password, show_guidance


@app.command()
def generate_coldkey(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Coldkey name"),
    key_type: str = typer.Option(
        "sr25519", "--type", "-t", help="Key type (sr25519/ed25519)"
    ),
    password: Optional[str] = typer.Option(
        None, "--password", "-p", help="Key password"
    ),
    show_guidance: Optional[bool] = typer.Option(
        None, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Generate a new coldkey with comprehensive guidance."""

    # Interactive prompting for missing arguments
    name, key_type, password, show_guidance = prompt_for_coldkey_args(
        name, key_type, password, show_guidance
    )

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
        keypair_info = generate_coldkey_pair(name, key_type, password)
        print_success("✅ Coldkey generated successfully!")

        # Display key information
        console.print(f"Name: {keypair_info.name}")
        console.print(f"Type: {keypair_info.key_type}")
        console.print(f"Public Key: {keypair_info.public_key}")
        console.print(f"SS58 Address: {keypair_info.ss58_address}")

        if show_guidance:
            from rich.panel import Panel
            guidance_panel = Panel(
                f"[bold cyan]🔐 Coldkey Generated Successfully[/bold cyan]\n\n"
                f"[bold]Coldkey Details:[/bold]\n"
                f"• Name: {name}\n"
                f"• Address: {keypair_info.ss58_address}\n"
                f"• Type: {key_type}\n\n"
                f"[bold]What is a Coldkey?[/bold]\n"
                f"• Controls account ownership and funds\n"
                f"• Should be kept offline/secure\n"
                f"• Used for critical operations\n"
                f"• Can own multiple hotkeys\n\n"
                f"[bold]Usage Examples:[/bold]\n"
                f"• Register subnet: htcli subnet register (uses this coldkey)\n"
                f"• Transfer funds: htcli wallet transfer --from {keypair_info.ss58_address}\n"
                f"• Create hotkey: htcli wallet generate-hotkey --owner {keypair_info.ss58_address}\n\n"
                f"[yellow]⚠️ Security Warning:[/yellow] Keep this coldkey secure - it controls your funds!",
                title="Coldkey Generation Complete",
                border_style="blue",
            )
            console.print(guidance_panel)

    except Exception as e:
        print_error(f"Failed to generate coldkey: {str(e)}")
        raise typer.Exit(1)


def prompt_for_restore_args(name: Optional[str] = None, private_key: Optional[str] = None,
                           key_type: Optional[str] = None, password: Optional[str] = None,
                           show_guidance: Optional[bool] = None) -> tuple[str, str, str, Optional[str], bool]:
    """Interactive prompt for restore arguments."""

    # Prompt for name if missing
    if not name:
        while True:
            name = Prompt.ask("Enter key name", default="imported-key")
            if validate_wallet_name(name):
                break
            print_error("Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only.")

    # Prompt for private key if missing
    if not private_key:
        while True:
            private_key = Prompt.ask("Enter private key (64-character hex)", password=True)
            if validate_private_key(private_key):
                break
            print_error("Invalid private key format. Should be a 64-character hex string.")

    # Prompt for key type if missing
    if not key_type:
        key_type = Prompt.ask("Enter key type", choices=["sr25519", "ed25519"], default="sr25519")

    # Prompt for password (optional)
    if password is None:
        use_password = Confirm.ask("Do you want to set a password for this imported key?", default=False)
        if use_password:
            while True:
                password = Prompt.ask("Enter password (min 8 chars, letters + numbers)", password=True)
                if validate_password(password):
                    break
                print_error("Invalid password. Must be at least 8 characters with letters and numbers.")
        else:
            password = None

    # Prompt for guidance (optional)
    if show_guidance is None:
        show_guidance = Confirm.ask("Show comprehensive guidance?", default=True)

    return name, private_key, key_type, password, show_guidance


@app.command()
def restore(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Key name"),
    private_key: Optional[str] = typer.Option(
        None, "--private-key", "-k", help="Private key (64-character hex)"
    ),
    key_type: str = typer.Option(
        "sr25519", "--type", "-t", help="Key type (sr25519/ed25519)"
    ),
    password: Optional[str] = typer.Option(
        None, "--password", "-p", help="Key password"
    ),
    show_guidance: Optional[bool] = typer.Option(
        None, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Import a keypair from private key with comprehensive guidance."""

    # Interactive prompting for missing arguments
    name, private_key, key_type, password, show_guidance = prompt_for_restore_args(
        name, private_key, key_type, password, show_guidance
    )

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

        if show_guidance:
            from rich.panel import Panel
            guidance_panel = Panel(
                f"[bold cyan]🔑 Key Imported Successfully[/bold cyan]\n\n"
                f"[bold]Imported Key Details:[/bold]\n"
                f"• Name: {name}\n"
                f"• Address: {keypair_info.ss58_address}\n"
                f"• Type: {key_type}\n\n"
                f"[bold]What was imported?[/bold]\n"
                f"• Your private key has been securely stored\n"
                f"• The key is encrypted with your password\n"
                f"• You can now use this key for operations\n\n"
                f"[bold]Usage Examples:[/bold]\n"
                f"• View key: htcli wallet list\n"
                f"• Use for operations: htcli subnet register\n"
                f"• Transfer funds: htcli wallet transfer\n\n"
                f"[yellow]💡 Security Tip:[/yellow] Keep your private key secure and never share it!",
                title="Key Import Complete",
                border_style="green",
            )
            console.print(guidance_panel)

    except Exception as e:
        print_error(f"Failed to import key: {str(e)}")
        raise typer.Exit(1)


@app.command()
def list(
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
            # Create table with hotkey/coldkey distinction
            headers = ["Name", "Type", "Key Type", "Address", "Owner"]
            rows = []
            for key_info in keys:
                is_hotkey = key_info.get("is_hotkey", False)
                key_type_display = "🔑 Hotkey" if is_hotkey else "🔐 Coldkey"
                owner = key_info.get("owner_address", "N/A") if is_hotkey else "N/A"

                rows.append(
                    [
                        key_info.get("name", "N/A"),
                        key_info.get("key_type", "N/A"),
                        key_type_display,
                        key_info.get("ss58_address", "N/A"),
                        owner,
                    ]
                )

            table = format_table(headers, rows, "Stored Keys")
            console.print(table)

            # Show summary
            coldkeys = [k for k in keys if not k.get("is_hotkey", False)]
            hotkeys = [k for k in keys if k.get("is_hotkey", False)]

            console.print(f"\n[bold]Summary:[/bold] {len(coldkeys)} coldkeys, {len(hotkeys)} hotkeys")
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


def prompt_for_delete_args(name: Optional[str] = None, confirm: Optional[bool] = None,
                          show_guidance: Optional[bool] = None) -> tuple[str, bool, bool]:
    """Interactive prompt for delete arguments."""

    # Prompt for name if missing
    if not name:
        # First show available keys
        keys = list_keys_util()
        if not keys:
            print_error("No keys found to delete.")
            raise typer.Exit(1)

        console.print("\n[bold]Available keys:[/bold]")
        for i, key in enumerate(keys, 1):
            console.print(f"{i}. {key['name']} ({key['ss58_address']})")

        while True:
            name = Prompt.ask("\nEnter key name to delete")
            if validate_wallet_name(name):
                # Check if key exists
                key_names = [k['name'] for k in keys]
                if name in key_names:
                    break
                else:
                    print_error(f"Key '{name}' not found. Please choose from the list above.")
            else:
                print_error("Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only.")

    # Prompt for confirmation if not provided
    if confirm is None:
        confirm = Confirm.ask(f"Are you sure you want to delete key '{name}'?", default=False)

    # Prompt for guidance if not provided
    if show_guidance is None:
        show_guidance = Confirm.ask("Show comprehensive guidance?", default=True)

    return name, confirm, show_guidance


@app.command()
def delete(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Key name to delete"),
    confirm: bool = typer.Option(
        False, "--confirm", "-y", help="Skip confirmation prompt"
    ),
    show_guidance: Optional[bool] = typer.Option(
        None, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Delete a stored key with comprehensive guidance."""

    # Interactive prompting for missing arguments
    name, confirm, show_guidance = prompt_for_delete_args(name, confirm, show_guidance)

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
        delete_keypair(name)
        print_success(f"✅ Key '{name}' deleted successfully!")

        if show_guidance:
            from rich.panel import Panel
            guidance_panel = Panel(
                f"[bold red]🗑️ Key Deleted Successfully[/bold red]\n\n"
                f"[bold]Deleted Key:[/bold] {name}\n\n"
                f"[bold]What happened?[/bold]\n"
                f"• The key has been permanently removed from your system\n"
                f"• The encrypted private key file has been deleted\n"
                f"• You can no longer use this key for operations\n\n"
                f"[bold]Important Notes:[/bold]\n"
                f"• If you had funds associated with this key, they are still on the blockchain\n"
                f"• You can recover them by importing the private key again\n"
                f"• Make sure you have a backup of the private key if needed\n\n"
                f"[yellow]⚠️ Warning:[/yellow] This action cannot be undone!",
                title="Key Deletion Complete",
                border_style="red",
            )
            console.print(guidance_panel)

    except Exception as e:
        print_error(f"Failed to delete key: {str(e)}")
        raise typer.Exit(1)
