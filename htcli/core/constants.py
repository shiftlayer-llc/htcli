import os
from pathlib import Path

# Default paths
DEFAULT_WALLET_PATH = str(Path.home() / ".hypertensor" / "wallets")

# Default chain values
DEFAULT_RPC_URL = "ws://127.0.0.1:9944"
DEFAULT_CHAIN_ENV = "local"

# Default subnet values
DEFAULT_SUBNET_ID = 0
DEFAULT_SUBNET_NAME = "default"

# Wallet file names
COLDKEY_FILE_NAME = "coldkey"
HOTKEYS_DIR_NAME = "hotkeys"
