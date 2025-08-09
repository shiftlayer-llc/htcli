# Hypertensor CLI Command Tree - 3-Level Structure

## Overview

The Hypertensor CLI has been restructured from a 4-level hierarchy to a clean **3-level hierarchy** for better usability and simplicity.

## Command Tree Structure

```text
htcli
├── subnet                    # Subnet operations
│   ├── register             # Register a new subnet
│   ├── activate             # Activate a registered subnet
│   ├── list                 # List all subnets
│   ├── info                 # Get subnet information
│   ├── add-node             # Add a node to subnet
│   ├── list-nodes           # List subnet nodes
│   └── remove               # Remove a subnet
│
├── wallet                    # Wallet operations
│   ├── generate-key         # Generate a new keypair
│   ├── import-key           # Import a keypair
│   ├── list-keys            # List stored keys
│   ├── delete-key           # Delete a stored key
│   ├── add-stake            # Add stake to node
│   ├── remove-stake         # Remove stake from node
│   ├── stake-info           # Get stake information
│   └── claim-unbondings     # Claim unbonded stake
│
└── chain                     # Chain operations
    ├── network               # Network statistics
    ├── epoch                 # Epoch information
    ├── account               # Account information
    ├── balance               # Account balance
    ├── peers                 # Network peers
    ├── block                 # Block information
    ├── head                  # Chain head
    └── runtime-version       # Runtime version
```

## Command Usage Examples

### Subnet Commands

```bash
# Register a new subnet
htcli subnet register my-subnet --memory 1024 --blocks 1000 --interval 100

# Activate a subnet
htcli subnet activate 1

# List all subnets
htcli subnet list

# Get subnet information
htcli subnet info 1

# Add a node to subnet
htcli subnet add-node 1 --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY --peer-id QmTestPeerId123

# List subnet nodes
htcli subnet list-nodes 1

# Remove a subnet
htcli subnet remove 1
```

### Wallet Commands

```bash
# Generate a new key
htcli wallet generate-key my-key --type sr25519

# Import a key
htcli wallet import-key my-key --private-key 1234567890abcdef...

# List all keys
htcli wallet list-keys

# Delete a key
htcli wallet delete-key my-key

# Add stake to a node
htcli wallet add-stake --subnet-id 1 --node-id 1 --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY --amount 1000000000000000000

# Remove stake from a node
htcli wallet remove-stake --subnet-id 1 --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY --amount 500000000000000000

# Get stake information
htcli wallet stake-info 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY --subnet-id 1

# Claim unbonded stake
htcli wallet claim-unbondings --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
```

### Chain Commands

```bash
# Get network statistics
htcli chain network

# Get epoch information
htcli chain epoch

# Get account information
htcli chain account 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY

# Get account balance
htcli chain balance 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY

# Get network peers
htcli chain peers --limit 10

# Get block information
htcli chain block --number 12345
htcli chain block --hash 0x1234567890abcdef...

# Get chain head
htcli chain head

# Get runtime version
htcli chain runtime-version
```

## Benefits of 3-Level Structure

### 1. **Simplified Navigation**

- **Before**: `htcli subnet register create` (4 levels)
- **After**: `htcli subnet register` (3 levels)

### 2. **Intuitive Commands**

- Commands are more descriptive and self-explanatory
- Easier to remember and type
- Better discoverability

### 3. **Consistent Pattern**

- All commands follow the same 3-level pattern
- Predictable command structure
- Reduced cognitive load

### 4. **Better Help System**

- Clearer help output
- Easier to find available commands
- Better command organization

## Migration Guide

### Old 4-Level Commands → New 3-Level Commands

| Old Command | New Command | Description |
|-------------|-------------|-------------|
| `htcli subnet register create` | `htcli subnet register` | Register subnet |
| `htcli subnet register activate` | `htcli subnet activate` | Activate subnet |
| `htcli subnet manage list` | `htcli subnet list` | List subnets |
| `htcli subnet manage info` | `htcli subnet info` | Subnet info |
| `htcli subnet nodes add` | `htcli subnet add-node` | Add node |
| `htcli subnet nodes list` | `htcli subnet list-nodes` | List nodes |
| `htcli wallet keys generate` | `htcli wallet generate-key` | Generate key |
| `htcli wallet keys import` | `htcli wallet import-key` | Import key |
| `htcli wallet keys list` | `htcli wallet list-keys` | List keys |
| `htcli wallet keys delete` | `htcli wallet delete-key` | Delete key |
| `htcli wallet stake add` | `htcli wallet add-stake` | Add stake |
| `htcli wallet stake remove` | `htcli wallet remove-stake` | Remove stake |
| `htcli wallet stake info` | `htcli wallet stake-info` | Stake info |
| `htcli chain info network` | `htcli chain network` | Network stats |
| `htcli chain info epoch` | `htcli chain epoch` | Epoch info |
| `htcli chain info account` | `htcli chain account` | Account info |
| `htcli chain query balance` | `htcli chain balance` | Account balance |
| `htcli chain query peers` | `htcli chain peers` | Network peers |
| `htcli chain query block` | `htcli chain block` | Block info |

## Command Categories

### 🏗️ **Subnet Operations** (7 commands)

- **Registration**: `register`, `activate`
- **Management**: `list`, `info`, `remove`
- **Node Operations**: `add-node`, `list-nodes`

### 💰 **Wallet Operations** (8 commands)

- **Key Management**: `generate-key`, `import-key`, `list-keys`, `delete-key`
- **Staking Operations**: `add-stake`, `remove-stake`, `stake-info`, `claim-unbondings`

### 🔍 **Chain Operations** (8 commands)

- **Information**: `network`, `epoch`, `account`, `balance`
- **Data Queries**: `peers`, `block`, `head`, `runtime-version`

## Global Options

All commands support these global options:

```bash
htcli [OPTIONS] COMMAND [ARGS]...

Options:
  --config PATH           Configuration file path
  --endpoint TEXT         Blockchain endpoint URL
  --verbose              Enable verbose output
  --format TEXT          Output format (table/json/csv)
  --help                 Show this message and exit
```

## Output Formats

Most commands support multiple output formats:

```bash
# Table format (default)
htcli subnet list

# JSON format
htcli subnet list --format json

# CSV format
htcli subnet list --format csv
```

## Error Handling

The CLI provides comprehensive error handling:

- **Invalid commands**: Clear error messages with suggestions
- **Missing arguments**: Helpful prompts for required parameters
- **Network errors**: Graceful handling of connection issues
- **Validation errors**: Clear feedback for invalid inputs

## Help System

Get help at any level:

```bash
# Main help
htcli --help

# Category help
htcli subnet --help
htcli wallet --help
htcli chain --help

# Command help
htcli subnet register --help
htcli wallet generate-key --help
htcli chain network --help
```

This 3-level structure provides a clean, intuitive, and powerful interface for managing the Hypertensor blockchain network.
