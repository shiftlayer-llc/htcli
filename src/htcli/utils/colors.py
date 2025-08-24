"""
Standardized color scheme for htcli application.

This module provides eye-friendly colors based on medical research and terminal compatibility.
Colors are designed to reduce eye strain and work well across different terminal environments.
"""

from enum import Enum
from typing import Optional


class ColorScheme(Enum):
    """Available color schemes for different terminal environments."""

    DEFAULT = "default"
    DARK = "dark"
    LIGHT = "light"
    HIGH_CONTRAST = "high_contrast"
    SOFT = "soft"


class Colors:
    """
    Standardized color palette for htcli.

    - Avoid pure white (#FFFFFF) - too bright and causes eye strain
    - Avoid pure black (#000000) - too harsh contrast
    - Avoid deep greens - can cause eye fatigue
    - Use softer, muted colors with lower saturation
    - Ensure good contrast ratios without being harsh
    - Work well in both light and dark terminals
    - Use colors that reduce blue light exposure
    """

    # Primary colors - Soft, eye-friendly alternatives
    PRIMARY = "bright_blue"  # Soft blue - good for primary elements
    SECONDARY = "cyan"  # Gentle cyan - good for secondary info
    SUCCESS = "bright_green"  # Softer green - less harsh than deep green
    WARNING = "yellow"  # Gentle yellow - warnings
    ERROR = "bright_red"  # Softer red - less harsh than deep red
    INFO = "blue"  # Soft blue - informational

    # Text colors - Easy on the eyes, avoiding pure white
    TEXT_PRIMARY = "bright_white"  # Softer white for primary text
    TEXT_SECONDARY = "bright_black"  # Soft gray for secondary text
    TEXT_MUTED = "dim"  # Very soft gray for muted text

    # Background colors - Subtle and non-intrusive
    BG_PRIMARY = "black"  # Standard terminal background
    BG_SECONDARY = "bright_black"  # Slightly lighter background
    BG_HIGHLIGHT = "blue"  # Subtle highlight background

    # Border colors - Clean and professional, avoiding harsh whites
    BORDER_PRIMARY = "bright_white"  # Softer white borders
    BORDER_SECONDARY = "bright_black"  # Subtle borders

    # Status colors - Clear but not harsh
    STATUS_ONLINE = "bright_green"  # Softer green for online/active
    STATUS_OFFLINE = "bright_red"  # Softer red for offline/inactive
    STATUS_PENDING = "yellow"  # Gentle yellow for pending/waiting

    # Balance colors - Financial clarity with eye-friendly alternatives
    BALANCE_POSITIVE = "bright_green"  # Softer green for positive balances
    BALANCE_NEGATIVE = "bright_red"  # Softer red for negative balances
    BALANCE_ZERO = "bright_black"  # Soft gray for zero balances

    # Wallet colors - Clear identification with softer tones
    WALLET_COLDKEY = "cyan"  # Cyan for coldkey identification
    WALLET_HOTKEY = "blue"  # Blue for hotkey identification
    WALLET_ADDRESS = "bright_green"  # Softer green for address display

    # Table colors - Professional appearance with reduced eye strain
    TABLE_HEADER = "bright_white"  # Softer white for headers
    TABLE_ROW = "bright_black"  # Soft gray for row text
    TABLE_BORDER = "bright_white"  # Softer white borders
    TABLE_HIGHLIGHT = "blue"  # Subtle blue for highlighted rows

    # Interactive elements - Gentle colors for user interaction
    PROMPT = "cyan"  # Cyan for user prompts
    INPUT = "bright_white"  # Softer white for user input
    BUTTON = "blue"  # Blue for interactive buttons
    LINK = "cyan"  # Cyan for clickable links

    # Special purpose colors - Important but not harsh
    SECURITY = "bright_red"  # Softer red for security items
    ENCRYPTION = "bright_green"  # Softer green for encryption status
    MNEMONIC = "yellow"  # Yellow for recovery phrases (important!)
    PASSWORD = "bright_red"  # Softer red for password fields

    # Alternative color schemes for different preferences
    ALTERNATIVE_SUCCESS = "cyan"  # Cyan alternative for success states
    ALTERNATIVE_BALANCE = "blue"  # Blue alternative for balances
    ALTERNATIVE_WALLET = "magenta"  # Magenta alternative for wallet types

    # Soft color scheme - Even more eye-friendly
    SOFT_SUCCESS = "cyan"  # Cyan instead of green for success
    SOFT_BALANCE = "blue"  # Blue instead of green for balances
    SOFT_WALLET = "magenta"  # Magenta for wallet types
    SOFT_TEXT = "bright_black"  # Very soft text color
    SOFT_BORDER = "bright_black"  # Very soft borders

    # Accessibility colors - High contrast option
    ACCESSIBILITY_HIGH_CONTRAST = {
        "text": "bright_white",
        "background": "black",
        "border": "bright_white",
        "error": "bright_red",
        "success": "bright_green",
        "warning": "bright_yellow",
    }


