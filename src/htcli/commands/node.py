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
    validate_amount,
    validate_delegate_reward_rate,
)
from ..utils.formatting import (
    print_success,
    print_error,
    print_info,
    format_node_list,
    format_balance,
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
                "• Node must meet subnet's hardware requirements",
            ],
            "process": [
                "1. Validates all input parameters",
                "2. Checks subnet exists and is accepting nodes",
                "3. Verifies your balance is sufficient",
                "4. Submits node registration transaction",
                "5. Node enters queue for activation",
            ],
            "tips": [
                "💡 Check subnet requirements with: htcli subnet info --subnet-id <ID>",
                "💡 Verify your balance with: htcli chain balance <address>",
                "💡 Generate peer ID with your node software",
                "💡 Keep your hotkey secure - it identifies your node",
            ],
        },
        "remove": {
            "title": "🗑️ Removing Node from Subnet",
            "description": "This operation will deregister your node from a subnet.",
            "requirements": [
                "• Valid subnet ID and node ID",
                "• Node must be owned by your hotkey",
                "• Node must not be actively validating",
                "• Any staked tokens will be unbonded",
            ],
            "process": [
                "1. Validates node ownership",
                "2. Checks node is not in active validation",
                "3. Initiates unbonding of staked tokens",
                "4. Removes node from subnet",
                "5. Tokens available after unbonding period",
            ],
            "tips": [
                "⚠️ Removing a node will unbond all staked tokens",
                "⚠️ Unbonding period applies before tokens are available",
                "💡 Check node status before removal",
                "💡 Consider deactivating instead of removing if temporary",
            ],
        },
        "deactivate": {
            "title": "⏸️ Deactivating Node",
            "description": "This operation will temporarily deactivate your node.",
            "requirements": [
                "• Valid subnet ID and node ID",
                "• Node must be owned by your hotkey",
                "• Node must be currently active",
            ],
            "process": [
                "1. Validates node ownership and status",
                "2. Sets node status to inactive",
                "3. Node stops participating in validation",
                "4. Stake remains locked but not earning",
                "5. Can be reactivated later",
            ],
            "tips": [
                "💡 Deactivation is reversible unlike removal",
                "💡 Stake remains locked during deactivation",
                "💡 Use this for maintenance or temporary shutdown",
                "💡 Reactivate with appropriate command when ready",
            ],
        },
        "list": {
            "title": "📋 Listing Subnet Nodes",
            "description": "This operation shows all nodes in a subnet.",
            "requirements": ["• Valid subnet ID"],
            "process": [
                "1. Queries subnet node registry",
                "2. Retrieves node information",
                "3. Displays formatted node list",
                "4. Shows status and stake information",
            ],
            "tips": [
                "💡 Use --format json for programmatic access",
                "💡 Check node status to understand network health",
                "💡 Monitor stake amounts to see network participation",
            ],
        },
    }

    if operation in guidance_messages:
        msg = guidance_messages[operation]

        # Create comprehensive guidance panel
        content = f"[bold]{msg['description']}[/bold]\n\n"

        if "requirements" in msg:
            content += "[bold cyan]📋 Requirements:[/bold cyan]\n"
            for req in msg["requirements"]:
                content += f"{req}\n"
            content += "\n"

        if "process" in msg:
            content += "[bold green]⚙️ Process:[/bold green]\n"
            for step in msg["process"]:
                content += f"{step}\n"
            content += "\n"

        if "tips" in msg:
            content += "[bold yellow]💡 Tips & Warnings:[/bold yellow]\n"
            for tip in msg["tips"]:
                content += f"{tip}\n"

        # Add specific details if provided
        if details:
            content += "\n[bold magenta]📊 Current Operation:[/bold magenta]\n"
            for key, value in details.items():
                content += f"• {key}: {value}\n"

        panel = Panel(content, title=msg["title"], border_style="cyan", padding=(1, 2))

        console.print(panel)
        console.print()


