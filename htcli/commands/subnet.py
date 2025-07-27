import typer
import json
from substrateinterface import SubstrateInterface
from htcli.core.config.subnet import subnet_config
from htcli.core.config import chain_config_instance
from htcli.core.constants import DEFAULT_RPC_URL, DEFAULT_CHAIN_ENV

app = typer.Typer(name="subnet", help="Subnet commands")


def get_substrate_interface(rpc_url: str = None, env: str = None) -> SubstrateInterface:
    """
    Create a SubstrateInterface instance for connecting to Hypertensor chain.
    """
    try:
        if not rpc_url:
            if env == "testnet":
                rpc_url = "wss://testnet.hypertensor.org"
            elif env == "mainnet":
                rpc_url = "wss://mainnet.hypertensor.org"
            else:
                rpc_url = DEFAULT_RPC_URL

        substrate = SubstrateInterface(url=rpc_url, ss58_format=42)
        return substrate
    except Exception as e:
        raise typer.Exit(f"Failed to connect to chain: {str(e)}")


@app.command()
def list(
    rpc_url: str = chain_config_instance.rpc_url,
    env: str = chain_config_instance.env,
    detailed: bool = typer.Option(False, "--detailed", "-d", help="Show detailed information")
):
    """
    List all available subnets on the Hypertensor network.

    Examples:
        htcli subnet list
        htcli subnet list --detailed
        htcli subnet list --env testnet
    """
    try:
        substrate = get_substrate_interface(rpc_url, env)

        typer.echo(typer.style("🧠 Available Subnets", bold=True))

        try:
            # Query subnet registry
            # Note: This is a placeholder - actual implementation depends on Hypertensor's specific pallet
            subnets = substrate.query_runtime_state("SubnetRegistry", "Subnets", [])

            if not subnets:
                typer.echo("No subnets found or subnet registry not available")
                return

            # Display subnets in a table format
            headers = ["ID", "Name", "Validators", "Stake"]
            rows = []

            for subnet in subnets:
                subnet_id = subnet.get('id', 'Unknown')
                subnet_name = subnet.get('name', 'Unknown')
                validator_count = subnet.get('validator_count', 0)
                total_stake = subnet.get('total_stake', 0)

                rows.append([str(subnet_id), subnet_name, str(validator_count), str(total_stake)])

            # Print table
            if rows:
                # Calculate column widths
                col_widths = [max(len(headers[i]), max(len(row[i]) for row in rows)) for i in range(len(headers))]

                # Print header
                header = " | ".join(headers[i].ljust(col_widths[i]) for i in range(len(headers)))
                separator = "-" * len(header)
                typer.echo(separator)
                typer.echo(header)
                typer.echo(separator)

                # Print rows
                for row in rows:
                    row_str = " | ".join(row[i].ljust(col_widths[i]) for i in range(len(row)))
                    typer.echo(row_str)
                typer.echo(separator)

            if detailed:
                typer.echo(f"\nTotal Subnets: {len(rows)}")

        except Exception as e:
            typer.echo(typer.style(f"❌ Error querying subnets: {str(e)}", fg=typer.colors.RED))
            typer.echo("Note: Subnet registry might not be available or implemented differently")

    except Exception as e:
        typer.echo(typer.style(f"❌ Error connecting to chain: {str(e)}", fg=typer.colors.RED))


