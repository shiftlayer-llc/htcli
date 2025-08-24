"""
Cryptographic utility functions for the Hypertensor CLI.
"""

import base64
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet
from substrateinterface import Keypair

from .password import get_secure_password


@dataclass
class KeypairInfo:
    """Information about a keypair."""

    name: str
    key_type: str
    public_key: str
    ss58_address: str
    mnemonic: Optional[str] = None  # Recovery phrase
    owner_address: Optional[str] = None  # For hotkeys


def generate_coldkey_pair(
    name: str, key_type: str = "sr25519", password: Optional[str] = None
) -> KeypairInfo:
    """Generate a new coldkey pair."""
    try:
        # Generate random keypair
        if key_type == "sr25519":
            mnemonic = Keypair.generate_mnemonic()
            keypair = Keypair.create_from_uri(mnemonic)
        elif key_type == "ed25519":
            mnemonic = Keypair.generate_mnemonic()
            keypair = Keypair.create_from_uri(
                mnemonic, crypto_type=0
            )  # 0 for ed25519, 1 for sr25519
        else:
            raise ValueError(f"Unsupported key type: {key_type}")

        # Create keypair info
        keypair_info = KeypairInfo(
            name=name,
            key_type=key_type,
            public_key=keypair.public_key.hex(),
            ss58_address=keypair.ss58_address,
            mnemonic=mnemonic,  # Include the recovery phrase
            owner_address=None,  # Coldkeys don't have owners
        )

        # Use the password directly from the CLI function
        # The CLI function already handles the password prompting
        save_coldkey(name, keypair, password)

        return keypair_info

    except Exception as e:
        raise Exception(f"Failed to generate coldkey: {str(e)}")


def generate_hotkey_pair(
    name: str,
    owner_address: str,
    key_type: str = "sr25519",
    password: Optional[str] = None,
) -> KeypairInfo:
    """Generate a new hotkey pair owned by a coldkey."""
    try:
        # Generate random keypair
        if key_type == "sr25519":
            mnemonic = Keypair.generate_mnemonic()
            keypair = Keypair.create_from_uri(mnemonic)
        elif key_type == "ed25519":
            mnemonic = Keypair.generate_mnemonic()
            keypair = Keypair.create_from_uri(
                mnemonic, crypto_type=0
            )  # 0 for ed25519, 1 for sr25519
        else:
            raise ValueError(f"Unsupported key type: {key_type}")

        # Create keypair info
        keypair_info = KeypairInfo(
            name=name,
            key_type=key_type,
            public_key=keypair.public_key.hex(),
            ss58_address=keypair.ss58_address,
            mnemonic=mnemonic,  # Include the recovery phrase
            owner_address=owner_address,  # Hotkeys have owners
        )

        # Use the password directly from the CLI function
        # The CLI function already handles the password prompting
        save_hotkey(name, keypair, owner_address, password)

        return keypair_info

    except Exception as e:
        raise Exception(f"Failed to generate hotkey: {str(e)}")


def generate_keypair(
    name: str, key_type: str = "sr25519", password: Optional[str] = None
) -> KeypairInfo:
    """Generate a new keypair (legacy function - now creates coldkey)."""
    return generate_coldkey_pair(name, key_type, password)


def import_keypair(
    name: str,
    private_key: str,
    key_type: str = "sr25519",
    password: Optional[str] = None,
) -> KeypairInfo:
    """Import an existing keypair."""
    try:
        # Import keypair
        if key_type == "sr25519":
            keypair = Keypair.create_from_private_key(private_key)
        elif key_type == "ed25519":
            keypair = Keypair.create_from_private_key(
                private_key, crypto_type=0
            )  # 0 for ed25519, 1 for sr25519
        else:
            raise ValueError(f"Unsupported key type: {key_type}")

        # Create keypair info
        keypair_info = KeypairInfo(
            name=name,
            key_type=key_type,
            public_key=keypair.public_key.hex(),
            ss58_address=keypair.ss58_address,
            owner_address=None,  # Coldkeys don't have owners
        )

        # Use provided password or None (no prompting)
        save_keypair(name, keypair, password)

        return keypair_info

    except Exception as e:
        raise Exception(f"Failed to import keypair: {str(e)}")


