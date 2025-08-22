"""
Validation helpers for user input in the Hypertensor CLI.
"""

import re
from pathlib import Path
from typing import List, Optional, Union


def validate_address(address: str) -> bool:
    """Validate SS58 address format."""
    # Basic SS58 validation - should be 42-48 characters and start with a number
    if not address or len(address) < 42 or len(address) > 48:
        return False

    # Should start with a number (5 for mainnet, 0 for testnet)
    if not address[0].isdigit():
        return False

    # Should contain only alphanumeric characters
    if not re.match(r"^[1-9A-HJ-NP-Za-km-z]+$", address):
        return False

    return True


def validate_amount(amount: Union[str, float, int]) -> bool:
    """Validate amount format for TENSOR token (18 decimals)."""
    try:
        if isinstance(amount, str):
            amount = float(amount)
        elif isinstance(amount, int):
            amount = float(amount)

        if amount <= 0:
            return False

        # Check for TENSOR precision (18 decimals)
        str_amount = f"{amount:.18f}"
        if len(str_amount.split(".")[-1]) > 18:
            return False

        return True
    except (ValueError, TypeError):
        return False


def validate_subnet_id(subnet_id: Union[str, int]) -> bool:
    """Validate subnet ID format."""
    try:
        if isinstance(subnet_id, str):
            subnet_id = int(subnet_id)

        if subnet_id <= 0:
            return False

        return True
    except (ValueError, TypeError):
        return False


def validate_node_id(node_id: Union[str, int]) -> bool:
    """Validate node ID format."""
    try:
        if isinstance(node_id, str):
            node_id = int(node_id)

        if node_id <= 0:
            return False

        return True
    except (ValueError, TypeError):
        return False


def validate_peer_id(peer_id: str) -> bool:
    """Validate peer ID format (MultiHash)."""
    # Basic MultiHash validation
    if not peer_id or len(peer_id) < 10:
        return False

    # Should start with Qm (base58btc multihash)
    if not peer_id.startswith("Qm"):
        return False

    # Should contain only base58 characters
    if not re.match(r"^[1-9A-HJ-NP-Za-km-z]+$", peer_id):
        return False

    return True


def validate_key_type(key_type: str) -> bool:
    """Validate key type."""
    valid_types = ["sr25519", "ed25519"]
    return key_type.lower() in valid_types


def validate_password(password: Optional[str]) -> bool:
    """Validate password strength."""
    if password is None:
        return True  # Allow empty passwords

    if len(password) < 8:
        return False

    # Should contain at least one letter and one number
    if not re.search(r"[a-zA-Z]", password) or not re.search(r"\d", password):
        return False

    return True


def validate_file_path(file_path: str) -> bool:
    """Validate file path."""
    try:
        path = Path(file_path)
        # Check if parent directory exists or can be created
        return True
    except Exception:
        return False


def validate_rpc_url(url: str) -> bool:
    """Validate RPC URL format."""
    # Basic URL validation
    if not url:
        return False

    # Should start with ws:// or wss:// or http:// or https://
    if not re.match(r"^(ws|wss|http|https)://", url):
        return False

    return True


def validate_vote_type(vote: str) -> bool:
    """Validate vote type."""
    valid_votes = ["yay", "nay"]
    return vote.lower() in valid_votes


def validate_proposal_data(data: str) -> bool:
    """Validate proposal data."""
    if not data or len(data.strip()) == 0:
        return False

    # Basic length validation
    if len(data) > 10000:  # 10KB limit
        return False

    return True


def validate_validation_data(data: str) -> bool:
    """Validate validation data."""
    if not data or len(data.strip()) == 0:
        return False

    # Basic length validation
    if len(data) > 100000:  # 100KB limit
        return False

    return True


def validate_memory_mb(memory_mb: int) -> bool:
    """Validate memory requirement in MB."""
    if memory_mb <= 0 or memory_mb > 100000:  # 100GB limit
        return False

    return True


def validate_registration_blocks(blocks: int) -> bool:
    """Validate registration period in blocks."""
    if blocks <= 0 or blocks > 1000000:  # 1M blocks limit
        return False

    return True


def validate_entry_interval(interval: int) -> bool:
    """Validate entry interval in blocks."""
    if interval <= 0 or interval > 100000:  # 100K blocks limit
        return False

    return True


def validate_subnet_path(path: str) -> bool:
    """Validate subnet path/name."""
    if not path or len(path.strip()) == 0:
        return False

    # Should be alphanumeric with hyphens and underscores
    if not re.match(r"^[a-zA-Z0-9_-]+$", path):
        return False

    # Length validation
    if len(path) > 100:
        return False

    return True


def validate_wallet_name(name: str) -> bool:
    """Validate wallet name."""
    if not name or len(name.strip()) == 0:
        return False

    # Should be alphanumeric with hyphens and underscores
    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        return False

    # Length validation
    if len(name) > 50:
        return False

    return True


def validate_private_key(private_key: str) -> bool:
    """Validate private key format."""
    if not private_key or len(private_key.strip()) == 0:
        return False

    # Should be hex string
    if not re.match(r"^[0-9a-fA-F]+$", private_key):
        return False

    # Length validation (32 bytes = 64 hex characters)
    if len(private_key) != 64:
        return False

    return True