@app.command()
def register(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID to register to"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey address (node identity)"),
    peer_id: str = typer.Option(..., "--peer-id", "-p", help="Peer ID for networking"),
    bootnode_peer_id: str = typer.Option(..., "--bootnode-peer-id", "-b", help="Bootstrap peer ID for bootnode"),
    client_peer_id: str = typer.Option(..., "--client-peer-id", "-c", help="Client peer ID for client-side operations"),
    stake_amount: int = typer.Option(
        ..., "--stake", "-st", help="Initial stake amount (in smallest units, minimum 100 TENSOR)"
    ),
    delegate_reward_rate: int = typer.Option(
        ..., "--reward-rate", "-r", help="Delegate reward rate (in smallest units)"
    ),
    bootnode: Optional[str] = typer.Option(
        None, "--bootnode", help="Bootnode multiaddress for DHT connection (optional)"
    ),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for registration)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Register a subnet node with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]🔗 Register Subnet Node Guide[/bold cyan]\n\n"
            f"This will register your node to subnet {subnet_id}:\n\n"
            f"[bold]What is Node Registration:[/bold]\n"
            f"• Registers your node to participate in subnet consensus\n"
            f"• Transfers stake as proof-of-stake requirement\n"
            f"• Node enters activation queue with start epoch\n"
            f"• Hotkey becomes network-unique identifier\n\n"
            f"[bold]Registration Parameters:[/bold]\n"
            f"• Subnet ID: {subnet_id}\n"
            f"• Hotkey: {hotkey}\n"
            f"• Peer ID: {peer_id}\n"
            f"• Bootnode Peer ID: {bootnode_peer_id}\n"
            f"• Client Peer ID: {client_peer_id}\n"
            f"• Stake Amount: {format_balance(stake_amount)}\n"
            f"• Reward Rate: {format_balance(delegate_reward_rate)}\n"
            f"• Bootnode: {bootnode or 'Not provided'}\n\n"
            f"[bold]Requirements:[/bold]\n"
            f"• Minimum 100 TENSOR stake (subnet may require more)\n"
            f"• Hotkey must be network-unique (never used before)\n"
            f"• Hotkey cannot match your coldkey\n"
            f"• Valid peer IDs for networking\n"
            f"• Sufficient balance for staking\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Hotkeys are network-unique for security\n"
            f"• Node enters queue after registration\n"
            f"• Start epoch assigned based on queue position\n"
            f"• Grace epochs allow flexible activation timing",
            title="[bold blue]🔗 Register Subnet Node[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Register node to subnet {subnet_id} with {format_balance(stake_amount)} stake?"):
            print_info("Node registration cancelled.")
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

    if not validate_peer_id(bootnode_peer_id):
        print_error("❌ Invalid bootnode peer ID format. Must be a valid MultiHash.")
        raise typer.Exit(1)

    if not validate_peer_id(client_peer_id):
        print_error("❌ Invalid client peer ID format. Must be a valid MultiHash.")
        raise typer.Exit(1)

    if not validate_amount(stake_amount):
        print_error("❌ Invalid stake amount. Must be positive.")
        raise typer.Exit(1)

    # Check minimum stake requirement (100 TENSOR = 100 * 10^18)
    min_stake = 100 * 10**18
    if stake_amount < min_stake:
        print_error(f"❌ Stake amount too low. Minimum required: {format_balance(min_stake)}")
        raise typer.Exit(1)

    if not validate_amount(delegate_reward_rate):
        print_error("❌ Invalid delegate reward rate. Must be positive.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for registration)
    if not key_name:
        print_error("❌ Key name is required for node registration. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        print_info(f"🔄 Registering node to subnet {subnet_id}...")

        # Load keypair for signing
        from ..utils.crypto import load_keypair
        # TODO: Get password from user or config
        password = "default_password_12345"  # This should be improved
        keypair = load_keypair(key_name, password)

        response = client.register_subnet_node(
            subnet_id=subnet_id,
            hotkey=hotkey,
            peer_id=peer_id,
            bootnode_peer_id=bootnode_peer_id,
            client_peer_id=client_peer_id,
            stake_amount=stake_amount,
            delegate_reward_rate=delegate_reward_rate,
            bootnode=bootnode,
            keypair=keypair
        )

        if response.success:
            print_success(f"✅ Node successfully registered to subnet {subnet_id}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]🎉 Node Registration Complete![/bold green]\n\n"
                f"Your node has been successfully registered to subnet {subnet_id}.\n"
                f"• Hotkey: {hotkey}\n"
                f"• Peer ID: {peer_id}\n"
                f"• Bootnode Peer ID: {bootnode_peer_id}\n"
                f"• Client Peer ID: {client_peer_id}\n"
                f"• Initial Stake: {format_balance(stake_amount)}\n"
                f"• Reward Rate: {format_balance(delegate_reward_rate)}\n"
                f"• Bootnode: {bootnode or 'Not provided'}\n\n"
                f"[yellow]⏳ Your node is now in the activation queue.[/yellow]\n"
                f"• Node has Registered classification\n"
                f"• Assigned start epoch for activation\n"
                f"• Grace epochs allow flexible activation\n"
                f"• Monitor status with: [bold]htcli node list --subnet-id {subnet_id}[/bold]\n\n"
                f"[yellow]📊 Next Steps:[/yellow]\n"
                f"• Wait for start epoch to activate\n"
                f"• Monitor queue position\n"
                f"• Prepare for validation duties",
                title="Registration Success",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to register node: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to register node to subnet: {str(e)}")
        raise typer.Exit(1)


@app.command()
def activate(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID to activate in"),
    node_id: int = typer.Option(..., "--node-id", "-n", help="Node ID to activate"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for activation)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Activate a registered subnet node with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]🚀 Activate Subnet Node Guide[/bold cyan]\n\n"
            f"This will activate node {node_id} in subnet {subnet_id}:\n\n"
            f"[bold]What is Node Activation:[/bold]\n"
            f"• Moves node from Registered to Active status\n"
            f"• Node enters Idle classification for idle epochs\n"
            f"• Node can participate in validation after activation\n"
            f"• Must be done within queue period + grace epochs\n\n"
            f"[bold]Activation Timeline:[/bold]\n"
            f"• Start Epoch: When node can first activate\n"
            f"• Grace Epochs: Flexible activation window\n"
            f"• Idle Epochs: Node stays in Idle classification\n"
            f"• Included: Automatic upgrade after idle epochs\n\n"
            f"[bold]Activation Requirements:[/bold]\n"
            f"• Node must be in Registered status\n"
            f"• Must be within activation timeframe\n"
            f"• Subnet must have available slots (or replacement policy)\n"
            f"• Valid signing key required\n\n"
            f"[bold]Full Subnet Handling:[/bold]\n"
            f"• If subnet slots are full:\n"
            f"  - Node can replace existing node\n"
            f"  - Or be pushed back into queue\n"
            f"• Must activate within allowed period\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Activation window is time-limited\n"
            f"• Missing activation requires re-registration\n"
            f"• Node enters Idle classification after activation\n"
            f"• Included classification requires 66%+ attestation ratio",
            title="[bold blue]🚀 Activate Subnet Node[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Activate node {node_id} in subnet {subnet_id}?"):
            print_info("Node activation cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_node_id(node_id):
        print_error("❌ Invalid node ID. Must be a positive integer.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for activation)
    if not key_name:
        print_error("❌ Key name is required for node activation. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        print_info(f"🔄 Activating node {node_id} in subnet {subnet_id}...")

        # Load keypair for signing
        from ..utils.crypto import load_keypair
        # TODO: Get password from user or config
        password = "default_password_12345"  # This should be improved
        keypair = load_keypair(key_name, password)

        response = client.activate_subnet_node(
            subnet_id=subnet_id,
            node_id=node_id,
            keypair=keypair
        )

        if response.success:
            print_success(f"✅ Node {node_id} successfully activated in subnet {subnet_id}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]🚀 Node Activation Complete![/bold green]\n\n"
                f"Node {node_id} has been successfully activated in subnet {subnet_id}.\n\n"
                f"[yellow]📊 Node Status Changes:[/yellow]\n"
                f"• Status: Registered → Active\n"
                f"• Classification: Idle (for idle epochs)\n"
                f"• Storage: Moved to SubnetNodesData\n"
                f"• Count: Added to TotalSubnetNodes\n\n"
                f"[yellow]⏳ Next Phases:[/yellow]\n"
                f"• Idle Classification: Node stays idle for idle epochs\n"
                f"• Included Classification: Automatic upgrade after idle epochs\n"
                f"• Attestation Requirement: 66%+ ratio for included status\n"
                f"• Validation: Node can participate in consensus\n\n"
                f"[yellow]📋 Monitor Progress:[/yellow]\n"
                f"• Check status: [bold]htcli node list --subnet-id {subnet_id}[/bold]\n"
                f"• Monitor classification changes\n"
                f"• Track attestation ratios",
                title="Activation Success",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to activate node: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to activate node: {str(e)}")
        raise typer.Exit(1)


@app.command()
def status(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(..., "--node-id", "-n", help="Node ID to check"),
    format_type: str = typer.Option(
        "table", "--format", "-f", help="Output format (table/json)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Show detailed node status and classification information."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]📊 Node Status & Classification Guide[/bold cyan]\n\n"
            f"This will show detailed status for node {node_id} in subnet {subnet_id}:\n\n"
            f"[bold]Node Classifications:[/bold]\n"
            f"• [yellow]Registered[/yellow]: Node is in registration queue\n"
            f"• [blue]Idle[/blue]: Node is active but not yet included\n"
            f"• [green]Included[/green]: Node participates in consensus\n"
            f"• [red]Validator[/red]: Node is a validator (highest level)\n\n"
            f"[bold]Status Information:[/bold]\n"
            f"• Current classification and epoch\n"
            f"• Activation eligibility and timing\n"
            f"• Stake amounts and reward rates\n"
            f"• Attestation ratios and penalties\n"
            f"• Network participation status\n\n"
            f"[bold]Timeline Tracking:[/bold]\n"
            f"• Registration epoch and queue position\n"
            f"• Start epoch for activation\n"
            f"• Grace period remaining\n"
            f"• Classification upgrade progress\n\n"
            f"[yellow]💡 Tip:[/yellow] Monitor this regularly to track your node's progress!",
            title="[bold blue]📊 Node Status Guide[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_node_id(node_id):
        print_error("❌ Invalid node ID. Must be a positive integer.")
        raise typer.Exit(1)

    try:
        print_info(f"📊 Checking status for node {node_id} in subnet {subnet_id}...")

        # Get node data
        response = client.get_subnet_node_status(subnet_id, node_id)

        if response.success:
            node_data = response.data.get("node", {})

            if format_type == "json":
                console.print_json(data=node_data)
            else:
                # Create detailed status panel
                from rich.panel import Panel
                from rich.table import Table

                # Determine classification color
                classification = node_data.get("classification", "Unknown")
                if classification == "Registered":
                    class_color = "yellow"
                elif classification == "Idle":
                    class_color = "blue"
                elif classification == "Included":
                    class_color = "green"
                elif classification == "Validator":
                    class_color = "red"
                else:
                    class_color = "white"

                # Create status panel
                status_panel = Panel(
                    f"[bold]Node ID:[/bold] {node_id}\n"
                    f"[bold]Subnet ID:[/bold] {subnet_id}\n"
                    f"[bold]Classification:[/bold] [{class_color}]{classification}[/{class_color}]\n"
                    f"[bold]Hotkey:[/bold] {node_data.get('hotkey', 'N/A')}\n"
                    f"[bold]Peer ID:[/bold] {node_data.get('peer_id', 'N/A')}\n"
                    f"[bold]Stake:[/bold] {format_balance(node_data.get('stake', 0))}\n"
                    f"[bold]Reward Rate:[/bold] {format_balance(node_data.get('delegate_reward_rate', 0))}\n"
                    f"[bold]Registration Epoch:[/bold] {node_data.get('registration_epoch', 'N/A')}\n"
                    f"[bold]Start Epoch:[/bold] {node_data.get('start_epoch', 'N/A')}\n"
                    f"[bold]Current Epoch:[/bold] {node_data.get('current_epoch', 'N/A')}\n"
                    f"[bold]Attestation Ratio:[/bold] {node_data.get('attestation_ratio', 'N/A')}%\n"
                    f"[bold]Penalties:[/bold] {node_data.get('penalties', 0)}",
                    title=f"[bold green]Node {node_id} Status[/bold green]",
                    border_style="green"
                )
                console.print(status_panel)
                console.print()

                # Create timeline table
                timeline_table = Table(title="[bold cyan]Node Timeline[/bold cyan]")
                timeline_table.add_column("Phase", style="cyan", no_wrap=True)
                timeline_table.add_column("Status", style="white")
                timeline_table.add_column("Epoch", style="yellow")
                timeline_table.add_column("Notes", style="dim")

                # Add timeline rows
                registration_epoch = node_data.get('registration_epoch', 'N/A')
                start_epoch = node_data.get('start_epoch', 'N/A')
                current_epoch = node_data.get('current_epoch', 'N/A')
                grace_epochs = node_data.get('grace_epochs', 'N/A')
                idle_epochs = node_data.get('idle_epochs', 'N/A')

                timeline_table.add_row("Registration", "✅ Complete", str(registration_epoch), "Node registered to subnet")
                timeline_table.add_row("Queue Period", "⏳ Active", f"{registration_epoch} → {start_epoch}", "Waiting for activation window")
                timeline_table.add_row("Activation Window", "🎯 Ready", f"{start_epoch} + {grace_epochs}", "Can activate now")
                timeline_table.add_row("Idle Classification", "🔄 Progress", f"{idle_epochs} epochs", "Building attestation ratio")
                timeline_table.add_row("Included Classification", "📈 Target", "Auto-upgrade", "Requires 66%+ attestation")

                console.print(timeline_table)
                console.print()

                # Create action recommendations
                classification = node_data.get("classification", "Unknown")
                if classification == "Registered":
                    action_panel = Panel(
                        f"[bold yellow]🎯 Next Action Required:[/bold yellow]\n\n"
                        f"Your node is registered and ready for activation!\n\n"
                        f"[bold]Activation Command:[/bold]\n"
                        f"htcli node activate --subnet-id {subnet_id} --node-id {node_id} --key-name <your-key>\n\n"
                        f"[yellow]⚠️ Important:[/yellow]\n"
                        f"• Activation window is time-limited\n"
                        f"• Must activate within grace period\n"
                        f"• Missing activation requires re-registration",
                        title="[bold yellow]🚀 Ready to Activate[/bold yellow]",
                        border_style="yellow"
                    )
                elif classification == "Idle":
                    action_panel = Panel(
                        f"[bold blue]🔄 Node is Active:[/bold blue]\n\n"
                        f"Your node is in Idle classification and building attestation ratio.\n\n"
                        f"[bold]Current Status:[/bold]\n"
                        f"• Active in subnet {subnet_id}\n"
                        f"• Building attestation ratio\n"
                        f"• Working towards Included classification\n\n"
                        f"[yellow]📊 Monitor Progress:[/yellow]\n"
                        f"• Check attestation ratio regularly\n"
                        f"• Ensure 66%+ ratio for Included upgrade\n"
                        f"• Monitor for penalties",
                        title="[bold blue]⏳ Building Attestation[/bold blue]",
                        border_style="blue"
                    )
                elif classification == "Included":
                    action_panel = Panel(
                        f"[bold green]✅ Node is Included:[/bold green]\n\n"
                        f"Your node is successfully included in consensus!\n\n"
                        f"[bold]Current Status:[/bold]\n"
                        f"• Participating in consensus\n"
                        f"• Earning rewards\n"
                        f"• Contributing to network security\n\n"
                        f"[yellow]🎉 Congratulations![/yellow]\n"
                        f"• Your node is fully operational\n"
                        f"• Continue monitoring performance\n"
                        f"• Maintain good attestation ratio",
                        title="[bold green]🎉 Fully Operational[/bold green]",
                        border_style="green"
                    )
                else:
                    action_panel = Panel(
                        f"[bold white]📊 Node Status: {classification}[/bold white]\n\n"
                        f"Your node is in {classification} classification.\n\n"
                        f"[yellow]💡 Monitor:[/yellow]\n"
                        f"• Check status regularly\n"
                        f"• Monitor for any issues\n"
                        f"• Follow subnet guidelines",
                        title="[bold white]📊 Status Monitor[/bold white]",
                        border_style="white"
                    )

                console.print(action_panel)

        else:
            print_error(f"❌ Failed to get node status: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to get node status: {str(e)}")
        raise typer.Exit(1)


@app.command()
def remove(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(..., "--node-id", "-n", help="Node ID to remove"),
    remove_stake: bool = typer.Option(
        False, "--remove-stake", "-rs", help="Automatically remove stake after node removal"
    ),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Remove a node from a subnet with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]🗑️ Remove Subnet Node Guide[/bold cyan]\n\n"
            f"This will remove node {node_id} from subnet {subnet_id}:\n\n"
            f"[bold]What is Node Removal:[/bold]\n"
            f"• Removes node from subnet participation\n"
            f"• Node stops validating and attesting\n"
            f"• Stake remains locked (must be removed separately)\n"
            f"• Cannot remove if node is current epoch validator\n\n"
            f"[bold]Removal Process:[/bold]\n"
            f"• Validates node is not current epoch validator\n"
            f"• Removes node from attestation data\n"
            f"• Clears peer ID and hotkey mappings\n"
            f"• Updates total node counts\n"
            f"• Resets node penalties\n\n"
            f"[bold]Stake Management:[/bold]\n"
            f"• [yellow]Node removal does NOT remove stake automatically[/yellow]\n"
            f"• Stake remains locked and must be removed separately\n"
            f"• Use --remove-stake flag for automatic stake removal\n"
            f"• Manual removal: htcli stake remove --subnet-id {subnet_id} --node-id {node_id}\n\n"
            f"[bold]Removal Requirements:[/bold]\n"
            f"• Node must not be current epoch validator\n"
            f"• Valid signing key required\n"
            f"• Node must be owned by your hotkey\n"
            f"• Any staked tokens will remain locked\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Removal is irreversible\n"
            f"• Stake must be removed separately\n"
            f"• Cannot remove during active validation\n"
            f"• Consider deactivation instead of removal",
            title="[bold blue]🗑️ Remove Subnet Node[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation with warning
        console.print(
            "[bold red]⚠️ WARNING: This action will remove your node and leave stake locked![/bold red]"
        )
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

    # Check if key_name is provided (required for removal)
    if not key_name:
        print_error("❌ Key name is required for node removal. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        print_info(f"🔄 Removing node {node_id} from subnet {subnet_id}...")

        # Load keypair for signing
        from ..utils.crypto import load_keypair
        # TODO: Get password from user or config
        password = "default_password_12345"  # This should be improved
        keypair = load_keypair(key_name, password)

        # Remove the node
        response = client.remove_subnet_node(
            subnet_id=subnet_id,
            node_id=node_id,
            keypair=keypair
        )

        if response.success:
            print_success(f"✅ Node {node_id} successfully removed from subnet {subnet_id}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            # Handle stake removal
            if remove_stake:
                print_info("🔄 Removing stake automatically...")

                # TODO: Implement automatic stake removal
                # For now, show what would happen
                console.print(Panel(
                    f"[bold yellow]🔄 Automatic Stake Removal[/bold yellow]\n\n"
                    f"This would automatically remove stake for node {node_id}:\n\n"
                    f"[bold]Stake Removal Process:[/bold]\n"
                    f"• Query current stake amount\n"
                    f"• Remove all stake from node\n"
                    f"• Process unbonding period\n"
                    f"• Return tokens to wallet\n\n"
                    f"[yellow]Note:[/yellow] Automatic stake removal is not yet implemented.\n"
                    f"Please remove stake manually using:\n"
                    f"[bold]htcli stake remove --subnet-id {subnet_id} --node-id {node_id} --key-name {key_name}[/bold]",
                    title="Stake Removal",
                    border_style="yellow"
                ))
            else:
                # Show manual stake removal instructions
                console.print(Panel(
                    f"[bold yellow]💰 Stake Still Locked[/bold yellow]\n\n"
                    f"Node {node_id} has been removed, but stake remains locked.\n\n"
                    f"[bold]To remove stake manually:[/bold]\n"
                    f"htcli stake remove --subnet-id {subnet_id} --node-id {node_id} --key-name {key_name}\n\n"
                    f"[bold]Stake Removal Process:[/bold]\n"
                    f"• Remove all staked tokens\n"
                    f"• Process unbonding period\n"
                    f"• Return tokens to your wallet\n\n"
                    f"[yellow]⚠️ Important:[/yellow]\n"
                    f"• Stake remains locked until manually removed\n"
                    f"• Unbonding period applies before tokens are available\n"
                    f"• Check stake status with: htcli stake info --subnet-id {subnet_id}",
                    title="Manual Stake Removal Required",
                    border_style="yellow"
                ))

            console.print(Panel(
                f"[bold green]🗑️ Node Removal Complete![/bold green]\n\n"
                f"Node {node_id} has been successfully removed from subnet {subnet_id}.\n\n"
                f"[yellow]📊 What Happened:[/yellow]\n"
                f"• Node removed from subnet participation\n"
                f"• Peer ID and hotkey mappings cleared\n"
                f"• Total node count updated\n"
                f"• Node penalties reset\n"
                f"• Attestation data removed\n\n"
                f"[yellow]📋 Next Steps:[/yellow]\n"
                f"• Remove stake: htcli stake remove --subnet-id {subnet_id} --node-id {node_id}\n"
                f"• Check balance: htcli chain balance --address <your-address>\n"
                f"• Monitor unbonding: htcli stake info --subnet-id {subnet_id}\n\n"
                f"[yellow]💡 Tip:[/yellow]\n"
                f"• Consider deactivation instead of removal for temporary shutdown\n"
                f"• Removal is irreversible - node must re-register to return",
                title="Removal Success",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to remove node: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to remove node: {str(e)}")
        raise typer.Exit(1)


@app.command()
def deactivate(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(..., "--node-id", "-n", help="Node ID to deactivate"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Deactivate a subnet node temporarily with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]⏸️ Deactivate Subnet Node Guide[/bold cyan]\n\n"
            f"This will temporarily deactivate node {node_id} in subnet {subnet_id}:\n\n"
            f"[bold]What is Node Deactivation:[/bold]\n"
            f"• Temporarily stops node participation\n"
            f"• Node becomes inactive but not removed\n"
            f"• Stake remains locked during deactivation\n"
            f"• Only Validator-classified nodes can deactivate\n"
            f"• Must last at least one epoch\n\n"
            f"[bold]Deactivation vs Removal:[/bold]\n"
            f"• [green]Deactivation[/green]: Temporary, reversible, stake locked\n"
            f"• [red]Removal[/red]: Permanent, irreversible, stake must be removed separately\n"
            f"• [yellow]Use deactivation for maintenance or temporary shutdown[/yellow]\n\n"
            f"[bold]Deactivation Process:[/bold]\n"
            f"• Validates node is Validator classification\n"
            f"• Moves node from active to deactivated storage\n"
            f"• Updates total node counts\n"
            f"• Stake remains locked and secure\n"
            f"• Node stops earning rewards\n\n"
            f"[bold]Stake During Deactivation:[/bold]\n"
            f"• [yellow]Stake remains locked[/yellow] - no automatic unbonding\n"
            f"• [yellow]No rewards earned[/yellow] - node not participating\n"
            f"• [yellow]Stake is secure[/yellow] - cannot be slashed while inactive\n"
            f"• [yellow]Can be reactivated[/yellow] - stake automatically available\n\n"
            f"[bold]Deactivation Requirements:[/bold]\n"
            f"• Node must be Validator classification\n"
            f"• Valid signing key required\n"
            f"• Must last at least one epoch\n"
            f"• Cannot exceed MaxDeactivationEpochs\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Deactivation is temporary and reversible\n"
            f"• Stake remains locked during deactivation\n"
            f"• Use for maintenance, not permanent removal\n"
            f"• Reactivate when ready to resume participation",
            title="[bold blue]⏸️ Deactivate Subnet Node[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Deactivate node {node_id} in subnet {subnet_id}?"):
            print_info("Node deactivation cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_node_id(node_id):
        print_error("❌ Invalid node ID. Must be a positive integer.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for deactivation)
    if not key_name:
        print_error("❌ Key name is required for node deactivation. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        print_info(f"🔄 Deactivating node {node_id} in subnet {subnet_id}...")

        # Load keypair for signing
        from ..utils.crypto import load_keypair
        # TODO: Get password from user or config
        password = "default_password_12345"  # This should be improved
        keypair = load_keypair(key_name, password)

        # Deactivate the node
        response = client.deactivate_subnet_node(
            subnet_id=subnet_id,
            node_id=node_id,
            keypair=keypair
        )

        if response.success:
            print_success(f"✅ Node {node_id} successfully deactivated in subnet {subnet_id}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]⏸️ Node Deactivation Complete![/bold green]\n\n"
                f"Node {node_id} has been successfully deactivated in subnet {subnet_id}.\n\n"
                f"[yellow]📊 What Happened:[/yellow]\n"
                f"• Node moved from active to deactivated storage\n"
                f"• Total node count updated\n"
                f"• Node stopped participating in consensus\n"
                f"• Stake remains locked and secure\n\n"
                f"[yellow]💰 Stake Status:[/yellow]\n"
                f"• [green]Stake remains locked[/green] - no automatic unbonding\n"
                f"• [yellow]No rewards earned[/yellow] - node not participating\n"
                f"• [green]Stake is secure[/green] - cannot be slashed while inactive\n"
                f"• [green]Ready for reactivation[/green] - stake automatically available\n\n"
                f"[yellow]⏳ Deactivation Period:[/yellow]\n"
                f"• Must last at least one epoch\n"
                f"• Cannot exceed MaxDeactivationEpochs\n"
                f"• Monitor deactivation status\n"
                f"• Reactivate when ready\n\n"
                f"[yellow]📋 Next Steps:[/yellow]\n"
                f"• Monitor status: htcli node status --subnet-id {subnet_id} --node-id {node_id}\n"
                f"• Reactivate when ready: htcli node reactivate --subnet-id {subnet_id} --node-id {node_id}\n"
                f"• Check stake status: htcli stake info --subnet-id {subnet_id}\n\n"
                f"[yellow]💡 Tip:[/yellow]\n"
                f"• Deactivation is temporary and reversible\n"
                f"• Use for maintenance or temporary shutdown\n"
                f"• Stake remains secure during deactivation\n"
                f"• Reactivate when ready to resume participation",
                title="Deactivation Success",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to deactivate node: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to deactivate node: {str(e)}")
        raise typer.Exit(1)


@app.command()
def reactivate(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(..., "--node-id", "-n", help="Node ID to reactivate"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Reactivate a subnet node with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]🚀 Reactivate Subnet Node Guide[/bold cyan]\n\n"
            f"This will reactivate node {node_id} in subnet {subnet_id}:\n\n"
            f"[bold]What is Node Reactivation:[/bold]\n"
            f"• Moves node from deactivated to active status\n"
            f"• Node becomes Validator classification immediately\n"
            f"• Begins consensus participation on following epoch\n"
            f"• Stake becomes available for earning rewards\n"
            f"• Must reactivate within MaxDeactivationEpochs\n\n"
            f"[bold]Reactivation Process:[/bold]\n"
            f"• Validates node is in deactivated storage\n"
            f"• Moves node to active storage (SubnetNodesData)\n"
            f"• Sets classification to Validator\n"
            f"• Sets start epoch to current epoch + 1\n"
            f"• Updates total node counts\n"
            f"• Stake becomes available for rewards\n\n"
            f"[bold]Time Limits:[/bold]\n"
            f"• Must reactivate within MaxDeactivationEpochs\n"
            f"• From deactivation epoch + 1\n"
            f"• After MaxDeactivationEpochs, must remove and re-register\n"
            f"• Cleanup functions available for expired nodes\n\n"
            f"[bold]Stake During Reactivation:[/bold]\n"
            f"• [green]Stake becomes available[/green] - can be used for staking\n"
            f"• [green]Rewards resume[/green] - node can earn rewards\n"
            f"• [green]Stake is secure[/green] - cannot be slashed while active\n"
            f"• [green]Ready for full operation[/green] - node is fully operational\n\n"
            f"[bold]Reactivation Requirements:[/bold]\n"
            f"• Node must be in deactivated status\n"
            f"• Valid signing key required\n"
            f"• Cannot exceed MaxDeactivationEpochs\n"
            f"• Must reactivate within time limit\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Reactivation has strict time limits\n"
            f"• After MaxDeactivationEpochs, must remove and re-register\n"
            f"• Node becomes Validator classification immediately\n"
            f"• Begins consensus participation on following epoch\n"
            f"• Cleanup functions available for expired nodes",
            title="[bold blue]🚀 Reactivate Subnet Node[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Reactivate node {node_id} in subnet {subnet_id}?"):
            print_info("Node reactivation cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_node_id(node_id):
        print_error("❌ Invalid node ID. Must be a positive integer.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for reactivation)
    if not key_name:
        print_error("❌ Key name is required for node reactivation. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        print_info(f"🔄 Reactivating node {node_id} in subnet {subnet_id}...")

        # Load keypair for signing
        from ..utils.crypto import load_keypair
        # TODO: Get password from user or config
        password = "default_password_12345"  # This should be improved
        keypair = load_keypair(key_name, password)

        # Reactivate the node
        response = client.reactivate_subnet_node(
            subnet_id=subnet_id,
            node_id=node_id,
            keypair=keypair
        )

        if response.success:
            print_success(f"✅ Node {node_id} successfully reactivated in subnet {subnet_id}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]🚀 Node Reactivation Complete![/bold green]\n\n"
                f"Node {node_id} has been successfully reactivated in subnet {subnet_id}.\n\n"
                f"[yellow]📊 What Happened:[/yellow]\n"
                f"• Node moved from deactivated to active storage\n"
                f"• Classification set to Validator\n"
                f"• Start epoch set to current epoch + 1\n"
                f"• Total node count updated\n"
                f"• Node will begin consensus on following epoch\n"
                f"• Stake became available for rewards\n\n"
                f"[yellow]💰 Stake Status:[/yellow]\n"
                f"• [green]Stake became available[/green] - can be used for staking\n"
                f"• [green]Rewards resume[/green] - node can earn rewards\n"
                f"• [green]Stake is secure[/green] - cannot be slashed while active\n"
                f"• [green]Ready for full operation[/green] - node is fully operational\n\n"
                f"[yellow]⏳ Consensus Participation:[/yellow]\n"
                f"• Node classification: Validator\n"
                f"• Start epoch: Current epoch + 1\n"
                f"• Consensus participation begins on following epoch\n"
                f"• Full validator duties resume\n\n"
                f"[yellow]📋 Next Steps:[/yellow]\n"
                f"• Monitor status: htcli node status --subnet-id {subnet_id} --node-id {node_id}\n"
                f"• Check consensus participation\n"
                f"• Monitor rewards: htcli stake info --subnet-id {subnet_id}\n"
                f"• Track validator performance\n\n"
                f"[yellow]💡 Tip:[/yellow]\n"
                f"• Node is now fully operational as a Validator\n"
                f"• Consensus participation begins on following epoch\n"
                f"• Monitor performance and rewards\n"
                f"• Keep node running for optimal performance",
                title="Reactivation Success",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to reactivate node: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to reactivate node: {str(e)}")
        raise typer.Exit(1)


@app.command()
def cleanup_expired(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(..., "--node-id", "-n", help="Node ID to cleanup"),
    cleanup_type: str = typer.Option(
        "deactivated", "--type", "-t", help="Cleanup type (deactivated/registered)"
    ),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (optional for cleanup)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Cleanup expired nodes that failed to activate or reactivate."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]🧹 Cleanup Expired Node Guide[/bold cyan]\n\n"
            f"This will cleanup expired node {node_id} in subnet {subnet_id}:\n\n"
            f"[bold]What is Node Cleanup:[/bold]\n"
            f"• Removes nodes that failed to activate/reactivate in time\n"
            f"• Anyone can call cleanup functions\n"
            f"• Frees up storage and resources\n"
            f"• Required for nodes that exceed time limits\n\n"
            f"[bold]Cleanup Types:[/bold]\n"
            f"• [yellow]deactivated[/yellow]: Nodes that failed to reactivate in time\n"
            f"• [yellow]registered[/yellow]: Nodes that failed to activate in time\n"
            f"• [yellow]Both types[/yellow]: Can be cleaned up by anyone\n\n"
            f"[bold]When Cleanup is Needed:[/bold]\n"
            f"• Deactivated nodes exceed MaxDeactivationEpochs\n"
            f"• Registered nodes exceed activation time limits\n"
            f"• Nodes that failed to meet requirements\n"
            f"• Storage cleanup and resource management\n\n"
            f"[bold]Cleanup Process:[/bold]\n"
            f"• Validates node is expired and eligible for cleanup\n"
            f"• Removes node from storage\n"
            f"• Frees up resources and storage\n"
            f"• Stake handling depends on node state\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Cleanup is irreversible\n"
            f"• Anyone can call cleanup functions\n"
            f"• Only affects expired/failed nodes\n"
            f"• Stake may need separate handling",
            title="[bold blue]🧹 Cleanup Expired Node[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Cleanup expired {cleanup_type} node {node_id} in subnet {subnet_id}?"):
            print_info("Node cleanup cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_node_id(node_id):
        print_error("❌ Invalid node ID. Must be a positive integer.")
        raise typer.Exit(1)

    if cleanup_type not in ["deactivated", "registered"]:
        print_error("❌ Invalid cleanup type. Must be 'deactivated' or 'registered'.")
        raise typer.Exit(1)

    try:
        print_info(f"🧹 Cleaning up expired {cleanup_type} node {node_id} in subnet {subnet_id}...")

        # Load keypair for signing if provided
        keypair = None
        if key_name:
            from ..utils.crypto import load_keypair
            # TODO: Get password from user or config
            password = "default_password_12345"  # This should be improved
            keypair = load_keypair(key_name, password)

        # Cleanup the expired node
        response = client.cleanup_expired_node(
            subnet_id=subnet_id,
            node_id=node_id,
            cleanup_type=cleanup_type,
            keypair=keypair
        )

        if response.success:
            print_success(f"✅ Successfully cleaned up expired {cleanup_type} node {node_id}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]🧹 Node Cleanup Complete![/bold green]\n\n"
                f"Expired {cleanup_type} node {node_id} has been cleaned up from subnet {subnet_id}.\n\n"
                f"[yellow]📊 What Happened:[/yellow]\n"
                f"• Node removed from {cleanup_type} storage\n"
                f"• Storage and resources freed\n"
                f"• Network cleanup completed\n"
                f"• Expired node data cleared\n\n"
                f"[yellow]💰 Stake Status:[/yellow]\n"
                f"• [yellow]Stake may need separate handling[/yellow]\n"
                f"• [yellow]Check stake status with: htcli stake info --subnet-id {subnet_id}[/yellow]\n"
                f"• [yellow]Remove stake if needed: htcli stake remove --subnet-id {subnet_id} --node-id {node_id}[/yellow]\n\n"
                f"[yellow]📋 Next Steps:[/yellow]\n"
                f"• Check stake status: htcli stake info --subnet-id {subnet_id}\n"
                f"• Remove stake if needed\n"
                f"• Consider re-registering if desired\n"
                f"• Monitor network health\n\n"
                f"[yellow]💡 Tip:[/yellow]\n"
                f"• Cleanup is irreversible\n"
                f"• Only affects expired/failed nodes\n"
                f"• Anyone can call cleanup functions\n"
                f"• Helps maintain network efficiency",
                title="Cleanup Success",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to cleanup node: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to cleanup node: {str(e)}")
        raise typer.Exit(1)


@app.command()
def update(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(..., "--node-id", "-n", help="Node ID to update"),
    delegate_reward_rate: int = typer.Option(
        ..., "--delegate-reward-rate", "-r", help="New delegate reward rate (in smallest units)"
    ),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Update subnet node delegate stake rate with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]🔄 Update Subnet Node Guide[/bold cyan]\n\n"
            f"This will update the delegate reward rate for node {node_id} in subnet {subnet_id}:\n\n"
            f"[bold]What is Delegate Stake Rate:[/bold]\n"
            f"• Percentage of node's incentives shared with delegators\n"
            f"• Determines how much delegators earn from node rewards\n"
            f"• Higher rate = more rewards for delegators\n"
            f"• Lower rate = more rewards for node operator\n"
            f"• Affects delegation attractiveness\n\n"
            f"[bold]Rate Update Rules:[/bold]\n"
            f"• [green]Increase[/green]: No limitations, can increase anytime\n"
            f"• [yellow]Decrease[/yellow]: Limited to 1% decrease per 24 hours\n"
            f"• [yellow]Gradual Changes[/yellow]: Large decreases must be done gradually\n"
            f"• [yellow]Strategic Planning[/yellow]: Plan rate changes carefully\n\n"
            f"[bold]Impact on Delegators:[/bold]\n"
            f"• [green]Rate Increase[/green]: More rewards for delegators\n"
            f"• [yellow]Rate Decrease[/yellow]: Fewer rewards for delegators\n"
            f"• [yellow]Delegation Decisions[/yellow]: Rate affects delegation choices\n"
            f"• [yellow]Competitive Positioning[/yellow]: Rate affects node attractiveness\n\n"
            f"[bold]Update Process:[/bold]\n"
            f"• Validates current delegate reward rate\n"
            f"• Checks rate change limitations\n"
            f"• Updates rate on blockchain\n"
            f"• Affects future reward distribution\n"
            f"• Requires valid signing key\n\n"
            f"[bold]Strategic Considerations:[/bold]\n"
            f"• [yellow]Competitive Rates[/yellow]: Balance operator and delegator interests\n"
            f"• [yellow]Market Conditions[/yellow]: Adjust based on network conditions\n"
            f"• [yellow]Delegation Growth[/yellow]: Higher rates attract more delegators\n"
            f"• [yellow]Revenue Optimization[/yellow]: Find optimal rate for your strategy\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Rate decreases are limited to 1% per 24 hours\n"
            f"• Plan large decreases carefully\n"
            f"• Rate changes affect delegation decisions\n"
            f"• Monitor delegation response to rate changes\n"
            f"• Balance operator and delegator interests",
            title="[bold blue]🔄 Update Subnet Node[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Update delegate reward rate for node {node_id} in subnet {subnet_id}?"):
            print_info("Node update cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_node_id(node_id):
        print_error("❌ Invalid node ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_delegate_reward_rate(delegate_reward_rate):
        print_error("❌ Invalid delegate reward rate. Must be a positive integer.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for update)
    if not key_name:
        print_error("❌ Key name is required for node update. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        print_info(f"🔄 Updating delegate reward rate for node {node_id} in subnet {subnet_id}...")

        # Load keypair for signing
        from ..utils.crypto import load_keypair
        # TODO: Get password from user or config
        password = "default_password_12345"  # This should be improved
        keypair = load_keypair(key_name, password)

        # Update the node's delegate reward rate
        response = client.update_node_delegate_reward_rate(
            subnet_id=subnet_id,
            node_id=node_id,
            new_delegate_reward_rate=delegate_reward_rate,
            keypair=keypair
        )

        if response.success:
            print_success(f"✅ Successfully updated delegate reward rate for node {node_id}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]🔄 Node Update Complete![/bold green]\n\n"
                f"Delegate reward rate for node {node_id} has been updated in subnet {subnet_id}.\n\n"
                f"[yellow]📊 What Happened:[/yellow]\n"
                f"• Delegate reward rate updated on blockchain\n"
                f"• New rate: {delegate_reward_rate} (in smallest units)\n"
                f"• Rate change affects future reward distribution\n"
                f"• Delegators will see updated rates\n"
                f"• Node attractiveness may change\n\n"
                f"[yellow]💰 Impact on Rewards:[/yellow]\n"
                f"• [green]Future rewards[/green] will use new rate\n"
                f"• [yellow]Existing delegations[/yellow] affected by new rate\n"
                f"• [yellow]Delegation decisions[/yellow] may change\n"
                f"• [yellow]Competitive positioning[/yellow] updated\n\n"
                f"[yellow]📈 Strategic Impact:[/yellow]\n"
                f"• [green]Higher rate[/green]: More attractive to delegators\n"
                f"• [yellow]Lower rate[/yellow]: More rewards for operator\n"
                f"• [yellow]Market positioning[/yellow]: Affects delegation choices\n"
                f"• [yellow]Revenue optimization[/yellow]: Balance operator/delegator interests\n\n"
                f"[yellow]📋 Next Steps:[/yellow]\n"
                f"• Monitor delegation response: htcli stake info --subnet-id {subnet_id}\n"
                f"• Check node status: htcli node status --subnet-id {subnet_id} --node-id {node_id}\n"
                f"• Track reward changes over time\n"
                f"• Consider further rate adjustments if needed\n\n"
                f"[yellow]💡 Tip:[/yellow]\n"
                f"• Monitor how delegators respond to rate changes\n"
                f"• Balance operator and delegator interests\n"
                f"• Consider market conditions when setting rates\n"
                f"• Plan rate decreases carefully (1% per 24 hours limit)",
                title="Update Success",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to update node: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to update node: {str(e)}")
        raise typer.Exit(1)


@app.command()
def list(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    format_type: str = typer.Option(
        "table", "--format", "-f", help="Output format (table/json)"
    ),
    show_guidance: bool = typer.Option(
        False, "--guidance", help="Show comprehensive guidance"
    ),
):
    """List all nodes in a subnet with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance if requested
    if show_guidance:
        show_comprehensive_guidance(
            "list", {"Subnet ID": subnet_id, "Output Format": format_type}
        )

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
                console.print(
                    Panel(
                        f"[bold yellow]📭 No nodes found in subnet {subnet_id}[/bold yellow]\n\n"
                        f"This subnet currently has no registered nodes.\n"
                        f"Add a node with: [bold]htcli node add --subnet-id {subnet_id}[/bold]",
                        title="Empty Subnet",
                        border_style="yellow",
                    )
                )
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
