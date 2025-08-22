from typing import Optional

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt

from src.htcli.utils.crypto import list_keys, get_wallet_info_by_name
from src.htcli.utils.formatting import print_error
from src.htcli.utils.validation import (
    validate_password,
    validate_private_key,
    validate_wallet_name,
    validate_mnemonic,
)

console = Console()


def prompt_for_missing_args(
    name: Optional[str] = None,
    owner_name: Optional[str] = None,
    key_type: Optional[str] = None,
    password: Optional[str] = None,
    show_guidance: Optional[bool] = None,
) -> tuple[str, str, str, str, Optional[str], bool]:
    """Interactive prompt for missing arguments."""

    # Prompt for name if missing
    if not name:
        while True:
            name = Prompt.ask("Enter hotkey name", default="my-hotkey")
            if validate_wallet_name(name):
                break
            print_error(
                "Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only."
            )

    # Prompt for owner wallet name if missing
    if not owner_name:
        while True:
            owner_name = Prompt.ask("Enter coldkey wallet name that owns this hotkey")
            try:
                # Validate that the wallet exists and is a coldkey
                wallet_info = get_wallet_info_by_name(owner_name)
                if wallet_info.get("is_hotkey", False):
                    print_error(f"'{owner_name}' is a hotkey. Please provide a coldkey wallet name.")
                    continue
                break
            except FileNotFoundError:
                print_error(f"Coldkey wallet '{owner_name}' not found. Please provide an existing coldkey wallet name.")
            except Exception as e:
                print_error(f"Error accessing wallet '{owner_name}': {str(e)}")

    # Get the owner address from the wallet name
    try:
        wallet_info = get_wallet_info_by_name(owner_name)
        owner_address = wallet_info["ss58_address"]
    except Exception as e:
        print_error(f"Failed to get address for wallet '{owner_name}': {str(e)}")
        raise typer.Exit(1)

    # Prompt for key type if missing
    if not key_type:
        key_type = Prompt.ask(
            "Enter key type", choices=["sr25519", "ed25519"], default="sr25519"
        )

    # Prompt for password (optional)
    if password is None:
        use_password = Confirm.ask(
            "Do you want to set a password for this hotkey?", default=False
        )
        if use_password:
            while True:
                password = Prompt.ask(
                    "Enter password (min 8 chars, letters + numbers)", password=True
                )
                if validate_password(password):
                    break
                print_error(
                    "Invalid password. Must be at least 8 characters with letters and numbers."
                )
        else:
            password = None

    # Prompt for guidance (optional)
    if show_guidance is None:
        show_guidance = Confirm.ask("Show comprehensive guidance?", default=True)

    return name, owner_address, key_type, owner_name, password, show_guidance


def prompt_for_coldkey_args(
    name: Optional[str] = None,
    key_type: Optional[str] = None,
    password: Optional[str] = None,
    show_guidance: Optional[bool] = None,
) -> tuple[str, str, Optional[str], bool]:
    """Interactive prompt for coldkey arguments."""

    # Prompt for name if missing
    if not name:
        while True:
            name = Prompt.ask("Enter coldkey name", default="my-coldkey")
            if validate_wallet_name(name):
                break
            print_error(
                "Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only."
            )

    # Prompt for key type if missing
    if not key_type:
        key_type = Prompt.ask(
            "Enter key type", choices=["sr25519", "ed25519"], default="sr25519"
        )

    # Prompt for password (optional)
    if password is None:
        use_password = Confirm.ask(
            "Do you want to set a password for this coldkey?", default=False
        )
        if use_password:
            while True:
                password = Prompt.ask(
                    "Enter password (min 8 chars, letters + numbers)", password=True
                )
                if validate_password(password):
                    break
                print_error(
                    "Invalid password. Must be at least 8 characters with letters and numbers."
                )
        else:
            password = None

    # Prompt for guidance (optional)
    if show_guidance is None:
        show_guidance = Confirm.ask("Show comprehensive guidance?", default=True)

    return name, key_type, password, show_guidance


