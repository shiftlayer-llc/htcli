import os
from pathlib import Path
from substrateinterface import Keypair
import json


def obfuscate_bytes(data: bytes, key: str) -> bytes:
    """
    Basic XOR obfuscation/de-obfuscation of bytes using a key string.
    If no key is provided, returns the original data unchanged.
    """
    if not key:
        return data  # Return original data if no password
    key_bytes = key.encode("utf-8")
    return bytes(data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data)))


def create_wallet(
    name: str,  # This will be the file name (coldkey or hotkey name)
    wallet_dir: Path,  # Accept the full target directory path
    password: str = None,  # Add password parameter
    save_as_json: bool = False,  # New parameter to control saving format
    mnemonic: str = None,  # Optional mnemonic for regeneration
) -> tuple[str, str, str]:  # Return main wallet file path, ss58_address, and mnemonic
    """
    Create a Hypertensor-compatible wallet (coldkey or hotkey) in the specified directory.
    Generates a new keypair and saves it either as raw private key bytes + .pub file (default) or as a JSON file.

    Args:
        name: The desired file name.
        wallet_dir: The full Path object for the directory where the wallet files should be created.
        password: Optional password for basic obfuscation.
        save_as_json: If True, saves data as a single JSON file with all info. If False (default), saves raw private key + .pub file.
        mnemonic: Optional mnemonic phrase for regeneration. If provided, uses this instead of generating a new one.

    Returns:
        Tuple of (main_wallet_file_path, ss58_address, mnemonic)
    """
    # Create directory if it doesn't exist
    wallet_dir.mkdir(parents=True, exist_ok=True)

    main_wallet_file_path = wallet_dir / name

    # Check if wallet file already exists
    if main_wallet_file_path.exists():
        # We don't know if it's a coldkey or hotkey here anymore, simplify the error message
        # Refine error message to be more general as file name could be coldkey or hotkey name
        raise ValueError(
            f"Wallet file '{name}' already exists in {wallet_dir}. Remove existing file or use a different name."
        )

    # If saving as JSON, also check if .pub file exists (though we won't create it in this case)
    # This check is more relevant for the default raw+pub format, but keep a basic check for filename collision
    if not save_as_json and (wallet_dir / f"{name}.pub").exists():
        raise ValueError(
            f".pub file with name '{name}.pub' already exists in {wallet_dir}. Remove existing file or use a different name."
        )

    # Generate keypair using provided mnemonic or generate new one
    try:
        if mnemonic:
            keypair = Keypair.create_from_mnemonic(mnemonic, ss58_format=42)
        else:
            mnemonic = Keypair.generate_mnemonic()
            keypair = Keypair.create_from_mnemonic(mnemonic, ss58_format=42)
    except Exception as e:
        raise RuntimeError(f"Failed to generate keypair: {e}")

    def obfuscate_str(data: str, key: str) -> str:
        if not key:
            return data  # Return original data if no password
        return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

    if save_as_json:
        # --- Save as JSON file (for hotkeys) ---
        # Obfuscate private key and mnemonic (secretPhrase) if password is provided
        obfuscated_private_key_hex = obfuscate_bytes(
            keypair.private_key, password
        ).hex()
        obfuscated_mnemonic = obfuscate_str(keypair.mnemonic, password)

        wallet_data = {
            "accountId": "0x" + keypair.public_key.hex(),
            "publicKey": "0x" + keypair.public_key.hex(),
            "privateKey": "0x"
            + obfuscated_private_key_hex,  # Save obfuscated private key hex
            "secretPhrase": obfuscated_mnemonic,  # Save obfuscated mnemonic
            "secretSeed": None,  # Seed not directly available from mnemonic in this way
            "ss58Address": keypair.ss58_address,
        }

        try:
            with open(main_wallet_file_path, "w") as f:
                json.dump(wallet_data, f, indent=4)
            os.chmod(main_wallet_file_path, 0o600)  # Secure file permissions
        except Exception as e:
            # Clean up file if saving fails
            if main_wallet_file_path.exists():
                os.remove(main_wallet_file_path)
            raise RuntimeError(f"Failed to save wallet JSON file: {e}")

        return str(main_wallet_file_path), keypair.ss58_address, mnemonic

    else:
        # --- Save as raw private key bytes + .pub file (for coldkeys) ---
        private_key_file_path = (
            main_wallet_file_path  # In this case, main file is the private key file
        )
        public_key_file_path = wallet_dir / f"{name}.pub"

        # Obfuscate private key bytes if password is provided
        private_bytes_to_save = obfuscate_bytes(keypair.private_key, password)

        # Save obfuscated private key bytes
        try:
            with open(private_key_file_path, "wb") as f:
                f.write(private_bytes_to_save)
            os.chmod(private_key_file_path, 0o600)  # Secure file permissions
        except Exception as e:
            raise RuntimeError(f"Failed to save private key file: {e}")

        # Save public key info to .pub file
        pub_data = {
            "accountId": "0x" + keypair.public_key.hex(),
            "ss58Address": keypair.ss58_address,
            "publicKey": "0x" + keypair.public_key.hex(),
        }
        try:
            with open(public_key_file_path, "w") as f:
                json.dump(pub_data, f, indent=4)
            os.chmod(public_key_file_path, 0o600)  # Secure file permissions
        except Exception as e:
            # Clean up private key file if public key file saving fails
            if private_key_file_path.exists():
                os.remove(private_key_file_path)
            raise RuntimeError(f"Failed to save public key file: {e}")

        return str(private_key_file_path), keypair.ss58_address, mnemonic


if __name__ == "__main__":
    print(
        create_wallet(
            name="w8",
            wallet_dir=Path("~/.hypertensor/wallets"),
            save_as_json=False,
            mnemonic="",
        ).ss58_address,
        "a",
    )
