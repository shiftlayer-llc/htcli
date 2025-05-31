import typer
from pathlib import Path
import json
import logging
from htcli.utils.wallet import create_wallet
from htcli.utils.helpers import (
    read_wallet_data_for_verification,
    deobfuscate_bytes,
)


from htcli.core.config import wallet_config
from htcli.core.constants import COLDKEY_FILE_NAME, HOTKEYS_DIR_NAME
import getpass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="htcli.log",
    filemode="a",
)
logger = logging.getLogger(__name__)

app = typer.Typer(name="wallet", help="Wallet commands")


@app.command()
def info():
    """
    Get the info of the wallet
    """
    typer.echo("Getting info of the wallet...")
    # This is a placeholder for the actual implementation


@app.command()
def create(
    name: str = wallet_config.name,
    password: str = wallet_config.password,
    path: str = wallet_config.path,
    hotkey: str = wallet_config.hotkey,
):
    """
    Create a new wallet with cryptographic keys (coldkey and optional hotkey) following the Bittensor structure.
    Generates a new keypair, saves password-obfuscated private key bytes to a file, and public key info to a .pub file.
    """
    base_path = path or wallet_config.default_wallet_path
    base_wallet_dir = Path(base_path)

    # Prompt for wallet name if not provided
    if not name:
        name = typer.prompt("Enter wallet name")
        if not name:
            typer.echo("Error: Wallet name cannot be empty.")
            return

    if password is None:
        if not hotkey:
            prompt_name = name
            password = getpass.getpass(f"Enter password for wallet '{prompt_name}': ")
            if not password:
                typer.echo("Error: Password cannot be empty.")
                return

    try:
        coldkey_ss58 = None

        if not hotkey:
            coldkey_dir = base_wallet_dir / name
            coldkey_file_name = COLDKEY_FILE_NAME

            private_key_file_path, coldkey_ss58, coldkey_mnemonic = create_wallet(
                name=coldkey_file_name,
                wallet_dir=coldkey_dir,
                password=password,
                save_as_json=False,
            )

            typer.echo(
                typer.style(
                    f"✅ Successfully created coldkey wallet '{name}'",
                    fg=typer.colors.GREEN,
                )
            )
            typer.echo(f"📍 Coldkey Address: {coldkey_ss58}")
            typer.echo(
                f"📁 Coldkey Private Key Path: {private_key_file_path} {'(password-protected)' if password else ''}"
            )
            typer.echo(f"📄 Coldkey Public Key Path: {private_key_file_path}.pub")
            typer.echo(
                typer.style(
                    "\n⚠️  IMPORTANT: Save this mnemonic phrase in a secure location!",
                    fg=typer.colors.YELLOW,
                )
            )
            typer.echo(
                typer.style(
                    "It is the only way to recover your coldkey if you lose access to your wallet files.",
                    fg=typer.colors.YELLOW,
                )
            )
            typer.echo(
                typer.style(
                    f"🔑 Coldkey Mnemonic: {coldkey_mnemonic}", fg=typer.colors.YELLOW
                )
            )

        if hotkey:
            coldkey_dir_check = base_wallet_dir / name
            if not coldkey_dir_check.exists():
                typer.echo(
                    f"Error: Parent coldkey '{name}' not found at {coldkey_dir_check}. Create the coldkey first."
                )
                return

            hotkey_dir = base_wallet_dir / name / HOTKEYS_DIR_NAME
            hotkey_file_name = hotkey

            hotkey_private_key_file_path, hotkey_ss58, hotkey_mnemonic = create_wallet(
                name=hotkey_file_name,
                wallet_dir=hotkey_dir,
                password=password,
                save_as_json=True,
            )

            typer.echo(
                typer.style(
                    f"✅ Successfully created hotkey wallet '{hotkey}'",
                    fg=typer.colors.GREEN,
                )
            )
            typer.echo(f"📍 Hotkey Address: {hotkey_ss58}")
            typer.echo(
                f"📁 Hotkey Wallet File Path: {hotkey_private_key_file_path} {'(password-protected)' if password else ''}"
            )
            typer.echo(
                typer.style(
                    "\n⚠️  IMPORTANT: Save this mnemonic phrase in a secure location!",
                    fg=typer.colors.YELLOW,
                )
            )
            typer.echo(
                typer.style(
                    "It is the only way to recover your hotkey if you lose access to your wallet files.",
                    fg=typer.colors.YELLOW,
                )
            )
            typer.echo(
                typer.style(
                    f"🔑 Hotkey Mnemonic: {hotkey_mnemonic}", fg=typer.colors.YELLOW
                )
            )

        if hotkey and coldkey_ss58 is None:
            coldkey_pub_path = base_wallet_dir / name / "coldkey.pub"
            if coldkey_pub_path.exists():
                try:
                    with open(coldkey_pub_path, "r") as f:
                        pub_data = json.load(f)
                        coldkey_ss58 = pub_data.get("ss58Address", "Unknown")
                except Exception:
                    coldkey_ss58 = "Unknown (Error reading coldkey.pub)"
            else:
                coldkey_ss58 = "Unknown (coldkey.pub not found)"

        # --- Verification of Obfuscation/De-obfuscation ---
        try:
            # Only perform verification if a wallet was actually created and password was used
            if (
                not hotkey and password is not None
            ):  # Verify coldkey if created with password
                deobfuscated_bytes = read_wallet_data_for_verification(
                    Path(private_key_file_path),
                    is_json=False,
                    password=password,
                )
                temp_keypair = Keypair.create_from_mnemonic(
                    Keypair.generate_mnemonic(), ss58_format=42
                )
                original_coldkey_private_key = temp_keypair.private_key

                typer.echo(
                    typer.style(
                        "Verification skipped for now due to complexity of retrieving original key with different save formats.",
                        fg=typer.colors.YELLOW,
                    )
                )
            if hotkey and password is not None:
                deobfuscated_bytes = read_wallet_data_for_verification(
                    Path(hotkey_private_key_file_path),
                    is_json=True,
                    password=password,
                )
                typer.echo(
                    typer.style(
                        "Verification skipped for now due to complexity of retrieving original key with different save formats.",
                        fg=typer.colors.YELLOW,
                    )
                )
        except Exception as e:
            typer.echo(
                f"Warning: Could not perform obfuscation verification - {str(e)}"
            )

        # --- Print Summary ---
        # If only hotkey was created, we need to get the coldkey address for the summary.
        if hotkey and coldkey_ss58 is None:
            # Try to read coldkey.pub to get the address
            coldkey_pub_path = base_wallet_dir / name / "coldkey.pub"
            if coldkey_pub_path.exists():
                try:
                    with open(coldkey_pub_path, "r") as f:
                        pub_data = json.load(f)
                        coldkey_ss58 = pub_data.get("ss58Address", "Unknown")
                except Exception:
                    coldkey_ss58 = "Unknown (Error reading coldkey.pub)"
            else:
                coldkey_ss58 = "Unknown (coldkey.pub not found)"

        typer.echo(typer.style("\nWallet Creation Summary:", bold=True))
        typer.echo("=======================")
        # Use the potentially updated coldkey_ss58 for the summary
        typer.echo(
            f"📍 Coldkey Address: {coldkey_ss58 if coldkey_ss58 else 'Not created'}"
        )
        typer.echo(f"📍 Hotkey Address: {hotkey_ss58 if hotkey else 'Not created'}")

    except ValueError as e:
        typer.echo(f"Error: {str(e)}")
        return
    except RuntimeError as e:
        typer.echo(f"Error: {str(e)}")
        return
    except Exception as e:
        typer.echo(f"An unexpected error occurred: {str(e)}")
        return