@app.command()
def info(
    subnet_id: int = subnet_config.id,
    subnet_name: str = subnet_config.name,
    rpc_url: str = chain_config_instance.rpc_url,
    env: str = chain_config_instance.env
):
    """
    Get detailed information about a specific subnet.

    Examples:
        htcli subnet info --id 1
        htcli subnet info --name "my_subnet"
    """
    try:
        substrate = get_substrate_interface(rpc_url, env)

        typer.echo(typer.style(f"🧠 Subnet Information", bold=True))
        typer.echo(f"Subnet ID: {subnet_id}")
        typer.echo(f"Subnet Name: {subnet_name}")

        try:
            # Query subnet information
            # Note: This is a placeholder - actual implementation depends on Hypertensor's specific pallet
            subnet_info = substrate.query_runtime_state("SubnetRegistry", "SubnetInfo", [subnet_id])

            if subnet_info:
                typer.echo(f"Status: {'Active' if subnet_info.get('active', False) else 'Inactive'}")
                typer.echo(f"Validator Count: {subnet_info.get('validator_count', 0)}")
                typer.echo(f"Total Stake: {subnet_info.get('total_stake', 0)} TENSOR")
                typer.echo(f"Min Stake: {subnet_info.get('min_stake', 0)} TENSOR")
                typer.echo(f"Max Validators: {subnet_info.get('max_validators', 0)}")

                if subnet_info.get('consensus_mechanism'):
                    typer.echo(f"Consensus: {subnet_info['consensus_mechanism']}")

            else:
                typer.echo("Subnet not found or information not available")

        except Exception as e:
            typer.echo(typer.style(f"❌ Error getting subnet info: {str(e)}", fg=typer.colors.RED))

    except Exception as e:
        typer.echo(typer.style(f"❌ Error connecting to chain: {str(e)}", fg=typer.colors.RED))


@app.command()
def validators(
    subnet_id: int = subnet_config.id,
    rpc_url: str = chain_config_instance.rpc_url,
    env: str = chain_config_instance.env,
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of validators to show")
):
    """
    List validators on a specific subnet.

    Examples:
        htcli subnet validators --id 1
        htcli subnet validators --id 1 --limit 50
    """
    try:
        substrate = get_substrate_interface(rpc_url, env)

        typer.echo(typer.style(f"👥 Validators on Subnet {subnet_id}", bold=True))

        try:
            # Query validators for the subnet
            # Note: This is a placeholder - actual implementation depends on Hypertensor's specific pallet
            validators = substrate.query_runtime_state("SubnetRegistry", "SubnetValidators", [subnet_id])

            if not validators:
                typer.echo("No validators found for this subnet")
                return

            # Display validators in a table format
            headers = ["Address", "Stake", "Commission", "Status"]
            rows = []

            for validator in validators[:limit]:
                address = validator.get('address', 'Unknown')
                stake = validator.get('stake', 0)
                commission = validator.get('commission', 0)
                status = 'Active' if validator.get('active', False) else 'Inactive'

                rows.append([address, str(stake), f"{commission}%", status])

            # Print table
            if rows:
                col_widths = [max(len(headers[i]), max(len(row[i]) for row in rows)) for i in range(len(headers))]

                header = " | ".join(headers[i].ljust(col_widths[i]) for i in range(len(headers)))
                separator = "-" * len(header)
                typer.echo(separator)
                typer.echo(header)
                typer.echo(separator)

                for row in rows:
                    row_str = " | ".join(row[i].ljust(col_widths[i]) for i in range(len(row)))
                    typer.echo(row_str)
                typer.echo(separator)

                if len(validators) > limit:
                    typer.echo(f"Showing {limit} of {len(validators)} validators")

        except Exception as e:
            typer.echo(typer.style(f"❌ Error getting validators: {str(e)}", fg=typer.colors.RED))

    except Exception as e:
        typer.echo(typer.style(f"❌ Error connecting to chain: {str(e)}", fg=typer.colors.RED))


@app.command()
def register(
    subnet_id: int = subnet_config.id,
    wallet_name: str = typer.Option(None, "--wallet", "-w", help="Wallet name to use"),
    rpc_url: str = chain_config_instance.rpc_url,
    env: str = chain_config_instance.env,
    force: bool = typer.Option(False, "--force", help="Skip confirmation")
):
    """
    Register as a validator on a subnet.

    Examples:
        htcli subnet register --id 1 --wallet mywallet
        htcli subnet register --id 1 --wallet mywallet --force
    """
    try:
        substrate = get_substrate_interface(rpc_url, env)

        if not wallet_name:
            wallet_name = typer.prompt("Enter wallet name")

        typer.echo(typer.style(f"🔧 Registering as Validator", bold=True))
        typer.echo(f"Subnet ID: {subnet_id}")
        typer.echo(f"Wallet: {wallet_name}")

        if not force:
            confirm = typer.confirm(f"Register as validator on subnet {subnet_id}?")
            if not confirm:
                typer.echo("Registration cancelled")
                return

        # Note: This is a placeholder - actual implementation requires:
        # 1. Loading wallet keypair
        # 2. Creating and signing the registration transaction
        # 3. Submitting the transaction to the chain

        typer.echo("Note: Validator registration requires wallet integration and transaction signing")
        typer.echo("This feature needs to be implemented with proper wallet loading and transaction submission")

    except Exception as e:
        typer.echo(typer.style(f"❌ Error registering validator: {str(e)}", fg=typer.colors.RED))


