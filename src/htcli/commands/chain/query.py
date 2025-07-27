"""
Data query commands.
"""

import typer
from rich.console import Console
from typing import Optional
from ...utils.validation import validate_address, validate_block_number
from ...utils.formatting import print_error, format_balance, format_table
from ...dependencies import get_client

app = typer.Typer(name="query", help="Data query commands")
console = Console()


@app.command()
def balance(
    address: str = typer.Argument(..., help="Account address"),
    client = typer.Option(None, help="Client instance")
):
    """Get account balance."""
    # Get client if not provided
    if client is None:
        client = get_client()

    # Validate address
    if not validate_address(address):
        print_error("Invalid address format.")
        raise typer.Exit(1)

    try:
        response = client.get_balance(address)

        if response.data:
            balance = format_balance(response.data.get("balance", 0))
            console.print(f"Balance: {balance}")
        else:
            console.print(f"No balance found for {address}.")

    except Exception as e:
        print_error(f"Failed to get balance: {str(e)}")
        raise typer.Exit(1)


@app.command()
def peers(
    client = typer.Option(None, help="Client instance")
):
    """Get connected peers."""
    # Get client if not provided
    if client is None:
        client = get_client()

    try:
        response = client.get_peers()

        if response.data and response.data.get("peers"):
            headers = ["Peer ID", "Address", "Protocol"]
            rows = []
            for peer in response.data["peers"]:
                rows.append([
                    peer.get("peer_id", "N/A"),
                    peer.get("address", "N/A"),
                    peer.get("protocol", "N/A")
                ])

            table = format_table(headers, rows, "Connected Peers")
            console.print(table)
        else:
            console.print("No peers connected.")

    except Exception as e:
        print_error(f"Failed to get peers: {str(e)}")
        raise typer.Exit(1)


@app.command()
def block(
    block_number: Optional[int] = typer.Argument(None, help="Block number (default: latest)"),
    client = typer.Option(None, help="Client instance")
):
    """Get block information."""
    # Get client if not provided
    if client is None:
        client = get_client()

    # Validate block number if provided
    if block_number is not None and not validate_block_number(block_number):
        print_error("Invalid block number.")
        raise typer.Exit(1)

    try:
        response = client.get_block_info(block_number)

        if response.data:
            from rich.panel import Panel
            block_data = response.data
            info_text = f"""
Block Number: {block_data.get('number', 'N/A')}
Block Hash: {block_data.get('hash', 'N/A')}
Parent Hash: {block_data.get('parent_hash', 'N/A')}
Extrinsics: {len(block_data.get('extrinsics', []))}
            """
            console.print(Panel(info_text, title="Block Information"))
        else:
            console.print("Block not found.")

    except Exception as e:
        print_error(f"Failed to get block info: {str(e)}")
        raise typer.Exit(1)
