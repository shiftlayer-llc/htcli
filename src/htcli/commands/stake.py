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
    validate_amount
)
from ..utils.formatting import (
    print_success, print_error, print_info, format_balance, format_stake_info
)
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
                "• Valid hotkey address for the node"
            ],
            "process": [
                "1. Validates all input parameters",
                "2. Checks your TENSOR balance is sufficient",
                "3. Verifies node exists and is active",
                "4. Locks tokens in staking contract",
                "5. Updates your stake position",
                "6. Begins earning staking rewards"
            ],
            "tips": [
                "💡 Check node status with: htcli node status --subnet-id <ID> --node-id <ID>",
                "💡 Verify your balance with: htcli chain balance --address <address>",
                "💡 Staked tokens are locked and earn rewards",
                "💡 Higher stake = higher potential rewards",
                "⚠️ Unstaking has an unbonding period before tokens are available"
            ]
        },
        "remove": {
            "title": "📤 Removing Stake from Node",
            "description": "This operation will unstake TENSOR tokens from a node.",
            "requirements": [
                "• Valid subnet ID and node ID",
                "• Existing stake position with the node",
                "• Valid hotkey address",
                "• Amount must not exceed current stake"
            ],
            "process": [
                "1. Validates stake position exists",
                "2. Checks requested amount is available",
                "3. Initiates unbonding process",
                "4. Tokens enter unbonding period",
                "5. Reduces your stake position",
                "6. Stops earning rewards on unstaked amount"
            ],
            "tips": [
                "⚠️ Unbonding period applies before tokens are available",
                "⚠️ Unstaked tokens stop earning rewards immediately",
                "💡 Check current stake with: htcli stake info --address <addr> --subnet-id <ID>",
                "💡 Use claim-unbondings to retrieve unbonded tokens",
                "💡 Consider partial unstaking to maintain some rewards"
            ]
        },
        "info": {
            "title": "📊 Checking Stake Information",
            "description": "This operation shows your staking positions and rewards.",
            "requirements": [
                "• Valid account address",
                "• Valid subnet ID (optional for all stakes)"
            ],
            "process": [
                "1. Queries your stake positions",
                "2. Retrieves current rewards",
                "3. Shows unbonding positions",
                "4. Calculates total staked amounts",
                "5. Displays formatted stake summary"
            ],
            "tips": [
                "💡 Monitor your rewards regularly",
                "💡 Check unbonding status before claiming",
                "💡 Use --format json for programmatic access",
                "💡 Track performance across multiple subnets"
            ]
        },
        "claim": {
            "title": "🎯 Claiming Unbonded Tokens",
            "description": "This operation claims tokens that have completed unbonding.",
            "requirements": [
                "• Unbonded tokens available for claiming",
                "• Valid hotkey address",
                "• Unbonding period must be complete"
            ],
            "process": [
                "1. Checks for completed unbondings",
                "2. Validates unbonding period is finished",
                "3. Transfers tokens back to your account",
                "4. Updates unbonding records",
                "5. Tokens become freely available"
            ],
            "tips": [
                "💡 Check unbonding status before claiming",
                "💡 Claim regularly to free up tokens",
                "💡 Claimed tokens can be restaked or transferred",
                "⚠️ Can only claim after unbonding period expires"
            ]
        },
        "delegate": {
            "title": "🤝 Delegate Staking Operations",
            "description": "This operation manages delegate staking positions.",
            "requirements": [
                "• Valid subnet ID",
                "• Sufficient TENSOR balance",
                "• Active subnet accepting delegates"
            ],
            "process": [
                "1. Validates subnet and delegate parameters",
                "2. Locks tokens in delegate staking",
                "3. Begins earning delegate rewards",
                "4. Updates delegate position"
            ],
            "tips": [
                "💡 Delegate staking has different reward mechanics",
                "💡 Monitor delegate performance and rewards",
                "💡 Can transfer between different subnets",
                "⚠️ Delegate rewards depend on subnet performance"
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
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(..., "--node-id", "-n", help="Node ID"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey address"),
    amount: int = typer.Option(..., "--amount", "-a", help="Stake amount (in smallest units)"),
    key_name: Optional[str] = typer.Option(None, "--key-name", "-k", help="Key name for signing"),
    show_guidance: bool = typer.Option(True, "--guidance/--no-guidance", help="Show comprehensive guidance")
):
    """Add stake to a node with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        show_staking_guidance("add", {
            "Subnet ID": subnet_id,
            "Node ID": node_id,
            "Hotkey": hotkey,
            "Stake Amount": format_balance(amount)
        })

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
        print_info(f"🔄 Adding {format_balance(amount)} stake to node {node_id} in subnet {subnet_id}...")

        request = StakeAddRequest(
            subnet_id=subnet_id,
            node_id=node_id,
            hotkey=hotkey,
            stake_to_be_added=amount
        )

        # Get keypair for signing if provided
        keypair = None
        if key_name:
            # TODO: Load keypair from storage
            print_info(f"🔑 Using key: {key_name}")

        response = client.add_to_stake(request, keypair)

        if response.success:
            print_success(f"✅ Successfully added {format_balance(amount)} stake!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]💰 Stake Addition Complete![/bold green]\n\n"
                f"Added {format_balance(amount)} to node {node_id} in subnet {subnet_id}.\n"
                f"• Hotkey: {hotkey}\n"
                f"• Your stake is now active and earning rewards\n"
                f"• Rewards will be distributed according to node performance\n\n"
                f"[yellow]📊 Monitor your stake:[/yellow]\n"
                f"Use: [bold]htcli stake info --address {hotkey} --subnet-id {subnet_id}[/bold]",
                title="Staking Success",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to add stake: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to add stake: {str(e)}")
        raise typer.Exit(1)


@app.command()
def remove(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey address"),
    amount: int = typer.Option(..., "--amount", "-a", help="Stake amount to remove (in smallest units)"),
    key_name: Optional[str] = typer.Option(None, "--key-name", "-k", help="Key name for signing"),
    show_guidance: bool = typer.Option(True, "--guidance/--no-guidance", help="Show comprehensive guidance")
):
    """Remove stake from a node with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        show_staking_guidance("remove", {
            "Subnet ID": subnet_id,
            "Hotkey": hotkey,
            "Amount to Remove": format_balance(amount)
        })

        # Ask for confirmation with warning
        console.print("[bold red]⚠️ WARNING: Removed stake will enter unbonding period![/bold red]")
        if not typer.confirm("Are you sure you want to remove this stake?"):
            print_info("Stake removal cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_address(hotkey):
        print_error("❌ Invalid hotkey address format.")
        raise typer.Exit(1)

    if not validate_amount(amount):
        print_error("❌ Invalid stake amount. Must be positive.")
        raise typer.Exit(1)

    try:
        print_info(f"🔄 Removing {format_balance(amount)} stake from subnet {subnet_id}...")

        request = StakeRemoveRequest(
            subnet_id=subnet_id,
            hotkey=hotkey,
            stake_to_be_removed=amount
        )

        # Get keypair for signing if provided
        keypair = None
        if key_name:
            # TODO: Load keypair from storage
            print_info(f"🔑 Using key: {key_name}")

        response = client.remove_stake(request, keypair)

        if response.success:
            print_success(f"✅ Successfully removed {format_balance(amount)} stake!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold yellow]📤 Stake Removal Complete![/bold yellow]\n\n"
                f"Removed {format_balance(amount)} from subnet {subnet_id}.\n"
                f"• Hotkey: {hotkey}\n"
                f"• Tokens are now unbonding\n"
                f"• No longer earning rewards on removed amount\n\n"
                f"[yellow]⏳ Unbonding Period Active:[/yellow]\n"
                f"Tokens will be available after unbonding period.\n"
                f"Claim with: [bold]htcli stake claim --hotkey {hotkey}[/bold]",
                title="Unbonding Started",
                border_style="yellow"
            ))
        else:
            print_error(f"❌ Failed to remove stake: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to remove stake: {str(e)}")
        raise typer.Exit(1)


@app.command()
def info(
    address: str = typer.Option(..., "--address", "-a", help="Account address"),
    subnet_id: Optional[int] = typer.Option(None, "--subnet-id", "-s", help="Subnet ID (optional, shows all if not specified)"),
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)"),
    show_guidance: bool = typer.Option(False, "--guidance", help="Show comprehensive guidance")
):
    """Get stake information for an account with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance if requested
    if show_guidance:
        show_staking_guidance("info", {
            "Address": address,
            "Subnet ID": subnet_id or "All subnets",
            "Output Format": format_type
        })

    # Validate inputs
    if not validate_address(address):
        print_error("❌ Invalid address format.")
        raise typer.Exit(1)

    if subnet_id is not None and not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    try:
        if subnet_id:
            print_info(f"🔄 Retrieving stake information for subnet {subnet_id}...")
            response = client.get_account_subnet_stake(address, subnet_id)
        else:
            print_info("🔄 Retrieving stake information for all subnets...")
            # TODO: Implement get_all_stakes method
            print_error("❌ All-subnet stake info not yet implemented. Please specify --subnet-id")
            raise typer.Exit(1)

        if response.success:
            stake_data = response.data

            if format_type == "json":
                console.print_json(data=stake_data)
            else:
                format_stake_info(stake_data, address, subnet_id)

            print_success("✅ Retrieved stake information successfully")
        else:
            print_error(f"❌ Failed to retrieve stake info: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to get stake info: {str(e)}")
        raise typer.Exit(1)


@app.command()
def claim(
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey address"),
    key_name: Optional[str] = typer.Option(None, "--key-name", "-k", help="Key name for signing"),
    show_guidance: bool = typer.Option(True, "--guidance/--no-guidance", help="Show comprehensive guidance")
):
    """Claim unbonded stake with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        show_staking_guidance("claim", {
            "Hotkey": hotkey
        })

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
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]🎯 Unbonded Tokens Claimed![/bold green]\n\n"
                f"Your unbonded tokens have been returned to your account.\n"
                f"• Hotkey: {hotkey}\n"
                f"• Tokens are now freely available\n"
                f"• Can be restaked or transferred as needed\n\n"
                f"[yellow]💡 Next Steps:[/yellow]\n"
                f"• Check balance: [bold]htcli chain balance --address {hotkey}[/bold]\n"
                f"• Restake if desired: [bold]htcli stake add --subnet-id <ID>[/bold]",
                title="Claim Complete",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to claim unbondings: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to claim unbondings: {str(e)}")
        raise typer.Exit(1)


