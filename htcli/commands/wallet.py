import typer
import os
from pathlib import Path
import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ed25519
import multihash
from hivemind.proto import crypto_pb2
from hivemind.p2p.p2p_daemon_bindings.datastructures import PeerID
from hivemind.utils.logging import get_logger
from htcli.core.config import wallet_config
from htcli.utils.wallet import create_wallet
import getpass

logger = get_logger(__name__)

app = typer.Typer(name="wallet", help="Wallet commands")

@app.command()
def info():
    """
    Get the info of the wallet
    """
    typer.echo("Getting info of the wallet...")
    # Here you would implement the logic to get the info of the wallet
    # For now, we'll just print a message
    # This is a placeholder for the actual implementation

@app.command()
def create(
    name: str = typer.Option(None, "--wallet.name", help="Name of the wallet"),
    password: str = typer.Option(None, "--wallet.password", help="Password for the wallet"),
    key_type: str = typer.Option("ed25519", "--wallet.key-type", help="Type of key to generate (ed25519 or rsa)"),
    path: str = typer.Option(None, "--wallet.path", help="Path to store the wallet")
):
    """
    Create a new wallet with cryptographic keys
    """
    # Prompt for missing required parameters
    if not name:
        name = typer.prompt("Enter wallet name")
    if not password:
        password = getpass.getpass("Enter wallet password: ")
    
    try:
        wallet_path, peer_id = create_wallet(name, key_type, path, password=password)
        typer.echo(f"Successfully created wallet '{name}' at {wallet_path}")
        typer.echo(f"Peer ID: {peer_id}")
    except Exception as e:
        typer.echo(str(e))
        raise typer.Exit(code=1)

@app.command()
def list(
    path: str = typer.Option(None, "--path", help="Path to the wallets directory (optional)")
):
    """
    List all available wallets and their public keys
    """
    # Use default path if not provided
    if path is None:
        path = os.path.expanduser("~/.hypertensor/wallets")
    
    # Get wallet directory
    wallet_dir = Path(path)
    
    if not wallet_dir.exists():
        typer.echo(f"No wallets directory found at {wallet_dir}")
        raise typer.Exit(code=1)
    
    # Find all wallet files
    wallet_files = [f for f in wallet_dir.glob("*.wallet")]
    
    if not wallet_files:
        typer.echo("No wallets found")
        return
    
    # Display wallet information
    typer.echo("\nAvailable Wallets:")
    typer.echo("-" * 80)
    
    for wallet_file in wallet_files:
        try:
            # Get wallet name (remove .wallet extension)
            wallet_name = wallet_file.stem
            
            # Read the private key file
            with open(wallet_file, "rb") as f:
                data = f.read()
                try:
                    private_key_proto = crypto_pb2.PrivateKey.FromString(data)
                except Exception as e:
                    typer.echo(f"Wallet: {wallet_name}")
                    typer.echo(f"Status: Invalid format - {str(e)}")
                    typer.echo(f"Path: {wallet_file}")
                    typer.echo("-" * 80)
                    continue
                
                if private_key_proto.key_type == crypto_pb2.RSA:
                    try:
                        # Load RSA private key
                        private_key = serialization.load_der_private_key(
                            private_key_proto.data,
                            password=None
                        )
                        
                        # Get public key in DER format
                        public_key = private_key.public_key().public_bytes(
                            encoding=serialization.Encoding.DER,
                            format=serialization.PublicFormat.SubjectPublicKeyInfo
                        )
                        
                        # Create crypto_pb2.PublicKey
                        encoded_public_key = crypto_pb2.PublicKey(
                            key_type=crypto_pb2.RSA,
                            data=public_key
                        ).SerializeToString()
                        
                        # Generate multihash
                        encoded_digest = multihash.encode(
                            hashlib.sha256(encoded_public_key).digest(),
                            multihash.coerce_code("sha2-256")
                        )
                        key_type = "RSA"
                        
                    except Exception as e:
                        typer.echo(f"Wallet: {wallet_name}")
                        typer.echo(f"Status: Invalid RSA key - {str(e)}")
                        typer.echo(f"Path: {wallet_file}")
                        typer.echo("-" * 80)
                        continue
                    
                elif private_key_proto.key_type == crypto_pb2.Ed25519:
                    try:
                        # Load Ed25519 private key
                        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_proto.data[:32])
                        public_key = private_key.public_key().public_bytes(
                            encoding=serialization.Encoding.Raw,
                            format=serialization.PublicFormat.Raw
                        )
                        
                        # Create crypto_pb2.PublicKey
                        encoded_public_key = crypto_pb2.PublicKey(
                            key_type=crypto_pb2.Ed25519,
                            data=public_key
                        ).SerializeToString()
                        
                        # Generate encoded digest
                        encoded_digest = b"\x00$" + encoded_public_key
                        key_type = "Ed25519"
                        
                    except Exception as e:
                        typer.echo(f"Wallet: {wallet_name}")
                        typer.echo(f"Status: Invalid Ed25519 key - {str(e)}")
                        typer.echo(f"Path: {wallet_file}")
                        typer.echo("-" * 80)
                        continue
                    
                else:
                    typer.echo(f"Wallet: {wallet_name}")
                    typer.echo(f"Status: Unsupported key type - {private_key_proto.key_type}")
                    typer.echo(f"Path: {wallet_file}")
                    typer.echo("-" * 80)
                    continue
                
                # Generate and display PeerID
                if encoded_digest:
                    peer_id = PeerID(encoded_digest)
                    typer.echo(f"Wallet: {wallet_name}")
                    typer.echo(f"Type: {key_type}")
                    typer.echo(f"Peer ID: {peer_id}")
                    typer.echo(f"Path: {wallet_file}")
                    typer.echo("-" * 80)
                
        except Exception as e:
            typer.echo(f"Wallet: {wallet_name}")
            typer.echo(f"Status: Error reading wallet - {str(e)}")
            typer.echo(f"Path: {wallet_file}")
            typer.echo("-" * 80)
  