@app.command()
def list(name: str = wallet_config.name, path: str = wallet_config.path):
    """
    List wallet information. If --wallet.name is provided, shows details for that specific wallet.
    Otherwise, lists all available wallets.
    """
    base_path = path or wallet_config.default_wallet_path
    base_wallet_dir = Path(base_path)

    if not base_wallet_dir.exists():
        typer.echo(f"No wallets found at {base_wallet_dir}")
        return

    try:
        if name:
            # List specific wallet
            wallet_dir = base_wallet_dir / name
            if not wallet_dir.exists():
                logger.error(f"Wallet '{name}' not found at {wallet_dir}")
                typer.echo(
                    typer.style(f"❌ Wallet '{name}' not found", fg=typer.colors.RED)
                )
                return

            # Check for coldkey
            coldkey_path = wallet_dir / "coldkey"
            coldkey_pub_path = wallet_dir / "coldkey.pub"

            if coldkey_path.exists():
                typer.echo(typer.style(f"\nColdkey Wallet: {name}", bold=True))
                typer.echo("=======================")
                try:
                    with open(coldkey_pub_path, "r") as f:
                        pub_data = json.load(f)
                        typer.echo(
                            f"📍 Address: {pub_data.get('ss58Address', 'Unknown')}"
                        )
                        typer.echo(
                            f"📁 Private Key Path: {coldkey_path} {'(password-protected)' if coldkey_path.stat().st_mode & 0o600 else ''}"
                        )
                        typer.echo(f"📄 Public Key Path: {coldkey_pub_path}")
                except Exception as e:
                    typer.echo(f"Error reading coldkey info: {str(e)}")

            # Check for hotkeys
            hotkeys_dir = wallet_dir / "hotkeys"
            if hotkeys_dir.exists():
                hotkey_files = list(hotkeys_dir.glob("*"))
                if hotkey_files:
                    typer.echo(typer.style(f"\nHotkeys for {name}:", bold=True))
                    typer.echo("=======================")
                    for hotkey_file in hotkey_files:
                        try:
                            with open(hotkey_file, "r") as f:
                                hotkey_data = json.load(f)
                                typer.echo(f"📍 Hotkey: {hotkey_file.name}")
                                typer.echo(
                                    f"  Address: {hotkey_data.get('ss58Address', 'Unknown')}"
                                )
                                typer.echo(
                                    f"  Path: {hotkey_file} {'(password-protected)' if hotkey_file.stat().st_mode & 0o600 else ''}"
                                )
                        except Exception as e:
                            typer.echo(
                                f"Error reading hotkey {hotkey_file.name}: {str(e)}"
                            )

        else:
            # List all wallets
            wallet_dirs = [d for d in base_wallet_dir.iterdir() if d.is_dir()]
            if not wallet_dirs:
                typer.echo("No wallets found")
                return

            typer.echo(
                typer.style(f"\nAvailable Wallets ({len(wallet_dirs)}):", bold=True)
            )
            typer.echo("=======================")

            for wallet_dir in wallet_dirs:
                wallet_name = wallet_dir.name
                coldkey_path = wallet_dir / "coldkey"
                coldkey_pub_path = wallet_dir / "coldkey.pub"
                hotkeys_dir = wallet_dir / "hotkeys"

                # Get coldkey address if available
                coldkey_address = "Unknown"
                if coldkey_pub_path.exists():
                    try:
                        with open(coldkey_pub_path, "r") as f:
                            pub_data = json.load(f)
                            coldkey_address = pub_data.get("ss58Address", "Unknown")
                    except Exception:
                        pass

                # Count hotkeys
                hotkey_count = 0
                hotkey_addresses = []
                if hotkeys_dir.exists():
                    hotkey_files = [f for f in hotkeys_dir.iterdir() if f.is_file()]
                    hotkey_count = len(hotkey_files)
                    # Get hotkey addresses
                    for hotkey_file in hotkey_files:
                        try:
                            with open(hotkey_file, "r") as f:
                                hotkey_data = json.load(f)
                                hotkey_addresses.append(
                                    hotkey_data.get("ss58Address", "Unknown")
                                )
                        except Exception:
                            pass

                typer.echo(f"📁 Wallet: {wallet_name}")
                typer.echo(f"  📍 Coldkey Address: {coldkey_address}")
                if hotkey_count > 0:
                    typer.echo(f"  🔑 Hotkeys ({hotkey_count}):")
                    for addr in hotkey_addresses:
                        typer.echo(f"    • {addr}")
                else:
                    typer.echo(f"  🔑 Hotkeys: {hotkey_count}")

    except Exception as e:
        typer.echo(f"An error occurred while listing wallets: {str(e)}")
        return


