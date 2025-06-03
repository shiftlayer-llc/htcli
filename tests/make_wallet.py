from substrateinterface import Keypair
import json
from pathlib import Path
import os

# Generate keypair
mnemonic = Keypair.generate_mnemonic()
print("Generated mnemonic:", mnemonic)
keypair = Keypair.create_from_mnemonic(mnemonic, ss58_format=42)
# keypair = Keypair.create_from_uri('//CHARLIE')

# Get private key bytes
private_bytes = keypair.private_key

# Write public information to `coldkey.pub`
pub_data = {
    "accountId": "0x" + keypair.public_key.hex(),
    "ss58Address": keypair.ss58_address,
    "publicKey": "0x" + keypair.public_key.hex()
}

wallet_dir = Path(os.path.expanduser("~/.hypertensor/wallets/node3"))
wallet_dir.mkdir(parents=True, exist_ok=True)
wallet_path = wallet_dir / "coldkey.pub"

# Write private key to `coldkey` without encryption
with open(wallet_dir / "coldkey", "wb") as f:
    f.write(private_bytes)

with open(wallet_path, "w") as f:
    json.dump(pub_data, f, indent=4)