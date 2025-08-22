"""
Hypertensor CLI wallet commands for managing coldkeys and hotkeys,
including generation, import, listing, status, and deletion.
Implements a user-friendly, interactive interface for blockchain key management.
"""

from typing import Optional

import typer
from rich.console import Console
from src.htcli.guides.wallet import (
    CAPABILITIES_TEMPLATE,
    COLDKEY_GUIDANCE_TEMPLATE,
    HOTKEY_GUIDANCE_TEMPLATE,
    IDENTITY_TEMPLATE,
    NO_KEYS_TEMPLATE,
    RESTORE_GUIDANCE_TEMPLATE,
    WALLET_DELETE_GUIDANCE_TEMPLATE,
    WALLET_STATUS_GUIDANCE_TEMPLATE,
)
from src.htcli.helpers.wallet import (
    display_keys_table,
    display_keys_tree,
    prompt_for_coldkey_args,
    prompt_for_delete_args,
    prompt_for_missing_args,
    prompt_for_restore_args,
)

from ..utils.crypto import (
    delete_keypair,
    generate_coldkey_pair,
    generate_hotkey_pair,
    import_keypair,
    list_keys,
)
from ..utils.formatting import print_error, print_success
from ..utils.validation import (
    validate_key_type,
    validate_password,
    validate_private_key,
    validate_wallet_name,
)

app = typer.Typer(name="wallet", help="Wallet operations")
console = Console()


