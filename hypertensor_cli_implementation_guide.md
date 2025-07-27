# Hypertensor CLI Implementation Guide

## Complete Implementation Roadmap

This document provides a comprehensive guide for implementing the Hypertensor blockchain CLI application from scratch.

## Project Structure

```python
hypertensor-cli/
├── src/
│   ├── __init__.py
│   ├── main.py                    # Typer CLI entry point
│   ├── client.py                  # RPC client wrapper
│   ├── commands/                  # Command modules
│   │   ├── __init__.py
│   │   ├── subnet/               # Subnet operations
│   │   │   ├── __init__.py
│   │   │   ├── register.py       # Subnet registration
│   │   │   ├── manage.py         # Subnet management
│   │   │   ├── nodes.py          # Subnet node operations
│   │   │   ├── validation.py     # Validation & attestation
│   │   │   └── governance.py     # Subnet governance
│   │   ├── wallet/               # Wallet operations
│   │   │   ├── __init__.py
│   │   │   ├── keys.py           # Key management
│   │   │   ├── staking.py        # Staking operations
│   │   │   ├── rewards.py        # Rewards & incentives
│   │   │   ├── transfers.py      # Token transfers
│   │   │   └── atomic_swap.py    # Cross-chain swaps
│   │   └── chain/                # Chain commands
│   │       ├── __init__.py
│   │       ├── info.py           # Chain information
│   │       ├── query.py          # Data queries
│   │       ├── admin.py          # Administrative operations
│   │       └── network.py        # Network statistics
│   ├── utils/                    # Utility functions
│   │   ├── __init__.py
│   │   ├── crypto.py             # Cryptographic operations
│   │   ├── formatting.py         # Output formatting
│   │   ├── validation.py         # Input validation
│   │   └── config.py             # Configuration management
│   ├── models/                   # Pydantic models
│   │   ├── __init__.py
│   │   ├── requests.py           # Request models
│   │   ├── responses.py          # Response models
│   │   └── errors.py             # Error models
│   └── config.py                 # Configuration management
├── tests/                        # Test suite
├── requirements.txt               # Python dependencies
├── setup.py                      # Package setup
├── pyproject.toml               # Project configuration
├── config.yaml                  # Default configuration
└── README.md                    # Documentation
```

## Implementation Table

| Component | File | Status | Priority | Description |
|-----------|------|--------|----------|-------------|
| **Core Setup** | | | | |
| Project Structure | - | TODO | High | Create directory structure |
| Dependencies | requirements.txt | TODO | High | Define Python dependencies |
| Configuration | config.py | TODO | High | Configuration management |
| **Client Layer** | | | | |
| RPC Client | client.py | TODO | High | Blockchain connection wrapper |
| Connection Management | client.py | TODO | High | Handle WebSocket connections |
| Error Handling | client.py | TODO | High | Network and RPC error handling |
| **Models** | | | | |
| Request Models | models/requests.py | TODO | High | Pydantic models for requests |
| Response Models | models/responses.py | TODO | High | Pydantic models for responses |
| Error Models | models/errors.py | TODO | High | Error handling models |
| **Commands - Subnet** | | | | |
| Subnet Registration | commands/subnet/register.py | TODO | High | Subnet registration |
| Subnet Management | commands/subnet/manage.py | TODO | High | Subnet lifecycle management |
| Subnet Nodes | commands/subnet/nodes.py | TODO | High | Node operations |
| Subnet Validation | commands/subnet/validation.py | TODO | High | Validation & attestation |
| Subnet Governance | commands/subnet/governance.py | TODO | High | Governance operations |
| **Commands - Wallet** | | | | |
| Key Management | commands/wallet/keys.py | TODO | High | Wallet key operations |
| Staking Operations | commands/wallet/staking.py | TODO | High | Staking management |
| Rewards Management | commands/wallet/rewards.py | TODO | Medium | Rewards queries |
| Token Transfers | commands/wallet/transfers.py | TODO | Medium | Token transfer operations |
| Atomic Swaps | commands/wallet/atomic_swap.py | TODO | Medium | Cross-chain operations |
| **Commands - Chain** | | | | |
| Chain Information | commands/chain/info.py | TODO | High | Chain data queries |
| Data Queries | commands/chain/query.py | TODO | Medium | General data queries |
| Admin Operations | commands/chain/admin.py | TODO | Low | Administrative functions |
| Network Statistics | commands/chain/network.py | TODO | Medium | Network data |
| **Utilities** | | | | |
| Crypto Utils | utils/crypto.py | TODO | High | Cryptographic operations |
| Formatting Utils | utils/formatting.py | TODO | High | Output formatting |
| Validation Utils | utils/validation.py | TODO | High | Input validation |
| **Testing** | | | | |
| Unit Tests | tests/ | TODO | Medium | Test coverage |
| Integration Tests | tests/ | TODO | Medium | End-to-end testing |
| **Documentation** | | | | |
| README | README.md | TODO | Medium | User documentation |
| API Docs | docs/ | TODO | Low | API documentation |

