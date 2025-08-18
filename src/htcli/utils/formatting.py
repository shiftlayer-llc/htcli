"""
Output formatting utility functions for the Hypertensor CLI.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Any, Dict, List
import json

# TENSOR token precision constant
TENSOR_DECIMALS = 18


def tensor_to_smallest_unit(tensor_amount: float) -> int:
    """Convert TENSOR amount to smallest unit (18 decimals)."""
    return int(tensor_amount * (10**TENSOR_DECIMALS))


def smallest_unit_to_tensor(smallest_unit: int) -> float:
    """Convert smallest unit to TENSOR amount (18 decimals)."""
    return smallest_unit / (10**TENSOR_DECIMALS)


def validate_tensor_amount(amount: float) -> bool:
    """Validate TENSOR amount has proper precision."""
    # Check if amount has more than 18 decimal places
    str_amount = f"{amount:.18f}"
    if len(str_amount.split(".")[-1]) > TENSOR_DECIMALS:
        return False
    return True


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


def format_balance(amount: int, decimals: int = TENSOR_DECIMALS) -> str:
    """Format balance amount with proper decimal places for TENSOR token (18 decimals)."""
    if amount == 0:
        return "0 TENSOR"

    # Convert from smallest unit (18 decimals for TENSOR)
    balance = amount / (10**decimals)
    return f"{balance:.18f} TENSOR".rstrip("0").rstrip(".")


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
            stake,
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
            stake,
        )

    return table


def create_stake_info_panel(
    stake_data: Dict[str, Any], subnet_id: int, hotkey: str
) -> Panel:
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
        status = "Active" if subnet.get("activated", 0) > 0 else "Inactive"
        table.add_row(
            str(subnet.get("subnet_id", "N/A")),
            subnet.get("path", "N/A"),
            status,
            str(subnet.get("node_count", 0)),
            format_balance(subnet.get("total_stake", 0)),
        )

    console.print(table)


def format_subnet_info(subnet_info: Dict[str, Any]):
    """Format and display comprehensive subnet information."""
    if not subnet_info:
        console.print("Subnet information not available.")
        return

    # Check data completeness
    data_completeness = subnet_info.get("data_completeness", "unknown")
    is_partial = data_completeness == "partial"

    # Basic Information Section
    basic_info = f"""[bold cyan]Basic Information:[/bold cyan]
Subnet ID: {subnet_info.get('subnet_id', 'N/A')}
Name: {subnet_info.get('name', 'N/A')}
Repository: {subnet_info.get('repo', 'N/A') or 'Not specified'}
Description: {subnet_info.get('description', 'N/A') or 'Not specified'}
State: {subnet_info.get('state', 'N/A')}
Owner: {subnet_info.get('owner', 'N/A') or 'Not assigned'}
Start Epoch: {subnet_info.get('start_epoch', 'N/A')}
Registration Epoch: {subnet_info.get('registration_epoch', 'N/A')}"""

    # Node Information Section
    node_info = f"""[bold green]Node Information:[/bold green]
Total Nodes: {subnet_info.get('total_nodes', 0)}
Active Nodes: {subnet_info.get('total_active_nodes', 0)}
Max Registered Nodes: {subnet_info.get('max_registered_nodes', 0)}
Node Registration Epochs: {subnet_info.get('node_registration_epochs', 0)}
Node Activation Interval: {subnet_info.get('node_activation_interval', 0)}
Churn Limit: {subnet_info.get('churn_limit', 0)}"""

    # Staking Information Section
    min_stake = subnet_info.get("min_stake", 0)
    max_stake = subnet_info.get("max_stake", 0)
    delegate_stake_balance = subnet_info.get("total_delegate_stake_balance", 0)
    delegate_stake_shares = subnet_info.get("total_delegate_stake_shares", 0)

    staking_info = f"""[bold yellow]Staking Information:[/bold yellow]
Minimum Stake: {format_balance(min_stake)}
Maximum Stake: {format_balance(max_stake)}
Delegate Stake Percentage: {subnet_info.get('delegate_stake_percentage', 0) / 1000000:.1f}%
Total Delegate Stake Balance: {format_balance(delegate_stake_balance)}
Total Delegate Stake Shares: {delegate_stake_shares}"""

    # System Information Section
    system_info = f"""[bold red]System Information:[/bold red]
Max Node Penalties: {subnet_info.get('max_node_penalties', 0)}
Penalty Count: {subnet_info.get('penalty_count', 0)}
Data Completeness: {data_completeness.title()}"""

    # Combine all sections
    full_info = f"{basic_info}\n\n{node_info}\n\n{staking_info}\n\n{system_info}"

    # Additional info section
    misc = subnet_info.get("misc", "")
    if misc:
        full_info += f"\n\n[bold blue]Additional Information:[/bold blue]\n{misc}"

    # Add note for partial data
    if is_partial:
        full_info += "\n\n[bold yellow]⚠️ Note:[/bold yellow] This subnet exists but has partial registration data.\nSome fields may show default values or be unavailable."

    # Set title and border based on data completeness
    title = "📊 Subnet Information"
    if is_partial:
        title += " (Partial Data)"
    border_style = "yellow" if is_partial else "cyan"

    panel = Panel(full_info, title=title, border_style=border_style)
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
            str(node.get("node_id", "N/A")),
            format_address(node.get("peer_id", "N/A")),
            format_address(node.get("hotkey", "N/A")),
            format_balance(node.get("stake", 0)),
            node.get("status", "N/A"),
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
        console=console,
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
