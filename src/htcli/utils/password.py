"""
Simplified but secure password management for Hypertensor CLI.

Provides essential password handling with security features appropriate for CLI usage.
"""

import base64
import json
import logging
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Configure logging
logger = logging.getLogger(__name__)
console = Console()


# Simple cache with expiration
@dataclass
class CachedPassword:
    password: str
    expires_at: float


_password_cache: Dict[str, CachedPassword] = {}


# Configuration
class PasswordConfig:
    """Password configuration for CLI usage."""

    # Security settings
    MIN_PASSWORD_LENGTH = 8  # Reduced for CLI convenience
    CACHE_TIMEOUT = 1800  # 30 minutes
    MAX_LOGIN_ATTEMPTS = 5  # More lenient for CLI
    LOCKOUT_DURATION = 300  # 5 minutes

    # File settings
    PASSWORD_FILE = "passwords.enc"
    AUDIT_LOG_FILE = "password_audit.log"

    # Environment variables
    MASTER_KEY_ENV = "HTCLI_MASTER_KEY"
    PASSWORD_PREFIX = "HTCLI_PASSWORD_"

    # Default fallback (should be changed in production)
    DEFAULT_PASSWORD = "htcli-default-password-2024-change-me"


# Track login attempts
_login_attempts: Dict[str, tuple[int, float]] = {}


def get_secure_password(
    key_name: str,
    prompt_message: str = "Enter password",
    allow_default: bool = False,
    use_cache: bool = True,
) -> str:
    """
    Get a password with simplified but secure flow.

    Args:
        key_name: Name of the key requiring password
        prompt_message: Custom prompt message
        allow_default: Whether to allow default password fallback
        use_cache: Whether to use password caching

    Returns:
        The password string
    """
    # Check for lockout
    if is_account_locked(key_name):
        raise LockoutException(
            f"Account {key_name} is temporarily locked due to failed attempts"
        )

    try:
        # 1. Check cache first (if enabled)
        if use_cache:
            cached_password = get_cached_password(key_name)
            if cached_password:
                log_password_access(key_name, "cache", success=True)
                return cached_password

        # 2. Check environment variable
        env_password = get_environment_password(key_name)
        if env_password:
            if use_cache:
                set_cached_password(key_name, env_password)
            log_password_access(key_name, "environment", success=True)
            return env_password

        # 3. Check stored password
        stored_password = get_stored_password(key_name)
        if stored_password:
            if use_cache:
                set_cached_password(key_name, stored_password)
            log_password_access(key_name, "storage", success=True)
            return stored_password

        # 4. Prompt user for password
        password = prompt_for_password(
            message=f"{prompt_message} for {key_name}",
            min_length=PasswordConfig.MIN_PASSWORD_LENGTH,
        )

        if not password:
            if allow_default:
                log_password_access(key_name, "default", success=True)
                return PasswordConfig.DEFAULT_PASSWORD
            else:
                raise SecurityException("Password is required and cannot be empty")

        # 5. Cache and store the password
        if use_cache:
            set_cached_password(key_name, password)

        if password != PasswordConfig.DEFAULT_PASSWORD:
            store_password(key_name, password)

        log_password_access(key_name, "prompt", success=True)
        return password

    except Exception as e:
        log_password_access(key_name, "unknown", success=False, error=str(e))
        record_failed_attempt(key_name)
        raise