def import_keypair_from_mnemonic(
    name: str,
    mnemonic: str,
    key_type: str = "sr25519",
    password: Optional[str] = None,
) -> KeypairInfo:
    """Import an existing keypair from mnemonic phrase."""
    try:
        # Import keypair from mnemonic
        if key_type == "sr25519":
            keypair = Keypair.create_from_mnemonic(
                mnemonic, ss58_format=42, crypto_type=1
            )
        elif key_type == "ed25519":
            keypair = Keypair.create_from_mnemonic(
                mnemonic, ss58_format=42, crypto_type=0
            )
        else:
            raise ValueError(f"Unsupported key type: {key_type}")

        # Create keypair info
        keypair_info = KeypairInfo(
            name=name,
            key_type=key_type,
            public_key=keypair.public_key.hex(),
            ss58_address=keypair.ss58_address,
            owner_address=None,  # Coldkeys don't have owners
        )

        # Use provided password or None (no prompting)
        save_keypair(name, keypair, password)

        return keypair_info

    except Exception as e:
        raise Exception(f"Failed to import keypair from mnemonic: {str(e)}")


def import_hotkey_from_private_key(
    name: str,
    private_key: str,
    owner_address: str,
    key_type: str = "sr25519",
    password: Optional[str] = None,
) -> KeypairInfo:
    """Import an existing hotkey from private key."""
    try:
        # Import keypair
        if key_type == "sr25519":
            keypair = Keypair.create_from_private_key(private_key)
        elif key_type == "ed25519":
            keypair = Keypair.create_from_private_key(
                private_key, crypto_type=0
            )  # 0 for ed25519, 1 for sr25519
        else:
            raise ValueError(f"Unsupported key type: {key_type}")

        # Create keypair info
        keypair_info = KeypairInfo(
            name=name,
            key_type=key_type,
            public_key=keypair.public_key.hex(),
            ss58_address=keypair.ss58_address,
            owner_address=owner_address,  # Hotkeys have owners
        )

        # Use provided password or None (no prompting)
        save_hotkey(name, keypair, owner_address, password)

        return keypair_info

    except Exception as e:
        raise Exception(f"Failed to import hotkey from private key: {str(e)}")


def import_hotkey_from_mnemonic(
    name: str,
    mnemonic: str,
    owner_address: str,
    key_type: str = "sr25519",
    password: Optional[str] = None,
) -> KeypairInfo:
    """Import an existing hotkey from mnemonic phrase."""
    try:
        # Import keypair from mnemonic
        if key_type == "sr25519":
            keypair = Keypair.create_from_mnemonic(
                mnemonic, ss58_format=42, crypto_type=1
            )
        elif key_type == "ed25519":
            keypair = Keypair.create_from_mnemonic(
                mnemonic, ss58_format=42, crypto_type=0
            )
        else:
            raise ValueError(f"Unsupported key type: {key_type}")

        # Create keypair info
        keypair_info = KeypairInfo(
            name=name,
            key_type=key_type,
            public_key=keypair.public_key.hex(),
            ss58_address=keypair.ss58_address,
            owner_address=owner_address,  # Hotkeys have owners
        )

        # Use provided password or None (no prompting)
        save_hotkey(name, keypair, owner_address, password)

        return keypair_info

    except Exception as e:
        raise Exception(f"Failed to import hotkey from mnemonic: {str(e)}")


def save_coldkey(name: str, keypair: Keypair, password: Optional[str]):
    """Save a coldkey to disk with encryption."""
    try:
        # Create wallet directory
        wallet_dir = Path.home() / ".htcli" / "wallets"
        wallet_dir.mkdir(parents=True, exist_ok=True)

        if password is not None:
            # Encrypt private key with password
            key = Fernet.generate_key()
            cipher = Fernet(key)
            private_key_bytes = keypair.private_key
            encrypted_private_key = cipher.encrypt(private_key_bytes)

            # Create wallet data with encryption
            wallet_data = {
                "name": name,
                "key_type": "sr25519" if keypair.crypto_type == 1 else "ed25519",
                "public_key": keypair.public_key.hex(),
                "ss58_address": keypair.ss58_address,
                "encrypted_private_key": base64.b64encode(
                    encrypted_private_key
                ).decode(),
                "salt": base64.b64encode(key).decode(),
                "is_hotkey": False,  # This is a coldkey
                "owner_address": None,  # Coldkeys don't have owners
                "is_encrypted": True,
            }
        else:
            # Store private key without encryption (less secure but user's choice)
            private_key_bytes = keypair.private_key

            # Create wallet data without encryption
            wallet_data = {
                "name": name,
                "key_type": "sr25519" if keypair.crypto_type == 1 else "ed25519",
                "public_key": keypair.public_key.hex(),
                "ss58_address": keypair.ss58_address,
                "private_key": private_key_bytes.hex(),  # Store unencrypted
                "is_hotkey": False,  # This is a coldkey
                "owner_address": None,  # Coldkeys don't have owners
                "is_encrypted": False,
            }

        # Save to file
        wallet_file = wallet_dir / f"{name}.json"
        with open(wallet_file, "w") as f:
            json.dump(wallet_data, f, indent=2)

        # Set secure permissions
        wallet_file.chmod(0o600)

    except Exception as e:
        raise Exception(f"Failed to save coldkey: {str(e)}")


