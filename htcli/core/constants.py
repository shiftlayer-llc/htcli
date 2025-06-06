import os
from pathlib import Path

# Default paths
DEFAULT_WALLET_PATH = str(Path.home() / ".hypertensor" / "wallets")

# Default chain values
DEFAULT_RPC_URL = "wss://hypertensor.duckdns.org"
DEFAULT_CHAIN_ENV = "testnet"
CHAIN_ENV_URLS = {
    "local": "ws://localhost:8545",
    "testnet": "wss://hypertensor.duckdns.org",
    "mainnet": "wss://mainnet.hypertensor.org",
}
# Default subnet values
DEFAULT_SUBNET_ID = 0
DEFAULT_SUBNET_NAME = "default"

BLOCK_SECS = 6
# Default subnet register values
DEFAULT_MODEL_PATH = ""
DEFAULT_NODE_REGISTRATION_EPOCHS = 1000
DEFAULT_NODE_REGISTRATION_INTERVAL = 100
DEFAULT_NODE_AACTIVATION_INTERVAL = 100
DEFAULT_NODE_QUEUE_PERIOD = 10
DEFAULT_MAX_NODE_PENALTIES = 5