def get_color(color_name: str, scheme: ColorScheme = ColorScheme.DEFAULT) -> str:
    """
    Get a standardized color based on the current color scheme.

    Args:
        color_name: Name of the color to retrieve
        scheme: Color scheme to use

    Returns:
        Rich-compatible color string
    """
    if scheme == ColorScheme.HIGH_CONTRAST:
        return Colors.ACCESSIBILITY_HIGH_CONTRAST.get(color_name, "white")

    # Get the color attribute from Colors class
    color_attr = getattr(Colors, color_name.upper(), None)
    if color_attr:
        return color_attr.value

    # Fallback to safe defaults
    return "bright_white"


def get_current_color_scheme() -> ColorScheme:
    """
    Get the current color scheme from configuration.

    Returns:
        Current ColorScheme enum value
    """
    try:
        from src.htcli.config import load_config

        config = load_config()
        scheme_name = config.output.color_scheme.lower()

        # Map config values to ColorScheme enum
        scheme_mapping = {
            "default": ColorScheme.DEFAULT,
            "dark": ColorScheme.DARK,
            "light": ColorScheme.LIGHT,
            "high_contrast": ColorScheme.HIGH_CONTRAST,
            "high-contrast": ColorScheme.HIGH_CONTRAST,
            "soft": ColorScheme.SOFT,
        }

        return scheme_mapping.get(scheme_name, ColorScheme.DEFAULT)
    except Exception:
        # Fallback to default if config loading fails
        return ColorScheme.DEFAULT


def get_table_style(scheme: ColorScheme = ColorScheme.DEFAULT) -> dict:
    """
    Get standardized table styling.

    Args:
        scheme: Color scheme to use

    Returns:
        Dictionary with table styling parameters
    """
    if scheme == ColorScheme.HIGH_CONTRAST:
        return {
            "header_style": "bold bright_white",
            "border_style": "bright_white",
            "row_styles": ["bright_white", "bright_black"],
        }
    elif scheme == ColorScheme.SOFT:
        return {
            "header_style": f"bold {Colors.SOFT_TEXT}",
            "border_style": Colors.SOFT_BORDER,
            "row_styles": [Colors.SOFT_TEXT, Colors.SOFT_TEXT],
        }

    return {
        "header_style": f"bold {Colors.TABLE_HEADER}",
        "border_style": Colors.TABLE_BORDER,
        "row_styles": [Colors.TABLE_ROW, Colors.TEXT_PRIMARY],
    }


def get_status_color(status: str, scheme: ColorScheme = ColorScheme.DEFAULT) -> str:
    """
    Get appropriate color for status indicators.

    Args:
        status: Status string (online, offline, pending, etc.)
        scheme: Color scheme to use

    Returns:
        Rich-compatible color string
    """
    status_colors = {
        "online": Colors.STATUS_ONLINE,
        "offline": Colors.STATUS_OFFLINE,
        "pending": Colors.STATUS_PENDING,
        "active": Colors.STATUS_ONLINE,
        "inactive": Colors.STATUS_OFFLINE,
        "success": Colors.SUCCESS,
        "error": Colors.ERROR,
        "warning": Colors.WARNING,
        "info": Colors.INFO,
    }

    return status_colors.get(status.lower(), Colors.TEXT_PRIMARY)


def get_balance_color(balance: float, scheme: ColorScheme = ColorScheme.DEFAULT) -> str:
    """
    Get appropriate color for balance display.

    Args:
        balance: Balance amount
        scheme: Color scheme to use

    Returns:
        Rich-compatible color string
    """
    if scheme == ColorScheme.SOFT:
        if balance > 0:
            return Colors.SOFT_BALANCE
        elif balance < 0:
            return Colors.ERROR
        else:
            return Colors.SOFT_TEXT
    else:
        if balance > 0:
            return Colors.BALANCE_POSITIVE
        elif balance < 0:
            return Colors.BALANCE_NEGATIVE
        else:
            return Colors.BALANCE_ZERO


def get_wallet_color(
    wallet_type: str, scheme: ColorScheme = ColorScheme.DEFAULT
) -> str:
    """
    Get appropriate color for wallet type display.

    Args:
        wallet_type: Type of wallet (coldkey, hotkey, etc.)
        scheme: Color scheme to use

    Returns:
        Rich-compatible color string
    """
    if scheme == ColorScheme.SOFT:
        wallet_colors = {
            "coldkey": Colors.SOFT_WALLET,
            "hotkey": Colors.SOFT_WALLET,
            "address": Colors.SOFT_BALANCE,
            "external": Colors.SOFT_TEXT,
        }
    else:
        wallet_colors = {
            "coldkey": Colors.WALLET_COLDKEY,
            "hotkey": Colors.WALLET_HOTKEY,
            "address": Colors.WALLET_ADDRESS,
            "external": Colors.TEXT_SECONDARY,
        }

    return wallet_colors.get(wallet_type.lower(), Colors.TEXT_PRIMARY)


# Convenience functions for common use cases
def success_color() -> str:
    """Get success color."""
    return Colors.SUCCESS


def error_color() -> str:
    """Get error color."""
    return Colors.ERROR


def warning_color() -> str:
    """Get warning color."""
    return Colors.WARNING


def info_color() -> str:
    """Get info color."""
    return Colors.INFO


def primary_color() -> str:
    """Get primary color."""
    return Colors.PRIMARY


def text_color() -> str:
    """Get primary text color."""
    return Colors.TEXT_PRIMARY


def muted_color() -> str:
    """Get muted text color."""
    return Colors.TEXT_MUTED