@app.command()
def remove(
    name: str = wallet_config.name,
    all: bool = wallet_config.all,
    path: str = wallet_config.path,
    force: bool = wallet_config.force,
):
    """
    Remove a specific wallet or all wallets. Requires confirmation unless --force is used.
    """
    if not name and not all:
        typer.echo("Error: Either --wallet.nam or --all must be specified")
        raise typer.Exit(code=1)

    if name and all:
        typer.echo("Error: Cannot specify both --wallet.name and --all")
        raise typer.Exit(code=1)

    base_path = path or wallet_config.default_wallet_path
    base_wallet_dir = Path(base_path)

    if not base_wallet_dir.exists():
        logger.error(f"No wallets found at {base_wallet_dir}")
        typer.echo(typer.style("❌ No wallets found", fg=typer.colors.RED))
        return

    try:
        if all:
            # List all wallets to be removed
            wallet_dirs = [d for d in base_wallet_dir.iterdir() if d.is_dir()]
            if not wallet_dirs:
                typer.echo("No wallets found to remove")
                return

            typer.echo(typer.style("\nWallets to be removed:", bold=True))
            typer.echo("=======================")
            for wallet_dir in wallet_dirs:
                typer.echo(f"📁 {wallet_dir.name}")

            if not force:
                if not typer.confirm(
                    typer.style(
                        "\n⚠️  Are you sure you want to remove ALL wallets? This action cannot be undone!",
                        fg=typer.colors.RED,
                    ),
                    default=False,
                ):
                    typer.echo("Operation cancelled")
                    return

            # Remove all wallets
            for wallet_dir in wallet_dirs:
                try:
                    import shutil

                    shutil.rmtree(wallet_dir)
                    typer.echo(f"✅ Removed wallet: {wallet_dir.name}")
                except Exception as e:
                    typer.echo(f"❌ Failed to remove wallet: {str(e)}")

        else:
            # Prompt for wallet name if not provided
            if not name:
                name = typer.prompt("Enter wallet name to remove")
                if not name:
                    typer.echo("Error: Wallet name cannot be empty.")
                    return

            # Remove specific wallet
            wallet_dir = base_wallet_dir / name
            if not wallet_dir.exists():
                logger.error(f"Wallet '{name}' not found at {wallet_dir}")
                typer.echo(
                    typer.style(f"❌ Wallet '{name}' not found", fg=typer.colors.RED)
                )
                return

            # Show wallet details before removal
            typer.echo(typer.style(f"\nWallet to be removed:", bold=True))
            typer.echo("=======================")
            typer.echo(f"📁 {name}")

            # Check for hotkeys
            hotkeys_dir = wallet_dir / "hotkeys"
            if hotkeys_dir.exists():
                hotkey_count = len([f for f in hotkeys_dir.iterdir() if f.is_file()])
                typer.echo(f"  🔑 Has {hotkey_count} hotkeys")

            if not force:
                if not typer.confirm(
                    typer.style(
                        f"\n⚠️  Are you sure you want to remove wallet '{name}'? This action cannot be undone!",
                        fg=typer.colors.RED,
                    ),
                    default=False,
                ):
                    typer.echo("Operation cancelled")
                    return

            # Remove the wallet
            try:
                import shutil

                shutil.rmtree(wallet_dir)
                typer.echo(f"✅ Successfully removed wallet: {name}")
            except Exception as e:
                typer.echo(f"❌ Failed to remove wallet: {str(e)}")

    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}")
        return


