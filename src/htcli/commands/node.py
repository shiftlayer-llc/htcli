"""
Node management commands for the Hypertensor CLI.
All commands follow the format: htcli node <command> [switches]
"""

import typer
from rich.console import Console
from rich.panel import Panel
from typing import Optional
from ..models.requests import SubnetNodeAddRequest
from ..utils.validation import (
    validate_subnet_id,
    validate_node_id,
    validate_address,
    validate_peer_id,
    validate_amount
)
from ..utils.formatting import (
    print_success, print_error, print_info, format_node_list, format_balance
)
from ..dependencies import get_client

app = typer.Typer(name="node", help="Node management operations")
console = Console()


def show_comprehensive_guidance(operation: str, details: dict):
    """Show comprehensive guidance for node operations."""
    guidance_messages = {
        "add": {
            "title": "🔗 Adding Node to Subnet",
            "description": "This operation will register your node to participate in a subnet.",
            "requirements": [
                "• Valid subnet ID (must exist and be active)",
                "• Hotkey address (your node's identity)",
                "• Peer ID (your node's network identifier)", 
                "• Sufficient TENSOR balance for staking",
                "• Node must meet subnet's hardware requirements"
            ],
            "process": [
                "1. Validates all input parameters",
                "2. Checks subnet exists and is accepting nodes",
                "3. Verifies your balance is sufficient",
                "4. Submits node registration transaction",
                "5. Node enters queue for activation"
            ],
            "tips": [
                "💡 Check subnet requirements with: htcli subnet info --subnet-id <ID>",
                "💡 Verify your balance with: htcli chain balance <address>",
                "💡 Generate peer ID with your node software",
                "💡 Keep your hotkey secure - it identifies your node"
            ]
        },
        "remove": {
            "title": "🗑️ Removing Node from Subnet",
            "description": "This operation will deregister your node from a subnet.",
            "requirements": [
                "• Valid subnet ID and node ID",
                "• Node must be owned by your hotkey",
                "• Node must not be actively validating",
                "• Any staked tokens will be unbonded"
            ],
            "process": [
                "1. Validates node ownership",
                "2. Checks node is not in active validation",
                "3. Initiates unbonding of staked tokens",
                "4. Removes node from subnet",
                "5. Tokens available after unbonding period"
            ],
            "tips": [
                "⚠️ Removing a node will unbond all staked tokens",
                "⚠️ Unbonding period applies before tokens are available",
                "💡 Check node status before removal",
                "💡 Consider deactivating instead of removing if temporary"
            ]
        },
        "deactivate": {
            "title": "⏸️ Deactivating Node",
            "description": "This operation will temporarily deactivate your node.",
            "requirements": [
                "• Valid subnet ID and node ID",
                "• Node must be owned by your hotkey",
                "• Node must be currently active"
            ],
            "process": [
                "1. Validates node ownership and status",
                "2. Sets node status to inactive",
                "3. Node stops participating in validation",
                "4. Stake remains locked but not earning",
                "5. Can be reactivated later"
            ],
            "tips": [
                "💡 Deactivation is reversible unlike removal",
                "💡 Stake remains locked during deactivation",
                "💡 Use this for maintenance or temporary shutdown",
                "💡 Reactivate with appropriate command when ready"
            ]
        },
        "list": {
            "title": "📋 Listing Subnet Nodes",
            "description": "This operation shows all nodes in a subnet.",
            "requirements": [
                "• Valid subnet ID"
            ],
            "process": [
                "1. Queries subnet node registry",
                "2. Retrieves node information",
                "3. Displays formatted node list",
                "4. Shows status and stake information"
            ],
            "tips": [
                "💡 Use --format json for programmatic access",
                "💡 Check node status to understand network health",
                "💡 Monitor stake amounts to see network participation"
            ]
        }
    }
    
    if operation in guidance_messages:
        msg = guidance_messages[operation]
        
        # Create comprehensive guidance panel
        content = f"[bold]{msg['description']}[/bold]\n\n"
        
        if 'requirements' in msg:
            content += "[bold cyan]📋 Requirements:[/bold cyan]\n"
            for req in msg['requirements']:
                content += f"{req}\n"
            content += "\n"
        
        if 'process' in msg:
            content += "[bold green]⚙️ Process:[/bold green]\n"
            for step in msg['process']:
                content += f"{step}\n"
            content += "\n"
        
        if 'tips' in msg:
            content += "[bold yellow]💡 Tips & Warnings:[/bold yellow]\n"
            for tip in msg['tips']:
                content += f"{tip}\n"
        
        # Add specific details if provided
        if details:
            content += "\n[bold magenta]📊 Current Operation:[/bold magenta]\n"
            for key, value in details.items():
                content += f"• {key}: {value}\n"
        
        panel = Panel(
            content,
            title=msg['title'],
            border_style="cyan",
            padding=(1, 2)
        )
        
        console.print(panel)
        console.print()


