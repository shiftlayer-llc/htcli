"""
Flattened subnet commands - 3-level hierarchy.
"""

import typer
from rich.console import Console
from typing import Optional
from ..models.requests import SubnetRegisterRequest
from ..utils.validation import (
    validate_subnet_name,
    validate_repo_url,
    validate_subnet_description,
    validate_stake_amount,
    validate_delegate_percentage,
    validate_epoch_value,
    validate_churn_limit,
    validate_max_nodes,
    validate_max_penalties,
    validate_key_types,
    validate_coldkey_addresses,
    validate_subnet_id,
    validate_address,
    validate_node_id,
)
from ..utils.formatting import (
    print_info,
    print_success,
    print_error,
    format_subnet_list,
    format_subnet_info,
    format_balance,
)
from ..utils.ownership import user_owns_subnet, require_user_keys, show_mine_filter_info
from ..dependencies import get_client

app = typer.Typer(name="subnet", help="Subnet operations")
console = Console()


@app.command()
def register(
    name: str = typer.Option(..., "--name", "-n", help="Unique name of the subnet"),
    repo: str = typer.Option(
        ..., "--repo", "-r", help="GitHub or similar link to source code"
    ),
    description: str = typer.Option(
        ..., "--description", "-d", help="Description of the subnet"
    ),
    misc: str = typer.Option("", "--misc", "-m", help="Miscellaneous information"),
    # Stake configuration
    min_stake: int = typer.Option(
        ..., "--min-stake", help="Minimum required stake balance to register a node"
    ),
    max_stake: int = typer.Option(
        ..., "--max-stake", help="Maximum allowable stake balance for a subnet node"
    ),
    delegate_stake_percentage: int = typer.Option(
        ...,
        "--delegate-percentage",
        help="Percentage ratio of emissions given to delegate stakers",
    ),
    # Epoch and timing configuration
    churn_limit: int = typer.Option(
        ..., "--churn-limit", help="Number of subnet activations per epoch"
    ),
    registration_queue_epochs: int = typer.Option(
        ...,
        "--queue-epochs",
        help="Number of epochs for registered nodes to be in queue before activation",
    ),
    activation_grace_epochs: int = typer.Option(
        ...,
        "--grace-epochs",
        help="Grace period epochs during which nodes can activate",
    ),
    queue_classification_epochs: int = typer.Option(
        ..., "--queue-classification", help="Number of epochs for queue classification"
    ),
    included_classification_epochs: int = typer.Option(
        ...,
        "--included-classification",
        help="Number of epochs for included classification",
    ),
    # Node configuration
    max_node_penalties: int = typer.Option(
        ..., "--max-penalties", help="Maximum penalties a node can have before removal"
    ),
    max_registered_nodes: int = typer.Option(
        ..., "--max-nodes", help="Maximum number of nodes in registration queue"
    ),
    initial_coldkeys: Optional[str] = typer.Option(
        None,
        "--initial-coldkeys",
        help="Comma-separated list of initial coldkey addresses",
    ),
    # Key types
    key_types: str = typer.Option(
        "Ed25519",
        "--key-types",
        help="Comma-separated key types (RSA,Ed25519,Secp256k1,ECDSA)",
    ),
    # Node removal system
    node_removal_system: str = typer.Option(
        "default", "--removal-system", help="Node removal system type"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Register a new subnet with comprehensive guidance based on official specification."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel

        guidance_panel = Panel(
            f"[bold cyan]🏗️ Subnet Registration Guide[/bold cyan]\n\n"
            f"This will register a new subnet on the Hypertensor network:\n\n"
            f"[bold]Subnet Details:[/bold]\n"
            f"• Name: {name}\n"
            f"• Repository: {repo}\n"
            f"• Description: {description}\n\n"
            f"[bold]Stake Configuration:[/bold]\n"
            f"• Min Stake: {min_stake} TENSOR\n"
            f"• Max Stake: {max_stake} TENSOR\n"
            f"• Delegate Percentage: {delegate_stake_percentage}%\n\n"
            f"[bold]Timing Configuration:[/bold]\n"
            f"• Churn Limit: {churn_limit} activations/epoch\n"
            f"• Queue Epochs: {registration_queue_epochs}\n"
            f"• Grace Epochs: {activation_grace_epochs}\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Registration fee is non-refundable\n"
            f"• Registration period lasts 1 week\n"
            f"• Initial coldkeys can register nodes during registration phase\n"
            f"• Subnet becomes decentralized after activation",
            title="[bold yellow]🔐 Subnet Registration[/bold yellow]",
            border_style="yellow",
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm("Do you want to proceed with subnet registration?"):
            print_info("Subnet registration cancelled.")
            return

    try:
        # Parse initial coldkeys if provided
        coldkeys = []
        if initial_coldkeys:
            coldkeys = [addr.strip() for addr in initial_coldkeys.split(",")]

        # Parse key types
        key_types_list = [kt.strip() for kt in key_types.split(",")]

        # Validate all inputs
        if not validate_subnet_name(name):
            print_error(
                "❌ Invalid subnet name. Use alphanumeric characters, hyphens, underscores, and spaces only."
            )
            raise typer.Exit(1)

        if not validate_repo_url(repo):
            print_error("❌ Invalid repository URL. Must be a valid HTTP/HTTPS URL.")
            raise typer.Exit(1)

        if not validate_subnet_description(description):
            print_error(
                "❌ Invalid description. Must be between 10 and 1000 characters."
            )
            raise typer.Exit(1)

        if not validate_stake_amount(min_stake):
            print_error(
                "❌ Invalid minimum stake amount. Must be positive and reasonable."
            )
            raise typer.Exit(1)

        if not validate_stake_amount(max_stake):
            print_error(
                "❌ Invalid maximum stake amount. Must be positive and reasonable."
            )
            raise typer.Exit(1)

        if min_stake >= max_stake:
            print_error("❌ Maximum stake must be greater than minimum stake.")
            raise typer.Exit(1)

        if not validate_delegate_percentage(delegate_stake_percentage):
            print_error("❌ Invalid delegate percentage. Must be between 0 and 100.")
            raise typer.Exit(1)

        if not validate_churn_limit(churn_limit):
            print_error("❌ Invalid churn limit. Must be between 1 and 1000.")
            raise typer.Exit(1)

        if not validate_epoch_value(registration_queue_epochs):
            print_error(
                "❌ Invalid registration queue epochs. Must be between 0 and 1,000,000."
            )
            raise typer.Exit(1)

        if not validate_epoch_value(activation_grace_epochs):
            print_error(
                "❌ Invalid activation grace epochs. Must be between 0 and 1,000,000."
            )
            raise typer.Exit(1)

        if not validate_epoch_value(queue_classification_epochs):
            print_error(
                "❌ Invalid queue classification epochs. Must be between 0 and 1,000,000."
            )
            raise typer.Exit(1)

        if not validate_epoch_value(included_classification_epochs):
            print_error(
                "❌ Invalid included classification epochs. Must be between 0 and 1,000,000."
            )
            raise typer.Exit(1)

        if not validate_max_penalties(max_node_penalties):
            print_error("❌ Invalid max node penalties. Must be between 1 and 100.")
            raise typer.Exit(1)

        if not validate_max_nodes(max_registered_nodes):
            print_error(
                "❌ Invalid max registered nodes. Must be between 1 and 10,000."
            )
            raise typer.Exit(1)

        if not validate_key_types(key_types_list):
            print_error(
                "❌ Invalid key types. Supported: RSA, Ed25519, Secp256k1, ECDSA."
            )
            raise typer.Exit(1)

        if not validate_coldkey_addresses(coldkeys):
            print_error("❌ Invalid coldkey addresses. Must be valid SS58 addresses.")
            raise typer.Exit(1)

        request = SubnetRegisterRequest(
            name=name,
            repo=repo,
            description=description,
            misc=misc,
            min_stake=min_stake,
            max_stake=max_stake,
            delegate_stake_percentage=delegate_stake_percentage,
            churn_limit=churn_limit,
            registration_queue_epochs=registration_queue_epochs,
            activation_grace_epochs=activation_grace_epochs,
            queue_classification_epochs=queue_classification_epochs,
            included_classification_epochs=included_classification_epochs,
            max_node_penalties=max_node_penalties,
            max_registered_nodes=max_registered_nodes,
            initial_coldkeys=coldkeys,
            key_types=key_types_list,
            node_removal_system=node_removal_system,
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
    subnet_id: int = typer.Option(
        ..., "--subnet-id", "-s", help="Subnet ID to activate"
    ),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Activate a registered subnet with comprehensive guidance based on official specification."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel

        guidance_panel = Panel(
            f"[bold cyan]🚀 Subnet Activation Guide[/bold cyan]\n\n"
            f"This will activate subnet {subnet_id} on the Hypertensor network:\n\n"
            f"[bold]Requirements for Activation:[/bold]\n"
            f"• Must have minimum required subnet nodes (MinSubnetNodes)\n"
            f"• Must have floating minimum delegate stake balance\n"
            f"• Must meet MinSubnetDelegateStakeFactor percentage of total supply\n"
            f"• Owner must sign the activation transaction\n\n"
            f"[bold]What Happens After Activation:[/bold]\n"
            f"• Subnet gets an open slot for rewards distribution\n"
            f"• Initial coldkeys list is removed\n"
            f"• Anyone can register nodes (decentralized)\n"
            f"• Subnet starts earning and distributing rewards\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Only the subnet owner can activate\n"
            f"• If requirements aren't met, subnet is deactivated and removed\n"
            f"• Delegate stake balance must be maintained each epoch",
            title="[bold yellow]🔐 Subnet Activation[/bold yellow]",
            border_style="yellow",
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm("Do you want to proceed with subnet activation?"):
            print_info("Subnet activation cancelled.")
            return

    try:
        # Check if key_name is provided (required for owner activation)
        if not key_name:
            print_error(
                "❌ Key name is required for subnet activation. Use --key-name to specify your signing key."
            )
            raise typer.Exit(1)

        # Get subnet info to check ownership and requirements
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(
                f"❌ Failed to get subnet information: {subnet_response.message}"
            )
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get("exists", False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check if subnet is already activated
        if subnet_info.get("activated", False):
            print_error(f"❌ Subnet {subnet_id} is already activated.")
            raise typer.Exit(1)

        # Check ownership (user must be the owner to activate)
        from ..utils.ownership import get_user_addresses, user_owns_subnet

        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(
                f"❌ You are not the owner of subnet {subnet_id}. Only the owner can activate a subnet."
            )
            raise typer.Exit(1)

        print_info(f"🔄 Activating subnet {subnet_id}...")
        print_info(f"📋 Checking activation requirements...")

        # Check activation requirements
        requirements = client.check_subnet_activation_requirements(subnet_id)
        
        # Display requirements status
        if requirements["errors"]:
            console.print(Panel(
                f"[bold red]❌ Activation Requirements Not Met[/bold red]\n\n"
                f"The following requirements must be met before activation:\n\n"
                f"{chr(10).join([f'• [red]{error}[/red]' for error in requirements['errors']])}\n\n"
                f"[yellow]📋 Required Actions:[/yellow]\n"
                f"• Address all requirements above\n"
                f"• Ensure subnet is in registration phase\n"
                f"• Meet minimum node and stake requirements\n"
                f"• Check network consensus status\n\n"
                f"[yellow]💡 Tip:[/yellow]\n"
                f"• Use 'htcli subnet info --subnet-id {subnet_id}' to check current status\n"
                f"• Add more nodes or delegate stake as needed\n"
                f"• Wait for network consensus to be ready",
                title="Activation Requirements Failed",
                border_style="red"
            ))
            raise typer.Exit(1)
        
        if requirements["warnings"]:
            console.print(Panel(
                f"[bold yellow]⚠️ Activation Warnings[/bold yellow]\n\n"
                f"The following warnings were found:\n\n"
                f"{chr(10).join([f'• [yellow]{warning}[/yellow]' for warning in requirements['warnings']])}\n\n"
                f"[yellow]📋 Recommendations:[/yellow]\n"
                f"• Consider addressing warnings for better stability\n"
                f"• Activation can proceed but may not be optimal\n"
                f"• Monitor subnet performance after activation\n\n"
                f"[yellow]💡 Tip:[/yellow]\n"
                f"• Add more nodes for better stability\n"
                f"• Increase delegate stake for better performance\n"
                f"• Monitor network conditions",
                title="Activation Warnings",
                border_style="yellow"
            ))

        # Show requirements summary
        details = requirements["details"]
        console.print(Panel(
            f"[bold green]✅ Activation Requirements Met[/bold green]\n\n"
            f"[bold]Requirements Summary:[/bold]\n"
            f"• [green]Minimum Nodes[/green]: {details.get('min_nodes', 'N/A')} (Current: {details.get('current_nodes', 'N/A')})\n"
            f"• [green]Minimum Delegate Stake[/green]: {format_balance(details.get('min_delegate_stake', 0))} (Current: {format_balance(details.get('current_delegate_stake', 0))})\n"
            f"• [green]Initial Coldkeys[/green]: {details.get('initial_coldkeys', 0)}\n"
            f"• [green]Stake Factor[/green]: {'✅ Met' if details.get('stake_factor', {}).get('met', False) else '❌ Not Met'}\n"
            f"• [green]Network Consensus[/green]: {'✅ Ready' if details.get('consensus', {}).get('met', False) else '❌ Not Ready'}\n\n"
            f"[yellow]💡 Proceeding with activation...[/yellow]",
            title="Requirements Check Passed",
            border_style="green"
        ))

        response = client.activate_subnet(subnet_id, key_name=key_name)

        if response.success:
            print_success(f"✅ Subnet {subnet_id} activated successfully!")
            console.print(
                f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]"
            )
            if response.block_number:
                console.print(
                    f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]"
                )

            console.print(Panel(
                f"[bold green]🚀 Subnet Activation Complete![/bold green]\n\n"
                f"Subnet {subnet_id} is now active and:\n"
                f"• Has an open slot for rewards distribution\n"
                f"• Initial coldkeys have been removed\n"
                f"• Anyone can now register nodes\n"
                f"• Subnet is earning and distributing rewards\n\n"
                f"[yellow]📊 Monitor your subnet:[/yellow]\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Activation Success",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to activate subnet: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to activate subnet: {str(e)}")
        raise typer.Exit(1)


@app.command()
def list(
    format_type: str = typer.Option(
        "table", "--format", "-f", help="Output format (table/json)"
    )
):
    """List subnets. Use --mine flag globally to show only your subnets."""
    client = get_client()

    # Check if --mine filter is enabled globally
    config = client.config
    filter_mine = getattr(config.filter, "mine", False)

    try:
        response = client.get_subnets_data()
        if response.success:
            subnets = response.data.get("subnets", [])
            original_count = len(subnets)

            # Apply --mine filtering if enabled
            if filter_mine:
                user_addresses = require_user_keys()

                # Enhance subnets with ownership information
                enhanced_subnets = []
                for subnet in subnets:
                    subnet_id = subnet.get("subnet_id")
                    if subnet_id:
                        # Get detailed subnet data to check ownership
                        detail_response = client.get_subnet_data(subnet_id)
                        if detail_response.success:
                            subnet_detail = detail_response.data
                            # Check if user owns this subnet
                            if user_owns_subnet(subnet_detail, user_addresses):
                                enhanced_subnets.append(
                                    {
                                        **subnet,
                                        "owner": subnet_detail.get("owner", ""),
                                        "is_mine": True,
                                    }
                                )

                subnets = enhanced_subnets
                show_mine_filter_info(user_addresses, len(subnets), original_count)

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
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    format_type: str = typer.Option(
        "table", "--format", "-f", help="Output format (table/json)"
    ),
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
def pause(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID to pause"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Pause an active subnet with comprehensive guidance based on official specification."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel

        guidance_panel = Panel(
            f"[bold cyan]⏸️ Subnet Pause Guide[/bold cyan]\n\n"
            f"This will pause subnet {subnet_id} on the Hypertensor network:\n\n"
            f"[bold]What Happens When Paused:[/bold]\n"
            f"• All subnet functionality is paused on-chain\n"
            f"• Validator election stops\n"
            f"• Emissions distribution stops\n"
            f"• Subnet becomes inactive temporarily\n\n"
            f"[bold]Important Limitations:[/bold]\n"
            f"• Maximum pause duration: 4 days\n"
            f"• Only subnet owner can pause\n"
            f"• Penalties increase each epoch if not unpaused\n"
            f"• Subnet will be removed if max penalties reached\n\n"
            f"[yellow]⚠️ Warning:[/yellow]\n"
            f"• Pausing affects all subnet operations\n"
            f"• Stakeholders may lose rewards during pause\n"
            f"• Plan pause duration carefully",
            title="[bold yellow]⏸️ Subnet Pause[/bold yellow]",
            border_style="yellow",
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm("Do you want to proceed with pausing the subnet?"):
            print_info("Subnet pause cancelled.")
            return

    try:
        # Check if key_name is provided (required for owner operations)
        if not key_name:
            print_error(
                "❌ Key name is required for subnet pause. Use --key-name to specify your signing key."
            )
            raise typer.Exit(1)

        # Get subnet info to check ownership and status
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(
                f"❌ Failed to get subnet information: {subnet_response.message}"
            )
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get("exists", False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check if subnet is active (can only pause active subnets)
        if not subnet_info.get("activated", False):
            print_error(
                f"❌ Subnet {subnet_id} is not active. Only active subnets can be paused."
            )
            raise typer.Exit(1)

        # Check if subnet is already paused
        if subnet_info.get("paused", False):
            print_error(f"❌ Subnet {subnet_id} is already paused.")
            raise typer.Exit(1)

        # Check ownership (user must be the owner to pause)
        from ..utils.ownership import get_user_addresses, user_owns_subnet

        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(
                f"❌ You are not the owner of subnet {subnet_id}. Only the owner can pause a subnet."
            )
            raise typer.Exit(1)

        print_info(f"⏸️ Pausing subnet {subnet_id}...")

        response = client.pause_subnet(subnet_id, key_name=key_name)

        if response.success:
            print_success(f"✅ Subnet {subnet_id} paused successfully!")
            console.print(
                f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]"
            )
            if response.block_number:
                console.print(
                    f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]"
                )

            console.print(Panel(
                f"[bold yellow]⏸️ Subnet Paused Successfully![/bold yellow]\n\n"
                f"Subnet {subnet_id} is now paused and:\n"
                f"• All functionality is suspended\n"
                f"• Validator election stopped\n"
                f"• Emissions distribution paused\n"
                f"• Penalties will increase if not unpaused\n\n"
                f"[yellow]📊 Monitor your subnet:[/yellow]\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]\n\n"
                f"[yellow]🔄 To unpause:[/yellow]\n"
                f"Use: [bold]htcli subnet unpause --subnet-id {subnet_id} --key-name {key_name}[/bold]",
                title="Pause Success",
                border_style="yellow"
            ))
        else:
            print_error(f"❌ Failed to pause subnet: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to pause subnet: {str(e)}")
        raise typer.Exit(1)


@app.command()
def unpause(
    subnet_id: int = typer.Option(
        ..., "--subnet-id", "-s", help="Subnet ID to unpause"
    ),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Unpause a paused subnet with comprehensive guidance based on official specification."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel

        guidance_panel = Panel(
            f"[bold cyan]▶️ Subnet Unpause Guide[/bold cyan]\n\n"
            f"This will unpause subnet {subnet_id} on the Hypertensor network:\n\n"
            f"[bold]What Happens When Unpaused:[/bold]\n"
            f"• Subnet resumes consensus on next epoch\n"
            f"• Validator election resumes\n"
            f"• Emissions distribution resumes\n"
            f"• Registered nodes are pushed back in queue\n"
            f"• Idle nodes are not affected\n\n"
            f"[bold]Queue Impact:[/bold]\n"
            f"• Registered nodes: pushed back by pause duration\n"
            f"• Idle nodes: no change to queue position\n"
            f"• New consensus begins immediately\n\n"
            f"[yellow]✅ Benefits:[/yellow]\n"
            f"• Stops penalty accumulation\n"
            f"• Resumes normal operations\n"
            f"• Stakeholders can earn rewards again",
            title="[bold green]▶️ Subnet Unpause[/bold green]",
            border_style="green",
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm("Do you want to proceed with unpausing the subnet?"):
            print_info("Subnet unpause cancelled.")
            return

    try:
        # Check if key_name is provided (required for owner operations)
        if not key_name:
            print_error(
                "❌ Key name is required for subnet unpause. Use --key-name to specify your signing key."
            )
            raise typer.Exit(1)

        # Get subnet info to check ownership and status
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(
                f"❌ Failed to get subnet information: {subnet_response.message}"
            )
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get("exists", False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check if subnet is paused (can only unpause paused subnets)
        if not subnet_info.get("paused", False):
            print_error(
                f"❌ Subnet {subnet_id} is not paused. Only paused subnets can be unpaused."
            )
            raise typer.Exit(1)

        # Check ownership (user must be the owner to unpause)
        from ..utils.ownership import get_user_addresses, user_owns_subnet

        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(
                f"❌ You are not the owner of subnet {subnet_id}. Only the owner can unpause a subnet."
            )
            raise typer.Exit(1)

        print_info(f"▶️ Unpausing subnet {subnet_id}...")

        response = client.unpause_subnet(subnet_id, key_name=key_name)

        if response.success:
            print_success(f"✅ Subnet {subnet_id} unpaused successfully!")
            console.print(
                f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]"
            )
            if response.block_number:
                console.print(
                    f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]"
                )

            console.print(Panel(
                f"[bold green]▶️ Subnet Unpaused Successfully![/bold green]\n\n"
                f"Subnet {subnet_id} is now active and:\n"
                f"• Consensus resumes on next epoch\n"
                f"• Validator election active\n"
                f"• Emissions distribution resumed\n"
                f"• Registered nodes pushed back in queue\n"
                f"• Idle nodes unaffected\n\n"
                f"[yellow]📊 Monitor your subnet:[/yellow]\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Unpause Success",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to unpause subnet: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to unpause subnet: {str(e)}")
        raise typer.Exit(1)


@app.command()
def remove(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID to remove"),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Remove a subnet with comprehensive guidance."""
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


# ============================================================================
# SUBNET OWNER OPERATIONS
# ============================================================================

@app.command()
def owner_update_name(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    name: str = typer.Option(..., "--name", "-n", help="New subnet name"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Update the unique name of a subnet (owner only)."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]📝 Update Subnet Name Guide[/bold cyan]\n\n"
            f"This will update the name of subnet {subnet_id} to '{name}':\n\n"
            f"[bold]What This Does:[/bold]\n"
            f"• Changes the unique name of your subnet\n"
            f"• Updates the on-chain subnet information\n"
            f"• Affects how your subnet appears in listings\n"
            f"• Requires owner authentication\n\n"
            f"[bold]Requirements:[/bold]\n"
            f"• You must be the subnet owner\n"
            f"• Name must be unique across all subnets\n"
            f"• Valid signing key required\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• This is a permanent change\n"
            f"• Name changes affect subnet discoverability\n"
            f"• Consider the impact on your subnet's branding",
            title="[bold blue]📝 Update Subnet Name[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Update subnet {subnet_id} name to '{name}'?"):
            print_info("Subnet name update cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_subnet_name(name):
        print_error("❌ Invalid subnet name.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for owner operations)
    if not key_name:
        print_error("❌ Key name is required for subnet owner operations. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        # Check ownership (user must be the owner to update)
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(f"❌ Failed to get subnet information: {subnet_response.message}")
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get('exists', False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check ownership (user must be the owner to update)
        from ..utils.ownership import get_user_addresses, user_owns_subnet
        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(f"❌ You are not the owner of subnet {subnet_id}. Only the owner can update subnet information.")
            raise typer.Exit(1)

        print_info(f"📝 Updating subnet {subnet_id} name to '{name}'...")

        response = client.owner_update_name(subnet_id, name, key_name=key_name)

        if response.success:
            print_success(f"✅ Subnet {subnet_id} name updated to '{name}' successfully!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]📝 Name Update Complete![/bold green]\n\n"
                f"Subnet {subnet_id} is now named '{name}'.\n"
                f"• On-chain information updated\n"
                f"• Subnet discoverability improved\n"
                f"• Branding updated successfully\n\n"
                f"[yellow]📊 Verify Changes:[/yellow]\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Name Update Success",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to update subnet name: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to update subnet name: {str(e)}")
        raise typer.Exit(1)


@app.command()
def owner_update_repo(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    repo: str = typer.Option(..., "--repo", "-r", help="New repository URL"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Update the repository URL of a subnet (owner only)."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]🔗 Update Subnet Repository Guide[/bold cyan]\n\n"
            f"This will update the repository URL of subnet {subnet_id} to '{repo}':\n\n"
            f"[bold]What This Does:[/bold]\n"
            f"• Updates the open-source code repository link\n"
            f"• Changes where users can find your subnet's source code\n"
            f"• Updates the on-chain subnet information\n"
            f"• Requires owner authentication\n\n"
            f"[bold]Requirements:[/bold]\n"
            f"• You must be the subnet owner\n"
            f"• Repository URL must be valid and accessible\n"
            f"• Valid signing key required\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• This affects code discoverability\n"
            f"• Ensure the repository is public and accessible\n"
            f"• Consider the impact on developer adoption",
            title="[bold blue]🔗 Update Subnet Repository[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Update subnet {subnet_id} repository to '{repo}'?"):
            print_info("Subnet repository update cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_repo_url(repo):
        print_error("❌ Invalid repository URL.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for owner operations)
    if not key_name:
        print_error("❌ Key name is required for subnet owner operations. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        # Check ownership (user must be the owner to update)
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(f"❌ Failed to get subnet information: {subnet_response.message}")
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get('exists', False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check ownership (user must be the owner to update)
        from ..utils.ownership import get_user_addresses, user_owns_subnet
        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(f"❌ You are not the owner of subnet {subnet_id}. Only the owner can update subnet information.")
            raise typer.Exit(1)

        print_info(f"🔗 Updating subnet {subnet_id} repository to '{repo}'...")

        response = client.owner_update_repo(subnet_id, repo, key_name=key_name)

        if response.success:
            print_success(f"✅ Subnet {subnet_id} repository updated to '{repo}' successfully!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]🔗 Repository Update Complete![/bold green]\n\n"
                f"Subnet {subnet_id} repository is now '{repo}'.\n"
                f"• Source code location updated\n"
                f"• Developer accessibility improved\n"
                f"• On-chain information updated\n\n"
                f"[yellow]📊 Verify Changes:[/yellow]\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Repository Update Success",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to update subnet repository: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to update subnet repository: {str(e)}")
        raise typer.Exit(1)


@app.command()
def owner_update_description(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    description: str = typer.Option(..., "--description", "-d", help="New subnet description"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Update the description of a subnet (owner only)."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]📄 Update Subnet Description Guide[/bold cyan]\n\n"
            f"This will update the description of subnet {subnet_id}:\n\n"
            f"[bold]What This Does:[/bold]\n"
            f"• Updates the subnet's description\n"
            f"• Changes how your subnet is presented to users\n"
            f"• Updates the on-chain subnet information\n"
            f"• Requires owner authentication\n\n"
            f"[bold]Requirements:[/bold]\n"
            f"• You must be the subnet owner\n"
            f"• Description should be clear and informative\n"
            f"• Valid signing key required\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• This affects user understanding of your subnet\n"
            f"• Make the description clear and compelling\n"
            f"• Consider the impact on adoption",
            title="[bold blue]📄 Update Subnet Description[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Update subnet {subnet_id} description?"):
            print_info("Subnet description update cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_subnet_description(description):
        print_error("❌ Invalid subnet description.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for owner operations)
    if not key_name:
        print_error("❌ Key name is required for subnet owner operations. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        # Check ownership (user must be the owner to update)
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(f"❌ Failed to get subnet information: {subnet_response.message}")
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get('exists', False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check ownership (user must be the owner to update)
        from ..utils.ownership import get_user_addresses, user_owns_subnet
        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(f"❌ You are not the owner of subnet {subnet_id}. Only the owner can update subnet information.")
            raise typer.Exit(1)

        print_info(f"📄 Updating subnet {subnet_id} description...")

        response = client.owner_update_description(subnet_id, description, key_name=key_name)

        if response.success:
            print_success(f"✅ Subnet {subnet_id} description updated successfully!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]📄 Description Update Complete![/bold green]\n\n"
                f"Subnet {subnet_id} description has been updated.\n"
                f"• On-chain information updated\n"
                f"• User understanding improved\n"
                f"• Subnet presentation enhanced\n\n"
                f"[yellow]📊 Verify Changes:[/yellow]\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Description Update Success",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to update subnet description: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to update subnet description: {str(e)}")
        raise typer.Exit(1)


@app.command()
def owner_transfer_ownership(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    new_owner: str = typer.Option(..., "--new-owner", "-o", help="New owner account address"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Transfer subnet ownership to another account (owner only)."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]👑 Transfer Subnet Ownership Guide[/bold cyan]\n\n"
            f"This will transfer ownership of subnet {subnet_id} to {new_owner}:\n\n"
            f"[bold]What This Does:[/bold]\n"
            f"• Initiates a two-step ownership transfer process\n"
            f"• New owner must accept the transfer\n"
            f"• You retain ownership until transfer is accepted\n"
            f"• Can be undone before acceptance\n\n"
            f"[bold]Two-Step Process:[/bold]\n"
            f"1. You initiate transfer (this command)\n"
            f"2. New owner accepts transfer\n"
            f"3. Ownership officially transfers\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• This is a major operation\n"
            f"• New owner will have full control\n"
            f"• You can undo before acceptance\n"
            f"• Verify the new owner address carefully",
            title="[bold red]👑 Transfer Subnet Ownership[/bold red]",
            border_style="red"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Transfer ownership of subnet {subnet_id} to {new_owner}?"):
            print_info("Subnet ownership transfer cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_address(new_owner):
        print_error("❌ Invalid new owner address.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for owner operations)
    if not key_name:
        print_error("❌ Key name is required for subnet owner operations. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        # Check ownership (user must be the owner to transfer)
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(f"❌ Failed to get subnet information: {subnet_response.message}")
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get('exists', False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check ownership (user must be the owner to transfer)
        from ..utils.ownership import get_user_addresses, user_owns_subnet
        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(f"❌ You are not the owner of subnet {subnet_id}. Only the owner can transfer ownership.")
            raise typer.Exit(1)

        print_info(f"👑 Initiating ownership transfer of subnet {subnet_id} to {new_owner}...")

        response = client.transfer_subnet_ownership(subnet_id, new_owner, key_name=key_name)

        if response.success:
            print_success(f"✅ Ownership transfer initiated for subnet {subnet_id}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold yellow]👑 Ownership Transfer Initiated![/bold yellow]\n\n"
                f"Subnet {subnet_id} ownership transfer to {new_owner}:\n"
                f"• Transfer initiated successfully\n"
                f"• New owner must accept the transfer\n"
                f"• You retain ownership until acceptance\n"
                f"• Can be undone before acceptance\n\n"
                f"[yellow]📋 Next Steps:[/yellow]\n"
                f"• New owner runs: [bold]htcli subnet owner-accept-ownership --subnet-id {subnet_id}[/bold]\n"
                f"• To undo: [bold]htcli subnet owner-undo-transfer --subnet-id {subnet_id}[/bold]\n"
                f"• Monitor: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Transfer Initiated",
                border_style="yellow"
            ))
        else:
            print_error(f"❌ Failed to initiate ownership transfer: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to initiate ownership transfer: {str(e)}")
        raise typer.Exit(1)


@app.command()
def owner_accept_ownership(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for new owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Accept subnet ownership transfer (new owner only)."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]👑 Accept Subnet Ownership Guide[/bold cyan]\n\n"
            f"This will accept ownership of subnet {subnet_id}:\n\n"
            f"[bold]What This Does:[/bold]\n"
            f"• Accepts a pending ownership transfer\n"
            f"• Makes you the official subnet owner\n"
            f"• Gives you full control over the subnet\n"
            f"• Entitles you to 24% of subnet emissions\n\n"
            f"[bold]Requirements:[/bold]\n"
            f"• You must be the designated new owner\n"
            f"• Transfer must be pending (not accepted yet)\n"
            f"• Valid signing key required\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• This is irreversible once accepted\n"
            f"• You become responsible for the subnet\n"
            f"• You gain 24% of subnet emissions\n"
            f"• Previous owner loses all control",
            title="[bold green]👑 Accept Subnet Ownership[/bold green]",
            border_style="green"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Accept ownership of subnet {subnet_id}?"):
            print_info("Subnet ownership acceptance cancelled.")
            return

    # Check if key_name is provided (required for owner operations)
    if not key_name:
        print_error("❌ Key name is required for subnet ownership operations. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        print_info(f"👑 Accepting ownership of subnet {subnet_id}...")

        response = client.accept_subnet_ownership(subnet_id, key_name=key_name)

        if response.success:
            print_success(f"✅ Successfully accepted ownership of subnet {subnet_id}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]👑 Ownership Accepted![/bold green]\n\n"
                f"You are now the owner of subnet {subnet_id}.\n"
                f"• Full control over subnet operations\n"
                f"• 24% of subnet emissions\n"
                f"• All owner privileges activated\n"
                f"• Previous owner no longer has control\n\n"
                f"[yellow]🎯 Your New Capabilities:[/yellow]\n"
                f"• Activate/pause subnet\n"
                f"• Update subnet information\n"
                f"• Manage nodes and policies\n"
                f"• Transfer ownership to others\n\n"
                f"[yellow]📊 Monitor Your Subnet:[/yellow]\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Ownership Transfer Complete",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to accept ownership: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to accept ownership: {str(e)}")
        raise typer.Exit(1)


@app.command()
def owner_undo_transfer(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for current owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Undo a pending ownership transfer (current owner only)."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]🔄 Undo Ownership Transfer Guide[/bold cyan]\n\n"
            f"This will undo the pending ownership transfer for subnet {subnet_id}:\n\n"
            f"[bold]What This Does:[/bold]\n"
            f"• Cancels a pending ownership transfer\n"
            f"• Keeps you as the subnet owner\n"
            f"• Prevents the new owner from accepting\n"
            f"• Maintains your current control\n\n"
            f"[bold]Requirements:[/bold]\n"
            f"• You must be the current owner\n"
            f"• Transfer must be pending (not accepted)\n"
            f"• Valid signing key required\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• This cancels the transfer completely\n"
            f"• New owner cannot accept after this\n"
            f"• You retain full ownership\n"
            f"• Can initiate new transfer if needed",
            title="[bold yellow]🔄 Undo Ownership Transfer[/bold yellow]",
            border_style="yellow"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Undo ownership transfer for subnet {subnet_id}?"):
            print_info("Ownership transfer undo cancelled.")
            return

    # Check if key_name is provided (required for owner operations)
    if not key_name:
        print_error("❌ Key name is required for subnet ownership operations. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        print_info(f"🔄 Undoing ownership transfer for subnet {subnet_id}...")

        response = client.undo_subnet_ownership_transfer(subnet_id, key_name=key_name)

        if response.success:
            print_success(f"✅ Successfully undone ownership transfer for subnet {subnet_id}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold yellow]🔄 Transfer Undone![/bold yellow]\n\n"
                f"Ownership transfer for subnet {subnet_id} has been cancelled.\n"
                f"• You remain the subnet owner\n"
                f"• Transfer is completely cancelled\n"
                f"• New owner cannot accept\n"
                f"• Full control maintained\n\n"
                f"[yellow]📊 Verify Status:[/yellow]\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Transfer Undone",
                border_style="yellow"
            ))
        else:
            print_error(f"❌ Failed to undo ownership transfer: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to undo ownership transfer: {str(e)}")
        raise typer.Exit(1)


@app.command()
def owner_remove_node(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    node_id: int = typer.Option(..., "--node-id", "-n", help="Node ID to remove"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Remove a subnet node (owner only)."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]🗑️ Remove Subnet Node Guide[/bold cyan]\n\n"
            f"This will remove node {node_id} from subnet {subnet_id}:\n\n"
            f"[bold]What This Does:[/bold]\n"
            f"• Removes the node from the subnet\n"
            f"• Node loses validator status\n"
            f"• Node stops earning rewards\n"
            f"• Subnet capacity reduced\n\n"
            f"[bold]Requirements:[/bold]\n"
            f"• You must be the subnet owner\n"
            f"• Node must exist in the subnet\n"
            f"• Valid signing key required\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• This affects subnet performance\n"
            f"• Node operator loses income\n"
            f"• Consider impact on consensus\n"
            f"• Ensure minimum node requirements",
            title="[bold red]🗑️ Remove Subnet Node[/bold red]",
            border_style="red"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Remove node {node_id} from subnet {subnet_id}?"):
            print_info("Node removal cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_node_id(node_id):
        print_error("❌ Invalid node ID. Must be a positive integer.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for owner operations)
    if not key_name:
        print_error("❌ Key name is required for subnet owner operations. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        # Check ownership (user must be the owner to remove nodes)
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(f"❌ Failed to get subnet information: {subnet_response.message}")
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get('exists', False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check ownership (user must be the owner to remove nodes)
        from ..utils.ownership import get_user_addresses, user_owns_subnet
        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(f"❌ You are not the owner of subnet {subnet_id}. Only the owner can remove nodes.")
            raise typer.Exit(1)

        print_info(f"🗑️ Removing node {node_id} from subnet {subnet_id}...")

        response = client.owner_remove_subnet_node(subnet_id, node_id, key_name=key_name)

        if response.success:
            print_success(f"✅ Successfully removed node {node_id} from subnet {subnet_id}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold red]🗑️ Node Removed![/bold red]\n\n"
                f"Node {node_id} has been removed from subnet {subnet_id}.\n"
                f"• Node is no longer a validator\n"
                f"• Node stops earning rewards\n"
                f"• Subnet capacity reduced\n"
                f"• Node operator notified\n\n"
                f"[yellow]📊 Monitor Impact:[/yellow]\n"
                f"• Check subnet performance\n"
                f"• Monitor consensus stability\n"
                f"• Consider adding new nodes\n\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Node Removal Complete",
                border_style="red"
            ))
        else:
            print_error(f"❌ Failed to remove node: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to remove node: {str(e)}")
        raise typer.Exit(1)


@app.command()
def owner_update_churn_limit(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    churn_limit: int = typer.Option(..., "--churn-limit", "-c", help="New churn limit"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Update the churn limit for a subnet (owner only)."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]⚙️ Update Churn Limit Guide[/bold cyan]\n\n"
            f"This will update the churn limit for subnet {subnet_id} to {churn_limit}:\n\n"
            f"[bold]What is Churn Limit:[/bold]\n"
            f"• Number of nodes that can activate per epoch\n"
            f"• Controls how quickly nodes join the subnet\n"
            f"• Affects node activation timing\n"
            f"• Balances growth with stability\n\n"
            f"[bold]Impact:[/bold]\n"
            f"• Higher limit = faster node onboarding\n"
            f"• Lower limit = more controlled growth\n"
            f"• Affects queue processing speed\n"
            f"• Influences subnet expansion rate\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Consider current queue size\n"
            f"• Balance growth with stability\n"
            f"• Monitor activation patterns\n"
            f"• Ensure adequate capacity",
            title="[bold blue]⚙️ Update Churn Limit[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Update churn limit for subnet {subnet_id} to {churn_limit}?"):
            print_info("Churn limit update cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_churn_limit(churn_limit):
        print_error("❌ Invalid churn limit. Must be a positive integer.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for owner operations)
    if not key_name:
        print_error("❌ Key name is required for subnet owner operations. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        # Check ownership (user must be the owner to update parameters)
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(f"❌ Failed to get subnet information: {subnet_response.message}")
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get('exists', False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check ownership (user must be the owner to update parameters)
        from ..utils.ownership import get_user_addresses, user_owns_subnet
        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(f"❌ You are not the owner of subnet {subnet_id}. Only the owner can update parameters.")
            raise typer.Exit(1)

        print_info(f"⚙️ Updating churn limit for subnet {subnet_id} to {churn_limit}...")

        response = client.owner_update_churn_limit(subnet_id, churn_limit, key_name=key_name)

        if response.success:
            print_success(f"✅ Successfully updated churn limit for subnet {subnet_id} to {churn_limit}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]⚙️ Churn Limit Updated![/bold green]\n\n"
                f"Subnet {subnet_id} churn limit is now {churn_limit}.\n"
                f"• {churn_limit} nodes can activate per epoch\n"
                f"• Queue processing speed adjusted\n"
                f"• Node onboarding rate changed\n"
                f"• Growth pattern modified\n\n"
                f"[yellow]📊 Monitor Impact:[/yellow]\n"
                f"• Watch queue processing speed\n"
                f"• Monitor node activation patterns\n"
                f"• Check subnet growth rate\n\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Churn Limit Update Complete",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to update churn limit: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to update churn limit: {str(e)}")
        raise typer.Exit(1)


@app.command()
def owner_update_min_stake(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    min_stake: int = typer.Option(..., "--min-stake", "-m", help="New minimum stake amount"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Update the minimum stake requirement for a subnet (owner only)."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]💰 Update Minimum Stake Guide[/bold cyan]\n\n"
            f"This will update the minimum stake for subnet {subnet_id} to {format_balance(min_stake)}:\n\n"
            f"[bold]What is Minimum Stake:[/bold]\n"
            f"• Minimum balance required for nodes to register\n"
            f"• Affects node registration requirements\n"
            f"• Can force existing nodes to be removed\n"
            f"• Balances are checked during operations\n\n"
            f"[bold]Impact:[/bold]\n"
            f"• Higher minimum = more expensive to join\n"
            f"• Lower minimum = easier to join\n"
            f"• Existing nodes may be affected\n"
            f"• Influences subnet quality\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• This can force nodes to be removed!\n"
            f"• Consider impact on existing nodes\n"
            f"• Balance is checked during:\n"
            f"  - Registering\n"
            f"  - Activating\n"
            f"  - Validating\n"
            f"  - Attesting",
            title="[bold red]💰 Update Minimum Stake[/bold red]",
            border_style="red"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Update minimum stake for subnet {subnet_id} to {format_balance(min_stake)}?"):
            print_info("Minimum stake update cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_stake_amount(min_stake):
        print_error("❌ Invalid minimum stake amount.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for owner operations)
    if not key_name:
        print_error("❌ Key name is required for subnet owner operations. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        # Check ownership (user must be the owner to update parameters)
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(f"❌ Failed to get subnet information: {subnet_response.message}")
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get('exists', False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check ownership (user must be the owner to update parameters)
        from ..utils.ownership import get_user_addresses, user_owns_subnet
        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(f"❌ You are not the owner of subnet {subnet_id}. Only the owner can update parameters.")
            raise typer.Exit(1)

        print_info(f"💰 Updating minimum stake for subnet {subnet_id} to {format_balance(min_stake)}...")

        response = client.owner_update_min_stake(subnet_id, min_stake, key_name=key_name)

        if response.success:
            print_success(f"✅ Successfully updated minimum stake for subnet {subnet_id} to {format_balance(min_stake)}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]💰 Minimum Stake Updated![/bold green]\n\n"
                f"Subnet {subnet_id} minimum stake is now {format_balance(min_stake)}.\n"
                f"• New nodes must meet this requirement\n"
                f"• Existing nodes may be affected\n"
                f"• Registration requirements changed\n"
                f"• Quality threshold adjusted\n\n"
                f"[yellow]📊 Monitor Impact:[/yellow]\n"
                f"• Check if existing nodes are affected\n"
                f"• Monitor node registration patterns\n"
                f"• Watch subnet quality changes\n\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Minimum Stake Update Complete",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to update minimum stake: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to update minimum stake: {str(e)}")
        raise typer.Exit(1)


@app.command()
def owner_update_max_stake(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    max_stake: int = typer.Option(..., "--max-stake", "-m", help="New maximum stake amount"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Update the maximum stake limit for a subnet (owner only)."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]💰 Update Maximum Stake Guide[/bold cyan]\n\n"
            f"This will update the maximum stake for subnet {subnet_id} to {format_balance(max_stake)}:\n\n"
            f"[bold]What is Maximum Stake:[/bold]\n"
            f"• Maximum balance for subnet nodes to register\n"
            f"• Nodes cannot register or increase stake past this value\n"
            f"• Balances can be higher than this threshold\n"
            f"• Controls node capacity limits\n\n"
            f"[bold]Impact:[/bold]\n"
            f"• Higher maximum = more node capacity\n"
            f"• Lower maximum = restricted growth\n"
            f"• Affects node registration limits\n"
            f"• Influences subnet scalability\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• This affects node registration limits\n"
            f"• Consider current and future growth\n"
            f"• Balance scalability with stability\n"
            f"• Monitor registration patterns",
            title="[bold blue]💰 Update Maximum Stake[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Update maximum stake for subnet {subnet_id} to {format_balance(max_stake)}?"):
            print_info("Maximum stake update cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_stake_amount(max_stake):
        print_error("❌ Invalid maximum stake amount.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for owner operations)
    if not key_name:
        print_error("❌ Key name is required for subnet owner operations. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        # Check ownership (user must be the owner to update parameters)
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(f"❌ Failed to get subnet information: {subnet_response.message}")
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get('exists', False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check ownership (user must be the owner to update parameters)
        from ..utils.ownership import get_user_addresses, user_owns_subnet
        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(f"❌ You are not the owner of subnet {subnet_id}. Only the owner can update parameters.")
            raise typer.Exit(1)

        print_info(f"💰 Updating maximum stake for subnet {subnet_id} to {format_balance(max_stake)}...")

        response = client.owner_update_max_stake(subnet_id, max_stake, key_name=key_name)

        if response.success:
            print_success(f"✅ Successfully updated maximum stake for subnet {subnet_id} to {format_balance(max_stake)}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]💰 Maximum Stake Updated![/bold green]\n\n"
                f"Subnet {subnet_id} maximum stake is now {format_balance(max_stake)}.\n"
                f"• Node registration limit adjusted\n"
                f"• Growth capacity modified\n"
                f"• Scalability parameters changed\n"
                f"• Registration requirements updated\n\n"
                f"[yellow]📊 Monitor Impact:[/yellow]\n"
                f"• Watch node registration patterns\n"
                f"• Monitor growth capacity\n"
                f"• Check scalability metrics\n\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Maximum Stake Update Complete",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to update maximum stake: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to update maximum stake: {str(e)}")
        raise typer.Exit(1)


@app.command()
def owner_update_registration_epochs(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    epochs: int = typer.Option(..., "--epochs", "-e", help="New registration queue epochs"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Update registration queue epochs for a subnet (owner only)."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]⏱️ Update Registration Queue Epochs Guide[/bold cyan]\n\n"
            f"This will update the registration queue epochs for subnet {subnet_id} to {epochs}:\n\n"
            f"[bold]What are Registration Queue Epochs:[/bold]\n"
            f"• Number of epochs nodes must wait in queue before activation\n"
            f"• Controls how long nodes wait before becoming active\n"
            f"• Works with churn limit to calculate start epochs\n"
            f"• Affects node onboarding timing\n\n"
            f"[bold]Impact:[/bold]\n"
            f"• Higher epochs = longer wait time\n"
            f"• Lower epochs = faster activation\n"
            f"• Affects queue processing speed\n"
            f"• Influences subnet growth rate\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Consider current queue size\n"
            f"• Balance speed with stability\n"
            f"• Monitor activation patterns\n"
            f"• Works with churn limit",
            title="[bold blue]⏱️ Update Registration Queue Epochs[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Update registration queue epochs for subnet {subnet_id} to {epochs}?"):
            print_info("Registration queue epochs update cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_epoch_value(epochs):
        print_error("❌ Invalid epoch value. Must be a positive integer.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for owner operations)
    if not key_name:
        print_error("❌ Key name is required for subnet owner operations. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        # Check ownership (user must be the owner to update parameters)
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(f"❌ Failed to get subnet information: {subnet_response.message}")
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get('exists', False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check ownership (user must be the owner to update parameters)
        from ..utils.ownership import get_user_addresses, user_owns_subnet
        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(f"❌ You are not the owner of subnet {subnet_id}. Only the owner can update parameters.")
            raise typer.Exit(1)

        print_info(f"⏱️ Updating registration queue epochs for subnet {subnet_id} to {epochs}...")

        response = client.owner_update_registration_epochs(subnet_id, epochs, key_name=key_name)

        if response.success:
            print_success(f"✅ Successfully updated registration queue epochs for subnet {subnet_id} to {epochs}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]⏱️ Registration Queue Epochs Updated![/bold green]\n\n"
                f"Subnet {subnet_id} registration queue epochs is now {epochs}.\n"
                f"• Nodes wait {epochs} epochs before activation\n"
                f"• Queue processing timing adjusted\n"
                f"• Node onboarding rate modified\n"
                f"• Growth pattern changed\n\n"
                f"[yellow]📊 Monitor Impact:[/yellow]\n"
                f"• Watch queue processing speed\n"
                f"• Monitor node activation timing\n"
                f"• Check growth patterns\n\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Registration Epochs Update Complete",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to update registration queue epochs: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to update registration queue epochs: {str(e)}")
        raise typer.Exit(1)


@app.command()
def owner_update_activation_grace_epochs(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    epochs: int = typer.Option(..., "--epochs", "-e", help="New activation grace epochs"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Update activation grace epochs for a subnet (owner only)."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]⏱️ Update Activation Grace Epochs Guide[/bold cyan]\n\n"
            f"This will update the activation grace epochs for subnet {subnet_id} to {epochs}:\n\n"
            f"[bold]What are Activation Grace Epochs:[/bold]\n"
            f"• Grace period for nodes to activate from their start epoch\n"
            f"• Allows flexibility in activation timing\n"
            f"• Extends activation window beyond start epoch\n"
            f"• Provides buffer for node operators\n\n"
            f"[bold]Impact:[/bold]\n"
            f"• Higher epochs = more flexible activation\n"
            f"• Lower epochs = stricter timing\n"
            f"• Affects node activation success rate\n"
            f"• Influences subnet reliability\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Consider node operator needs\n"
            f"• Balance flexibility with efficiency\n"
            f"• Monitor activation success rates\n"
            f"• Works with registration epochs",
            title="[bold blue]⏱️ Update Activation Grace Epochs[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Update activation grace epochs for subnet {subnet_id} to {epochs}?"):
            print_info("Activation grace epochs update cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_epoch_value(epochs):
        print_error("❌ Invalid epoch value. Must be a positive integer.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for owner operations)
    if not key_name:
        print_error("❌ Key name is required for subnet owner operations. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        # Check ownership (user must be the owner to update parameters)
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(f"❌ Failed to get subnet information: {subnet_response.message}")
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get('exists', False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check ownership (user must be the owner to update parameters)
        from ..utils.ownership import get_user_addresses, user_owns_subnet
        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(f"❌ You are not the owner of subnet {subnet_id}. Only the owner can update parameters.")
            raise typer.Exit(1)

        print_info(f"⏱️ Updating activation grace epochs for subnet {subnet_id} to {epochs}...")

        response = client.owner_update_activation_grace_epochs(subnet_id, epochs, key_name=key_name)

        if response.success:
            print_success(f"✅ Successfully updated activation grace epochs for subnet {subnet_id} to {epochs}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]⏱️ Activation Grace Epochs Updated![/bold green]\n\n"
                f"Subnet {subnet_id} activation grace epochs is now {epochs}.\n"
                f"• Nodes have {epochs} epochs grace period\n"
                f"• More flexible activation timing\n"
                f"• Better success rate for nodes\n"
                f"• Improved subnet reliability\n\n"
                f"[yellow]📊 Monitor Impact:[/yellow]\n"
                f"• Watch activation success rates\n"
                f"• Monitor node onboarding\n"
                f"• Check subnet stability\n\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Activation Grace Epochs Update Complete",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to update activation grace epochs: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to update activation grace epochs: {str(e)}")
        raise typer.Exit(1)


@app.command()
def owner_update_idle_epochs(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    epochs: int = typer.Option(..., "--epochs", "-e", help="New idle classification epochs"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Update idle classification epochs for a subnet (owner only)."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]⏱️ Update Idle Classification Epochs Guide[/bold cyan]\n\n"
            f"This will update the idle classification epochs for subnet {subnet_id} to {epochs}:\n\n"
            f"[bold]What are Idle Classification Epochs:[/bold]\n"
            f"• Number of epochs nodes stay in idle classification\n"
            f"• Period before upgrading to included classification\n"
            f"• Affects node progression through classifications\n"
            f"• Influences validator selection timing\n\n"
            f"[bold]Impact:[/bold]\n"
            f"• Higher epochs = longer idle period\n"
            f"• Lower epochs = faster progression\n"
            f"• Affects validator selection\n"
            f"• Influences subnet performance\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Consider subnet performance needs\n"
            f"• Balance progression with stability\n"
            f"• Monitor validator selection\n"
            f"• Works with other classification epochs",
            title="[bold blue]⏱️ Update Idle Classification Epochs[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Update idle classification epochs for subnet {subnet_id} to {epochs}?"):
            print_info("Idle classification epochs update cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_epoch_value(epochs):
        print_error("❌ Invalid epoch value. Must be a positive integer.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for owner operations)
    if not key_name:
        print_error("❌ Key name is required for subnet owner operations. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        # Check ownership (user must be the owner to update parameters)
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(f"❌ Failed to get subnet information: {subnet_response.message}")
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get('exists', False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check ownership (user must be the owner to update parameters)
        from ..utils.ownership import get_user_addresses, user_owns_subnet
        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(f"❌ You are not the owner of subnet {subnet_id}. Only the owner can update parameters.")
            raise typer.Exit(1)

        print_info(f"⏱️ Updating idle classification epochs for subnet {subnet_id} to {epochs}...")

        response = client.owner_update_idle_epochs(subnet_id, epochs, key_name=key_name)

        if response.success:
            print_success(f"✅ Successfully updated idle classification epochs for subnet {subnet_id} to {epochs}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]⏱️ Idle Classification Epochs Updated![/bold green]\n\n"
                f"Subnet {subnet_id} idle classification epochs is now {epochs}.\n"
                f"• Nodes stay idle for {epochs} epochs\n"
                f"• Progression timing adjusted\n"
                f"• Validator selection affected\n"
                f"• Performance parameters modified\n\n"
                f"[yellow]📊 Monitor Impact:[/yellow]\n"
                f"• Watch node progression\n"
                f"• Monitor validator selection\n"
                f"• Check subnet performance\n\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Idle Epochs Update Complete",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to update idle classification epochs: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to update idle classification epochs: {str(e)}")
        raise typer.Exit(1)


@app.command()
def owner_update_included_epochs(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    epochs: int = typer.Option(..., "--epochs", "-e", help="New included classification epochs"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Update included classification epochs for a subnet (owner only)."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]⏱️ Update Included Classification Epochs Guide[/bold cyan]\n\n"
            f"This will update the included classification epochs for subnet {subnet_id} to {epochs}:\n\n"
            f"[bold]What are Included Classification Epochs:[/bold]\n"
            f"• Number of epochs nodes stay in included classification\n"
            f"• Period before upgrading to validator classification\n"
            f"• Final stage before becoming active validators\n"
            f"• Critical for validator selection\n\n"
            f"[bold]Impact:[/bold]\n"
            f"• Higher epochs = longer included period\n"
            f"• Lower epochs = faster validator promotion\n"
            f"• Affects validator pool size\n"
            f"• Influences consensus stability\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Consider consensus stability needs\n"
            f"• Balance promotion with quality\n"
            f"• Monitor validator pool size\n"
            f"• Critical for subnet performance",
            title="[bold blue]⏱️ Update Included Classification Epochs[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Update included classification epochs for subnet {subnet_id} to {epochs}?"):
            print_info("Included classification epochs update cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_epoch_value(epochs):
        print_error("❌ Invalid epoch value. Must be a positive integer.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for owner operations)
    if not key_name:
        print_error("❌ Key name is required for subnet owner operations. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        # Check ownership (user must be the owner to update parameters)
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(f"❌ Failed to get subnet information: {subnet_response.message}")
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get('exists', False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check ownership (user must be the owner to update parameters)
        from ..utils.ownership import get_user_addresses, user_owns_subnet
        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(f"❌ You are not the owner of subnet {subnet_id}. Only the owner can update parameters.")
            raise typer.Exit(1)

        print_info(f"⏱️ Updating included classification epochs for subnet {subnet_id} to {epochs}...")

        response = client.owner_update_included_epochs(subnet_id, epochs, key_name=key_name)

        if response.success:
            print_success(f"✅ Successfully updated included classification epochs for subnet {subnet_id} to {epochs}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]⏱️ Included Classification Epochs Updated![/bold green]\n\n"
                f"Subnet {subnet_id} included classification epochs is now {epochs}.\n"
                f"• Nodes stay included for {epochs} epochs\n"
                f"• Validator promotion timing adjusted\n"
                f"• Validator pool size affected\n"
                f"• Consensus stability modified\n\n"
                f"[yellow]📊 Monitor Impact:[/yellow]\n"
                f"• Watch validator pool size\n"
                f"• Monitor consensus stability\n"
                f"• Check subnet performance\n\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Included Epochs Update Complete",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to update included classification epochs: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to update included classification epochs: {str(e)}")
        raise typer.Exit(1)


@app.command()
def owner_update_max_penalties(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    max_penalties: int = typer.Option(..., "--max-penalties", "-p", help="New maximum node penalties"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Update maximum node penalties for a subnet (owner only)."""
    client = get_client()

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]⚠️ Update Maximum Node Penalties Guide[/bold cyan]\n\n"
            f"This will update the maximum node penalties for subnet {subnet_id} to {max_penalties}:\n\n"
            f"[bold]What are Maximum Node Penalties:[/bold]\n"
            f"• Maximum number of penalties a validator node can have\n"
            f"• Nodes are removed when they exceed this limit\n"
            f"• Affects validator quality and reliability\n"
            f"• Influences subnet performance standards\n\n"
            f"[bold]Impact:[/bold]\n"
            f"• Higher limit = more tolerance for errors\n"
            f"• Lower limit = stricter quality standards\n"
            f"• Affects validator retention\n"
            f"• Influences subnet reliability\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• This affects validator quality\n"
            f"• Consider subnet performance needs\n"
            f"• Monitor penalty patterns\n"
            f"• Balance tolerance with quality",
            title="[bold red]⚠️ Update Maximum Node Penalties[/bold red]",
            border_style="red"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Update maximum node penalties for subnet {subnet_id} to {max_penalties}?"):
            print_info("Maximum node penalties update cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not validate_max_penalties(max_penalties):
        print_error("❌ Invalid maximum penalties value. Must be a positive integer.")
        raise typer.Exit(1)

    # Check if key_name is provided (required for owner operations)
    if not key_name:
        print_error("❌ Key name is required for subnet owner operations. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        # Check ownership (user must be the owner to update parameters)
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(f"❌ Failed to get subnet information: {subnet_response.message}")
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get('exists', False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check ownership (user must be the owner to update parameters)
        from ..utils.ownership import get_user_addresses, user_owns_subnet
        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(f"❌ You are not the owner of subnet {subnet_id}. Only the owner can update parameters.")
            raise typer.Exit(1)

        print_info(f"⚠️ Updating maximum node penalties for subnet {subnet_id} to {max_penalties}...")

        response = client.owner_update_max_penalties(subnet_id, max_penalties, key_name=key_name)

        if response.success:
            print_success(f"✅ Successfully updated maximum node penalties for subnet {subnet_id} to {max_penalties}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]⚠️ Maximum Node Penalties Updated![/bold green]\n\n"
                f"Subnet {subnet_id} maximum node penalties is now {max_penalties}.\n"
                f"• Validators can have up to {max_penalties} penalties\n"
                f"• Quality standards adjusted\n"
                f"• Validator retention affected\n"
                f"• Performance requirements modified\n\n"
                f"[yellow]📊 Monitor Impact:[/yellow]\n"
                f"• Watch validator quality\n"
                f"• Monitor penalty patterns\n"
                f"• Check subnet reliability\n\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Maximum Penalties Update Complete",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to update maximum node penalties: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to update maximum node penalties: {str(e)}")
        raise typer.Exit(1)


@app.command()
def owner_add_initial_coldkeys(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    coldkeys: str = typer.Option(..., "--coldkeys", "-c", help="Comma-separated list of coldkey addresses"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Add initial coldkeys to a subnet (owner only, registration phase only)."""
    client = get_client()

    # Parse coldkeys
    coldkey_list = [addr.strip() for addr in coldkeys.split(",") if addr.strip()]

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]🔑 Add Initial Coldkeys Guide[/bold cyan]\n\n"
            f"This will add {len(coldkey_list)} initial coldkeys to subnet {subnet_id}:\n\n"
            f"[bold]What are Initial Coldkeys:[/bold]\n"
            f"• Coldkeys that can register nodes during registration phase\n"
            f"• Only these coldkeys can register before activation\n"
            f"• Can be updated while subnet is in registration phase\n"
            f"• Removed once subnet is activated\n\n"
            f"[bold]Impact:[/bold]\n"
            f"• Controls who can register nodes initially\n"
            f"• Affects subnet launch strategy\n"
            f"• Influences early validator selection\n"
            f"• Only available during registration phase\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Only works during registration phase\n"
            f"• Coldkeys are removed after activation\n"
            f"• Consider your launch strategy\n"
            f"• Verify coldkey addresses carefully",
            title="[bold blue]🔑 Add Initial Coldkeys[/bold blue]",
            border_style="blue"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Add {len(coldkey_list)} initial coldkeys to subnet {subnet_id}?"):
            print_info("Initial coldkeys addition cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not coldkey_list:
        print_error("❌ No valid coldkey addresses provided.")
        raise typer.Exit(1)

    for coldkey in coldkey_list:
        if not validate_coldkey_addresses(coldkey):
            print_error(f"❌ Invalid coldkey address: {coldkey}")
            raise typer.Exit(1)

    # Check if key_name is provided (required for owner operations)
    if not key_name:
        print_error("❌ Key name is required for subnet owner operations. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        # Check ownership (user must be the owner to update parameters)
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(f"❌ Failed to get subnet information: {subnet_response.message}")
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get('exists', False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check ownership (user must be the owner to update parameters)
        from ..utils.ownership import get_user_addresses, user_owns_subnet
        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(f"❌ You are not the owner of subnet {subnet_id}. Only the owner can update parameters.")
            raise typer.Exit(1)

        print_info(f"🔑 Adding {len(coldkey_list)} initial coldkeys to subnet {subnet_id}...")

        response = client.owner_add_initial_coldkeys(subnet_id, coldkey_list, key_name=key_name)

        if response.success:
            print_success(f"✅ Successfully added {len(coldkey_list)} initial coldkeys to subnet {subnet_id}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold green]🔑 Initial Coldkeys Added![/bold green]\n\n"
                f"Subnet {subnet_id} now has {len(coldkey_list)} additional initial coldkeys.\n"
                f"• These coldkeys can register nodes\n"
                f"• Only available during registration phase\n"
                f"• Will be removed after activation\n"
                f"• Launch strategy enhanced\n\n"
                f"[yellow]📊 Monitor Impact:[/yellow]\n"
                f"• Watch node registration patterns\n"
                f"• Monitor subnet growth\n"
                f"• Check activation readiness\n\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Initial Coldkeys Addition Complete",
                border_style="green"
            ))
        else:
            print_error(f"❌ Failed to add initial coldkeys: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to add initial coldkeys: {str(e)}")
        raise typer.Exit(1)


@app.command()
def owner_remove_initial_coldkeys(
    subnet_id: int = typer.Option(..., "--subnet-id", "-s", help="Subnet ID"),
    coldkeys: str = typer.Option(..., "--coldkeys", "-c", help="Comma-separated list of coldkey addresses"),
    key_name: Optional[str] = typer.Option(
        None, "--key-name", "-k", help="Key name for signing (required for owner)"
    ),
    show_guidance: bool = typer.Option(
        True, "--guidance/--no-guidance", help="Show comprehensive guidance"
    ),
):
    """Remove initial coldkeys from a subnet (owner only, registration phase only)."""
    client = get_client()

    # Parse coldkeys
    coldkey_list = [addr.strip() for addr in coldkeys.split(",") if addr.strip()]

    # Show comprehensive guidance
    if show_guidance:
        from rich.panel import Panel
        guidance_panel = Panel(
            f"[bold cyan]🔑 Remove Initial Coldkeys Guide[/bold cyan]\n\n"
            f"This will remove {len(coldkey_list)} initial coldkeys from subnet {subnet_id}:\n\n"
            f"[bold]What This Does:[/bold]\n"
            f"• Removes coldkeys from initial coldkeys list\n"
            f"• These coldkeys can no longer register nodes\n"
            f"• Only works during registration phase\n"
            f"• May affect existing registered nodes\n\n"
            f"[bold]Impact:[/bold]\n"
            f"• Reduces who can register nodes\n"
            f"• May affect existing registrations\n"
            f"• Influences subnet launch strategy\n"
            f"• Only available during registration phase\n\n"
            f"[yellow]⚠️ Important:[/yellow]\n"
            f"• Only works during registration phase\n"
            f"• May affect existing nodes\n"
            f"• Consider impact on registrations\n"
            f"• Verify coldkey addresses carefully",
            title="[bold red]🔑 Remove Initial Coldkeys[/bold red]",
            border_style="red"
        )
        console.print(guidance_panel)
        console.print()

        # Ask for confirmation
        if not typer.confirm(f"Remove {len(coldkey_list)} initial coldkeys from subnet {subnet_id}?"):
            print_info("Initial coldkeys removal cancelled.")
            return

    # Validate inputs
    if not validate_subnet_id(subnet_id):
        print_error("❌ Invalid subnet ID. Must be a positive integer.")
        raise typer.Exit(1)

    if not coldkey_list:
        print_error("❌ No valid coldkey addresses provided.")
        raise typer.Exit(1)

    for coldkey in coldkey_list:
        if not validate_coldkey_addresses(coldkey):
            print_error(f"❌ Invalid coldkey address: {coldkey}")
            raise typer.Exit(1)

    # Check if key_name is provided (required for owner operations)
    if not key_name:
        print_error("❌ Key name is required for subnet owner operations. Use --key-name to specify your signing key.")
        raise typer.Exit(1)

    try:
        # Check ownership (user must be the owner to update parameters)
        subnet_response = client.get_subnet_data(subnet_id)
        if not subnet_response.success:
            print_error(f"❌ Failed to get subnet information: {subnet_response.message}")
            raise typer.Exit(1)

        subnet_info = subnet_response.data

        # Check if subnet exists
        if not subnet_info.get('exists', False):
            print_error(f"❌ Subnet {subnet_id} does not exist.")
            raise typer.Exit(1)

        # Check ownership (user must be the owner to update parameters)
        from ..utils.ownership import get_user_addresses, user_owns_subnet
        user_addresses = get_user_addresses()
        if not user_owns_subnet(subnet_info, user_addresses):
            print_error(f"❌ You are not the owner of subnet {subnet_id}. Only the owner can update parameters.")
            raise typer.Exit(1)

        print_info(f"🔑 Removing {len(coldkey_list)} initial coldkeys from subnet {subnet_id}...")

        response = client.owner_remove_initial_coldkeys(subnet_id, coldkey_list, key_name=key_name)

        if response.success:
            print_success(f"✅ Successfully removed {len(coldkey_list)} initial coldkeys from subnet {subnet_id}!")
            console.print(f"📄 Transaction Hash: [bold cyan]{response.transaction_hash}[/bold cyan]")
            if response.block_number:
                console.print(f"📦 Block Number: [bold cyan]#{response.block_number}[/bold cyan]")

            console.print(Panel(
                f"[bold red]🔑 Initial Coldkeys Removed![/bold red]\n\n"
                f"Subnet {subnet_id} has {len(coldkey_list)} fewer initial coldkeys.\n"
                f"• These coldkeys can no longer register nodes\n"
                f"• May affect existing registrations\n"
                f"• Launch strategy modified\n"
                f"• Registration access reduced\n\n"
                f"[yellow]📊 Monitor Impact:[/yellow]\n"
                f"• Check existing node registrations\n"
                f"• Monitor registration patterns\n"
                f"• Verify launch strategy\n\n"
                f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                title="Initial Coldkeys Removal Complete",
                border_style="red"
            ))
        else:
            print_error(f"❌ Failed to remove initial coldkeys: {response.message}")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"❌ Failed to remove initial coldkeys: {str(e)}")
        raise typer.Exit(1)