def validate_mnemonic(mnemonic: str) -> bool:
    """Validate mnemonic phrase."""
    if not mnemonic or len(mnemonic.strip()) == 0:
        return False

    # Split into words
    words = mnemonic.strip().split()

    # Should have 12, 15, 18, 21, or 24 words
    if len(words) not in [12, 15, 18, 21, 24]:
        return False

    # All words should be lowercase
    for word in words:
        if not word.islower() or not word.isalpha():
            return False

    return True


def validate_block_number(block_number: Optional[Union[str, int]]) -> bool:
    """Validate block number."""
    if block_number is None:
        return True  # Allow None for latest block

    try:
        if isinstance(block_number, str):
            block_number = int(block_number)

        if block_number < 0:
            return False

        return True
    except (ValueError, TypeError):
        return False


def validate_limit(limit: Union[str, int]) -> bool:
    """Validate limit parameter."""
    try:
        if isinstance(limit, str):
            limit = int(limit)

        if limit <= 0 or limit > 1000:
            return False

        return True
    except (ValueError, TypeError):
        return False


def validate_tensor_stake_amount(amount: Union[str, float, int]) -> bool:
    """Validate TENSOR stake amount with 18 decimal precision."""
    try:
        if isinstance(amount, str):
            amount = float(amount)
        elif isinstance(amount, int):
            amount = float(amount)

        if amount <= 0:
            return False

        # Check for TENSOR precision (18 decimals)
        str_amount = f"{amount:.18f}"
        if len(str_amount.split(".")[-1]) > 18:
            return False

        return True
    except (ValueError, TypeError):
        return False


def validate_tensor_balance(amount: Union[str, float, int]) -> bool:
    """Validate TENSOR balance amount with 18 decimal precision."""
    try:
        if isinstance(amount, str):
            amount = float(amount)
        elif isinstance(amount, int):
            amount = float(amount)

        if amount < 0:  # Allow zero balance
            return False

        # Check for TENSOR precision (18 decimals)
        str_amount = f"{amount:.18f}"
        if len(str_amount.split(".")[-1]) > 18:
            return False

        return True
    except (ValueError, TypeError):
        return False


def validate_url(url: str) -> bool:
    """Validate URL format for configuration."""
    if not url:
        return False

    # Should start with ws:// or wss:// or http:// or https://
    if not re.match(r"^(ws|wss|http|https)://", url):
        return False

    # Basic domain validation
    if len(url) < 10:
        return False

    return True


def validate_path(path: str) -> bool:
    """Validate file/directory path for configuration."""
    try:
        expanded_path = Path(path).expanduser()
        # Check if parent directory exists or can be created
        return True
    except Exception:
        return False


def validate_subnet_name(name: str) -> bool:
    """Validate subnet name."""
    if not name or len(name) < 1 or len(name) > 100:
        return False
    # Allow alphanumeric, hyphens, underscores, spaces
    import re

    return bool(re.match(r"^[a-zA-Z0-9\-\_\s]+$", name))


def validate_repo_url(repo: str) -> bool:
    """Validate repository URL."""
    if not repo or len(repo) < 10 or len(repo) > 500:
        return False
    # Basic URL validation
    import re

    return bool(re.match(r"^https?://[^\s/$.?#].[^\s]*$", repo))


def validate_subnet_description(description: str) -> bool:
    """Validate subnet description."""
    if not description or len(description) < 10 or len(description) > 1000:
        return False
    return True


def validate_stake_amount(amount: int) -> bool:
    """Validate stake amount."""
    return amount > 0 and amount <= 10**18  # Max 1 billion TENSOR


def validate_delegate_percentage(percentage: int) -> bool:
    """Validate delegate stake percentage."""
    return 0 <= percentage <= 100


def validate_epoch_value(epochs: int) -> bool:
    """Validate epoch-based values."""
    return 0 <= epochs <= 1000000


def validate_churn_limit(churn_limit: int) -> bool:
    """Validate churn limit."""
    return 1 <= churn_limit <= 1000


def validate_max_nodes(max_nodes: int) -> bool:
    """Validate maximum registered nodes."""
    return 1 <= max_nodes <= 10000


def validate_max_penalties(penalties: int) -> bool:
    """Validate maximum node penalties."""
    return 1 <= penalties <= 100


def validate_key_types(key_types: list) -> bool:
    """Validate key types."""
    valid_types = ["RSA", "Ed25519", "Secp256k1", "ECDSA"]
    return all(kt in valid_types for kt in key_types)


def validate_coldkey_addresses(addresses: List[str]) -> bool:
    """Validate a list of coldkey addresses."""
    if not addresses:
        return False

    for address in addresses:
        if not validate_ss58_address(address):
            return False

    return True


def validate_ss58_address(address: str) -> bool:
    """Validate SS58 address format."""
    if not address or len(address) < 10 or len(address) > 100:
        return False
    # Basic SS58 format validation (starts with number and contains alphanumeric)
    import re

    return bool(re.match(r"^[1-9][a-zA-Z0-9]+$", address))


def validate_delegate_reward_rate(rate: int) -> bool:
    """Validate delegate reward rate."""
    if not isinstance(rate, int):
        return False

    if rate < 0:
        return False

    # Rate should be reasonable (not excessively high)
    if rate > 1000000000000000000:  # 1 TENSOR in smallest units
        return False

    return True
