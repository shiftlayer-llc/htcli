import typer
from htcli.core.constants import (
    DEFAULT_WALLET_PATH,
    DEFAULT_RPC_URL,
    DEFAULT_CHAIN_ENV,
    DEFAULT_SUBNET_ID,
    DEFAULT_SUBNET_NAME,
)


class chain_config:
    rpc_url = typer.Option(
        DEFAULT_RPC_URL,
        "--chain.rpc_url",
        "--rpc_url",
        "--chain.url",
        help="RPC URL for the chain",
    )
    env = typer.Option(
        DEFAULT_CHAIN_ENV,
        "--chain.env",
        "--env",
        help="Environment for the chain (local/testnet/mainnet)",
    )

    def __repr__(self):
        return f"chain_config(rpc_url={self.rpc_url}, env={self.env})"


class subnet_config:
    id = typer.Option(
        DEFAULT_SUBNET_ID,
        "--subnet.id",
        "--subnet-id",
        "--netuid",
        help="Unique ID for the subnetwork",
    )
    name = typer.Option(
        DEFAULT_SUBNET_NAME,
        "--subnet.name",
        "--subnet-name",
        help="Name of the subnetwork",
    )


class wallet_config:
    path = typer.Option(
        DEFAULT_WALLET_PATH,
        "--wallet.path",
        "--wallet-path",
        help="Path to the wallets directory",
    )
    name = typer.Option(
        None,
        "--wallet.name",
        "--wallet-name",
        help="Name of the wallet",
    )
    password = typer.Option(
        None,
        "--wallet.password",
        "--wallet-password",
        help="Password for the wallet",
    )
    hotkey = typer.Option(None, "--wallet.hotkey", help="Name of the hotkey wallet")
    ss58_address = typer.Option(
        None, "--ss58-address", help="SS58 address to check balance"
    )
    remove_all = typer.Option(False, "--all", help="Remove all wallets")
    mnemonic = typer.Option(
        None,
        "--mnemonic",
        help='Mnemonic phrase to regenerate the coldkey (must be in quotes, e.g. --mnemonic "word1 word2 word3 ...")',
    )
    force = typer.Option(
        False, "--force", help="Skip confirmation prompt or overwrite existing wallet"
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