@app.command()
def regen_coldkey(
    name: str = wallet_config.name,
    mnemonic: str = wallet_config.mnemonic,
    password: str = wallet_config.password,
    path: str = wallet_config.path,
    force: bool = wallet_config.force,
):
    """
    Regenerate a coldkey wallet from a mnemonic phrase. This will create a new coldkey with the same keys as the original.

    Example:
        htcli wallet regen-coldkey --wallet.name mywallet --mnemonic "word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12"
    """
    base_path = path or wallet_config.default_wallet_path
    base_wallet_dir = Path(base_path)

    # Create base directory if it doesn't exist
    base_wallet_dir.mkdir(parents=True, exist_ok=True)

    # Determine coldkey directory and file name
    coldkey_dir = base_wallet_dir / name
    coldkey_file_name = COLDKEY_FILE_NAME

    # Check if wallet already exists
    if coldkey_dir.exists() and not force:
        typer.echo(f"Error: Wallet '{name}' already exists at {coldkey_dir}")
        typer.echo("Use --force to overwrite existing wallet")
        return

    try:
        # Prompt for password if not provided
        if password is None:
            password = getpass.getpass(f"Enter password for wallet '{name}': ")
            if not password:
                typer.echo("Error: Password cannot be empty.")
                return

        # Create keypair from mnemonic
        try:
            keypair = Keypair.create_from_mnemonic(mnemonic, ss58_format=42)
        except Exception as e:
            typer.echo(f"Error: Invalid mnemonic phrase - {str(e)}")
            return

        # Create directory if it doesn't exist
        coldkey_dir.mkdir(parents=True, exist_ok=True)

        # Save the coldkey using create_wallet function
        private_key_file_path, coldkey_ss58, coldkey_mnemonic = create_wallet(
            name=coldkey_file_name,
            wallet_dir=coldkey_dir,
            password=password,
            save_as_json=False,
            mnemonic=mnemonic,  # Pass the provided mnemonic
        )

        typer.echo(
            typer.style(
                f"✅ Successfully regenerated coldkey wallet '{name}'",
                fg=typer.colors.GREEN,
            )
        )
        typer.echo(f"📍 Coldkey Address: {coldkey_ss58}")
        typer.echo(
            f"📁 Coldkey Private Key Path: {private_key_file_path} {'(password-protected)' if password else ''}"
        )
        typer.echo(f"📄 Coldkey Public Key Path: {private_key_file_path}.pub")
        typer.echo(
            typer.style(
                "\n⚠️  IMPORTANT: This is the same mnemonic you provided:",
                fg=typer.colors.YELLOW,
            )
        )
        typer.echo(
            typer.style(
                f"🔑 Coldkey Mnemonic: {coldkey_mnemonic}", fg=typer.colors.YELLOW
            )
        )

    except ValueError as e:
        typer.echo(f"Error: {str(e)}")
        return
    except RuntimeError as e:
        typer.echo(f"Error: {str(e)}")
        return
    except Exception as e:
        typer.echo(f"An unexpected error occurred: {str(e)}")
        return


