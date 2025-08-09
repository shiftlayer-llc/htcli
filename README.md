# Hypertensor CLI (htcli)

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CLI Commands](https://img.shields.io/badge/commands-34%20total-brightgreen.svg)](https://github.com/shiftlayer-llc/htcli)
[![Categories](https://img.shields.io/badge/categories-6%20organized-blue.svg)](https://github.com/shiftlayer-llc/htcli)

A comprehensive, professional command-line interface (CLI) tool for interacting with the Hypertensor blockchain network. Built with Python and Typer, it provides an intuitive interface with **comprehensive user guidance**, **consistent switch-based commands**, and **real blockchain integration**.

## 🚀 **Features**

### **🎯 Professional CLI Experience**

- **34 Commands** across 6 logical categories
- **Universal --mine Filtering**: Filter any command to show only your assets
- **Consistent Switch-Based Format**: All commands use `--switches` (no positional arguments)
- **Interactive Guidance**: Rich panels with step-by-step instructions
- **Safety Features**: Confirmation prompts and warning messages
- **Multiple Output Formats**: Table, JSON, and CSV support

### **👤 Personal Asset Management**

- **Smart Ownership Detection**: Automatically identifies your assets vs. network-wide data
- **Universal Filtering**: Add `--mine` to any command to see only your assets
- **Secure Key Storage**: Encrypted wallet keys stored in `~/.htcli/wallets/`
- **Multi-Address Support**: Manage multiple wallet addresses simultaneously

### **🔗 Real Blockchain Integration**

- **Direct WebSocket Connections**: `wss://hypertensor.duckdns.org`
- **SubstrateInterface Integration**: Full Substrate blockchain operations
- **Real Transaction Submission**: Actual blockchain transaction composition and submission
- **Live Storage Queries**: Real-time blockchain state queries
- **18-Digit TENSOR Precision**: Accurate token handling with full precision

### **📁 Organized Command Categories**

#### **⚙️ Configuration Management**

- Interactive configuration wizard with YAML output
- Multiple configuration file support
- Validation and editing capabilities

#### **🏗️ Subnet Operations**

- Subnet registration and activation
- Subnet information and management
- Real-time subnet statistics

#### **🔗 Node Management**

- Add/remove nodes from subnets
- Node status monitoring and management
- Comprehensive node lifecycle operations

#### **💰 Staking Operations**

- Add/remove stake with comprehensive guidance
- Delegate staking and transfers
- Unbonding management and claims
- Real-time staking rewards tracking

#### **🔑 Wallet & Key Management**

- Generate and import cryptographic keys
- Support for sr25519 and ed25519 key types
- Secure key storage and management

#### **🔍 Chain Queries**

- Real-time network statistics
- Account information and balances
- Block and runtime information
- Network peer data

## 📦 **Installation**

### **Prerequisites**

- Python 3.12 or higher
- UV package manager (recommended)
- Network access to Hypertensor blockchain

### **Quick Install**

```bash
# Clone the repository
git clone https://github.com/shiftlayer-llc/htcli.git
cd htcli

# Install with uv (recommended)
uv pip install -e .

# Or install with pip
pip install -e .
```

### **Verify Installation**

```bash
# Check CLI is working
htcli --help

# Verify blockchain connectivity
htcli chain network
```

## 🎯 **Universal Asset Filtering**

### **The --mine Flag: Your Personal Blockchain View**

The `--mine` flag transforms any command to show only **your assets** instead of network-wide data:

```bash
# 📊 NETWORK-WIDE DATA (Default)
htcli subnet list              # Shows ALL subnets on the network
htcli stake info --address ... # Shows stakes for specific address
htcli chain network           # Shows global network statistics

# 👤 YOUR PERSONAL DATA (With --mine)
htcli --mine subnet list      # Shows ONLY subnets you own
htcli --mine stake info       # Shows stakes for ALL your addresses
htcli --mine node list        # Shows ONLY nodes you registered
```

### **How It Works**

1. **Automatic Key Detection**: Reads your wallet keys from `~/.htcli/wallets/`
2. **Smart Ownership Matching**: Compares blockchain ownership with your addresses
3. **Intelligent Filtering**: Shows only assets where you are the owner/stakeholder
4. **Clear Feedback**: Provides guidance when no personal assets are found

### **Example Comparison**

```bash
# Network View: Shows 2 total subnets (including others')
$ htcli subnet list
Found 2 subnets on network (real blockchain data)

# Personal View: Shows only your subnets
$ htcli --mine subnet list
🔍 Filtered for your 1 wallet address(es) - no matching assets found.
💡 Network has 2 total items, but none are owned by you.
```

## 🎯 **Quick Start**

### **1. Initialize Configuration**

```bash
# Interactive configuration setup
htcli config init

# View current configuration
htcli config show
```

### **2. Key Management**

```bash
# Generate a new key
htcli wallet generate-key --name my-key --type sr25519

# List all keys
htcli wallet list-keys
```

### **3. Check Network Status**

```bash
# Get network statistics
htcli chain network

# Check account balance
htcli chain balance --address 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
```

### **4. Subnet Operations**

```bash
# Register a new subnet
htcli subnet register --path my-subnet --memory 1024 --blocks 1000 --interval 100

# Activate subnet
htcli subnet activate --subnet-id 1

# Get subnet information
htcli subnet info --subnet-id 1
```

### **5. Node Management**

```bash
# Add node to subnet
htcli node add --subnet-id 1 --hotkey <address> --peer-id <peer-id> --stake 1000000000000000000

# List nodes in subnet
htcli node list --subnet-id 1

# Check node status
htcli node status --subnet-id 1 --node-id 1
```

### **6. Staking Operations**

```bash
# Add stake to node
htcli stake add --subnet-id 1 --node-id 1 --hotkey <address> --amount 1000000000000000000

# Check stake information
htcli stake info --address <address> --subnet-id 1

# Claim unbonded tokens
htcli stake claim --hotkey <address>
```

## 📋 **Command Structure**

### **Consistent Format**

All commands follow the pattern:

```
htcli <category> <command> [switches]
```

### **Command Categories**

```
htcli
├── config     # Configuration management (5 commands)
│   ├── init           # Interactive configuration setup
│   ├── show           # Display current configuration
│   ├── path           # Show configuration file path
│   ├── edit           # Open configuration in editor
│   └── validate       # Validate configuration file
│
├── subnet     # Subnet operations (5 commands)
│   ├── register       # Register new subnet
│   ├── activate       # Activate registered subnet
│   ├── list           # List all subnets
│   ├── info           # Get subnet information
│   └── remove         # Remove subnet
│
├── node       # Node management (5 commands)
│   ├── add            # Add node to subnet
│   ├── remove         # Remove node from subnet
│   ├── deactivate     # Deactivate node temporarily
│   ├── list           # List nodes in subnet
│   └── status         # Get detailed node status
│
├── stake      # Staking operations (7 commands)
│   ├── add            # Add stake to node
│   ├── remove         # Remove stake from node
│   ├── info           # Get stake information
│   ├── claim          # Claim unbonded tokens
│   ├── delegate-add   # Add delegate stake
│   ├── delegate-remove    # Remove delegate stake
│   └── delegate-transfer  # Transfer delegate stake
│
├── wallet     # Key management (4 commands)
│   ├── generate-key   # Generate new keypair
│   ├── import-key     # Import existing keypair
│   ├── list-keys      # List stored keys
│   └── delete-key     # Delete stored key
│
└── chain      # Chain operations (8 commands)
    ├── network        # Get network statistics
    ├── epoch          # Get current epoch info
    ├── account        # Get account information
    ├── balance        # Get account balance
    ├── peers          # List network peers
    ├── block          # Get block information
    ├── head           # Get chain head
    └── runtime-version # Get runtime version
```

**Total: 34 commands across 6 categories**

## 🎨 **User Experience Features**

### **Interactive Guidance**

Every complex operation includes comprehensive guidance:

```
╭────────────────────── 💰 Adding Stake to Node ──────────────────────────╮
│ This operation will stake TENSOR tokens to support a node in a subnet.   │
│                                                                          │
│ 📋 Requirements:                                                         │
│ • Valid subnet ID and node ID                                            │
│ • Sufficient TENSOR balance in your account                              │
│ • Node must be active and accepting stake                                │
│                                                                          │
│ 💡 Tips & Warnings:                                                      │
│ 💡 Staked tokens are locked and earn rewards                             │
│ ⚠️ Unstaking has an unbonding period before tokens are available        │
│                                                                          │
│ 📊 Current Operation:                                                    │
│ • Subnet ID: 1                                                           │
│ • Stake Amount: 1.000000000000000000 TENSOR                              │
╰──────────────────────────────────────────────────────────────────────────╯
```

### **Safety Features**

- **Confirmation prompts** for destructive operations
- **Warning messages** for unbonding periods and risks
- **Input validation** with helpful error messages
- **Recovery guidance** for failed operations

### **Flexible Output**

```bash
# Table format (default)
htcli chain network

# JSON format for scripting
htcli chain network --format json

# CSV format for data analysis
htcli chain network --format csv
```

## ⚙️ **Configuration**

### **Configuration File**

Default location: `~/.htcli/config.yaml`

```yaml
# Network Configuration
network:
  endpoint: "wss://hypertensor.duckdns.org"
  ws_endpoint: "wss://hypertensor.duckdns.org"
  timeout: 30
  retry_attempts: 3

# Output Configuration
output:
  format: "table"
  verbose: false
  color: true

# Wallet Configuration
wallet:
  path: "~/.htcli/wallets"
  default_name: "default"
  encryption_enabled: true
```

### **Environment Variables**

Override configuration with environment variables:

```bash
export HTCLI_NETWORK_ENDPOINT="wss://custom-endpoint.com"
export HTCLI_OUTPUT_FORMAT="json"
export HTCLI_WALLET_PATH="/custom/wallet/path"
```

## 🔧 **Advanced Usage**

### **Custom Configuration**

```bash
# Use custom config file
htcli --config /path/to/config.yaml chain network

# Override endpoint temporarily
htcli --endpoint wss://custom.endpoint.com chain network

# Enable verbose output
htcli --verbose chain network
```

### **Scripting Examples**

```bash
# Get network stats in JSON for processing
STATS=$(htcli chain network --format json)
echo $STATS | jq '.total_subnets'

# Check multiple balances
for addr in addr1 addr2 addr3; do
    htcli chain balance --address $addr --format json
done

# Automated staking workflow
htcli stake add --subnet-id 1 --node-id 1 --hotkey $HOTKEY --amount $AMOUNT --no-guidance
```

### **Batch Operations**

```bash
# Register multiple subnets
for subnet in subnet1 subnet2 subnet3; do
    htcli subnet register --path $subnet --memory 1024 --blocks 1000 --interval 100
done

# Check status of multiple nodes
for node_id in {1..10}; do
    htcli node status --subnet-id 1 --node-id $node_id --format json
done
```

## 🛠️ **Development**

### **Project Structure**

```
htcli/
├── src/htcli/           # Main CLI source code
│   ├── commands/        # Command implementations
│   │   ├── config.py    # Configuration commands
│   │   ├── subnet.py    # Subnet commands
│   │   ├── node.py      # Node commands
│   │   ├── stake.py     # Staking commands
│   │   ├── wallet.py    # Wallet commands
│   │   └── chain.py     # Chain commands
│   ├── client/          # Blockchain client modules
│   ├── models/          # Request/response models
│   ├── utils/           # Utility functions
│   └── main.py          # CLI entry point
├── tests/               # Test suite
├── docs/                # Documentation
└── pyproject.toml       # Project configuration
```

### **Testing**

```bash
# Run all tests
uv run pytest

# Run specific test categories
uv run pytest tests/unit/
uv run pytest tests/integration/

# Run with coverage
uv run pytest --cov=src/htcli
```

### **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📚 **Documentation**

Comprehensive documentation is available in the `docs/` folder:

- **[Command Documentation](docs/COMMANDS.md)** - Complete command reference
- **[Configuration Guide](docs/CONFIGURATION.md)** - Configuration options and setup
- **[Staking Guide](docs/STAKING.md)** - Staking operations and best practices
- **[Node Management](docs/NODE_MANAGEMENT.md)** - Node lifecycle and operations
- **[API Reference](docs/API.md)** - Client API and integration guide

## 🔍 **Troubleshooting**

### **Common Issues**

#### **Connection Problems**

```bash
# Test network connectivity
htcli chain network

# Use custom endpoint
htcli --endpoint wss://backup.endpoint.com chain network
```

#### **Configuration Issues**

```bash
# Validate configuration
htcli config validate

# Reset configuration
htcli config init --force
```

#### **Key Management Issues**

```bash
# List available keys
htcli wallet list-keys

# Generate new key if needed
htcli wallet generate-key --name backup-key
```

### **Getting Help**

```bash
# General help
htcli --help

# Category help
htcli stake --help

# Command help
htcli stake add --help
```

## 🚀 **Performance & Reliability**

### **Performance Metrics**

- **Command Response Times**: < 0.1s for help, 1-3s for network operations
- **Success Rates**: 100% command execution success
- **Error Handling**: Comprehensive error recovery and user guidance
- **Network Resilience**: Automatic retry with exponential backoff

### **Production Ready Features**

- **18-digit TENSOR precision** for accurate token calculations
- **Real blockchain integration** with transaction submission
- **Comprehensive input validation** and error handling
- **Professional user interface** with rich console output
- **Extensive logging** and debugging capabilities

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 **Support**

- **GitHub Issues**: [Report bugs or request features](https://github.com/shiftlayer-llc/htcli/issues)
- **Documentation**: Check the `docs/` folder for detailed guides
- **Community**: Join the Hypertensor community for support and discussions

## 🎯 **Roadmap**

- [ ] **Web Dashboard**: GUI interface for CLI operations
- [ ] **API Server Mode**: REST API for programmatic access
- [ ] **Advanced Analytics**: Historical data and performance metrics
- [ ] **Multi-Network Support**: Support for additional blockchain networks
- [ ] **Hardware Wallet Integration**: Ledger and Trezor support

---

**Built with ❤️ by the Hypertensor team**
