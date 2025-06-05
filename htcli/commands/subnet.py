import typer
from htcli.core.config.chain import chain_config
from htcli.core.config.subnet import subnet_config
from htcli.core.config.wallet import wallet_config
from htcli.utils.substrate import SubstrateConfigwithKeypair
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from substrateinterface import SubstrateInterface
from pathlib import Path
from htcli.utils.chain_functions import (
    register_subnet,
    activate_subnet,
    remove_subnet,
    get_subnets_list,
    get_subnet_info
)

from htcli.utils.subnet import (
    get_rpc,
    check_name,
    check_path,
    check_wallet_path,
    check_password
)

console = Console()
app = typer.Typer(name="subnet", help="Subnet commands")

@app.command()
def register(
    rpc_url: str = chain_config.rpc_url,
    rpc_network: str = chain_config.env,
    name: str = wallet_config.name,
    wallet_path: str = wallet_config.path,
    path: str = subnet_config.path,
    wallet_password: str = wallet_config.password,
    max_node_registration_epochs: int = subnet_config.max_node_registration_epochs, # The maximum number of epochs a node can stay registered without being validated or promoted.
    node_registration_interval: int = subnet_config.node_registration_interval, # How frequently (in blocks) new nodes can be registered to the subnet.
    node_activation_interval: int = subnet_config.node_activation_interval, # How frequently (in blocks) registered nodes are activated into the network for participation.
    node_queue_period: int = subnet_config.node_queue_period, # How many epochs a node spends in the Queue class (a waiting area) before being considered for consensus.
    max_node_penalties: int = subnet_config.max_node_penalties, # Maximum number of penalties a node can receive before being kicked from the subnet.
    coldkey_whitelist: Optional[List[str]] = subnet_config.coldkey_whitelist,  # List of coldkeys to whitelist for the subnet
):
    """
    Register a new subnet
    This command registers a new subnet with the specified parameters.
    The subnet is identified by a unique ID and can have a specific path for data storage.
    The command also allows for setting various parameters related to node registration and activation.
    The coldkey whitelist is a list of coldkeys that are allowed to register nodes in the subnet.
    If no coldkey whitelist is provided, a default list of coldkeys will be used.
    The command will connect to the specified RPC URL or use the default RPC URL for the specified network.
    If the RPC URL is not provided, it will use the RPC URL from the environment variable or the default configuration.
    Usage:
    htcli subnet register --rpc_url <RPC_URL> --name <WALLET_NAME> --path <SUBNET_PATH>
    --max_node_registration_epochs <EPOCHS> --node_registration_interval <INTERVAL> --node_activation_interval <INTERVAL> --node_queue_period <PERIOD> --max_node_penalties <PENALTIES> --coldkey_whitelist <COLDKEYS>
    """

    rpc = get_rpc(rpc_url, rpc_network)
    typer.echo(f"Connecting to {rpc}")
    name = check_name(name)
    wallet_path = Path(check_wallet_path(wallet_path))
    path = check_path(path)
    wallet_password = check_password(wallet_password)

    substrate = SubstrateConfigwithKeypair(name, rpc, wallet_path, wallet_password)
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


@app.command()
def info(    
    rpc_url: str = chain_config.rpc_url,
    rpc_network: str = chain_config.env,
    subnet_id: int = subnet_config.id,
):
    """
    Get the info of the subnet
    """
    rpc = get_rpc(rpc_url, rpc_network)
    typer.echo(f"Connecting to {rpc}")
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
    rpc_network: str = chain_config.env,
    name: str = wallet_config.name,
    subnet_id: int = subnet_config.id,
):
    """
    Activate a registered subnet
    """
    rpc = get_rpc(rpc_url, rpc_network)
    typer.echo(f"Connecting to {rpc}")
    name = check_name(name)
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
    rpc_network: str = chain_config.env,
):
    """
    List all registered subnets
    """
    rpc = get_rpc(rpc_url, rpc_network)
    typer.echo(f"Connecting to {rpc}")
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
    rpc_network: str = chain_config.env,
    name: str = wallet_config.name,
    subnet_id: int = subnet_config.id,
):
    """
    Remove a subnet
    """
    rpc = get_rpc(rpc_url, rpc_network)
    typer.echo(f"Connecting to {rpc}")
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
    """
    Print a table of registered subnets
    """
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