# Hypertensor CLI Commands Reference

Complete reference for all Hypertensor CLI commands with comprehensive examples and usage patterns.

## 📋 Command Overview

The Hypertensor CLI provides **50+ commands** across **8 categories** for complete blockchain management:

- **Configuration Management** (5 commands) - Setup and manage CLI configuration
- **Subnet Operations** (15 commands) - Complete subnet lifecycle management
- **Node Management** (10 commands) - Complete node lifecycle management
- **Staking Operations** (12 commands) - Comprehensive staking and delegation
- **Wallet & Key Management** (6 commands) - Generate and manage cryptographic keys
- **Chain Queries** (8 commands) - Query blockchain information
- **Automated Flows** (3 commands) - Multi-step automated workflows
- **Personal Asset Filtering** - Universal `--mine` flag across all commands

## 🎯 Universal --mine Filtering

**NEW**: The `--mine` flag works across all commands to filter results to show only your assets:

```bash
# View only your subnets
htcli subnet list --mine

# View only your stakes
htcli stake info --mine

# View only your nodes
htcli node list --mine

# Works with any command that returns asset lists
htcli subnet info --subnet-id 1 --mine
htcli node status --subnet-id 1 --node-id 5 --mine
```

## 🔧 Configuration Management

### Initialize Configuration

```bash
htcli config init
```

Interactive configuration wizard for initial setup.

### View Configuration

```bash
htcli config show
```

Display current configuration settings.

### Edit Configuration

```bash
htcli config edit
```

Interactive configuration editor within terminal.

### Set Configuration Value

```bash
htcli config set network.endpoint wss://testnet.hypertensor.ai
```

Set specific configuration values.

### Get Configuration Value

```bash
htcli config get network.endpoint
```

Retrieve specific configuration values.

## 🔑 Subnet Operations

### Register Subnet

```bash
htcli subnet register \
  --name "My AI Subnet" \
  --repo "https://github.com/my/ai-subnet" \
  --description "Advanced AI computation subnet" \
  --min-stake 1000000000000000000 \
  --max-stake 10000000000000000000 \
  --churn-limit 4 \
  --registration-epochs 10 \
  --activation-grace-epochs 5 \
  --idle-epochs 3 \
  --included-epochs 2 \
  --max-penalties 3 \
  --key-name my-subnet-key
```

Register a new subnet with comprehensive parameters.

### Activate Subnet

```bash
htcli subnet activate --subnet-id 1 --key-name my-subnet-key
```

Activate a registered subnet (requires minimum nodes and delegate stake).

### Pause Subnet

```bash
htcli subnet pause --subnet-id 1 --key-name my-subnet-key
```

Temporarily pause subnet operations.

### Unpause Subnet

```bash
htcli subnet unpause --subnet-id 1 --key-name my-subnet-key
```

Resume paused subnet operations.

### List Subnets

```bash
htcli subnet list --format table --limit 10
```

List all subnets with optional filtering and formatting.

### Get Subnet Info

```bash
htcli subnet info --subnet-id 1 --format table
```

Get detailed information about a specific subnet.

### Update Subnet Name

```bash
htcli subnet owner-update-name --subnet-id 1 --name "Updated Subnet Name" --key-name my-subnet-key
```

Update subnet name (owner only).

### Update Subnet Repository

```bash
htcli subnet owner-update-repo --subnet-id 1 --repo "https://github.com/my/updated-subnet" --key-name my-subnet-key
```

Update subnet repository URL (owner only).

### Update Subnet Description

```bash
htcli subnet owner-update-description --subnet-id 1 --description "Updated description" --key-name my-subnet-key
```

Update subnet description (owner only).

### Update Churn Limit

```bash
htcli subnet owner-update-churn-limit --subnet-id 1 --churn-limit 6 --key-name my-subnet-key
```

Update subnet churn limit (owner only).

### Update Min Stake

```bash
htcli subnet owner-update-min-stake --subnet-id 1 --min-stake 2000000000000000000 --key-name my-subnet-key
```

Update minimum stake requirement (owner only).

### Update Max Stake

```bash
htcli subnet owner-update-max-stake --subnet-id 1 --max-stake 20000000000000000000 --key-name my-subnet-key
```