@app.command()
def generate_hotkey(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Hotkey name"),
    owner_name: Optional[str] = typer.Option(
        None, "--owner", "-o", help="Coldkey wallet name that owns this hotkey"
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
    """Generate a new hotkey with comprehensive guidance."""

    # Interactive prompting for missing arguments
    name, owner_address, key_type, owner_name, password, show_guidance = prompt_for_missing_args(
        name, owner_name, key_type, password, show_guidance
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

    # Validate that owner is a coldkey, not a hotkey
    try:
        from ..utils.crypto import get_wallet_info_by_name
        owner_wallet_info = get_wallet_info_by_name(owner_name)
        if owner_wallet_info.get("is_hotkey", False):
            print_error(f"'{owner_name}' is a hotkey. Please provide a coldkey wallet name as the owner.")
            raise typer.Exit(1)
    except FileNotFoundError:
        print_error(f"Owner wallet '{owner_name}' not found. Please provide an existing coldkey wallet name.")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Error validating owner wallet '{owner_name}': {str(e)}")
        raise typer.Exit(1)

    try:
        keypair_info = generate_hotkey_pair(name, owner_address, key_type, password)
        print_success("✅ Hotkey generated successfully!")

        if show_guidance:
            from rich.panel import Panel

            guidance_panel = Panel(
                HOTKEY_GUIDANCE_TEMPLATE.format(
                    name=name,
                    address=keypair_info.ss58_address,
                    owner_name=owner_name,
                    owner_address=owner_address,
                ),
                title="Hotkey Generation Complete",
                border_style="green",
            )
            console.print(guidance_panel)
        else:
            # Display key information
            console.print(f"Name: {keypair_info.name}")
            console.print(f"Type: {keypair_info.key_type}")
            console.print(f"Public Key: {keypair_info.public_key}")
            console.print(f"SS58 Address: {keypair_info.ss58_address}")
            console.print(f"Owner: {owner_name} ({owner_address})")

    except Exception as e:
        print_error(f"Failed to generate hotkey: {str(e)}")
        raise typer.Exit(1)


@app.command()
def generate_coldkey(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Coldkey name"),
    key_type: str = typer.Option(
        "sr25519",
        "--type",
        "-t",
        help="Key type (sr25519/ed25519)",
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

        if show_guidance:
            from rich.panel import Panel

            guidance_panel = Panel(
                COLDKEY_GUIDANCE_TEMPLATE.format(
                    name=name,
                    address=keypair_info.ss58_address,
                    key_type=key_type,
                ),
                title="Coldkey Generation Complete",
                border_style="green",
            )
            console.print(guidance_panel)
        else:
            # Display key information
            console.print(f"Name: {keypair_info.name}")
            console.print(f"Type: {keypair_info.key_type}")
            console.print(f"Public Key: {keypair_info.public_key}")
            console.print(f"SS58 Address: {keypair_info.ss58_address}")

    except Exception as e:
        print_error(f"Failed to generate coldkey: {str(e)}")
        raise typer.Exit(1)


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
        print_success("Key imported successfully!")

        # Display key information
        console.print(f"Name: {keypair_info.name}")
        console.print(f"Type: {keypair_info.key_type}")
        console.print(f"Public Key: {keypair_info.public_key}")
        console.print(f"SS58 Address: {keypair_info.ss58_address}")

        if show_guidance:
            from rich.panel import Panel

            guidance_panel = Panel(
                RESTORE_GUIDANCE_TEMPLATE.format(
                    name=name,
                    address=keypair_info.ss58_address,
                    key_type=key_type,
                ),
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
        "tree", "--format", "-f", help="Output format (tree/table/json)"
    )
):
    """List all stored keys in hierarchical format."""
    try:
        keys = list_keys()
        if not keys:
            console.print("No keys found.")
            return

        if format_type == "json":
            console.print_json(data=keys)
        elif format_type == "table":
            # Display in table format
            display_keys_table(keys)
        else:
            # Display in hierarchical tree format (default)
            display_keys_tree(keys)

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

    try:
        # Show guidance
        if show_guidance:
            console.print(Panel(WALLET_STATUS_GUIDANCE_TEMPLATE, border_style="yellow"))
            console.print()

        # Get all keys for proper display
        keys = list_keys()

        if not keys:
            console.print(
                Panel(
                    NO_KEYS_TEMPLATE,
                    title="[bold red]🔑 No Blockchain Identity[/bold red]",
                    border_style="red",
                )
            )
            return

        # Identity summary
        console.print(
            Panel(
                IDENTITY_TEMPLATE.format(num_keys=len(keys), num_addresses=len(keys)),
                title="[bold green]🔐 Your Blockchain Identity[/bold green]",
                border_style="green",
            )
        )
        console.print()

        # Keys table with hotkey/coldkey distinction
        table = Table(
            title="[bold cyan]Your Keys & Addresses[/bold cyan]",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Key Name", style="cyan", no_wrap=True)
        table.add_column("Address (SS58)", style="green")
        table.add_column("Key Type", style="blue")
        table.add_column("Owner", style="purple")
        table.add_column("Status", style="white")

        # Separate coldkeys and hotkeys
        coldkeys = [k for k in keys if not k.get("is_hotkey", False)]
        hotkeys = [k for k in keys if k.get("is_hotkey", False)]

        # Create address to name mapping for owner display
        address_to_name = {}
        for key_info in coldkeys:
            address_to_name[key_info.get("ss58_address")] = key_info.get("name")

        # Add coldkeys first
        for key_info in coldkeys:
            key_type_display = "🔐 Coldkey"
            owner = "N/A"
            table.add_row(
                key_info.get("name", "N/A"),
                key_info.get("ss58_address", "N/A"),
                key_type_display,
                owner,
                "✅ Active",
            )

        # Add hotkeys
        for key_info in hotkeys:
            key_type_display = "🔑 Hotkey"
            owner_address = key_info.get("owner_address", "N/A")

            # Format owner as "address (name)" if we have the coldkey name
            if owner_address != "N/A" and owner_address in address_to_name:
                owner = f"{owner_address} ({address_to_name[owner_address]})"
            else:
                owner = owner_address

            table.add_row(
                key_info.get("name", "N/A"),
                key_info.get("ss58_address", "N/A"),
                key_type_display,
                owner,
                "✅ Active",
            )

        console.print(table)
        console.print()

        # Capabilities
        console.print(
            Panel(
                CAPABILITIES_TEMPLATE,
                title="[bold blue]🎯 Your Capabilities[/bold blue]",
                border_style="blue",
            )
        )

    except Exception as e:
        print_error(f"Failed to get wallet status: {str(e)}")
        raise typer.Exit(1)


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
        print_success(f" Key '{name}' deleted successfully!")

        if show_guidance:
            from rich.panel import Panel

            guidance_panel = Panel(
                WALLET_DELETE_GUIDANCE_TEMPLATE.format(name=name),
                title="Key Deletion Complete",
                border_style="red",
            )
            console.print(guidance_panel)

    except Exception as e:
        print_error(f"Failed to delete key: {str(e)}")
        raise typer.Exit(1)
