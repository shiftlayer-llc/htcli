import typer
from htcli.core.config import subnet_config, chain_config, wallet_config, options_config
from htcli.hypertensor.substrate.config import SubstrateConfigCustom
from htcli.hypertensor.substrate.chain_functions import (
    get_max_subnet_entry_interval,
    get_max_subnet_registration_blocks,
    get_min_subnet_registration_blocks,
    register_subnet,
    activate_subnet,
    remove_subnet,
    get_block_number,
)
from pathlib import Path

app = typer.Typer(name="subnet", help="Subnet commands")

chain_cfg = chain_config()
subnet_cfg = subnet_config()
wallet_cfg = wallet_config()
options_cfg = options_config()

@app.command()
def info(    
    subnet_id: int = subnet_cfg.id,
):
    """
    Get the info of the subnet
    """
    typer.echo(f"Getting info of the subnet {subnet_id}...")
    
    
    substrate = SubstrateConfigCustom("", "ws://127.0.0.1:9944")

    try:
        receipt = get_block_number(
            substrate.interface,
        )
        typer.echo(f"✅ Success, block number: {receipt}")
    except Exception as e:
        typer.echo(f"Error: {e}")

@app.command()
def register(
    rpc_url: str = chain_cfg.rpc_url,
    env: str = chain_cfg.env,
    phrase: str = wallet_cfg.phrase,
    path: str = subnet_config.path,
    memory_mb: int = subnet_config.memory_mb,
    registration_blocks: int = options_cfg.registration_blocks,
    entry_interval: int = options_cfg.entry_interval,
):
    """
    Register a subnet
    """
    typer.echo(f"Regsitering a subnet...")

    if rpc_url:
        rpc = rpc_url
    else:
        if env == "local":
            rpc = "ws://127.0.0.1"
        elif env == "dev":
            #TODO: please add dev rpc url
            rpc = "DEV_RPC"

    if phrase is not None:
        substrate = SubstrateConfigCustom(phrase, rpc)
    else:
        substrate = SubstrateConfigCustom(PHRASE, rpc)

    if registration_blocks == 0:
        registration_blocks = int(
            str(get_min_subnet_registration_blocks(substrate.interface))
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

    try:
        receipt = register_subnet(
            substrate.interface,
            substrate.keypair,
            path,
            memory_mb,
            registration_blocks,
            entry_interval,
        )
        if receipt.is_success:
            typer.echo("✅ Success, triggered events:")
            for event in receipt.triggered_events:
                typer.echo(f"* {event.value}")
        else:
            typer.echo("⚠️ Extrinsic Failed: ", receipt.error_message)
    except Exception as e:
        typer.echo("Error: ", e, exc_info=True)



@app.command()
def activate(
    rpc_url: str = chain_cfg.rpc_url,
    env: str = chain_cfg.env,
    phrase: str = wallet_cfg.phrase,
    subnet_id: int = subnet_cfg.id,
):
    """
    Activate a registered subnet
    """
    typer.echo(f"Activating a subnet {subnet_id}...")
    
    if rpc_url:
        rpc = rpc_url
    else:
        if env == "local":
            rpc = "ws://127.0.0.1"
        elif env == "dev":
            #TODO: please add dev rpc url
            rpc = "DEV_RPC"
    if phrase is not None:
        substrate = SubstrateConfigCustom(phrase, rpc)
    else:
        substrate = SubstrateConfigCustom(PHRASE, rpc)

    try:
        receipt = activate_subnet(
            substrate.interface,
            substrate.keypair,
            subnet_id,
        )
        if receipt.is_success:
            typer.echo('✅ Success, triggered events:')
            for event in receipt.triggered_events:
                typer.echo(f'* {event.value}')
        else:
            typer.echo('⚠️ Extrinsic Failed: ', receipt.error_message)
    except Exception as e:
        typer.echo("Error: ", e, exc_info=True)



@app.command()
def remove(
    rpc_url: str = chain_cfg.rpc_url,
    env: str = chain_cfg.env,
    phrase: str = wallet_cfg.phrase,
    subnet_id: int = subnet_cfg.id,
):
    """
    Remove a subnet
    """
    typer.echo(f"Removing a subnet {subnet_id}...")
    if rpc_url:
        rpc = rpc_url
    else:
        if env == "local":
            rpc = "ws://127.0.0.1"
        elif env == "dev":
            #TODO: please add dev rpc url
            rpc = "DEV_RPC"
    if phrase is not None:
        substrate = SubstrateConfigCustom(phrase, rpc)
    else:
        substrate = SubstrateConfigCustom(PHRASE, rpc)
    try:
        receipt = remove_subnet(
            substrate.interface,
            substrate.keypair,
            subnet_id,
        )
        if receipt.is_success:
            typer.echo('✅ Success, triggered events:')
            for event in receipt.triggered_events:
                typer.echo(f'* {event.value}')
        else:
            typer.echo('⚠️ Extrinsic Failed: ', receipt.error_message)
    except Exception as e:
        typer.echo("Error: ", e, exc_info=True)


@app.command()
def nodes(
    subnet_id: int = subnet_cfg.id,
):
    """
    List all subnet nodes info in the subnet
    """
    typer.echo(f"List all subnet nodes info in the subnet {subnet_id}...")
    # Here you would implement the logic to list all subnet nodes info in the subnet
    # For now, we'll just print a message
    # This is a placeholder for the actual implementation


@app.command()
def list():
    """
    List all subnets
    """
    typer.echo(f"List all subnets...")
    # Here you would implement the logic to list all subnets
    # For now, we'll just print a message
    # This is a placeholder for the actual implementation