@app.command()
def regen_hotkey(
    name: str = wallet_config.name,
    hotkey: str = wallet_config.hotkey,
    mnemonic: str = wallet_config.mnemonic,
    path: str = wallet_config.path,
    force: bool = wallet_config.force,
):
    """
    Regenerate a hotkey wallet from a mnemonic phrase. This will create a new hotkey with the same keys as the original.

    Example:
        htcli wallet regen-hotkey --wallet.name mywallet --wallet.hotkey myhotkey --wallet.path /path/to/wallets --mnemonic "word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12"
    """
    # Prompt for path if not provided
    if not path:
        path = typer.prompt(
            "Enter wallet path", default=wallet_config.default_wallet_path
        )
        if not path:
            typer.echo("Error: Wallet path cannot be empty.")
            return

    base_path = path
    base_wallet_dir = Path(base_path)

    # Create base directory if it doesn't exist
    base_wallet_dir.mkdir(parents=True, exist_ok=True)

    # Prompt for wallet name if not provided
    if not name:
        name = typer.prompt("Enter wallet name")
        if not name:
            typer.echo("Error: Wallet name cannot be empty.")
            return

    # Prompt for hotkey name if not provided
    if not hotkey:
        hotkey = typer.prompt("Enter hotkey name")
        if not hotkey:
            typer.echo("Error: Hotkey name cannot be empty.")
            return

    # Prompt for mnemonic if not provided
    if not mnemonic:
        typer.echo("Enter the mnemonic phrase (12 words separated by spaces):")
        mnemonic = typer.prompt("Mnemonic", hide_input=True)
        if not mnemonic:
            typer.echo("Error: Mnemonic phrase cannot be empty.")
            return

    # Check if parent coldkey exists
    coldkey_dir = base_wallet_dir / name
    if not coldkey_dir.exists():
        typer.echo(f"Error: Parent coldkey wallet '{name}' not found at {coldkey_dir}")
        typer.echo("Create the coldkey wallet first using 'htcli wallet create'")
        return

    # Determine hotkey directory and file name
    hotkey_dir = coldkey_dir / HOTKEYS_DIR_NAME
    hotkey_file_name = hotkey  # Use the provided hotkey name

    # Check if hotkey already exists
    hotkey_path = hotkey_dir / hotkey_file_name
    if hotkey_path.exists() and not force:
        typer.echo(f"Error: Hotkey '{hotkey}' already exists at {hotkey_path}")
        typer.echo("Use --force to overwrite existing hotkey")
        return

    try:
        # Create keypair from mnemonic
        try:
            keypair = Keypair.create_from_mnemonic(mnemonic, ss58_format=42)
        except Exception as e:
            typer.echo(f"Error: Invalid mnemonic phrase - {str(e)}")
            return

        # Create directory if it doesn't exist
        hotkey_dir.mkdir(parents=True, exist_ok=True)

        # Save the hotkey using create_wallet function without password
        private_key_file_path, hotkey_ss58, hotkey_mnemonic = create_wallet(
            name=hotkey_file_name,
            wallet_dir=hotkey_dir,
            password=None,  # No password needed for hotkey regeneration
            save_as_json=True,
            mnemonic=mnemonic,  # Pass the provided mnemonic
        )

        typer.echo(
            typer.style(
                f"✅ Successfully regenerated hotkey wallet '{hotkey}'",
                fg=typer.colors.GREEN,
            )
        )
        typer.echo(f"📍 Hotkey Address: {hotkey_ss58}")
        typer.echo(f"📁 Hotkey Wallet File Path: {private_key_file_path}")
        typer.echo(
            typer.style(
                f"🔑 Hotkey Mnemonic: {hotkey_mnemonic}", fg=typer.colors.YELLOW
            )
        )

    except ValueError as e:
        typer.echo(f"Error: {str(e)}")
        return
    except RuntimeError as e:
        typer.echo(f"Error: {str(e)}")
        return
    except Exception as e:
        typer.echo(f"An unexpected error occurred: {str(e)}")
        return


