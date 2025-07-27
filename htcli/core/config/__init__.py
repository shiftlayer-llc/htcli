# Import config classes to make them available
from .subnet import subnet_config
from .wallet import wallet_config

# Define chain_config here to avoid circular imports
import typer
from htcli.core.constants import DEFAULT_RPC_URL, DEFAULT_CHAIN_ENV

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

# Create instances for easy importing
chain_config_instance = chain_config()