def prompt_for_restore_args(
    name: Optional[str] = None,
    private_key: Optional[str] = None,
    mnemonic: Optional[str] = None,
    key_type: Optional[str] = None,
    password: Optional[str] = None,
    show_guidance: Optional[bool] = None,
) -> tuple[str, Optional[str], Optional[str], str, Optional[str], bool]:
    """Interactive prompt for restore arguments."""

    # Prompt for name if missing
    if not name:
        while True:
            name = Prompt.ask("Enter key name", default="imported-key")
            if validate_wallet_name(name):
                break
            print_error(
                "Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only."
            )

    # Prompt for import method if neither private key nor mnemonic is provided
    if not private_key and not mnemonic:
        import_method = Prompt.ask(
            "Choose import method", 
            choices=["private-key", "mnemonic"], 
            default="mnemonic"
        )
    else:
        import_method = "private-key" if private_key else "mnemonic"

    # Prompt for private key or mnemonic based on chosen method
    if import_method == "private-key" and not private_key:
        while True:
            private_key = Prompt.ask(
                "Enter private key (64-character hex)", password=True
            )
            if validate_private_key(private_key):
                break
            print_error(
                "Invalid private key format. Should be a 64-character hex string."
            )
    elif import_method == "mnemonic" and not mnemonic:
        while True:
            mnemonic = Prompt.ask(
                "Enter mnemonic phrase (12 or 24 words)", password=True
            )
            if validate_mnemonic(mnemonic):
                break
            print_error(
                "Invalid mnemonic format. Should be 12 or 24 lowercase words."
            )

    # Prompt for key type if missing
    if not key_type:
        key_type = Prompt.ask(
            "Enter key type", choices=["sr25519", "ed25519"], default="sr25519"
        )

    # Prompt for password (optional)
    if password is None:
        use_password = Confirm.ask(
            "Do you want to set a password for this imported key?", default=False
        )
        if use_password:
            while True:
                password = Prompt.ask(
                    "Enter password (min 8 chars, letters + numbers)", password=True
                )
                if validate_password(password):
                    break
                print_error(
                    "Invalid password. Must be at least 8 characters with letters and numbers."
                )
        else:
            password = None

    # Prompt for guidance (optional)
    if show_guidance is None:
        show_guidance = Confirm.ask("Show comprehensive guidance?", default=True)

    return name, private_key, mnemonic, key_type, password, show_guidance


def display_keys_tree(keys: list):
    """Display keys in hierarchical tree format."""
    from collections import defaultdict

    # Separate coldkeys and hotkeys
    coldkeys = [k for k in keys if not k.get("is_hotkey", False)]
    hotkeys = [k for k in keys if k.get("is_hotkey", False)]

    # Group hotkeys by owner
    hotkeys_by_owner = defaultdict(list)
    for hotkey in hotkeys:
        owner = hotkey.get("owner_address")
        if owner:
            hotkeys_by_owner[owner].append(hotkey)

    # Display coldkeys with their hotkeys
    for i, coldkey in enumerate(coldkeys):
        coldkey_name = coldkey.get("name", "N/A")
        coldkey_address = coldkey.get("ss58_address", "N/A")

        # Display coldkey on one line
        console.print(
            f"[purple]Coldkey[/purple] [cyan]{coldkey_name}[/cyan] [white]ss58_address[/white]: [green]{coldkey_address}[/green]"
        )

        # Find and display hotkeys owned by this coldkey
        owned_hotkeys = hotkeys_by_owner.get(coldkey_address, [])
        for j, hotkey in enumerate(owned_hotkeys):
            hotkey_name = hotkey.get("name", "N/A")
            hotkey_address = hotkey.get("ss58_address", "N/A")

            # Use L-shaped connector for hotkeys
            if j == len(owned_hotkeys) - 1:
                # Last hotkey - use └──
                connector = "    └── "
            else:
                # Not last hotkey - use ├──
                connector = "    ├── "

            console.print(
                f"{connector}[red]Hotkey[/red] [cyan]{hotkey_name}[/cyan] [white]ss58_address[/white]: [green]{hotkey_address}[/green]"
            )

        # Add spacing between coldkeys
        if i < len(coldkeys) - 1:
            console.print()

    # Display orphaned hotkeys (hotkeys without a coldkey owner)
    orphaned_hotkeys = [h for h in hotkeys if not h.get("owner_address")]
    if orphaned_hotkeys:
        if coldkeys:  # Add spacing if we had coldkeys
            console.print()

        console.print("[yellow]Orphaned Hotkeys (no owner):[/yellow]")
        for i, hotkey in enumerate(orphaned_hotkeys):
            hotkey_name = hotkey.get("name", "N/A")
            hotkey_address = hotkey.get("ss58_address", "N/A")

            if i == len(orphaned_hotkeys) - 1:
                connector = "└── "
            else:
                connector = "├── "

            console.print(
                f"{connector}[red]Hotkey[/red] [cyan]{hotkey_name}[/cyan] [white]ss58_address[/white]: [green]{hotkey_address}[/green]"
            )

    # Show summary
    console.print(
        f"\n[bold]Summary:[/bold] {len(coldkeys)} coldkeys, {len(hotkeys)} hotkeys"
    )


