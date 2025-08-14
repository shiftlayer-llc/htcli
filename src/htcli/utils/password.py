#!/usr/bin/env python3
"""
Password management utilities for Hypertensor CLI.

Provides secure password handling, caching, and configuration integration.
"""

import os
import getpass
from typing import Optional, Dict, Any
from pathlib import Path
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

# Global password cache
_password_cache: Dict[str, str] = {}

# Configuration for password management
DEFAULT_PASSWORD = "default_password_12345"  # Fallback password
PASSWORD_CACHE_TIMEOUT = 300  # 5 minutes
PASSWORD_FILE = "passwords.enc"


def get_secure_password(
    key_name: str,
    prompt_message: str = "Enter password",
    allow_default: bool = True,
    use_cache: bool = True
) -> str:
    """
    Get a secure password for a key, with caching and fallback options.

    Args:
        key_name: Name of the key requiring password
        prompt_message: Custom prompt message
        allow_default: Whether to allow default password fallback
        use_cache: Whether to use password caching

    Returns:
        The password string
    """
    # Check cache first
    if use_cache and key_name in _password_cache:
        return _password_cache[key_name]

    # Try to get from environment variable
    env_var = f"HTCLI_PASSWORD_{key_name.upper()}"
    if env_var in os.environ:
        password = os.environ[env_var]
        if use_cache:
            _password_cache[key_name] = password
        return password

    # Try to get from stored passwords
    stored_password = get_stored_password(key_name)
    if stored_password:
        if use_cache:
            _password_cache[key_name] = stored_password
        return stored_password

    # Prompt user for password
    try:
        password = Prompt.ask(
            f"{prompt_message} for {key_name}",
            password=True,
            default=DEFAULT_PASSWORD if allow_default else None
        )

        # Cache the password
        if use_cache and password:
            _password_cache[key_name] = password

        # Store the password for future use
        if password and password != DEFAULT_PASSWORD:
            store_password(key_name, password)

        return password

    except KeyboardInterrupt:
        console.print("\n[yellow]Password input cancelled. Using default password.[/yellow]")
        return DEFAULT_PASSWORD if allow_default else ""


def prompt_for_password(
    message: str = "Enter password",
    confirm: bool = True,
    min_length: int = 8
) -> str:
    """
    Prompt user for a password with optional confirmation.

    Args:
        message: Password prompt message
        confirm: Whether to require password confirmation
        min_length: Minimum password length

    Returns:
        The confirmed password
    """
    while True:
        try:
            password = Prompt.ask(message, password=True)

            if len(password) < min_length:
                console.print(f"[red]Password must be at least {min_length} characters long[/red]")
                continue

            if confirm:
                confirm_password = Prompt.ask("Confirm password", password=True)
                if password != confirm_password:
                    console.print("[red]Passwords do not match. Please try again.[/red]")
                    continue

            return password

        except KeyboardInterrupt:
            console.print("\n[yellow]Password input cancelled.[/yellow]")
            return ""


def store_password(key_name: str, password: str) -> bool:
    """
    Store a password securely for future use.

    Args:
        key_name: Name of the key
        password: Password to store

    Returns:
        True if stored successfully, False otherwise
    """
    try:
        # Get the config directory
        config_dir = Path.home() / ".htcli"
        config_dir.mkdir(exist_ok=True)

        password_file = config_dir / PASSWORD_FILE

        # Load existing passwords
        passwords = load_stored_passwords()
        passwords[key_name] = password

        # Encrypt and save
        encrypted_data = encrypt_passwords(passwords)
        password_file.write_bytes(encrypted_data)

        return True

    except Exception as e:
        console.print(f"[red]Failed to store password: {str(e)}[/red]")
        return False


def get_stored_password(key_name: str) -> Optional[str]:
    """
    Retrieve a stored password.

    Args:
        key_name: Name of the key

    Returns:
        The stored password or None if not found
    """
    try:
        passwords = load_stored_passwords()
        return passwords.get(key_name)

    except Exception:
        return None


