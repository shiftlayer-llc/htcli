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


class Colors:
    """
    Standardized color palette for htcli.
    
    Based on medical research for eye-friendly colors:
    - Avoid pure white (#FFFFFF) - too bright
    - Avoid pure black (#000000) - too harsh
    - Use softer, muted colors
    - Ensure good contrast ratios
    - Work well in both light and dark terminals
    """
    
    # Primary colors - Soft, eye-friendly
    PRIMARY = "bright_blue"      # Soft blue - good for primary elements
    SECONDARY = "cyan"           # Gentle cyan - good for secondary info
    SUCCESS = "green"            # Soft green - success states
    WARNING = "yellow"           # Gentle yellow - warnings
    ERROR = "red"                # Muted red - errors
    INFO = "blue"                # Soft blue - informational
    
    # Text colors - Easy on the eyes
    TEXT_PRIMARY = "white"       # Soft white for primary text
    TEXT_SECONDARY = "bright_black"  # Soft gray for secondary text
    TEXT_MUTED = "dim"           # Very soft gray for muted text
    
    # Background colors - Subtle
    BG_PRIMARY = "black"         # Standard terminal background
    BG_SECONDARY = "bright_black"  # Slightly lighter background
    BG_HIGHLIGHT = "blue"        # Subtle highlight background
    
    # Border colors - Clean and professional
    BORDER_PRIMARY = "white"     # Clean white borders
    BORDER_SECONDARY = "bright_black"  # Subtle borders
    
    # Status colors - Clear but not harsh
    STATUS_ONLINE = "green"      # Online/active status
    STATUS_OFFLINE = "red"       # Offline/inactive status
    STATUS_PENDING = "yellow"    # Pending/waiting status
    
    # Balance colors - Financial clarity
    BALANCE_POSITIVE = "green"   # Positive balances
    BALANCE_NEGATIVE = "red"     # Negative balances
    BALANCE_ZERO = "bright_black"  # Zero balances
    
    # Wallet colors - Clear identification
    WALLET_COLDKEY = "cyan"      # Coldkey identification
    WALLET_HOTKEY = "blue"       # Hotkey identification
    WALLET_ADDRESS = "green"     # Address display
    
    # Table colors - Professional appearance
    TABLE_HEADER = "white"       # Table headers
    TABLE_ROW = "bright_black"   # Table row text
    TABLE_BORDER = "white"       # Table borders
    TABLE_HIGHLIGHT = "blue"     # Highlighted rows
    
    # Interactive elements
    PROMPT = "cyan"              # User prompts
    INPUT = "white"              # User input
    BUTTON = "blue"              # Interactive buttons
    LINK = "cyan"                # Clickable links
    
    # Special purpose colors
    SECURITY = "red"             # Security-related items
    ENCRYPTION = "green"         # Encryption status
    MNEMONIC = "yellow"          # Recovery phrases (important!)
    PASSWORD = "red"             # Password fields
    
    # Accessibility colors - High contrast option
    ACCESSIBILITY_HIGH_CONTRAST = {
        "text": "bright_white",
        "background": "black",
        "border": "bright_white",
        "error": "bright_red",
        "success": "bright_green",
        "warning": "bright_yellow"
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
    return "white"


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
            "row_styles": ["bright_white", "bright_black"]
        }
    
    return {
        "header_style": f"bold {Colors.TABLE_HEADER}",
        "border_style": Colors.TABLE_BORDER,
        "row_styles": [Colors.TABLE_ROW, Colors.TEXT_PRIMARY]
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
        "info": Colors.INFO
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
    if balance > 0:
        return Colors.BALANCE_POSITIVE
    elif balance < 0:
        return Colors.BALANCE_NEGATIVE
    else:
        return Colors.BALANCE_ZERO


def get_wallet_color(wallet_type: str, scheme: ColorScheme = ColorScheme.DEFAULT) -> str:
    """
    Get appropriate color for wallet type display.
    
    Args:
        wallet_type: Type of wallet (coldkey, hotkey, etc.)
        scheme: Color scheme to use
        
    Returns:
        Rich-compatible color string
    """
    wallet_colors = {
        "coldkey": Colors.WALLET_COLDKEY,
        "hotkey": Colors.WALLET_HOTKEY,
        "address": Colors.WALLET_ADDRESS,
        "external": Colors.TEXT_SECONDARY
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
