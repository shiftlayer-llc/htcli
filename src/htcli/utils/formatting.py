"""
Output formatting utility functions for the Hypertensor CLI.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Any, Dict, List, Optional
import json


console = Console()


def format_table(headers: List[str], rows: List[List[Any]], title: str = "") -> Table:
    """Create a formatted table."""
    table = Table(title=title)

    # Add columns
    for header in headers:
        table.add_column(header, style="cyan")

    # Add rows
    for row in rows:
        table.add_row(*[str(cell) for cell in row])

    return table


def format_json(data: Any) -> str:
    """Format data as JSON."""
    return json.dumps(data, indent=2, default=str)


def format_csv(headers: List[str], rows: List[List[Any]]) -> str:
    """Format data as CSV."""
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)
    return output.getvalue()


def print_success(message: str):
    """Print a success message."""
    console.print(f"✅ {message}", style="green")


def print_error(message: str):
    """Print an error message."""
    console.print(f"❌ {message}", style="red")


def print_warning(message: str):
    """Print a warning message."""
    console.print(f"⚠️  {message}", style="yellow")


def print_info(message: str):
    """Print an info message."""
    console.print(f"ℹ️  {message}", style="blue")


def format_balance(amount: int, decimals: int = 9) -> str:
    """Format balance amount with proper decimal places."""
    if amount == 0:
        return "0 TENSOR"

    # Convert from smallest unit
    balance = amount / (10 ** decimals)
    return f"{balance:.9f} TENSOR".rstrip('0').rstrip('.')


def format_address(address: str, max_length: int = 20) -> str:
    """Format address with truncation."""
    if len(address) <= max_length:
        return address
    return f"{address[:max_length//2]}...{address[-max_length//2:]}"


def format_block_number(block_number: int) -> str:
    """Format block number."""
    return f"#{block_number:,}"


def format_transaction_hash(tx_hash: str) -> str:
    """Format transaction hash."""
    if len(tx_hash) <= 16:
        return tx_hash
    return f"{tx_hash[:8]}...{tx_hash[-8:]}"


def create_subnet_table(subnets: List[Dict[str, Any]]) -> Table:
    """Create a table for subnet information."""
    table = Table(title="Subnets")
    table.add_column("ID", style="cyan")
    table.add_column("Path", style="white")
    table.add_column("Status", style="green")
    table.add_column("Nodes", style="yellow")
    table.add_column("Stake", style="magenta")

    for subnet in subnets:
        status = "Active" if subnet.get("activated", 0) > 0 else "Inactive"
        stake = format_balance(subnet.get("total_stake", 0))

        table.add_row(
            str(subnet.get("subnet_id", "N/A")),
            subnet.get("path", "N/A"),
            status,
            str(subnet.get("node_count", 0)),
            stake
        )

    return table


def create_node_table(nodes: List[Dict[str, Any]], subnet_id: int) -> Table:
    """Create a table for node information."""
    table = Table(title=f"Nodes in Subnet {subnet_id}")
    table.add_column("Node ID", style="cyan")
    table.add_column("Peer ID", style="white")
    table.add_column("Hotkey", style="green")
    table.add_column("Stake", style="yellow")

    for node in nodes:
        stake = format_balance(node.get("stake", 0))

        table.add_row(
            str(node.get("node_id", "N/A")),
            format_address(node.get("peer_id", "N/A")),
            format_address(node.get("hotkey", "N/A")),
            stake
        )

    return table


def create_stake_info_panel(stake_data: Dict[str, Any], subnet_id: int, hotkey: str) -> Panel:
    """Create a panel for stake information."""
    stake_amount = format_balance(stake_data.get("stake", 0))
    unbonding = format_balance(stake_data.get("unbonding", 0))

    info_text = f"""
Subnet ID: {subnet_id}
Hotkey: {format_address(hotkey)}
Stake Amount: {stake_amount}
Unbonding: {unbonding}
    """

    return Panel(info_text, title="Stake Information")


def create_network_stats_panel(stats: Dict[str, Any]) -> Panel:
    """Create a panel for network statistics."""
    total_stake = format_balance(stats.get("total_stake", 0))

    info_text = f"""
Total Subnets: {stats.get('total_subnets', 0)}
Active Subnets: {stats.get('active_subnets', 0)}
Total Nodes: {stats.get('total_nodes', 0)}
Total Stake: {total_stake}
Current Epoch: {stats.get('current_epoch', 0)}
    """

    return Panel(info_text, title="Network Statistics")


def create_account_info_panel(account_data: Dict[str, Any], address: str) -> Panel:
    """Create a panel for account information."""
    balance = format_balance(account_data.get("balance", 0))

    info_text = f"""
Address: {format_address(address)}
Balance: {balance}
Nonce: {account_data.get('nonce', 0)}
    """

    return Panel(info_text, title="Account Information")


def create_epoch_info_panel(epoch_data: Dict[str, Any]) -> Panel:
    """Create a panel for epoch information."""
    info_text = f"""