## Command Structure by Category

### 1. Subnet Operations (`commands/subnet/`)

#### 1.1 Subnet Registration (`register.py`)

```python
import typer
from rich.console import Console
from typing import Optional
from ...models.requests import SubnetRegisterRequest
from ...client import HypertensorClient

app = typer.Typer(name="register", help="Subnet registration commands")
console = Console()

@app.command()
def create(
    path: str = typer.Argument(..., help="Subnet path"),
    memory_mb: int = typer.Option(..., "--memory", "-m", help="Memory requirement in MB"),
    registration_blocks: int = typer.Option(..., "--blocks", "-b", help="Registration period in blocks"),
    entry_interval: int = typer.Option(..., "--interval", "-i", help="Entry interval in blocks"),
    client: HypertensorClient = typer.Option(None, help="Client instance")
):
    """Register a new subnet."""
    request = SubnetRegisterRequest(
        path=path,
        memory_mb=memory_mb,
        registration_blocks=registration_blocks,
        entry_interval=entry_interval
    )

    try:
        response = client.register_subnet(request)
        console.print(f"✅ Subnet registered successfully!")
        console.print(f"Transaction: {response.transaction_hash}")
    except Exception as e:
        console.print(f"❌ Failed to register subnet: {str(e)}", style="red")

@app.command()
def activate(
    subnet_id: int = typer.Argument(..., help="Subnet ID to activate"),
    client: HypertensorClient = typer.Option(None, help="Client instance")
):
    """Activate a registered subnet."""
    try:
        response = client.activate_subnet(subnet_id)
        console.print(f"✅ Subnet {subnet_id} activated successfully!")
    except Exception as e:
        console.print(f"❌ Failed to activate subnet: {str(e)}", style="red")
```

#### 1.2 Subnet Management (`manage.py`)

```python
import typer
from rich.console import Console
from typing import Optional
from ...client import HypertensorClient

app = typer.Typer(name="manage", help="Subnet management commands")
console = Console()

@app.command()
def list(
    active_only: bool = typer.Option(False, "--active", "-a", help="Show only active subnets"),
    client: HypertensorClient = typer.Option(None, help="Client instance")
):
    """List all subnets."""
    try:
        response = client.list_subnets(active_only=active_only)

        if response.data["subnets"]:
            from rich.table import Table
            table = Table(title="Subnets")
            table.add_column("ID", style="cyan")
            table.add_column("Path", style="white")
            table.add_column("Status", style="green")
            table.add_column("Nodes", style="yellow")

            for subnet in response.data["subnets"]:
                status = "Active" if subnet.get("activated", 0) > 0 else "Inactive"
                table.add_row(
                    str(subnet.get("subnet_id", "N/A")),
                    subnet.get("path", "N/A"),
                    status,
                    str(subnet.get("node_count", 0))
                )

            console.print(table)
        else:
            console.print("No subnets found.")

    except Exception as e:
        console.print(f"❌ Failed to list subnets: {str(e)}", style="red")

@app.command()
def info(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    client: HypertensorClient = typer.Option(None, help="Client instance")
):
    """Get detailed subnet information."""
    try:
        response = client.get_subnet_info(subnet_id)

        if response.data:
            from rich.panel import Panel
            info_text = f"""
Subnet ID: {subnet_id}
Path: {response.data.get('path', 'N/A')}
Status: {'Active' if response.data.get('activated', 0) > 0 else 'Inactive'}
Registration Cost: {response.data.get('registration_cost', 'N/A')}
Node Count: {response.data.get('node_count', 0)}
            """
            console.print(Panel(info_text, title="Subnet Information"))
        else:
            console.print(f"Subnet {subnet_id} not found.")

    except Exception as e:
        console.print(f"❌ Failed to get subnet info: {str(e)}", style="red")
```