Update maximum stake limit (owner only).

### Transfer Ownership

```bash
htcli subnet owner-transfer-ownership --subnet-id 1 --new-owner 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu --key-name my-subnet-key
```

Transfer subnet ownership to another account.

### Accept Ownership

```bash
htcli subnet owner-accept-ownership --subnet-id 1 --key-name new-owner-key
```

Accept transferred subnet ownership.

### Undo Ownership Transfer

```bash
htcli subnet owner-undo-transfer --subnet-id 1 --key-name my-subnet-key
```

Undo a pending ownership transfer.

## 🔗 Node Management

### Register Node

```bash
htcli node register \
  --subnet-id 1 \
  --hotkey 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu \
  --peer-id 12D3KooWABC123DEF456 \
  --bootnode-peer-id 12D3KooWXYZ789GHI012 \
  --client-peer-id 12D3KooWJKL345MNO678 \
  --stake 1000000000000000000 \
  --reward-rate 50000000000000000 \
  --bootnode /ip4/127.0.0.1/tcp/30333/p2p/12D3KooWABC123DEF456 \
  --key-name my-node-key
```

Register a new node with comprehensive parameters.

### Activate Node

```bash
htcli node activate --subnet-id 1 --node-id 5 --key-name my-node-key
```

Activate a registered node within its time window.

### Update Delegate Reward Rate

```bash
htcli node update --subnet-id 1 --node-id 5 --delegate-reward-rate 60000000000000000 --key-name my-node-key
```

Update node's delegate reward rate (1% decrease per 24 hours, unlimited increases).

### Update Coldkey

```bash
htcli node update-coldkey --subnet-id 1 --node-id 5 --new-coldkey 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu --key-name my-node-key
```

Update node's coldkey (requires current hotkey signature).

### Update Hotkey

```bash
htcli node update-hotkey --subnet-id 1 --node-id 5 --new-hotkey 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu --key-name my-node-key
```

Update node's hotkey (requires current coldkey signature).

### Deactivate Node

```bash
htcli node deactivate --subnet-id 1 --node-id 5 --key-name my-node-key
```

Temporarily deactivate a node (validators only).

### Reactivate Node

```bash
htcli node reactivate --subnet-id 1 --node-id 5 --key-name my-node-key
```

Reactivate a deactivated node within time limits.

### Remove Node

```bash
# Remove with automatic stake removal
htcli node remove --subnet-id 1 --node-id 5 --remove-stake --key-name my-node-key

# Remove without automatic stake removal
htcli node remove --subnet-id 1 --node-id 5 --key-name my-node-key
```

Remove a node with beautiful stake management options.

### Cleanup Expired Nodes

```bash
htcli node cleanup-expired --subnet-id 1 --node-id 5 --cleanup-type deactivated --key-name my-node-key
```

Clean up expired registered or deactivated nodes.

### Get Node Status

```bash
htcli node status --subnet-id 1 --node-id 5 --format table
```

Get detailed node status and classification information.

### List Nodes

```bash
htcli node list --subnet-id 1 --format table --limit 10
```

List nodes in a subnet with optional filtering.

## 💰 Staking Operations

### Subnet Delegate Staking

#### Add Subnet Delegate Stake

```bash
htcli stake delegate-add --subnet-id 1 --amount 1000000000000000000 --key-name my-staking-key
```

Add stake to subnet delegate pool.

#### Remove Subnet Delegate Stake

```bash
htcli stake delegate-remove --subnet-id 1 --shares 500000000000000000 --key-name my-staking-key
```

Remove stake shares from subnet delegate pool.

#### Transfer Subnet Delegate Stake

```bash
htcli stake delegate-transfer --subnet-id 1 --to-account 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu --shares 100000000000000000 --key-name my-staking-key
```

Transfer subnet delegate stake shares to another account.

#### Increase Subnet Delegate Stake Pool

```bash
htcli stake delegate-increase --subnet-id 1 --amount 500000000000000000 --key-name my-staking-key
```

Increase subnet delegate stake pool (airdrop rewards).

### Node Delegate Staking

#### Add Node Delegate Stake

```bash
htcli stake node-add --subnet-id 1 --node-id 5 --amount 1000000000000000000 --key-name my-staking-key
```

