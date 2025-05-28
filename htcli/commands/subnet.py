import typer
from htcli.core.config import subnet_config, chain_config
from htcli.hypertensor.substrate.config import SubstrateConfigCustom


from htcli.hypertensor.substrate.chain_functions import (
    get_max_subnet_entry_interval,
    get_max_subnet_registration_blocks,
    get_min_subnet_registration_blocks,
    register_subnet,
    activate_subnet,
    remove_subnet,
)

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(Path.cwd(), ".env"))

app = typer.Typer(name="subnet", help="Subnet commands")

subnet_cfg = subnet_config()

PHRASE = os.getenv("PHRASE")

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
    rpc_network: str = chain_config.rpc_network
):
    """
    Register a new subnet
    """
    if rpc_url:
        rpc = rpc_url
        typer.echo(f"Connecting to {rpc}")
    else:
        if rpc_network:
            rpc = get_rpc_url(rpc_network)
            typer.echo(f"Connecting to {rpc_network} ({rpc})")
    typer.echo(f"Registering subnet")


@app.command()
def info(subnet_id: int = subnet_cfg.id, subnet_name: str = subnet_cfg.name):
    """
    Get the info of the subnet
    """
    typer.echo(f"Getting info of subnet {subnet_name} with {subnet_id} ...")
    # Here you would implement the logic to get the info of the subnet
    # For now, we'll just print a message
    # This is a placeholder for the actual implementation