@app.command()
def balance(
    name: str = wallet_config.name,
    ss58_address: str = wallet_config.ss58_address,
    path: str = wallet_config.path,
):
    """
    Check the balance of a wallet using either the wallet name or SS58 address.

    Examples:
        htcli wallet balance --wallet.name mywallet
        htcli wallet balance --ss58-address 5DaTcPcom7o9wRYdCB9qkfkobPREmgXcyRhE1qPXb7UDeXkY
    """
    base_path = path or wallet_config.default_wallet_path
    base_wallet_dir = Path(base_path)

    if not name and not ss58_address:
        typer.echo("Error: Either --wallet.name or --ss58-address must be specified")
        return

    if name and ss58_address:
        typer.echo("Error: Cannot specify both --wallet.name and --ss58-address")
        return

    try:
        # If wallet name is provided, get the SS58 address from the wallet
        if name:
            coldkey_pub_path = base_wallet_dir / name / "coldkey.pub"

            if not coldkey_pub_path.exists():
                typer.echo(f"Error: Wallet '{name}' not found at {coldkey_pub_path}")
                return

            try:
                with open(coldkey_pub_path, "r") as f:
                    pub_data = json.load(f)
                    ss58_address = pub_data.get("ss58Address")
                    if not ss58_address:
                        typer.echo(
                            f"Error: Could not find SS58 address in wallet '{name}'"
                        )
                        return
            except Exception as e:
                typer.echo(f"Error reading wallet file: {str(e)}")
                return

        # TODO: Implement actual balance checking using the network
        # For now, just show a placeholder message
        typer.echo(f"Checking balance for address: {ss58_address}")
        typer.echo(
            "Balance checking functionality will be implemented in a future update."
        )
        typer.echo(
            "This will connect to the Hypertensor network to fetch the actual balance."
        )

    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}")
        return


# Remove other wallet commands for now, focusing on 'create'
# @app.command()
# def list(...): pass
# @app.command()
# def remove(...): pass
# @app.command()
# def recover(...): pass
# @app.command()
# def reveal(...): pass # This command would need significant changes to handle raw key files
# @app.command()
# def balance(...): pass