#### 1.3 Subnet Nodes (`nodes.py`)

```python
import typer
from rich.console import Console
from typing import Optional
from ...models.requests import SubnetNodeAddRequest
from ...client import HypertensorClient

app = typer.Typer(name="nodes", help="Subnet node operations")
console = Console()

@app.command()
def add(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    peer_id: str = typer.Argument(..., help="Peer ID"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey account"),
    client: HypertensorClient = typer.Option(None, help="Client instance")
):
    """Add a node to a subnet."""
    request = SubnetNodeAddRequest(
        subnet_id=subnet_id,
        peer_id=peer_id,
        hotkey=hotkey
    )

    try:
        response = client.add_subnet_node(request)
        console.print(f"✅ Node added to subnet {subnet_id} successfully!")
    except Exception as e:
        console.print(f"❌ Failed to add node: {str(e)}", style="red")

@app.command()
def list(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    client: HypertensorClient = typer.Option(None, help="Client instance")
):
    """List nodes in a subnet."""
    try:
        response = client.get_subnet_nodes(subnet_id)

        if response.data["nodes"]:
            from rich.table import Table
            table = Table(title=f"Nodes in Subnet {subnet_id}")
            table.add_column("Node ID", style="cyan")
            table.add_column("Peer ID", style="white")
            table.add_column("Hotkey", style="green")
            table.add_column("Stake", style="yellow")

            for node in response.data["nodes"]:
                table.add_row(
                    str(node.get("node_id", "N/A")),
                    node.get("peer_id", "N/A"),
                    node.get("hotkey", "N/A"),
                    str(node.get("stake", 0))
                )

            console.print(table)
        else:
            console.print(f"No nodes found in subnet {subnet_id}.")

    except Exception as e:
        console.print(f"❌ Failed to list nodes: {str(e)}", style="red")
```

### 2. Wallet Operations (`commands/wallet/`)

#### 2.1 Key Management (`keys.py`)

```python
import typer
from rich.console import Console
from typing import Optional
from ...utils.crypto import generate_keypair, import_keypair
from ...client import HypertensorClient

app = typer.Typer(name="keys", help="Wallet key management")
console = Console()

@app.command()
def generate(
    name: str = typer.Argument(..., help="Key name"),
    key_type: str = typer.Option("sr25519", "--type", "-t", help="Key type (sr25519/ed25519)"),
    password: Optional[str] = typer.Option(None, "--password", "-p", help="Key password")
):
    """Generate a new keypair."""
    try:
        keypair = generate_keypair(name, key_type, password)
        console.print(f"✅ Keypair '{name}' generated successfully!")
        console.print(f"Public Key: {keypair.public_key}")
        console.print(f"Address: {keypair.ss58_address}")
    except Exception as e:
        console.print(f"❌ Failed to generate keypair: {str(e)}", style="red")

@app.command()
def list():
    """List all available keys."""
    try:
        from ...utils.crypto import list_keys
        keys = list_keys()

        if keys:
            from rich.table import Table
            table = Table(title="Available Keys")
            table.add_column("Name", style="cyan")
            table.add_column("Type", style="white")
            table.add_column("Address", style="green")

            for key in keys:
                table.add_row(key.name, key.key_type, key.ss58_address)

            console.print(table)
        else:
            console.print("No keys found.")

    except Exception as e:
        console.print(f"❌ Failed to list keys: {str(e)}", style="red")

@app.command()
def import_key(
    name: str = typer.Argument(..., help="Key name"),
    private_key: str = typer.Option(..., "--private-key", "-k", help="Private key"),
    key_type: str = typer.Option("sr25519", "--type", "-t", help="Key type"),
    password: Optional[str] = typer.Option(None, "--password", "-p", help="Key password")
):
    """Import an existing keypair."""
    try:
        keypair = import_keypair(name, private_key, key_type, password)
        console.print(f"✅ Keypair '{name}' imported successfully!")
        console.print(f"Address: {keypair.ss58_address}")
    except Exception as e:
        console.print(f"❌ Failed to import keypair: {str(e)}", style="red")
```

