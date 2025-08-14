# Hypertensor CLI Documentation

Welcome to the comprehensive documentation for the Hypertensor CLI (htcli) - a powerful command-line interface for managing the Hypertensor blockchain network.

## 🚀 Quick Start

```bash
# Install the CLI
pip install htcli

# Initialize configuration
htcli config init

# Generate your first keypair
htcli wallet generate-key --name my-key

# View network information
htcli chain info
```

## 📚 Documentation Index

### Core Features
- **[Commands Overview](COMMANDS.md)** - Complete command reference and usage patterns
- **[Command Tree](COMMAND_TREE.md)** - Visual command hierarchy and structure
- **[API Reference](API.md)** - Programmatic interface and client methods
- **[Configuration Guide](CONFIGURATION.md)** - Setup and configuration management

### Blockchain Operations
- **[Node Management](NODE_MANAGEMENT.md)** - Complete node lifecycle management
- **[Staking Guide](STAKING.md)** - Comprehensive staking operations and strategies
- **[Personal Asset Filtering](PERSONAL_ASSET_FILTERING.md)** - Universal --mine flag usage

### Advanced Features
- **[Automated Flows](AUTOMATED_FLOWS.md)** - Multi-step automated workflows
- **[Tensor Precision Guide](TENSOR_PRECISION_GUIDE.md)** - Token precision and calculations

### Development & Testing
- **[Command Testing Results](COMMAND_TESTING_RESULTS.md)** - Testing status and results
- **[Command Restructure Summary](COMMAND_RESTRUCTURE_SUMMARY.md)** - Recent improvements
- **[Test Update Summary](TEST_UPDATE_SUMMARY.md)** - Testing framework updates

## 🎯 Key Features

### 🔗 Complete Node Lifecycle Management
```bash
# Register a new node
htcli node register --subnet-id 1 --hotkey 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu --peer-id 12D3KooW... --stake 1000000000000000000 --key-name my-node-key

# Activate the node
htcli node activate --subnet-id 1 --node-id 5 --key-name my-node-key

# Update delegate reward rate
htcli node update --subnet-id 1 --node-id 5 --delegate-reward-rate 50000000000000000 --key-name my-node-key

# Update node keys
htcli node update-coldkey --subnet-id 1 --node-id 5 --new-coldkey 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu --key-name my-node-key
htcli node update-hotkey --subnet-id 1 --node-id 5 --new-hotkey 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu --key-name my-node-key

# Deactivate temporarily
htcli node deactivate --subnet-id 1 --node-id 5 --key-name my-node-key

# Reactivate within time limits
htcli node reactivate --subnet-id 1 --node-id 5 --key-name my-node-key

# Remove with beautiful stake management
htcli node remove --subnet-id 1 --node-id 5 --remove-stake --key-name my-node-key
```

### 💰 Comprehensive Staking System
```bash
# Subnet delegate staking
htcli stake delegate-add --subnet-id 1 --amount 1000000000000000000 --key-name my-staking-key
htcli stake delegate-remove --subnet-id 1 --shares 500000000000000000 --key-name my-staking-key
htcli stake delegate-transfer --subnet-id 1 --to-account 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu --shares 100000000000000000 --key-name my-staking-key
htcli stake delegate-increase --subnet-id 1 --amount 500000000000000000 --key-name my-staking-key

# Node delegate staking
htcli stake node-add --subnet-id 1 --node-id 5 --amount 1000000000000000000 --key-name my-staking-key
htcli stake node-remove --subnet-id 1 --node-id 5 --shares 500000000000000000 --key-name my-staking-key
htcli stake node-transfer --subnet-id 1 --node-id 5 --to-account 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu --shares 100000000000000000 --key-name my-staking-key
htcli stake node-increase --subnet-id 1 --node-id 5 --amount 500000000000000000 --key-name my-staking-key
```

### 🔑 Complete Subnet Management
```bash
# Register a new subnet
htcli subnet register --name "My Subnet" --repo "https://github.com/my/subnet" --description "A great subnet" --min-stake 1000000000000000000 --max-stake 10000000000000000000 --key-name my-subnet-key

# Activate the subnet
htcli subnet activate --subnet-id 1 --key-name my-subnet-key

# Pause/unpause subnet
htcli subnet pause --subnet-id 1 --key-name my-subnet-key
htcli subnet unpause --subnet-id 1 --key-name my-subnet-key

# Update subnet parameters
htcli subnet owner-update-name --subnet-id 1 --name "Updated Subnet Name" --key-name my-subnet-key
htcli subnet owner-update-repo --subnet-id 1 --repo "https://github.com/my/updated-subnet" --key-name my-subnet-key
htcli subnet owner-update-description --subnet-id 1 --description "Updated description" --key-name my-subnet-key

# Transfer ownership
htcli subnet owner-transfer-ownership --subnet-id 1 --new-owner 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu --key-name my-subnet-key
```