Add stake to specific node.

#### Remove Node Delegate Stake

```bash
htcli stake node-remove --subnet-id 1 --node-id 5 --shares 500000000000000000 --key-name my-staking-key
```

Remove stake shares from specific node.

#### Transfer Node Delegate Stake

```bash
htcli stake node-transfer --subnet-id 1 --node-id 5 --to-account 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu --shares 100000000000000000 --key-name my-staking-key
```

Transfer node delegate stake shares to another account.

#### Increase Node Delegate Stake Pool

```bash
htcli stake node-increase --subnet-id 1 --node-id 5 --amount 500000000000000000 --key-name my-staking-key
```

Increase node delegate stake pool (airdrop rewards).

### Legacy Staking (Deprecated)

#### Add Stake

```bash
htcli stake add --subnet-id 1 --node-id 5 --amount 1000000000000000000 --key-name my-staking-key
```

Add stake to a specific node (legacy command).

#### Remove Stake

```bash
htcli stake remove --subnet-id 1 --node-id 5 --amount 500000000000000000 --key-name my-staking-key
```

Remove stake from a specific node (legacy command).

#### Get Staking Info

```bash
htcli stake info --subnet-id 1 --node-id 5 --format table
```

Get staking information (supports --mine flag).

## 🔐 Wallet & Key Management

### Generate Key

```bash
htcli wallet generate-key --name my-key --crypto-type sr25519
```

Generate a new cryptographic keypair.

### Generate Hotkey

```bash
htcli wallet generate-hotkey --name my-hotkey --crypto-type sr25519
```

Generate a hotkey specifically for node operations.

### Import Key

```bash
htcli wallet import-key --name imported-key --private-key 0x1234567890abcdef... --crypto-type sr25519
```

Import an existing private key.

### List Keys

```bash
htcli wallet list-keys --format table
```

List all stored keys.

### Get Wallet Status

```bash
htcli wallet status --key-name my-key
```

Get detailed wallet status and key information.

### Delete Key

```bash
htcli wallet delete-key --name my-key
```

Delete a stored key (with confirmation).

## 🔍 Chain Queries

### Get Network Info

```bash
htcli chain info --format table
```

Get comprehensive network information.

### Get Balance

```bash
htcli chain balance --address 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu --format table
```

Get account balance.

### Get Block Info

```bash
htcli chain block --block-number 12345 --format table
```

Get block information.

### Get Transaction Info

```bash
htcli chain transaction --hash 0x1234567890abcdef... --format table
```

Get transaction information.

### Get Network Stats

```bash
htcli chain network --format table
```

Get network statistics.

### Get Subnet Stats

```bash
htcli chain subnet --subnet-id 1 --format table
```

Get subnet statistics.

### Get Node Stats

```bash
htcli chain node --subnet-id 1 --node-id 5 --format table
```

Get node statistics.

### Get Stake Stats

```bash
htcli chain stake --subnet-id 1 --format table
```

Get staking statistics.

## 🔄 Automated Flows

### List Available Flows

```bash
htcli flow list --format table
```

List all available automated workflows.

### Get Flow Information

```bash
htcli flow info subnet-deployment --format table
```

Get detailed information about a specific flow.

### Run Automated Flow

```bash
htcli flow run subnet-deployment --interactive
```

Run an automated workflow with interactive prompts.

## 📊 General Usage Patterns

### Command Structure

All commands follow a consistent pattern:

```bash
htcli <category> <command> [options] [arguments]
```

### Common Options

Most commands support these common options:

- `--format <format>` - Output format (table, json, csv)
- `--limit <number>` - Limit number of results
- `--mine` - Filter to show only your assets
- `--guidance/--no-guidance` - Show/hide comprehensive guidance
- `--help` - Show command help

### Output Formats

```bash
# Table format (default)
htcli subnet list --format table

# JSON format
htcli subnet list --format json

# CSV format
htcli subnet list --format csv
```

### Personal Asset Filtering

```bash
# View only your subnets
htcli subnet list --mine

# View only your stakes
htcli stake info --mine

# View only your nodes
htcli node list --mine
```

## 🎯 Advanced Usage Examples