def save_hotkey(
    name: str, keypair: Keypair, owner_address: str, password: Optional[str]
):
    """Save a hotkey to disk with encryption."""
    try:
        # Create wallet directory
        wallet_dir = Path.home() / ".htcli" / "wallets"
        wallet_dir.mkdir(parents=True, exist_ok=True)

        if password is not None:
            # Encrypt private key with password
            key = Fernet.generate_key()
            cipher = Fernet(key)
            private_key_bytes = keypair.private_key
            encrypted_private_key = cipher.encrypt(private_key_bytes)

            # Create wallet data with encryption
            wallet_data = {
                "name": name,
                "key_type": "sr25519" if keypair.crypto_type == 1 else "ed25519",
                "public_key": keypair.public_key.hex(),
                "ss58_address": keypair.ss58_address,
                "encrypted_private_key": base64.b64encode(
                    encrypted_private_key
                ).decode(),
                "salt": base64.b64encode(key).decode(),
                "is_hotkey": True,  # This is a hotkey
                "owner_address": owner_address,  # Hotkeys have owners
                "is_encrypted": True,
            }
        else:
            # Store private key without encryption (less secure but user's choice)
            private_key_bytes = keypair.private_key

            # Create wallet data without encryption
            wallet_data = {
                "name": name,
                "key_type": "sr25519" if keypair.crypto_type == 1 else "ed25519",
                "public_key": keypair.public_key.hex(),
                "ss58_address": keypair.ss58_address,
                "private_key": private_key_bytes.hex(),  # Store unencrypted
                "is_hotkey": True,  # This is a hotkey
                "owner_address": owner_address,  # Hotkeys have owners
                "is_encrypted": False,
            }

        # Save to file
        wallet_file = wallet_dir / f"{name}.json"
        with open(wallet_file, "w") as f:
            json.dump(wallet_data, f, indent=2)

        # Set secure permissions
        wallet_file.chmod(0o600)

    except Exception as e:
        raise Exception(f"Failed to save hotkey: {str(e)}")


def save_keypair(name: str, keypair: Keypair, password: str):
    """Save a keypair to disk with encryption (legacy function)."""
    save_coldkey(name, keypair, password)


def load_keypair(name: str, password: Optional[str] = None) -> Keypair:
    """Load a keypair from disk."""
    try:
        wallet_dir = Path.home() / ".htcli" / "wallets"
        keypair_file = wallet_dir / f"{name}.json"

        if not keypair_file.exists():
            raise FileNotFoundError(f"Keypair '{name}' not found")

        with open(keypair_file, "r") as f:
            keypair_data = json.load(f)

        # Check if the key is encrypted
        is_encrypted = keypair_data.get(
            "is_encrypted", True
        )  # Default to True for backward compatibility

        if is_encrypted:
            # Get secure password for decryption
            decrypt_password = password or get_secure_password(
                name,
                prompt_message="Enter password to unlock this keypair",
                allow_default=True,
            )

            # Decrypt private key
            salt = base64.b64decode(keypair_data["salt"])
            encrypted_private_key = base64.b64decode(
                keypair_data["encrypted_private_key"]
            )

            cipher = Fernet(salt)
            private_key_bytes = cipher.decrypt(encrypted_private_key)
        else:
            # Key is not encrypted, load directly
            if "private_key" in keypair_data:
                private_key_bytes = bytes.fromhex(keypair_data["private_key"])
            else:
                raise ValueError("Key file is corrupted: missing private key")

        # Create keypair
        if keypair_data["key_type"] == "sr25519":
            keypair = Keypair.create_from_private_key(
                private_key_bytes.hex(), ss58_format=42
            )
        else:
            keypair = Keypair.create_from_private_key(
                private_key_bytes.hex(), crypto_type=0, ss58_format=42
            )  # 0 for ed25519

        return keypair

    except Exception as e:
        raise Exception(f"Failed to load keypair: {str(e)}")


