"""
Base error classes for htcli.
"""

from typing import List, Optional
from rich.console import Console

console = Console()


class HTCLIError(Exception):
    """Base exception class for htcli errors."""

    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        self.message = message
        self.suggestions = suggestions or []
        super().__init__(self.message)

    def display(self):
        """Display the error with suggestions."""
        console.print(f"❌ {self.message}")

        if self.suggestions:
            console.print("\n[bold yellow]💡 Helpful Suggestions:[/bold yellow]")
            for suggestion in self.suggestions:
                console.print(f"• {suggestion}")


class WalletError(HTCLIError):
    """Base class for wallet-related errors."""
    pass


class TransferError(HTCLIError):
    """Base class for transfer-related errors."""
    pass


class BalanceError(HTCLIError):
    """Base class for balance-related errors."""
    pass


class KeyGenerationError(HTCLIError):
    """Base class for key generation errors."""
    pass


class KeyDeletionError(HTCLIError):
    """Base class for key deletion errors."""
    pass
