# Hypertensor CLI Commands Documentation

This document provides comprehensive documentation for all Hypertensor CLI commands, organized by category with detailed explanations of workflows and use cases.

## 📋 **Table of Contents**

1. [Command Overview](#command-overview)
2. [General Usage Patterns](#general-usage-patterns)
3. [Configuration Commands](#configuration-commands)
4. [Subnet Commands](#subnet-commands)
5. [Node Management Commands](#node-management-commands)
6. [Staking Commands](#staking-commands)
7. [Wallet Commands](#wallet-commands)
8. [Chain Query Commands](#chain-query-commands)
9. [Command Workflows](#command-workflows)
10. [Best Practices](#best-practices)

## 🎯 **Command Overview**

The Hypertensor CLI provides **34 commands** organized into **6 logical categories** with **universal --mine filtering** for personal asset management:

| Category | Commands | Purpose |
|----------|----------|---------|
| **config** | 5 | Configuration management and setup |
| **subnet** | 5 | Subnet registration and management |
| **node** | 5 | Node lifecycle and operations |
| **stake** | 7 | Staking operations and rewards |
| **wallet** | 4 | Key management and security |
| **chain** | 8 | Blockchain queries and information |

All commands follow the consistent format:

```bash
htcli [--mine] <category> <command> [switches]
```

## 🔧 **General Usage Patterns**

### **🎯 Universal --mine Filtering**

The `--mine` flag transforms commands to show only **your assets**:

```bash
# Network-wide data (default)
htcli subnet list              # Shows ALL subnets
htcli stake info --address ... # Shows stakes for specific address

# Personal data (with --mine)
htcli --mine subnet list       # Shows ONLY your subnets
htcli --mine stake info        # Shows stakes for ALL your addresses
```

**How it works:**

1. Reads wallet keys from `~/.htcli/wallets/`
2. Filters blockchain data by ownership
3. Provides clear feedback on results

### **Consistent Switch-Based Format**

All commands use switches (no positional arguments):

```bash
# ✅ Correct format
htcli subnet register --path my-subnet --memory 1024

# ❌ Incorrect format (no positional arguments)
htcli subnet register my-subnet --memory 1024
```

### **Common Options**

Most commands support these common options:

- `--mine, -m` - Filter to show only your assets (global option)
- `--help` - Show command help
- `--format <table|json|csv>` - Output format (where applicable)
- `--guidance/--no-guidance` - Show/hide comprehensive guidance

### **Output Formats**

Commands that return data support multiple output formats:

```bash
# Table format (default, human-readable)
htcli chain network

# JSON format (for scripting and APIs)
htcli chain network --format json

# CSV format (for data analysis)
htcli chain network --format csv
```

---

## ⚙️ **Configuration Commands**

Configuration commands manage CLI settings and blockchain connection parameters.

### **Command Flow**

```
Initial Setup → Configure Settings → Validate → Use CLI
```

### **htcli config init**

**Purpose**: Interactive configuration wizard with comprehensive guidance.

**Usage**:

```bash
htcli config init [OPTIONS]
```

**Options**:

- `--config PATH` - Custom configuration file path
- `--force` - Overwrite existing configuration

**Example**:

```bash
# Interactive setup with default location
htcli config init

# Custom configuration file
htcli config init --config /path/to/my-config.yaml

# Force overwrite existing config
htcli config init --force
```

**What it does**:

1. Prompts for network settings (RPC endpoint, timeout, retries)
2. Configures output preferences (format, colors, verbosity)
3. Sets up wallet storage paths and encryption
4. Creates beautifully formatted YAML configuration
5. Provides comprehensive guidance and validation

### **htcli config show**

**Purpose**: Display current configuration in various formats.

**Usage**:

```bash
htcli config show [OPTIONS]
```

**Options**:

- `--config PATH` - Custom configuration file
- `--format <table|yaml|json>` - Output format

**Examples**:

```bash
# Show config in table format (default)
htcli config show

# Show raw YAML configuration
htcli config show --format yaml

# Show as JSON for scripting
htcli config show --format json

# Show custom config file
htcli config show --config /path/to/config.yaml
```

### **htcli config path**

**Purpose**: Display configuration file location.

**Usage**:

```bash
htcli config path [OPTIONS]
```

**Options**:

- `--config PATH` - Custom configuration file path

**Example**:

```bash
# Show default config path
htcli config path

# Show custom config path
htcli config path --config /custom/path/config.yaml
```

### **htcli config edit**

**Purpose**: Open configuration file in default editor.

**Usage**:

```bash
htcli config edit [OPTIONS]
```

**Options**:

- `--config PATH` - Custom configuration file

**Example**:

```bash
# Edit default configuration
htcli config edit

# Edit custom configuration
htcli config edit --config /path/to/config.yaml
```

**Supported Editors**: VS Code, nano, vim, vi, gedit (auto-detected)

### **htcli config validate**

**Purpose**: Validate configuration file syntax and settings.

**Usage**:

```bash
htcli config validate [OPTIONS]
```

**Options**:

- `--config PATH` - Custom configuration file

**Example**:

```bash
# Validate default configuration
htcli config validate

# Validate custom configuration
htcli config validate --config /path/to/config.yaml
```

---

## 🏗️ **Subnet Commands**

Subnet commands manage the lifecycle of subnets on the Hypertensor network.

### **Command Flow**

```
Register Subnet → Activate Subnet → Manage Nodes → Monitor Performance
```

### **htcli subnet register**

**Purpose**: Register a new subnet with comprehensive configuration.

**Usage**:

```bash
htcli subnet register [OPTIONS]
```

**Required Options**:

- `--path TEXT` - Subnet identifier/name
- `--memory INTEGER` - Memory requirement in MB
- `--blocks INTEGER` - Registration period in blocks
- `--interval INTEGER` - Entry interval in blocks

**Optional Options**:

- `--max-epochs INTEGER` - Maximum node registration epochs (default: 100)
- `--node-interval INTEGER` - Node registration interval (default: 100)
- `--activation-interval INTEGER` - Node activation interval (default: 100)
- `--queue-period INTEGER` - Node queue period (default: 100)
- `--max-penalties INTEGER` - Maximum node penalties (default: 10)
- `--whitelist TEXT` - Comma-separated coldkey whitelist
- `--guidance/--no-guidance` - Show comprehensive guidance (default: true)

**Example**:

```bash
# Register a basic subnet
htcli subnet register --path ai-training --memory 2048 --blocks 1000 --interval 100

# Register with advanced options
htcli subnet register \
  --path high-performance-compute \
  --memory 8192 \
  --blocks 2000 \
  --interval 50 \
  --max-epochs 200 \
  --max-penalties 5 \
  --whitelist 5GrwvaEF...,5HGjWAeFD...
```

**What it does**:

1. Validates all subnet parameters
2. Checks for naming conflicts
3. Composes blockchain transaction
4. Submits registration to network
5. Returns transaction hash and block number

### **htcli subnet activate**

**Purpose**: Activate a registered subnet to begin operations.

**Usage**:

```bash
htcli subnet activate [OPTIONS]
```

**Required Options**:

- `--subnet-id INTEGER` - Subnet ID to activate

**Optional Options**:

- `--guidance/--no-guidance` - Show comprehensive guidance

**Example**:

```bash
# Activate subnet with guidance
htcli subnet activate --subnet-id 1

# Activate without guidance (for scripting)
htcli subnet activate --subnet-id 1 --no-guidance
```

**What it does**:

1. Verifies subnet exists and is registered
2. Checks activation requirements
3. Submits activation transaction
4. Subnet becomes available for node registration

### **htcli subnet list**

**Purpose**: List all subnets with their status and information.

**Usage**:

```bash
htcli subnet list [OPTIONS]
```

**Options**:

- `--format <table|json>` - Output format

**Example**:

```bash
# List all subnets in table format
htcli subnet list

# Get subnet data as JSON
htcli subnet list --format json
```

**Output includes**:

- Subnet ID and path
- Status (registered, active, inactive)
- Node count and requirements
- Memory and performance metrics

### **htcli subnet info**

**Purpose**: Get detailed information about a specific subnet.

**Usage**:

```bash
htcli subnet info [OPTIONS]
```

**Required Options**:

- `--subnet-id INTEGER` - Subnet ID

**Optional Options**:

- `--format <table|json>` - Output format

**Example**:

```bash
# Get subnet information
htcli subnet info --subnet-id 1

# Get detailed JSON data
htcli subnet info --subnet-id 1 --format json
```

**Information includes**:

- Subnet configuration and parameters
- Node requirements and limits
- Current node count and status
- Performance metrics and statistics

### **htcli subnet remove**

**Purpose**: Remove a subnet from the network (destructive operation).

**Usage**:

```bash
htcli subnet remove [OPTIONS]
```

**Required Options**:

- `--subnet-id INTEGER` - Subnet ID to remove

**Optional Options**:

- `--guidance/--no-guidance` - Show comprehensive guidance

**Example**:

```bash
# Remove subnet with confirmation
htcli subnet remove --subnet-id 1
```

**What it does**:

1. Shows comprehensive warning about consequences
2. Requires user confirmation
3. Removes all associated nodes
4. Initiates unbonding for all staked tokens
5. Permanently removes subnet from network

---

## 🔗 **Node Management Commands**

Node commands handle the complete lifecycle of nodes within subnets.

### **Command Flow**

```
Add Node → Monitor Status → Manage Lifecycle → Remove/Deactivate
```

### **htcli node add**

**Purpose**: Add a node to a subnet with comprehensive configuration.

**Usage**:

```bash
htcli node add [OPTIONS]
```

**Required Options**:

- `--subnet-id INTEGER` - Subnet ID to join
- `--hotkey TEXT` - Node hotkey address
- `--peer-id TEXT` - Network peer ID
- `--stake INTEGER` - Initial stake amount (smallest units)

**Optional Options**:

- `--reward-rate FLOAT` - Delegate reward rate 0.0-1.0 (default: 0.1)
- `--key-name TEXT` - Key name for transaction signing
- `--guidance/--no-guidance` - Show comprehensive guidance

**Example**:

```bash
# Add node with minimum stake
htcli node add \
  --subnet-id 1 \
  --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY \
  --peer-id QmYwAPJzv5CZsnA625s3ofHtUyJ9eykQZ6d3s5hgcEAuSo \
  --stake 1000000000000000000

# Add node with custom reward rate
htcli node add \
  --subnet-id 1 \
  --hotkey 5GrwvaEF... \
  --peer-id QmYwAPJzv... \
  --stake 5000000000000000000 \
  --reward-rate 0.15
```

**What it does**:

1. Validates subnet exists and accepts nodes
2. Checks hotkey and peer ID formats
3. Verifies sufficient balance for staking
4. Submits node registration transaction
5. Node enters activation queue

### **htcli node remove**

**Purpose**: Remove a node from a subnet (permanent operation).

**Usage**:

```bash
htcli node remove [OPTIONS]
```

**Required Options**:

- `--subnet-id INTEGER` - Subnet ID
- `--node-id INTEGER` - Node ID to remove

**Optional Options**:

- `--key-name TEXT` - Key name for signing
- `--guidance/--no-guidance` - Show comprehensive guidance

**Example**:

```bash
# Remove node with confirmation
htcli node remove --subnet-id 1 --node-id 2

# Remove with custom signing key
htcli node remove --subnet-id 1 --node-id 2 --key-name my-key
```

**What it does**:

1. Shows warning about permanent removal
2. Requires explicit confirmation
3. Initiates unbonding of all staked tokens
4. Removes node from subnet permanently
5. Tokens become available after unbonding period

### **htcli node deactivate**

**Purpose**: Temporarily deactivate a node (reversible operation).

**Usage**:

```bash
htcli node deactivate [OPTIONS]
```

**Required Options**:

- `--subnet-id INTEGER` - Subnet ID
- `--node-id INTEGER` - Node ID to deactivate

**Optional Options**:

- `--key-name TEXT` - Key name for signing
- `--guidance/--no-guidance` - Show comprehensive guidance

**Example**:

```bash
# Deactivate node temporarily
htcli node deactivate --subnet-id 1 --node-id 2
```

**What it does**:

1. Sets node status to inactive
2. Stops participation in validation
3. Stake remains locked (no unbonding)
4. Can be reactivated later
5. Useful for maintenance or troubleshooting

### **htcli node list**

**Purpose**: List all nodes in a subnet with their status.

**Usage**:

```bash
htcli node list [OPTIONS]
```

**Required Options**:

- `--subnet-id INTEGER` - Subnet ID

**Optional Options**:

- `--format <table|json>` - Output format
- `--guidance` - Show comprehensive guidance

**Example**:

```bash
# List nodes in table format
htcli node list --subnet-id 1

# Get node data as JSON
htcli node list --subnet-id 1 --format json
```

**Output includes**:

- Node ID and hotkey
- Peer ID and network status
- Stake amount and rewards
- Node status and last activity

### **htcli node status**

**Purpose**: Get detailed status information for a specific node.

**Usage**:

```bash
htcli node status [OPTIONS]
```

**Required Options**:

- `--subnet-id INTEGER` - Subnet ID
- `--node-id INTEGER` - Node ID

**Optional Options**:

- `--format <table|json>` - Output format

**Example**:

```bash
# Get node status
htcli node status --subnet-id 1 --node-id 2

# Get detailed JSON status
htcli node status --subnet-id 1 --node-id 2 --format json
```

**Status information includes**:

- Node configuration and parameters
- Current stake and reward information
- Network connectivity status
- Performance metrics and history

---

## 💰 **Staking Commands**

Staking commands manage all aspects of token staking and rewards.

### **Command Flow**

```
Add Stake → Monitor Rewards → Manage Position → Remove/Claim
```

### **htcli stake add**

**Purpose**: Add stake to a node with comprehensive guidance.

**Usage**:

```bash
htcli stake add [OPTIONS]
```

**Required Options**:

- `--subnet-id INTEGER` - Subnet ID
- `--node-id INTEGER` - Node ID
- `--hotkey TEXT` - Hotkey address
- `--amount INTEGER` - Stake amount in smallest units

**Optional Options**:

- `--key-name TEXT` - Key name for signing
- `--guidance/--no-guidance` - Show comprehensive guidance

**Example**:

```bash
# Add stake with guidance
htcli stake add \
  --subnet-id 1 \
  --node-id 2 \
  --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY \
  --amount 1000000000000000000

# Add stake without guidance (scripting)
htcli stake add \
  --subnet-id 1 \
  --node-id 2 \
  --hotkey 5GrwvaEF... \
  --amount 1000000000000000000 \
  --no-guidance
```

**What it does**:

1. Validates node exists and accepts stake
2. Checks sufficient balance for staking
3. Locks tokens in staking contract
4. Updates stake position
5. Begins earning staking rewards

### **htcli stake remove**

**Purpose**: Remove stake from a node (initiates unbonding).

**Usage**:

```bash
htcli stake remove [OPTIONS]
```

**Required Options**:

- `--subnet-id INTEGER` - Subnet ID
- `--hotkey TEXT` - Hotkey address
- `--amount INTEGER` - Amount to remove (smallest units)

**Optional Options**:

- `--key-name TEXT` - Key name for signing
- `--guidance/--no-guidance` - Show comprehensive guidance

**Example**:

```bash
# Remove partial stake
htcli stake remove \
  --subnet-id 1 \
  --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY \
  --amount 500000000000000000
```

**What it does**:

1. Shows warning about unbonding period
2. Validates stake position exists
3. Initiates unbonding process
4. Tokens enter unbonding period
5. Stops earning rewards on unstaked amount

### **htcli stake info**

**Purpose**: Get detailed stake information and rewards.

**Usage**:

```bash
htcli stake info [OPTIONS]
```

**Required Options**:

- `--address TEXT` - Account address

**Optional Options**:

- `--subnet-id INTEGER` - Specific subnet (optional)
- `--format <table|json>` - Output format
- `--guidance` - Show comprehensive guidance

**Example**:

```bash
# Get stake info for specific subnet
htcli stake info --address 5GrwvaEF... --subnet-id 1

# Get all stake positions as JSON
htcli stake info --address 5GrwvaEF... --format json
```

**Information includes**:

- Current stake positions
- Earned rewards and rates
- Unbonding positions and timelines
- Total staked amounts across subnets

### **htcli stake claim**

**Purpose**: Claim unbonded tokens after unbonding period.

**Usage**:

```bash
htcli stake claim [OPTIONS]
```

**Required Options**:

- `--hotkey TEXT` - Hotkey address

**Optional Options**:

- `--key-name TEXT` - Key name for signing
- `--guidance/--no-guidance` - Show comprehensive guidance

**Example**:

```bash
# Claim unbonded tokens
htcli stake claim --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
```

**What it does**:

1. Checks for completed unbondings
2. Validates unbonding period is finished
3. Transfers tokens back to account
4. Tokens become freely available

### **htcli stake delegate-add**

**Purpose**: Add delegate stake to a subnet.

**Usage**:

```bash
htcli stake delegate-add [OPTIONS]
```

**Required Options**:

- `--subnet-id INTEGER` - Subnet ID
- `--amount INTEGER` - Delegate amount (smallest units)

**Optional Options**:

- `--key-name TEXT` - Key name for signing
- `--guidance/--no-guidance` - Show comprehensive guidance

**Example**:

```bash
# Add delegate stake
htcli stake delegate-add --subnet-id 1 --amount 2000000000000000000
```

### **htcli stake delegate-remove**

**Purpose**: Remove delegate stake from a subnet.

**Usage**:

```bash
htcli stake delegate-remove [OPTIONS]
```

**Required Options**:

- `--subnet-id INTEGER` - Subnet ID
- `--shares INTEGER` - Number of shares to remove

**Optional Options**:

- `--key-name TEXT` - Key name for signing
- `--guidance/--no-guidance` - Show comprehensive guidance

**Example**:

```bash
# Remove delegate shares
htcli stake delegate-remove --subnet-id 1 --shares 1000
```

### **htcli stake delegate-transfer**

**Purpose**: Transfer delegate stake between subnets.

**Usage**:

```bash
htcli stake delegate-transfer [OPTIONS]
```

**Required Options**:

- `--from-subnet INTEGER` - Source subnet ID
- `--to-subnet INTEGER` - Destination subnet ID
- `--shares INTEGER` - Number of shares to transfer

**Optional Options**:

- `--key-name TEXT` - Key name for signing
- `--guidance/--no-guidance` - Show comprehensive guidance

**Example**:

```bash
# Transfer delegate stake
htcli stake delegate-transfer --from-subnet 1 --to-subnet 2 --shares 500
```

---

## 🔑 **Wallet Commands**

Wallet commands focus exclusively on cryptographic key management and security.

### **Command Flow**

```
Generate/Import Keys → Manage Keys → Secure Storage → Use for Transactions
```

### **htcli wallet generate-key**

**Purpose**: Generate a new cryptographic keypair.

**Usage**:

```bash
htcli wallet generate-key [OPTIONS]
```

**Required Options**:

- `--name TEXT` - Key name for storage

**Optional Options**:

- `--type <sr25519|ed25519>` - Key type (default: sr25519)
- `--password TEXT` - Password for encryption
- `--guidance/--no-guidance` - Show comprehensive guidance

**Example**:

```bash
# Generate basic key
htcli wallet generate-key --name my-key

# Generate with specific type and password
htcli wallet generate-key \
  --name secure-key \
  --type ed25519 \
  --password mySecretPassword
```

**What it does**:

1. Generates cryptographically secure keypair using SubstrateInterface
2. Creates mnemonic phrase for recovery (sr25519) or secure random generation (ed25519)
3. **Always encrypts and stores** keys in `~/.htcli/wallets/` (uses default password if none provided)
4. Returns public address and confirms successful storage
5. Keys are immediately available for `--mine` filtering and staking operations

### **htcli wallet import-key**

**Purpose**: Import an existing keypair from private key.

**Usage**:

```bash
htcli wallet import-key [OPTIONS]
```

**Required Options**:

- `--name TEXT` - Key name for storage
- `--private-key TEXT` - 64-character hex private key

**Optional Options**:

- `--type <sr25519|ed25519>` - Key type (default: sr25519)
- `--password TEXT` - Password for encryption
- `--guidance/--no-guidance` - Show comprehensive guidance

**Example**:

```bash
# Import private key
htcli wallet import-key \
  --name imported-key \
  --private-key 0x1234567890abcdef... \
  --password myPassword
```

**What it does**:

1. Validates private key format (64-character hex)
2. Derives public key and SS58 address using correct crypto type constants
3. **Always encrypts and stores** keys in `~/.htcli/wallets/` (uses default password if none provided)
4. Verifies import was successful and keys are accessible
5. Keys are immediately available for `--mine` filtering and staking operations

### **htcli wallet list-keys**

**Purpose**: List all stored cryptographic keys.

**Usage**:

```bash
htcli wallet list-keys [OPTIONS]
```

**Options**:

- `--format <table|json>` - Output format

**Example**:

```bash
# List keys in table format
htcli wallet list-keys

# Get key data as JSON
htcli wallet list-keys --format json
```

**Output includes**:

- Key names and types
- Public addresses
- Creation timestamps
- Encryption status

### **htcli wallet delete-key**

**Purpose**: Delete a stored cryptographic key.

**Usage**:

```bash
htcli wallet delete-key [OPTIONS]
```

**Required Options**:

- `--name TEXT` - Key name to delete

**Optional Options**:

- `--confirm` - Skip confirmation prompt
- `--guidance/--no-guidance` - Show comprehensive guidance

**Example**:

```bash
# Delete key with confirmation
htcli wallet delete-key --name old-key

# Force delete without confirmation
htcli wallet delete-key --name old-key --confirm
```

**What it does**:

1. Shows warning about permanent deletion
2. Requires explicit confirmation
3. Securely deletes key files
4. Confirms successful deletion

---

## 🔍 **Chain Query Commands**

Chain commands provide real-time information about the blockchain state.

### **Command Flow**

```
Connect to Network → Query Information → Process Data → Display Results
```

### **htcli chain network**

**Purpose**: Get real-time network statistics.

**Usage**:

```bash
htcli chain network [OPTIONS]
```

**Options**:

- `--format <table|json>` - Output format

**Example**:

```bash
# Get network stats
htcli chain network

# Get as JSON for processing
htcli chain network --format json
```

**Information includes**:

- Total subnets and active subnets
- Total active nodes
- Total staked tokens
- Network health metrics

### **htcli chain epoch**

**Purpose**: Get current epoch information.

**Usage**:

```bash
htcli chain epoch [OPTIONS]
```

**Options**:

- `--format <table|json>` - Output format

**Example**:

```bash
# Get current epoch
htcli chain epoch

# Get epoch data as JSON
htcli chain epoch --format json
```

### **htcli chain account**

**Purpose**: Get detailed account information.

**Usage**:

```bash
htcli chain account [OPTIONS]
```

**Required Options**:

- `--address TEXT` - Account address

**Optional Options**:

- `--format <table|json>` - Output format

**Example**:

```bash
# Get account information
htcli chain account --address 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY

# Get as JSON
htcli chain account --address 5GrwvaEF... --format json
```

**Information includes**:

- Account balance and nonce
- Staking positions
- Transaction history summary
- Account metadata

### **htcli chain balance**

**Purpose**: Get account balance with 18-digit precision.

**Usage**:

```bash
htcli chain balance [OPTIONS]
```

**Required Options**:

- `--address TEXT` - Account address

**Optional Options**:

- `--format <table|json>` - Output format

**Example**:

```bash
# Get balance
htcli chain balance --address 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY

# Get balance as JSON
htcli chain balance --address 5GrwvaEF... --format json
```

**Output includes**:

- Free balance (available for transactions)
- Reserved balance (locked in operations)
- Total balance with full 18-digit precision

### **htcli chain peers**

**Purpose**: List network peers and connectivity.

**Usage**:

```bash
htcli chain peers [OPTIONS]
```

**Options**:

- `--limit INTEGER` - Maximum peers to show
- `--format <table|json>` - Output format

**Example**:

```bash
# List all peers
htcli chain peers

# Limit to 10 peers
htcli chain peers --limit 10

# Get peer data as JSON
htcli chain peers --format json
```

### **htcli chain block**

**Purpose**: Get block information by number or hash.

**Usage**:

```bash
htcli chain block [OPTIONS]
```

**Options** (one required):

- `--number INTEGER` - Block number
- `--hash TEXT` - Block hash
- `--format <table|json>` - Output format

**Example**:

```bash
# Get block by number
htcli chain block --number 12345

# Get block by hash
htcli chain block --hash 0x1234...

# Get block data as JSON
htcli chain block --number 12345 --format json
```

### **htcli chain head**

**Purpose**: Get current chain head information.

**Usage**:

```bash
htcli chain head [OPTIONS]
```

**Options**:

- `--format <table|json>` - Output format

**Example**:

```bash
# Get chain head
htcli chain head

# Get as JSON
htcli chain head --format json
```

### **htcli chain runtime-version**

**Purpose**: Get blockchain runtime version information.

**Usage**:

```bash
htcli chain runtime-version [OPTIONS]
```

**Options**:

- `--format <table|json>` - Output format

**Example**:

```bash
# Get runtime version
htcli chain runtime-version

# Get as JSON
htcli chain runtime-version --format json
```

---

## 🔄 **Command Workflows**

### **Complete Subnet Setup Workflow**

```bash
# 1. Configure CLI
htcli config init

# 2. Generate keys
htcli wallet generate-key --name subnet-owner

# 3. Check balance
htcli chain balance --address <your-address>

# 4. Register subnet
htcli subnet register --path ai-compute --memory 4096 --blocks 1000 --interval 100

# 5. Activate subnet
htcli subnet activate --subnet-id 1

# 6. Add node to subnet
htcli node add --subnet-id 1 --hotkey <hotkey> --peer-id <peer-id> --stake 1000000000000000000

# 7. Monitor node status
htcli node status --subnet-id 1 --node-id 1
```

### **Staking Management Workflow**

```bash
# 1. Check current stake positions
htcli stake info --address <your-address>

# 2. Add stake to promising node
htcli stake add --subnet-id 1 --node-id 2 --hotkey <hotkey> --amount 2000000000000000000

# 3. Monitor performance and rewards
htcli stake info --address <your-address> --subnet-id 1

# 4. Remove underperforming stake
htcli stake remove --subnet-id 1 --hotkey <hotkey> --amount 1000000000000000000

# 5. Claim unbonded tokens when ready
htcli stake claim --hotkey <hotkey>
```

### **Network Monitoring Workflow**

```bash
# 1. Check overall network health
htcli chain network

# 2. Monitor specific subnet
htcli subnet info --subnet-id 1

# 3. Check node performance
htcli node list --subnet-id 1

# 4. Verify account status
htcli chain account --address <your-address>

# 5. Check current epoch and timing
htcli chain epoch
```

---

## 💡 **Best Practices**

### **Security Best Practices**

1. **Use strong passwords** for key encryption
2. **Backup mnemonic phrases** securely
3. **Use separate keys** for different purposes
4. **Validate addresses** before transactions
5. **Use confirmation prompts** for destructive operations

### **Operational Best Practices**

1. **Start with configuration**: Always run `htcli config init` first
2. **Use guidance mode**: Keep `--guidance` enabled for complex operations
3. **Monitor regularly**: Check stake positions and node status frequently
4. **Batch operations**: Use JSON output for scripting multiple operations
5. **Test with small amounts**: Start with minimal stakes before scaling

### **Performance Best Practices**

1. **Use JSON format** for programmatic access
2. **Cache configuration**: Use custom config files for different environments
3. **Limit output**: Use `--limit` options for large datasets
4. **Monitor network**: Check `htcli chain network` for network health
5. **Plan unbonding**: Account for unbonding periods in staking strategies

### **Troubleshooting Best Practices**

1. **Check connectivity**: Use `htcli chain network` to verify connection
2. **Validate configuration**: Run `htcli config validate` regularly
3. **Use verbose mode**: Add `--verbose` for detailed error information
4. **Check balances**: Verify sufficient funds before transactions
5. **Read error messages**: CLI provides detailed error guidance

---

This completes the comprehensive command documentation for the Hypertensor CLI. Each command includes detailed usage information, examples, and workflow guidance to help users effectively interact with the Hypertensor blockchain network.