def display_keys_table(keys: list):
    """Display keys in table format with hotkey/coldkey distinction."""
    from rich.table import Table

    # Create table
    table = Table(
        title="[bold cyan]Stored Keys[/bold cyan]",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Type", style="yellow")
    table.add_column("Key Type", style="blue")
    table.add_column("Address (SS58)", style="green")
    table.add_column("Owner", style="purple")
    table.add_column("Encrypted", style="white")

    # Separate coldkeys and hotkeys for better organization
    coldkeys = [k for k in keys if not k.get("is_hotkey", False)]
    hotkeys = [k for k in keys if k.get("is_hotkey", False)]

    # Create a mapping of addresses to coldkey names for better owner display
    address_to_name = {}
    for key_info in coldkeys:
        address_to_name[key_info.get("ss58_address")] = key_info.get("name")

    # Add coldkeys first
    for key_info in coldkeys:
        key_type_display = "🔐 Coldkey"
        owner = "N/A"
        encrypted_status = "✅ Yes" if key_info.get("is_encrypted", True) else "❌ No"

        table.add_row(
            key_info.get("name", "N/A"),
            key_info.get("key_type", "N/A"),
            key_type_display,
            key_info.get("ss58_address", "N/A"),
            owner,
            encrypted_status,
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

        encrypted_status = "✅ Yes" if key_info.get("is_encrypted", True) else "❌ No"

        table.add_row(
            key_info.get("name", "N/A"),
            key_info.get("key_type", "N/A"),
            key_type_display,
            key_info.get("ss58_address", "N/A"),
            owner,
            encrypted_status,
        )

    # Display table
    console.print(table)

    # Show summary
    console.print(
        f"\n[bold]Summary:[/bold] {len(coldkeys)} coldkeys, {len(hotkeys)} hotkeys"
    )


def prompt_for_delete_args(
    name: Optional[str] = None,
    confirm: Optional[bool] = None,
    show_guidance: Optional[bool] = None,
) -> tuple[str, bool, bool]:
    """Interactive prompt for delete arguments."""

    # Prompt for name if missing
    if not name:
        # First show available keys
        keys = list_keys()
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
                key_names = [k["name"] for k in keys]
                if name in key_names:
                    break
                else:
                    print_error(
                        f"Key '{name}' not found. Please choose from the list above."
                    )
            else:
                print_error(
                    "Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only."
                )

    # Prompt for confirmation if not provided
    if confirm is None:
        confirm = Confirm.ask(
            f"Are you sure you want to delete key '{name}'?", default=False
        )

    # Prompt for guidance if not provided
    if show_guidance is None:
        show_guidance = Confirm.ask("Show comprehensive guidance?", default=True)

    return name, confirm, show_guidance
