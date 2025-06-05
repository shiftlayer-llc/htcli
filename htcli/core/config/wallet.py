import typer
from htcli.core.constants import DEFAULT_WALLET_PATH


class wallet_config:
    """Wallet configuration options."""

    name = typer.Option(
        None,
        "--name",
        "--wallet.name",
        "--wallet-name",
        help="Name of the wallet",
    )
    password = typer.Option(
        None,
        "--password",
        "--wallet.password",
        "--wallet-password",
        help="Password for the wallet",
    )
    path = typer.Option(
        None,
        "--path",
        "--wallet.path",
        "--wallet-path",
        help="Path to the wallets directory",
    )
    type = typer.Option(
        None,
        "--type",
        "--wallet.type",
        "--wallet-type",
        help="Type of wallet (coldkey or hotkey)",
    )
    coldkey = typer.Option(
        None,
        "--coldkey",
        "--wallet.coldkey",
        "--wallet-coldkey",
        help="Coldkey name for owned hotkey",
    )
    hotkey = typer.Option(
        None,
        "--hotkey",
        "--wallet.hotkey",
        "--wallet-hotkey",
        help="Hotkey name for owned hotkey",
    )
    force = typer.Option(
        False,
        "--force",
        help="Skip confirmation prompt or overwrite existing wallet",
    )
    all = typer.Option(
        False,
        "--all",
        help="Indicates to <all wallets>, <whole balance>, ....",
    )
    mnemonic = typer.Option(
        None,
        "--mnemonic",
        "--wallet.mnemonic",
        "--wallet-mnemonic",
        help='Mnemonic phrase of the wallet (must be in quotes, e.g. --mnemonic "word1 word2 word3 ...")',
    )
    ss58_address = typer.Option(
        None,
        "--ss58-address",
        "--wallet.ss58-address",
        help="SS58 address to check balance",
    )
    default_wallet_path = DEFAULT_WALLET_PATH

    def __repr__(self):
        return f"wallet_config(wallet_path={self.path}, name={self.name}"

    def __str__(self):
        return f"wallet_config(wallet_path={self.path}, name={self.name}"
