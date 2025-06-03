import typer
from htcli.core.config import subnet_config, chain_config, wallet_config, options_config
from htcli.hypertensor.substrate.config import SubstrateConfigCustom, SubstrateConfigwithKeypair
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from substrateinterface import SubstrateInterface
import os
from htcli.hypertensor.substrate.chain_functions import (
    register_subnet_node
)
subnet_cfg = subnet_config()
wallet_cfg = wallet_config()
options_cfg = options_config()
console = Console()

app = typer.Typer(name="node", help="Node commands")

def get_rpc_url(rpc_network: str):
    """
    Get the RPC URL based on the network
    """
    if rpc_network == "main":
        return os.getenv("RPC_URL_MAINNET")
    elif rpc_network == "test":
        return os.getenv("RPC_URL_TESTNET")
    elif rpc_network == "local":
        return os.getenv("RPC_URL_LOCALNET")
    else:
        raise ValueError(f"Unknown network: {rpc_network}")


@app.command()
def register(
    rpc_url: str = chain_config.rpc_url,
    rpc_network: str = chain_config.rpc_network,
    wallet_name: str = wallet_cfg.name,
    subnet_id: int = subnet_cfg.id,
):
    """
    Register a node to the subnet.
    """
    # Create a SubstrateInterface instance using the chain configuration
    if rpc_url:
        rpc = rpc_url
        typer.echo(f"Connecting to {rpc}")
    else:
        if rpc_network:
            rpc = get_rpc_url(rpc_network)
            typer.echo(f"Connecting to {rpc_network} ({rpc})")
        else:
            rpc = os.getenv("RPC_URL_MAINNET")
    
    substrate = SubstrateConfigwithKeypair(wallet_name, rpc)
    # try:
    #     with console.status("[bold green]Registering subnet...[/bold green]", spinner="dots"):
    #         receipt = register_subnet_node(
    #             substrate.interface,
    #             substrate.keypair,
    #             subnet_id,
    #             wallet_name
    #         )
    # except Exception as e:
    #     typer.echo("Error: ", e)