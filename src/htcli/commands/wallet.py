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
    WALLET_STATUS_GUIDANCE_TEMPLATE,
    COLDKEY_RESTORE_GUIDANCE_TEMPLATE,
    HOTKEY_RESTORE_GUIDANCE_TEMPLATE,
    COLDKEY_UPDATE_GUIDANCE_TEMPLATE,
    HOTKEY_UPDATE_GUIDANCE_TEMPLATE,
    BALANCE_GUIDANCE_TEMPLATE,
    TRANSFER_GUIDANCE_TEMPLATE,
)
from src.htcli.helpers.wallet import (
    display_keys_table,
    display_keys_tree,
    prompt_for_coldkey_args,
    prompt_for_delete_args,
    prompt_for_missing_args,
    prompt_for_restore_coldkey_args,
    prompt_for_restore_hotkey_args,
    prompt_for_update_coldkey_args,
    prompt_for_update_hotkey_args,
    prompt_for_balance_args,
    prompt_for_transfer_args,
)

from ..utils.crypto import (
    delete_keypair,
    generate_coldkey_pair,
    generate_hotkey_pair,
    import_keypair,
    import_keypair_from_mnemonic,
    import_hotkey_from_private_key,
    import_hotkey_from_mnemonic,
    list_keys,
    delete_coldkey_and_hotkeys,
    wallet_name_exists,
    update_coldkey,
    update_hotkey,
)
from ..utils.formatting import print_error, print_success
from ..utils.validation import (
    validate_key_type,
    validate_password,
    validate_private_key,
    validate_wallet_name,
    validate_mnemonic,
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
        from src.htcli.errors import HTCLIError
        if isinstance(e, HTCLIError):
            e.display()
        else:
            from src.htcli.errors import handle_and_display_error
            handle_and_display_error(e, "generate-hotkey")
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
        from src.htcli.errors import HTCLIError
        if isinstance(e, HTCLIError):
            e.display()
        else:
            from src.htcli.errors import handle_and_display_error
            handle_and_display_error(e, "generate-coldkey")
        raise typer.Exit(1)


@app.command()
def restore_coldkey(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Coldkey name"),
    private_key: Optional[str] = typer.Option(
        None, "--private-key", "-k", help="Private key (64-character hex)"
    ),
    mnemonic: Optional[str] = typer.Option(
        None, "--mnemonic", "-m", help="Mnemonic phrase (12 or 24 words)"
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
    """Import a coldkey from private key or mnemonic phrase with comprehensive guidance."""

    # Interactive prompting for missing arguments
    name, private_key, mnemonic, key_type, password, show_guidance = prompt_for_restore_coldkey_args(
        name, private_key, mnemonic, key_type, password, show_guidance
    )

    # Validate inputs
    if not validate_wallet_name(name):
        print_error(
            "Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only."
        )
        raise typer.Exit(1)

    # Validate that either private key or mnemonic is provided, but not both
    if not private_key and not mnemonic:
        print_error("Either private key or mnemonic phrase must be provided.")
        raise typer.Exit(1)

    if private_key and mnemonic:
        print_error("Please provide either private key OR mnemonic phrase, not both.")
        raise typer.Exit(1)

    if private_key and not validate_private_key(private_key):
        print_error("Invalid private key format. Should be a 64-character hex string.")
        raise typer.Exit(1)

    if mnemonic and not validate_mnemonic(mnemonic):
        print_error("Invalid mnemonic format. Should be 12 or 24 lowercase words.")
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
        if private_key:
            keypair_info = import_keypair(name, private_key, key_type, password)
            import_method = "private key"
        else:
            keypair_info = import_keypair_from_mnemonic(name, mnemonic, key_type, password)
            import_method = "mnemonic phrase"

        print_success(f"✅ Coldkey imported successfully from {import_method}!")



        if show_guidance:
            from rich.panel import Panel

            guidance_panel = Panel(
                COLDKEY_RESTORE_GUIDANCE_TEMPLATE.format(
                    name=name,
                    address=keypair_info.ss58_address,
                    key_type=key_type,
                    import_method=import_method,
                ),
                title="Coldkey Import Complete",
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
        print_error(f"Failed to import coldkey: {str(e)}")
        raise typer.Exit(1)


@app.command()
def restore_hotkey(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Hotkey name"),
    private_key: Optional[str] = typer.Option(
        None, "--private-key", "-k", help="Private key (64-character hex)"
    ),
    mnemonic: Optional[str] = typer.Option(
        None, "--mnemonic", "-m", help="Mnemonic phrase (12 or 24 words)"
    ),
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
    """Import a hotkey from private key or mnemonic phrase with comprehensive guidance."""

    # Interactive prompting for missing arguments
    name, private_key, mnemonic, owner_name, key_type, password, show_guidance = prompt_for_restore_hotkey_args(
        name, private_key, mnemonic, owner_name, key_type, password, show_guidance
    )

    # Validate inputs
    if not validate_wallet_name(name):
        print_error(
            "Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only."
        )
        raise typer.Exit(1)

    # Validate that either private key or mnemonic is provided, but not both
    if not private_key and not mnemonic:
        print_error("Either private key or mnemonic phrase must be provided.")
        raise typer.Exit(1)

    if private_key and mnemonic:
        print_error("Please provide either private key OR mnemonic phrase, not both.")
        raise typer.Exit(1)

    if private_key and not validate_private_key(private_key):
        print_error("Invalid private key format. Should be a 64-character hex string.")
        raise typer.Exit(1)

    if mnemonic and not validate_mnemonic(mnemonic):
        print_error("Invalid mnemonic format. Should be 12 or 24 lowercase words.")
        raise typer.Exit(1)

    if not validate_key_type(key_type):
        print_error("Invalid key type. Use 'sr25519' or 'ed25519'.")
        raise typer.Exit(1)

    if password and not validate_password(password):
        print_error(
            "Invalid password. Must be at least 8 characters with letters and numbers."
        )
        raise typer.Exit(1)

    # Get owner address from owner name
    try:
        from ..utils.crypto import get_wallet_info_by_name
        owner_wallet_info = get_wallet_info_by_name(owner_name)
        if owner_wallet_info.get("is_hotkey", False):
            print_error(f"'{owner_name}' is a hotkey. Please provide a coldkey wallet name as the owner.")
            raise typer.Exit(1)
        owner_address = owner_wallet_info["ss58_address"]
    except FileNotFoundError:
        print_error(f"Owner wallet '{owner_name}' not found. Please provide an existing coldkey wallet name.")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Error validating owner wallet '{owner_name}': {str(e)}")
        raise typer.Exit(1)

    try:
        if private_key:
            keypair_info = import_hotkey_from_private_key(name, private_key, owner_address, key_type, password)
            import_method = "private key"
        else:
            keypair_info = import_hotkey_from_mnemonic(name, mnemonic, owner_address, key_type, password)
            import_method = "mnemonic phrase"

        print_success(f"✅ Hotkey imported successfully from {import_method}!")

        if show_guidance:
            from rich.panel import Panel

            guidance_panel = Panel(
                HOTKEY_RESTORE_GUIDANCE_TEMPLATE.format(
                    name=name,
                    address=keypair_info.ss58_address,
                    key_type=key_type,
                    import_method=import_method,
                    owner_name=owner_name,
                    owner_address=owner_address,
                ),
                title="Hotkey Import Complete",
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
        print_error(f"Failed to import hotkey: {str(e)}")
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
    names: Optional[str] = typer.Argument(None, help="Key names to delete (comma-separated for multiple)"),
    confirm: bool = typer.Option(
        False, "--confirm", "-y", help="Skip confirmation prompt"
    ),
    show_guidance: Optional[bool] = typer.Option(
        None, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Delete one or more stored keys with comprehensive guidance."""

    # Parse names string into list
    name_list = None
    if names:
        name_list = [n.strip() for n in names.split(",") if n.strip()]

    # Interactive prompting for missing arguments
    name_list, confirm, show_guidance = prompt_for_delete_args(name_list, confirm, show_guidance)

    # Validate all wallet names
    for name in name_list:
        if not validate_wallet_name(name):
            print_error(f"Invalid wallet name: {name}")
            raise typer.Exit(1)

    try:
        # Track deletion results
        deleted_coldkeys = []
        deleted_hotkeys = []
        total_associated_hotkeys_deleted = 0

        # Process each key
        for name in name_list:
            # Check if this is a coldkey and has associated hotkeys
            from ..utils.crypto import get_wallet_info_by_name
            wallet_info = get_wallet_info_by_name(name)
            is_coldkey = not wallet_info.get("is_hotkey", False)

            if is_coldkey:
                # Check for associated hotkeys
                all_keys = list_keys()
                coldkey_address = wallet_info["ss58_address"]
                associated_hotkeys = []

                for key_info in all_keys:
                    if (key_info.get("is_hotkey", False) and
                        key_info.get("owner_address") == coldkey_address):
                        associated_hotkeys.append(key_info["name"])

                if associated_hotkeys:
                    # Show warning about associated hotkeys
                    console.print(f"\n[yellow]⚠️  Warning:[/yellow] Coldkey '{name}' has {len(associated_hotkeys)} associated hotkey(s):")
                    for hotkey in associated_hotkeys:
                        console.print(f"   • {hotkey}")
                    console.print(f"[yellow]All associated hotkeys will be deleted together with the coldkey '{name}'.[/yellow]")

                    # Delete coldkey and all associated hotkeys
                    result = delete_coldkey_and_hotkeys(name)
                    deleted_coldkeys.append(name)
                    total_associated_hotkeys_deleted += result['total_hotkeys_deleted']
                    print_success(f"✅ Coldkey '{name}' and {result['total_hotkeys_deleted']} associated hotkeys deleted successfully!")
                else:
                    # No associated hotkeys, proceed with normal deletion
                    delete_keypair(name)
                    deleted_coldkeys.append(name)
                    print_success(f"✅ Coldkey '{name}' deleted successfully!")
            else:
                # It's a hotkey, proceed with normal deletion
                delete_keypair(name)
                deleted_hotkeys.append(name)
                print_success(f"✅ Hotkey '{name}' deleted successfully!")

        # Show summary
        if len(name_list) > 1:
            console.print(f"\n[bold green]🎉 Bulk Deletion Complete![/bold green]")
            console.print(f"[bold]Summary:[/bold] {len(deleted_coldkeys)} coldkeys, {len(deleted_hotkeys)} hotkeys deleted")
            if total_associated_hotkeys_deleted > 0:
                console.print(f"[bold]Additional hotkeys deleted due to coldkey associations:[/bold] {total_associated_hotkeys_deleted}")

        # Show guidance if requested
        if show_guidance:
            from rich.panel import Panel

            if len(name_list) == 1:
                # Single key deletion - show detailed guidance
                name = name_list[0]
                if name in deleted_coldkeys:
                    guidance_panel = Panel(
                        f"[bold red]🗑️ Coldkey Deleted Successfully[/bold red]\n\n"
                        f"[bold]Deleted Coldkey:[/bold] {name}\n\n"
                        f"[bold]What happened?[/bold]\n"
                        f"• The coldkey has been permanently removed\n"
                        f"• All encrypted private key files have been deleted\n"
                        f"• You can no longer use this key for operations\n\n"
                        f"[bold]Important Notes:[/bold]\n"
                        f"• If you had funds associated with the coldkey, they are still on the blockchain\n"
                        f"• You can recover them by importing the private key again\n"
                        f"• Make sure you have a backup of the private keys if needed\n\n"
                        f"[yellow]⚠️ Warning:[/yellow] This action cannot be undone!",
                        title="Coldkey Deletion Complete",
                        border_style="red",
                    )
                else:
                    guidance_panel = Panel(
                        f"[bold red]🗑️ Hotkey Deleted Successfully[/bold red]\n\n"
                        f"[bold]Deleted Hotkey:[/bold] {name}\n\n"
                        f"[bold]What happened?[/bold]\n"
                        f"• The hotkey has been permanently removed\n"
                        f"• All encrypted private key files have been deleted\n"
                        f"• You can no longer use this key for operations\n\n"
                        f"[yellow]⚠️ Warning:[/yellow] This action cannot be undone!",
                        title="Hotkey Deletion Complete",
                        border_style="red",
                    )
                console.print(guidance_panel)
            else:
                # Multiple key deletion - show summary guidance
                guidance_panel = Panel(
                    f"[bold red]🗑️ Bulk Deletion Complete[/bold red]\n\n"
                    f"[bold]Deleted Keys:[/bold]\n"
                    f"• Coldkeys: {', '.join(deleted_coldkeys) if deleted_coldkeys else 'None'}\n"
                    f"• Hotkeys: {', '.join(deleted_hotkeys) if deleted_hotkeys else 'None'}\n"
                    f"• Additional hotkeys (from coldkey associations): {total_associated_hotkeys_deleted}\n\n"
                    f"[bold]What happened?[/bold]\n"
                    f"• All specified keys have been permanently removed\n"
                    f"• All encrypted private key files have been deleted\n"
                    f"• Associated hotkeys were automatically deleted with their coldkeys\n\n"
                    f"[yellow]⚠️ Warning:[/yellow] This action cannot be undone!",
                    title="Bulk Deletion Complete",
                    border_style="red",
                )
                console.print(guidance_panel)

    except Exception as e:
        from src.htcli.errors import HTCLIError
        if isinstance(e, HTCLIError):
            e.display()
        else:
            from src.htcli.errors import handle_and_display_error
            handle_and_display_error(e, "delete")
        raise typer.Exit(1)


@app.command(name="update-coldkey")
def update_coldkey_cmd(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Current coldkey name"),
    new_name: Optional[str] = typer.Option(None, "--new-name", help="New coldkey name"),
    new_password: Optional[str] = typer.Option(None, "--new-password", help="New password"),
    remove_password: bool = typer.Option(False, "--remove-password", help="Remove password protection"),
    show_guidance: Optional[bool] = typer.Option(
        None, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Update a coldkey's properties (name, password)."""

    # Interactive prompting for missing arguments
    name, new_name, new_password, remove_password, show_guidance = prompt_for_update_coldkey_args(
        name, new_name, new_password, remove_password, show_guidance
    )

    # Validate inputs
    if not validate_wallet_name(name):
        print_error("Invalid current wallet name.")
        raise typer.Exit(1)

    if new_name and not validate_wallet_name(new_name):
        print_error("Invalid new wallet name.")
        raise typer.Exit(1)

    if new_password and not validate_password(new_password):
        print_error("Invalid new password. Must be at least 8 characters with letters and numbers.")
        raise typer.Exit(1)

    try:
        result = update_coldkey(name, new_name, new_password, remove_password)
        print_success("✅ Coldkey updated successfully!")

        if show_guidance:
            from rich.panel import Panel
            guidance_panel = Panel(
                COLDKEY_UPDATE_GUIDANCE_TEMPLATE.format(
                    old_name=result["old_name"],
                    new_name=result["new_name"],
                    key_type=result["key_type"],
                    ss58_address=result["ss58_address"],
                    name_updated_status="✅ Yes" if result["name_updated"] else "❌ No",
                    password_updated_status="✅ Yes" if result["password_updated"] else "❌ No",
                ),
                title="Coldkey Update Complete",
                border_style="green",
            )
            console.print(guidance_panel)
        else:
            # Display update information
            console.print(f"Name: {result['old_name']} → {result['new_name']}")
            console.print(f"Type: {result['key_type']}")
            console.print(f"Address: {result['ss58_address']}")
            if result["name_updated"]:
                console.print("✅ Name updated")
            if result["password_updated"]:
                console.print("✅ Password updated")

    except Exception as e:
        print_error(f"Failed to update coldkey: {str(e)}")
        raise typer.Exit(1)


@app.command(name="update-hotkey")
def update_hotkey_cmd(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Current hotkey name"),
    new_name: Optional[str] = typer.Option(None, "--new-name", help="New hotkey name"),
    new_password: Optional[str] = typer.Option(None, "--new-password", help="New password"),
    remove_password: bool = typer.Option(False, "--remove-password", help="Remove password protection"),
    new_owner: Optional[str] = typer.Option(None, "--new-owner", help="New coldkey owner name"),
    show_guidance: Optional[bool] = typer.Option(
        None, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Update a hotkey's properties (name, password, owner)."""

    # Interactive prompting for missing arguments
    name, new_name, new_password, remove_password, new_owner, show_guidance = prompt_for_update_hotkey_args(
        name, new_name, new_password, remove_password, new_owner, show_guidance
    )

    # Validate inputs
    if not validate_wallet_name(name):
        print_error("Invalid current wallet name.")
        raise typer.Exit(1)

    if new_name and not validate_wallet_name(new_name):
        print_error("Invalid new wallet name.")
        raise typer.Exit(1)

    if new_password and not validate_password(new_password):
        print_error("Invalid new password. Must be at least 8 characters with letters and numbers.")
        raise typer.Exit(1)

    try:
        result = update_hotkey(name, new_name, new_password, remove_password, new_owner)
        print_success("✅ Hotkey updated successfully!")

        if show_guidance:
            from rich.panel import Panel
            guidance_panel = Panel(
                HOTKEY_UPDATE_GUIDANCE_TEMPLATE.format(
                    old_name=result["old_name"],
                    new_name=result["new_name"],
                    key_type=result["key_type"],
                    ss58_address=result["ss58_address"],
                    old_owner_address=result["old_owner_address"],
                    new_owner_address=result["new_owner_address"],
                    name_updated_status="✅ Yes" if result["name_updated"] else "❌ No",
                    password_updated_status="✅ Yes" if result["password_updated"] else "❌ No",
                    owner_updated_status="✅ Yes" if result["owner_updated"] else "❌ No",
                ),
                title="Hotkey Update Complete",
                border_style="green",
            )
            console.print(guidance_panel)
        else:
            # Display update information
            console.print(f"Name: {result['old_name']} → {result['new_name']}")
            console.print(f"Type: {result['key_type']}")
            console.print(f"Address: {result['ss58_address']}")
            if result["name_updated"]:
                console.print("✅ Name updated")
            if result["password_updated"]:
                console.print("✅ Password updated")
            if result["owner_updated"]:
                console.print(f"✅ Owner updated: {result['old_owner_address']} → {result['new_owner_address']}")

    except Exception as e:
        print_error(f"Failed to update hotkey: {str(e)}")
        raise typer.Exit(1)


@app.command()
def balance(
    wallet_name: Optional[str] = typer.Option(None, "--wallet", "-w", help="Wallet name to check balance"),
    address: Optional[str] = typer.Option(None, "--address", "-a", help="Address to check balance"),
    format_type: str = typer.Option(
        "table", "--format", "-f", help="Output format (table/json)"
    ),
    show_guidance: Optional[bool] = typer.Option(
        None, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Check balance of a wallet or address."""

    # Interactive prompting for missing arguments
    wallet_name, address, format_type, show_guidance = prompt_for_balance_args(
        wallet_name, address, format_type, show_guidance
    )

    # Get client for blockchain operations
    from ..dependencies import get_client
    client = get_client()

    try:
        # If wallet name provided, get the address from the wallet
        if wallet_name:
            from ..utils.crypto import get_wallet_info_by_name
            wallet_info = get_wallet_info_by_name(wallet_name)
            address = wallet_info["ss58_address"]
            wallet_type = "Hotkey" if wallet_info.get("is_hotkey", False) else "Coldkey"
        else:
            wallet_type = "External Address"

        # Get balance from blockchain
        response = client.get_balance(address)
        if response.success:
            balance_data = response.data

            if show_guidance:
                from rich.panel import Panel
                guidance_panel = Panel(
                    BALANCE_GUIDANCE_TEMPLATE.format(
                        wallet_name=wallet_name or "N/A",
                        address=address,
                        wallet_type=wallet_type,
                        formatted_balance=balance_data.get('formatted_balance', 'N/A'),
                        raw_balance=balance_data.get('balance', 'N/A'),
                        unit=balance_data.get('unit', 'HT'),
                    ),
                    title="Balance Information",
                    border_style="blue",
                )
                console.print(guidance_panel)
            else:
                if format_type == "json":
                    console.print_json(data=balance_data)
                else:
                    console.print(f"[bold]Wallet:[/bold] {wallet_name or 'External Address'}")
                    console.print(f"[bold]Address:[/bold] {address}")
                    console.print(f"[bold]Type:[/bold] {wallet_type}")
                    console.print(f"[bold]Balance:[/bold] {balance_data.get('formatted_balance', 'N/A')}")
                    console.print(f"[bold]Raw Balance:[/bold] {balance_data.get('balance', 'N/A')}")

                    # Add helpful information if balance is 0
                    from src.htcli.errors import display_balance_info
                    display_balance_info(address, balance_data.get('balance', 0))
        else:
            print_error(f"Failed to retrieve balance: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"Failed to get balance: {str(e)}")
        raise typer.Exit(1)


@app.command()
def transfer(
    from_wallet: Optional[str] = typer.Option(None, "--from", "-f", help="Source wallet name"),
    to_address: Optional[str] = typer.Option(None, "--to", "-t", help="Destination address"),
    amount: Optional[str] = typer.Option(None, "--amount", "-a", help="Amount to transfer"),
    password: Optional[str] = typer.Option(None, "--password", "-p", help="Wallet password"),
    show_guidance: Optional[bool] = typer.Option(
        None, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Transfer balance from one wallet to another address."""

    # Interactive prompting for missing arguments
    from_wallet, to_address, amount, password, show_guidance = prompt_for_transfer_args(
        from_wallet, to_address, amount, password, show_guidance
    )

    # Get client for blockchain operations
    from ..dependencies import get_client
    client = get_client()

    try:
        # Load the source wallet
        from ..utils.crypto import get_wallet_info_by_name, load_keypair
        wallet_info = get_wallet_info_by_name(from_wallet)

        # Verify it's a coldkey (only coldkeys can transfer funds)
        if wallet_info.get("is_hotkey", False):
            print_error(f"'{from_wallet}' is a hotkey. Only coldkeys can transfer funds.")
            raise typer.Exit(1)

        # Load the keypair
        keypair = load_keypair(from_wallet, password)

        # Validate destination address or resolve wallet name
        from ..utils.validation import validate_address
        if not validate_address(to_address):
            # If not a valid address, try to treat it as a wallet name
            if validate_wallet_name(to_address):
                try:
                    # Check if wallet exists and get its address
                    dest_wallet_info = get_wallet_info_by_name(to_address)
                    console.print(f"[green]✓[/green] Resolved wallet '{to_address}' to address: {dest_wallet_info['ss58_address']}")
                    to_address = dest_wallet_info["ss58_address"]
                except FileNotFoundError:
                    print_error(f"Destination wallet '{to_address}' not found.")
                    raise typer.Exit(1)
                except Exception as e:
                    print_error(f"Error accessing destination wallet '{to_address}': {str(e)}")
                    raise typer.Exit(1)
            else:
                print_error("Invalid destination address or wallet name format.")
                raise typer.Exit(1)

        # Perform the transfer
        response = client.transfer_funds(
            from_address=wallet_info["ss58_address"],
            to_address=to_address,
            amount=amount,
            keypair=keypair
        )

        if response.success:
            transfer_data = response.data

            if show_guidance:
                from rich.panel import Panel
                guidance_panel = Panel(
                    TRANSFER_GUIDANCE_TEMPLATE.format(
                        from_wallet=from_wallet,
                        from_address=wallet_info["ss58_address"],
                        to_address=to_address,
                        amount=amount,
                        tx_hash=transfer_data.get('tx_hash', 'N/A'),
                        block_number=transfer_data.get('block_number', 'N/A'),
                        fee=transfer_data.get('fee', 'N/A'),
                    ),
                    title="Transfer Complete",
                    border_style="green",
                )
                console.print(guidance_panel)
            else:
                console.print(f"[bold green]✅ Transfer successful![/bold green]")
                console.print(f"[bold]From:[/bold] {from_wallet} ({wallet_info['ss58_address']})")
                console.print(f"[bold]To:[/bold] {to_address}")
                console.print(f"[bold]Amount:[/bold] {amount}")
                console.print(f"[bold]Transaction Hash:[/bold] {transfer_data.get('tx_hash', 'N/A')}")
                console.print(f"[bold]Block Number:[/bold] {transfer_data.get('block_number', 'N/A')}")
                console.print(f"[bold]Fee:[/bold] {transfer_data.get('fee', 'N/A')}")
        else:
            print_error(f"Transfer failed: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        from src.htcli.errors import HTCLIError
        if isinstance(e, HTCLIError):
            e.display()
        else:
            from src.htcli.errors import handle_and_display_error
            handle_and_display_error(e, "transfer")
        raise typer.Exit(1)
