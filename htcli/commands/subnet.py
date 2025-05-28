import typer
from htcli.core.config import subnet_config, chain_config, wallet_config, options_config
from htcli.hypertensor.substrate.config import SubstrateConfigCustom, SubstrateConfigwithKeypair
from typing import Optional, List

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
wallet_cfg = wallet_config()
options_cfg = options_config()

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
    rpc_network: str = chain_config.rpc_network,
    name: str = wallet_cfg.name,
    path: str = subnet_config.path,
    memory_mb: int = subnet_config.memory_mb,
    registration_blocks: int = options_cfg.registration_blocks,
    entry_interval: int = options_cfg.entry_interval,
    max_node_registration_epochs: int = 10,
    node_registration_interval: int = 10,
    node_activation_interval: int = 10,
    node_queue_period: int = 10,
    max_node_penalties: int = 10,
    coldkey_whitelist: Optional[List[str]] = typer.Option(
        None,
        "--subnet.coldkey_whitelist",
        "--coldkey_whitelist",
        help="List of coldkeys to whitelist",
    )
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
    
    substrate = SubstrateConfigwithKeypair(name, rpc)
    
    if registration_blocks == 0:
        registration_blocks = int(
            str(get_max_subnet_registration_blocks(substrate.interface))
        )
    else:
        min_registration_blocks = int(
            str(get_min_subnet_registration_blocks(substrate.interface))
        )
        assert (
            registration_blocks >= min_registration_blocks
        ), f"Registration blocks must be >= {min_registration_blocks}. "

        max_registration_blocks = int(
            str(get_max_subnet_registration_blocks(substrate.interface))
        )
        assert (
            registration_blocks <= max_registration_blocks
        ), f"Registration blocks must be <= {max_registration_blocks}. "

    if entry_interval != 0:
        max_entry_interval = get_max_subnet_entry_interval(substrate.interface)
        assert (
            entry_interval <= max_entry_interval
        ), f"Entry interval blocks must be <= {max_entry_interval}. "

    print(f"Registering subnet at registration block - {registration_blocks}, entry interval - {entry_interval}")
    if coldkey_whitelist is None:
        coldkey_whitelist = []
    try:
        receipt = register_subnet(
            substrate.interface,
            substrate.keypair,
            path,
            memory_mb,
            registration_blocks,
            entry_interval,
            max_node_registration_epochs,
            node_registration_interval,
            node_activation_interval,
            node_queue_period,
            max_node_penalties,
            coldkey_whitelist
        )
        print(receipt)
    #     if receipt.is_success:
    #         typer.echo("✅ Success, triggered events:")
    #         for event in receipt.triggered_events:
    #             typer.echo(f"* {event.value}")
    #     else:
    #         typer.echo("⚠️ Extrinsic Failed: ", receipt.error_message)
    except Exception as e:
        typer.echo("Error: ", e)
    # typer.echo(f"Registering new subnet...")


@app.command()
def info(    
    subnet_id: int = subnet_cfg.id,
    wallet_name: str = wallet_cfg.name,
):
    """
    Get the info of the subnet
    """
    typer.echo(f"Getting info of the subnet {subnet_id}...")
    
    substrate = SubstrateConfigwithKeypair(wallet_name, "ws://127.0.0.1:9944")

    try:
        receipt = get_max_subnet_entry_interval(
            substrate.interface,
        )
        typer.echo(f"✅ Success, {receipt}")
    except Exception as e:
        typer.echo(f"Error: {e}")