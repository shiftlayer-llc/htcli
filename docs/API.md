# Hypertensor CLI API Reference

This document provides comprehensive API reference for integrating with the Hypertensor CLI programmatically and understanding the underlying client architecture.

## 📋 **Table of Contents**

1. [API Overview](#api-overview)
2. [Client Architecture](#client-architecture)
3. [Configuration API](#configuration-api)
4. [Subnet Client API](#subnet-client-api)
5. [Node Client API](#node-client-api)
6. [Staking Client API](#staking-client-api)
7. [Wallet Client API](#wallet-client-api)
8. [Chain Client API](#chain-client-api)
9. [Models and Data Structures](#models-and-data-structures)
10. [Error Handling](#error-handling)
11. [Integration Examples](#integration-examples)

## 🎯 **API Overview**

The Hypertensor CLI provides both command-line interface and programmatic API access through its modular client architecture. The API is built on top of the SubstrateInterface library for blockchain interactions.

### **Key Features**

- **Modular Design**: Separate clients for different functionalities
- **Type Safety**: Pydantic models for request/response validation
- **Real Blockchain Integration**: Direct interaction with Hypertensor network
- **Comprehensive Error Handling**: Detailed error messages and recovery guidance
- **18-Digit Precision**: Full TENSOR token precision support
- **🆕 Personal Asset Filtering**: Universal ownership-based filtering across all operations

### **Architecture Overview**

```
HypertensorClient (Base)
├── SubnetClient (Subnet operations)
├── NodeClient (Node management)
├── StakingClient (Staking operations)
├── WalletClient (Key management)
└── ChainClient (Blockchain queries)
```

## 🏗️ **Client Architecture**

### **Base Client**

The `HypertensorClient` provides the foundation for all blockchain interactions:

```python
from src.htcli.client import HypertensorClient

# Initialize client with configuration
client = HypertensorClient(
    endpoint="wss://hypertensor.duckdns.org",
    timeout=30,
    retry_attempts=3
)

# Access specialized clients
subnet_client = client.subnet
node_client = client.node
staking_client = client.staking
wallet_client = client.wallet
chain_client = client.chain
```

### **Client Initialization**

```python
# Basic initialization
client = HypertensorClient()

# Custom endpoint
client = HypertensorClient(endpoint="wss://custom.endpoint.com")

# Full configuration
client = HypertensorClient(
    endpoint="wss://hypertensor.duckdns.org",
    ws_endpoint="wss://hypertensor.duckdns.org",
    timeout=60,
    retry_attempts=5
)
```

### **Connection Management**

```python
# Check connection status
if client.is_connected():
    print("Connected to blockchain")

# Reconnect if needed
client.reconnect()

# Close connection
client.close()
```

## ⚙️ **Configuration API**

### **Configuration Loading**

```python
from src.htcli.config import load_config, Config

# Load default configuration
config = load_config()

# Load custom configuration
config = load_config("/path/to/custom/config.yaml")

# Access configuration sections
network_config = config.network
output_config = config.output
wallet_config = config.wallet
```

### **Configuration Models**

```python
from src.htcli.config import NetworkConfig, OutputConfig, WalletConfig

# Network configuration
network = NetworkConfig(
    endpoint="wss://hypertensor.duckdns.org",
    ws_endpoint="wss://hypertensor.duckdns.org",
    timeout=30,
    retry_attempts=3
)

# Output configuration
output = OutputConfig(
    format="json",
    verbose=True,
    color=False
)

# Wallet configuration
wallet = WalletConfig(
    path="~/.htcli/wallets",
    default_name="api-client",
    encryption_enabled=True
)
```

## 🏗️ **Subnet Client API**

### **Subnet Registration**

```python
from src.htcli.models.requests import SubnetRegisterRequest

# Create subnet registration request
request = SubnetRegisterRequest(
    path="ai-compute",
    memory_mb=4096,
    registration_blocks=1000,
    entry_interval=100,
    max_node_registration_epochs=200,
    node_registration_interval=50,
    node_activation_interval=50,
    node_queue_period=100,
    max_penalties=10,
    coldkey_whitelist=[]
)

# Submit registration
response = client.subnet.register_subnet(request, keypair=None)

if response.success:
    print(f"Subnet registered: {response.transaction_hash}")
    print(f"Block: {response.block_number}")
else:
    print(f"Registration failed: {response.message}")
```

### **Subnet Management**

```python
# Activate subnet
response = client.subnet.activate_subnet(subnet_id=1, keypair=None)

# Remove subnet
response = client.subnet.remove_subnet(subnet_id=1, keypair=None)

# Get subnet data
response = client.subnet.get_subnet_data(subnet_id=1)
if response.success:
    subnet_data = response.data
    print(f"Subnet path: {subnet_data['path']}")
    print(f"Active nodes: {subnet_data['node_count']}")

# Get all subnets
response = client.subnet.get_subnets_data()
if response.success:
    subnets = response.data
    for subnet in subnets:
        print(f"Subnet {subnet['id']}: {subnet['path']}")
```

### **Subnet Queries**

```python
# Get subnet nodes
response = client.subnet.get_subnet_nodes(subnet_id=1)
if response.success:
    nodes = response.data
    for node in nodes:
        print(f"Node {node['id']}: {node['hotkey']}")

# Check subnet capacity
response = client.subnet.get_subnet_data(subnet_id=1)
if response.success:
    data = response.data
    capacity = data.get('max_nodes', 0)
    current = data.get('node_count', 0)
    available = capacity - current
    print(f"Capacity: {current}/{capacity} ({available} available)")
```

## 🔗 **Node Client API**

### **Node Management**

```python
from src.htcli.models.requests import SubnetNodeAddRequest

# Add node to subnet
request = SubnetNodeAddRequest(
    subnet_id=1,
    hotkey="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
    peer_id="QmYwAPJzv5CZsnA625s3ofHtUyJ9eykQZ6d3s5hgcEAuSo",
    stake_to_be_added=5000000000000000000,
    delegate_reward_rate=0.10,
    a="1",
    b="1",
    c="1"
)

response = client.node.add_subnet_node(request, keypair=None)

if response.success:
    print(f"Node added: {response.transaction_hash}")
else:
    print(f"Failed to add node: {response.message}")
```

### **Node Lifecycle Operations**

```python
from src.htcli.models.requests import NodeRemoveRequest, NodeDeactivateRequest

# Remove node permanently
remove_request = NodeRemoveRequest(
    subnet_id=1,
    node_id=2
)
response = client.node.remove_subnet_node(remove_request, keypair=None)

# Deactivate node temporarily
deactivate_request = NodeDeactivateRequest(
    subnet_id=1,
    node_id=2
)
response = client.node.deactivate_subnet_node(deactivate_request, keypair=None)
```

### **Node Queries**

```python
# Get node status
response = client.node.get_node_status(subnet_id=1, node_id=2)
if response.success:
    status = response.data
    print(f"Status: {status['state']}")
    print(f"Performance: {status['performance_score']}")
    print(f"Stake: {status['total_stake']} wei")

# List all nodes in subnet
response = client.node.get_subnet_nodes(subnet_id=1)
if response.success:
    nodes = response.data
    for node in nodes:
        print(f"Node {node['id']}: {node['hotkey']} ({node['status']})")
```

## 💰 **Staking Client API**

### **Direct Staking Operations**

```python
from src.htcli.models.requests import StakeAddRequest, StakeRemoveRequest

# Add stake to node
add_request = StakeAddRequest(
    subnet_id=1,
    node_id=2,
    hotkey="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
    stake_to_be_added=2000000000000000000
)

response = client.staking.add_to_stake(add_request, keypair=None)

# Remove stake from node
remove_request = StakeRemoveRequest(
    subnet_id=1,
    hotkey="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
    stake_to_be_removed=1000000000000000000
)

response = client.staking.remove_stake(remove_request, keypair=None)
```

### **Delegate Staking Operations**

```python
# Add delegate stake
response = client.staking.add_to_delegate_stake(
    subnet_id=1,
    amount=3000000000000000000,
    keypair=None
)

# Remove delegate stake
response = client.staking.remove_delegate_stake(
    subnet_id=1,
    shares=1500,
    keypair=None
)

# Transfer delegate stake between subnets
response = client.staking.transfer_delegate_stake(
    from_subnet=1,
    to_subnet=2,
    shares=1000,
    keypair=None
)
```

### **Staking Queries**

```python
# Get account stake information
response = client.staking.get_account_subnet_stake(
    address="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
    subnet_id=1
)

if response.success:
    stake_info = response.data
    print(f"Total Stake: {stake_info['total_stake']} wei")
    print(f"Earned Rewards: {stake_info['rewards']} wei")
    print(f"Unbonding: {stake_info['unbonding']} wei")

# Claim unbonded tokens
response = client.staking.claim_unbondings(keypair=None)
```

## 🔑 **Wallet Client API**

### **Key Generation and Import**

```python
from src.htcli.utils.crypto import generate_keypair, import_keypair

# Generate new keypair
keypair_data = generate_keypair(
    name="api-key",
    key_type="sr25519",
    password="secure_password"
)

print(f"Address: {keypair_data['address']}")
print(f"Public Key: {keypair_data['public_key']}")

# Import existing keypair
imported_keypair = import_keypair(
    name="imported-key",
    private_key="0x1234567890abcdef...",
    key_type="sr25519",
    password="secure_password"
)
```

### **Key Management**

```python
from src.htcli.utils.crypto import list_keys, delete_keypair

# List all stored keys
keys = list_keys()
for key in keys:
    print(f"Name: {key['name']}")
    print(f"Type: {key['type']}")
    print(f"Address: {key['address']}")

# Delete a key
success = delete_keypair("old-key")
if success:
    print("Key deleted successfully")
```

### **Key Loading for Transactions**

```python
from src.htcli.utils.crypto import load_keypair

# Load keypair for transaction signing
keypair = load_keypair("my-key", password="secure_password")

# Use keypair in transactions
response = client.subnet.register_subnet(request, keypair=keypair)
```

## 🔍 **Chain Client API**

### **Network Information**

```python
# Get network statistics
response = client.chain.get_network_stats()
if response.success:
    stats = response.data
    print(f"Total Subnets: {stats['total_subnets']}")
    print(f"Active Subnets: {stats['active_subnets']}")
    print(f"Total Nodes: {stats['total_nodes']}")
    print(f"Total Stake: {stats['total_stake']} wei")

# Get current epoch
response = client.chain.get_current_epoch()
if response.success:
    epoch = response.data
    print(f"Current Epoch: {epoch['number']}")
    print(f"Epoch Start: {epoch['start_time']}")
```

### **Account Information**

```python
# Get account balance
response = client.chain.get_balance(
    "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
)

if response.success:
    balance = response.data
    print(f"Free Balance: {balance['free']} wei")
    print(f"Reserved Balance: {balance['reserved']} wei")
    print(f"Total Balance: {balance['total']} wei")

# Get detailed account information
response = client.chain.get_account_info(
    "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
)

if response.success:
    account = response.data
    print(f"Nonce: {account['nonce']}")
    print(f"Consumers: {account['consumers']}")
    print(f"Providers: {account['providers']}")
```

### **Block and Chain Information**

```python
# Get block information
response = client.chain.get_block_info(block_number=12345)
if response.success:
    block = response.data
    print(f"Block Hash: {block['hash']}")
    print(f"Parent Hash: {block['parent_hash']}")
    print(f"Timestamp: {block['timestamp']}")

# Get chain head
response = client.chain.get_chain_head()
if response.success:
    head = response.data
    print(f"Best Block: {head['best_number']}")
    print(f"Best Hash: {head['best_hash']}")

# Get runtime version
response = client.chain.get_runtime_version()
if response.success:
    runtime = response.data
    print(f"Spec Name: {runtime['spec_name']}")
    print(f"Spec Version: {runtime['spec_version']}")
```

## 📊 **Models and Data Structures**

### **Request Models**

```python
from src.htcli.models.requests import (
    SubnetRegisterRequest,
    SubnetNodeAddRequest,
    StakeAddRequest,
    StakeRemoveRequest,
    NodeRemoveRequest,
    NodeDeactivateRequest
)

# All request models use Pydantic for validation
request = SubnetRegisterRequest(
    path="my-subnet",
    memory_mb=2048,
    registration_blocks=1000,
    entry_interval=100
    # ... other fields with validation
)
```

### **Response Models**

```python
from src.htcli.models.responses import (
    TransactionResponse,
    QueryResponse
)

# Transaction responses include success status and details
class TransactionResponse:
    success: bool
    message: str
    transaction_hash: Optional[str] = None
    block_number: Optional[int] = None

# Query responses include success status and data
class QueryResponse:
    success: bool
    message: str
    data: Optional[Dict] = None
```

### **Configuration Models**

```python
from src.htcli.config import Config, NetworkConfig, OutputConfig, WalletConfig

# Main configuration structure
class Config:
    network: NetworkConfig
    output: OutputConfig
    wallet: WalletConfig

# Network configuration
class NetworkConfig:
    endpoint: str = "wss://hypertensor.duckdns.org"
    ws_endpoint: str = "wss://hypertensor.duckdns.org"
    timeout: int = 30
    retry_attempts: int = 3

# Output configuration
class OutputConfig:
    format: str = "table"
    verbose: bool = False
    color: bool = True

# Wallet configuration
class WalletConfig:
    path: str = "~/.htcli/wallets"
    default_name: str = "default"
    encryption_enabled: bool = True
```

## 🚨 **Error Handling**

### **Exception Types**

```python
from src.htcli.exceptions import (
    HypertensorClientError,
    NetworkConnectionError,
    TransactionError,
    ValidationError
)

try:
    response = client.subnet.register_subnet(request, keypair)
except NetworkConnectionError as e:
    print(f"Network error: {e}")
    # Handle network connectivity issues
except TransactionError as e:
    print(f"Transaction error: {e}")
    # Handle blockchain transaction errors
except ValidationError as e:
    print(f"Validation error: {e}")
    # Handle input validation errors
except HypertensorClientError as e:
    print(f"Client error: {e}")
    # Handle general client errors
```

### **Response Error Handling**

```python
# All operations return response objects with success indicators
response = client.subnet.register_subnet(request, keypair)

if response.success:
    print(f"Success: {response.transaction_hash}")
else:
    print(f"Error: {response.message}")
    # Handle specific error cases
    if "insufficient balance" in response.message.lower():
        print("Need to add more tokens to account")
    elif "subnet already exists" in response.message.lower():
        print("Choose a different subnet name")
```

### **Retry Logic**

```python
import time
from typing import Callable, Any

def retry_operation(operation: Callable, max_retries: int = 3, delay: float = 1.0) -> Any:
    """Retry an operation with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return operation()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(delay * (2 ** attempt))

# Usage
def register_subnet():
    return client.subnet.register_subnet(request, keypair)

response = retry_operation(register_subnet, max_retries=3)
```

## 🎯 **Personal Asset Filtering API**

The CLI includes powerful utilities for filtering blockchain data to show only user-owned assets. These utilities are used internally by the `--mine` flag but can also be used programmatically.

### **Ownership Utilities**

```python
from src.htcli.utils.ownership import (
    get_user_addresses,
    user_owns_subnet,
    require_user_keys,
    show_mine_filter_info
)

# Get all user addresses from wallet keys
user_addresses = get_user_addresses()
print(f"Found {len(user_addresses)} wallet addresses")

# Check if user owns a specific subnet
subnet_data = client.subnet.get_subnet_data(subnet_id=1)
if subnet_data.success:
    is_owner = user_owns_subnet(subnet_data.data, user_addresses)
    print(f"User owns subnet 1: {is_owner}")

# Require user keys (raises error if none found)
try:
    addresses = require_user_keys()
    print(f"User has {len(addresses)} addresses available")
except Exception as e:
    print(f"No wallet keys found: {e}")
```

### **Filtering Examples**

#### **Filter Subnets by Ownership**
```python
def get_user_subnets(client):
    """Get only subnets owned by the user"""
    user_addresses = get_user_addresses()
    if not user_addresses:
        return []

    # Get all subnets
    response = client.subnet.get_subnets_data()
    if not response.success:
        return []

    user_subnets = []
    for subnet in response.data.get('subnets', []):
        subnet_id = subnet.get('subnet_id')
        if subnet_id:
            # Get detailed subnet info
            detail_response = client.subnet.get_subnet_data(subnet_id)
            if detail_response.success:
                if user_owns_subnet(detail_response.data, user_addresses):
                    user_subnets.append(subnet)

    return user_subnets

# Usage
user_subnets = get_user_subnets(client)
print(f"User owns {len(user_subnets)} subnets")
```

#### **Filter Stakes by Address**
```python
def get_user_stakes(client):
    """Get stakes for all user addresses"""
    user_addresses = get_user_addresses()
    if not user_addresses:
        return []

    all_stakes = []
    for key_name, address in user_addresses:
        # Get stakes for this address
        response = client.staking.get_stake_info(address)
        if response.success:
            stakes = response.data.get('stakes', [])
            for stake in stakes:
                stake['key_name'] = key_name
                stake['address'] = address
                all_stakes.append(stake)

    return all_stakes

# Usage
user_stakes = get_user_stakes(client)
print(f"User has {len(user_stakes)} stake positions")
```

### **Configuration Integration**

The personal asset filtering respects the configuration settings:

```python
from src.htcli.config import load_config

# Load configuration
config = load_config()

# Check if --mine filtering is enabled by default
filter_mine = getattr(config.filter, 'mine', False)
if filter_mine:
    print("Personal filtering enabled by default")
else:
    print("Network-wide view by default")

# Override in client usage
client = HypertensorClient(config)
client.config.filter.mine = True  # Enable personal filtering
```

## 🔧 **Integration Examples**

### **Basic CLI Integration**

```python
#!/usr/bin/env python3
"""
Basic integration example showing how to use the Hypertensor CLI API
"""

from src.htcli.client import HypertensorClient
from src.htcli.config import load_config
from src.htcli.models.requests import SubnetRegisterRequest

def main():
    # Load configuration
    config = load_config()

    # Initialize client
    client = HypertensorClient(
        endpoint=config.network.endpoint,
        timeout=config.network.timeout
    )

    # Check network connection
    response = client.chain.get_network_stats()
    if not response.success:
        print(f"Failed to connect to network: {response.message}")
        return

    print("Connected to Hypertensor network")
    print(f"Total subnets: {response.data['total_subnets']}")

    # Register a subnet
    request = SubnetRegisterRequest(
        path="api-test-subnet",
        memory_mb=1024,
        registration_blocks=1000,
        entry_interval=100
    )

    response = client.subnet.register_subnet(request, keypair=None)
    if response.success:
        print(f"Subnet registered: {response.transaction_hash}")
    else:
        print(f"Registration failed: {response.message}")

if __name__ == "__main__":
    main()
```

### **Monitoring Script**

```python
#!/usr/bin/env python3
"""
Network monitoring script using the Hypertensor CLI API
"""

import time
import json
from datetime import datetime
from src.htcli.client import HypertensorClient

class NetworkMonitor:
    def __init__(self, endpoint: str):
        self.client = HypertensorClient(endpoint=endpoint)
        self.log_file = "network_monitor.log"

    def log_event(self, event_type: str, data: dict):
        """Log monitoring events"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "data": data
        }

        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def check_network_health(self) -> dict:
        """Check overall network health"""
        response = self.client.chain.get_network_stats()
        if response.success:
            return response.data
        return {}

    def check_subnet_status(self, subnet_id: int) -> dict:
        """Check specific subnet status"""
        response = self.client.subnet.get_subnet_data(subnet_id)
        if response.success:
            return response.data
        return {}

    def monitor_loop(self, interval: int = 60):
        """Main monitoring loop"""
        print(f"Starting network monitor (interval: {interval}s)")

        while True:
            try:
                # Check network health
                network_stats = self.check_network_health()
                if network_stats:
                    self.log_event("network_stats", network_stats)
                    print(f"Network: {network_stats['total_subnets']} subnets, "
                          f"{network_stats['total_nodes']} nodes")

                # Check specific subnets
                for subnet_id in [1, 2, 3]:  # Monitor first 3 subnets
                    subnet_stats = self.check_subnet_status(subnet_id)
                    if subnet_stats:
                        self.log_event("subnet_stats", {
                            "subnet_id": subnet_id,
                            **subnet_stats
                        })

                time.sleep(interval)

            except KeyboardInterrupt:
                print("Monitoring stopped")
                break
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(interval)

if __name__ == "__main__":
    monitor = NetworkMonitor("wss://hypertensor.duckdns.org")
    monitor.monitor_loop(interval=30)
```

### **Automated Staking Bot**

```python
#!/usr/bin/env python3
"""
Automated staking bot using the Hypertensor CLI API
"""

from src.htcli.client import HypertensorClient
from src.htcli.models.requests import StakeAddRequest, StakeRemoveRequest
from src.htcli.utils.crypto import load_keypair

class StakingBot:
    def __init__(self, endpoint: str, key_name: str, password: str):
        self.client = HypertensorClient(endpoint=endpoint)
        self.keypair = load_keypair(key_name, password)
        self.address = self.keypair.ss58_address

    def get_balance(self) -> int:
        """Get current account balance"""
        response = self.client.chain.get_balance(self.address)
        if response.success:
            return int(response.data['free'])
        return 0

    def get_stake_positions(self) -> dict:
        """Get current stake positions"""
        positions = {}
        for subnet_id in range(1, 10):  # Check first 10 subnets
            response = self.client.staking.get_account_subnet_stake(
                self.address, subnet_id
            )
            if response.success and response.data['total_stake'] > 0:
                positions[subnet_id] = response.data
        return positions

    def analyze_performance(self, subnet_id: int) -> float:
        """Analyze subnet performance for staking decisions"""
        response = self.client.subnet.get_subnet_nodes(subnet_id)
        if not response.success:
            return 0.0

        nodes = response.data
        if not nodes:
            return 0.0

        # Calculate average performance score
        total_performance = sum(
            node.get('performance_score', 0) for node in nodes
        )
        return total_performance / len(nodes)

    def rebalance_stakes(self):
        """Rebalance stake positions based on performance"""
        print("Starting stake rebalancing...")

        # Get current positions
        positions = self.get_stake_positions()
        print(f"Current positions: {len(positions)} subnets")

        # Analyze performance of each subnet
        performance_scores = {}
        for subnet_id in range(1, 6):  # Analyze first 5 subnets
            score = self.analyze_performance(subnet_id)
            if score > 0:
                performance_scores[subnet_id] = score

        # Sort by performance
        sorted_subnets = sorted(
            performance_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        print("Subnet performance scores:")
        for subnet_id, score in sorted_subnets:
            print(f"  Subnet {subnet_id}: {score:.3f}")

        # Rebalancing logic
        target_stake_per_subnet = 1000000000000000000  # 1 TENSOR

        for subnet_id, score in sorted_subnets[:3]:  # Top 3 subnets
            current_stake = positions.get(subnet_id, {}).get('total_stake', 0)

            if current_stake < target_stake_per_subnet:
                # Add stake to high-performing subnet
                amount_to_add = target_stake_per_subnet - current_stake
                self.add_stake(subnet_id, amount_to_add)

        # Remove stake from low-performing subnets
        for subnet_id in positions:
            if subnet_id not in [s[0] for s in sorted_subnets[:3]]:
                self.remove_stake(subnet_id, positions[subnet_id]['total_stake'])

    def add_stake(self, subnet_id: int, amount: int):
        """Add stake to a subnet"""
        # Find best node in subnet
        response = self.client.subnet.get_subnet_nodes(subnet_id)
        if not response.success or not response.data:
            return

        # Select highest performing node
        best_node = max(
            response.data,
            key=lambda n: n.get('performance_score', 0)
        )

        request = StakeAddRequest(
            subnet_id=subnet_id,
            node_id=best_node['id'],
            hotkey=self.address,
            stake_to_be_added=amount
        )

        response = self.client.staking.add_to_stake(request, self.keypair)
        if response.success:
            print(f"Added {amount} wei stake to subnet {subnet_id}, node {best_node['id']}")
        else:
            print(f"Failed to add stake: {response.message}")

    def remove_stake(self, subnet_id: int, amount: int):
        """Remove stake from a subnet"""
        request = StakeRemoveRequest(
            subnet_id=subnet_id,
            hotkey=self.address,
            stake_to_be_removed=amount
        )

        response = self.client.staking.remove_stake(request, self.keypair)
        if response.success:
            print(f"Removed {amount} wei stake from subnet {subnet_id}")
        else:
            print(f"Failed to remove stake: {response.message}")

if __name__ == "__main__":
    bot = StakingBot(
        endpoint="wss://hypertensor.duckdns.org",
        key_name="staking-bot",
        password="secure_password"
    )

    bot.rebalance_stakes()
```

This comprehensive API reference provides all the information needed to integrate with the Hypertensor CLI programmatically, from basic client usage to advanced automation scripts.
