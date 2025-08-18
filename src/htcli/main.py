"""
Main CLI entry point for the Hypertensor CLI.
"""

import typer
from rich.console import Console
from pathlib import Path
from typing import Optional

from .commands.subnet import app as subnet_app
from .commands.wallet import app as wallet_app
from .commands.chain import app as chain_app
from .commands.config import app as config_app
from .commands.node import app as node_app
from .commands.stake import app as stake_app
from .commands.flow import app as flow_app
from .config import load_config
from .dependencies import set_config


def get_ascii_art():
    """Return  ASCII art for the CLI."""
    return """
    ██╗  ██╗████████╗ ██████╗██╗     ██╗
    ██║  ██║╚══██╔══╝██╔════╝██║     ██║
    ███████║   ██║   ██║     ██║     ██║
    ██╔══██║   ██║   ██║     ██║     ██║
    ██║  ██║   ██║   ╚██████╗███████╗██║
    ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚══════╝╚═╝
    """


app = typer.Typer(
    name="htcli",
    help="Hypertensor Blockchain CLI - Manage subnets, wallets, and chain operations.",
    add_completion=True,
    rich_markup_mode="rich",
    no_args_is_help=False,
)

console = Console()

# Global configuration
config = None


@app.callback(invoke_without_command=True)
def main(
    config_file: Optional[Path] = typer.Option(
        None, "--config", "-c", help="Configuration file path"
    ),
    endpoint: Optional[str] = typer.Option(
        None, "--endpoint", "-e", help="Blockchain endpoint"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    output_format: str = typer.Option(
        "table", "--format", "-f", help="Output format (table/json/csv)"
    ),
    mine: bool = typer.Option(
        False, "--mine", "-m", help="Filter results to show only your assets"
    ),
):
    """Hypertensor Blockchain CLI - Manage subnets, wallets, and chain operations."""
    global config

    # Show beautiful welcome screen when no command is provided
    import sys

    if len(sys.argv) == 1:
        from rich.panel import Panel
        from rich.table import Table
        from rich.text import Text

        # Display ASCII art first
        console.print(get_ascii_art())
        console.print()

        # Create a beautiful welcome panel
        welcome_text = Text()
        welcome_text.append("Welcome to ", style="bold white")
        welcome_text.append("Hypertensor CLI", style="bold cyan")
        welcome_text.append(
            "\nYour gateway to the Hypertensor blockchain ecosystem", style="italic dim"
        )

        welcome_panel = Panel(
            welcome_text,
            title="[bold cyan]HTCLI[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )

        console.print(welcome_panel)
        console.print()

        # Create command categories table
        table = Table(
            title="[bold cyan]Available Commands[/bold cyan]",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Category", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Example", style="dim")

        table.add_row("config", "Configuration management", "htcli config init")
        table.add_row("subnet", "Subnet operations", "htcli subnet list")
        table.add_row("node", "Node management", "htcli node add --subnet-id 1")
        table.add_row(
            "stake", "Staking operations", "htcli stake add --subnet-id 1 --amount 100"
        )
        table.add_row("wallet", "Wallet management", "htcli wallet generate-key")
        table.add_row("chain", "Chain operations", "htcli chain network")
        table.add_row("flow", "Automated workflows", "htcli flow list")

        console.print(table)
        console.print()

        # Quick tips section
        tips_panel = Panel(
            "[bold yellow]Quick Tips:[/bold yellow]\n"
            "• [bold cyan]🔑 Setup Keys:[/bold cyan] htcli wallet generate-key --name my-wallet\n"
            "• [bold cyan]Check Identity:[/bold cyan] htcli wallet status\n"
            "• [bold cyan]Filter Assets:[/bold cyan] Use --mine to see only your assets\n"
            "• [bold cyan]Get Help:[/bold cyan] Use --help with any command\n"
            "• [bold cyan]JSON Output:[/bold cyan] Use --format json for scripts",
            title="[bold yellow]💡 Getting Started[/bold yellow]",
            border_style="yellow",
        )

        console.print(tips_panel)
        raise typer.Exit()

    # Load configuration
    config = load_config(config_file)

    # Override endpoint if provided
    if endpoint:
        config.network.endpoint = endpoint

    # Set global options
    config.output.verbose = verbose
    config.output.format = output_format
    config.filter.mine = mine

    # Store config globally for lazy client initialization
    # Client will be initialized only when needed for blockchain operations
    set_config(config)


# Include the main command groups with flattened structure
app.add_typer(config_app, name="config", help="Configuration management")
app.add_typer(subnet_app, name="subnet", help="Subnet operations")
app.add_typer(node_app, name="node", help="Node management operations")
app.add_typer(stake_app, name="stake", help="Staking operations and management")
app.add_typer(wallet_app, name="wallet", help="Wallet and key management")
app.add_typer(chain_app, name="chain", help="Chain operations")
app.add_typer(flow_app, name="flow", help="Automated workflows for common tasks")


if __name__ == "__main__":
    app()
