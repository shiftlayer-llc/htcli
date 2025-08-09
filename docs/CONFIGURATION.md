# Hypertensor CLI Configuration Guide

This guide covers all aspects of configuring the Hypertensor CLI for optimal performance and usability.

## 📋 **Table of Contents**

1. [Configuration Overview](#configuration-overview)
2. [Configuration File Structure](#configuration-file-structure)
3. [Interactive Configuration](#interactive-configuration)
4. [Environment Variables](#environment-variables)
5. [Custom Configuration Files](#custom-configuration-files)
6. [Network Configuration](#network-configuration)
7. [Output Configuration](#output-configuration)
8. [Wallet Configuration](#wallet-configuration)
9. [Advanced Configuration](#advanced-configuration)
10. [Troubleshooting](#troubleshooting)

## 🎯 **Configuration Overview**

The Hypertensor CLI uses a hierarchical configuration system that supports:

- **YAML configuration files** with comments and structure
- **Environment variables** for overrides
- **Command-line options** for temporary changes
- **Interactive configuration wizard** for easy setup
- **🆕 Personal asset filtering** with universal --mine flag support

### **Configuration Priority**

1. Command-line options (highest priority)
2. Environment variables
3. Configuration file
4. Default values (lowest priority)

### **Default Configuration Location**

```
~/.htcli/config.yaml
```

## 📄 **Configuration File Structure**

The configuration file is organized into three main sections:

```yaml
# Hypertensor CLI Configuration
# This file contains the configuration settings for the Hypertensor CLI tool.
# You can edit this file directly or use 'htcli config init' to regenerate it.

# Network Configuration
# Settings for connecting to the Hypertensor blockchain network
network:
  # RPC endpoint for blockchain communication
  endpoint: "wss://hypertensor.duckdns.org"

  # WebSocket endpoint for real-time communication
  ws_endpoint: "wss://hypertensor.duckdns.org"

  # Connection timeout in seconds
  timeout: 30

  # Number of retry attempts for failed connections
  retry_attempts: 3

# Output Configuration
# Settings for CLI output formatting and display
output:
  # Default output format (table, json, csv)
  format: "table"

  # Enable verbose output with detailed information
  verbose: false

  # Enable colored output in terminal
  color: true

# Wallet Configuration
# Settings for wallet and key management
wallet:
  # Path where wallets and keys are stored
  path: "~/.htcli/wallets"

  # Default wallet name to use
  default_name: "default"

  # Enable wallet encryption for security
  encryption_enabled: true

# Personal Asset Filtering Configuration
# Settings for the universal --mine filtering system
filter:
  # Default behavior for --mine flag (can be overridden per command)
  mine: false
```

## 🛠️ **Interactive Configuration**

### **Initial Setup**

The easiest way to configure the CLI is using the interactive wizard:

```bash
htcli config init
```

This will guide you through:

1. **Network Settings**
   - RPC endpoint selection
   - Connection timeout preferences
   - Retry attempt configuration

2. **Output Preferences**
   - Default output format
   - Verbose mode settings
   - Color output preferences

3. **Wallet Configuration**
   - Key storage location
   - Default wallet name
   - Encryption preferences

### **Configuration Wizard Features**

#### **Rich Interactive Interface**

```
╭───────────────────────── Welcome ──────────────────────────────╮
│ 🚀 Hypertensor CLI Configuration Setup                        │
│                                                               │
│ This wizard will help you configure the Hypertensor CLI.      │
│ Press Enter to use default values or type your preferences.   │
╰───────────────────────────────────────────────────────────────╯
```

#### **Step-by-Step Guidance**

- **Network Configuration**: Blockchain connection settings
- **Output Configuration**: Display and formatting preferences
- **Wallet Configuration**: Security and storage settings

#### **Validation and Confirmation**

- Real-time input validation
- Configuration summary before saving
- Confirmation prompts for safety

### **Updating Existing Configuration**

```bash
# Update existing configuration
htcli config init

# Force overwrite existing configuration
htcli config init --force

# Use custom configuration file
htcli config init --config /path/to/custom-config.yaml
```

## 🌍 **Environment Variables**

Override configuration settings using environment variables:

### **Network Environment Variables**

```bash
export HTCLI_NETWORK_ENDPOINT="wss://custom-endpoint.com"
export HTCLI_NETWORK_WS_ENDPOINT="wss://custom-ws-endpoint.com"
export HTCLI_NETWORK_TIMEOUT="60"
export HTCLI_NETWORK_RETRY_ATTEMPTS="5"
```

### **Output Environment Variables**

```bash
export HTCLI_OUTPUT_FORMAT="json"
export HTCLI_OUTPUT_VERBOSE="true"
export HTCLI_OUTPUT_COLOR="false"
```

### **Wallet Environment Variables**

```bash
export HTCLI_WALLET_PATH="/custom/wallet/path"
export HTCLI_WALLET_DEFAULT_NAME="production"
export HTCLI_WALLET_ENCRYPTION_ENABLED="true"
```

### **Using Environment Variables**

```bash
# Set environment variables for session
export HTCLI_OUTPUT_FORMAT="json"
htcli chain network  # Will output JSON

# Set for single command
HTCLI_OUTPUT_FORMAT="json" htcli chain network

# Use in scripts
#!/bin/bash
export HTCLI_NETWORK_ENDPOINT="wss://testnet.endpoint.com"
export HTCLI_OUTPUT_FORMAT="json"
htcli chain network | jq '.total_subnets'
```

## 📁 **Custom Configuration Files**

### **Creating Custom Configurations**

```bash
# Create configuration for different environments
htcli config init --config ~/.htcli/testnet-config.yaml
htcli config init --config ~/.htcli/mainnet-config.yaml
htcli config init --config ~/.htcli/development-config.yaml
```

### **Using Custom Configurations**

```bash
# Use specific configuration file
htcli --config ~/.htcli/testnet-config.yaml chain network

# Set as environment variable
export HTCLI_CONFIG_FILE="~/.htcli/testnet-config.yaml"
htcli chain network

# Use in scripts
CONFIG_FILE="~/.htcli/production-config.yaml"
htcli --config $CONFIG_FILE subnet list
```

### **Configuration File Templates**

#### **Development Configuration**

```yaml
network:
  endpoint: "ws://localhost:9944"
  ws_endpoint: "ws://localhost:9944"
  timeout: 10
  retry_attempts: 1

output:
  format: "json"
  verbose: true
  color: false

wallet:
  path: "~/.htcli/dev-wallets"
  default_name: "dev"
  encryption_enabled: false
```

#### **Production Configuration**

```yaml
network:
  endpoint: "wss://hypertensor.duckdns.org"
  ws_endpoint: "wss://hypertensor.duckdns.org"
  timeout: 30
  retry_attempts: 3

output:
  format: "table"
  verbose: false
  color: true

wallet:
  path: "~/.htcli/production-wallets"
  default_name: "production"
  encryption_enabled: true
```

## 🌐 **Network Configuration**

### **Endpoint Configuration**

```yaml
network:
  # Primary RPC endpoint
  endpoint: "wss://hypertensor.duckdns.org"

  # WebSocket endpoint (usually same as RPC)
  ws_endpoint: "wss://hypertensor.duckdns.org"
```

### **Connection Settings**

```yaml
network:
  # Connection timeout in seconds
  timeout: 30

  # Number of retry attempts for failed connections
  retry_attempts: 3
```

### **Custom Endpoints**

```yaml
# Testnet configuration
network:
  endpoint: "wss://testnet.hypertensor.org"
  ws_endpoint: "wss://testnet.hypertensor.org"

# Local development node
network:
  endpoint: "ws://localhost:9944"
  ws_endpoint: "ws://localhost:9944"
  timeout: 10
  retry_attempts: 1

# Load balancer with multiple endpoints
network:
  endpoint: "wss://lb.hypertensor.org"
  ws_endpoint: "wss://ws.hypertensor.org"
  timeout: 45
  retry_attempts: 5
```

### **Testing Network Configuration**

```bash
# Test connection with current config
htcli chain network

# Test with custom endpoint
htcli --endpoint wss://custom.endpoint.com chain network

# Validate network configuration
htcli config validate
```

## 📊 **Output Configuration**

### **Format Options**

```yaml
output:
  # Default output format
  format: "table"  # Options: table, json, csv

  # Enable verbose output
  verbose: false

  # Enable colored output
  color: true
```

### **Format Examples**

#### **Table Format (Human-Readable)**

```bash
htcli chain network --format table
```

```
Network Statistics
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Metric             ┃ Value  ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ Total Subnets      │ 15     │
│ Active Subnets     │ 12     │
│ Total Nodes        │ 1,247  │
│ Total Stake        │ 15.2M  │
└────────────────────┴────────┘
```

#### **JSON Format (Scripting)**

```bash
htcli chain network --format json
```

```json
{
  "total_subnets": 15,
  "active_subnets": 12,
  "total_nodes": 1247,
  "total_stake": 15200000000000000000000000
}
```

#### **CSV Format (Data Analysis)**

```bash
htcli chain network --format csv
```

```csv
metric,value
total_subnets,15
active_subnets,12
total_nodes,1247
total_stake,15200000000000000000000000
```

### **Verbose Output**

```yaml
output:
  verbose: true
```

Enables detailed output including:

- Request/response timing
- Connection details
- Debug information
- Error stack traces

### **Color Configuration**

```yaml
output:
  color: true  # Enable colors
  color: false # Disable colors (for logs/scripts)
```

## 🔑 **Wallet Configuration**

### **Storage Path Configuration**

```yaml
wallet:
  # Path where wallets and keys are stored
  path: "~/.htcli/wallets"
```

### **Custom Wallet Paths**

```yaml
# Development environment
wallet:
  path: "~/.htcli/dev-wallets"
  default_name: "dev"

# Production environment
wallet:
  path: "/secure/production/wallets"
  default_name: "production"

# Shared team environment
wallet:
  path: "/shared/team/wallets"
  default_name: "team"
```

### **Security Configuration**

```yaml
wallet:
  # Enable wallet encryption
  encryption_enabled: true

  # Default wallet name
  default_name: "default"
```

### **Wallet Directory Structure**

```
~/.htcli/wallets/
├── default/
│   ├── keypair.json
│   └── metadata.json
├── production/
│   ├── keypair.json
│   └── metadata.json
└── backup/
    ├── keypair.json
    └── metadata.json
```

## 🎯 **Personal Asset Filtering Configuration**

The CLI includes a powerful universal --mine filtering system that allows you to view only your personal assets across all commands.

### **Filter Configuration Section**

```yaml
# Personal Asset Filtering Configuration
filter:
  # Default behavior for --mine flag
  mine: false  # Set to true to make --mine the default behavior
```

### **Environment Variable Override**

```bash
# Enable --mine filtering by default
export HTCLI_FILTER_MINE=true

# Disable --mine filtering (default)
export HTCLI_FILTER_MINE=false
```

### **How It Works**

The filtering system:

1. **Reads wallet keys** from the configured wallet path (`~/.htcli/wallets/`)
2. **Identifies ownership** by comparing blockchain data with your addresses
3. **Filters results** to show only assets you own
4. **Provides clear feedback** when no personal assets are found

### **Supported Commands**

The --mine flag works with:

- `htcli --mine subnet list` - Shows only subnets you own
- `htcli --mine stake info` - Shows stakes for ALL your addresses
- `htcli --mine node list` - Shows only nodes you registered

### **Configuration Examples**

#### **Personal Development Setup**

```yaml
filter:
  mine: true  # Default to personal view

wallet:
  path: "~/.htcli/dev-wallets"
  default_name: "dev-key"
```

#### **Network Monitoring Setup**

```yaml
filter:
  mine: false  # Default to network-wide view

output:
  format: "json"  # For automated processing
  verbose: true
```

#### **Multi-Address Portfolio Management**

```yaml
filter:
  mine: false  # Explicit --mine usage preferred

wallet:
  path: "~/.htcli/portfolio-wallets"
  encryption_enabled: true
```

### **Best Practices**

- **Keep `mine: false`** in config for explicit control
- **Use `--mine` flag explicitly** when you want personal view
- **Ensure wallet keys are properly stored** in the configured path
- **Use environment variables** for temporary behavior changes

## 🔧 **Advanced Configuration**

### **Multiple Environment Setup**

```bash
# Create different configs for different purposes
mkdir -p ~/.htcli/configs

# Development config
htcli config init --config ~/.htcli/configs/dev.yaml

# Staging config
htcli config init --config ~/.htcli/configs/staging.yaml

# Production config
htcli config init --config ~/.htcli/configs/prod.yaml
```

### **Environment-Specific Scripts**

```bash
#!/bin/bash
# dev-htcli.sh
export HTCLI_CONFIG_FILE="~/.htcli/configs/dev.yaml"
htcli "$@"
```

```bash
#!/bin/bash
# prod-htcli.sh
export HTCLI_CONFIG_FILE="~/.htcli/configs/prod.yaml"
htcli "$@"
```

### **Configuration Validation**

```bash
# Validate default configuration
htcli config validate

# Validate specific configuration
htcli config validate --config ~/.htcli/configs/prod.yaml

# Validate all configurations
for config in ~/.htcli/configs/*.yaml; do
    echo "Validating $config"
    htcli config validate --config "$config"
done
```

### **Configuration Backup and Restore**

```bash
# Backup configuration
cp ~/.htcli/config.yaml ~/.htcli/config-backup-$(date +%Y%m%d).yaml

# Restore configuration
cp ~/.htcli/config-backup-20240315.yaml ~/.htcli/config.yaml

# Version control configurations
git add ~/.htcli/configs/
git commit -m "Update CLI configurations"
```

## 🔍 **Configuration Management Commands**

### **View Configuration**

```bash
# Show current configuration in table format
htcli config show

# Show configuration as YAML
htcli config show --format yaml

# Show configuration as JSON
htcli config show --format json

# Show specific configuration file
htcli config show --config ~/.htcli/configs/prod.yaml
```

### **Edit Configuration**

```bash
# Edit default configuration
htcli config edit

# Edit specific configuration
htcli config edit --config ~/.htcli/configs/dev.yaml
```

### **Configuration Path**

```bash
# Show default configuration path
htcli config path

# Show specific configuration path
htcli config path --config ~/.htcli/configs/prod.yaml
```

## 🚨 **Troubleshooting**

### **Common Configuration Issues**

#### **Connection Problems**

```bash
# Test network connectivity
htcli chain network

# Try different endpoint
htcli --endpoint wss://backup.endpoint.com chain network

# Check configuration
htcli config show --format yaml
```

#### **File Permission Issues**

```bash
# Check configuration file permissions
ls -la ~/.htcli/config.yaml

# Fix permissions
chmod 600 ~/.htcli/config.yaml
chmod 700 ~/.htcli/
```

#### **Invalid Configuration**

```bash
# Validate configuration
htcli config validate

# Reset to defaults
htcli config init --force

# Create new configuration
mv ~/.htcli/config.yaml ~/.htcli/config.yaml.backup
htcli config init
```

### **Configuration Debugging**

#### **Verbose Mode**

```bash
# Enable verbose output
htcli --verbose chain network

# Or set in configuration
output:
  verbose: true
```

#### **Configuration Override Testing**

```bash
# Test with different settings
HTCLI_OUTPUT_FORMAT="json" htcli chain network
HTCLI_NETWORK_TIMEOUT="60" htcli chain network
```

#### **Environment Variable Check**

```bash
# Check current environment variables
env | grep HTCLI

# Clear environment variables
unset HTCLI_OUTPUT_FORMAT
unset HTCLI_NETWORK_ENDPOINT
```

### **Recovery Procedures**

#### **Reset Configuration**

```bash
# Backup current configuration
cp ~/.htcli/config.yaml ~/.htcli/config.yaml.backup

# Reset to defaults
rm ~/.htcli/config.yaml
htcli config init
```

#### **Restore from Backup**

```bash
# Restore configuration
cp ~/.htcli/config.yaml.backup ~/.htcli/config.yaml

# Validate restored configuration
htcli config validate
```

This comprehensive configuration guide covers all aspects of setting up and managing the Hypertensor CLI configuration for optimal performance and usability across different environments and use cases.
