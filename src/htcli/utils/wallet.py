import json
import os
from pathlib import Path
from enum import Enum
import hashlib
import logging
from substrateinterface import Keypair

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="htcli.log",
    filemode="a",
)
logger = logging.getLogger(__name__)


class WalletType(Enum):
    COLDKEY = 0
    INDEPENDENT_HOTKEY = 1
    OWNED_HOTKEY = 2


def generate_mnemonic() -> str:
    """
    Generate a new mnemonic phrase.

    Returns:
        str: A new mnemonic phrase
    """
    return Keypair.generate_mnemonic()


def create_keypair_from_mnemonic(mnemonic: str) -> Keypair:
    """
    Create a keypair from a mnemonic phrase.

    Args:
        mnemonic: The mnemonic phrase to create the keypair from

    Returns:
        Keypair: The generated keypair

    Raises:
        RuntimeError: If the mnemonic is invalid
    """
    try:
        keypair = Keypair.create_from_mnemonic(mnemonic, ss58_format=42)
        logger.info("Created keypair from mnemonic:")
        logger.info(f"  Address: {keypair.ss58_address}")
        logger.info(f"  Public Key: 0x{keypair.public_key.hex()}")
        logger.info(f"  Private Key: 0x{keypair.private_key.hex()}")
        return keypair
    except Exception as e:
        raise RuntimeError(f"Failed to create keypair from mnemonic: {e}")


def get_account_id(public_key: bytes) -> str:
    """
    Generate the account ID from a public key.
    This is a 32-byte blake2b hash of the public key.

    Args:
        public_key: The public key bytes

    Returns:
        str: The account ID in hex format with 0x prefix
    """
    # Use blake2b hash function with 32-byte output
    blake2b = hashlib.blake2b(digest_size=32)
    blake2b.update(public_key)
    return "0x" + blake2b.hexdigest()


def encrypt_data(data: bytes, password: str) -> bytes:
    """
    Encrypt data using XOR with the password and add a password hash for validation.

    Args:
        data: The data to encrypt
        password: The password to use for encryption

    Returns:
        bytes: The encrypted data with password hash
    """
    # For empty password, return data as is (unencrypted)
    if not password:
        return data

    # Generate password hash for validation
    password_hash = hashlib.sha256(password.encode()).digest()

    # Encrypt the data
    key_bytes = password.encode("utf-8")
    encrypted = bytes(data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data)))

    # Combine password hash and encrypted data
    return password_hash + encrypted


def decrypt_data(encrypted_data: bytes, password: str) -> bytes:
    """
    Decrypt data that was encrypted with XOR using the password.
    Also validates the password using the stored hash.

    Args:
        encrypted_data: The encrypted data with password hash
        password: The password used for encryption

    Returns:
        bytes: The decrypted data

    Raises:
        RuntimeError: If the password is incorrect
    """
    if not password:
        return encrypted_data

    # Extract password hash and encrypted data
    stored_hash = encrypted_data[:32]  # First 32 bytes are the hash
    encrypted = encrypted_data[32:]  # Rest is the encrypted data

    # Verify password
    password_hash = hashlib.sha256(password.encode()).digest()
    if password_hash != stored_hash:
        raise RuntimeError("Invalid password")

    # Decrypt the data
    key_bytes = password.encode("utf-8")
    return bytes(
        encrypted[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(encrypted))
    )