@app.command()
def delegate_add(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    amount: int = typer.Option(..., "--amount", "-a", help="Stake amount to delegate (in smallest units)"),
    key_name: Optional[str] = typer.Option(None, "--key-name", "-k", help="Key name for signing"),
    show_guidance: bool = typer.Option(True, "--guidance/--no-guidance", help="Show comprehensive guidance")
):
    """Add delegate stake with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        show_staking_guidance("delegate", {
            "Subnet ID": subnet_id,
            "Delegate Amount": format_balance(amount),
            "Operation": "Add Delegate Stake"
        })

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
        print_info(f"🔄 Adding {format_balance(amount)} delegate stake to subnet {subnet_id}...")

        # Get keypair for signing if provided
        keypair = None
        if key_name:
            # TODO: Load keypair from storage
            print_info(f"🔑 Using key: {key_name}")

        response = client.add_to_delegate_stake(subnet_id, amount, keypair)

        if response.success:
            print_success(f"✅ Successfully added {format_balance(amount)} delegate stake!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]🤝 Delegate Stake Added![/bold green]\n\n"
                f"Added {format_balance(amount)} delegate stake to subnet {subnet_id}.\n"
                f"• Earning delegate rewards based on subnet performance\n"
                f"• Can transfer to other subnets if needed\n"
                f"• Monitor performance and rewards regularly\n\n"
                f"[yellow]💡 Management:[/yellow]\n"
                f"• Transfer: [bold]htcli stake delegate-transfer[/bold]\n"
                f"• Remove: [bold]htcli stake delegate-remove[/bold]",
                title="Delegate Staking Active",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to add delegate stake: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to add delegate stake: {str(e)}")
        raise typer.Exit(1)


@app.command()
def delegate_remove(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    shares: int = typer.Option(..., "--shares", "-sh", help="Number of shares to remove"),
    key_name: Optional[str] = typer.Option(None, "--key-name", "-k", help="Key name for signing"),
    show_guidance: bool = typer.Option(True, "--guidance/--no-guidance", help="Show comprehensive guidance")
):
    """Remove delegate stake with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        show_staking_guidance("delegate", {
            "Subnet ID": subnet_id,
            "Shares to Remove": shares,
            "Operation": "Remove Delegate Stake"
        })

        # Ask for confirmation
        console.print("[bold red]⚠️ WARNING: Removing delegate stake will stop earning rewards![/bold red]")
        if not typer.confirm("Are you sure you want to remove this delegate stake?"):
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
            # TODO: Load keypair from storage
            print_info(f"🔑 Using key: {key_name}")

        response = client.remove_delegate_stake(subnet_id, shares, keypair)

        if response.success:
            print_success(f"✅ Successfully removed {shares} delegate shares!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold yellow]📤 Delegate Stake Removed![/bold yellow]\n\n"
                f"Removed {shares} shares from subnet {subnet_id}.\n"
                f"• No longer earning rewards from this position\n"
                f"• Tokens may enter unbonding period\n"
                f"• Can be restaked in other subnets if desired\n\n"
                f"[yellow]⏳ Check Status:[/yellow]\n"
                f"Monitor unbonding and claim when ready.",
                title="Delegate Removal Complete",
                border_style="yellow"
            ))
        else:
            print_error(f"❌ Failed to remove delegate stake: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to remove delegate stake: {str(e)}")
        raise typer.Exit(1)