def prompt_for_password(
    message: str = "Enter password",
    confirm: bool = False,  # Simplified - no confirmation by default
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


def store_password(key_name: str, password: str) -> bool:
    """
    Store a password securely.

    Args:
        key_name: Name of the key
        password: Password to store

    Returns:
        True if stored successfully, False otherwise
    """
    try:
        config_dir = get_config_directory()
        password_file = config_dir / PasswordConfig.PASSWORD_FILE

        # Load existing passwords
        passwords = load_stored_passwords()
        passwords[key_name] = password

        # Encrypt and save
        encrypted_data = encrypt_passwords(passwords)
        password_file.write_bytes(encrypted_data)

        log_password_operation(key_name, "store", success=True)
        return True

    except Exception as e:
        logger.error(f"Failed to store password for {key_name}: {e}")
        log_password_operation(key_name, "store", success=False, error=str(e))
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

    except Exception as e:
        logger.error(f"Failed to retrieve stored password for {key_name}: {e}")
        return None


def load_stored_passwords() -> Dict[str, str]:
    """
    Load all stored passwords.

    Returns:
        Dictionary of stored passwords
    """
    try:
        config_dir = get_config_directory()
        password_file = config_dir / PasswordConfig.PASSWORD_FILE

        if not password_file.exists():
            return {}

        encrypted_data = password_file.read_bytes()
        return decrypt_passwords(encrypted_data)

    except Exception as e:
        logger.error(f"Failed to load stored passwords: {e}")
        return {}


def encrypt_passwords(passwords: Dict[str, str]) -> bytes:
    """
    Encrypt passwords using Fernet.

    Args:
        passwords: Dictionary of passwords to encrypt

    Returns:
        Encrypted data
    """
    master_key = get_master_key()
    data = json.dumps(passwords).encode()

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

    except Exception as e:
        logger.error(f"Failed to decrypt passwords: {e}")
        return {}


def get_master_key() -> bytes:
    """
    Get or generate a master key for encryption.

    Returns:
        Master key bytes
    """
    # Try to get from environment variable first
    env_key = os.getenv(PasswordConfig.MASTER_KEY_ENV)
    if env_key:
        return derive_key_from_password(env_key)

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


def derive_key_from_password(password: str) -> bytes:
    """
    Derive encryption key from password using PBKDF2.

    Args:
        password: Password to derive key from

    Returns:
        Derived key bytes
    """
    # Generate a deterministic salt based on the password
    import hashlib

    salt = hashlib.sha256(password.encode()).digest()[:16]

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )

    key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(key)


def get_environment_password(key_name: str) -> Optional[str]:
    """
    Get password from environment variable.

    Args:
        key_name: Name of the key

    Returns:
        Password from environment or None
    """
    env_var = f"{PasswordConfig.PASSWORD_PREFIX}{key_name.upper()}"
    return os.environ.get(env_var)


def get_cached_password(key_name: str) -> Optional[str]:
    """
    Get a password from cache with expiration check.

    Args:
        key_name: Name of the key

    Returns:
        Cached password or None if expired/not found
    """
    if key_name not in _password_cache:
        return None

    cached = _password_cache[key_name]
    if time.time() > cached.expires_at:
        del _password_cache[key_name]
        return None

    return cached.password


def set_cached_password(key_name: str, password: str) -> None:
    """
    Set a password in cache with expiration.

    Args:
        key_name: Name of the key
        password: Password to cache
    """
    expires_at = time.time() + PasswordConfig.CACHE_TIMEOUT
    _password_cache[key_name] = CachedPassword(password=password, expires_at=expires_at)


def clear_password_cache() -> None:
    """Clear the password cache."""
    global _password_cache
    _password_cache.clear()
    logger.info("Password cache cleared")


def get_config_directory() -> Path:
    """
    Get the configuration directory with proper permissions.

    Returns:
        Configuration directory path
    """
    config_dir = Path.home() / ".htcli"
    config_dir.mkdir(mode=0o700, exist_ok=True)
    return config_dir


def is_account_locked(key_name: str) -> bool:
    """
    Check if account is locked due to failed attempts.

    Args:
        key_name: Name of the key

    Returns:
        True if account is locked
    """
    if key_name not in _login_attempts:
        return False

    attempts, timestamp = _login_attempts[key_name]
    if attempts >= PasswordConfig.MAX_LOGIN_ATTEMPTS:
        if time.time() - timestamp < PasswordConfig.LOCKOUT_DURATION:
            return True
        else:
            # Reset after lockout period
            del _login_attempts[key_name]

    return False


def record_failed_attempt(key_name: str) -> None:
    """
    Record a failed login attempt.

    Args:
        key_name: Name of the key
    """
    current_time = time.time()

    if key_name in _login_attempts:
        attempts, timestamp = _login_attempts[key_name]
        # Reset if lockout period has passed
        if current_time - timestamp > PasswordConfig.LOCKOUT_DURATION:
            attempts = 0
        attempts += 1
    else:
        attempts = 1

    _login_attempts[key_name] = (attempts, current_time)

    if attempts >= PasswordConfig.MAX_LOGIN_ATTEMPTS:
        logger.warning(f"Account {key_name} locked due to {attempts} failed attempts")


