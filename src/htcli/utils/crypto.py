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
            owner_address=None,  # Coldkeys don't have owners
        )

        # Get secure password for saving
        save_password = password or get_secure_password(
            name,
            prompt_message="Enter password to secure this coldkey",
            allow_default=True,
        )
        save_coldkey(name, keypair, save_password)

        return keypair_info

    except Exception as e:
        raise Exception(f"Failed to generate coldkey: {str(e)}")


def generate_hotkey_pair(
    name: str, owner_address: str, key_type: str = "sr25519", password: Optional[str] = None
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
            owner_address=owner_address,  # Hotkeys have owners
        )

        # Get secure password for saving
        save_password = password or get_secure_password(
            name,
            prompt_message="Enter password to secure this hotkey",
            allow_default=True,
        )
        save_hotkey(name, keypair, owner_address, save_password)

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

        # Get secure password for saving
        save_password = password or get_secure_password(
            name,
            prompt_message="Enter password to secure this imported keypair",
            allow_default=True,
        )
        save_keypair(name, keypair, save_password)

        return keypair_info

    except Exception as e:
        raise Exception(f"Failed to import keypair: {str(e)}")


def save_coldkey(name: str, keypair: Keypair, password: str):
    """Save a coldkey to disk with encryption."""
    try:
        # Create wallet directory
        wallet_dir = Path.home() / ".htcli" / "wallets"
        wallet_dir.mkdir(parents=True, exist_ok=True)

        # Generate encryption key from password
        key = Fernet.generate_key()
        cipher = Fernet(key)

        # Encrypt private key
        private_key_bytes = keypair.private_key
        encrypted_private_key = cipher.encrypt(private_key_bytes)

        # Create wallet data
        wallet_data = {
            "name": name,
            "key_type": "sr25519" if keypair.crypto_type == 1 else "ed25519",
            "public_key": keypair.public_key.hex(),
            "ss58_address": keypair.ss58_address,
            "encrypted_private_key": base64.b64encode(encrypted_private_key).decode(),
            "salt": base64.b64encode(key).decode(),
            "is_hotkey": False,  # This is a coldkey
            "owner_address": None,  # Coldkeys don't have owners
        }

        # Save to file
        wallet_file = wallet_dir / f"{name}.json"
        with open(wallet_file, "w") as f:
            json.dump(wallet_data, f, indent=2)

        # Set secure permissions
        wallet_file.chmod(0o600)

    except Exception as e:
        raise Exception(f"Failed to save coldkey: {str(e)}")


def save_hotkey(name: str, keypair: Keypair, owner_address: str, password: str):
    """Save a hotkey to disk with encryption."""
    try:
        # Create wallet directory
        wallet_dir = Path.home() / ".htcli" / "wallets"
        wallet_dir.mkdir(parents=True, exist_ok=True)

        # Generate encryption key from password
        key = Fernet.generate_key()
        cipher = Fernet(key)

        # Encrypt private key
        private_key_bytes = keypair.private_key
        encrypted_private_key = cipher.encrypt(private_key_bytes)

        # Create wallet data
        wallet_data = {
            "name": name,
            "key_type": "sr25519" if keypair.crypto_type == 1 else "ed25519",
            "public_key": keypair.public_key.hex(),
            "ss58_address": keypair.ss58_address,
            "encrypted_private_key": base64.b64encode(encrypted_private_key).decode(),
            "salt": base64.b64encode(key).decode(),
            "is_hotkey": True,  # This is a hotkey
            "owner_address": owner_address,  # Hotkeys have owners
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

        # Get secure password for decryption
        decrypt_password = password or get_secure_password(
            name,
            prompt_message="Enter password to unlock this keypair",
            allow_default=True,
        )

        # Decrypt private key
        salt = base64.b64decode(keypair_data["salt"])
        encrypted_private_key = base64.b64decode(keypair_data["encrypted_private_key"])

        cipher = Fernet(salt)
        private_key_bytes = cipher.decrypt(encrypted_private_key)

        # Create keypair
        if keypair_data["key_type"] == "sr25519":
            keypair = Keypair.create_from_private_key(private_key_bytes.hex())
        else:
            keypair = Keypair.create_from_private_key(
                private_key_bytes.hex(), crypto_type=0
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
                }
                keys.append(key_info)
            except Exception:
                # Skip corrupted files
                continue

        return keys

    except Exception as e:
        raise Exception(f"Failed to list keys: {str(e)}")


def delete_keypair(name: str):
    """Delete a keypair from disk."""
    try:
        wallet_dir = Path.home() / ".htcli" / "wallets"
        keypair_file = wallet_dir / f"{name}.json"

        if keypair_file.exists():
            keypair_file.unlink()
        else:
            raise FileNotFoundError(f"Keypair '{name}' not found")

    except Exception as e:
        raise Exception(f"Failed to delete keypair: {str(e)}")
