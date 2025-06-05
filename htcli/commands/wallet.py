import typer
from pathlib import Path
import json
import logging
from htcli.utils.wallet import create_wallet, import_wallet
from htcli.utils.helpers import (
    read_wallet_data_for_verification,
    deobfuscate_bytes,
)
from substrateinterface import Keypair
import click

from htcli.core.config.wallet import wallet_config
from htcli.core.constants import (
    COLDKEY_FILE_NAME,
    HOTKEYS_DIR_NAME,
    DEFAULT_WALLET_PATH,
)
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
    force: bool = wallet_config.force,
):
    """
    Create a new wallet.

    Examples:
        # Create a wallet
        htcli wallet create --name first --password asdf
        htcli wallet create --wallet.name first --wallet.password asdf
        htcli wallet create --wallet-name first --wallet-password asdf
    """
    # Prompt for wallet name if not provided
    if not name:
        name = typer.prompt("Enter wallet name", default="default")
        if not name:
            name = "default"

    # Prompt for password if not provided
    if password is None:
        prompt_name = name
        while True:
            password = getpass.getpass(
                f"Enter password for wallet '{prompt_name}' (press Enter for unencrypted wallet): "
            )
            confirm_password = getpass.getpass(
                f"Confirm password for wallet '{prompt_name}': "
            )
            if password == confirm_password:
                if password == "":
                    password = None
                    typer.echo(
                        typer.style(
                            "⚠️  Creating unencrypted wallet", fg=typer.colors.YELLOW
                        )
                    )
                break
            else:
                typer.echo(
                    typer.style(
                        "❌ Passwords do not match. Please try again.",
                        fg=typer.colors.RED,
                    )
                )

    # Prompt for path if not provided
    if not path:
        path = typer.prompt(
            "Enter wallet path",
            default=DEFAULT_WALLET_PATH,
            show_default=True,
        )

    # Create wallet (always as coldkey by default)
    try:
        wallet_dir = Path(path or DEFAULT_WALLET_PATH).expanduser()
        wallet_path, address, mnemonic = create_wallet(
            name=name,
            wallet_dir=wallet_dir,
            is_hotkey=False,  # Always create as coldkey
            password=password,
            force=force,
        )

        # Print success message
        typer.echo(f"✅ Created wallet at: {wallet_path}")
        typer.echo(f"📍 Address: {address}")
        typer.echo(f"\n⚠️  IMPORTANT: Save this mnemonic phrase in a secure location:")
        typer.echo(f"🔑 {mnemonic}")
        if password is None:
            typer.echo(
                typer.style(
                    "⚠️  Warning: This wallet is not encrypted", fg=typer.colors.YELLOW
                )
            )

    except Exception as e:
        raise typer.Exit(str(e))


