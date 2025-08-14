# Command Tree Structure

Complete visual representation of the Hypertensor CLI command hierarchy and structure.

## 🌳 Complete Command Tree

```
htcli
├── config
│   ├── init                    # Initialize configuration
│   ├── show                    # Show configuration
│   ├── edit                    # Edit configuration
│   ├── set                     # Set configuration value
│   └── get                     # Get configuration value
│
├── subnet
│   ├── register                # Register new subnet
│   ├── activate                # Activate subnet
│   ├── pause                   # Pause subnet
│   ├── unpause                 # Unpause subnet
│   ├── list                    # List subnets
│   ├── info                    # Get subnet info
│   ├── owner-update-name       # Update subnet name
│   ├── owner-update-repo       # Update subnet repository
│   ├── owner-update-description # Update subnet description
│   ├── owner-update-churn-limit # Update churn limit
│   ├── owner-update-min-stake  # Update minimum stake
│   ├── owner-update-max-stake  # Update maximum stake
│   ├── owner-update-registration-epochs # Update registration epochs
│   ├── owner-update-activation-grace-epochs # Update activation grace epochs
│   ├── owner-update-idle-epochs # Update idle epochs
│   ├── owner-update-included-epochs # Update included epochs
│   ├── owner-update-max-penalties # Update max penalties
│   ├── owner-add-initial-coldkeys # Add initial coldkeys
│   ├── owner-remove-initial-coldkeys # Remove initial coldkeys
│   ├── owner-transfer-ownership # Transfer ownership
│   ├── owner-accept-ownership  # Accept ownership
│   ├── owner-undo-transfer     # Undo ownership transfer
│   └── owner-remove-node       # Remove subnet node
│
├── node
│   ├── register                # Register new node
│   ├── activate                # Activate node
│   ├── update                  # Update delegate reward rate
│   ├── update-coldkey          # Update node coldkey
│   ├── update-hotkey           # Update node hotkey
│   ├── deactivate              # Deactivate node
│   ├── reactivate              # Reactivate node
│   ├── remove                  # Remove node
│   ├── cleanup-expired         # Cleanup expired nodes
│   ├── status                  # Get node status
│   └── list                    # List nodes
│
├── stake
│   ├── delegate-add            # Add subnet delegate stake
│   ├── delegate-remove         # Remove subnet delegate stake
│   ├── delegate-transfer       # Transfer subnet delegate stake
│   ├── delegate-increase       # Increase subnet delegate stake pool
│   ├── node-add                # Add node delegate stake
│   ├── node-remove             # Remove node delegate stake
│   ├── node-transfer           # Transfer node delegate stake
│   ├── node-increase           # Increase node delegate stake pool
│   ├── add                     # Add stake (legacy)
│   ├── remove                  # Remove stake (legacy)
│   ├── info                    # Get staking info
│   └── claim                   # Claim unbonded tokens
│
├── wallet
│   ├── generate-key            # Generate new key
│   ├── generate-hotkey         # Generate hotkey
│   ├── import-key              # Import existing key
│   ├── list-keys               # List stored keys
│   ├── status                  # Get wallet status
│   └── delete-key              # Delete stored key
│
├── chain
│   ├── info                    # Get network info
│   ├── balance                 # Get account balance
│   ├── block                   # Get block info
│   ├── transaction             # Get transaction info
│   ├── network                 # Get network stats
│   ├── subnet                  # Get subnet stats
│   ├── node                    # Get node stats
│   └── stake                   # Get staking stats
│
└── flow
    ├── list                    # List available flows
    ├── info                    # Get flow information
    └── run                     # Run automated flow
```

## 📊 Command Categories

### Configuration Management (5 commands)
- **config init**: Interactive configuration wizard
- **config show**: Display current configuration
- **config edit**: Interactive configuration editor
- **config set**: Set specific configuration values
- **config get**: Retrieve specific configuration values

### Subnet Operations (15 commands)
- **subnet register**: Register new subnet with comprehensive parameters
- **subnet activate**: Activate registered subnet
- **subnet pause/unpause**: Pause and resume subnet operations
- **subnet list/info**: List and get subnet information
- **subnet owner-***: Complete owner management operations

### Node Management (10 commands)
- **node register**: Register new node with comprehensive parameters
- **node activate**: Activate registered node
- **node update**: Update node parameters (reward rate, keys)
- **node deactivate/reactivate**: Node lifecycle management
- **node remove**: Remove node with beautiful stake management
- **node cleanup-expired**: Cleanup expired nodes
- **node status/list**: Node monitoring and listing

### Staking Operations (12 commands)
- **stake delegate-***: Subnet delegate staking operations
- **stake node-***: Node delegate staking operations
- **stake add/remove**: Legacy staking operations
- **stake info**: Comprehensive staking information
- **stake claim**: Claim unbonded tokens

### Wallet & Key Management (6 commands)
- **wallet generate-key**: Generate new cryptographic keys
- **wallet generate-hotkey**: Generate hotkeys for node operations
- **wallet import-key**: Import existing keys
- **wallet list-keys**: List stored keys
- **wallet status**: Get detailed wallet status
- **wallet delete-key**: Delete stored keys

### Chain Queries (8 commands)
- **chain info**: Network information
- **chain balance**: Account balances
- **chain block**: Block information
- **chain transaction**: Transaction information
- **chain network**: Network statistics
- **chain subnet**: Subnet statistics
- **chain node**: Node statistics
- **chain stake**: Staking statistics

