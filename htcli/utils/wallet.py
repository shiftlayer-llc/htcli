import typer
import os
from pathlib import Path
import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ed25519
import multihash
from htcli.utils import crypto_pb2
import getpass
from substrateinterface import KeypairType, Keypair

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
    wallet_path = wallet_dir / f"{name}.wallet"
        
    # Prompt for password
    password = getpass.getpass("Enter wallet password: ")
    if not password:
        typer.echo("Password cannot be empty")
        raise typer.Exit(code=1)
    
    # Read the private key file
    with open(wallet_path, "rb") as f:
        # Get Key proto from the private key raw bytes
        private_key_proto = crypto_pb2.PrivateKey.FromString(f.read())
        
        try:
            # Load private key with password
            private_key = serialization.load_der_private_key(
                private_key_proto.data,
                password=password.encode()
            )
        except Exception:
            typer.echo("Invalid password")
            raise typer.Exit(code=1)

        # Get private key bytes
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        ).hex()
        
        # Return the Keypair object from the private key
        return Keypair.create_from_private_key(
            private_key_bytes,
            crypto_type=KeypairType.ECDSA,
        )

