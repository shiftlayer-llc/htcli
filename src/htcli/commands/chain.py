"""
Flattened chain commands - 3-level hierarchy.
"""

import typer
from rich.console import Console
from typing import Optional
from ..utils.validation import validate_address, validate_block_number, validate_limit
from ..utils.formatting import (
    print_success, print_error, format_network_stats, format_account_info,
    format_epoch_info, format_table
)
from ..dependencies import get_client

app = typer.Typer(name="chain", help="Chain operations")
console = Console()


@app.command()
def network(
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """Get network statistics."""
    client = get_client()

    try:
        response = client.get_network_stats()
        if response.success:
            stats = response.data
            if format_type == "json":
                console.print_json(data=stats)
            else:
                format_network_stats(stats)
        else:
            print_error(f"Failed to retrieve network stats: {response.message}")
    except Exception as e:
        print_error(f"Failed to get network stats: {str(e)}")
        raise typer.Exit(1)


@app.command()
def epoch(
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """Get current epoch information."""
    client = get_client()

    try:
        response = client.get_current_epoch()
        if response.success:
            epoch_data = response.data
            if format_type == "json":
                console.print_json(data=epoch_data)
            else:
                format_epoch_info(epoch_data)
        else:
            print_error(f"Failed to retrieve epoch info: {response.message}")
    except Exception as e:
        print_error(f"Failed to get epoch info: {str(e)}")
        raise typer.Exit(1)


@app.command()
def account(
    address: str = typer.Argument(..., help="Account address"),
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """Get account information."""
    client = get_client()

    # Validate inputs
    if not validate_address(address):
        print_error("Invalid address format.")
        raise typer.Exit(1)

    try:
        response = client.get_account_info(address)
        if response.success:
            account_data = response.data
            if format_type == "json":
                console.print_json(data=account_data)
            else:
                format_account_info(account_data)
        else:
            print_error(f"Failed to retrieve account info: {response.message}")
    except Exception as e:
        print_error(f"Failed to get account info: {str(e)}")
        raise typer.Exit(1)


@app.command()
def balance(
    address: str = typer.Argument(..., help="Account address"),
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """Get account balance."""
    client = get_client()

    # Validate inputs
    if not validate_address(address):
        print_error("Invalid address format.")
        raise typer.Exit(1)

    try:
        response = client.get_balance(address)
        if response.success:
            balance_data = response.data
            if format_type == "json":
                console.print_json(data=balance_data)
            else:
                console.print(f"Address: {address}")
                console.print(f"Balance: {balance_data.get('formatted_balance', 'N/A')}")
                console.print(f"Raw Balance: {balance_data.get('balance', 'N/A')}")
        else:
            print_error(f"Failed to retrieve balance: {response.message}")
    except Exception as e:
        print_error(f"Failed to get balance: {str(e)}")
        raise typer.Exit(1)


@app.command()
def peers(
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum number of peers to show"),
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """Get network peers information."""
    client = get_client()

    # Validate inputs
    if not validate_limit(limit):
        print_error("Invalid limit. Must be between 1 and 1000.")
        raise typer.Exit(1)

    try:
        response = client.get_peers()
        if response.success:
            peers = response.data.get('peers', [])
            # Limit the number of peers shown
            peers = peers[:limit]

            if format_type == "json":
                console.print_json(data=peers)
            else:
                # Create table
                headers = ["Peer ID", "Address", "Protocol"]
                rows = []
                for peer in peers:
                    rows.append([
                        peer.get("peer_id", "N/A"),
                        peer.get("address", "N/A"),
                        peer.get("protocol", "N/A")
                    ])

                table = format_table(headers, rows, f"Network Peers (showing {len(peers)})")
                console.print(table)
        else:
            print_error(f"Failed to retrieve peers: {response.message}")
    except Exception as e:
        print_error(f"Failed to get peers: {str(e)}")
        raise typer.Exit(1)


@app.command()
def block(
    block_hash: Optional[str] = typer.Option(None, "--hash", "-h", help="Block hash"),
    block_number: Optional[int] = typer.Option(None, "--number", "-n", help="Block number"),
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """Get block information."""
    client = get_client()

    # Validate inputs
    if block_number is not None and not validate_block_number(block_number):
        print_error("Invalid block number.")
        raise typer.Exit(1)

    if not block_hash and not block_number:
        print_error("Either block hash or block number must be provided.")
        raise typer.Exit(1)

    try:
        response = client.get_block_info(block_hash, block_number)
        if response.success:
            block_data = response.data
            if format_type == "json":
                console.print_json(data=block_data)
            else:
                console.print(f"Block Number: {block_data.get('block_number', 'N/A')}")
                console.print(f"Block Hash: {block_data.get('block_hash', 'N/A')}")
                console.print(f"Parent Hash: {block_data.get('parent_hash', 'N/A')}")
                console.print(f"State Root: {block_data.get('state_root', 'N/A')}")
                console.print(f"Extrinsics Count: {block_data.get('extrinsics_count', 'N/A')}")
                console.print(f"Timestamp: {block_data.get('timestamp', 'N/A')}")
        else:
            print_error(f"Failed to retrieve block info: {response.message}")
    except Exception as e:
        print_error(f"Failed to get block info: {str(e)}")
        raise typer.Exit(1)


@app.command()
def head(
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """Get chain head information."""
    client = get_client()

    try:
        response = client.get_chain_head()
        if response.success:
            head_data = response.data
            if format_type == "json":
                console.print_json(data=head_data)
            else:
                console.print(f"Block Number: {head_data.get('block_number', 'N/A')}")
                console.print(f"Block Hash: {head_data.get('block_hash', 'N/A')}")
                console.print(f"Parent Hash: {head_data.get('parent_hash', 'N/A')}")
                console.print(f"State Root: {head_data.get('state_root', 'N/A')}")
                console.print(f"Extrinsics Root: {head_data.get('extrinsics_root', 'N/A')}")
        else:
            print_error(f"Failed to retrieve chain head: {response.message}")
    except Exception as e:
        print_error(f"Failed to get chain head: {str(e)}")
        raise typer.Exit(1)


@app.command()
def runtime_version(
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """Get runtime version information."""
    client = get_client()

    try:
        response = client.get_runtime_version()
        if response.success:
            version_data = response.data
            if format_type == "json":
                console.print_json(data=version_data)
            else:
                console.print(f"Spec Name: {version_data.get('spec_name', 'N/A')}")
                console.print(f"Spec Version: {version_data.get('spec_version', 'N/A')}")
                console.print(f"Impl Name: {version_data.get('impl_name', 'N/A')}")
                console.print(f"Impl Version: {version_data.get('impl_version', 'N/A')}")
                console.print(f"Authoring Version: {version_data.get('authoring_version', 'N/A')}")
        else:
            print_error(f"Failed to retrieve runtime version: {response.message}")
    except Exception as e:
        print_error(f"Failed to get runtime version: {str(e)}")
        raise typer.Exit(1)
