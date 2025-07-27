# Hypertensor CLI (htcli)

A command-line interface for interacting with the Hypertensor blockchain network.

## Features

- **Subnet Management**: Register, activate, and manage subnets
- **Wallet Operations**: Generate keys, manage wallets, and perform staking operations
- **Chain Information**: Query network statistics, account information, and blockchain data
- **Rich Output**: Beautiful tables and formatted output using Rich

## Installation

```bash
# Install the package
pip install -e .

# Or using uv
uv sync
```

## Usage

### Basic Commands

```bash
# Get help
htcli --help

# List all subnets
htcli manage list

# Get network statistics
htcli info network

# Generate a new keypair
htcli keys generate my-wallet
```

### Subnet Operations

```bash
# Register a new subnet
htcli register create my-subnet --memory 1024 --blocks 1000 --interval 100

# Activate a subnet
htcli register activate 1

# List subnets
htcli manage list --active

# Get subnet information
htcli manage info 1

# Add a node to a subnet
htcli nodes add 1 QmPeerId --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY

# List nodes in a subnet
htcli nodes list 1
```

### Wallet Operations

```bash
# Generate a new keypair
htcli keys generate my-wallet --type sr25519

# List all keys
htcli keys list

# Import an existing keypair
htcli keys import-key my-wallet --private-key 0x1234... --type sr25519

# Delete a keypair
htcli keys delete my-wallet
```

### Staking Operations

```bash
# Add stake to a subnet node
htcli stake add 1 1 100.0 --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY

# Remove stake from a subnet
htcli stake remove 1 50.0 --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY

# Get stake information
htcli stake info 1 --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
```

### Chain Information

```bash
# Get network statistics
htcli info network

# Get account information
htcli info account 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY

# Get current epoch information
htcli info epoch

# Query account balance
htcli query balance 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY

# Get connected peers
htcli query peers

# Get block information
htcli query block --number 12345
```

## Project Structure

```
src/htcli/
├── __init__.py
├── main.py                    # CLI entry point
├── client.py                  # RPC client wrapper
├── config.py                  # Configuration management
├── dependencies.py            # Dependency injection
├── commands/                  # Command modules
│   ├── subnet/               # Subnet operations
│   │   ├── register.py       # Subnet registration
│   │   ├── manage.py         # Subnet management
│   │   └── nodes.py          # Subnet node operations
│   ├── wallet/               # Wallet operations
│   │   ├── keys.py           # Key management
│   │   └── staking.py        # Staking operations
│   └── chain/                # Chain commands
│       ├── info.py           # Chain information
│       └── query.py          # Data queries
├── models/                   # Pydantic models
│   ├── requests.py           # Request models
│   ├── responses.py          # Response models
│   └── errors.py             # Error models
└── utils/                    # Utility functions
    ├── crypto.py             # Cryptographic operations
    ├── formatting.py         # Output formatting
    ├── validation.py         # Input validation
    ├── blockchain.py         # Blockchain utilities
    ├── helpers.py            # Helper functions
    └── wallet.py             # Wallet utilities
```

## Configuration

The CLI supports configuration through:

1. **Command line options**: Use `--endpoint`, `--config`, etc.
2. **Configuration file**: Create a YAML configuration file
3. **Environment variables**: Set environment variables for defaults

### Example Configuration

```yaml
network:
  endpoint: "ws://127.0.0.1:9944"
  ws_endpoint: "ws://127.0.0.1:9944"
  timeout: 30
  retry_attempts: 3

output:
  format: "table"
  verbose: false
  color: true

wallet:
  path: "~/.htcli/wallets"
  default_name: "default"
  encryption_enabled: true
```

## Development

### Setup Development Environment

```bash
# Install dependencies
uv sync

# Install in development mode
pip install -e .

# Run tests
pytest
```

### Adding New Commands

1. Create a new command module in the appropriate directory
2. Import the command in `main.py`
3. Add the command to the CLI using `app.add_typer()`

### Example Command Structure

```python
import typer
from rich.console import Console
from ...dependencies import get_client

app = typer.Typer(name="example", help="Example commands")
console = Console()

@app.command()
def example_command(
    param: str = typer.Argument(..., help="Parameter description"),
    client = typer.Option(None, help="Client instance")
):
    """Example command description."""
    # Get client if not provided
    if client is None:
        client = get_client()

    # Command implementation
    pass
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