@app.command()
def list(name: str = wallet_config.name, path: str = wallet_config.path):
    """
    List wallet information. If --wallet.name is provided, shows details for that specific wallet.
    Otherwise, lists all available wallets.

    Examples:
        # List all wallets
        htcli wallet list

        # List specific wallet
        htcli wallet list --name mywallet
    """
    # Get the actual path value from click context
    ctx = click.get_current_context()
    base_path = ctx.params.get("path") or DEFAULT_WALLET_PATH
    base_wallet_dir = Path(base_path).expanduser().resolve()

    if not base_wallet_dir.exists():
        typer.echo(f"No wallets found at {base_wallet_dir}")
        return

    try:
        if name:
            # List specific wallet
            wallet_file = base_wallet_dir / f"{name}.key"
            if not wallet_file.exists():
                typer.echo(
                    typer.style(
                        f"❌ Wallet '{name}' not found at {wallet_file}",
                        fg=typer.colors.RED,
                    )
                )
                return

            try:
                with open(wallet_file, "r") as f:
                    wallet_data = json.load(f)
                typer.echo(typer.style(f"\nWallet: {name}", bold=True))
                typer.echo(f"  📍 Address: {wallet_data.get('ss58Address', 'Unknown')}")
                typer.echo(
                    f"  🔑 Public Key: {wallet_data.get('publicKey', 'Unknown')}"
                )
            except Exception as e:
                typer.echo(f"Error reading wallet info: {str(e)}")

        else:
            # List all wallets
            wallet_files = sorted(base_wallet_dir.glob("*.key"))
            if not wallet_files:
                typer.echo("No wallets found")
                return

            typer.echo(
                typer.style(f"Available Wallets ({len(wallet_files)}):", bold=True)
            )
            # Create table headers
            headers = ["Wallet", "Address"]
            rows = []
            max_wallet_len = len("Wallet")  # Initialize with header length
            max_address_len = len("Address")  # Initialize with header length

            # Collect data and calculate column widths
            for wallet_file in wallet_files:
                wallet_name = wallet_file.stem
                max_wallet_len = max(max_wallet_len, len(wallet_name))
                try:
                    with open(wallet_file, "r") as f:
                        wallet_data = json.load(f)
                    address = wallet_data.get("ss58Address", "Unknown")
                    max_address_len = max(max_address_len, len(address))
                    rows.append([wallet_name, address])
                except Exception as e:
                    rows.append([wallet_name, f"Error: {str(e)}"])

            # Print table header
            header = f"| {'Wallet'.ljust(max_wallet_len)} | {'Address'.ljust(max_address_len)} |"
            separator = f"|{'-' * (max_wallet_len + 2)}|{'-' * (max_address_len + 2)}|"
            typer.echo(separator)
            typer.echo(header)
            typer.echo(separator)

            # Print table rows
            for row in rows:
                typer.echo(
                    f"| {row[0].ljust(max_wallet_len)} | {row[1].ljust(max_address_len)} |"
                )
            typer.echo(separator)

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
        if not all:
            # prompt for wallet name
            name = typer.prompt("Enter wallet name")
            if not name:
                typer.echo("Error: Wallet name cannot be empty.")
                raise typer.Exit(code=1)
        else:
            raise typer.Exit(code=1)

    if name and all:
        typer.echo("Error: Cannot specify both --wallet.name and --all")
        raise typer.Exit(code=1)

    base_path = path or wallet_config.default_wallet_path
    base_wallet_dir = Path(base_path).expanduser().resolve()

    if not base_wallet_dir.exists():
        logger.error(f"No wallets found at {base_wallet_dir}")
        typer.echo(typer.style("❌ No wallets found", fg=typer.colors.RED))
        return

    try:
        if all:
            # List all wallets to be removed
            # Convert glob iterator to list and sort for consistent ordering
            wallet_files = sorted(base_wallet_dir.glob("*.key"))
            if not wallet_files:
                typer.echo("No wallets found to remove")
                return

            typer.echo(typer.style("\nWallets to be removed:", bold=True))
            typer.echo("=======================")
            for wallet_file in wallet_files:
                typer.echo(f"📁 {wallet_file.stem}")

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
            for wallet_file in wallet_files:
                try:
                    wallet_file.unlink()
                    typer.echo(f"✅ Removed wallet: {wallet_file.stem}")
                except Exception as e:
                    typer.echo(f"❌ Failed to remove wallet: {str(e)}")

        else:
            # Remove specific wallet
            wallet_file = base_wallet_dir / f"{name}.key"
            if not wallet_file.exists():
                logger.error(f"Wallet '{name}' not found at {wallet_file}")
                typer.echo(
                    typer.style(f"❌ Wallet '{name}' not found", fg=typer.colors.RED)
                )
                return

            # Show wallet details before removal
            typer.echo(typer.style(f"\nWallet to be removed:", bold=True))
            typer.echo("=======================")
            typer.echo(f"📁 {name}")

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
                wallet_file.unlink()
                typer.echo(f"✅ Successfully removed wallet: {name}")
            except Exception as e:
                typer.echo(f"❌ Failed to remove wallet: {str(e)}")

    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}")
        return


