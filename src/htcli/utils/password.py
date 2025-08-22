"""
Simplified but secure password management for Hypertensor CLI.

Provides essential password handling with security features appropriate for CLI usage.
"""

import logging
from typing import Optional

from rich.console import Console
from rich.prompt import Prompt

# Configure logging
logger = logging.getLogger(__name__)
console = Console()


class PasswordConfig:
    """Password configuration for CLI usage."""

    MIN_PASSWORD_LENGTH = 8  # Minimum password length


def get_secure_password(
    key_name: str,
    prompt_message: str = "Enter password",
    allow_default: bool = False,
) -> str:
    """
    Prompt the user for a password with basic validation.

    Args:
        key_name: Name of the key requiring password
        prompt_message: Custom prompt message
        allow_default: Whether to allow default password fallback

    Returns:
        The password string
    """
    while True:
        try:
            password = prompt_for_password(
                message=f"{prompt_message} for {key_name}",
                min_length=PasswordConfig.MIN_PASSWORD_LENGTH,
            )

            if not password:
                if allow_default:
                    return ""
                else:
                    raise SecurityException("Password is required and cannot be empty")

            return password

        except KeyboardInterrupt:
            console.print("\n[yellow]Password input cancelled.[/yellow]")
            raise


def prompt_for_password(
    message: str = "Enter password",
    confirm: bool = False,
    min_length: int = None,
) -> str:
    """
    Prompt user for a password with basic validation.

    Args:
        message: Password prompt message
        confirm: Whether to require password confirmation
        min_length: Minimum password length

    Returns:
        The password
    """
    min_length = min_length or PasswordConfig.MIN_PASSWORD_LENGTH

    while True:
        try:
            password = Prompt.ask(message, password=True)

            if not password:
                console.print("[red]Password cannot be empty[/red]")
                continue

            if len(password) < min_length:
                console.print(
                    f"[red]Password must be at least {min_length} characters long[/red]"
                )
                continue

            if confirm:
                confirm_password = Prompt.ask("Confirm password", password=True)
                if password != confirm_password:
                    console.print(
                        "[red]Passwords do not match. Please try again.[/red]"
                    )
                    continue

            return password

        except KeyboardInterrupt:
            console.print("\n[yellow]Password input cancelled.[/yellow]")
            return ""


def show_password_help() -> None:
    """Show help information about password management."""
    console.print(
        "[bold cyan]🔐 Password Prompt Only Mode[/bold cyan]\n\n"
        "[bold]How it works:[/bold]\n"
        "• You will be prompted for your password each time it is needed.\n"
        "• Passwords are never cached or stored on disk.\n\n"
        "[bold]Password Requirements:[/bold]\n"
        f"• [green]Minimum length:[/green] {PasswordConfig.MIN_PASSWORD_LENGTH} characters\n"
        "• [green]Cannot be empty[/green]\n\n"
        "[bold]Usage Example:[/bold]\n"
        "• When prompted, enter your password securely in the terminal.\n"
        "[yellow]💡 Tips:[/yellow]\n"
        "• Use a strong password and do not share it with others."
    )


# Custom exceptions for better error handling
class SecurityException(Exception):
    """Raised when security requirements are not met."""

    pass
