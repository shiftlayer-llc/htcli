"""
Flattened subnet commands - 3-level hierarchy.
"""

import typer
from rich.console import Console
from typing import Optional
from ..models.requests import SubnetRegisterRequest, SubnetNodeAddRequest
from ..utils.validation import (
    validate_subnet_path,
    validate_memory_mb,
    validate_registration_blocks,
    validate_entry_interval,
    validate_address,
    validate_peer_id
)
from ..utils.formatting import (
    print_success, print_error, format_subnet_list, format_subnet_info, format_node_list
)
from ..dependencies import get_client

app = typer.Typer(name="subnet", help="Subnet operations")
console = Console()


@app.command()
def register(
    path: str = typer.Argument(..., help="Subnet path"),
    memory_mb: int = typer.Option(..., "--memory", "-m", help="Memory requirement in MB"),
    registration_blocks: int = typer.Option(..., "--blocks", "-b", help="Registration period in blocks"),
    entry_interval: int = typer.Option(..., "--interval", "-i", help="Entry interval in blocks"),
    max_node_registration_epochs: int = typer.Option(100, "--max-epochs", help="Maximum node registration epochs"),
    node_registration_interval: int = typer.Option(100, "--node-interval", help="Node registration interval"),
    node_activation_interval: int = typer.Option(100, "--activation-interval", help="Node activation interval"),
    node_queue_period: int = typer.Option(100, "--queue-period", help="Node queue period"),
    max_node_penalties: int = typer.Option(10, "--max-penalties", help="Maximum node penalties"),
    coldkey_whitelist: Optional[str] = typer.Option(None, "--whitelist", help="Comma-separated coldkey whitelist"),
):
    """Register a new subnet."""
    client = get_client()

    # Validate inputs
    if not validate_subnet_path(path):
        print_error("Invalid subnet path. Use alphanumeric characters, hyphens, and underscores only.")
        raise typer.Exit(1)

    if not validate_memory_mb(memory_mb):
        print_error("Invalid memory requirement. Must be between 1 and 100000 MB.")
        raise typer.Exit(1)

    if not validate_registration_blocks(registration_blocks):
        print_error("Invalid registration blocks. Must be between 1 and 1000000 blocks.")
        raise typer.Exit(1)

    if not validate_entry_interval(entry_interval):
        print_error("Invalid entry interval. Must be between 1 and 100000 blocks.")
        raise typer.Exit(1)

    try:
        # Parse whitelist if provided
        whitelist = []
        if coldkey_whitelist:
            whitelist = [addr.strip() for addr in coldkey_whitelist.split(",")]

        request = SubnetRegisterRequest(
            path=path,
            memory_mb=memory_mb,
            registration_blocks=registration_blocks,
            entry_interval=entry_interval,
            max_node_registration_epochs=max_node_registration_epochs,
            node_registration_interval=node_registration_interval,
            node_activation_interval=node_activation_interval,
            node_queue_period=node_queue_period,
            max_node_penalties=max_node_penalties,
            coldkey_whitelist=whitelist
        )

        response = client.register_subnet(request)
        print_success("✅ Subnet registered successfully!")
        console.print(f"Transaction: {response.transaction_hash}")
        if response.block_number:
            console.print(f"Block: #{response.block_number}")
    except Exception as e:
        print_error(f"Failed to register subnet: {str(e)}")
        raise typer.Exit(1)


@app.command()
def activate(
    subnet_id: int = typer.Argument(..., help="Subnet ID to activate"),
):
    """Activate a registered subnet."""
    client = get_client()

    try:
        response = client.activate_subnet(subnet_id)
        print_success(f"✅ Subnet {subnet_id} activated successfully!")
        console.print(f"Transaction: {response.transaction_hash}")
        if response.block_number:
            console.print(f"Block: #{response.block_number}")
    except Exception as e:
        print_error(f"Failed to activate subnet: {str(e)}")
        raise typer.Exit(1)


@app.command()
def list(
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """List all subnets."""
    client = get_client()

    try:
        response = client.get_subnets_data()
        if response.success:
            subnets = response.data.get('subnets', [])
            if format_type == "json":
                console.print_json(data=subnets)
            else:
                format_subnet_list(subnets)
        else:
            print_error(f"Failed to retrieve subnets: {response.message}")
    except Exception as e:
        print_error(f"Failed to list subnets: {str(e)}")
        raise typer.Exit(1)


@app.command()
def info(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """Get detailed information about a subnet."""
    client = get_client()

    try:
        response = client.get_subnet_data(subnet_id)
        if response.success:
            subnet_info = response.data
            if format_type == "json":
                console.print_json(data=subnet_info)
            else:
                format_subnet_info(subnet_info)
        else:
            print_error(f"Failed to retrieve subnet info: {response.message}")
    except Exception as e:
        print_error(f"Failed to get subnet info: {str(e)}")
        raise typer.Exit(1)


@app.command()
def add_node(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Node hotkey address"),
    peer_id: str = typer.Option(..., "--peer-id", "-p", help="Node peer ID"),
    delegate_reward_rate: int = typer.Option(1000, "--reward-rate", "-r", help="Delegate reward rate"),
    stake_amount: int = typer.Option(1000000000000000000, "--stake", "-s", help="Initial stake amount"),
):
    """Add a node to a subnet."""
    client = get_client()

    # Validate inputs
    if not validate_address(hotkey):
        print_error("Invalid hotkey address format.")
        raise typer.Exit(1)

    if not validate_peer_id(peer_id):
        print_error("Invalid peer ID format.")
        raise typer.Exit(1)

    try:
        request = SubnetNodeAddRequest(
            subnet_id=subnet_id,
            peer_id=peer_id,
            hotkey=hotkey,
            delegate_reward_rate=delegate_reward_rate,
            stake_to_be_added=stake_amount
        )

        response = client.add_subnet_node(request)
        print_success(f"✅ Node added to subnet {subnet_id} successfully!")
        console.print(f"Transaction: {response.transaction_hash}")
        if response.block_number:
            console.print(f"Block: #{response.block_number}")
    except Exception as e:
        print_error(f"Failed to add node: {str(e)}")
        raise typer.Exit(1)


@app.command()
def list_nodes(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """List all nodes in a subnet."""
    client = get_client()

    try:
        response = client.get_subnet_nodes(subnet_id)
        if response.success:
            nodes = response.data.get('nodes', [])
            if format_type == "json":
                console.print_json(data=nodes)
            else:
                format_node_list(nodes)
        else:
            print_error(f"Failed to retrieve subnet nodes: {response.message}")
    except Exception as e:
        print_error(f"Failed to list subnet nodes: {str(e)}")
        raise typer.Exit(1)


@app.command()
def remove(
    subnet_id: int = typer.Argument(..., help="Subnet ID to remove"),
):
    """Remove a subnet."""
    client = get_client()

    try:
        response = client.remove_subnet(subnet_id)
        print_success(f"✅ Subnet {subnet_id} removed successfully!")
        console.print(f"Transaction: {response.transaction_hash}")
        if response.block_number:
            console.print(f"Block: #{response.block_number}")
    except Exception as e:
        print_error(f"Failed to remove subnet: {str(e)}")
        raise typer.Exit(1)
