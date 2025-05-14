import os
from pathlib import Path
import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ed25519
import multihash
from hivemind.proto import crypto_pb2
from hivemind.p2p.p2p_daemon_bindings.datastructures import PeerID

def create_wallet(name: str, key_type: str = "ed25519", path: str = None, mnemonic: str = None, password: str = None) -> tuple[str, PeerID]:
    """
    Create or regenerate a wallet with cryptographic keys
    
    Args:
        name: Name of the wallet
        key_type: Type of key to generate (ed25519 or rsa)
        path: Path to store the wallet (optional)
        mnemonic: Mnemonic for regenerating wallet (optional)
        password: Password for encrypting the private key
    
    Returns:
        tuple: (wallet_path, peer_id)
    """
    # Use default path if not provided
    if path is None:
        path = os.path.expanduser("~/.hypertensor/wallets")
    
    # Create wallet directory if it doesn't exist
    wallet_dir = Path(path)
    wallet_dir.mkdir(parents=True, exist_ok=True)
    
    # Create wallet file path
    wallet_path = wallet_dir / f"{name}.wallet"
    
    if wallet_path.exists() and not mnemonic:
        raise ValueError(f"Wallet '{name}' already exists at {wallet_path}")
    
    try:
        # Generate keys based on type
        if key_type.lower() == "rsa":
            # Generate RSA key pair
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
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
            
            # Save private key with password encryption
            private_key_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(password.encode()) if password else serialization.NoEncryption()
            )
            
            # Create and save PrivateKey protobuf
            private_key_proto = crypto_pb2.PrivateKey(
                key_type=crypto_pb2.RSA,
                data=private_key_bytes
            )
            
        elif key_type.lower() == "ed25519":
            # Generate Ed25519 key pair
            private_key = ed25519.Ed25519PrivateKey.generate()
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
            
            # Save private key with password encryption
            private_key_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(password.encode()) if password else serialization.NoEncryption()
            )
            
            # Create and save PrivateKey protobuf
            private_key_proto = crypto_pb2.PrivateKey(
                key_type=crypto_pb2.Ed25519,
                data=private_key_bytes
            )
            
        else:
            raise ValueError("Invalid key type. Supported types: rsa, ed25519")
        
        # Save the private key to file
        with open(wallet_path, "wb") as f:
            f.write(private_key_proto.SerializeToString())
        
        # Generate and return PeerID
        peer_id = PeerID(encoded_digest)
        return str(wallet_path), peer_id
        
    except Exception as e:
        raise Exception(f"Failed to create wallet: {str(e)}") 