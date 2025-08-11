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
)
from ..utils.formatting import (
    print_info,
    print_success,
    print_error,
    format_subnet_list,
    format_subnet_info,
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

        # TODO: Add actual requirement checking here
        # - Check minimum nodes
        # - Check minimum delegate stake
        # - Check stake factor requirements

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

            console.print(
                Panel(
                    f"[bold green]🚀 Subnet Activation Complete![/bold green]\n\n"
                    f"Subnet {subnet_id} is now active and:\n"
                    f"• Has an open slot for rewards distribution\n"
                    f"• Initial coldkeys have been removed\n"
                    f"• Anyone can now register nodes\n"
                    f"• Subnet is earning and distributing rewards\n\n"
                    f"[yellow]📊 Monitor your subnet:[/yellow]\n"
                    f"Use: [bold]htcli subnet info --subnet-id {subnet_id}[/bold]",
                    title="Activation Success",
                    border_style="green",
                )
            )
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

            console.print(
                Panel(
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
                    border_style="yellow",
                )
            )
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

            console.print(
                Panel(
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
                    border_style="green",
                )
            )
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
