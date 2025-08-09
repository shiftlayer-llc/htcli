# Hypertensor CLI Documentation

Welcome to the comprehensive documentation for the Hypertensor CLI (htcli). This documentation covers everything from basic usage to advanced integration and API development.

## 📚 **Documentation Overview**

The Hypertensor CLI documentation is organized into several comprehensive guides:

### **🎯 Core Documentation**

#### **[📋 Commands Reference](COMMANDS.md)**

Complete reference for all 34 CLI commands across 6 categories:

- **Configuration Management** (5 commands) - Setup and manage CLI configuration
- **Subnet Operations** (5 commands) - Register and manage subnets
- **Node Management** (5 commands) - Add, monitor, and manage nodes
- **Staking Operations** (7 commands) - Stake tokens and earn rewards
- **Wallet & Key Management** (4 commands) - Generate and manage cryptographic keys
- **Chain Queries** (8 commands) - Query blockchain information

#### **[⚙️ Configuration Guide](CONFIGURATION.md)**

Comprehensive configuration management covering:

- Interactive configuration wizard
- YAML configuration files
- Environment variable overrides
- Multiple environment setups
- Configuration validation and troubleshooting

#### **[💰 Staking Guide](STAKING.md)**

Complete staking operations manual including:

- Direct node staking strategies
- Delegate staking for diversification
- Unbonding and claims management
- Risk management and portfolio optimization
- Performance monitoring and rebalancing

#### **[🔗 Node Management Guide](NODE_MANAGEMENT.md)**

Comprehensive node lifecycle management covering:

- Node registration and activation
- Performance monitoring and optimization
- Maintenance and troubleshooting
- Best practices for node operators

#### **[🔧 API Reference](API.md)**

Complete programmatic API documentation including:

- Client architecture and initialization
- All client APIs (Subnet, Node, Staking, Wallet, Chain)
- Request/response models and data structures
- Error handling and retry strategies
- Integration examples and automation scripts

### **📊 Technical References**

#### **[🌳 Command Tree Structure](COMMAND_TREE.md)**

Visual representation of the complete CLI command hierarchy

#### **[📏 TENSOR Precision Guide](TENSOR_PRECISION_GUIDE.md)**

Detailed guide on 18-digit TENSOR token precision handling

#### **[✅ Command Testing Results](COMMAND_TESTING_RESULTS.md)**

Comprehensive testing results showing 100% command success rate

## 🚀 **Quick Start Guide**

### **1. Installation**

```bash
# Clone and install
git clone https://github.com/shiftlayer-llc/htcli.git
cd htcli
uv pip install -e .
```

### **2. Initial Configuration**

```bash
# Interactive configuration setup
htcli config init

# Verify installation
htcli --help
```

### **3. Basic Operations**

```bash
# Check network status
htcli chain network

# Generate a key
htcli wallet generate-key --name my-key

# Check balance
htcli chain balance --address <your-address>
```

### **4. Advanced Operations**

```bash
# Register a subnet
htcli subnet register --path my-subnet --memory 2048 --blocks 1000 --interval 100

# Add a node
htcli node add --subnet-id 1 --hotkey <address> --peer-id <peer> --stake 1000000000000000000

# Stake tokens
htcli stake add --subnet-id 1 --node-id 1 --hotkey <address> --amount 2000000000000000000
```

## 📖 **Documentation Structure**

### **User Guides**

- **Beginners**: Start with [Commands Reference](COMMANDS.md) and [Configuration Guide](CONFIGURATION.md)
- **Node Operators**: Focus on [Node Management Guide](NODE_MANAGEMENT.md)
- **Stakers**: Read the [Staking Guide](STAKING.md) thoroughly
- **Developers**: Use the [API Reference](API.md) for integration

### **Reference Materials**

- **Command Syntax**: [Commands Reference](COMMANDS.md)
- **Configuration Options**: [Configuration Guide](CONFIGURATION.md)
- **API Methods**: [API Reference](API.md)
- **Technical Details**: Technical reference documents

## 🎯 **Key Features Covered**

### **Professional CLI Experience**

- **34 commands** across 6 logical categories
- **Consistent switch-based format** for all commands
- **Interactive guidance** with comprehensive help
- **Multiple output formats** (table, JSON, CSV)
- **Safety features** with confirmation prompts

### **Real Blockchain Integration**

- **Direct WebSocket connections** to Hypertensor network
- **18-digit TENSOR precision** for accurate calculations
- **Real transaction submission** and blockchain queries
- **Comprehensive error handling** and recovery guidance

### **Advanced Features**

- **Modular client architecture** for programmatic access
- **Configuration management** with multiple environments
- **Performance monitoring** and optimization tools
- **Risk management** strategies and best practices

## 🔄 **Workflow Examples**

### **Complete Subnet Setup**

```bash
htcli config init                    # Configure CLI
htcli wallet generate-key --name owner  # Generate keys
htcli subnet register --path ai-net --memory 4096 --blocks 1000 --interval 100
htcli subnet activate --subnet-id 1
htcli node add --subnet-id 1 --hotkey <addr> --peer-id <peer> --stake 5000000000000000000
```

### **Staking Management**

```bash
htcli stake info --address <addr>    # Check current positions
htcli stake add --subnet-id 1 --node-id 2 --hotkey <addr> --amount 2000000000000000000
htcli stake remove --subnet-id 1 --hotkey <addr> --amount 1000000000000000000
htcli stake claim --hotkey <addr>    # Claim unbonded tokens
```

### **Network Monitoring**

```bash
htcli chain network                  # Network overview
htcli subnet list                    # All subnets
htcli node list --subnet-id 1        # Nodes in subnet
htcli stake info --address <addr>    # Stake positions
```

## 🛠️ **Development Resources**

### **API Integration**

```python
from src.htcli.client import HypertensorClient

client = HypertensorClient()
response = client.chain.get_network_stats()
print(f"Total subnets: {response.data['total_subnets']}")
```

### **Configuration Management**

```python
from src.htcli.config import load_config

config = load_config()
endpoint = config.network.endpoint
```

### **Automation Scripts**

The documentation includes complete examples for:

- Network monitoring bots
- Automated staking strategies
- Performance optimization scripts
- Batch operations and management

## 📞 **Support and Resources**

### **Getting Help**

```bash
# General help
htcli --help

# Category help
htcli stake --help

# Command-specific help
htcli stake add --help
```

### **Troubleshooting**

Each guide includes comprehensive troubleshooting sections:

- Common issues and solutions
- Error message explanations
- Recovery procedures
- Performance optimization tips

### **Community Resources**

- **GitHub Issues**: Report bugs and request features
- **Documentation**: This comprehensive guide collection
- **API Reference**: Complete programmatic interface documentation

## 🎉 **Documentation Features**

### **Comprehensive Coverage**

- **Every command documented** with examples and use cases
- **Complete workflow guides** from setup to advanced operations
- **Real-world examples** and practical scenarios
- **Best practices** and optimization strategies

### **User-Friendly Format**

- **Clear structure** with logical organization
- **Rich examples** with actual command syntax
- **Visual aids** including command trees and workflows
- **Progressive complexity** from basic to advanced topics

### **Practical Focus**

- **Real blockchain integration** examples
- **Production-ready scripts** and automation
- **Security best practices** and risk management
- **Performance optimization** and monitoring

---

**This documentation covers everything you need to effectively use the Hypertensor CLI, from basic operations to advanced automation and integration.** Each guide is designed to be comprehensive yet practical, with real examples and best practices for successful Hypertensor network participation.

**Start with the [Commands Reference](COMMANDS.md) for a complete overview, then dive into specific guides based on your use case and experience level.**
