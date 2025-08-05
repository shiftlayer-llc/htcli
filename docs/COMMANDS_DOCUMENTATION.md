# HTCLI Commands Documentation

This document provides comprehensive documentation for all available commands in the HTCLI (Hypertensor Command Line Interface) application.

## Table of Contents

1. [Overview](#overview)
2. [Command Structure](#command-structure)
3. [Subnet Commands](#subnet-commands)
4. [Wallet Commands](#wallet-commands)
5. [Chain Commands](#chain-commands)
6. [Global Options](#global-options)
7. [Examples](#examples)

## Overview

HTCLI is a command-line interface for interacting with the Hypertensor blockchain. It provides commands for managing subnets, wallets, and querying blockchain information.

## Command Structure

The CLI follows a hierarchical structure:
```
htcli <command-group> <subcommand> [options] [arguments]
```

### Command Groups
- `subnet`: Subnet management operations
- `wallet`: Wallet and key management operations
- `chain`: Blockchain query operations

## Subnet Commands

### `htcli subnet register`

**Purpose**: Register new subnets on the Hypertensor blockchain

**Subcommands**:
- `create`: Create a new subnet
- `activate`: Activate an existing subnet

#### `htcli subnet register create`

**Description**: Register a new subnet with the specified parameters

**Arguments**:
- `path`: Subnet path (required)
- `--memory-mb`: Memory allocation in MB (required)
- `--registration-blocks`: Number of registration blocks (required)
- `--entry-interval`: Entry interval (required)
- `--max-node-registration-epochs`: Maximum node registration epochs (required)
- `--node-registration-interval`: Node registration interval (required)
- `--node-activation-interval`: Node activation interval (required)
- `--node-queue-period`: Node queue period (required)
- `--max-node-penalties`: Maximum node penalties (required)
- `--coldkey-whitelist`: Coldkey whitelist (optional, default: [])

**Example**:
```bash
htcli subnet register create /test/subnet \
  --memory-mb 1024 \
  --registration-blocks 1000 \
  --entry-interval 100 \
  --max-node-registration-epochs 50 \
  --node-registration-interval 20 \
  --node-activation-interval 30 \
  --node-queue-period 40 \
  --max-node-penalties 5
```

#### `htcli subnet register activate`

**Description**: Activate an existing subnet

**Arguments**:
- `subnet-id`: Subnet ID to activate (required)

**Example**:
```bash
htcli subnet register activate 1
```

### `htcli subnet manage`

**Purpose**: Manage existing subnets

**Subcommands**:
- `list`: List all subnets
- `info`: Get information about a specific subnet

#### `htcli subnet manage list`

**Description**: List all registered subnets

**Options**:
- `--format`: Output format (table, json, csv)
- `--verbose`: Verbose output

**Example**:
```bash
htcli subnet manage list --format json
```

#### `htcli subnet manage info`

**Description**: Get detailed information about a specific subnet

**Arguments**:
- `subnet-id`: Subnet ID (required)

**Example**:
```bash
htcli subnet manage info 1
```

### `htcli subnet nodes`

**Purpose**: Manage subnet nodes

**Subcommands**:
- `add`: Add a node to a subnet
- `list`: List nodes in a subnet

#### `htcli subnet nodes add`

**Description**: Add a node to a subnet

**Arguments**:
- `subnet-id`: Subnet ID (required)
- `--peer-id`: Peer ID (required)
- `--hotkey`: Hotkey address (required)
- `--delegate-reward-rate`: Delegate reward rate (required)
- `--stake-to-be-added`: Stake amount to add (required)

**Example**:
```bash
htcli subnet nodes add 1 \
  --peer-id "QmTestPeerId123456789" \
  --hotkey "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY" \
  --delegate-reward-rate 1000 \
  --stake-to-be-added 1000000000000
```

#### `htcli subnet nodes list`

**Description**: List all nodes in a subnet

**Arguments**:
- `subnet-id`: Subnet ID (required)

**Example**:
```bash
htcli subnet nodes list 1
```

## Wallet Commands

### `htcli wallet keys`

**Purpose**: Manage cryptographic keys

**Subcommands**:
- `generate`: Generate a new keypair
- `list`: List all keys
- `import-key`: Import a key from private key
- `delete`: Delete a key

#### `htcli wallet keys generate`

**Description**: Generate a new cryptographic keypair

**Arguments**:
- `name`: Key name (required)
- `--type`: Key type (sr25519, ed25519) (default: sr25519)
- `--path`: Wallet directory path (optional)

**Example**:
```bash
htcli wallet keys generate my-key --type sr25519
```

#### `htcli wallet keys list`

**Description**: List all available keys

**Options**:
- `--path`: Wallet directory path (optional)
- `--format`: Output format (table, json, csv)

**Example**:
```bash
htcli wallet keys list --format json
```

#### `htcli wallet keys import-key`

**Description**: Import a key from private key

**Arguments**:
- `name`: Key name (required)
- `private-key`: Private key in hex format (required)
- `--type`: Key type (sr25519, ed25519) (default: sr25519)
- `--path`: Wallet directory path (optional)

**Example**:
```bash
htcli wallet keys import-key my-imported-key \
  0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef \
  --type sr25519
```

#### `htcli wallet keys delete`

**Description**: Delete a key

**Arguments**:
- `name`: Key name to delete (required)
- `--path`: Wallet directory path (optional)
- `--force`: Force deletion without confirmation

**Example**:
```bash
htcli wallet keys delete my-key --force
```

### `htcli wallet stake`

**Purpose**: Manage staking operations

**Subcommands**:
- `add`: Add stake to a subnet node
- `remove`: Remove stake from a subnet
- `info`: Get staking information

#### `htcli wallet stake add`

**Description**: Add stake to a subnet node

**Arguments**:
- `subnet-id`: Subnet ID (required)
- `node-id`: Node ID (required)
- `--hotkey`: Hotkey address (required)
- `--amount`: Stake amount to add (required)

**Example**:
```bash
htcli wallet stake add 1 1 \
  --hotkey "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY" \
  --amount 1000000000000
```

#### `htcli wallet stake remove`

**Description**: Remove stake from a subnet

**Arguments**:
- `subnet-id`: Subnet ID (required)
- `--hotkey`: Hotkey address (required)
- `--amount`: Stake amount to remove (required)

**Example**:
```bash
htcli wallet stake remove 1 \
  --hotkey "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY" \
  --amount 500000000000
```

#### `htcli wallet stake info`

**Description**: Get staking information for an account

**Arguments**:
- `address`: Account address (required)
- `subnet-id`: Subnet ID (required)

**Example**:
```bash
htcli wallet stake info "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY" 1
```

## Chain Commands

### `htcli chain info`

**Purpose**: Get blockchain information

**Subcommands**:
- `network`: Get network statistics
- `account`: Get account information
- `epoch`: Get current epoch information

#### `htcli chain info network`

**Description**: Get network statistics

**Options**:
- `--format`: Output format (table, json, csv)
- `--verbose`: Verbose output

**Example**:
```bash
htcli chain info network --format json
```

#### `htcli chain info account`

**Description**: Get account information

**Arguments**:
- `address`: Account address (required)

**Options**:
- `--format`: Output format (table, json, csv)

**Example**:
```bash
htcli chain info account "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
```

#### `htcli chain info epoch`

**Description**: Get current epoch information

**Options**:
- `--format`: Output format (table, json, csv)

**Example**:
```bash
htcli chain info epoch
```

### `htcli chain query`

**Purpose**: Query blockchain data

**Subcommands**:
- `balance`: Get account balance
- `peers`: Get network peers
- `block`: Get block information

#### `htcli chain query balance`

**Description**: Get account balance

**Arguments**:
- `address`: Account address (required)

**Options**:
- `--format`: Output format (table, json, csv)

**Example**:
```bash
htcli chain query balance "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
```

#### `htcli chain query peers`

**Description**: Get network peers

**Options**:
- `--format`: Output format (table, json, csv)

**Example**:
```bash
htcli chain query peers
```

#### `htcli chain query block`

**Description**: Get block information

**Arguments**:
- `block-number`: Block number (optional, defaults to latest)

**Options**:
- `--format`: Output format (table, json, csv)

**Example**:
```bash
htcli chain query block 12345
```

## Global Options

All commands support these global options:

- `--help, -h`: Show help message
- `--version`: Show version information
- `--config`: Configuration file path
- `--endpoint`: Blockchain RPC endpoint
- `--verbose`: Enable verbose output
- `--format`: Output format (table, json, csv)
- `--color`: Enable/disable colored output

## Examples

### Complete Subnet Workflow

```bash
# 1. Register a new subnet
htcli subnet register create /my-subnet \
  --memory-mb 1024 \
  --registration-blocks 1000 \
  --entry-interval 100 \
  --max-node-registration-epochs 50 \
  --node-registration-interval 20 \
  --node-activation-interval 30 \
  --node-queue-period 40 \
  --max-node-penalties 5

# 2. Add a node to the subnet
htcli subnet nodes add 1 \
  --peer-id "QmMyPeerId123456789" \
  --hotkey "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY" \
  --delegate-reward-rate 1000 \
  --stake-to-be-added 1000000000000

# 3. Activate the subnet
htcli subnet register activate 1

# 4. Check subnet status
htcli subnet manage info 1
```

### Wallet Management Workflow

```bash
# 1. Generate a new keypair
htcli wallet keys generate my-key --type sr25519

# 2. List all keys
htcli wallet keys list

# 3. Add stake to a subnet node
htcli wallet stake add 1 1 \
  --hotkey "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY" \
  --amount 1000000000000

# 4. Check staking information
htcli wallet stake info "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY" 1
```

### Blockchain Query Workflow

```bash
# 1. Get network statistics
htcli chain info network

# 2. Get account balance
htcli chain query balance "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"

# 3. Get current epoch
htcli chain info epoch

# 4. Get latest block information
htcli chain query block
```

## Error Handling

The CLI provides comprehensive error handling:

- **Validation Errors**: Invalid input parameters
- **Network Errors**: Connection issues with blockchain
- **Resource Errors**: Missing subnets, accounts, etc.
- **Permission Errors**: Insufficient permissions for operations

All errors include:
- Clear error messages
- Suggested solutions
- Error codes for programmatic handling

## Output Formats

All commands support multiple output formats:

- **Table** (default): Human-readable tabular format
- **JSON**: Machine-readable JSON format
- **CSV**: Comma-separated values format

Example:
```bash
# Table format (default)
htcli chain info network

# JSON format
htcli chain info network --format json

# CSV format
htcli chain info network --format csv
```

## Configuration

The CLI can be configured using:

1. **Environment Variables**:
   ```bash
   export HTCLI_NETWORK_ENDPOINT="wss://hypertensor.duckdns.org"
   export HTCLI_OUTPUT_FORMAT="json"
   ```

2. **Configuration File**:
   ```yaml
   network:
     endpoint: "wss://hypertensor.duckdns.org"
     timeout: 30
   output:
     format: "table"
     verbose: false
   ```

3. **Command Line Options**:
   ```bash
   htcli --endpoint "wss://custom.endpoint:9944" --format json
   ```
