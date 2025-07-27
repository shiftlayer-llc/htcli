import json
from pathlib import Path


def read_wallet_data_for_verification(file_path: Path, is_json: bool, password: str):
    """
    Read and deobfuscate wallet data from a file.

    Args:
        file_path (Path): Path to the wallet file
        is_json (bool): Whether the file is in JSON format
        password (str): Password for deobfuscation

    Returns:
        bytes: Deobfuscated private key bytes
    """
    if is_json:
        with open(file_path, "r") as f:
            wallet_data = json.load(f)
            obfuscated_private_key_hex = wallet_data.get("privateKey", "").replace(
                "0x", ""
            )
            obfuscated_private_key_bytes = bytes.fromhex(obfuscated_private_key_hex)
            # De-obfuscate the private key bytes
            return deobfuscate_bytes(obfuscated_private_key_bytes, password)
    else:
        with open(file_path, "rb") as f:
            saved_obfuscated_private_key = f.read()
            # De-obfuscate the private key bytes
            return deobfuscate_bytes(saved_obfuscated_private_key, password)


def deobfuscate_bytes(data: bytes, key: str) -> bytes:
    """
    Deobfuscate bytes using a key.

    Args:
        data (bytes): The obfuscated data
        key (str): The key to use for deobfuscation

    Returns:
        bytes: The deobfuscated data
    """
    if not key:
        return data
    key_bytes = key.encode("utf-8")
    return bytes(data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data)))
