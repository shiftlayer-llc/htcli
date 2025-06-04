import typer
from htcli.core.config import subnet_config, chain_config, wallet_config, options_config
from htcli.hypertensor.substrate.config import SubstrateConfigCustom, SubstrateConfigwithKeypair
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from substrateinterface import SubstrateInterface

console = Console()
from htcli.hypertensor.substrate.chain_functions import (
    get_max_subnet_entry_interval,
    get_max_subnet_registration_blocks,
    get_min_subnet_registration_blocks,
    register_subnet,
    activate_subnet,
    remove_subnet,
    get_subnets_list,
    get_subnet_info

)

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(Path.cwd(), ".env"))

app = typer.Typer(name="subnet", help="Subnet commands")

# subnet_config = subnet_config()
# wallet_config = wallet_config()

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
    name: str = wallet_config.name,
    path: str = subnet_config.path,
    max_node_registration_epochs: int = 1000, # The maximum number of epochs a node can stay registered without being validated or promoted.
    node_registration_interval: int = 100, # How frequently (in blocks) new nodes can be registered to the subnet.
    node_activation_interval: int = 100, # How frequently (in blocks) registered nodes are activated into the network for participation.
    node_queue_period: int = 10, # How many epochs a node spends in the Queue class (a waiting area) before being considered for consensus.
    max_node_penalties: int = 5, # Maximum number of penalties a node can receive before being kicked from the subnet.
    coldkey_whitelist: Optional[List[str]] = subnet_config.coldkey_whitelist,  # List of coldkeys to whitelist for the subnet
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
        else:
            rpc = os.getenv("RPC_URL_MAINNET")
    
    substrate = SubstrateConfigwithKeypair(name, rpc)

    if coldkey_whitelist is None:
        coldkey_whitelist = [
            "0x64d24a7d9588413f790a80122ca1664f5b0ac53055974476b65706f5e480da6e",
            "0xfa8180d137b00905c369bcd5ea808a63654b754413327f6e894b19f61d931561"
        ]    
    try:
        
        receipt = register_subnet(
            substrate.interface,
            substrate.keypair,
            path,
            max_node_registration_epochs,
            node_registration_interval,
            node_activation_interval,
            node_queue_period,
            max_node_penalties,
            coldkey_whitelist
        )

        if receipt is None:
            console.log("[red]No receipt returned. Please check the transaction status.[/red]")
        else:
            console.print(f"[blue]Extrinsic Hash: {receipt.extrinsic_hash}[/blue]")
            console.print(f"[blue]Block Hash: {receipt.block_hash}[/blue]")
            console.print("[green]✅ Subnet registered successfully![/green]")

    except Exception as e:
        console.log(f"[red]❌ Failed to register subnet: {str(e)}[/red]")
        typer.echo(f"Error: {str(e)}")


@app.command()
def info(    
    rpc_url: str = chain_config.rpc_url,
    rpc_network: str = chain_config.rpc_network,
    subnet_id: int = subnet_config.id,
    # wallet_name: str = wallet_config.name,
):
    """
    Get the info of the subnet
    """

    if rpc_url:
        rpc = rpc_url
        typer.echo(f"Connecting to {rpc}")
    else:
        if rpc_network:
            rpc = get_rpc_url(rpc_network)
            typer.echo(f"Connecting to {rpc_network} ({rpc})")
        else:
            rpc = os.getenv("RPC_URL_MAINNET")
    
    substrate_interface = SubstrateInterface(url=rpc)

    try:
        with console.status(f"[bold green]Getting info of subnet {subnet_id}...[/bold green]", spinner="dots"):
            receipt = get_subnet_info(
                substrate_interface, subnet_id
            )
        if receipt["is_success"] is True:
            console.print(f"[blue]Subnet ID: {receipt['meta']['id']}[/blue]")
            console.print(f"[blue]Path: {receipt['meta']['path']}[/blue]")
            console.print(f"[blue]State: {receipt['meta']['state']}[/blue]")
            console.print(f"[blue]Total Active Nodes: {receipt['meta']['total_active_nodes']}[/blue]")
            console.print(f"[blue]Subnet Owner: {receipt['meta']['owner']}[/blue]")
        else:
            console.log(f"[red]Error Message: {receipt['error_message']}[/red]")
            return
    except Exception as e:
        typer.echo(f"Error: {e}")