#### 2.2 Staking Operations (`staking.py`)

```python
import typer
from rich.console import Console
from typing import Optional
from ...models.requests import StakeAddRequest, StakeRemoveRequest
from ...client import HypertensorClient

app = typer.Typer(name="staking", help="Staking operations")
console = Console()

@app.command()
def add(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    node_id: int = typer.Argument(..., help="Subnet node ID"),
    amount: str = typer.Argument(..., help="Stake amount"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey account"),
    client: HypertensorClient = typer.Option(None, help="Client instance")
):
    """Add stake to a subnet node."""
    # Convert amount to smallest unit
    amount_int = int(float(amount) * 1e9)  # Assuming 9 decimal places

    request = StakeAddRequest(
        subnet_id=subnet_id,
        subnet_node_id=node_id,
        hotkey=hotkey,
        stake_to_be_added=amount_int
    )

    try:
        response = client.add_stake(request)
        console.print(f"✅ Added {amount} stake to subnet {subnet_id} successfully!")
        console.print(f"Transaction: {response.transaction_hash}")
    except Exception as e:
        console.print(f"❌ Failed to add stake: {str(e)}", style="red")

@app.command()
def remove(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    amount: str = typer.Argument(..., help="Stake amount to remove"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey account"),
    client: HypertensorClient = typer.Option(None, help="Client instance")
):
    """Remove stake from a subnet."""
    amount_int = int(float(amount) * 1e9)

    request = StakeRemoveRequest(
        subnet_id=subnet_id,
        hotkey=hotkey,
        stake_to_be_removed=amount_int
    )

    try:
        response = client.remove_stake(request)
        console.print(f"✅ Removed {amount} stake from subnet {subnet_id} successfully!")
        console.print(f"Transaction: {response.transaction_hash}")
    except Exception as e:
        console.print(f"❌ Failed to remove stake: {str(e)}", style="red")

@app.command()
def info(
    subnet_id: int = typer.Argument(..., help="Subnet ID"),
    hotkey: str = typer.Option(..., "--hotkey", "-h", help="Hotkey account"),
    client: HypertensorClient = typer.Option(None, help="Client instance")
):
    """Get stake information."""
    try:
        response = client.get_stake_info(subnet_id, hotkey)

        if response.data:
            from rich.panel import Panel
            stake_amount = response.data.get("stake", 0) / 1e9  # Convert from smallest unit
            info_text = f"""
Subnet ID: {subnet_id}
Hotkey: {hotkey}
Stake Amount: {stake_amount} TAO
Unbonding: {response.data.get('unbonding', 0) / 1e9} TAO
            """
            console.print(Panel(info_text, title="Stake Information"))
        else:
            console.print(f"No stake found for hotkey {hotkey} in subnet {subnet_id}.")

    except Exception as e:
        console.print(f"❌ Failed to get stake info: {str(e)}", style="red")
```

### 3. Chain Commands (`commands/chain/`)

