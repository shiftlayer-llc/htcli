# API Reference

Complete API reference for the Hypertensor CLI, including client methods, request/response models, and integration examples.

## 🎯 Overview

The Hypertensor CLI provides a comprehensive programmatic API for blockchain integration:

- **Client Architecture**: Modular client design for easy integration
- **Real Blockchain Integration**: Direct SubstrateInterface integration
- **Comprehensive Methods**: Complete coverage of blockchain operations
- **Error Handling**: Robust error handling and recovery
- **Type Safety**: Pydantic models for request/response validation

## 🏗️ Client Architecture

### Client Initialization

```python
from src.htcli.client import HypertensorClient

# Initialize client
client = HypertensorClient()

# Or with custom configuration
from src.htcli.config import load_config
config = load_config()
client = HypertensorClient(config=config)
```

### Client Components

- **Subnet Client**: Subnet registration and management
- **Node Client**: Node lifecycle management
- **Staking Client**: Staking operations and portfolio management
- **Wallet Client**: Key management and wallet operations
- **Chain Client**: Blockchain queries and information

## 🔑 Subnet Operations API

### Register Subnet

```python
from src.htcli.models.requests import SubnetRegisterRequest

request = SubnetRegisterRequest(
    name="My AI Subnet",
    repo="https://github.com/my/ai-subnet",
    description="Advanced AI computation subnet",
    min_stake=1000000000000000000,
    max_stake=10000000000000000000,
    churn_limit=4,
    registration_epochs=10,
    activation_grace_epochs=5,
    idle_epochs=3,
    included_epochs=2,
    max_penalties=3,
    initial_coldkeys=["5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu"],
    key_types=["RSA", "Ed25519"]
)

response = client.register_subnet(request, keypair)
print(f"Subnet registered: {response.success}")
print(f"Transaction hash: {response.transaction_hash}")
```

### Activate Subnet

```python
response = client.activate_subnet(
    subnet_id=1,
    keypair=keypair
)
print(f"Subnet activated: {response.success}")
```

### Pause/Unpause Subnet

```python
# Pause subnet
response = client.pause_subnet(
    subnet_id=1,
    keypair=keypair
)

# Unpause subnet
response = client.unpause_subnet(
    subnet_id=1,
    keypair=keypair
)
```

### Update Subnet Parameters

```python
# Update subnet name
response = client.owner_update_name(
    subnet_id=1,
    name="Updated Subnet Name",
    keypair=keypair
)

# Update subnet repository
response = client.owner_update_repo(
    subnet_id=1,
    repo="https://github.com/my/updated-subnet",
    keypair=keypair
)

# Update subnet description
response = client.owner_update_description(
    subnet_id=1,
    description="Updated description",
    keypair=keypair
)
```

### Ownership Management

```python
# Transfer ownership
response = client.transfer_subnet_ownership(
    subnet_id=1,
    new_owner="5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu",
    keypair=keypair
)

# Accept ownership
response = client.accept_subnet_ownership(
    subnet_id=1,
    keypair=keypair
)

# Undo ownership transfer
response = client.undo_subnet_ownership_transfer(
    subnet_id=1,
    keypair=keypair
)
```

### Get Subnet Information

```python
# Get subnet data
subnet_data = client.get_subnet_data(subnet_id=1)
print(f"Subnet name: {subnet_data.name}")
print(f"Total nodes: {subnet_data.total_nodes}")

# List all subnets
subnets = client.list_subnets()
for subnet in subnets:
    print(f"Subnet {subnet.id}: {subnet.name}")
```

## 🔗 Node Operations API

### Register Node

```python
from src.htcli.models.requests import SubnetNodeAddRequest

request = SubnetNodeAddRequest(
    subnet_id=1,
    hotkey="5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu",
    peer_id="12D3KooWABC123DEF456",
    bootnode_peer_id="12D3KooWXYZ789GHI012",
    client_peer_id="12D3KooWJKL345MNO678",
    stake_amount=1000000000000000000,
    delegate_reward_rate=50000000000000000,
    bootnode="/ip4/127.0.0.1/tcp/30333/p2p/12D3KooWABC123DEF456"
)

response = client.register_subnet_node(request, keypair)
print(f"Node registered: {response.success}")
```