### Complete Node Lifecycle

```bash
# 1. Register node
htcli node register --subnet-id 1 --hotkey <hotkey> --peer-id <peer-id> --stake 1000000000000000000 --key-name my-node-key

# 2. Activate node
htcli node activate --subnet-id 1 --node-id <node-id> --key-name my-node-key

# 3. Update reward rate
htcli node update --subnet-id 1 --node-id <node-id> --delegate-reward-rate 50000000000000000 --key-name my-node-key

# 4. Monitor status
htcli node status --subnet-id 1 --node-id <node-id>

# 5. Deactivate temporarily
htcli node deactivate --subnet-id 1 --node-id <node-id> --key-name my-node-key

# 6. Reactivate
htcli node reactivate --subnet-id 1 --node-id <node-id> --key-name my-node-key

# 7. Remove with automatic stake removal
htcli node remove --subnet-id 1 --node-id <node-id> --remove-stake --key-name my-node-key
```

### Complete Staking Portfolio

```bash
# 1. Add subnet delegate stake
htcli stake delegate-add --subnet-id 1 --amount 1000000000000000000 --key-name my-staking-key

# 2. Add node delegate stake
htcli stake node-add --subnet-id 1 --node-id 5 --amount 500000000000000000 --key-name my-staking-key

# 3. Diversify to another subnet
htcli stake delegate-add --subnet-id 2 --amount 500000000000000000 --key-name my-staking-key

# 4. Monitor portfolio
htcli stake info --mine

# 5. Transfer some stake
htcli stake node-transfer --subnet-id 1 --node-id 5 --to-account <recipient> --shares 100000000000000000 --key-name my-staking-key

# 6. Remove some stake
htcli stake delegate-remove --subnet-id 1 --shares 200000000000000000 --key-name my-staking-key
```

### Complete Subnet Management

```bash
# 1. Register subnet
htcli subnet register --name "My Subnet" --repo "https://github.com/my/subnet" --description "A great subnet" --key-name my-subnet-key

# 2. Activate subnet
htcli subnet activate --subnet-id <subnet-id> --key-name my-subnet-key

# 3. Update parameters
htcli subnet owner-update-name --subnet-id <subnet-id> --name "Updated Name" --key-name my-subnet-key
htcli subnet owner-update-repo --subnet-id <subnet-id> --repo "https://github.com/my/updated-subnet" --key-name my-subnet-key

# 4. Pause for maintenance
htcli subnet pause --subnet-id <subnet-id> --key-name my-subnet-key

# 5. Resume operations
htcli subnet unpause --subnet-id <subnet-id> --key-name my-subnet-key

# 6. Transfer ownership
htcli subnet owner-transfer-ownership --subnet-id <subnet-id> --new-owner <new-owner> --key-name my-subnet-key
```

## 🛡️ Safety Features

### Confirmation Prompts

Critical operations require confirmation:

```bash
htcli node remove --subnet-id 1 --node-id 5 --key-name my-node-key
# Prompts: "Are you sure you want to remove this node?"
```

### Validation

All inputs are validated:

- Subnet IDs must be positive integers
- Node IDs must be positive integers
- Addresses must be valid SS58 format
- Amounts must be positive integers
- Key names must be valid

### Error Handling

Comprehensive error handling with clear messages:

```bash
htcli node activate --subnet-id 999 --node-id 999 --key-name my-node-key
# Error: "❌ Subnet 999 does not exist"
```

## 📈 Performance Tips

### Efficient Queries

```bash
# Use --limit to reduce data transfer
htcli subnet list --limit 5

# Use --format json for programmatic processing
htcli node list --subnet-id 1 --format json

# Use --mine for personal asset filtering
htcli stake info --mine
```

### Batch Operations

```bash
# Use scripts for batch operations
for subnet_id in {1..5}; do
  htcli subnet info --subnet-id $subnet_id --format json
done
```

### Monitoring

```bash
# Regular status checks
htcli node status --subnet-id 1 --node-id 5
htcli stake info --mine
htcli chain info
```

---

**This comprehensive command reference covers all 50+ commands available in the Hypertensor CLI, providing complete blockchain management capabilities with professional-grade user experience and strategic guidance.** 🚀