def load_stored_passwords() -> Dict[str, str]:
    """
    Load all stored passwords.

    Returns:
        Dictionary of stored passwords
    """
    try:
        config_dir = Path.home() / ".htcli"
        password_file = config_dir / PASSWORD_FILE

        if not password_file.exists():
            return {}

        encrypted_data = password_file.read_bytes()
        return decrypt_passwords(encrypted_data)

    except Exception:
        return {}


def encrypt_passwords(passwords: Dict[str, str]) -> bytes:
    """
    Encrypt passwords for storage.

    Args:
        passwords: Dictionary of passwords to encrypt

    Returns:
        Encrypted data
    """
    # Generate a key from a master password or system key
    master_key = get_master_key()

    # Convert passwords to JSON
    data = json.dumps(passwords).encode()

    # Encrypt
    f = Fernet(master_key)
    return f.encrypt(data)


def decrypt_passwords(encrypted_data: bytes) -> Dict[str, str]:
    """
    Decrypt stored passwords.

    Args:
        encrypted_data: Encrypted password data

    Returns:
        Dictionary of decrypted passwords
    """
    try:
        master_key = get_master_key()
        f = Fernet(master_key)
        decrypted_data = f.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())

    except Exception:
        return {}


def get_master_key() -> bytes:
    """
    Get or generate a master key for password encryption.

    Returns:
        Master key bytes
    """
    # Use a system-specific key for simplicity
    # In production, this should be more secure
    system_key = os.getenv("HTCLI_MASTER_KEY", "htcli-default-master-key-2024")

    # Generate a key from the system key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"htcli-salt-2024",
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(system_key.encode()))
    return key


def clear_password_cache() -> None:
    """Clear the password cache."""
    global _password_cache
    _password_cache.clear()


def get_cached_password(key_name: str) -> Optional[str]:
    """
    Get a password from cache.

    Args:
        key_name: Name of the key

    Returns:
        Cached password or None
    """
    return _password_cache.get(key_name)


def set_cached_password(key_name: str, password: str) -> None:
    """
    Set a password in cache.

    Args:
        key_name: Name of the key
        password: Password to cache
    """
    _password_cache[key_name] = password


def show_password_help() -> None:
    """Show help information about password management."""
    help_panel = Panel(
        "[bold cyan]🔐 Password Management Help[/bold cyan]\n\n"
        "[bold]Password Sources (in order of priority):[/bold]\n"
        "1. [green]Cache[/green] - Recently used passwords\n"
        "2. [green]Environment Variables[/green] - HTCLI_PASSWORD_<KEYNAME>\n"
        "3. [green]Stored Passwords[/green] - Securely encrypted local storage\n"
        "4. [green]User Prompt[/green] - Interactive password input\n"
        "5. [yellow]Default Password[/yellow] - Fallback option\n\n"
        "[bold]Security Features:[/bold]\n"
        "• [green]Encrypted storage[/green] using Fernet encryption\n"
        "• [green]Password caching[/green] for convenience\n"
        "• [green]Environment variable support[/green] for automation\n"
        "• [green]Minimum length validation[/green] for new passwords\n"
        "• [green]Password confirmation[/green] for new passwords\n\n"
        "[bold]Usage Examples:[/bold]\n"
        "• Set environment variable: [cyan]export HTCLI_PASSWORD_MYKEY=mypassword[/cyan]\n"
        "• Store password: [cyan]htcli wallet store-password mykey[/cyan]\n"
        "• Clear cache: [cyan]htcli wallet clear-cache[/cyan]\n\n"
        "[yellow]💡 Tip:[/yellow] Use environment variables for automated scripts\n"
        "[yellow]💡 Tip:[/yellow] Store frequently used passwords for convenience\n"
        "[yellow]💡 Tip:[/yellow] Clear cache when switching between environments",
        title="Password Management",
        border_style="blue"
    )
    console.print(help_panel)
