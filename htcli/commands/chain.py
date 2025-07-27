import typer
import json
from substrateinterface import SubstrateInterface
from htcli.core.config import chain_config_instance
from htcli.core.constants import DEFAULT_RPC_URL, DEFAULT_CHAIN_ENV

app = typer.Typer(name="chain", help="Chain commands")


def get_substrate_interface(rpc_url: str = None, env: str = None) -> SubstrateInterface:
    """
    Create a SubstrateInterface instance for connecting to Hypertensor chain.

    Args:
        rpc_url: RPC URL to connect to
        env: Environment (local/testnet/mainnet)

    Returns:
        SubstrateInterface: Connected interface instance
    """
    try:
        # Use provided RPC URL or default based on environment
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
def info(
    rpc_url: str = chain_config_instance.rpc_url,
    env: str = chain_config_instance.env,
    detailed: bool = typer.Option(False, "--detailed", "-d", help="Show detailed information")
):
    """
    Get chain information including block height, network status, and chain metadata.

    Examples:
        htcli chain info
        htcli chain info --detailed
        htcli chain info --env testnet
    """
    try:
        substrate = get_substrate_interface(rpc_url, env)

        # Get chain information
        chain_info = {
            "environment": env,
            "rpc_url": rpc_url,
            "connected": True
        }

        # Get block information
        try:
            block_header = substrate.get_chain_head()
            chain_info["block_height"] = block_header
        except Exception as e:
            chain_info["block_height"] = f"Error: {str(e)}"

        # Get chain properties
        try:
            properties = substrate.get_chain_properties()
            chain_info["chain_properties"] = properties
        except Exception as e:
            chain_info["chain_properties"] = f"Error: {str(e)}"

        # Get runtime version
        try:
            runtime_version = substrate.get_runtime_version()
            chain_info["runtime_version"] = runtime_version
        except Exception as e:
            chain_info["runtime_version"] = f"Error: {str(e)}"

        if detailed:
            # Get additional detailed information
            try:
                # Get system events
                events = substrate.query_runtime_state("System", "Events", [])
                chain_info["recent_events"] = len(events) if events else 0
            except Exception as e:
                chain_info["recent_events"] = f"Error: {str(e)}"

        # Display information
        typer.echo(typer.style("🔗 Chain Information", bold=True))
        typer.echo(f"Environment: {chain_info['environment']}")
        typer.echo(f"RPC URL: {chain_info['rpc_url']}")
        typer.echo(f"Connected: {'✅' if chain_info['connected'] else '❌'}")
        typer.echo(f"Block Height: {chain_info['block_height']}")

        if detailed:
            typer.echo(f"Runtime Version: {chain_info['runtime_version']}")
            if 'recent_events' in chain_info:
                typer.echo(f"Recent Events: {chain_info['recent_events']}")

    except Exception as e:
        typer.echo(typer.style(f"❌ Error getting chain info: {str(e)}", fg=typer.colors.RED))


@app.command()
def peers(
    rpc_url: str = chain_config_instance.rpc_url,
    env: str = chain_config_instance.env,
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of peers to show")
):
    """
    List connected peers and network information.

    Examples:
        htcli chain peers
        htcli chain peers --limit 50
    """
    try:
        substrate = get_substrate_interface(rpc_url, env)

        # Get peer information
        try:
            # This is a simplified version - actual peer query might vary
            peers_info = substrate.query_runtime_state("System", "PeerCount", [])
            typer.echo(typer.style("🌐 Network Peers", bold=True))
            typer.echo(f"Connected Peers: {peers_info if peers_info else 'Unknown'}")

            # Note: Detailed peer information might require different RPC calls
            # depending on the specific Hypertensor implementation
            typer.echo("Note: Detailed peer information requires specific RPC implementation")

        except Exception as e:
            typer.echo(typer.style(f"❌ Error getting peer info: {str(e)}", fg=typer.colors.RED))

    except Exception as e:
        typer.echo(typer.style(f"❌ Error connecting to chain: {str(e)}", fg=typer.colors.RED))


@app.command()
def block(
    block_hash: str = typer.Option(None, "--hash", "-h", help="Block hash to query"),
    block_number: int = typer.Option(None, "--number", "-n", help="Block number to query"),
    rpc_url: str = chain_config_instance.rpc_url,
    env: str = chain_config_instance.env
):
    """
    Get block information by hash or number.

    Examples:
        htcli chain block --number 12345
        htcli chain block --hash 0x1234...
    """
    try:
        substrate = get_substrate_interface(rpc_url, env)

        if not block_hash and not block_number:
            # Get latest block
            block_hash = substrate.get_chain_head()
            typer.echo("No block specified, getting latest block...")

        try:
            if block_number:
                # Get block by number
                block_info = substrate.get_block_header(block_number=block_number)
            else:
                # Get block by hash
                block_info = substrate.get_block_header(block_hash=block_hash)

            typer.echo(typer.style("📦 Block Information", bold=True))
            typer.echo(f"Block Hash: {block_info['header']['hash']}")
            typer.echo(f"Block Number: {block_info['header']['number']}")
            typer.echo(f"Parent Hash: {block_info['header']['parentHash']}")
            typer.echo(f"State Root: {block_info['header']['stateRoot']}")

        except Exception as e:
            typer.echo(typer.style(f"❌ Error getting block info: {str(e)}", fg=typer.colors.RED))

    except Exception as e:
        typer.echo(typer.style(f"❌ Error connecting to chain: {str(e)}", fg=typer.colors.RED))


@app.command()
def network(
    rpc_url: str = chain_config_instance.rpc_url,
    env: str = chain_config_instance.env
):
    """
    Get network statistics and status.

    Examples:
        htcli chain network
        htcli chain network --env testnet
    """
    try:
        substrate = get_substrate_interface(rpc_url, env)

        typer.echo(typer.style("🌐 Network Status", bold=True))

        # Get network information
        try:
            # Get chain head for latest block
            chain_head = substrate.get_chain_head()
            typer.echo(f"Latest Block: {chain_head}")

            # Get chain properties
            properties = substrate.get_chain_properties()
            if properties:
                typer.echo(f"Chain Name: {properties.get('chainName', 'Unknown')}")
                typer.echo(f"Token Symbol: {properties.get('tokenSymbol', 'Unknown')}")
                typer.echo(f"Token Decimals: {properties.get('tokenDecimals', 'Unknown')}")

            # Get runtime version
            runtime = substrate.get_runtime_version()
            if runtime:
                typer.echo(f"Runtime Version: {runtime.get('specVersion', 'Unknown')}")

        except Exception as e:
            typer.echo(f"Error getting network info: {str(e)}")

    except Exception as e:
        typer.echo(typer.style(f"❌ Error connecting to network: {str(e)}", fg=typer.colors.RED))
