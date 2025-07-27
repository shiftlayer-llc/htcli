import typer
from htcli.core.constants import (
    DEFAULT_RPC_URL,
    DEFAULT_CHAIN_ENV,
)
from pathlib import Path
from .config.wallet import wallet_config
from .config.subnet import subnet_config


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


# Create instances for easy importing
chain_config_instance = chain_config()
