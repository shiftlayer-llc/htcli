"""
Utility functions for ownership filtering and user asset detection.
"""

from typing import List, Tuple, Any, Dict
from ..utils.crypto import list_keys
from ..utils.formatting import print_error, print_info


def get_user_addresses() -> List[Tuple[str, str]]:
    """
    Get all wallet addresses for the current user.

    Returns:
        List of (key_name, address) tuples
    """
    try:
        keys = list_keys()
        if not keys:
            return []
        return [
            (key.get("name", "Unknown"), key.get("address", ""))
            for key in keys
            if key.get("address")
        ]
    except Exception as e:
        print_error(f"Failed to get wallet addresses: {e}")
        return []


def user_owns_subnet(
    subnet_data: Dict[str, Any], user_addresses: List[Tuple[str, str]]
) -> bool:
    """
    Check if the user owns a specific subnet.

    Args:
        subnet_data: Subnet information dictionary
        user_addresses: List of (key_name, address) tuples

    Returns:
        True if user owns the subnet, False otherwise
    """
    if not subnet_data or not user_addresses:
        return False

    owner = subnet_data.get("owner", "")
    if not owner:
        return False

    return any(owner == addr for _, addr in user_addresses)


def user_owns_address(address: str, user_addresses: List[Tuple[str, str]]) -> bool:
    """
    Check if an address belongs to the user.

    Args:
        address: Address to check
        user_addresses: List of (key_name, address) tuples

    Returns:
        True if user owns the address, False otherwise
    """
    if not address or not user_addresses:
        return False

    return any(address == addr for _, addr in user_addresses)


def filter_user_assets(
    items: List[Dict[str, Any]],
    filter_field: str,
    user_addresses: List[Tuple[str, str]],
) -> List[Dict[str, Any]]:
    """
    Filter a list of items to only include those owned by the user.

    Args:
        items: List of items to filter
        filter_field: Field name to check for ownership (e.g., 'owner', 'address')
        user_addresses: List of (key_name, address) tuples

    Returns:
        Filtered list containing only user-owned items
    """
    if not items or not user_addresses:
        return []

    filtered = []
    for item in items:
        owner_address = item.get(filter_field, "")
        if owner_address and user_owns_address(owner_address, user_addresses):
            filtered.append(item)

    return filtered


def get_ownership_summary(user_addresses: List[Tuple[str, str]]) -> Dict[str, Any]:
    """
    Get a summary of user ownership capabilities.

    Args:
        user_addresses: List of (key_name, address) tuples

    Returns:
        Dictionary with ownership summary information
    """
    return {
        "has_keys": len(user_addresses) > 0,
        "key_count": len(user_addresses),
        "addresses": [addr for _, addr in user_addresses],
        "key_names": [name for name, _ in user_addresses],
    }


def require_user_keys() -> List[Tuple[str, str]]:
    """
    Get user addresses and provide helpful guidance if none exist.

    Returns:
        List of (key_name, address) tuples

    Raises:
        SystemExit if no keys are found (after showing guidance)
    """
    user_addresses = get_user_addresses()

    if not user_addresses:
        print_error(
            "❌ No wallet keys found. The --mine filter requires stored wallet keys."
        )
        print_info("💡 Generate a key first:")
        print_info("   htcli wallet generate-key --name my-key")
        print_info("")
        print_info("💡 Or import an existing key:")
        print_info(
            "   htcli wallet import-key --name my-key --mnemonic 'your seed phrase'"
        )
        raise SystemExit(1)

    return user_addresses


def show_mine_filter_info(
    user_addresses: List[Tuple[str, str]], found_items: int, total_items: int = None
):
    """
    Show information about mine filtering results.

    Args:
        user_addresses: List of (key_name, address) tuples
        found_items: Number of items found for the user
        total_items: Total items in network (optional)
    """
    if found_items == 0:
        print_info(
            f"🔍 Filtered for your {len(user_addresses)} wallet address(es) - no matching assets found."
        )
        if total_items and total_items > 0:
            print_info(
                f"💡 Network has {total_items} total items, but none are owned by you."
            )
    else:
        print_info(
            f"🎯 Showing {found_items} asset(s) owned by your {len(user_addresses)} wallet address(es)."
        )
        if total_items and total_items > found_items:
            print_info(
                f"💡 Network has {total_items} total items ({total_items - found_items} owned by others)."
            )