#### 3.1 Chain Information (`info.py`)

```python
import typer
from rich.console import Console
from typing import Optional
from ...client import HypertensorClient

app = typer.Typer(name="info", help="Chain information commands")
console = Console()

@app.command()
def network(
    client: HypertensorClient = typer.Option(None, help="Client instance")
):
    """Get network statistics."""
    try:
        response = client.get_network_stats()

        if response.data:
            from rich.panel import Panel
            stats = response.data
            info_text = f"""
Total Subnets: {stats.get('total_subnets', 0)}
Active Subnets: {stats.get('active_subnets', 0)}
Total Nodes: {stats.get('total_nodes', 0)}
Total Stake: {stats.get('total_stake', 0) / 1e9} TAO
Current Epoch: {stats.get('current_epoch', 0)}
            """
            console.print(Panel(info_text, title="Network Statistics"))
        else:
            console.print("No network statistics available.")

    except Exception as e:
        console.print(f"❌ Failed to get network stats: {str(e)}", style="red")

@app.command()
def account(
    address: str = typer.Argument(..., help="Account address"),
    client: HypertensorClient = typer.Option(None, help="Client instance")
):
    """Get account information."""
    try:
        response = client.get_account_info(address)

        if response.data:
            from rich.panel import Panel
            balance = response.data.get("balance", 0) / 1e9
            info_text = f"""
Address: {address}
Balance: {balance} TAO
Nonce: {response.data.get('nonce', 0)}
            """
            console.print(Panel(info_text, title="Account Information"))
        else:
            console.print(f"Account {address} not found.")

    except Exception as e:
        console.print(f"❌ Failed to get account info: {str(e)}", style="red")

@app.command()
def epoch(
    client: HypertensorClient = typer.Option(None, help="Client instance")
):
    """Get current epoch information."""
    try:
        response = client.get_current_epoch()

        if response.data:
            from rich.panel import Panel
            epoch_data = response.data
            info_text = f"""
Current Epoch: {epoch_data.get('epoch', 0)}
Epoch Start: {epoch_data.get('start_block', 0)}
Epoch End: {epoch_data.get('end_block', 0)}
Blocks Remaining: {epoch_data.get('blocks_remaining', 0)}
            """
            console.print(Panel(info_text, title="Epoch Information"))
        else:
            console.print("No epoch information available.")

    except Exception as e:
        console.print(f"❌ Failed to get epoch info: {str(e)}", style="red")
```

#### 3.2 Data Queries (`query.py`)

```python
import typer
from rich.console import Console
from typing import Optional
from ...client import HypertensorClient

app = typer.Typer(name="query", help="Data query commands")
console = Console()

@app.command()
def balance(
    address: str = typer.Argument(..., help="Account address"),
    client: HypertensorClient = typer.Option(None, help="Client instance")
):
    """Get account balance."""
    try:
        response = client.get_balance(address)

        if response.data:
            balance = response.data.get("balance", 0) / 1e9
            console.print(f"Balance: {balance} TAO")
        else:
            console.print(f"No balance found for {address}.")

    except Exception as e:
        console.print(f"❌ Failed to get balance: {str(e)}", style="red")

@app.command()
def peers(
    client: HypertensorClient = typer.Option(None, help="Client instance")
):
    """Get connected peers."""
    try:
        response = client.get_peers()

        if response.data and response.data.get("peers"):
            from rich.table import Table
            table = Table(title="Connected Peers")
            table.add_column("Peer ID", style="cyan")
            table.add_column("Address", style="white")
            table.add_column("Protocol", style="green")

            for peer in response.data["peers"]:
                table.add_row(
                    peer.get("peer_id", "N/A"),
                    peer.get("address", "N/A"),
                    peer.get("protocol", "N/A")
                )

            console.print(table)
        else:
            console.print("No peers connected.")

    except Exception as e:
        console.print(f"❌ Failed to get peers: {str(e)}", style="red")

@app.command()
def block(
    block_number: Optional[int] = typer.Argument(None, help="Block number (default: latest)"),
    client: HypertensorClient = typer.Option(None, help="Client instance")
):
    """Get block information."""
    try:
        response = client.get_block_info(block_number)

        if response.data:
            from rich.panel import Panel
            block_data = response.data
            info_text = f"""
Block Number: {block_data.get('number', 'N/A')}
Block Hash: {block_data.get('hash', 'N/A')}
Parent Hash: {block_data.get('parent_hash', 'N/A')}
Extrinsics: {len(block_data.get('extrinsics', []))}
            """
            console.print(Panel(info_text, title="Block Information"))
        else:
            console.print("Block not found.")

    except Exception as e:
        console.print(f"❌ Failed to get block info: {str(e)}", style="red")
```

