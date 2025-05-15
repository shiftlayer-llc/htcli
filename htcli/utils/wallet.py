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
        data = f.read()
        private_key_proto = crypto_pb2.PrivateKey.FromString(data)
    
        # Get key type
        key_type = "RSA" if private_key_proto.key_type == crypto_pb2.RSA else "Ed25519"
        
        try:
            # Load private key with password
            private_key = serialization.load_der_private_key(
                private_key_proto.data,
                password=password.encode()
            )
        except Exception:
            typer.echo("Invalid password")
            raise typer.Exit(code=1)


        # Get public key
        public_key = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        # Create crypto_pb2.PublicKey
        encoded_public_key = crypto_pb2.PublicKey(
            key_type=private_key_proto.key_type,
            data=public_key
        ).SerializeToString()
        

        # Generate encoded digest
        if key_type == "RSA":
            encoded_digest = multihash.encode(
                hashlib.sha256(encoded_public_key).digest(),
                multihash.coerce_code("sha2-256")
            )
        else:
            encoded_digest = b"\x00$" + encoded_public_key
        
        # Generate and display PeerID
        # peer_id = PeerID(encoded_digest)

        # Display wallet information
        typer.echo("\nWallet Information:")
        typer.echo("-" * 80)
        typer.echo(f"Name: {name}")
        typer.echo(f"Type: {key_type}")
        # typer.echo(f"Peer ID: {peer_id}")
        typer.echo(f"Path: {wallet_path}")
        
        # Display mnemonic key
        typer.echo("\nMnemonic Key:")
        typer.echo("-" * 80)
        # Convert private key to mnemonic format
        mnemonic = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        ).hex()
        typer.echo(mnemonic)
        typer.echo("-" * 80)
        
        return Keypair.create_from_private_key(
            private_key,
            public_key=public_key,
            crypto_type=KeypairType.ECDSA,
        )