@app.command()
def restore(
    name: str = wallet_config.name,
    mnemonic: str = wallet_config.mnemonic,
    password: str = wallet_config.password,
    path: str = wallet_config.path,
    force: bool = wallet_config.force,
):
    """
    Restore a wallet from a mnemonic phrase. This will create a new wallet with the same keys as the original.

    Example:
        htcli wallet restore --name mywallet --mnemonic "<mnemonic_phrase>"
    """
    base_path = path or wallet_config.default_wallet_path
    base_wallet_dir = Path(base_path).expanduser().resolve()

    # Create base directory if it doesn't exist
    base_wallet_dir.mkdir(parents=True, exist_ok=True)

    # Prompt for wallet name if not provided
    if not name:
        name = typer.prompt("Enter wallet name")
        if not name:
            typer.echo("Error: Wallet name cannot be empty.")
            return

    # prompt for mnemonic if not provided
    if not mnemonic:
        mnemonic = typer.prompt(f"Enter mnemonic phrase for {name}")
        if not mnemonic:
            typer.echo("Error: Mnemonic phrase cannot be empty.")
            return

    # Check if wallet already exists
    wallet_file = base_wallet_dir / f"{name}.key"
    if wallet_file.exists() and not force:
        typer.echo(f"Error: Wallet '{name}' already exists at {wallet_file}")
        typer.echo(
            "Use --force to overwrite existing wallet or choose another wallet name"
        )
        return

    try:
        # Prompt for password if not provided
        if password is None:
            prompt_name = name
            while True:
                password = getpass.getpass(
                    f"Enter password for wallet '{prompt_name}' (press Enter for unencrypted wallet): "
                )
                confirm_password = getpass.getpass(
                    f"Confirm password for wallet '{prompt_name}': "
                )
                if password == confirm_password:
                    if password == "":
                        password = None
                        typer.echo(
                            typer.style(
                                "⚠️  Regenerating unencrypted wallet",
                                fg=typer.colors.YELLOW,
                            )
                        )
                    break
                else:
                    typer.echo(
                        typer.style(
                            "❌ Passwords do not match. Please try again.",
                            fg=typer.colors.RED,
                        )
                    )

        # Create the wallet using create_wallet function
        wallet_path, address, restored_mnemonic = create_wallet(
            name=name,
            wallet_dir=base_wallet_dir,
            password=password,
            mnemonic=mnemonic,  # Pass the provided mnemonic
            force=force,
        )

        typer.echo(
            typer.style(
                f"✅ Successfully restored wallet '{name}'",
                fg=typer.colors.GREEN,
            )
        )
        typer.echo(f"📍 Address: {address}")
        typer.echo(
            f"📁 Wallet Path: {wallet_path} {'(encrypted)' if password else '(unencrypted)'}"
        )
        typer.echo(
            typer.style(
                "\n⚠️  IMPORTANT: This is the same mnemonic you provided:",
                fg=typer.colors.YELLOW,
            )
        )
        typer.echo(
            typer.style(f"🔑 Mnemonic: {restored_mnemonic}", fg=typer.colors.YELLOW)
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
        # Check balance using wallet name
        htcli wallet balance --name mywallet

        # Check balance using SS58 address
        htcli wallet balance --ss58-address 5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty
    """
    base_path = path or wallet_config.default_wallet_path
    base_wallet_dir = Path(base_path).expanduser().resolve()

    if not name and not ss58_address:
        typer.echo("Error: Either --name or --ss58-address must be specified")
        return

    if name and ss58_address:
        typer.echo("Error: Cannot specify both --name and --ss58-address")
        return

    try:
        # If wallet name is provided, get the SS58 address from the wallet
        if name:
            wallet_file = base_wallet_dir / f"{name}.key"
            if not wallet_file.exists():
                typer.echo(f"Error: Wallet '{name}' not found at {wallet_file}")
                return

            try:
                with open(wallet_file, "r") as f:
                    wallet_data = json.load(f)
                    ss58_address = wallet_data.get("ss58Address")
                    if not ss58_address:
                        typer.echo(
                            f"Error: Could not find SS58 address in wallet '{name}'"
                        )
                        return
            except Exception as e:
                typer.echo(f"Error reading wallet file: {str(e)}")
                return

        # TODO: Implement actual balance checking using the network
        # For now, show a placeholder message with the address
        typer.echo(typer.style("\nWallet Balance", bold=True))
        typer.echo("=======================")
        typer.echo(f"📍 Address: {ss58_address}")
        typer.echo(
            typer.style(
                "⚠️  Balance checking functionality will be implemented in a future update.",
                fg=typer.colors.YELLOW,
            )
        )
        typer.echo(
            typer.style(
                "This will connect to the Hypertensor network to fetch the actual balance.",
                fg=typer.colors.YELLOW,
            )
        )

    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}")
        return


@app.command(name="import")
def import_wallet_cmd(
    name: str = wallet_config.name,
    password: str = wallet_config.password,
    path: str = wallet_config.path,
):
    """
    Import an existing wallet and return its keypair.

    Examples:
        # Import an encrypted wallet
        htcli wallet import --name mywallet --password mypassword
        htcli wallet import --wallet.name mywallet --wallet.password mypassword
        htcli wallet import --wallet-name mywallet --wallet-password mypassword

        # Import an unencrypted wallet
        htcli wallet import --name mywallet
    """
    try:
        # Use absolute path for wallet directory
        wallet_dir = Path(path or DEFAULT_WALLET_PATH).expanduser().resolve()

        # Prompt for wallet name if not provided
        if not name:
            name = typer.prompt("Enter wallet name")
            if not name:
                typer.echo("Error: Wallet name cannot be empty.")
                raise typer.Exit(code=1)

        wallet_path = wallet_dir / f"{name}.key"

        # Check if wallet exists before asking for password
        if not wallet_path.exists():
            raise typer.BadParameter(f"Wallet '{name}' not found at {wallet_path}")

        # Now that we know the wallet exists, prompt for password if not provided
        if password is None:
            password = getpass.getpass(f"Enter password for wallet '{name}': ")
            if password == "":
                password = None

        try:
            # Load the wallet
            keypair = import_wallet(name, wallet_dir, password)

            typer.echo(f"✅ Successfully imported wallet '{name}'")
            typer.echo(f"📍 Address: {keypair.ss58_address}")
            typer.echo(f"🔑 Public Key: 0x{keypair.public_key.hex()}")
            typer.echo(f"🔒 Private Key: 0x{keypair.private_key.hex()}")

            return keypair
        except ValueError as e:
            if "Invalid secret key" in str(e):
                typer.echo(
                    typer.style(
                        "❌ Error: Wrong Password - Failed to import wallet",
                        fg=typer.colors.RED,
                    )
                )
            else:
                typer.echo(
                    typer.style(
                        f"❌ Error: {str(e)}",
                        fg=typer.colors.RED,
                    )
                )
            raise typer.Exit(code=1)
        except Exception as e:
            typer.echo(
                typer.style(
                    f"❌ Error: Failed to import wallet - {str(e)}",
                    fg=typer.colors.RED,
                )
            )
            raise typer.Exit(code=1)

    except typer.BadParameter as e:
        typer.echo(
            typer.style(
                f"❌ Error: {str(e)}",
                fg=typer.colors.RED,
            )
        )
        raise typer.Exit(code=1)
    except Exception as e:
        if not str(e):  # Skip empty error messages
            raise typer.Exit(code=1)
        typer.echo(
            typer.style(
                f"❌ Error: Failed to import wallet - {str(e)}",
                fg=typer.colors.RED,
            )
        )
        raise typer.Exit(code=1)