## Main CLI Entry Point

```python
# src/main.py
import typer
from rich.console import Console
from pathlib import Path
from typing import Optional

from .commands.subnet import register, manage, nodes, validation, governance
from .commands.wallet import keys, staking, rewards, transfers, atomic_swap
from .commands.chain import info, query, admin, network
from .utils.config import load_config
from .client import HypertensorClient

app = typer.Typer(
    name="hypertensor",
    help="Hypertensor Blockchain CLI",
    add_completion=False,
    rich_markup_mode="rich"
)

console = Console()

# Global configuration and client
config = None
client = None

@app.callback()
def main(
    config_file: Optional[Path] = typer.Option(
        None, "--config", "-c", help="Configuration file path"
    ),
    endpoint: Optional[str] = typer.Option(
        None, "--endpoint", "-e", help="Blockchain endpoint"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    output_format: str = typer.Option("table", "--format", "-f", help="Output format (table/json/csv)")
):
    """Hypertensor Blockchain CLI - Manage subnets, wallets, and chain operations."""
    global config, client

    # Load configuration
    config = load_config(config_file)

    # Override endpoint if provided
    if endpoint:
        config.network.endpoint = endpoint

    # Initialize client
    client = HypertensorClient(config)

    # Set global options
    config.output.verbose = verbose
    config.output.format = output_format

# Include subnet command modules
app.add_typer(register.app, name="register", help="Subnet registration")
app.add_typer(manage.app, name="manage", help="Subnet management")
app.add_typer(nodes.app, name="nodes", help="Subnet node operations")
app.add_typer(validation.app, name="validate", help="Validation operations")
app.add_typer(governance.app, name="governance", help="Governance operations")

# Include wallet command modules
app.add_typer(keys.app, name="keys", help="Key management")
app.add_typer(staking.app, name="stake", help="Staking operations")
app.add_typer(rewards.app, name="rewards", help="Rewards management")
app.add_typer(transfers.app, name="transfer", help="Token transfers")
app.add_typer(atomic_swap.app, name="swap", help="Atomic swap operations")

# Include chain command modules
app.add_typer(info.app, name="info", help="Chain information")
app.add_typer(query.app, name="query", help="Data queries")
app.add_typer(admin.app, name="admin", help="Administrative operations")
app.add_typer(network.app, name="network", help="Network operations")

if __name__ == "__main__":
    app()
```

## Usage Examples

```bash
# Subnet operations
hypertensor register create my-subnet --memory 1024 --blocks 1000 --interval 100
hypertensor manage list --active
hypertensor nodes add 1 QmPeerId --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
hypertensor validate submit 1 --data "validation_data"

# Wallet operations
hypertensor keys generate my-wallet --type sr25519
hypertensor stake add 1 1 100.0 --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
hypertensor transfer 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY 50.0

# Chain commands
hypertensor info network
hypertensor query balance 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
hypertensor info epoch
```

This reorganized structure provides a clear separation of concerns with three main categories:

1. **Subnet Operations**: All subnet-related functionality
2. **Wallet Operations**: All wallet and key management functionality
3. **Chain Commands**: All chain information and query functionality

Each category has its own subdirectory with specific command modules, making the codebase more organized and maintainable.