### 🎯 Personal Asset Filtering
```bash
# View only your assets
htcli subnet list --mine
htcli stake info --mine
htcli node list --mine

# Universal --mine flag works across all commands
htcli subnet info --subnet-id 1 --mine
htcli node status --subnet-id 1 --node-id 5 --mine
```

### 🔄 Automated Workflows
```bash
# List available automated flows
htcli flow list

# Get detailed information about a flow
htcli flow info subnet-deployment

# Run an automated workflow
htcli flow run subnet-deployment
```

## 🏗️ Architecture Overview

### Core Components
- **Client Layer**: Direct blockchain interaction via SubstrateInterface
- **Command Layer**: Typer-based CLI with rich formatting
- **Validation Layer**: Comprehensive input validation and error handling
- **Guidance Layer**: Rich panels and strategic advice
- **Configuration Layer**: Secure key management and settings

### Key Design Principles
- **Lazy Initialization**: Blockchain connection only when needed
- **Comprehensive Validation**: Input validation and error handling
- **Rich User Experience**: Beautiful panels and clear guidance
- **Strategic Planning**: Guidance for optimal operations
- **Security First**: Proper key management and validation

## 🔧 Technical Specifications

### Blockchain Integration
- **SubstrateInterface**: Direct blockchain interaction
- **Real Transactions**: Actual transaction submission and confirmation
- **Storage Queries**: Direct blockchain state queries
- **Extrinsic Composition**: Proper call composition and signing

### Security Features
- **Key Management**: Secure key generation, storage, and loading
- **Validation**: Comprehensive input and state validation
- **Error Handling**: Graceful error handling and user feedback
- **Confirmation**: Proper confirmations for critical operations

### User Experience
- **Rich Formatting**: Beautiful panels, tables, and status indicators
- **Comprehensive Guidance**: Strategic advice and best practices
- **Progress Tracking**: Clear status updates and progress indication
- **Command Examples**: Exact commands and usage patterns

## 🚀 Getting Started

### Installation
```bash
# Install from source
git clone https://github.com/your-repo/htcli.git
cd htcli
pip install -e .

# Or install via pip
pip install htcli
```

### Initial Setup
```bash
# Initialize configuration
htcli config init

# Generate your first keypair
htcli wallet generate-key --name my-key

# Test connection
htcli chain info
```

### First Operations
```bash
# View network status
htcli chain info

# List subnets
htcli subnet list

# Generate a key for staking
htcli wallet generate-key --name my-staking-key

# Start staking
htcli stake delegate-add --subnet-id 1 --amount 1000000000000000000 --key-name my-staking-key
```

## 📈 Advanced Usage

### Node Management Strategy
```bash
# Complete node lifecycle
htcli node register --subnet-id 1 --hotkey <hotkey> --peer-id <peer-id> --stake 1000000000000000000 --key-name my-node-key
htcli node activate --subnet-id 1 --node-id <node-id> --key-name my-node-key
htcli node update --subnet-id 1 --node-id <node-id> --delegate-reward-rate 50000000000000000 --key-name my-node-key
htcli node status --subnet-id 1 --node-id <node-id>
```

### Staking Portfolio Management
```bash
# Diversify across subnets and nodes
htcli stake delegate-add --subnet-id 1 --amount 1000000000000000000 --key-name my-staking-key
htcli stake node-add --subnet-id 1 --node-id 5 --amount 500000000000000000 --key-name my-staking-key
htcli stake delegate-add --subnet-id 2 --amount 500000000000000000 --key-name my-staking-key

# Monitor your portfolio
htcli stake info --mine
```

### Subnet Ownership Management
```bash
# Complete subnet lifecycle
htcli subnet register --name "My Subnet" --repo "https://github.com/my/subnet" --description "A great subnet" --key-name my-subnet-key
htcli subnet activate --subnet-id <subnet-id> --key-name my-subnet-key
htcli subnet owner-update-name --subnet-id <subnet-id> --name "Updated Name" --key-name my-subnet-key
```

## 🎯 Best Practices

### Security
- Use hardware wallets for coldkeys
- Keep hotkeys and coldkeys separate
- Regularly backup your keys
- Use strong passwords for key encryption

### Performance
- Monitor node performance regularly
- Update delegate reward rates strategically
- Diversify staking across multiple subnets/nodes
- Plan node lifecycle operations carefully

### Strategy
- Research nodes before staking
- Monitor reward rates and performance
- Consider both subnet and node staking
- Plan for long-term network participation

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines and development documentation for more information.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**The Hypertensor CLI provides a comprehensive, professional-grade interface for managing the Hypertensor blockchain network with beautiful user experience and strategic guidance.** 🚀