def list_keys() -> list[dict]:
    """List all available keys."""
    try:
        wallet_dir = Path.home() / ".htcli" / "wallets"
        if not wallet_dir.exists():
            return []

        keys = []
        for keypair_file in wallet_dir.glob("*.json"):
            try:
                with open(keypair_file, "r") as f:
                    keypair_data = json.load(f)

                # Return as dictionary for compatibility with wallet commands
                key_info = {
                    "name": keypair_data["name"],
                    "key_type": keypair_data["key_type"],
                    "public_key": keypair_data["public_key"],
                    "ss58_address": keypair_data["ss58_address"],
                    "address": keypair_data[
                        "ss58_address"
                    ],  # Alias for ownership utils
                    # Add hotkey/coldkey information
                    "is_hotkey": keypair_data.get("is_hotkey", False),
                    "owner_address": keypair_data.get("owner_address", None),
                    # Add encryption status
                    "is_encrypted": keypair_data.get("is_encrypted", True),
                }
                keys.append(key_info)
            except Exception:
                # Skip corrupted files
                continue

        return keys

    except Exception as e:
        raise Exception(f"Failed to list keys: {str(e)}")


def get_wallet_info_by_name(name: str) -> dict:
    """Get wallet information by name without loading the private key."""
    try:
        wallet_dir = Path.home() / ".htcli" / "wallets"
        keypair_file = wallet_dir / f"{name}.json"

        if not keypair_file.exists():
            raise FileNotFoundError(f"Wallet '{name}' not found")

        with open(keypair_file, "r") as f:
            keypair_data = json.load(f)

        # Return wallet info without private key
        wallet_info = {
            "name": keypair_data["name"],
            "key_type": keypair_data["key_type"],
            "public_key": keypair_data["public_key"],
            "ss58_address": keypair_data["ss58_address"],
            "address": keypair_data["ss58_address"],  # Alias for compatibility
            "is_hotkey": keypair_data.get("is_hotkey", False),
            "owner_address": keypair_data.get("owner_address", None),
            "is_encrypted": keypair_data.get("is_encrypted", True),
        }

        return wallet_info

    except Exception as e:
        raise Exception(f"Failed to get wallet info: {str(e)}")


def wallet_name_exists(name: str) -> bool:
    """Check if a wallet name already exists."""
    try:
        wallet_dir = Path.home() / ".htcli" / "wallets"
        keypair_file = wallet_dir / f"{name}.json"
        return keypair_file.exists()
    except Exception:
        return False


def delete_keypair(name: str) -> bool:
    """Delete a keypair from disk."""
    try:
        wallet_dir = Path.home() / ".htcli" / "wallets"
        keypair_file = wallet_dir / f"{name}.json"

        if keypair_file.exists():
            keypair_file.unlink()
            return True
        else:
            return False

    except Exception as e:
        raise Exception(f"Failed to delete keypair: {str(e)}")


def delete_coldkey_and_hotkeys(coldkey_name: str) -> dict:
    """Delete a coldkey and all its associated hotkeys."""
    try:
        # First, get the coldkey info to get its address
        coldkey_info = get_wallet_info_by_name(coldkey_name)
        coldkey_address = coldkey_info["ss58_address"]

        # Check if it's actually a coldkey
        if coldkey_info.get("is_hotkey", False):
            raise Exception(f"'{coldkey_name}' is a hotkey, not a coldkey")

        # Find all hotkeys owned by this coldkey
        all_keys = list_keys()
        associated_hotkeys = []

        for key_info in all_keys:
            if (
                key_info.get("is_hotkey", False)
                and key_info.get("owner_address") == coldkey_address
            ):
                associated_hotkeys.append(key_info["name"])

        # Delete the coldkey first
        coldkey_deleted = delete_keypair(coldkey_name)
        if not coldkey_deleted:
            raise Exception(f"Failed to delete coldkey '{coldkey_name}'")

        # Delete all associated hotkeys
        hotkeys_deleted = []
        for hotkey_name in associated_hotkeys:
            try:
                if delete_keypair(hotkey_name):
                    hotkeys_deleted.append(hotkey_name)
                else:
                    print(f"Warning: Failed to delete hotkey '{hotkey_name}'")
            except Exception as e:
                print(f"Warning: Error deleting hotkey '{hotkey_name}': {str(e)}")

        return {
            "coldkey_deleted": coldkey_name,
            "coldkey_address": coldkey_address,
            "hotkeys_deleted": hotkeys_deleted,
            "total_hotkeys_deleted": len(hotkeys_deleted),
        }

    except Exception as e:
        raise Exception(f"Failed to delete coldkey and hotkeys: {str(e)}")