### Node Lifecycle Management

```python
# Activate node
response = client.activate_subnet_node(
    subnet_id=1,
    node_id=5,
    keypair=keypair
)

# Update delegate reward rate
response = client.update_node_delegate_reward_rate(
    subnet_id=1,
    node_id=5,
    new_delegate_reward_rate=60000000000000000,
    keypair=keypair
)

# Update coldkey
response = client.update_node_coldkey(
    subnet_id=1,
    hotkey="5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu",
    new_coldkey="5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu",
    keypair=keypair
)

# Update hotkey
response = client.update_node_hotkey(
    subnet_id=1,
    old_hotkey="5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu",
    new_hotkey="5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu",
    keypair=keypair
)
```

### Node Deactivation and Reactivation

```python
# Deactivate node
response = client.deactivate_subnet_node(
    subnet_id=1,
    node_id=5,
    keypair=keypair
)

# Reactivate node
response = client.reactivate_subnet_node(
    subnet_id=1,
    node_id=5,
    keypair=keypair
)
```

### Node Removal and Cleanup

```python
# Remove node
response = client.remove_subnet_node(
    subnet_id=1,
    node_id=5,
    keypair=keypair
)

# Cleanup expired nodes
response = client.cleanup_expired_node(
    subnet_id=1,
    node_id=5,
    cleanup_type="deactivated",
    keypair=keypair
)
```

### Get Node Information

```python
# Get node status
node_status = client.get_subnet_node_status(subnet_id=1, node_id=5)
print(f"Node classification: {node_status.classification}")
print(f"Stake amount: {node_status.stake_amount}")

# List nodes
nodes = client.list_subnet_nodes(subnet_id=1)
for node in nodes:
    print(f"Node {node.id}: {node.hotkey}")
```

## 💰 Staking Operations API

### Subnet Delegate Staking

```python
# Add subnet delegate stake
response = client.add_to_delegate_stake(
    subnet_id=1,
    amount=1000000000000000000,
    keypair=keypair
)

# Remove subnet delegate stake
response = client.remove_delegate_stake(
    subnet_id=1,
    shares=500000000000000000,
    keypair=keypair
)

# Transfer subnet delegate stake
response = client.transfer_delegate_stake(
    subnet_id=1,
    to_account="5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu",
    shares=100000000000000000,
    keypair=keypair
)

# Increase subnet delegate stake pool
response = client.increase_delegate_stake(
    subnet_id=1,
    amount=500000000000000000,
    keypair=keypair
)
```

### Node Delegate Staking

```python
# Add node delegate stake
response = client.add_to_node_delegate_stake(
    subnet_id=1,
    node_id=5,
    amount=1000000000000000000,
    keypair=keypair
)

# Remove node delegate stake
response = client.remove_node_delegate_stake(
    subnet_id=1,
    node_id=5,
    shares=500000000000000000,
    keypair=keypair
)

# Transfer node delegate stake
response = client.transfer_node_delegate_stake(
    subnet_id=1,
    node_id=5,
    to_account="5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu",
    shares=100000000000000000,
    keypair=keypair
)

# Increase node delegate stake pool
response = client.increase_node_delegate_stake(
    subnet_id=1,
    node_id=5,
    amount=500000000000000000,
    keypair=keypair
)
```

### Get Staking Information

```python
# Get staking info
staking_info = client.get_stake_info(subnet_id=1, node_id=5)
print(f"Stake amount: {staking_info.stake_amount}")
print(f"Reward rate: {staking_info.reward_rate}")

# Get delegate stake info
delegate_info = client.get_delegate_stake_info(subnet_id=1)
print(f"Total delegate stake: {delegate_info.total_stake}")
print(f"Your shares: {delegate_info.your_shares}")
```

## 🔐 Wallet Operations API

### Key Management