@app.command()
def delegate_transfer(
    from_subnet: int = typer.Option(..., "--from-subnet", "-f", help="Source subnet ID"),
    to_subnet: int = typer.Option(..., "--to-subnet", "-t", help="Destination subnet ID"),
    shares: int = typer.Option(..., "--shares", "-sh", help="Number of shares to transfer"),
    key_name: Optional[str] = typer.Option(None, "--key-name", "-k", help="Key name for signing"),
    show_guidance: bool = typer.Option(True, "--guidance/--no-guidance", help="Show comprehensive guidance")
):
    """Transfer delegate stake between subnets with comprehensive guidance."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        show_staking_guidance("delegate", {
            "From Subnet": from_subnet,
            "To Subnet": to_subnet,
            "Shares to Transfer": shares,
            "Operation": "Transfer Delegate Stake"
        })

        # Ask for confirmation
        if not typer.confirm(f"Transfer {shares} shares from subnet {from_subnet} to {to_subnet}?"):
            print_info("Delegate stake transfer cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(from_subnet):
        print_error("❌ Invalid source subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_subnet_id(to_subnet):
        print_error("❌ Invalid destination subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if from_subnet == to_subnet:
        print_error("❌ Source and destination subnets cannot be the same.")
        raise typer.Exit(1)

    if shares <= 0:
        print_error("❌ Invalid shares amount. Must be positive.")
        raise typer.Exit(1)

    try:
        print_info(f"🔄 Transferring {shares} shares from subnet {from_subnet} to {to_subnet}...")

        # Get keypair for signing if provided
        keypair = None
        if key_name:
            # TODO: Load keypair from storage
            print_info(f"🔑 Using key: {key_name}")

        response = client.transfer_delegate_stake(from_subnet, to_subnet, shares, keypair)

        if response.success:
            print_success(f"✅ Successfully transferred {shares} delegate shares!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]🔄 Delegate Stake Transferred![/bold green]\n\n"
                f"Transferred {shares} shares:\n"
                f"• From: Subnet {from_subnet}\n"
                f"• To: Subnet {to_subnet}\n"
                f"• Now earning rewards from destination subnet\n"
                f"• Transfer completed in single transaction\n\n"
                f"[yellow]💡 Monitor Performance:[/yellow]\n"
                f"Track rewards in the new subnet position.",
                title="Transfer Complete",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to transfer delegate stake: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to transfer delegate stake: {str(e)}")
        raise typer.Exit(1)