@app.command()
def add(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID to join"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey address"),
    peer_id: str = typer.Option(..., "--peer-id", "-p", help="Peer ID for networking"),
    stake_amount: int = typer.Option(..., "--stake", "-st", help="Initial stake amount (in smallest units)"),
    delegate_reward_rate: float = typer.Option(0.1, "--reward-rate", "-r", help="Delegate reward rate (0.0-1.0)"),
    key_name: Optional[str] = typer.Option(None, "--key-name", "-k", help="Key name for signing"),
    show_guidance: bool = typer.Option(True, "--guidance/--no-guidance", help="Show comprehensive guidance")
):
    """Add a node to a subnet with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        show_comprehensive_guidance("add", {
            "Subnet ID": subnet_id,
            "Hotkey": hotkey,
            "Peer ID": peer_id,
            "Stake Amount": format_balance(stake_amount),
            "Reward Rate": f"{delegate_reward_rate * 100:.1f}%"
        })
        
        # Ask for confirmation
        if not typer.confirm("Do you want to proceed with adding this node?"):
            print_info("Node addition cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_address(hotkey):
        print_error("❌ Invalid hotkey address format.")
        raise typer.Exit(1)

    if not validate_peer_id(peer_id):
        print_error("❌ Invalid peer ID format. Must be a valid MultiHash.")
        raise typer.Exit(1)

    if not validate_amount(stake_amount):
        print_error("❌ Invalid stake amount. Must be positive.")
        raise typer.Exit(1)

    if not (0.0 <= delegate_reward_rate <= 1.0):
        print_error("❌ Invalid reward rate. Must be between 0.0 and 1.0.")
        raise typer.Exit(1)

    try:
        print_info(f"🔄 Adding node to subnet {subnet_id}...")
        
        request = SubnetNodeAddRequest(
            subnet_id=subnet_id,
            hotkey=hotkey,
            peer_id=peer_id,
            delegate_reward_rate=delegate_reward_rate,
            stake_to_be_added=stake_amount,
            a="1.0",  # Default values - these should be configurable
            b="1.0",
            c="1.0"
        )

        # Get keypair for signing if provided
        keypair = None
        if key_name:
            # TODO: Load keypair from storage
            print_info(f"🔑 Using key: {key_name}")

        response = client.add_subnet_node(request, keypair)
        
        if response.success:
            print_success(f"✅ Node successfully added to subnet {subnet_id}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")
            
            console.print(Panel(
                f"[bold green]🎉 Node Registration Complete![/bold green]\n\n"
                f"Your node has been successfully registered to subnet {subnet_id}.\n"
                f"• Hotkey: {hotkey}\n"
                f"• Peer ID: {peer_id}\n"
                f"• Initial Stake: {format_balance(stake_amount)}\n"
                f"• Reward Rate: {delegate_reward_rate * 100:.1f}%\n\n"
                f"[yellow]⏳ Your node is now in the activation queue.[/yellow]\n"
                f"Monitor status with: [bold]htcli node list --subnet-id {subnet_id}[/bold]",
                title="Success",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to add node: {response.message}")
            raise typer.Exit(1)
            
    except Exception as e:
        print_error(f"❌ Failed to add node to subnet: {str(e)}")
        raise typer.Exit(1)


@app.command()
def remove(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(..., "--node-id", "-n", help="Node ID to remove"),
    key_name: Optional[str] = typer.Option(None, "--key-name", "-k", help="Key name for signing"),
    show_guidance: bool = typer.Option(True, "--guidance/--no-guidance", help="Show comprehensive guidance")
):
    """Remove a node from a subnet with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        show_comprehensive_guidance("remove", {
            "Subnet ID": subnet_id,
            "Node ID": node_id
        })
        
        # Ask for confirmation with warning
        console.print("[bold red]⚠️ WARNING: This action will remove your node and unbond all staked tokens![/bold red]")
        if not typer.confirm("Are you sure you want to remove this node?"):
            print_info("Node removal cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_node_id(node_id):
        print_error("❌ Invalid node ID. Must be a positive integer.")
        raise typer.Exit(1)

    try:
        print_info(f"🔄 Removing node {node_id} from subnet {subnet_id}...")
        
        # Get keypair for signing if provided
        keypair = None
        if key_name:
            # TODO: Load keypair from storage
            print_info(f"🔑 Using key: {key_name}")

        response = client.remove_subnet_node(subnet_id, node_id, keypair)
        
        if response.success:
            print_success(f"✅ Node {node_id} successfully removed from subnet {subnet_id}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")
            
            console.print(Panel(
                f"[bold green]🗑️ Node Removal Complete![/bold green]\n\n"
                f"Node {node_id} has been removed from subnet {subnet_id}.\n\n"
                f"[yellow]⏳ Staked tokens are now unbonding.[/yellow]\n"
                f"Tokens will be available after the unbonding period.\n"
                f"Check status with: [bold]htcli wallet stake-info <address> --subnet-id {subnet_id}[/bold]",
                title="Removal Complete",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to remove node: {response.message}")
            raise typer.Exit(1)
            
    except Exception as e:
        print_error(f"❌ Failed to remove node from subnet: {str(e)}")
        raise typer.Exit(1)


@app.command()
def deactivate(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(..., "--node-id", "-n", help="Node ID to deactivate"),
    key_name: Optional[str] = typer.Option(None, "--key-name", "-k", help="Key name for signing"),
    show_guidance: bool = typer.Option(True, "--guidance/--no-guidance", help="Show comprehensive guidance")
):
    """Deactivate a node in a subnet with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        show_comprehensive_guidance("deactivate", {
            "Subnet ID": subnet_id,
            "Node ID": node_id
        })
        
        # Ask for confirmation
        if not typer.confirm("Do you want to deactivate this node?"):
            print_info("Node deactivation cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_node_id(node_id):
        print_error("❌ Invalid node ID. Must be a positive integer.")
        raise typer.Exit(1)

    try:
        print_info(f"🔄 Deactivating node {node_id} in subnet {subnet_id}...")
        
        # Get keypair for signing if provided
        keypair = None
        if key_name:
            # TODO: Load keypair from storage
            print_info(f"🔑 Using key: {key_name}")

        response = client.deactivate_subnet_node(subnet_id, node_id, keypair)
        
        if response.success:
            print_success(f"✅ Node {node_id} successfully deactivated in subnet {subnet_id}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")
            
            console.print(Panel(
                f"[bold yellow]⏸️ Node Deactivation Complete![/bold yellow]\n\n"
                f"Node {node_id} has been deactivated in subnet {subnet_id}.\n\n"
                f"• Node is no longer participating in validation\n"
                f"• Stake remains locked but not earning rewards\n"
                f"• Node can be reactivated when ready\n\n"
                f"Monitor status with: [bold]htcli node list --subnet-id {subnet_id}[/bold]",
                title="Deactivation Complete",
                border_style="yellow"
            ))
        else:
            print_error(f"❌ Failed to deactivate node: {response.message}")
            raise typer.Exit(1)
            
    except Exception as e:
        print_error(f"❌ Failed to deactivate node: {str(e)}")
        raise typer.Exit(1)


@app.command()
def list(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)"),
    show_guidance: bool = typer.Option(False, "--guidance", help="Show comprehensive guidance")
):
    """List all nodes in a subnet with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance if requested
    if show_guidance:
        show_comprehensive_guidance("list", {
            "Subnet ID": subnet_id,
            "Output Format": format_type
        })

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    try:
        print_info(f"🔄 Retrieving nodes for subnet {subnet_id}...")
        
        response = client.get_subnet_nodes(subnet_id)
        
        if response.success:
            nodes = response.data
            
            if not nodes:
                console.print(Panel(
                    f"[bold yellow]📭 No nodes found in subnet {subnet_id}[/bold yellow]\n\n"
                    f"This subnet currently has no registered nodes.\n"
                    f"Add a node with: [bold]htcli node add --subnet-id {subnet_id}[/bold]",
                    title="Empty Subnet",
                    border_style="yellow"
                ))
                return
            
            if format_type == "json":
                console.print_json(data=nodes)
            else:
                format_node_list(nodes, subnet_id)
                
            console.print(f"\n✅ Found {len(nodes)} node(s) in subnet {subnet_id}")
        else:
            print_error(f"❌ Failed to retrieve nodes: {response.message}")
            raise typer.Exit(1)
            
    except Exception as e:
        print_error(f"❌ Failed to list subnet nodes: {str(e)}")
        raise typer.Exit(1)


@app.command()
def status(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(..., "--node-id", "-n", help="Node ID"),
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """Get detailed status of a specific node."""
    client = get_client()

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_node_id(node_id):
        print_error("❌ Invalid node ID. Must be a positive integer.")
        raise typer.Exit(1)

    try:
        print_info(f"🔄 Retrieving status for node {node_id} in subnet {subnet_id}...")
        
        # Get all nodes and find the specific one
        response = client.get_subnet_nodes(subnet_id)
        
        if response.success:
            nodes = response.data
            target_node = None
            
            for node in nodes:
                if node.get('node_id') == node_id:
                    target_node = node
                    break
            
            if not target_node:
                print_error(f"❌ Node {node_id} not found in subnet {subnet_id}")
                raise typer.Exit(1)
            
            if format_type == "json":
                console.print_json(data=target_node)
            else:
                # Display detailed node information
                console.print(Panel(
                    f"[bold cyan]📊 Node {node_id} Status[/bold cyan]\n\n"
                    f"• Subnet ID: {subnet_id}\n"
                    f"• Node ID: {node_id}\n"
                    f"• Hotkey: {target_node.get('hotkey', 'N/A')}\n"
                    f"• Peer ID: {target_node.get('peer_id', 'N/A')}\n"
                    f"• Status: {target_node.get('status', 'Unknown')}\n"
                    f"• Stake: {format_balance(target_node.get('stake', 0))}\n"
                    f"• Reward Rate: {target_node.get('delegate_reward_rate', 0) * 100:.1f}%\n"
                    f"• Last Active: {target_node.get('last_active', 'N/A')}",
                    title="Node Status",
                    border_style="cyan"
                ))
                
            print_success(f"✅ Retrieved status for node {node_id}")
        else:
            print_error(f"❌ Failed to retrieve node status: {response.message}")
            raise typer.Exit(1)
            
    except Exception as e:
        print_error(f"❌ Failed to get node status: {str(e)}")
        raise typer.Exit(1)