def log_password_access(
    key_name: str, source: str, success: bool, error: str = None
) -> None:
    """
    Log password access attempts for audit purposes.

    Args:
        key_name: Name of the key
        source: Source of password (cache, environment, storage, prompt, default)
        success: Whether access was successful
        error: Error message if failed
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"{timestamp} | {key_name} | {source} | {'SUCCESS' if success else 'FAILED'}"
    )
    if error:
        log_entry += f" | {error}"

    # Log to file
    try:
        config_dir = get_config_directory()
        audit_file = config_dir / PasswordConfig.AUDIT_LOG_FILE
        with open(audit_file, "a") as f:
            f.write(log_entry + "\n")
    except Exception as e:
        logger.error(f"Failed to write audit log: {e}")

    # Log to application logger
    if success:
        logger.info(f"Password access successful for {key_name} from {source}")
    else:
        logger.warning(f"Password access failed for {key_name} from {source}: {error}")


def log_password_operation(
    key_name: str, operation: str, success: bool, error: str = None
) -> None:
    """
    Log password operations for audit purposes.

    Args:
        key_name: Name of the key
        operation: Operation type (store, delete, update)
        success: Whether operation was successful
        error: Error message if failed
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"{timestamp} | {key_name} | {operation} | {'SUCCESS' if success else 'FAILED'}"
    )
    if error:
        log_entry += f" | {error}"

    try:
        config_dir = get_config_directory()
        audit_file = config_dir / PasswordConfig.AUDIT_LOG_FILE
        with open(audit_file, "a") as f:
            f.write(log_entry + "\n")
    except Exception as e:
        logger.error(f"Failed to write audit log: {e}")


def show_password_help() -> None:
    """Show help information about password management."""
    help_panel = Panel(
        "[bold cyan]🔐 Simplified Password Management[/bold cyan]\n\n"
        "[bold]Password Sources (in order of priority):[/bold]\n"
        "1. [green]Cache[/green] - Recently used passwords (30 min timeout)\n"
        "2. [green]Environment Variables[/green] - HTCLI_PASSWORD_<KEYNAME>\n"
        "3. [green]Stored Passwords[/green] - Securely encrypted local storage\n"
        "4. [green]User Prompt[/green] - Interactive password input\n"
        "5. [yellow]Default Password[/yellow] - Fallback option (disabled by default)\n\n"
        "[bold]Security Features:[/bold]\n"
        "• [green]Fernet encryption[/green] for stored passwords\n"
        "• [green]Account lockout[/green] after 5 failed attempts (5 min)\n"
        "• [green]Audit logging[/green] of password operations\n"
        "• [green]Secure file permissions[/green] (700 for directories)\n"
        "• [green]Environment variable support[/green] for automation\n"
        "• [green]Password expiration[/green] in cache\n\n"
        "[bold]Password Requirements:[/bold]\n"
        f"• [green]Minimum length:[/green] {PasswordConfig.MIN_PASSWORD_LENGTH} characters\n"
        "• [green]Cannot be empty[/green]\n\n"
        "[bold]Usage Examples:[/bold]\n"
        "• Set environment variable: [cyan]export HTCLI_PASSWORD_MYKEY=mypassword[/cyan]\n"
        "• Set master key: [cyan]export HTCLI_MASTER_KEY=your-secure-master-key[/cyan]\n"
        "• Store password: [cyan]htcli wallet store-password mykey[/cyan]\n"
        "• Clear cache: [cyan]htcli wallet clear-cache[/cyan]\n\n"
        "[yellow]💡 Tips:[/yellow]\n"
        "• Use environment variables for automated scripts\n"
        "• Set a strong HTCLI_MASTER_KEY environment variable\n"
        "• Clear cache when switching between environments\n"
        "• Check audit logs for security monitoring",
        title="Password Management",
        border_style="blue",
    )
    console.print(help_panel)


# Custom exceptions for better error handling
class SecurityException(Exception):
    """Raised when security requirements are not met."""

    pass


class LockoutException(Exception):
    """Raised when account is locked due to failed attempts."""

    pass
