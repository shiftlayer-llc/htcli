import typer
from htcli.core.constants import (
    DEFAULT_RPC_URL,
    DEFAULT_CHAIN_ENV,
)


class chain_config:
    rpc_url = typer.Option(
        None,
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