```python
from src.htcli.utils.crypto import generate_keypair, import_keypair, load_keypair

# Generate new keypair
keypair = generate_keypair("my-key", "password123", crypto_type=1)

# Import existing keypair
keypair = import_keypair("imported-key", "0x1234567890abcdef...", "password123", crypto_type=1)

# Load existing keypair
keypair = load_keypair("my-key", "password123")

# List keys
keys = list_keys()
for key in keys:
    print(f"Key: {key['name']}, Address: {key['address']}")
```

### Wallet Status

```python
# Get wallet status
status = get_wallet_status("my-key")
print(f"Address: {status.address}")
print(f"Crypto type: {status.crypto_type}")
print(f"Public key: {status.public_key}")
```

## 🔍 Chain Operations API

### Network Information

```python
# Get network info
network_info = client.get_network_info()
print(f"Total subnets: {network_info.total_subnets}")
print(f"Total nodes: {network_info.total_nodes}")

# Get chain info
chain_info = client.get_chain_info()
print(f"Chain name: {chain_info.name}")
print(f"Chain version: {chain_info.version}")
```

### Balance and Account Information

```python
# Get account balance
balance = client.get_balance("5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu")
print(f"Balance: {balance.free}")

# Get account info
account_info = client.get_account_info("5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu")
print(f"Account nonce: {account_info.nonce}")
```

### Block and Transaction Information

```python
# Get block info
block_info = client.get_block_info(block_number=12345)
print(f"Block hash: {block_info.hash}")
print(f"Block timestamp: {block_info.timestamp}")

# Get transaction info
tx_info = client.get_transaction_info("0x1234567890abcdef...")
print(f"Transaction status: {tx_info.status}")
print(f"Transaction block: {tx_info.block_number}")
```

## 📊 Request/Response Models

### Subnet Register Request

```python
from src.htcli.models.requests import SubnetRegisterRequest

request = SubnetRegisterRequest(
    name="My Subnet",
    repo="https://github.com/my/subnet",
    description="A great subnet",
    min_stake=1000000000000000000,
    max_stake=10000000000000000000,
    churn_limit=4,
    registration_epochs=10,
    activation_grace_epochs=5,
    idle_epochs=3,
    included_epochs=2,
    max_penalties=3,
    initial_coldkeys=["5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu"],
    key_types=["RSA", "Ed25519"]
)
```

### Subnet Node Add Request

```python
from src.htcli.models.requests import SubnetNodeAddRequest

request = SubnetNodeAddRequest(
    subnet_id=1,
    hotkey="5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu",
    peer_id="12D3KooWABC123DEF456",
    bootnode_peer_id="12D3KooWXYZ789GHI012",
    client_peer_id="12D3KooWJKL345MNO678",
    stake_amount=1000000000000000000,
    delegate_reward_rate=50000000000000000,
    bootnode="/ip4/127.0.0.1/tcp/30333/p2p/12D3KooWABC123DEF456"
)
```

### Response Models

```python
from src.htcli.models.responses import (
    SubnetRegisterResponse,
    NodeAddResponse,
    StakeResponse,
    SubnetPauseResponse,
    SubnetUnpauseResponse,
    SubnetOwnershipTransferResponse,
    SubnetOwnerUpdateResponse,
    DelegateStakeIncreaseResponse
)

# Example response handling
response = client.register_subnet(request, keypair)
if response.success:
    print(f"Transaction hash: {response.transaction_hash}")
    print(f"Block number: {response.block_number}")
else:
    print(f"Error: {response.message}")
```

## 🛡️ Error Handling

### Exception Handling

```python
try:
    response = client.register_subnet(request, keypair)
    if response.success:
        print("Subnet registered successfully")
    else:
        print(f"Registration failed: {response.message}")
except Exception as e:
    print(f"Error: {str(e)}")
```

### Validation Errors

```python
from src.htcli.utils.validation import validate_subnet_id, validate_amount

# Validate inputs before API calls
if not validate_subnet_id(subnet_id):
    raise ValueError("Invalid subnet ID")

if not validate_amount(amount):
    raise ValueError("Invalid amount")
```

### Network Errors

