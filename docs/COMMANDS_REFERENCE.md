# Hypertensor CLI (htcli) - Command Reference

## 🎯 **Quick Start**

```bash
# Get help
htcli --help

# Subnet operations
htcli subnet --help
htcli subnet register create my-subnet

# Wallet operations
htcli wallet --help
htcli wallet keys generate my-key

# Chain queries
htcli chain --help
htcli chain info network
```

## 🏗️ **Subnet Commands**

### **Registration**
```bash
# Create subnet
htcli subnet register create <name> [OPTIONS]
  --memory-mb INTEGER              [default: 1024]
  --registration-blocks INTEGER    [default: 1000]
  --entry-interval INTEGER         [default: 100]

# Activate subnet
htcli subnet register activate <subnet-id>
```

### **Management**
```bash
# List subnets
htcli subnet manage list

# Get subnet info
htcli subnet manage info <subnet-id>
```

### **Nodes**
```bash
# Add node to subnet
htcli subnet nodes add <subnet-id> [OPTIONS]
  --hotkey TEXT                    [required]
  --peer-id TEXT                   [required]
  --delegate-reward-rate INTEGER   [default: 1000]
  --stake-to-be-added INTEGER      [default: 1000000000000]

# List subnet nodes
htcli subnet nodes list <subnet-id>
```

## 💰 **Wallet Commands**

### **Key Management**
```bash
# Generate key
htcli wallet keys generate <name> [OPTIONS]
  --type TEXT                     [sr25519, ed25519] [default: sr25519]

# Import key
htcli wallet keys import <name> [OPTIONS]
  --mnemonic TEXT                 [required]
  --type TEXT                     [sr25519, ed25519]

# List keys
htcli wallet keys list

# Delete key
htcli wallet keys delete <name>
```

### **Staking**
```bash
# Add stake
htcli wallet stake add [OPTIONS]
  --subnet-id INTEGER             [required]
  --node-id INTEGER               [required]
  --amount INTEGER                [required]
  --key-name TEXT                 [required]

# Remove stake
htcli wallet stake remove [OPTIONS]
  --subnet-id INTEGER             [required]
  --node-id INTEGER               [required]
  --amount INTEGER                [required]
  --key-name TEXT                 [required]

# Get stake info
htcli wallet stake info [OPTIONS]
  --hotkey TEXT                   [required]
  --subnet-id INTEGER             [optional]
```

## 🔍 **Chain Commands**

### **Information**
```bash
# Network statistics
htcli chain info network

# Epoch information
htcli chain info epoch

# Account information
htcli chain info account <address>
```

### **Queries**
```bash
# Balance query
htcli chain query balance <address>

# Peers query
htcli chain query peers

# Block information
htcli chain query block [OPTIONS]
  --block-hash TEXT               [optional]
  --block-number INTEGER          [optional]
```

## 📝 **Examples**

### **Complete Workflow**
```bash
# 1. Generate key
htcli wallet keys generate my-key --type sr25519

# 2. Register subnet
htcli subnet register create my-subnet --memory-mb 1024

# 3. Activate subnet
htcli subnet register activate 1

# 4. Add node
htcli subnet nodes add 1 \
  --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY \
  --peer-id QmTestPeerId123456789

# 5. Add stake
htcli wallet stake add \
  --subnet-id 1 --node-id 5 \
  --amount 1000000000000 --key-name my-key

# 6. Check network
htcli chain info network
```

### **Advanced Usage**
```bash
# Verbose mode
htcli --verbose subnet register create test-subnet

# JSON output
htcli --format json chain info network

# Custom endpoint
htcli --endpoint wss://custom.endpoint:9944 chain info network
```

## ⚙️ **Global Options**

```bash
htcli [OPTIONS] COMMAND [ARGS]...

Options:
  --config PATH           Configuration file path
  --endpoint TEXT         Blockchain endpoint URL
  --verbose              Enable verbose output
  --format TEXT          Output format (table, json, yaml)
  --help                 Show this message and exit
```

## ⚠️ **Error Handling**

### **Common Issues**
- **Connection timeout**: Check network connectivity
- **Invalid address**: Use valid SS58 format
- **Insufficient balance**: Check account balance first
- **Command not found**: Use `--help` for available commands

### **Debugging**
```bash
# Enable verbose output
htcli --verbose <command>

# Check configuration
htcli --config /path/to/config.yaml --help

# JSON output for debugging
htcli --format json <command>
```

## 🔧 **Configuration**

### **Environment Variables**
```bash
export HTCLI_NETWORK_ENDPOINT="wss://hypertensor.duckdns.org"
export HTCLI_OUTPUT_FORMAT="table"
export HTCLI_OUTPUT_VERBOSE="false"
export HTCLI_WALLET_PATH="~/.htcli/wallets"
```

### **Config File** (`~/.htcli/config.yaml`)
```yaml
network:
  endpoint: "wss://hypertensor.duckdns.org"
  timeout: 30
  retry_attempts: 3

output:
  format: "table"
  verbose: false
  color: true

wallet:
  path: "~/.htcli/wallets"
  default_name: "default"
```

---

**Last Updated**: December 2024
**Version**: 1.0.0
**Status**: Production Ready ✅