def update_coldkey(
    current_name: str,
    new_name: Optional[str] = None,
    new_password: Optional[str] = None,
    remove_password: bool = False,
) -> dict:
    """Update a coldkey's properties."""
    try:
        # Load the current keypair
        keypair = load_keypair(current_name)

        # Get current wallet info
        wallet_info = get_wallet_info_by_name(current_name)

        # Verify it's a coldkey
        if wallet_info.get("is_hotkey", False):
            raise Exception(f"'{current_name}' is a hotkey, not a coldkey")

        # Determine new name
        final_name = new_name if new_name else current_name

        # Check if new name already exists (if changing name)
        if new_name and new_name != current_name:
            if wallet_name_exists(new_name):
                raise Exception(f"Wallet name '{new_name}' already exists")

        # Determine password
        if remove_password:
            final_password = None
        elif new_password:
            final_password = new_password
        else:
            # Keep current password (will be handled by save function)
            final_password = None

        # Save with new properties
        save_coldkey(final_name, keypair, final_password)

        # Delete old file if name changed
        if new_name and new_name != current_name:
            delete_keypair(current_name)

        return {
            "old_name": current_name,
            "new_name": final_name,
            "key_type": wallet_info["key_type"],
            "ss58_address": wallet_info["ss58_address"],
            "password_updated": new_password is not None or remove_password,
            "name_updated": new_name is not None and new_name != current_name,
        }

    except Exception as e:
        raise Exception(f"Failed to update coldkey: {str(e)}")


def update_hotkey(
    current_name: str,
    new_name: Optional[str] = None,
    new_password: Optional[str] = None,
    remove_password: bool = False,
    new_owner_name: Optional[str] = None,
) -> dict:
    """Update a hotkey's properties."""
    try:
        # Load the current keypair
        keypair = load_keypair(current_name)

        # Get current wallet info
        wallet_info = get_wallet_info_by_name(current_name)

        # Verify it's a hotkey
        if not wallet_info.get("is_hotkey", False):
            raise Exception(f"'{current_name}' is a coldkey, not a hotkey")

        # Determine new name
        final_name = new_name if new_name else current_name

        # Check if new name already exists (if changing name)
        if new_name and new_name != current_name:
            if wallet_name_exists(new_name):
                raise Exception(f"Wallet name '{new_name}' already exists")

        # Determine owner address
        owner_address = wallet_info["owner_address"]
        if new_owner_name:
            # Validate new owner exists and is a coldkey
            try:
                new_owner_info = get_wallet_info_by_name(new_owner_name)
                if new_owner_info.get("is_hotkey", False):
                    raise Exception(
                        f"'{new_owner_name}' is a hotkey. Please provide a coldkey wallet name as the owner."
                    )
                owner_address = new_owner_info["ss58_address"]
            except FileNotFoundError:
                raise Exception(
                    f"Owner wallet '{new_owner_name}' not found. Please provide an existing coldkey wallet name."
                )

        # Determine password
        if remove_password:
            final_password = None
        elif new_password:
            final_password = new_password
        else:
            # Keep current password (will be handled by save function)
            final_password = None

        # Save with new properties
        save_hotkey(final_name, keypair, owner_address, final_password)

        # Delete old file if name changed
        if new_name and new_name != current_name:
            delete_keypair(current_name)

        return {
            "old_name": current_name,
            "new_name": final_name,
            "key_type": wallet_info["key_type"],
            "ss58_address": wallet_info["ss58_address"],
            "old_owner_address": wallet_info["owner_address"],
            "new_owner_address": owner_address,
            "password_updated": new_password is not None or remove_password,
            "name_updated": new_name is not None and new_name != current_name,
            "owner_updated": new_owner_name is not None,
        }

    except Exception as e:
        raise Exception(f"Failed to update hotkey: {str(e)}")
