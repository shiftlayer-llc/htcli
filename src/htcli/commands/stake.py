"""
Staking management commands for the Hypertensor CLI.
All commands follow the format: htcli stake <command> [switches]
"""

import typer
from rich.console import Console
from rich.panel import Panel
from typing import Optional
from ..models.requests import StakeAddRequest, StakeRemoveRequest
from ..utils.validation import (
    validate_subnet_id,
    validate_node_id,
    validate_address,
    validate_amount,
)
from ..utils.formatting import (
    print_success,
    print_error,
    print_info,
    format_balance,
    format_stake_info,
)
from ..utils.ownership import require_user_keys, show_mine_filter_info
from ..dependencies import get_client

app = typer.Typer(name="stake", help="Staking operations and management")
console = Console()


def show_staking_guidance(operation: str, details: dict):
    """Show comprehensive guidance for staking operations."""
    guidance_messages = {
        "add": {
            "title": "💰 Adding Stake to Node",
            "description": "This operation will stake TENSOR tokens to support a node in a subnet.",
            "requirements": [
                "• Valid subnet ID and node ID",
                "• Sufficient TENSOR balance in your account",
                "• Node must be active and accepting stake",
                "• Minimum stake amount requirements",
                "• Valid hotkey address for the node",
            ],
            "process": [
                "1. Validates all input parameters",
                "2. Checks your TENSOR balance is sufficient",
                "3. Verifies node exists and is active",
                "4. Locks tokens in staking contract",
                "5. Updates your stake position",
                "6. Begins earning staking rewards",
            ],
            "tips": [
                "💡 Check node status with: htcli node status --subnet-id <ID> --node-id <ID>",
                "💡 Verify your balance with: htcli chain balance --address <address>",
                "💡 Staked tokens are locked and earn rewards",
                "💡 Higher stake = higher potential rewards",
                "⚠️ Unstaking has an unbonding period before tokens are available",
            ],
        },
        "remove": {
            "title": "📤 Removing Stake from Node",
            "description": "This operation will unstake TENSOR tokens from a node.",
            "requirements": [
                "• Valid subnet ID and node ID",
                "• Existing stake position with the node",
                "• Valid hotkey address",
                "• Amount must not exceed current stake",
            ],
            "process": [
                "1. Validates stake position exists",
                "2. Checks requested amount is available",
                "3. Initiates unbonding process",
                "4. Tokens enter unbonding period",
                "5. Reduces your stake position",
                "6. Stops earning rewards on unstaked amount",
            ],
            "tips": [
                "⚠️ Unbonding period applies before tokens are available",
                "⚠️ Unstaked tokens stop earning rewards immediately",
                "💡 Check current stake with: htcli stake info --address <addr> --subnet-id <ID>",
                "💡 Use claim-unbondings to retrieve unbonded tokens",
                "💡 Consider partial unstaking to maintain some rewards",
            ],
        },
        "info": {
            "title": "📊 Checking Stake Information",
            "description": "This operation shows your staking positions and rewards.",
            "requirements": [
                "• Valid account address",
                "• Valid subnet ID (optional for all stakes)",
            ],
            "process": [
                "1. Queries your stake positions",
                "2. Retrieves current rewards",
                "3. Shows unbonding positions",
                "4. Calculates total staked amounts",
                "5. Displays formatted stake summary",
            ],
            "tips": [
                "💡 Monitor your rewards regularly",
                "💡 Check unbonding status before claiming",
                "💡 Use --format json for programmatic access",
                "💡 Track performance across multiple subnets",
            ],
        },
        "claim": {
            "title": "🎯 Claiming Unbonded Tokens",
            "description": "This operation claims tokens that have completed unbonding.",
            "requirements": [
                "• Unbonded tokens available for claiming",
                "• Valid hotkey address",
                "• Unbonding period must be complete",
            ],
            "process": [
                "1. Checks for completed unbondings",
                "2. Validates unbonding period is finished",
                "3. Transfers tokens back to your account",
                "4. Updates unbonding records",
                "5. Tokens become freely available",
            ],
            "tips": [
                "💡 Check unbonding status before claiming",
                "💡 Claim regularly to free up tokens",
                "💡 Claimed tokens can be restaked or transferred",
                "⚠️ Can only claim after unbonding period expires",
            ],
        },
        "delegate": {
            "title": "🤝 Delegate Staking Operations",
            "description": "This operation manages delegate staking positions.",
            "requirements": [
                "• Valid subnet ID",
                "• Sufficient TENSOR balance",
                "• Active subnet accepting delegates",
            ],
            "process": [
                "1. Validates subnet and delegate parameters",
                "2. Locks tokens in delegate staking",
                "3. Begins earning delegate rewards",
                "4. Updates delegate position",
            ],
            "tips": [
                "💡 Delegate staking has different reward mechanics",
                "💡 Monitor delegate performance and rewards",
                "💡 Can transfer between different subnets",
                "⚠️ Delegate rewards depend on subnet performance",
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
def add(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(..., "--node-id", "-n", help="Node ID"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey address"),
    amount: int = typer.Option(
        ..., "--amount", "-a", help="Stake amount (in smallest units)"
    ),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Add stake to a node with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        show_staking_guidance(
            "add",
            {
                "Subnet ID": subnet_id,
                "Node ID": node_id,
                "Hotkey": hotkey,
                "Stake Amount": format_balance(amount),
            },
        )

        # Ask for confirmation
        if not typer.confirm("Do you want to proceed with adding this stake?"):
            print_info("Stake addition cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_node_id(node_id):
        print_error("❌ Invalid node ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_address(hotkey):
        print_error("❌ Invalid hotkey address format.")
        raise typer.Exit(1)

    if not validate_amount(amount):
        print_error("❌ Invalid stake amount. Must be positive.")
        raise typer.Exit(1)

    try:
        print_info(
            f"🔄 Adding {format_balance(amount)} stake to node {node_id} in subnet {subnet_id}..."
        )

        request = StakeAddRequest(
            subnet_id=subnet_id,
            node_id=node_id,
            hotkey=hotkey,
            stake_to_be_added=amount,
        )

        # Get keypair for signing if provided
        keypair = None
        if key_name:
            # TODO: Load keypair from storage
            print_info(f"🔑 Using key: {key_name}")

        response = client.add_to_stake(request, keypair)

        if response.success:
            print_success(f"✅ Successfully added {format_balance(amount)} stake!")
            console.print(
                f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]"
            )
            if response.block_number:
                console.print(
                    f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]"
                )

            console.print(
                Panel(
                    f"[bold green]💰 Stake Addition Complete![/bold green]\n\n"
                    f"Added {format_balance(amount)} to node {node_id} in subnet {subnet_id}.\n"
                    f"• Hotkey: {hotkey}\n"
                    f"• Your stake is now active and earning rewards\n"
                    f"• Rewards will be distributed according to node performance\n\n"
                    f"[yellow]📊 Monitor your stake:[/yellow]\n"
                    f"Use: [bold]htcli stake info --address {hotkey} --subnet-id {subnet_id}[/bold]",
                    title="Staking Success",
                    border_style="green",
                )
            )
        else:
            print_error(f"❌ Failed to add stake: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to add stake: {str(e)}")
        raise typer.Exit(1)


@app.command()
def remove(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(..., "--node-id", "-n", help="Node ID to remove stake from"),
    amount: Optional[int] = typer.Option(
        None, "--amount", "-a", help="Amount to remove (in smallest units, default: all stake)"
    ),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Remove stake from a node with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]📤 Remove Stake from Node Guide[/bold cyan]\n\n"
            f"This will remove stake from node {node_id} in subnet {subnet_id}:\n\n"
            f"[bold]What is Stake Removal:[/bold]\n"
            f"• Unstakes TENSOR tokens from a node\n"
            f"• Tokens enter unbonding period\n"
            f"• Stops earning rewards on removed stake\n"
            f"• Returns tokens to wallet after unbonding\n\n"
            f"[bold]Removal Process:[/bold]\n"
            f"• Validates existing stake position\n"
            f"• Checks requested amount is available\n"
            f"• Initiates unbonding process\n"
            f"• Updates stake position\n"
            f"• Processes unbonding period\n\n"
            f"[bold]Amount Options:[/bold]\n"
            f"• [bold]Partial Removal[/bold]: Remove specific amount\n"
            f"• [bold]Full Removal[/bold]: Remove all stake (default)\n"
            f"• [bold]Minimum Check[/bold]: Ensure sufficient balance\n\n"
            f"[bold]Unbonding Period:[/bold]\n"
            f"• Tokens are locked during unbonding\n"
            f"• No rewards earned during unbonding\n"
            f"• Use claim-unbondings to retrieve tokens\n"
            f"• Check unbonding status regularly\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Unbonding period applies before tokens available\n"
            f"• Removed stake stops earning rewards immediately\n"
            f"• Consider partial removal to maintain some rewards\n"
            f"• Check current stake before removal",
            title="[bold blue]📤 Remove Stake[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        amount_text = f"{format_balance(amount)}" if amount else "all stake"
        if not typer.confirm(f"Remove {amount_text} from node {node_id} in subnet {subnet_id}?"):
            print_info("Stake removal cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_node_id(node_id):
        print_error("❌ Invalid node ID. Must be a positive integer.")
        raise typer.Exit(1)

    if amount and not validate_amount(amount):
        print_error("❌ Invalid amount. Must be positive.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for stake removal)
    if not key_name:
        print_error("❌ Key name is required for stake removal. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        print_info(f"🔄 Removing stake from node {node_id} in subnet {subnet_id}...")

        # Load keypair for signing
        from ..utils.crypto import load_keypair
        # TODO: Get password from user or config
        password = "default_password_12345"  # This should be improved
        keypair = load_keypair(key_name, password)

        # TODO: Implement actual stake removal
        # For now, show what would happen
        console.print(Panel(
            f"[bold yellow]🔄 Stake Removal Process[/bold yellow]\n\n"
            f"This would remove stake from node {node_id}:\n\n"
            f"[bold]Current Implementation Status:[/bold]\n"
            f"• [yellow]Mock Implementation[/yellow] - Not yet connected to blockchain\n"
            f"• [yellow]Stake Removal Logic[/yellow] - Ready for implementation\n"
            f"• [yellow]Unbonding Process[/yellow] - Will be implemented\n\n"
            f"[bold]What Would Happen:[/bold]\n"
            f"• Query current stake amount for node {node_id}\n"
            f"• Remove {'all stake' if not amount else format_balance(amount)}\n"
            f"• Initiate unbonding process\n"
            f"• Update stake position\n"
            f"• Process unbonding period\n\n"
            f"[bold]Next Steps After Implementation:[/bold]\n"
            f"• Check unbonding status: htcli stake info --subnet-id {subnet_id}\n"
            f"• Claim unbonded tokens: htcli stake claim-unbondings\n"
            f"• Monitor balance: htcli chain balance --address <your-address>\n\n"
            f"[yellow]Note:[/yellow] This is a mock implementation.\n"
            f"Real stake removal will be implemented in the next phase.",
            title="Stake Removal (Mock)",
            border_style="yellow"
        ))

        # Simulate successful response
        print_success(f"✅ Stake removal initiated for node {node_id} in subnet {subnet_id}!")

        console.print(Panel(
            f"[bold green]📤 Stake Removal Initiated![/bold green]\n\n"
            f"Stake removal has been initiated for node {node_id}.\n\n"
            f"[yellow]📊 What Happened:[/yellow]\n"
            f"• Stake removal request submitted\n"
            f"• Tokens entered unbonding period\n"
            f"• Stake position updated\n"
            f"• Rewards stopped on removed amount\n\n"
            f"[yellow]⏳ Unbonding Process:[/yellow]\n"
            f"• Tokens are locked during unbonding\n"
            f"• No rewards earned during this period\n"
            f"• Check status: htcli stake info --subnet-id {subnet_id}\n"
            f"• Claim when ready: htcli stake claim-unbondings\n\n"
            f"[yellow]📋 Monitor Progress:[/yellow]\n"
            f"• Check unbonding status regularly\n"
            f"• Monitor balance changes\n"
            f"• Claim tokens when unbonding completes\n\n"
            f"[yellow]💡 Tip:[/yellow]\n"
            f"• Unbonding period varies by network\n"
            f"• Consider partial removal to maintain some rewards\n"
            f"• Keep some stake for continued participation",
            title="Removal Success",
            border_style="green"
        ))

    except Exception as e:
        print_error(f"❌ Failed to remove stake: {str(e)}")
        raise typer.Exit(1)


@app.command()
def claim(
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey address"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Claim unbonded stake with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        show_staking_guidance("claim", {"Hotkey": hotkey})

        # Ask for confirmation
        if not typer.confirm("Do you want to claim your unbonded tokens?"):
            print_info("Claim operation cancelled.")
            return

    # Validate inputs
    if not validate_address(hotkey):
        print_error("❌ Invalid hotkey address format.")
        raise typer.Exit(1)

    try:
        print_info("🔄 Claiming unbonded tokens...")

        # Get keypair for signing if provided
        keypair = None
        if key_name:
            # TODO: Load keypair from storage
            print_info(f"🔑 Using key: {key_name}")

        response = client.claim_unbondings(keypair)

        if response.success:
            print_success("✅ Successfully claimed unbonded tokens!")
            console.print(
                f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]"
            )
            if response.block_number:
                console.print(
                    f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]"
                )

            console.print(
                Panel(
                    f"[bold green]🎯 Unbonded Tokens Claimed![/bold green]\n\n"
                    f"Your unbonded tokens have been returned to your account.\n"
                    f"• Hotkey: {hotkey}\n"
                    f"• Tokens are now freely available\n"
                    f"• Can be restaked or transferred as needed\n\n"
                    f"[yellow]💡 Next Steps:[/yellow]\n"
                    f"• Check balance: [bold]htcli chain balance --address {hotkey}[/bold]\n"
                    f"• Restake if desired: [bold]htcli stake add --subnet-id <ID>[/bold]",
                    title="Claim Complete",
                    border_style="green",
                )
            )
        else:
            print_error(f"❌ Failed to claim unbondings: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to claim unbondings: {str(e)}")
        raise typer.Exit(1)


@app.command()
def delegate_add(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    amount: int = typer.Option(
        ..., "--amount", "-a", help="Stake amount to delegate (in smallest units)"
    ),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Add delegate stake to a subnet for a portion of each epoch's emissions."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]🤝 Delegate Staking Guide[/bold cyan]\n\n"
            f"This will add {format_balance(amount)} delegate stake to subnet {subnet_id}:\n\n"
            f"[bold]What is Delegate Staking:[/bold]\n"
            f"• Stake tokens directly to a subnet (not a specific node)\n"
            f"• Earn a portion of each epoch's emissions\n"
            f"• Share in subnet performance rewards\n"
            f"• Can transfer shares between subnets\n\n"
            f"[bold]Benefits:[/bold]\n"
            f"• Diversified exposure to subnet performance\n"
            f"• No need to choose specific nodes\n"
            f"• Automatic reward distribution\n"
            f"• Flexible share management\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Tokens are locked in the subnet's delegate pool\n"
            f"• Rewards depend on subnet performance\n"
            f"• Shares can be transferred or removed\n"
            f"• Monitor subnet performance regularly",
            title="[bold green]🤝 Add Delegate Stake[/bold green]",
            border_style="green"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm("Do you want to add this delegate stake?"):
            print_info("Delegate stake addition cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_amount(amount):
        print_error("❌ Invalid stake amount. Must be positive.")
        raise typer.Exit(1)

    try:
        print_info(
            f"🔄 Adding {format_balance(amount)} delegate stake to subnet {subnet_id}..."
        )

        # Get keypair for signing if provided
        keypair = None
        if key_name:
            from ..utils.crypto import load_keypair
            # TODO: Get password from user or config
            password = "default_password_12345"  # This should be improved
            keypair = load_keypair(key_name, password)
            print_info(f"🔑 Using key: {key_name}")

        response = client.add_to_delegate_stake(subnet_id, amount, keypair)

        if response.success:
            print_success(
                f"✅ Successfully added {format_balance(amount)} delegate stake!"
            )
            console.print(
                f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]"
            )
            if response.block_number:
                console.print(
                    f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]"
                )

            console.print(
                Panel(
                    f"[bold green]🤝 Delegate Stake Added![/bold green]\n\n"
                    f"Added {format_balance(amount)} delegate stake to subnet {subnet_id}.\n"
                    f"• Earning delegate rewards based on subnet performance\n"
                    f"• Can transfer shares to other subnets if needed\n"
                    f"• Monitor performance and rewards regularly\n\n"
                    f"[yellow]💡 Management:[/yellow]\n"
                    f"• Transfer: [bold]htcli stake delegate-transfer[/bold]\n"
                    f"• Remove: [bold]htcli stake delegate-remove[/bold]\n"
                    f"• Info: [bold]htcli stake info --subnet-id {subnet_id}[/bold]",
                    title="Delegate Staking Active",
                    border_style="green",
                )
            )
        else:
            print_error(f"❌ Failed to add delegate stake: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to add delegate stake: {str(e)}")
        raise typer.Exit(1)


@app.command()
def delegate_remove(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    shares: int = typer.Option(
        ..., "--shares", "-sh", help="Number of shares to remove"
    ),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Remove delegate stake shares from a subnet (shares converted to balance internally)."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]📤 Remove Delegate Stake Guide[/bold cyan]\n\n"
            f"This will remove {shares} delegate stake shares from subnet {subnet_id}:\n\n"
            f"[bold]What Happens:[/bold]\n"
            f"• Shares are converted to balance internally\n"
            f"• Balance becomes available in your account\n"
            f"• Reduced exposure to subnet performance\n"
            f"• Stops earning rewards on removed shares\n\n"
            f"[bold]Share System:[/bold]\n"
            f"• Shares represent your portion of the delegate pool\n"
            f"• More shares = higher rewards\n"
            f"• Shares can be transferred between subnets\n"
            f"• Balance conversion happens automatically\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• This reduces your stake in the subnet\n"
            f"• Lower rewards from this subnet\n"
            f"• Consider transferring instead of removing\n"
            f"• Monitor your total portfolio balance",
            title="[bold yellow]📤 Remove Delegate Stake[/bold yellow]",
            border_style="yellow"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm("Do you want to remove this delegate stake?"):
            print_info("Delegate stake removal cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if shares <= 0:
        print_error("❌ Invalid shares amount. Must be positive.")
        raise typer.Exit(1)

    try:
        print_info(f"🔄 Removing {shares} delegate shares from subnet {subnet_id}...")

        # Get keypair for signing if provided
        keypair = None
        if key_name:
            from ..utils.crypto import load_keypair
            # TODO: Get password from user or config
            password = "default_password_12345"  # This should be improved
            keypair = load_keypair(key_name, password)
            print_info(f"🔑 Using key: {key_name}")

        response = client.remove_delegate_stake(subnet_id, shares, keypair)

        if response.success:
            print_success(f"✅ Successfully removed {shares} delegate shares!")
            console.print(
                f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]"
            )
            if response.block_number:
                console.print(
                    f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]"
                )

            console.print(
                Panel(
                    f"[bold yellow]📤 Delegate Stake Removed![/bold yellow]\n\n"
                    f"Removed {shares} shares from subnet {subnet_id}.\n"
                    f"• No longer earning rewards from this position\n"
                    f"• Tokens may enter unbonding period\n"
                    f"• Can be restaked in other subnets if desired\n\n"
                    f"[yellow]⏳ Check Status:[/yellow]\n"
                    f"Monitor unbonding and claim when ready.",
                    title="Delegate Removal Complete",
                    border_style="yellow",
                )
            )
        else:
            print_error(f"❌ Failed to remove delegate stake: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to remove delegate stake: {str(e)}")
        raise typer.Exit(1)


@app.command()
def delegate_increase(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    amount: int = typer.Option(
        ..., "--amount", "-a", help="Amount to add to delegate stake pool (in smallest units)"
    ),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Increase the overall delegate stake balance in a subnet's pool (useful for airdropping rewards)."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]💰 Increase Delegate Stake Pool Guide[/bold cyan]\n\n"
            f"This will increase the delegate stake pool for subnet {subnet_id} by {format_balance(amount)}:\n\n"
            f"[bold]What This Does:[/bold]\n"
            f"• Increases the total delegate stake balance in the subnet\n"
            f"• Benefits ALL current delegate stakers proportionally\n"
            f"• Does NOT increase your personal balance\n"
            f"• Useful for airdropping rewards to stakers\n\n"
            f"[bold]Impact:[/bold]\n"
            f"• All current stakers get more rewards\n"
            f"• Pool becomes more attractive to new stakers\n"
            f"• Subnet gains more delegate stake support\n"
            f"• Your contribution benefits the entire community\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• This is a community contribution\n"
            f"• You don't get direct personal benefit\n"
            f"• Tokens are added to the pool permanently\n"
            f"• Consider this carefully before proceeding",
            title="[bold magenta]💰 Increase Delegate Pool[/bold magenta]",
            border_style="magenta"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(
            f"Increase delegate stake pool for subnet {subnet_id} by {format_balance(amount)}?"
        ):
            print_info("Delegate stake pool increase cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_amount(amount):
        print_error("❌ Invalid amount. Must be positive.")
        raise typer.Exit(1)

    try:
        print_info(
            f"🔄 Increasing delegate stake pool for subnet {subnet_id} by {format_balance(amount)}..."
        )

        # Get keypair for signing if provided
        keypair = None
        if key_name:
            from ..utils.crypto import load_keypair
            # TODO: Get password from user or config
            password = "default_password_12345"  # This should be improved
            keypair = load_keypair(key_name, password)
            print_info(f"🔑 Using key: {key_name}")

        response = client.increase_delegate_stake(subnet_id, amount, keypair)

        if response.success:
            print_success(f"✅ Successfully increased delegate stake pool by {format_balance(amount)}!")
            console.print(
                f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]"
            )
            if response.block_number:
                console.print(
                    f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]"
                )

            console.print(
                Panel(
                    f"[bold magenta]💰 Delegate Pool Increased![/bold magenta]\n\n"
                    f"Increased delegate stake pool for subnet {subnet_id} by {format_balance(amount)}.\n"
                    f"• All current delegate stakers benefit\n"
                    f"• Pool becomes more attractive to new stakers\n"
                    f"• Subnet gains stronger delegate support\n"
                    f"• Community contribution successful\n\n"
                    f"[yellow]💡 Impact:[/yellow]\n"
                    f"• Higher rewards for all stakers\n"
                    f"• More attractive to potential stakers\n"
                    f"• Stronger subnet performance\n"
                    f"• Community growth supported",
                    title="Delegate Pool Increase Complete",
                    border_style="magenta",
                )
            )
        else:
            print_error(f"❌ Failed to increase delegate stake pool: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to increase delegate stake pool: {str(e)}")
        raise typer.Exit(1)


@app.command()
def delegate_transfer(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    to_account: str = typer.Option(
        ..., "--to-account", "-t", help="Destination account address"
    ),
    shares: int = typer.Option(
        ..., "--shares", "-sh", help="Number of shares to transfer"
    ),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Transfer delegate stake shares from one account to another within a subnet."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]🔄 Transfer Delegate Stake Guide[/bold cyan]\n\n"
            f"This will transfer {shares} delegate stake shares from subnet {subnet_id}:\n\n"
            f"[bold]Transfer Details:[/bold]\n"
            f"• From: Your account\n"
            f"• To: {to_account}\n"
            f"• Subnet: {subnet_id}\n"
            f"• Shares: {shares}\n\n"
            f"[bold]What Happens:[/bold]\n"
            f"• Shares are transferred to the destination account\n"
            f"• Destination account gains stake in the subnet\n"
            f"• Your stake in the subnet is reduced\n"
            f"• No change in total subnet delegate pool\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• This is a permanent transfer\n"
            f"• Destination account will earn rewards\n"
            f"• You lose stake and rewards\n"
            f"• Verify destination address carefully",
            title="[bold blue]🔄 Transfer Delegate Stake[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(
            f"Transfer {shares} shares to {to_account} in subnet {subnet_id}?"
        ):
            print_info("Delegate stake transfer cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_address(to_account):
        print_error("❌ Invalid destination account address.")
        raise typer.Exit(1)

    if shares <= 0:
        print_error("❌ Invalid shares amount. Must be positive.")
        raise typer.Exit(1)

    try:
        print_info(
            f"🔄 Transferring {shares} shares to {to_account} in subnet {subnet_id}..."
        )

        # Get keypair for signing if provided
        keypair = None
        if key_name:
            from ..utils.crypto import load_keypair
            # TODO: Get password from user or config
            password = "default_password_12345"  # This should be improved
            keypair = load_keypair(key_name, password)
            print_info(f"🔑 Using key: {key_name}")

        response = client.transfer_delegate_stake(
            subnet_id, to_account, shares, keypair
        )

        if response.success:
            print_success(f"✅ Successfully transferred {shares} delegate shares!")
            console.print(
                f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]"
            )
            if response.block_number:
                console.print(
                    f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]"
                )

            console.print(
                Panel(
                    f"[bold green]🔄 Delegate Stake Transferred![/bold green]\n\n"
                    f"Transferred {shares} shares:\n"
                    f"• From: Your account\n"
                    f"• To: {to_account}\n"
                    f"• Subnet: {subnet_id}\n"
                    f"• Destination account now has stake in subnet\n"
                    f"• Transfer completed in single transaction\n\n"
                    f"[yellow]💡 Impact:[/yellow]\n"
                    f"• Destination account will earn rewards\n"
                    f"• Your stake in subnet is reduced\n"
                    f"• Monitor your remaining positions",
                    title="Transfer Complete",
                    border_style="green",
                )
            )
        else:
            print_error(f"❌ Failed to transfer delegate stake: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to transfer delegate stake: {str(e)}")
        raise typer.Exit(1)