@app.command()
def delete(
    name: str = wallet_config.name,
    path: str = wallet_config.path
):
    """
    delete a wallet by name
    """
    # Use default path if not provided
    if path is None:
        path = os.path.expanduser("~/.hypertensor/wallets")
    
    # Get wallet directory
    wallet_dir = Path(path)

    if not wallet_dir.exists():
        typer.echo(f"No wallets directory found at {wallet_dir}")
        raise typer.Exit(code=1)
    
    # Create wallet file path
    wallet_path = wallet_dir / f"{name}.wallet"

    if not wallet_path.exists():
        typer.echo(f"Wallet '{name}' not found at {wallet_path}")
        raise typer.Exit(code=1)
    
    try:
        # Delete the wallet file
        wallet_path.unlink()
        typer.echo(f"Successfully deleted wallet '{name}' at {wallet_path}")
    except Exception as e:
        typer.echo(f"Failed to delete wallet: {str(e)}")
        raise typer.Exit(code=1)
        
@app.command()
def regen(
    name: str = wallet_config.name,
    mnemonic: str = wallet_config.mnemonic,
    key_type: str = wallet_config.key_type,
    path: str = wallet_config.path
):
    """
    Regenerate a wallet using mnemonic
    """
    if not mnemonic:
        typer.echo("Mnemonic is required for wallet regeneration")
        raise typer.Exit(code=1)
        
    try:
        wallet_path, peer_id = create_wallet(name, key_type, path, mnemonic)
        typer.echo(f"Successfully regenerated wallet '{name}' at {wallet_path}")
        typer.echo(f"Peer ID: {peer_id}")
    except Exception as e:
        typer.echo(str(e))
        raise typer.Exit(code=1)

@app.command()
def reveal(
    name: str = wallet_config.name,
    path: str = wallet_config.path
):
    """
    reveal mnemonic key for a wallet. Requires password confirmation.
    """
    # Use default path if not provided
    if path is None:
        path = os.path.expanduser("~/.hypertensor/wallets")
    
    # Get wallet directory
    wallet_dir = Path(path)

    if not wallet_dir.exists():
        typer.echo(f"No wallets directory found at {wallet_dir}")
        raise typer.Exit(code=1)
    
    # Create wallet file path
    wallet_path = wallet_dir / f"{name}.wallet"

    if not wallet_path.exists():
        typer.echo(f"Wallet '{name}' not found at {wallet_path}")
        raise typer.Exit(code=1)
    
    # Prompt for password
    password = getpass.getpass("Enter wallet password: ")
    if not password:
        typer.echo("Password cannot be empty")
        raise typer.Exit(code=1)
    
    try:
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
            peer_id = PeerID(encoded_digest)
            
            # Display wallet information
            typer.echo("\nWallet Information:")
            typer.echo("-" * 80)
            typer.echo(f"Name: {name}")
            typer.echo(f"Type: {key_type}")
            typer.echo(f"Peer ID: {peer_id}")
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
            
    except Exception as e:
        typer.echo(f"Failed to reveal wallet: {str(e)}")
        raise typer.Exit(code=1)

