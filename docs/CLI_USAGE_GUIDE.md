# 🚀 **HTCLI COMMAND LINE USAGE GUIDE**

## ✅ **HOW TO RUN HTCLI**

You can run the CLI in two ways:

### **Method 1: Using the wrapper script (Recommended)**

```bash
./htcli.py [COMMAND] [OPTIONS]
```

### **Method 2: Using uv run**

```bash
uv run python -m src.htcli.main [COMMAND] [OPTIONS]
```

---

## 📋 **NEW COMMAND STRUCTURE**

The CLI now has three main command groups:

```bash
htcli subnet <actions>    # Subnet operations
htcli chain <actions>     # Chain operations
htcli wallet <actions>    # Wallet operations
```

---

## 🎯 **COMMAND EXAMPLES**

### **🌐 SUBNET OPERATIONS**

#### **Register Subnet**

```bash
# Register a new subnet
./htcli.py subnet register create <subnet-path> --memory <MB> --blocks <blocks> --interval <blocks>

# Example:
./htcli.py subnet register create test-subnet --memory 1024 --blocks 1000 --interval 100
```

#### **Activate Subnet**

```bash
# Activate a registered subnet
./htcli.py subnet register activate <subnet-id>

# Example:
./htcli.py subnet register activate 1
```

#### **Manage Subnets**

```bash
# List all subnets
./htcli.py subnet manage list

# Get subnet information
./htcli.py subnet manage info <subnet-id>

# Example:
./htcli.py subnet manage info 1
```

#### **Node Operations**

```bash
# Add node to subnet
./htcli.py subnet nodes add <subnet-id> <peer-id> --hotkey <address>

# List nodes in subnet
./htcli.py subnet nodes list <subnet-id>

# Example:
./htcli.py subnet nodes add 1 QmTestPeerId123 --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
./htcli.py subnet nodes list 1
```

### **💰 WALLET OPERATIONS**

#### **Key Management**

```bash
# Generate new keypair
./htcli.py wallet keys generate <name> [--type <key-type>] [--password <password>]

# List available keys
./htcli.py wallet keys list

# Import existing keypair
./htcli.py wallet keys import <name> --private-key <key> [--type <key-type>] [--password <password>]

# Delete keypair
./htcli.py wallet keys delete <name> [--force]

# Examples:
./htcli.py wallet keys generate my-key --type sr25519
./htcli.py wallet keys list
./htcli.py wallet keys import my-key --private-key 1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
./htcli.py wallet keys delete my-key --force
```

#### **Staking Operations**

```bash
# Add stake to subnet
./htcli.py wallet stake add <subnet-id> <node-id> <amount> --hotkey <address>

# Remove stake from subnet
./htcli.py wallet stake remove <subnet-id> <amount> --hotkey <address>

# Get stake information
./htcli.py wallet stake info <subnet-id> --hotkey <address>

# Examples:
./htcli.py wallet stake add 1 1 1000.0 --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
./htcli.py wallet stake remove 1 500.0 --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
./htcli.py wallet stake info 1 --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
```

### **🔗 CHAIN OPERATIONS**

#### **Chain Information**

```bash
# Get network statistics
./htcli.py chain info network

# Get account information
./htcli.py chain info account <address>

# Get epoch information
./htcli.py chain info epoch

# Examples:
./htcli.py chain info network
./htcli.py chain info account 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
./htcli.py chain info epoch
```

#### **Data Queries**

```bash
# Query account balance
./htcli.py chain query balance <address>

# Query network peers
./htcli.py chain query peers

# Query block information
./htcli.py chain query block [<block-number>]

# Examples:
./htcli.py chain query balance 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
./htcli.py chain query peers
./htcli.py chain query block 12345
```

---

## 🎯 **REAL EXAMPLES WITH OUTPUT**

### **Network Statistics**

```bash
./htcli.py chain info network
```

**Output:**

```
╭──────────────────────────── Network Statistics ─────────────────────────────╮
│                                                                             │
│ Total Subnets: 2                                                            │
│ Active Subnets: 0                                                           │
│ Total Nodes: 0                                                              │
│ Total Stake: 0 TAO                                                          │
│ Current Epoch: 0                                                            │
│ Total Validations: 0                                                        │
│ Total Attestations: 0                                                       │
│ Network Uptime: 0%                                                          │
│ Average Block Time: 0s                                                      │
│                                                                             │
╰─────────────────────────────────────────────────────────────────────────────╯
```

### **Account Balance**

```bash
./htcli.py chain query balance 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
```

**Output:**

```
Balance: 36301712327596.585937500 TAO
```

### **Subnet List**

```bash
./htcli.py subnet manage list
```

**Output:**

```
No subnets found.
```

---

## 🔧 **GLOBAL OPTIONS**

All commands support these global options:

```bash
./htcli.py [GLOBAL_OPTIONS] [COMMAND] [OPTIONS]
```

### **Global Options:**

- `--config, -c PATH` - Configuration file path
- `--endpoint, -e TEXT` - Blockchain endpoint
- `--verbose, -v` - Verbose output
- `--format, -f TEXT` - Output format (table/json/csv) [default: table]
- `--help` - Show help message

### **Examples:**

```bash
# Use custom endpoint
./htcli.py --endpoint wss://custom.endpoint.org chain info network

# Verbose output
./htcli.py --verbose chain info network

# JSON output format
./htcli.py --format json chain info network
```

---

## 🚀 **QUICK START EXAMPLES**

### **1. Check Network Status**

```bash
./htcli.py chain info network
```

### **2. Check Account Balance**

```bash
./htcli.py chain query balance 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
```

### **3. List All Subnets**

```bash
./htcli.py subnet manage list
```

### **4. Generate a New Key**

```bash
./htcli.py wallet keys generate my-wallet
```

### **5. Get Help for Any Command**

```bash
./htcli.py --help
./htcli.py subnet --help
./htcli.py subnet register --help
./htcli.py chain --help
./htcli.py wallet --help
```

---

## ⚠️ **IMPORTANT NOTES**

1. **Real Blockchain Connection**: All commands connect to the live Hypertensor blockchain at `wss://hypertensor.duckdns.org`

2. **Real Data**: All responses show actual blockchain data, not mock responses

3. **Network Calls**: Some operations (like subnet registration) require proper blockchain parameters and may fail if the blockchain structure doesn't match expectations

4. **Key Management**: Keys are stored locally in `~/.htcli/wallets/`

5. **Stake Operations**: Stake amounts are in TAO (the native token)

---

## 🎉 **READY TO USE!**

The `htcli` command line interface is now fully functional with the new clean structure:

```bash
htcli subnet <actions>    # Subnet operations
htcli chain <actions>     # Chain operations
htcli wallet <actions>    # Wallet operations
```

**Start exploring with:**

```bash
./htcli.py --help
```