### Automated Flows (3 commands)
- **flow list**: List available automated workflows
- **flow info**: Get detailed flow information
- **flow run**: Execute automated workflows

## 🎯 Universal Options

### Common Flags
All commands support these common options:
- `--help`: Show command help
- `--format <format>`: Output format (table, json, csv)
- `--limit <number>`: Limit number of results
- `--mine`: Filter to show only your assets
- `--guidance/--no-guidance`: Show/hide comprehensive guidance

### Personal Asset Filtering
The `--mine` flag works across all commands:
```bash
# Subnet operations
htcli subnet list --mine
htcli subnet info --subnet-id 1 --mine

# Node operations
htcli node list --mine
htcli node status --subnet-id 1 --node-id 5 --mine

# Staking operations
htcli stake info --mine
htcli stake delegate-add --subnet-id 1 --amount 1000000000000000000 --key-name my-key --mine

# Chain queries
htcli chain balance --address <your-address> --mine
```

## 🔧 Command Patterns

### Registration Commands
```bash
# Subnet registration
htcli subnet register \
  --name "My Subnet" \
  --repo "https://github.com/my/subnet" \
  --description "A great subnet" \
  --min-stake 1000000000000000000 \
  --max-stake 10000000000000000000 \
  --key-name my-subnet-key

# Node registration
htcli node register \
  --subnet-id 1 \
  --hotkey <hotkey> \
  --peer-id <peer-id> \
  --stake 1000000000000000000 \
  --key-name my-node-key
```

### Activation Commands
```bash
# Subnet activation
htcli subnet activate --subnet-id 1 --key-name my-subnet-key

# Node activation
htcli node activate --subnet-id 1 --node-id 5 --key-name my-node-key
```

### Update Commands
```bash
# Update subnet parameters
htcli subnet owner-update-name --subnet-id 1 --name "Updated Name" --key-name my-subnet-key

# Update node parameters
htcli node update --subnet-id 1 --node-id 5 --delegate-reward-rate 60000000000000000 --key-name my-node-key
```

### Staking Commands
```bash
# Subnet delegate staking
htcli stake delegate-add --subnet-id 1 --amount 1000000000000000000 --key-name my-staking-key

# Node delegate staking
htcli stake node-add --subnet-id 1 --node-id 5 --amount 1000000000000000000 --key-name my-staking-key
```

## 📈 Command Usage Statistics

### Most Used Commands
1. **htcli subnet list** - List all subnets
2. **htcli node list** - List nodes in subnet
3. **htcli stake info** - Get staking information
4. **htcli chain info** - Get network information
5. **htcli wallet list-keys** - List stored keys

### Advanced Commands
1. **htcli subnet register** - Complete subnet registration
2. **htcli node register** - Complete node registration
3. **htcli stake delegate-add** - Subnet delegate staking
4. **htcli node update** - Node parameter updates
5. **htcli flow run** - Automated workflows

## 🎯 Command Examples

### Complete Workflows
```bash
# Complete subnet deployment
htcli subnet register --name "My Subnet" --repo "https://github.com/my/subnet" --key-name my-key
htcli subnet activate --subnet-id 1 --key-name my-key
htcli node register --subnet-id 1 --hotkey <hotkey> --peer-id <peer-id> --stake 1000000000000000000 --key-name my-node-key
htcli node activate --subnet-id 1 --node-id 5 --key-name my-node-key

# Complete staking portfolio
htcli stake delegate-add --subnet-id 1 --amount 1000000000000000000 --key-name my-staking-key
htcli stake node-add --subnet-id 1 --node-id 5 --amount 500000000000000000 --key-name my-staking-key
htcli stake info --mine
```

### Monitoring Commands
```bash
# Network monitoring
htcli chain info
htcli subnet list --mine
htcli node list --mine
htcli stake info --mine

# Performance monitoring
htcli node status --subnet-id 1 --node-id 5
htcli chain subnet --subnet-id 1
htcli chain node --subnet-id 1 --node-id 5
```

### Management Commands
```bash
# Subnet management
htcli subnet owner-update-name --subnet-id 1 --name "Updated Name" --key-name my-key
htcli subnet pause --subnet-id 1 --key-name my-key
htcli subnet unpause --subnet-id 1 --key-name my-key

# Node management
htcli node update --subnet-id 1 --node-id 5 --delegate-reward-rate 60000000000000000 --key-name my-key
htcli node deactivate --subnet-id 1 --node-id 5 --key-name my-key
htcli node reactivate --subnet-id 1 --node-id 5 --key-name my-key
```

## 🔄 Command Integration

### Script Integration
```bash
#!/bin/bash
# Automated portfolio management

# Check portfolio status
htcli subnet list --mine --format json
htcli node list --mine --format json
htcli stake info --mine --format json

# Perform operations based on status
if [ "$(htcli node status --subnet-id 1 --node-id 5 --format json | jq -r '.status')" != "Active" ]; then
    htcli node activate --subnet-id 1 --node-id 5 --key-name my-key
fi
```

### API Integration
```python
from src.htcli.client import HypertensorClient

client = HypertensorClient()

# Get subnet information
subnets = client.list_subnets()

# Get node information
nodes = client.list_subnet_nodes(subnet_id=1)

# Get staking information
stakes = client.get_stake_info(subnet_id=1)
```

---

**This comprehensive command tree represents the complete Hypertensor CLI functionality, providing 50+ commands across 8 categories for complete blockchain management with professional-grade user experience and strategic guidance.** 🚀
