import os
from pathlib import Path
import typer

# Default paths
DEFAULT_WALLET_PATH = os.path.expanduser("~/.hypertensor/wallets")

# Wallet options
WALLET_NAME_OPTION = typer.Option(
    None,
    "--wallet.name",
    help="Name of the wallet"
)

WALLET_PASSWORD_OPTION = typer.Option(
    None,
    "--wallet.password",
    help="Password for the wallet (for encryption)"
)

WALLET_HOTKEY_OPTION = typer.Option(
    None,
    "--wallet.hotkey",
    help="Name of the hotkey wallet"
)

WALLET_PATH_OPTION = typer.Option(
    None,
    "--path",
    help="Base path to store the wallets"
)

# Balance command options
BALANCE_WALLET_NAME_OPTION = typer.Option(
    None,
    "--wallet.name",
    help="Name of the wallet to check balance"
)

BALANCE_SS58_OPTION = typer.Option(
    None,
    "--ss58-address",
    help="SS58 address to check balance"
)

# List command options
LIST_WALLET_NAME_OPTION = typer.Option(
    None,
    "--wallet.name",
    help="Name of the wallet to list (if not provided, lists all wallets)"
)

# Remove command options
REMOVE_WALLET_NAME_OPTION = typer.Option(
    None,
    "--wallet.name",
    help="Name of the wallet to remove"
)

REMOVE_ALL_OPTION = typer.Option(
    False,
    "--all",
    help="Remove all wallets"
)

REMOVE_FORCE_OPTION = typer.Option(
    False,
    "--force",
    help="Skip confirmation prompt"
)

# Regen command options
REGEN_WALLET_NAME_OPTION = typer.Option(
    ...,
    "--wallet.name",
    help="Name of the wallet to regenerate"
)

REGEN_MNEMONIC_OPTION = typer.Option(
    ...,
    "--mnemonic",
    help='Mnemonic phrase to regenerate the coldkey (must be in quotes, e.g. --mnemonic "word1 word2 word3 ...")'
)

REGEN_FORCE_OPTION = typer.Option(
    False,
    "--force",
    help="Overwrite existing wallet if it exists"
)

# File paths and names
COLDKEY_FILE_NAME = "coldkey"
HOTKEYS_DIR_NAME = "hotkeys" 