@app.command()
def activate(
    rpc_url: str = chain_config.rpc_url,
    rpc_network: str = chain_config.rpc_network,
    name: str = wallet_config.name,
    subnet_id: int = subnet_config.id,
):
    """
    Activate a registered subnet
    """
    if rpc_url:
        rpc = rpc_url
        typer.echo(f"Connecting to {rpc}")
    else:
        if rpc_network:
            rpc = get_rpc_url(rpc_network)
            typer.echo(f"Connecting to {rpc_network} ({rpc})")
    
    substrate = SubstrateConfigwithKeypair(name, rpc)

    try:
        with console.status(f"[bold green]Activating subnet {subnet_id}...[/bold green]", spinner="dots"):
            receipt = activate_subnet(
                substrate.interface,
                substrate.keypair,
                subnet_id,
            )
        if receipt.is_success == False:
            console.log(f"[red]Error Message: {receipt.error_message}[/red]")
        else:
            console.log("[green]Subnet activated successfully![/green]")
    except Exception as e:
        typer.echo("Error: ", e)



@app.command()
def list(
    rpc_url: str = chain_config.rpc_url,
    rpc_network: str = chain_config.rpc_network,
    name: str = wallet_config.name,
):
    """
    List all registered subnets
    """
    if rpc_url:
        rpc = rpc_url
        typer.echo(f"Connecting to {rpc}")
    else:
        if rpc_network:
            rpc = get_rpc_url(rpc_network)
            typer.echo(f"Connecting to {rpc_network} ({rpc})")
        else:
            rpc = get_rpc_url("main")
            typer.echo(f"Connecting to main ({rpc})")
    
    substrate_interface = SubstrateInterface(url=rpc)


    try:
        with console.status("[bold green]Listing all registered subnets...[/bold green]", spinner="dots"):
            receipt = get_subnets_list(
                substrate_interface,
            )

        print_subnets_table(receipt)
    except Exception as e:
        typer.echo("Error: ", e)

@app.command()
def remove(
    rpc_url: str = chain_config.rpc_url,
    rpc_network: str = chain_config.rpc_network,
    name: str = wallet_config.name,
    subnet_id: int = subnet_config.id,
):
    """
    Remove a subnet
    """
    if rpc_url:
        rpc = rpc_url
        typer.echo(f"Connecting to {rpc}")
    else:
        if rpc_network:
            rpc = get_rpc_url(rpc_network)
            typer.echo(f"Connecting to {rpc_network} ({rpc})")
        else:
            rpc = get_rpc_url("main")
            typer.echo(f"Connecting to main ({rpc})")

    substrate = SubstrateConfigwithKeypair(name, rpc)

    try:
        with console.status(f"[bold green]Removing subnet {subnet_id}...[/bold green]", spinner="dots"):
            receipt = remove_subnet(
                substrate.interface,
                substrate.keypair,
                subnet_id,
            )
        console.log(f"[blue]Extrinsic Hash: {receipt.extrinsic_hash} [/blue]")
        console.log(f"[blue]Block Hash: {receipt.block_hash} [/blue]", )
        if receipt.is_success == False:

            console.log(f"[red]Error Message: {receipt.error_message}[/red]")
        else:
            console.log("[green]Subnet registered successfully![/green]")
    except Exception as e:
        typer.echo("Error: ", e)

def print_subnets_table(receipt):
    table = Table(title="Registered Subnets")

    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Path", style="magenta")
    table.add_column("State", style="green")
    table.add_column("Active Nodes", justify="center", style="yellow")
    table.add_column("Owner", style="white")

    for subnet in receipt:
        table.add_row(
            str(subnet["id"]),
            subnet["path"] or "-",
            subnet["state"],
            str(subnet["total_active_nodes"]),
            subnet["subnet_owner"]
        )

    console = Console()
    console.print(table)