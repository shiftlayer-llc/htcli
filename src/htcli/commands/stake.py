"""
Staking management commands for the Hypertensor CLI.
All commands follow the format: htcli stake <command> [switches]
"""

import typer
from rich.console import Console
from rich.panel import Panel
from typing import Optional

from ..utils.password import get_secure_password
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
            # Load keypair for signing
            from ..utils.crypto import load_keypair

            # Get secure password for keypair
            password = get_secure_password(
                key_name,
                prompt_message="Enter password to unlock keypair",
                allow_default=True,
            )
            keypair = load_keypair(key_name, password)
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
    node_id: int = typer.Option(
        ..., "--node-id", "-n", help="Node ID to remove stake from"
    ),
    amount: Optional[int] = typer.Option(
        None,
        "--amount",
        "-a",
        help="Amount to remove (in smallest units, default: all stake)",
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
            border_style="blue",
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        amount_text = f"{format_balance(amount)}" if amount else "all stake"
        if not typer.confirm(
            f"Remove {amount_text} from node {node_id} in subnet {subnet_id}?"
        ):
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
        print_error(
            "❌ Key name is required for stake removal. Use --key-name to specify your signing key."
        )
        raise typer.Exit(1)

    try:
        print_info(f"🔄 Removing stake from node {node_id} in subnet {subnet_id}...")

        # Load keypair for signing
        from ..utils.crypto import load_keypair

        # Get secure password for keypair

        password = get_secure_password(
            key_name,
            prompt_message="Enter password to unlock keypair",
            allow_default=True,
        )
        keypair = load_keypair(key_name, password)

        # Implement actual stake removal
        stake_removal_response = client.remove_node_stake_automatically(
            subnet_id=subnet_id, node_id=node_id, key_name=key_name
        )

        if stake_removal_response.success:
            stake_data = stake_removal_response.data
            removed_amount = stake_data.get("removed_amount", 0)
            shares_removed = stake_data.get("shares_removed", 0)

            print_success(f"✅ Stake removal completed successfully!")
            console.print(
                f"📄 Transaction Hash: [bold cyan]{stake_removal_response.transaction_hash}[/bold cyan]"
            )
            if stake_removal_response.block_number:
                console.print(
                    f"📦 Block Number: [bold cyan]#{stake_removal_response.block_number}[/bold cyan]"
                )

            console.print(
                Panel(
                    f"[bold green]🔄 Stake Removal Success![/bold green]\n\n"
                    f"Successfully removed stake from node {node_id}:\n\n"
                    f"[yellow]📊 Removal Details:[/yellow]\n"
                    f"• [green]Shares Removed[/green]: {shares_removed:,}\n"
                    f"• [green]Estimated Value[/green]: {format_balance(removed_amount)} TENSOR\n"
                    f"• [green]Unbonding Started[/green]: Yes\n\n"
                    f"[yellow]⏳ Next Steps:[/yellow]\n"
                    f"• Wait for unbonding period to complete\n"
                    f"• Monitor unbonding status\n"
                    f"• Claim tokens when ready\n\n"
                    f"[yellow]💡 Tip:[/yellow]\n"
                    f"• Use 'htcli stake info' to monitor progress\n"
                    f"• Consider staking to other nodes/subnets",
                    title="Stake Removal Complete",
                    border_style="green",
                )
            )
        else:
            print_error(f"❌ Stake removal failed: {stake_removal_response.message}")
            raise typer.Exit(1)
        # For now, show what would happen
        console.print(
            Panel(
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
                border_style="yellow",
            )
        )

        # Simulate successful response
        print_success(
            f"✅ Stake removal initiated for node {node_id} in subnet {subnet_id}!"
        )

        console.print(
            Panel(
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
                border_style="green",
            )
        )

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
            # Load keypair for signing
            from ..utils.crypto import load_keypair

            # Get secure password for keypair
            password = get_secure_password(
                key_name,
                prompt_message="Enter password to unlock keypair",
                allow_default=True,
            )
            keypair = load_keypair(key_name, password)
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
            border_style="green",
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

            # Get secure password for keypair

            password = get_secure_password(
                key_name,
                prompt_message="Enter password to unlock keypair for delegate stake addition",
                allow_default=True,
            )
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
            border_style="yellow",
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

            # Get secure password for keypair

            password = get_secure_password(
                key_name,
                prompt_message="Enter password to unlock keypair for delegate stake removal",
                allow_default=True,
            )
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
        ...,
        "--amount",
        "-a",
        help="Amount to add to delegate stake pool (in smallest units)",
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
            border_style="magenta",
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

            # Get secure password for keypair

            password = get_secure_password(
                key_name,
                prompt_message="Enter password to unlock keypair for delegate stake increase",
                allow_default=True,
            )
            keypair = load_keypair(key_name, password)
            print_info(f"🔑 Using key: {key_name}")

        response = client.increase_delegate_stake(subnet_id, amount, keypair)

        if response.success:
            print_success(
                f"✅ Successfully increased delegate stake pool by {format_balance(amount)}!"
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
            print_error(
                f"❌ Failed to increase delegate stake pool: {response.message}"
            )
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
            border_style="blue",
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

            # Get secure password for keypair

            password = get_secure_password(
                key_name,
                prompt_message="Enter password to unlock keypair for delegate stake transfer",
                allow_default=True,
            )
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


@app.command()
def node_add(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(..., "--node-id", "-n", help="Node ID to stake to"),
    amount: int = typer.Option(
        ..., "--amount", "-a", help="Amount to stake (in smallest units)"
    ),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Add stake to a specific subnet node with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel

        guidance_panel = Panel(
            f"[bold cyan]💰 Node Delegate Staking Guide[/bold cyan]\n\n"
            f"This will add stake to node {node_id} in subnet {subnet_id}:\n\n"
            f"[bold]What is Node Delegate Staking:[/bold]\n"
            f"• Stake directly to a specific node (not just subnet)\n"
            f"• Earn rewards based on node's delegate reward rate\n"
            f"• Node-specific performance affects your returns\n"
            f"• More targeted than subnet delegate staking\n"
            f"• Higher potential returns with higher risk\n\n"
            f"[bold]Node vs Subnet Staking:[/bold]\n"
            f"• [green]Node Staking[/green]: Stake to specific node, node-specific rewards\n"
            f"• [yellow]Subnet Staking[/yellow]: Stake to subnet pool, subnet-wide rewards\n"
            f"• [green]Higher Returns[/green]: Node staking can offer better rates\n"
            f"• [yellow]Higher Risk[/yellow]: Node performance affects your returns\n"
            f"• [yellow]Node Selection[/yellow]: Choose nodes based on performance\n\n"
            f"[bold]Reward Rate Impact:[/bold]\n"
            f"• Node's delegate reward rate determines your earnings\n"
            f"• Higher rate = more rewards for delegators\n"
            f"• Check node's current rate before staking\n"
            f"• Rate can change over time\n"
            f"• Monitor node performance and rate changes\n\n"
            f"[bold]Staking Process:[/bold]\n"
            f"• Validates node exists and is active\n"
            f"• Checks node's current delegate reward rate\n"
            f"• Transfers stake amount to node\n"
            f"• Begins earning rewards immediately\n"
            f"• Requires valid signing key\n\n"
            f"[bold]Strategic Considerations:[/bold]\n"
            f"• [yellow]Node Performance[/yellow]: Research node's track record\n"
            f"• [yellow]Reward Rate[/yellow]: Compare rates across nodes\n"
            f"• [yellow]Risk Assessment[/yellow]: Node-specific risks vs rewards\n"
            f"• [yellow]Diversification[/yellow]: Consider staking to multiple nodes\n"
            f"• [yellow]Monitoring[/yellow]: Track node performance over time\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Node performance directly affects your returns\n"
            f"• Research node before staking\n"
            f"• Monitor node performance regularly\n"
            f"• Consider diversifying across multiple nodes\n"
            f"• Higher potential returns come with higher risk",
            title="[bold blue]💰 Node Delegate Staking[/bold blue]",
            border_style="blue",
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(
            f"Add {amount} stake to node {node_id} in subnet {subnet_id}?"
        ):
            print_info("Node staking cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_node_id(node_id):
        print_error("❌ Invalid node ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_amount(amount):
        print_error("❌ Invalid stake amount. Must be a positive integer.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for staking)
    if not key_name:
        print_error(
            "❌ Key name is required for staking. Use --key-name to specify your signing key."
        )
        raise typer.Exit(1)

    try:
        print_info(f"💰 Adding stake to node {node_id} in subnet {subnet_id}...")

        # Load keypair for signing
        from ..utils.crypto import load_keypair

        # Get secure password for keypair

        password = get_secure_password(
            key_name,
            prompt_message="Enter password to unlock keypair for node delegate stake addition",
            allow_default=True,
        )
        keypair = load_keypair(key_name, password)

        # Add stake to the specific node
        response = client.add_to_node_delegate_stake(
            subnet_id=subnet_id, node_id=node_id, amount=amount, keypair=keypair
        )

        if response.success:
            print_success(f"✅ Successfully added stake to node {node_id}!")
            console.print(
                f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]"
            )
            if response.block_number:
                console.print(
                    f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]"
                )

            console.print(
                Panel(
                    f"[bold green]💰 Node Staking Complete![/bold green]\n\n"
                    f"Successfully added stake to node {node_id} in subnet {subnet_id}.\n\n"
                    f"[yellow]📊 Staking Details:[/yellow]\n"
                    f"• Stake Amount: [bold cyan]{amount}[/bold cyan] (in smallest units)\n"
                    f"• Target Node: [bold cyan]Node {node_id}[/bold cyan]\n"
                    f"• Subnet: [bold cyan]Subnet {subnet_id}[/bold cyan]\n"
                    f"• Staking Type: [bold cyan]Node Delegate Staking[/bold cyan]\n"
                    f"• Reward Type: [bold cyan]Node-Specific Rewards[/bold cyan]\n\n"
                    f"[yellow]💰 Reward Information:[/yellow]\n"
                    f"• [green]Rewards based on[/green] node's delegate reward rate\n"
                    f"• [green]Node performance[/green] affects your returns\n"
                    f"• [green]Immediate earning[/green] starts now\n"
                    f"• [yellow]Monitor node performance[/yellow] for optimal returns\n"
                    f"• [yellow]Check reward rate changes[/yellow] over time\n\n"
                    f"[yellow]📈 Strategic Impact:[/yellow]\n"
                    f"• [green]Higher potential returns[/green] than subnet staking\n"
                    f"• [yellow]Node-specific risk[/yellow] affects your investment\n"
                    f"• [yellow]Performance monitoring[/yellow] is crucial\n"
                    f"• [yellow]Diversification[/yellow] across nodes recommended\n"
                    f"• [yellow]Active management[/yellow] may be needed\n\n"
                    f"[yellow]📋 Next Steps:[/yellow]\n"
                    f"• Monitor node performance: htcli node status --subnet-id {subnet_id} --node-id {node_id}\n"
                    f"• Check your stakes: htcli stake node-info --subnet-id {subnet_id} --node-id {node_id}\n"
                    f"• Track rewards over time\n"
                    f"• Consider diversifying to other nodes\n"
                    f"• Monitor node's reward rate changes\n\n"
                    f"[yellow]💡 Tip:[/yellow]\n"
                    f"• Research node performance before staking\n"
                    f"• Monitor node performance regularly\n"
                    f"• Consider staking to multiple nodes for diversification\n"
                    f"• Higher returns come with higher risk",
                    title="Node Staking Success",
                    border_style="green",
                )
            )
        else:
            print_error(f"❌ Failed to add stake to node: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to add stake to node: {str(e)}")
        raise typer.Exit(1)


@app.command()
def node_remove(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(
        ..., "--node-id", "-n", help="Node ID to remove stake from"
    ),
    shares: int = typer.Option(
        ..., "--shares", "-sh", help="Shares to remove (in smallest units)"
    ),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Remove stake from a specific subnet node with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel

        guidance_panel = Panel(
            f"[bold cyan]💰 Remove Node Stake Guide[/bold cyan]\n\n"
            f"This will remove stake from node {node_id} in subnet {subnet_id}:\n\n"
            f"[bold]What is Share Removal:[/bold]\n"
            f"• Remove stake shares from a specific node\n"
            f"• Shares are converted to balance internally\n"
            f"• Receive actual balance back to your account\n"
            f"• Stop earning rewards on removed shares\n"
            f"• Can be partial or complete removal\n\n"
            f"[bold]Share vs Balance:[/bold]\n"
            f"• [green]Shares[/green]: Your stake representation in the node\n"
            f"• [yellow]Balance[/yellow]: Actual tokens you receive back\n"
            f"• [yellow]Conversion[/yellow]: Shares converted to balance automatically\n"
            f"• [yellow]Value[/yellow]: Balance value depends on node performance\n"
            f"• [yellow]Timing[/yellow]: Conversion happens at current rates\n\n"
            f"[bold]Removal Process:[/bold]\n"
            f"• Validates you have sufficient shares\n"
            f"• Converts shares to balance internally\n"
            f"• Removes shares from node stake\n"
            f"• Returns balance to your account\n"
            f"• Stops earning on removed amount\n\n"
            f"[bold]Strategic Considerations:[/bold]\n"
            f"• [yellow]Node Performance[/yellow]: Consider node's current performance\n"
            f"• [yellow]Market Conditions[/yellow]: Assess current market situation\n"
            f"• [yellow]Reward Rates[/yellow]: Compare with other opportunities\n"
            f"• [yellow]Diversification[/yellow]: Rebalance your portfolio\n"
            f"• [yellow]Timing[/yellow]: Choose optimal time for removal\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• You'll stop earning rewards on removed shares\n"
            f"• Consider node performance before removing\n"
            f"• Balance received depends on current rates\n"
            f"• Partial removal is possible\n"
            f"• Plan your removal strategy carefully",
            title="[bold blue]💰 Remove Node Stake[/bold blue]",
            border_style="blue",
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(
            f"Remove {shares} shares from node {node_id} in subnet {subnet_id}?"
        ):
            print_info("Node stake removal cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_node_id(node_id):
        print_error("❌ Invalid node ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_amount(shares):
        print_error("❌ Invalid shares amount. Must be a positive integer.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for removal)
    if not key_name:
        print_error(
            "❌ Key name is required for stake removal. Use --key-name to specify your signing key."
        )
        raise typer.Exit(1)

    try:
        print_info(f"💰 Removing stake from node {node_id} in subnet {subnet_id}...")

        # Load keypair for signing
        from ..utils.crypto import load_keypair

        # Get secure password for keypair

        password = get_secure_password(
            key_name,
            prompt_message="Enter password to unlock keypair for node removal",
            allow_default=True,
        )
        keypair = load_keypair(key_name, password)

        # Remove stake from the specific node
        response = client.remove_node_delegate_stake(
            subnet_id=subnet_id, node_id=node_id, shares=shares, keypair=keypair
        )

        if response.success:
            print_success(f"✅ Successfully removed stake from node {node_id}!")
            console.print(
                f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]"
            )
            if response.block_number:
                console.print(
                    f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]"
                )

            console.print(
                Panel(
                    f"[bold green]💰 Node Stake Removal Complete![/bold green]\n\n"
                    f"Successfully removed stake from node {node_id} in subnet {subnet_id}.\n\n"
                    f"[yellow]📊 Removal Details:[/yellow]\n"
                    f"• Shares Removed: [bold cyan]{shares}[/bold cyan] (in smallest units)\n"
                    f"• Source Node: [bold cyan]Node {node_id}[/bold cyan]\n"
                    f"• Subnet: [bold cyan]Subnet {subnet_id}[/bold cyan]\n"
                    f"• Removal Type: [bold cyan]Node Delegate Stake Removal[/bold cyan]\n"
                    f"• Balance Returned: [bold cyan]Converted from shares[/bold cyan]\n\n"
                    f"[yellow]💰 Balance Information:[/yellow]\n"
                    f"• [green]Shares converted[/green] to balance automatically\n"
                    f"• [green]Balance returned[/green] to your account\n"
                    f"• [yellow]Conversion rate[/yellow] based on current node performance\n"
                    f"• [yellow]No more rewards[/yellow] on removed shares\n"
                    f"• [yellow]Remaining shares[/yellow] continue earning\n\n"
                    f"[yellow]📈 Strategic Impact:[/yellow]\n"
                    f"• [green]Reduced exposure[/green] to node-specific risk\n"
                    f"• [yellow]Lower potential returns[/yellow] from this node\n"
                    f"• [yellow]Freed capital[/yellow] for other opportunities\n"
                    f"• [yellow]Portfolio rebalancing[/yellow] opportunity\n"
                    f"• [yellow]Risk management[/yellow] improvement\n\n"
                    f"[yellow]📋 Next Steps:[/yellow]\n"
                    f"• Check your remaining stakes: htcli stake node-info --subnet-id {subnet_id} --node-id {node_id}\n"
                    f"• Consider other staking opportunities\n"
                    f"• Monitor remaining node performance\n"
                    f"• Plan your next staking strategy\n"
                    f"• Consider diversifying to other nodes\n\n"
                    f"[yellow]💡 Tip:[/yellow]\n"
                    f"• Monitor remaining node performance\n"
                    f"• Consider other staking opportunities\n"
                    f"• Plan your portfolio diversification\n"
                    f"• Balance risk and return in your strategy",
                    title="Node Stake Removal Success",
                    border_style="green",
                )
            )
        else:
            print_error(f"❌ Failed to remove stake from node: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to remove stake from node: {str(e)}")
        raise typer.Exit(1)


@app.command()
def node_transfer(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(..., "--node-id", "-n", help="Node ID"),
    to_account: str = typer.Option(
        ..., "--to-account", "-t", help="Destination account address"
    ),
    shares: int = typer.Option(
        ..., "--shares", "-sh", help="Shares to transfer (in smallest units)"
    ),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Transfer node delegate stake shares to another account with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel

        guidance_panel = Panel(
            f"[bold cyan]💰 Transfer Node Stake Guide[/bold cyan]\n\n"
            f"This will transfer stake shares from node {node_id} in subnet {subnet_id}:\n\n"
            f"[bold]What is Share Transfer:[/bold]\n"
            f"• Transfer stake shares to another account\n"
            f"• Shares move from your account to destination\n"
            f"• Destination account receives the shares\n"
            f"• No conversion to balance (shares remain shares)\n"
            f"• Useful for gifting or account management\n\n"
            f"[bold]Transfer vs Removal:[/bold]\n"
            f"• [green]Transfer[/green]: Shares move to another account\n"
            f"• [yellow]Removal[/yellow]: Shares converted to balance for you\n"
            f"• [green]No conversion[/green]: Shares remain as shares\n"
            f"• [yellow]Account change[/yellow]: Ownership transfers\n"
            f"• [yellow]Same node[/yellow]: Still staked to same node\n\n"
            f"[bold]Transfer Process:[/bold]\n"
            f"• Validates destination account exists\n"
            f"• Checks you have sufficient shares\n"
            f"• Transfers shares to destination account\n"
            f"• Destination receives stake ownership\n"
            f"• Shares continue earning for destination\n\n"
            f"[bold]Strategic Considerations:[/bold]\n"
            f"• [yellow]Account Management[/yellow]: Organize stakes across accounts\n"
            f"• [yellow]Gifting[/yellow]: Transfer stakes as gifts\n"
            f"• [yellow]Tax Planning[/yellow]: Consider tax implications\n"
            f"• [yellow]Security[/yellow]: Ensure destination account is secure\n"
            f"• [yellow]Documentation[/yellow]: Keep records of transfers\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Destination account receives stake ownership\n"
            f"• Shares continue earning for destination account\n"
            f"• Verify destination account address carefully\n"
            f"• Transfer is irreversible\n"
            f"• Consider tax and legal implications",
            title="[bold blue]💰 Transfer Node Stake[/bold blue]",
            border_style="blue",
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(
            f"Transfer {shares} shares to {to_account} from node {node_id} in subnet {subnet_id}?"
        ):
            print_info("Node stake transfer cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_node_id(node_id):
        print_error("❌ Invalid node ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_address(to_account):
        print_error(
            "❌ Invalid destination account address. Must be a valid SS58 address."
        )
        raise typer.Exit(1)

    if not validate_amount(shares):
        print_error("❌ Invalid shares amount. Must be a positive integer.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for transfer)
    if not key_name:
        print_error(
            "❌ Key name is required for stake transfer. Use --key-name to specify your signing key."
        )
        raise typer.Exit(1)

    try:
        print_info(
            f"💰 Transferring stake shares from node {node_id} in subnet {subnet_id}..."
        )

        # Load keypair for signing
        from ..utils.crypto import load_keypair

        # Get secure password for keypair

        password = get_secure_password(
            key_name,
            prompt_message="Enter password to unlock keypair for node delegate stake transfer",
            allow_default=True,
        )
        keypair = load_keypair(key_name, password)

        # Transfer stake shares to another account
        response = client.transfer_node_delegate_stake(
            subnet_id=subnet_id,
            node_id=node_id,
            to_account=to_account,
            shares=shares,
            keypair=keypair,
        )

        if response.success:
            print_success(
                f"✅ Successfully transferred stake shares from node {node_id}!"
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
                    f"[bold green]💰 Node Stake Transfer Complete![/bold green]\n\n"
                    f"Successfully transferred stake shares from node {node_id} in subnet {subnet_id}.\n\n"
                    f"[yellow]📊 Transfer Details:[/yellow]\n"
                    f"• Shares Transferred: [bold cyan]{shares}[/bold cyan] (in smallest units)\n"
                    f"• Source Node: [bold cyan]Node {node_id}[/bold cyan]\n"
                    f"• Subnet: [bold cyan]Subnet {subnet_id}[/bold cyan]\n"
                    f"• Destination: [bold cyan]{to_account}[/bold cyan]\n"
                    f"• Transfer Type: [bold cyan]Node Delegate Stake Transfer[/bold cyan]\n\n"
                    f"[yellow]💰 Share Information:[/yellow]\n"
                    f"• [green]Shares transferred[/green] to destination account\n"
                    f"• [green]No conversion[/green] to balance (shares remain shares)\n"
                    f"• [green]Destination ownership[/green] of the shares\n"
                    f"• [yellow]Shares continue earning[/yellow] for destination\n"
                    f"• [yellow]Same node stake[/yellow] (ownership changed)\n\n"
                    f"[yellow]📈 Strategic Impact:[/yellow]\n"
                    f"• [green]Account management[/green] flexibility\n"
                    f"• [yellow]Reduced exposure[/yellow] to node-specific risk\n"
                    f"• [yellow]Gifting capability[/yellow] for stake shares\n"
                    f"• [yellow]Portfolio organization[/yellow] across accounts\n"
                    f"• [yellow]Tax planning[/yellow] opportunities\n\n"
                    f"[yellow]📋 Next Steps:[/yellow]\n"
                    f"• Verify transfer with destination account\n"
                    f"• Check your remaining stakes: htcli stake node-info --subnet-id {subnet_id} --node-id {node_id}\n"
                    f"• Consider other staking opportunities\n"
                    f"• Plan your portfolio strategy\n"
                    f"• Keep records of the transfer\n\n"
                    f"[yellow]💡 Tip:[/yellow]\n"
                    f"• Verify destination account address carefully\n"
                    f"• Keep records of all transfers\n"
                    f"• Consider tax implications of transfers\n"
                    f"• Plan your account organization strategy",
                    title="Node Stake Transfer Success",
                    border_style="green",
                )
            )
        else:
            print_error(f"❌ Failed to transfer stake shares: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to transfer stake shares: {str(e)}")
        raise typer.Exit(1)


@app.command()
def node_increase(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(
        ..., "--node-id", "-n", help="Node ID to increase stake for"
    ),
    amount: int = typer.Option(
        ...,
        "--amount",
        "-a",
        help="Amount to add to node stake pool (in smallest units)",
    ),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Increase node delegate stake pool (airdrop rewards) with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel

        guidance_panel = Panel(
            f"[bold cyan]💰 Increase Node Stake Pool Guide[/bold cyan]\n\n"
            f"This will increase the stake pool for node {node_id} in subnet {subnet_id}:\n\n"
            f"[bold]What is Pool Increase:[/bold]\n"
            f"• Add balance to node's delegate stake pool\n"
            f"• Increases balance for ALL current delegators\n"
            f"• Does NOT increase your personal balance\n"
            f"• Useful for airdropping rewards to delegators\n"
            f"• Rewards all existing stake holders proportionally\n\n"
            f"[bold]Pool vs Personal Staking:[/bold]\n"
            f"• [green]Pool Increase[/green]: Benefits all delegators, not just you\n"
            f"• [yellow]Personal Staking[/yellow]: Adds your personal stake to node\n"
            f"• [green]Airdrop Effect[/green]: Rewards all existing delegators\n"
            f"• [yellow]No Personal Gain[/yellow]: You don't get additional balance\n"
            f"• [yellow]Community Benefit[/yellow]: Helps all node delegators\n\n"
            f"[bold]Reward Distribution:[/bold]\n"
            f"• [green]Proportional[/green]: All delegators benefit proportionally\n"
            f"• [green]Immediate[/green]: Rewards distributed immediately\n"
            f"• [yellow]Existing Stakes[/yellow]: Current delegators get rewards\n"
            f"• [yellow]No New Stakes[/yellow]: Doesn't create new stake positions\n"
            f"• [yellow]Pool Growth[/yellow]: Increases total pool value\n\n"
            f"[bold]Use Cases:[/bold]\n"
            f"• [green]Airdrop Rewards[/green]: Reward loyal delegators\n"
            f"• [green]Community Building[/green]: Incentivize delegation\n"
            f"• [green]Performance Bonuses[/green]: Reward good node performance\n"
            f"• [green]Marketing Tool[/green]: Attract more delegators\n"
            f"• [green]Competitive Advantage[/green]: Stand out from other nodes\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• This does NOT increase your personal balance\n"
            f"• All current delegators benefit proportionally\n"
            f"• Consider this as a community investment\n"
            f"• Can be used for marketing and incentives\n"
            f"• Plan the amount carefully",
            title="[bold blue]💰 Increase Node Stake Pool[/bold blue]",
            border_style="blue",
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(
            f"Increase stake pool for node {node_id} in subnet {subnet_id} by {amount}?"
        ):
            print_info("Node stake pool increase cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_node_id(node_id):
        print_error("❌ Invalid node ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_amount(amount):
        print_error("❌ Invalid amount. Must be a positive integer.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for increase)
    if not key_name:
        print_error(
            "❌ Key name is required for pool increase. Use --key-name to specify your signing key."
        )
        raise typer.Exit(1)

    try:
        print_info(
            f"💰 Increasing stake pool for node {node_id} in subnet {subnet_id}..."
        )

        # Load keypair for signing
        from ..utils.crypto import load_keypair

        # Get secure password for keypair

        password = get_secure_password(
            key_name,
            prompt_message="Enter password to unlock keypair for node delegate stake increase",
            allow_default=True,
        )
        keypair = load_keypair(key_name, password)

        # Increase the node's delegate stake pool
        response = client.increase_node_delegate_stake(
            subnet_id=subnet_id, node_id=node_id, amount=amount, keypair=keypair
        )

        if response.success:
            print_success(f"✅ Successfully increased stake pool for node {node_id}!")
            console.print(
                f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]"
            )
            if response.block_number:
                console.print(
                    f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]"
                )

            console.print(
                Panel(
                    f"[bold green]💰 Node Stake Pool Increase Complete![/bold green]\n\n"
                    f"Successfully increased stake pool for node {node_id} in subnet {subnet_id}.\n\n"
                    f"[yellow]📊 Pool Increase Details:[/yellow]\n"
                    f"• Amount Added: [bold cyan]{amount}[/bold cyan] (in smallest units)\n"
                    f"• Target Node: [bold cyan]Node {node_id}[/bold cyan]\n"
                    f"• Subnet: [bold cyan]Subnet {subnet_id}[/bold cyan]\n"
                    f"• Increase Type: [bold cyan]Node Delegate Stake Pool Increase[/bold cyan]\n"
                    f"• Beneficiaries: [bold cyan]All Current Delegators[/bold cyan]\n\n"
                    f"[yellow]💰 Reward Distribution:[/yellow]\n"
                    f"• [green]All delegators[/green] benefit proportionally\n"
                    f"• [green]Immediate distribution[/green] of rewards\n"
                    f"• [green]Pool value increased[/green] for everyone\n"
                    f"• [yellow]No personal balance increase[/yellow] for you\n"
                    f"• [yellow]Community investment[/yellow] in node success\n\n"
                    f"[yellow]📈 Strategic Impact:[/yellow]\n"
                    f"• [green]Community building[/green] through rewards\n"
                    f"• [green]Delegator loyalty[/green] enhancement\n"
                    f"• [green]Competitive advantage[/green] over other nodes\n"
                    f"• [yellow]Marketing tool[/yellow] for attracting delegators\n"
                    f"• [yellow]Performance incentive[/yellow] for node operators\n\n"
                    f"[yellow]📋 Next Steps:[/yellow]\n"
                    f"• Monitor delegator response to rewards\n"
                    f"• Check node performance: htcli node status --subnet-id {subnet_id} --node-id {node_id}\n"
                    f"• Consider additional pool increases for marketing\n"
                    f"• Track delegator growth and loyalty\n"
                    f"• Plan future reward strategies\n\n"
                    f"[yellow]💡 Tip:[/yellow]\n"
                    f"• Use pool increases strategically for marketing\n"
                    f"• Monitor delegator response and loyalty\n"
                    f"• Consider regular reward programs\n"
                    f"• Balance rewards with node performance",
                    title="Node Stake Pool Increase Success",
                    border_style="green",
                )
            )
        else:
            print_error(f"❌ Failed to increase node stake pool: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to increase node stake pool: {str(e)}")
        raise typer.Exit(1)


@app.command()
def info(
    subnet_id: Optional[int] = typer.Option(
        None, "--subnet-id", "-s", help="Subnet ID to show info for"
    ),
    node_id: Optional[int] = typer.Option(
        None, "--node-id", "-n", help="Node ID to show info for"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Show comprehensive staking information with guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel

        guidance_panel = Panel(
            f"[bold cyan]💰 Staking Information Guide[/bold cyan]\n\n"
            f"This will show comprehensive staking information:\n\n"
            f"[bold]What You'll See:[/bold]\n"
            f"• [green]Subnet Delegate Staking[/green]: Stake to subnet pools\n"
            f"• [green]Node Delegate Staking[/green]: Stake to specific nodes\n"
            f"• [yellow]Reward Rates[/yellow]: Current delegate reward rates\n"
            f"• [yellow]Stake Balances[/yellow]: Your current stake amounts\n"
            f"• [yellow]Performance Metrics[/yellow]: Staking performance data\n\n"
            f"[bold]Staking Types:[/bold]\n"
            f"• [green]Subnet Staking[/green]: Stake to entire subnet, subnet-wide rewards\n"
            f"• [green]Node Staking[/green]: Stake to specific node, node-specific rewards\n"
            f"• [yellow]Risk vs Reward[/yellow]: Node staking has higher risk/reward\n"
            f"• [yellow]Diversification[/yellow]: Consider both types for portfolio\n\n"
            f"[bold]Information Displayed:[/bold]\n"
            f"• [green]Current Stakes[/green]: Your active stake positions\n"
            f"• [green]Reward Rates[/green]: Current delegate reward rates\n"
            f"• [green]Performance[/green]: Historical performance data\n"
            f"• [green]Balances[/green]: Current stake balances and values\n"
            f"• [green]Recommendations[/green]: Strategic staking advice\n\n"
            f"[yellow]💡 Tip:[/yellow]\n"
            f"• Monitor your stakes regularly\n"
            f"• Compare reward rates across options\n"
            f"• Consider diversification strategies\n"
            f"• Plan your staking portfolio",
            title="[bold blue]💰 Staking Information[/bold blue]",
            border_style="blue",
        )
        console.print(guidance_panel)
        console.print()

    try:
        print_info("💰 Fetching comprehensive staking information...")

        # Get user address for personalized information
        user_address = None
        if config.filter.mine:
            user_addresses = get_user_addresses()
            if user_addresses:
                user_address = user_addresses[0]  # Use first address for now

        # Get staking information
        if subnet_id and node_id:
            # Node-specific staking info
            print_info(
                f"📊 Showing staking information for node {node_id} in subnet {subnet_id}"
            )

            response = client.get_node_staking_info(subnet_id, node_id, user_address)

            if response.success:
                data = response.data
                console.print(
                    Panel(
                        f"[bold cyan]🔗 Node Staking Information[/bold cyan]\n\n"
                        f"[bold]Node Details:[/bold]\n"
                        f"• [green]Subnet ID[/green]: {data.get('subnet_id', 'N/A')}\n"
                        f"• [green]Node ID[/green]: {data.get('node_id', 'N/A')}\n"
                        f"• [green]Classification[/green]: {data.get('node_classification', {}).get('class', 'Unknown')}\n"
                        f"• [green]Penalties[/green]: {data.get('node_penalties', 0)}\n\n"
                        f"[bold]Staking Details:[/bold]\n"
                        f"• [yellow]Total Node Stake[/yellow]: {data.get('node_delegate_stake', 0):,} TENSOR\n"
                        f"• [yellow]Reward Rate[/yellow]: {data.get('node_reward_rate', 0)}%\n"
                        f"• [yellow]Total Delegators[/yellow]: {data.get('total_delegators', 0)}\n"
                        f"• [yellow]Estimated Rewards[/yellow]: {data.get('estimated_rewards', 0):.2f} TENSOR\n\n"
                        f"[bold]Your Stake:[/bold]\n"
                        f"• [green]Your Shares[/green]: {data.get('user_node_shares', 0):,}\n"
                        f"• [green]Your Stake Value[/green]: {data.get('user_stake_value', 0):,} TENSOR\n"
                        f"• [green]Your Percentage[/green]: {(data.get('user_stake_value', 0) / data.get('node_delegate_stake', 1) * 100):.2f}%\n\n"
                        f"[yellow]💡 Tip:[/yellow]\n"
                        f"• Monitor node performance regularly\n"
                        f"• Check reward rates for optimization\n"
                        f"• Consider diversifying across multiple nodes",
                        title="Node Staking Information",
                        border_style="blue",
                    )
                )
            else:
                print_error(f"❌ Failed to get node staking info: {response.message}")
                raise typer.Exit(1)

        elif subnet_id:
            # Subnet-specific staking info
            print_info(f"📊 Showing staking information for subnet {subnet_id}")

            response = client.get_subnet_staking_info(subnet_id, user_address)

            if response.success:
                data = response.data
                console.print(
                    Panel(
                        f"[bold cyan]🌐 Subnet Staking Information[/bold cyan]\n\n"
                        f"[bold]Subnet Details:[/bold]\n"
                        f"• [green]Subnet ID[/green]: {data.get('subnet_id', 'N/A')}\n"
                        f"• [green]Total Nodes[/green]: {data.get('total_nodes', 0)}\n"
                        f"• [green]Active Nodes[/green]: {data.get('active_nodes', 0)}\n\n"
                        f"[bold]Staking Details:[/bold]\n"
                        f"• [yellow]Total Subnet Stake[/yellow]: {data.get('subnet_delegate_stake', 0):,} TENSOR\n"
                        f"• [yellow]Reward Rate[/yellow]: {data.get('subnet_reward_rate', 0)}%\n"
                        f"• [yellow]Total Delegators[/yellow]: {data.get('total_delegators', 0)}\n"
                        f"• [yellow]Estimated Rewards[/yellow]: {data.get('estimated_rewards', 0):.2f} TENSOR\n\n"
                        f"[bold]Your Stake:[/bold]\n"
                        f"• [green]Your Shares[/green]: {data.get('user_subnet_shares', 0):,}\n"
                        f"• [green]Your Stake Value[/green]: {data.get('user_stake_value', 0):,} TENSOR\n"
                        f"• [green]Your Percentage[/green]: {(data.get('user_stake_value', 0) / data.get('subnet_delegate_stake', 1) * 100):.2f}%\n\n"
                        f"[yellow]💡 Tip:[/yellow]\n"
                        f"• Subnet staking provides broader exposure\n"
                        f"• Monitor subnet performance and node activity\n"
                        f"• Consider both subnet and node staking for diversification",
                        title="Subnet Staking Information",
                        border_style="green",
                    )
                )
            else:
                print_error(f"❌ Failed to get subnet staking info: {response.message}")
                raise typer.Exit(1)

        else:
            # General staking info
            print_info("📊 Showing general staking information")

            response = client.get_general_staking_info(user_address)

            if response.success:
                data = response.data
                network_stats = data.get("network_stats", {})

                console.print(
                    Panel(
                        f"[bold cyan]🌍 Network Staking Overview[/bold cyan]\n\n"
                        f"[bold]Network Statistics:[/bold]\n"
                        f"• [green]Total Subnets[/green]: {network_stats.get('total_subnets', 0)}\n"
                        f"• [green]Total Network Stake[/green]: {network_stats.get('total_network_stake', 0):,} TENSOR\n"
                        f"• [green]Average Reward Rate[/green]: {network_stats.get('average_reward_rate', 0):.2f}%\n\n"
                        f"[bold]Your Portfolio:[/bold]\n"
                        f"• [yellow]Total User Stake[/yellow]: {network_stats.get('total_user_stake', 0):,} TENSOR\n"
                        f"• [yellow]Portfolio Percentage[/yellow]: {network_stats.get('user_stake_percentage', 0):.2f}%\n"
                        f"• [yellow]Address[/yellow]: {data.get('user_address', 'Not specified')}\n\n"
                        f"[bold]Top Performing Subnets:[/bold]\n"
                        f"• Subnet {network_stats.get('top_performing_subnets', [{}])[0].get('subnet_id', 'N/A')}: {network_stats.get('top_performing_subnets', [{}])[0].get('subnet_reward_rate', 0)}% rate\n\n"
                        f"[bold]Recommendations:[/bold]\n"
                        f"• Diversify across multiple subnets\n"
                        f"• Monitor performance regularly\n"
                        f"• Consider both high-reward and stable options\n\n"
                        f"[yellow]💡 Tip:[/yellow]\n"
                        f"• Diversify across multiple subnets and nodes\n"
                        f"• Monitor performance and adjust strategy\n"
                        f"• Consider both high-reward and stable options",
                        title="Network Staking Overview",
                        border_style="cyan",
                    )
                )
            else:
                print_error(
                    f"❌ Failed to get general staking info: {response.message}"
                )
                raise typer.Exit(1)

        print_success("✅ Staking information retrieved successfully!")

    except Exception as e:
        print_error(f"❌ Failed to get staking information: {str(e)}")
        raise typer.Exit(1)