def create_wallet(
    name: str,  # This will be the file name
    wallet_dir: Path,  # Accept the full target directory path
    is_hotkey: bool = False,  # True for hotkey, False for coldkey
    password: str = None,  # Password for encryption
    owner_address: str = None,  # Required for owned hotkeys
    mnemonic: str = None,  # Optional mnemonic for regeneration,
    force: bool = False,  # Skip confirmation prompt or overwrite existing wallet
) -> tuple[str, str, str]:  # Return main wallet file path, ss58_address, and mnemonic
    """
    Create a Hypertensor-compatible wallet in the specified directory.
    Generates a new keypair and saves it as a JSON file with encrypted private key.

    Args:
        name: The desired file name.
        wallet_dir: The full Path object for the directory where the wallet files should be created.
        is_hotkey: True for hotkey, False for coldkey.
        password: Optional password for encryption.
        owner_address: Required for owned hotkeys, specifies the coldkey address that owns this hotkey.
        mnemonic: Optional mnemonic phrase for regeneration. If provided, uses this instead of generating a new one.

    Returns:
        Tuple of (main_wallet_file_path, ss58_address, mnemonic)
    """
    # Create directory if it doesn't exist
    wallet_dir.mkdir(parents=True, exist_ok=True)

    main_wallet_file_path = wallet_dir / f"{name}.key"

    # Check if wallet file already exists
    if main_wallet_file_path.exists():
        if not force:
            raise ValueError(
                f"Wallet file '{name}' already exists in {wallet_dir}. Use --force to overwrite existing file or choose another name."
            )
        else:
            # Remove existing file
            logger.info(
                f"Wallet file '{name}' already exists in {wallet_dir}. Overwriting existing file."
            )  # Add to logging
            logger.info(f"Removing existing file '{name}'...")  # Add to logging
            main_wallet_file_path.unlink()
            logger.info(f"Removed existing file '{name}'.")  # Add to logging

    # Validate owner_address for owned hotkeys
    if is_hotkey and owner_address:
        if not owner_address.startswith("5"):
            raise ValueError(
                "Owner address must be a valid SS58 address starting with '5'"
            )

    # Generate or use provided mnemonic
    if not mnemonic:
        mnemonic = Keypair.generate_mnemonic()

    # Create keypair from mnemonic
    keypair = create_keypair_from_mnemonic(mnemonic)

    # Generate account ID from public key
    account_id = get_account_id(keypair.public_key)

    # Prepare wallet data
    wallet_data = {
        "isHotkey": is_hotkey,  # True for hotkey, False for coldkey
        "accountId": account_id,  # 32-byte blake2b hash of public key
        "publicKey": account_id,  # Same as accountId
        "ss58Address": keypair.ss58_address,
        "isEncrypted": password
        is not None,  # Add flag to indicate if wallet is encrypted
    }

    # Add owner address for owned hotkeys
    if is_hotkey and owner_address:
        wallet_data["owner"] = owner_address

    # Store private key
    if password:
        encrypted_private_key = encrypt_data(keypair.private_key, password)
        wallet_data["privateKey"] = "0x" + encrypted_private_key.hex()
    else:
        wallet_data["privateKey"] = "0x" + keypair.private_key.hex()

    try:
        with open(main_wallet_file_path, "w") as f:
            json.dump(wallet_data, f, indent=4)
        os.chmod(main_wallet_file_path, 0o600)  # Secure file permissions
    except Exception as e:
        if main_wallet_file_path.exists():
            os.remove(main_wallet_file_path)
        raise RuntimeError(f"Failed to save wallet file: {e}")

    return str(main_wallet_file_path), keypair.ss58_address, mnemonic


def import_wallet(name: str, wallet_dir: Path, password: str = None) -> Keypair:
    """
    Import a wallet and return its keypair.

    Args:
        name (str): Name of the wallet
        wallet_dir (Path): Directory containing the wallet file
        password (str, optional): Password for encrypted wallets

    Returns:
        Keypair: The wallet's keypair

    Raises:
        ValueError: If wallet file is not found or invalid
        RuntimeError: If password is incorrect or wallet is corrupted
    """
    wallet_path = wallet_dir / f"{name}.key"
    if not wallet_path.exists():
        raise ValueError(f"Wallet file not found at {wallet_path}")

    try:
        with open(wallet_path) as f:
            wallet_data = json.load(f)
    except json.JSONDecodeError:
        raise ValueError("Invalid wallet file: not a valid Key file")

    # Get private key
    private_key_hex = wallet_data.get("privateKey", "").replace("0x", "")
    if not private_key_hex:
        raise ValueError("Invalid wallet file: missing private key")

    try:
        private_key_bytes = bytes.fromhex(private_key_hex)
    except ValueError:
        raise ValueError("Invalid wallet file: private key is not valid hex")

    # Check if wallet is encrypted
    is_encrypted = wallet_data.get("isEncrypted")
    if is_encrypted is None:
        is_encrypted = len(private_key_bytes) != 32

    # For unencrypted wallets
    if not is_encrypted:
        if password:
            raise RuntimeError("Invalid password: This wallet is not encrypted")
        try:
            return Keypair.create_from_private_key(private_key_bytes, ss58_format=42)
        except Exception as e:
            raise RuntimeError(f"Failed to create keypair: {str(e)}")

    # For encrypted wallets
    if not password:
        raise RuntimeError(
            "Invalid password: Wallet is encrypted but no password provided"
        )

    try:
        private_key_bytes = decrypt_data(private_key_bytes, password)
        if not is_valid_private_key(private_key_bytes):
            raise RuntimeError("Invalid password: Failed to decrypt private key")
    except Exception:
        raise RuntimeError("Invalid password: Failed to decrypt private key")

    try:
        return Keypair.create_from_private_key(private_key_bytes, ss58_format=42)
    except Exception as e:
        raise RuntimeError(f"Failed to create keypair: {str(e)}")


def is_valid_private_key(private_key_bytes: bytes) -> bool:
    """
    Validate if the decrypted private key is valid.

    Args:
        private_key_bytes (bytes): The decrypted private key bytes

    Returns:
        bool: True if the private key is valid, False otherwise
    """
    try:
        # Try to create a keypair with the private key
        Keypair.create_from_private_key(private_key_bytes, ss58_format=42)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    print(
        create_wallet(
            name="w8",
            wallet_dir=Path("~/.hypertensor/wallets"),
            is_hotkey=True,
            password="",
            owner_address="",
            mnemonic="",
        ).ss58_address,
        "a",
    )
