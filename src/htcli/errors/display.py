"""
Display utility functions for error handling.
"""

from rich.console import Console

console = Console()


def display_balance_info(address: str, balance: float = 0):
    """Display helpful information when balance is 0."""
    if balance == 0:
        console.print(
            "\n[bold yellow]💡 Note:[/bold yellow] This wallet has no balance."
        )
        console.print(f"• To receive funds, share this address: [bold]{address}[/bold]")
        console.print(
            "• You can transfer funds from another wallet using: [bold]htcli wallet transfer[/bold]"
        )
        console.print("• Transaction fees are typically around 0.001-0.01 TENSOR")