```python
try:
    response = client.get_subnet_data(subnet_id=1)
except ConnectionError:
    print("Network connection failed")
except TimeoutError:
    print("Request timed out")
```

## 🔄 Integration Examples

### Automated Node Management

```python
import time
from src.htcli.client import HypertensorClient

client = HypertensorClient()

def monitor_node_performance(subnet_id, node_id, keypair):
    """Monitor node performance and adjust reward rate"""
    while True:
        # Get node status
        status = client.get_subnet_node_status(subnet_id, node_id)

        # Check performance
        if status.attestation_ratio < 0.8:
            # Lower reward rate to reduce delegation
            current_rate = status.delegate_reward_rate
            new_rate = int(current_rate * 0.95)  # 5% decrease

            response = client.update_node_delegate_reward_rate(
                subnet_id, node_id, new_rate, keypair
            )
            print(f"Updated reward rate to {new_rate}")

        time.sleep(3600)  # Check every hour
```

### Portfolio Management Bot

```python
def rebalance_portfolio(client, keypair):
    """Rebalance staking portfolio based on performance"""
    # Get all stakes
    stakes = client.get_stake_info(mine=True)

    # Calculate performance metrics
    total_staked = sum(stake.amount for stake in stakes)
    avg_performance = sum(stake.performance for stake in stakes) / len(stakes)

    # Rebalance if performance is low
    if avg_performance < 0.05:
        # Remove from low-performing stakes
        for stake in stakes:
            if stake.performance < 0.03:
                client.remove_delegate_stake(
                    stake.subnet_id, stake.shares, keypair
                )

        # Add to high-performing subnets
        high_performing_subnets = get_high_performing_subnets()
        for subnet in high_performing_subnets:
            client.add_to_delegate_stake(
                subnet.id, 1000000000000000000, keypair
            )
```

### Network Monitoring

```python
def monitor_network(client):
    """Monitor network health and performance"""
    # Get network stats
    network_info = client.get_network_info()

    # Check for issues
    if network_info.total_nodes < 100:
        print("Warning: Low node count")

    if network_info.total_subnets < 5:
        print("Warning: Low subnet count")

    # Monitor specific subnets
    subnets = client.list_subnets()
    for subnet in subnets:
        subnet_data = client.get_subnet_data(subnet.id)
        if subnet_data.total_nodes < 10:
            print(f"Warning: Subnet {subnet.id} has low node count")
```

## 📈 Performance Optimization

### Connection Pooling

```python
# Reuse client instance
client = HypertensorClient()

# Multiple operations with same client
for subnet_id in range(1, 6):
    subnet_data = client.get_subnet_data(subnet_id)
    print(f"Subnet {subnet_id}: {subnet_data.name}")
```

### Batch Operations

```python
def batch_stake_operations(client, keypair):
    """Perform multiple staking operations efficiently"""
    operations = [
        (1, 1000000000000000000),  # subnet_id, amount
        (2, 500000000000000000),
        (3, 750000000000000000),
    ]

    for subnet_id, amount in operations:
        response = client.add_to_delegate_stake(subnet_id, amount, keypair)
        if response.success:
            print(f"Staked {amount} to subnet {subnet_id}")
        else:
            print(f"Failed to stake to subnet {subnet_id}: {response.message}")
```

### Caching

```python
import functools

@functools.lru_cache(maxsize=128)
def get_cached_subnet_data(client, subnet_id):
    """Cache subnet data to reduce API calls"""
    return client.get_subnet_data(subnet_id)
```

## 🔧 Configuration Management

### Load Configuration

```python
from src.htcli.config import load_config

config = load_config()
print(f"Network endpoint: {config.network.endpoint}")
print(f"Default key: {config.wallet.default_key}")
```

### Custom Configuration

```python
from src.htcli.config import Config, NetworkConfig, WalletConfig

config = Config(
    network=NetworkConfig(
        endpoint="wss://testnet.hypertensor.ai",
        timeout=30
    ),
    wallet=WalletConfig(
        default_key="my-key",
        key_dir="/path/to/keys"
    )
)

client = HypertensorClient(config=config)
```
