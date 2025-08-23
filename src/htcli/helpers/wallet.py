from typing import Optional, List, Dict, Any

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from src.htcli.utils.crypto import list_keys, get_wallet_info_by_name, wallet_name_exists
from src.htcli.utils.formatting import print_error
from src.htcli.utils.validation import (
    validate_password,
    validate_private_key,
    validate_wallet_name,
    validate_mnemonic,
    validate_address,
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
                # Check if wallet name already exists
                if wallet_name_exists(name):
                    print_error(f"Wallet name '{name}' already exists. Please choose a different name.")
                    continue
                break
            print_error(
                "Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only."
            )
    else:
        # Check if provided name already exists
        if wallet_name_exists(name):
            print_error(f"Wallet name '{name}' already exists. Please choose a different name.")
            raise typer.Exit(1)

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
                # Check if wallet name already exists
                if wallet_name_exists(name):
                    print_error(f"Wallet name '{name}' already exists. Please choose a different name.")
                    continue
                break
            print_error(
                "Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only."
            )
    else:
        # Check if provided name already exists
        if wallet_name_exists(name):
            print_error(f"Wallet name '{name}' already exists. Please choose a different name.")
            raise typer.Exit(1)

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


def prompt_for_restore_coldkey_args(
    name: Optional[str] = None,
    private_key: Optional[str] = None,
    mnemonic: Optional[str] = None,
    key_type: Optional[str] = None,
    password: Optional[str] = None,
    show_guidance: Optional[bool] = None,
) -> tuple[str, Optional[str], Optional[str], str, Optional[str], bool]:
    """Interactive prompt for coldkey restore arguments."""

    # Prompt for name if missing
    if not name:
        while True:
            name = Prompt.ask("Enter coldkey name", default="imported-coldkey")
            if validate_wallet_name(name):
                # Check if wallet name already exists
                if wallet_name_exists(name):
                    print_error(f"Wallet name '{name}' already exists. Please choose a different name.")
                    continue
                break
            print_error(
                "Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only."
            )
    else:
        # Check if provided name already exists
        if wallet_name_exists(name):
            print_error(f"Wallet name '{name}' already exists. Please choose a different name.")
            raise typer.Exit(1)

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
            "Do you want to set a password for this imported coldkey?", default=False
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


def prompt_for_restore_hotkey_args(
    name: Optional[str] = None,
    private_key: Optional[str] = None,
    mnemonic: Optional[str] = None,
    owner_name: Optional[str] = None,
    key_type: Optional[str] = None,
    password: Optional[str] = None,
    show_guidance: Optional[bool] = None,
) -> tuple[str, Optional[str], Optional[str], str, str, Optional[str], bool]:
    """Interactive prompt for hotkey restore arguments."""

    # Prompt for name if missing
    if not name:
        while True:
            name = Prompt.ask("Enter hotkey name", default="imported-hotkey")
            if validate_wallet_name(name):
                # Check if wallet name already exists
                if wallet_name_exists(name):
                    print_error(f"Wallet name '{name}' already exists. Please choose a different name.")
                    continue
                break
            print_error(
                "Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only."
            )
    else:
        # Check if provided name already exists
        if wallet_name_exists(name):
            print_error(f"Wallet name '{name}' already exists. Please choose a different name.")
            raise typer.Exit(1)

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

    # Prompt for key type if missing
    if not key_type:
        key_type = Prompt.ask(
            "Enter key type", choices=["sr25519", "ed25519"], default="sr25519"
        )

    # Prompt for password (optional)
    if password is None:
        use_password = Confirm.ask(
            "Do you want to set a password for this imported hotkey?", default=False
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

    return name, private_key, mnemonic, owner_name, key_type, password, show_guidance


def display_keys_tree(keys: list):
    """Display keys in hierarchical tree format."""
    from collections import defaultdict

    # Separate coldkeys and hotkeys
    coldkeys = [k for k in keys if not k.get("is_hotkey", False)]
    hotkeys = [k for k in keys if k.get("is_hotkey", False)]

    # Create a set of coldkey addresses for quick lookup
    coldkey_addresses = {coldkey.get("ss58_address") for coldkey in coldkeys}

    # Group hotkeys by owner
    hotkeys_by_owner = defaultdict(list)
    orphaned_hotkeys = []

    for hotkey in hotkeys:
        owner_address = hotkey.get("owner_address")
        if owner_address and owner_address in coldkey_addresses:
            # Valid owner - add to grouped hotkeys
            hotkeys_by_owner[owner_address].append(hotkey)
        else:
            # Orphaned hotkey - no valid owner
            orphaned_hotkeys.append(hotkey)

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

    # Display orphaned hotkeys (hotkeys without a valid coldkey owner)
    if orphaned_hotkeys:
        if coldkeys:  # Add spacing if we had coldkeys
            console.print()

        console.print("[yellow]Orphaned Hotkeys (no valid owner):[/yellow]")
        for i, hotkey in enumerate(orphaned_hotkeys):
            hotkey_name = hotkey.get("name", "N/A")
            hotkey_address = hotkey.get("ss58_address", "N/A")
            owner_address = hotkey.get("owner_address", "N/A")

            if i == len(orphaned_hotkeys) - 1:
                connector = "└── "
            else:
                connector = "├── "

            console.print(
                f"{connector}[red]Hotkey[/red] [cyan]{hotkey_name}[/cyan] [white]ss58_address[/white]: [green]{hotkey_address}[/green] [white](owner: {owner_address})[/white]"
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
    names: Optional[list] = None,
    confirm: Optional[bool] = None,
    show_guidance: Optional[bool] = None,
) -> tuple[list, bool, bool]:
    """Interactive prompt for delete arguments."""

    # Prompt for names if missing
    if not names:
        # First show available keys
        keys = list_keys()
        if not keys:
            print_error("No keys found to delete.")
            raise typer.Exit(1)

        console.print("\n[bold]Available keys:[/bold]")
        for i, key in enumerate(keys, 1):
            console.print(f"{i}. {key['name']} ({key['ss58_address']})")

        names = []
        while True:
            name_input = Prompt.ask("\nEnter key name(s) to delete (comma-separated for multiple)")
            name_list = [n.strip() for n in name_input.split(",") if n.strip()]

            if not name_list:
                print_error("Please enter at least one key name.")
                continue

            # Validate all names
            valid_names = []
            key_names = [k["name"] for k in keys]

            for name in name_list:
                if validate_wallet_name(name):
                    if name in key_names:
                        valid_names.append(name)
                    else:
                        print_error(f"Key '{name}' not found. Please choose from the list above.")
                else:
                    print_error(f"Invalid wallet name '{name}'. Use alphanumeric characters, hyphens, and underscores only.")

            if valid_names:
                names = valid_names
                break

    # Prompt for confirmation if not provided
    if confirm is None:
        if len(names) == 1:
            confirm = Confirm.ask(
                f"Are you sure you want to delete key '{names[0]}'?", default=False
            )
        else:
            confirm = Confirm.ask(
                f"Are you sure you want to delete {len(names)} keys: {', '.join(names)}?", default=False
            )

    # Prompt for guidance if not provided
    if show_guidance is None:
        show_guidance = Confirm.ask("Show comprehensive guidance?", default=True)

    return names, confirm, show_guidance


def prompt_for_update_coldkey_args(
    name: Optional[str] = None,
    new_name: Optional[str] = None,
    new_password: Optional[str] = None,
    remove_password: Optional[bool] = None,
    show_guidance: Optional[bool] = None,
) -> tuple[str, Optional[str], Optional[str], bool, bool]:
    """Interactive prompt for update coldkey arguments."""

    # Prompt for current name if missing
    if not name:
        # First show available coldkeys
        keys = list_keys()
        coldkeys = [k for k in keys if not k.get("is_hotkey", False)]

        if not coldkeys:
            print_error("No coldkeys found to update.")
            raise typer.Exit(1)

        console.print("\n[bold]Available coldkeys:[/bold]")
        for i, key in enumerate(coldkeys, 1):
            console.print(f"{i}. {key['name']} ({key['ss58_address']})")

        while True:
            name = Prompt.ask("\nEnter coldkey name to update")
            if validate_wallet_name(name):
                # Check if key exists and is a coldkey
                key_names = [k["name"] for k in coldkeys]
                if name in key_names:
                    break
                else:
                    print_error(f"Coldkey '{name}' not found. Please choose from the list above.")
            else:
                print_error("Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only.")

    # Prompt for new name if not provided
    if new_name is None:
        change_name = Confirm.ask("Do you want to change the coldkey name?", default=False)
        if change_name:
            while True:
                new_name = Prompt.ask("Enter new coldkey name")
                if validate_wallet_name(new_name):
                    # Check if new name already exists
                    if wallet_name_exists(new_name):
                        print_error(f"Wallet name '{new_name}' already exists. Please choose a different name.")
                        continue
                    break
                else:
                    print_error("Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only.")

    # Prompt for password changes if not provided
    if new_password is None and remove_password is None:
        password_action = Prompt.ask(
            "Password action",
            choices=["keep", "change", "remove"],
            default="keep"
        )

        if password_action == "change":
            while True:
                new_password = Prompt.ask("Enter new password (min 8 chars, letters + numbers)", password=True)
                if validate_password(new_password):
                    break
                print_error("Invalid password. Must be at least 8 characters with letters and numbers.")
            remove_password = False
        elif password_action == "remove":
            remove_password = True
            new_password = None
        else:
            remove_password = False
            new_password = None

    # Prompt for guidance if not provided
    if show_guidance is None:
        show_guidance = Confirm.ask("Show comprehensive guidance?", default=True)

    return name, new_name, new_password, remove_password, show_guidance


def prompt_for_update_hotkey_args(
    name: Optional[str] = None,
    new_name: Optional[str] = None,
    new_password: Optional[str] = None,
    remove_password: Optional[bool] = None,
    new_owner: Optional[str] = None,
    show_guidance: Optional[bool] = None,
) -> tuple[str, Optional[str], Optional[str], bool, Optional[str], bool]:
    """Interactive prompt for update hotkey arguments."""

    # Prompt for current name if missing
    if not name:
        # First show available hotkeys
        keys = list_keys()
        hotkeys = [k for k in keys if k.get("is_hotkey", False)]

        if not hotkeys:
            print_error("No hotkeys found to update.")
            raise typer.Exit(1)

        console.print("\n[bold]Available hotkeys:[/bold]")
        for i, key in enumerate(hotkeys, 1):
            owner_info = f" (owner: {key['owner_address']})" if key.get('owner_address') else ""
            console.print(f"{i}. {key['name']} ({key['ss58_address']}){owner_info}")

        while True:
            name = Prompt.ask("\nEnter hotkey name to update")
            if validate_wallet_name(name):
                # Check if key exists and is a hotkey
                key_names = [k["name"] for k in hotkeys]
                if name in key_names:
                    break
                else:
                    print_error(f"Hotkey '{name}' not found. Please choose from the list above.")
            else:
                print_error("Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only.")

    # Prompt for new name if not provided
    if new_name is None:
        change_name = Confirm.ask("Do you want to change the hotkey name?", default=False)
        if change_name:
            while True:
                new_name = Prompt.ask("Enter new hotkey name")
                if validate_wallet_name(new_name):
                    # Check if new name already exists
                    if wallet_name_exists(new_name):
                        print_error(f"Wallet name '{new_name}' already exists. Please choose a different name.")
                        continue
                    break
                else:
                    print_error("Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only.")

    # Prompt for new owner if not provided
    if new_owner is None:
        change_owner = Confirm.ask("Do you want to change the hotkey owner?", default=False)
        if change_owner:
            # Show available coldkeys
            keys = list_keys()
            coldkeys = [k for k in keys if not k.get("is_hotkey", False)]

            if not coldkeys:
                print_error("No coldkeys available to assign as owner.")
                raise typer.Exit(1)

            console.print("\n[bold]Available coldkeys to assign as owner:[/bold]")
            for i, key in enumerate(coldkeys, 1):
                console.print(f"{i}. {key['name']} ({key['ss58_address']})")

            while True:
                new_owner = Prompt.ask("Enter new coldkey owner name")
                if validate_wallet_name(new_owner):
                    # Check if owner exists and is a coldkey
                    key_names = [k["name"] for k in coldkeys]
                    if new_owner in key_names:
                        break
                    else:
                        print_error(f"Coldkey '{new_owner}' not found. Please choose from the list above.")
                else:
                    print_error("Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only.")

    # Prompt for password changes if not provided
    if new_password is None and remove_password is None:
        password_action = Prompt.ask(
            "Password action",
            choices=["keep", "change", "remove"],
            default="keep"
        )

        if password_action == "change":
            while True:
                new_password = Prompt.ask("Enter new password (min 8 chars, letters + numbers)", password=True)
                if validate_password(new_password):
                    break
                print_error("Invalid password. Must be at least 8 characters with letters and numbers.")
            remove_password = False
        elif password_action == "remove":
            remove_password = True
            new_password = None
        else:
            remove_password = False
            new_password = None

    # Prompt for guidance if not provided
    if show_guidance is None:
        show_guidance = Confirm.ask("Show comprehensive guidance?", default=True)

    return name, new_name, new_password, remove_password, new_owner, show_guidance


def prompt_for_balance_args(
    wallet_name: Optional[str] = None,
    address: Optional[str] = None,
    format_type: Optional[str] = None,
    show_guidance: Optional[bool] = None,
) -> tuple[Optional[str], Optional[str], str, bool]:
    """Interactive prompt for balance arguments."""

    # Prompt for wallet name or address if missing
    if not wallet_name and not address:
        choice = Prompt.ask(
            "Check balance by",
            choices=["wallet", "address"],
            default="wallet"
        )

        if choice == "wallet":
            # Show available wallets
            keys = list_keys()

            if not keys:
                print_error("No wallets found.")
                raise typer.Exit(1)

            console.print("\n[bold]Available wallets:[/bold]")
            for i, key in enumerate(keys, 1):
                key_type = "Hotkey" if key.get("is_hotkey", False) else "Coldkey"
                console.print(f"{i}. {key['name']} ({key_type}) - {key['ss58_address']}")

            while True:
                wallet_name = Prompt.ask("\nEnter wallet name to check balance")
                if validate_wallet_name(wallet_name):
                    # Check if wallet exists
                    key_names = [k["name"] for k in keys]
                    if wallet_name in key_names:
                        break
                    else:
                        print_error(f"Wallet '{wallet_name}' not found. Please choose from the list above.")
                else:
                    print_error("Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only.")
        else:
            # Get address directly
            while True:
                address = Prompt.ask("Enter address to check balance")
                if validate_address(address):
                    break
                else:
                    print_error("Invalid address format.")

    # Prompt for format if not provided
    if format_type is None:
        format_type = Prompt.ask(
            "Output format",
            choices=["table", "json"],
            default="table"
        )

    # Prompt for guidance if not provided
    if show_guidance is None:
        show_guidance = Confirm.ask("Show comprehensive guidance?", default=True)

    return wallet_name, address, format_type, show_guidance


def prompt_for_transfer_args(
    from_wallet: Optional[str] = None,
    to_address: Optional[str] = None,
    amount: Optional[str] = None,
    password: Optional[str] = None,
    show_guidance: Optional[bool] = None,
) -> tuple[str, str, str, Optional[str], bool]:
    """Interactive prompt for transfer arguments."""

    # Prompt for source wallet if missing
    if not from_wallet:
        # Show available coldkeys (only coldkeys can transfer)
        keys = list_keys()
        coldkeys = [k for k in keys if not k.get("is_hotkey", False)]

        if not coldkeys:
            print_error("No coldkeys found. Only coldkeys can transfer funds.")
            raise typer.Exit(1)

        console.print("\n[bold]Available coldkeys for transfer:[/bold]")
        for i, key in enumerate(coldkeys, 1):
            console.print(f"{i}. {key['name']} ({key['ss58_address']})")

        while True:
            from_wallet = Prompt.ask("\nEnter source coldkey name")
            if validate_wallet_name(from_wallet):
                # Check if wallet exists and is a coldkey
                key_names = [k["name"] for k in coldkeys]
                if from_wallet in key_names:
                    break
                else:
                    print_error(f"Coldkey '{from_wallet}' not found. Please choose from the list above.")
            else:
                print_error("Invalid wallet name. Use alphanumeric characters, hyphens, and underscores only.")

    # Prompt for destination address if missing
    if not to_address:
        console.print("\n[bold]You can enter either:[/bold]")
        console.print("• A wallet name (e.g., 'my-wallet')")
        console.print("• A full SS58 address (e.g., '5CFhfdvxRwW6gdSMALYJxK8TTgURrDPyFedbvc7wagJD8H5B')")

        while True:
            to_address = Prompt.ask("Enter destination (wallet name or address)")

            # First try to validate as an address
            if validate_address(to_address):
                break

            # If not a valid address, try to treat it as a wallet name
            if validate_wallet_name(to_address):
                try:
                    # Check if wallet exists and get its address
                    wallet_info = get_wallet_info_by_name(to_address)
                    to_address = wallet_info["ss58_address"]
                    console.print(f"[green]✓[/green] Found wallet '{to_address}' with address: {wallet_info['ss58_address']}")
                    break
                except FileNotFoundError:
                    print_error(f"Wallet '{to_address}' not found.")
                except Exception as e:
                    print_error(f"Error accessing wallet '{to_address}': {str(e)}")
            else:
                print_error("Invalid wallet name or address format.")

    # If to_address is provided but not a valid SS58 address, try to resolve as wallet name
    elif not validate_address(to_address):
        if validate_wallet_name(to_address):
            try:
                # Check if wallet exists and get its address
                wallet_info = get_wallet_info_by_name(to_address)
                console.print(f"[green]✓[/green] Resolved wallet '{to_address}' to address: {wallet_info['ss58_address']}")
                to_address = wallet_info["ss58_address"]
            except FileNotFoundError:
                print_error(f"Destination wallet '{to_address}' not found.")
                raise typer.Exit(1)
            except Exception as e:
                print_error(f"Error accessing destination wallet '{to_address}': {str(e)}")
                raise typer.Exit(1)
        else:
            print_error("Invalid destination address or wallet name format.")
            raise typer.Exit(1)

    # Prompt for amount if missing
    if not amount:
        while True:
            amount = Prompt.ask("Enter amount to transfer")
            try:
                # Basic validation - should be a positive number
                float(amount)
                if float(amount) <= 0:
                    print_error("Amount must be greater than 0.")
                    continue
                break
            except ValueError:
                print_error("Invalid amount. Please enter a valid number.")

    # Prompt for password if wallet is encrypted
    if password is None:
        try:
            wallet_info = get_wallet_info_by_name(from_wallet)
            if wallet_info.get("is_encrypted", True):
                password = Prompt.ask("Enter wallet password", password=True)
        except Exception:
            # If we can't get wallet info, assume it might be encrypted
            password = Prompt.ask("Enter wallet password (if required)", password=True)

    # Prompt for guidance if not provided
    if show_guidance is None:
        show_guidance = Confirm.ask("Show comprehensive guidance?", default=True)

    return from_wallet, to_address, amount, password, show_guidance


def display_all_wallet_balances(client, format_type: str = "table", show_guidance: bool = False):
    """Display balance for all wallets in a table format similar to btcli."""
    try:
        from src.htcli.utils.crypto import list_keys

        # Get all wallets
        wallets = list_keys()

        if not wallets:
            console.print("[yellow]No wallets found. Create a wallet first using 'htcli wallet generate-coldkey'[/yellow]")
            return

        # Filter to only coldkeys for balance display (like btcli)
        coldkeys = [w for w in wallets if not w.get("is_hotkey", False)]

        if not coldkeys:
            console.print("[yellow]No coldkeys found. Create a coldkey first using 'htcli wallet generate-coldkey'[/yellow]")
            return

        # Get balances for all coldkeys
        wallet_balances = []
        total_free_balance = 0
        total_staked_value = 0

        for wallet in coldkeys:
            try:
                # Get balance from blockchain
                response = client.get_balance(wallet["ss58_address"])
                if response.success:
                    balance_data = response.data
                    free_balance = balance_data.get('balance', 0)

                    # For now, we'll set staked value to 0 since we don't have staking info yet
                    # TODO: Implement staking balance retrieval when staking is available
                    staked_value = 0

                    wallet_balances.append({
                        "name": wallet["name"],
                        "address": wallet["ss58_address"],
                        "free_balance": free_balance,
                        "staked_value": staked_value,
                        "total_balance": free_balance + staked_value
                    })

                    total_free_balance += free_balance
                    total_staked_value += staked_value
                else:
                    console.print(f"[red]Failed to get balance for {wallet['name']}: {response.message}[/red]")
            except Exception as e:
                console.print(f"[red]Error getting balance for {wallet['name']}: {str(e)}[/red]")

        if not wallet_balances:
            console.print("[red]Failed to retrieve any wallet balances.[/red]")
            return

        # Display network info
        console.print(f"[bold cyan]Using the specified network from config[/bold cyan]")
        console.print()

        if format_type == "json":
            # JSON format
            json_data = {
                "wallets": wallet_balances,
                "totals": {
                    "total_free_balance": total_free_balance,
                    "total_staked_value": total_staked_value,
                    "total_balance": total_free_balance + total_staked_value
                }
            }
            console.print_json(data=json_data)
        else:
            # Table format
            table = Table(
                title="[bold cyan]Wallet Coldkey Balance[/bold cyan]",
                show_header=True,
                header_style="bold cyan",
                border_style="cyan"
            )

            # Add columns
            table.add_column("Wallet Name", style="cyan", no_wrap=True)
            table.add_column("Coldkey Address", style="green", no_wrap=True)
            table.add_column("Free Balance", style="yellow", justify="right")
            table.add_column("Staked Value", style="blue", justify="right")
            table.add_column("Total Balance", style="bold white", justify="right")

            # Add wallet rows
            for wallet in wallet_balances:
                table.add_row(
                    wallet["name"],
                    wallet["address"],
                    f"{wallet['free_balance'] / 1e18:,.4f} τ",
                    f"{wallet['staked_value'] / 1e18:,.4f} τ",
                    f"{wallet['total_balance'] / 1e18:,.4f} τ"
                )

            # Add totals row
            table.add_row(
                "[bold]Total Balance[/bold]",
                "",
                f"[bold]{total_free_balance / 1e18:,.4f} τ[/bold]",
                f"[bold]{total_staked_value / 1e18:,.4f} τ[/bold]",
                f"[bold]{(total_free_balance + total_staked_value) / 1e18:,.4f} τ[/bold]"
            )

            console.print(table)

            # Show guidance if requested
            if show_guidance:
                from rich.panel import Panel
                guidance_text = """
[bold]Balance Information:[/bold]
• Free Balance: Liquid funds available for transfers and transactions
• Staked Value: Funds currently staked in the network (if any)
• Total Balance: Sum of free and staked balances

[bold]Note:[/bold] Staking functionality is not yet implemented in htcli.
Staked values will show 0.0000 τ until staking features are added.

[bold]Commands:[/bold]
• Check individual wallet: htcli wallet balance --wallet <name>
• Transfer funds: htcli wallet transfer --from <wallet> --to <address> --amount <value>
• List all wallets: htcli wallet list
                """
                guidance_panel = Panel(
                    guidance_text,
                    title="[bold blue]Balance Information[/bold blue]",
                    border_style="blue",
                    padding=(1, 2)
                )
                console.print(guidance_panel)

    except Exception as e:
        console.print(f"[red]Failed to display wallet balances: {str(e)}[/red]")
        raise typer.Exit(1)