@app.command()
def stake(
    subnet_id: int = subnet_config.id,
    amount: float = typer.Option(..., "--amount", "-a", help="Amount of TENSOR to stake"),
    wallet_name: str = typer.Option(None, "--wallet", "-w", help="Wallet name to use"),
    rpc_url: str = chain_config_instance.rpc_url,
    env: str = chain_config_instance.env,
    force: bool = typer.Option(False, "--force", help="Skip confirmation")
):
    """
    Stake TENSOR tokens on a subnet.

    Examples:
        htcli subnet stake --id 1 --amount 1000 --wallet mywallet
        htcli subnet stake --id 1 --amount 1000 --wallet mywallet --force
    """
    try:
        substrate = get_substrate_interface(rpc_url, env)

        if not wallet_name:
            wallet_name = typer.prompt("Enter wallet name")

        typer.echo(typer.style(f"💰 Staking TENSOR", bold=True))
        typer.echo(f"Subnet ID: {subnet_id}")
        typer.echo(f"Amount: {amount} TENSOR")
        typer.echo(f"Wallet: {wallet_name}")

        if not force:
            confirm = typer.confirm(f"Stake {amount} TENSOR on subnet {subnet_id}?")
            if not confirm:
                typer.echo("Staking cancelled")
                return

        # Note: This is a placeholder - actual implementation requires:
        # 1. Loading wallet keypair
        # 2. Creating and signing the staking transaction
        # 3. Submitting the transaction to the chain

        typer.echo("Note: Staking requires wallet integration and transaction signing")
        typer.echo("This feature needs to be implemented with proper transaction submission")

    except Exception as e:
        typer.echo(typer.style(f"❌ Error staking: {str(e)}", fg=typer.colors.RED))


@app.command()
def delegate(
    subnet_id: int = subnet_config.id,
    validator_address: str = typer.Option(..., "--validator", "-v", help="Validator address to delegate to"),
    amount: float = typer.Option(..., "--amount", "-a", help="Amount of TENSOR to delegate"),
    wallet_name: str = typer.Option(None, "--wallet", "-w", help="Wallet name to use"),
    rpc_url: str = chain_config_instance.rpc_url,
    env: str = chain_config_instance.env,
    force: bool = typer.Option(False, "--force", help="Skip confirmation")
):
    """
    Delegate TENSOR tokens to a validator on a subnet.

    Examples:
        htcli subnet delegate --id 1 --validator 5xxx... --amount 500 --wallet mywallet
    """
    try:
        substrate = get_substrate_interface(rpc_url, env)

        if not wallet_name:
            wallet_name = typer.prompt("Enter wallet name")

        typer.echo(typer.style(f"🎯 Delegating TENSOR", bold=True))
        typer.echo(f"Subnet ID: {subnet_id}")
        typer.echo(f"Validator: {validator_address}")
        typer.echo(f"Amount: {amount} TENSOR")
        typer.echo(f"Wallet: {wallet_name}")

        if not force:
            confirm = typer.confirm(f"Delegate {amount} TENSOR to {validator_address} on subnet {subnet_id}?")
            if not confirm:
                typer.echo("Delegation cancelled")
                return

        # Note: This is a placeholder - actual implementation requires:
        # 1. Loading wallet keypair
        # 2. Creating and signing the delegation transaction
        # 3. Submitting the transaction to the chain

        typer.echo("Note: Delegation requires wallet integration and transaction signing")
        typer.echo("This feature needs to be implemented with proper transaction submission")

    except Exception as e:
        typer.echo(typer.style(f"❌ Error delegating: {str(e)}", fg=typer.colors.RED))
