import typer
import os
from pathlib import Path
from cryptography.fernet import Fernet
import getpass
from substrateinterface import Keypair

def keypair_from_name(
    name: str = None,
    path: str = None,
) -> Keypair:
    """
    return Keypair object with the given wallet name

    Args:
        name: Name of the wallet (if not provided, use "default")
        path: Path to the wallet (optional)

    Returns:
        Keypair
    """

    # Use default wallet name "default" if not provided
    if name is None:
        name = "default"

    # Use default path if not provided
    if path is None:
        path = os.path.expanduser("~/.hypertensor/wallets")

    # Create wallet directory if it doesn't exist
    wallet_dir = Path(path)
    wallet_dir.mkdir(parents=True, exist_ok=True)

    # Create wallet file path
    wallet_path = wallet_dir / name / "coldkey"
        
    # Prompt for password
    # password = getpass.getpass("Enter wallet password: ")
    # if not password:
    #     typer.echo("Password cannot be empty")
    #     raise typer.Exit(code=1)
    
    # Read the encrypted private key file
    with open(wallet_path, "rb") as f:
        private_key_bytes = f.read()
        
    # Generate encryption key from password
    encryption_key = Fernet.generate_key()
    cipher = Fernet(encryption_key)

    # # Decrypt the private key
    # try:
    #     private_key_bytes = cipher.decrypt(encrypted_private_key)
    # except Exception:
    #     typer.echo("Invalid password or corrupted wallet")
    #     raise typer.Exit(code=1)

    # Return the Keypair object from the private key
    return Keypair.create_from_private_key(
        private_key_bytes,
        ss58_format=42
    )

if __name__ == "__main__":
    print(keypair_from_name(name="test").ss58_address)