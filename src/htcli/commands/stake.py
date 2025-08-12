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
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey address"),
    amount: int = typer.Option(
        ..., "--amount", "-a", help="Stake amount to remove (in smallest units)"
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
        show_staking_guidance(
            "remove",
            {
                "Subnet ID": subnet_id,
                "Hotkey": hotkey,
                "Amount to Remove": format_balance(amount),
            },
        )

        # Ask for confirmation with warning
        console.print(
            "[bold red]⚠️ WARNING: Removed stake will enter unbonding period![/bold red]"
        )
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
        print_info(
            f"🔄 Removing {format_balance(amount)} stake from subnet {subnet_id}..."
        )

        request = StakeRemoveRequest(
            subnet_id=subnet_id, hotkey=hotkey, stake_to_be_removed=amount
        )

        # Get keypair for signing if provided
        keypair = None
        if key_name:
            # TODO: Load keypair from storage
            print_info(f"🔑 Using key: {key_name}")

        response = client.remove_stake(request, keypair)

        if response.success:
            print_success(f"✅ Successfully removed {format_balance(amount)} stake!")
            console.print(
                f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]"
            )
            if response.block_number:
                console.print(
                    f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]"
                )

            console.print(
                Panel(
                    f"[bold yellow]📤 Stake Removal Complete![/bold yellow]\n\n"
                    f"Removed {format_balance(amount)} from subnet {subnet_id}.\n"
                    f"• Hotkey: {hotkey}\n"
                    f"• Tokens are now unbonding\n"
                    f"• No longer earning rewards on removed amount\n\n"
                    f"[yellow]⏳ Unbonding Period Active:[/yellow]\n"
                    f"Tokens will be available after unbonding period.\n"
                    f"Claim with: [bold]htcli stake claim --hotkey {hotkey}[/bold]",
                    title="Unbonding Started",
                    border_style="yellow",
                )
            )
        else:
            print_error(f"❌ Failed to remove stake: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to remove stake: {str(e)}")
        raise typer.Exit(1)


@app.command()
def info(
    address: Optional[str] = typer.Option(
        None, "--address", "-a", help="Account address (optional with --mine)"
    ),
    subnet_id: Optional[int] = typer.Option(
        None,
        "--subnet-id",
        "-s",
        help="Subnet ID (optional, shows all if not specified)",
    ),
    format_type: str = typer.Option(
        "table", "--format", "-f", help="Output format (table/json)"
    ),
    show_guidance: bool = typer.Option(
        False, "--guidance", help="Show comprehensive guidance"
    ),
):
    """Get stake information. Use --mine flag globally to show stakes for all your addresses."""
    client = get_client()

    # Check if --mine filter is enabled globally
    config = client.config
    filter_mine = getattr(config.filter, "mine", False)

    # Determine addresses to check
    if filter_mine:
        user_addresses = require_user_keys()
        addresses_to_check = [addr for _, addr in user_addresses]
        if address:
            print_info(
                "💡 --mine flag detected: ignoring --address parameter, using your wallet addresses"
            )
    else:
        if not address:
            print_error("❌ Address is required when not using --mine filter.")
            raise typer.Exit(1)
        addresses_to_check = [address]

    # Show comprehensive guidance if requested
    if show_guidance:
        show_staking_guidance(
            "info",
            {
                "Address": addresses_to_check if filter_mine else address,
                "Subnet ID": subnet_id or "All subnets",
                "Output Format": format_type,
                "Mine Filter": (
                    "Enabled - showing your addresses" if filter_mine else "Disabled"
                ),
            },
        )

    # Validate inputs
    for addr in addresses_to_check:
        if not validate_address(addr):
            print_error(f"❌ Invalid address format: {addr}")
            raise typer.Exit(1)

    if subnet_id is not None and not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    try:
        all_stake_data = []

        for addr in addresses_to_check:
            if subnet_id:
                print_info(
                    f"🔄 Retrieving stake information for {addr[:10]}... subnet {subnet_id}..."
                )
                response = client.get_account_subnet_stake(addr, subnet_id)
                if response.success and response.data:
                    stake_data = response.data
                    stake_data["address"] = addr
                    all_stake_data.append(stake_data)
            else:
                print_info(
                    f"🔄 Retrieving stake information for {addr[:10]}... all subnets..."
                )
                # Check multiple subnets for this address
                for sid in range(1, 10):  # Check first 10 subnets
                    try:
                        response = client.get_account_subnet_stake(addr, sid)
                        if response.success and response.data:
                            stake_data = response.data
                            total_stake = stake_data.get("total_stake", 0)
                            if total_stake > 0:  # Only include if there's actual stake
                                stake_data["address"] = addr
                                stake_data["subnet_id"] = sid
                                all_stake_data.append(stake_data)
                    except:
                        continue  # Skip non-existent stakes

        if filter_mine:
            show_mine_filter_info(user_addresses, len(all_stake_data))

        if all_stake_data:
            if format_type == "json":
                console.print_json(data=all_stake_data)
            else:
                if filter_mine:
                    # Show combined stake info for all addresses
                    from rich.table import Table

                    table = Table(title="🎯 Your Stake Positions")
                    table.add_column("Address", style="cyan")
                    if not subnet_id:
                        table.add_column("Subnet ID", style="magenta")
                    table.add_column("Total Stake", style="green")
                    table.add_column("Rewards", style="yellow")

                    total_stakes = 0
                    total_rewards = 0

                    for stake_data in all_stake_data:
                        addr = stake_data.get("address", "")
                        total_stake = stake_data.get("total_stake", 0)
                        rewards = stake_data.get("rewards", 0)
                        sid = stake_data.get("subnet_id", subnet_id)

                        row = [
                            addr[:20] + "...",
                            format_balance(total_stake),
                            format_balance(rewards),
                        ]
                        if not subnet_id:
                            row.insert(1, str(sid))
                        table.add_row(*row)

                        total_stakes += total_stake
                        total_rewards += rewards

                    console.print(table)
                    print_info(
                        f"📊 Total across all addresses: {format_balance(total_stakes)} staked, {format_balance(total_rewards)} rewards"
                    )
                else:
                    # Show single address stake info
                    format_stake_info(all_stake_data[0])

            print_success("✅ Retrieved stake information successfully")
        else:
            if filter_mine:
                print_info("💡 No active stakes found for your addresses.")
            else:
                print_info("💡 No stakes found for the specified address.")

    except Exception as e:
        print_error(f"❌ Failed to get stake info: {str(e)}")
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