Epoch: {epoch_data.get('epoch', 'N/A')}
Start Block: {epoch_data.get('start_block', 'N/A')}
End Block: {epoch_data.get('end_block', 'N/A')}
Blocks Remaining: {epoch_data.get('blocks_remaining', 'N/A')}
Epoch Duration: {epoch_data.get('epoch_duration', 'N/A')} blocks
Timestamp: {epoch_data.get('timestamp', 'N/A')}
    """
    return Panel(info_text, title="Epoch Information")


def format_subnet_list(subnets: List[Dict[str, Any]]):
    """Format and display subnet list."""
    if not subnets:
        console.print("No subnets found.")
        return

    table = Table(title="Subnets")
    table.add_column("ID", style="cyan")
    table.add_column("Path", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Nodes", style="blue")
    table.add_column("Total Stake", style="magenta")

    for subnet in subnets:
        status = "Active" if subnet.get('activated', 0) > 0 else "Inactive"
        table.add_row(
            str(subnet.get('subnet_id', 'N/A')),
            subnet.get('path', 'N/A'),
            status,
            str(subnet.get('node_count', 0)),
            format_balance(subnet.get('total_stake', 0))
        )

    console.print(table)


def format_subnet_info(subnet_info: Dict[str, Any]):
    """Format and display subnet information."""
    if not subnet_info:
        console.print("Subnet information not available.")
        return

    info_text = f"""
Subnet ID: {subnet_info.get('subnet_id', 'N/A')}
Path: {subnet_info.get('path', 'N/A')}
Status: {'Active' if subnet_info.get('activated', 0) > 0 else 'Inactive'}
Registration Cost: {format_balance(subnet_info.get('registration_cost', 0))}
Node Count: {subnet_info.get('node_count', 0)}
Total Stake: {format_balance(subnet_info.get('total_stake', 0))}
Memory: {subnet_info.get('memory_mb', 0)} MB
Registration Blocks: {subnet_info.get('registration_blocks', 0)}
Entry Interval: {subnet_info.get('entry_interval', 0)}
    """

    panel = Panel(info_text, title="Subnet Information")
    console.print(panel)


def format_node_list(nodes: List[Dict[str, Any]]):
    """Format and display node list."""
    if not nodes:
        console.print("No nodes found.")
        return

    table = Table(title="Subnet Nodes")
    table.add_column("Node ID", style="cyan")
    table.add_column("Peer ID", style="green")
    table.add_column("Hotkey", style="yellow")
    table.add_column("Stake", style="blue")
    table.add_column("Status", style="magenta")

    for node in nodes:
        table.add_row(
            str(node.get('node_id', 'N/A')),
            format_address(node.get('peer_id', 'N/A')),
            format_address(node.get('hotkey', 'N/A')),
            format_balance(node.get('stake', 0)),
            node.get('status', 'N/A')
        )

    console.print(table)


def format_stake_info(stake_data: Dict[str, Any]):
    """Format and display stake information."""
    if not stake_data:
        console.print("Stake information not available.")
        return

    info_text = f"""
Account: {format_address(stake_data.get('account', 'N/A'))}
Subnet ID: {stake_data.get('subnet_id', 'N/A')}
Current Stake: {format_balance(stake_data.get('stake', 0))}
Unbonding: {format_balance(stake_data.get('unbonding', 0))}
Total Stake: {format_balance(stake_data.get('total_stake', 0))}
    """

    panel = Panel(info_text, title="Stake Information")
    console.print(panel)


def format_network_stats(stats: Dict[str, Any]):
    """Format and display network statistics."""
    if not stats:
        console.print("Network statistics not available.")
        return

    info_text = f"""
Total Subnets: {stats.get('total_subnets', 0)}
Active Subnets: {stats.get('active_subnets', 0)}
Total Nodes: {stats.get('total_nodes', 0)}
Total Stake: {format_balance(stats.get('total_stake', 0))}
Current Epoch: {stats.get('current_epoch', 0)}
Total Validations: {stats.get('total_validations', 0)}
Total Attestations: {stats.get('total_attestations', 0)}
Network Uptime: {stats.get('network_uptime', 0)}%
Average Block Time: {stats.get('average_block_time', 0)}s
    """

    panel = Panel(info_text, title="Network Statistics")
    console.print(panel)


def format_account_info(account_data: Dict[str, Any]):
    """Format and display account information."""
    if not account_data:
        console.print("Account information not available.")
        return

    info_text = f"""
Account: {format_address(account_data.get('account', 'N/A'))}
Balance: {format_balance(account_data.get('balance', 0))}
Nonce: {account_data.get('nonce', 0)}
Reserved: {format_balance(account_data.get('reserved', 0))}
Misc Frozen: {format_balance(account_data.get('misc_frozen', 0))}
Fee Frozen: {format_balance(account_data.get('fee_frozen', 0))}
    """

    panel = Panel(info_text, title="Account Information")
    console.print(panel)


def format_epoch_info(epoch_data: Dict[str, Any]):
    """Format and display epoch information."""
    if not epoch_data:
        console.print("Epoch information not available.")
        return

    info_text = f"""
Epoch: {epoch_data.get('epoch', 'N/A')}
Start Block: {epoch_data.get('start_block', 'N/A')}
End Block: {epoch_data.get('end_block', 'N/A')}
Blocks Remaining: {epoch_data.get('blocks_remaining', 'N/A')}
Epoch Duration: {epoch_data.get('epoch_duration', 'N/A')} blocks
Timestamp: {epoch_data.get('timestamp', 'N/A')}
    """

    panel = Panel(info_text, title="Epoch Information")
    console.print(panel)


def show_progress(description: str):
    """Show a progress spinner."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(description, total=None)
        return progress, task


def output_data(data: Any, format_type: str = "table"):
    """Output data in the specified format."""
    if format_type == "json":
        console.print(format_json(data))
    elif format_type == "csv":
        console.print(format_csv(data))
    else:
        # Default to table format
        if isinstance(data, list) and data:
            # Try to create a table from list of dictionaries
            if isinstance(data[0], dict):
                headers = list(data[0].keys())
                rows = [[row.get(header, "") for header in headers] for row in data]
                table = format_table(headers, rows)
                console.print(table)
            else:
                console.print(data)
        else:
            console.print(data)
