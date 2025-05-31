import typer
import os


class chain_config:
    rpc_url = typer.Option(
        "http://localhost:8000",
        "--chain.rpc_url",
        "--rpc_url",
        "--chain.url",
        help="RPC URL for the chain",
    )
    env = typer.Option(
        "local",
        "--chain.env",
        "--env",
        help="Environment for the chain (local/testnet/mainnet)",
    )

    def __repr__(self):
        return f"chain_config(rpc_url={self.rpc_url}, env={self.env})"


class subnet_config:
    id = typer.Option(
        0,
        "--subnet.id",
        "--subnet_id",
        "--netuid",
        help="Unique ID for the subnetwork",
    )
    name = typer.Option(
        "default",
        "--subnet.name",
        "--subnet_name",
        help="Name of the subnetwork",
    )


class wallet_config:
    path = typer.Option(
        os.path.expanduser("~/.hypertensor/wallets"),
        "--wallet.path",
        "--wallet_path",
        help="Path to the wallets directory",
    )
    name = typer.Option(
        None,
        "--wallet.name",
        "--wallet_name",
        help="Name of the wallet",
    )
    password = typer.Option(
        None,
        "--wallet.password",
        "--wallet_password",
        help="Password for the wallet",
    )
    hotkey = typer.Option(
        None,
        "--wallet.hotkey",
        help="Name of the hotkey wallet"
    )
    balance_ss58 = typer.Option(
        None,
        "--ss58-address",
        help="SS58 address to check balance"
    )
    remove_all = typer.Option(
        False,
        "--all",
        help="Remove all wallets"
    )
    regen_mnemonic = typer.Option(
        ...,
        "--mnemonic",
        help='Mnemonic phrase to regenerate the coldkey (must be in quotes, e.g. --mnemonic "word1 word2 word3 ...")'
    )
    list_wallet_name = typer.Option(
        None,
        "--wallet.name",
        help="Name of the wallet to list"
    )
    remove_wallet_name = typer.Option(
        None,
        "--wallet.name",
        help="Name of the wallet to remove"
    )
    balance_wallet_name = typer.Option(
        None,
        "--wallet.name",
        help="Name of the wallet to check balance"
    )
    regen_wallet_name = typer.Option(
        ...,
        "--wallet.name",
        help="Name of the wallet to regenerate"
    )
    remove_force = typer.Option(
        False,
        "--force",
        help="Skip confirmation prompt"
    )
    regen_force = typer.Option(
        False,
        "--force",
        help="Overwrite existing wallet if it exists"
    )

    def __repr__(self):
        return f"wallet_config(wallet_path={self.path}, name={self.name}"

    def __str__(self):
        return f"wallet_config(wallet_path={self.path}, name={self.name}"


class htcli_config:
    def __init__(
        self, chain: chain_config, subnet: subnet_config, wallet: wallet_config
    ):
        self.chain = chain
        self.subnet = subnet
        self.wallet = wallet

    def __repr__(self):
        return f"htcli_config(chain={self.chain}, subnet={self.subnet}, wallet={self.wallet})"

    def __str__(self):
        return f"htcli_config(chain={self.chain}, subnet={self.subnet}, wallet={self.wallet})"

    def __hash__(self):
        return hash((self.chain, self.subnet, self.wallet))

    def __eq__(self, other):
        if not isinstance(other, htcli_config):
            return False
        return (
            self.chain == other.chain
            and self.subnet == other.subnet
            and self.wallet == other.wallet
        )
