# Configuration Guide

Complete guide to configuring the Hypertensor CLI, including setup, customization, and management of settings and preferences.

## 🎯 Overview

The Hypertensor CLI provides comprehensive configuration management for network connections, wallet settings, and user preferences with support for multiple environments and secure key management.

## 🚀 Quick Start

### Initialize Configuration
```bash
# Interactive configuration wizard
htcli config init

# Or with custom parameters
htcli config init --endpoint wss://testnet.hypertensor.ai --default-key my-key
```

### View Configuration
```bash
# Show current configuration
htcli config show

# Show specific configuration section
htcli config show --section network
htcli config show --section wallet
```

## 📁 Configuration Structure

### Configuration File Location
```
~/.htcli/
├── config.yaml          # Main configuration file
├── wallets/             # Wallet key storage
│   ├── my-key.json
│   └── imported-key.json
└── logs/                # Log files
    └── htcli.log
```

### Configuration Sections
```yaml
# Network Configuration
network:
  endpoint: "wss://testnet.hypertensor.ai"
  timeout: 30
  retry_attempts: 3
  websocket_options:
    max_size: 1048576
    compression: true

# Wallet Configuration
wallet:
  default_key: "my-key"
  key_dir: "~/.htcli/wallets"
  encryption_enabled: true
  backup_enabled: true

# User Interface Configuration
ui:
  format: "table"
  colors: true
  guidance: true
  confirmations: true

# Filtering Configuration
filtering:
  mine: false
  default_mine: false

# Logging Configuration
logging:
  level: "INFO"
  file: "~/.htcli/logs/htcli.log"
  max_size: 10485760
  backup_count: 5
```

## 🔧 Configuration Commands

### Initialize Configuration
```bash
# Interactive initialization
htcli config init

# Non-interactive initialization
htcli config init \
  --endpoint wss://testnet.hypertensor.ai \
  --default-key my-key \
  --timeout 30 \
  --format table
```

### View Configuration
```bash
# Show all configuration
htcli config show

# Show specific section
htcli config show --section network
htcli config show --section wallet
htcli config show --section ui

# Show in different formats
htcli config show --format json
htcli config show --format yaml
```

### Edit Configuration
```bash
# Interactive configuration editor
htcli config edit

# Edit specific section
htcli config edit --section network
htcli config edit --section wallet
```

### Set Configuration Values
```bash
# Set network endpoint
htcli config set --key network.endpoint --value wss://mainnet.hypertensor.ai

# Set default key
htcli config set --key wallet.default_key --value my-main-key

# Set UI format
htcli config set --key ui.format --value json

# Set timeout
htcli config set --key network.timeout --value 60
```

### Get Configuration Values
```bash
# Get network endpoint
htcli config get --key network.endpoint

# Get default key
htcli config get --key wallet.default_key

# Get UI format
htcli config get --key ui.format
```

## 🌐 Network Configuration

### Endpoint Configuration
```bash
# Set mainnet endpoint
htcli config set --key network.endpoint --value wss://mainnet.hypertensor.ai

# Set testnet endpoint
htcli config set --key network.endpoint --value wss://testnet.hypertensor.ai

# Set local endpoint
htcli config set --key network.endpoint --value ws://localhost:9944
```

### Connection Settings
```bash
# Set connection timeout
htcli config set --key network.timeout --value 60

# Set retry attempts
htcli config set --key network.retry_attempts --value 5

# Set WebSocket options
htcli config set --key network.websocket_options.max_size --value 2097152
htcli config set --key network.websocket_options.compression --value true
```

### Multiple Environments
```bash
# Create environment-specific configurations
htcli config set --key environments.mainnet.endpoint --value wss://mainnet.hypertensor.ai
htcli config set --key environments.testnet.endpoint --value wss://testnet.hypertensor.ai
htcli config set --key environments.local.endpoint --value ws://localhost:9944

# Switch environments
htcli config set --key network.endpoint --value $(htcli config get --key environments.mainnet.endpoint)
```

## 🔐 Wallet Configuration

### Key Management
```bash
# Set default key
htcli config set --key wallet.default_key --value my-main-key

# Set key directory
htcli config set --key wallet.key_dir --value ~/.htcli/wallets

# Enable encryption
htcli config set --key wallet.encryption_enabled --value true

# Enable backup
htcli config set --key wallet.backup_enabled --value true
```

### Security Settings
```bash
# Set encryption algorithm
htcli config set --key wallet.encryption_algorithm --value AES-256

# Set backup frequency
htcli config set --key wallet.backup_frequency --value daily

# Set backup retention
htcli config set --key wallet.backup_retention --value 30
```

## 🎨 User Interface Configuration

### Display Settings
```bash
# Set default format
htcli config set --key ui.format --value table
htcli config set --key ui.format --value json
htcli config set --key ui.format --value csv

# Enable/disable colors
htcli config set --key ui.colors --value true
htcli config set --key ui.colors --value false

# Enable/disable guidance
htcli config set --key ui.guidance --value true
htcli config set --key ui.guidance --value false

# Enable/disable confirmations
htcli config set --key ui.confirmations --value true
htcli config set --key ui.confirmations --value false
```

### Interactive Settings
```bash
# Set confirmation threshold
htcli config set --key ui.confirmation_threshold --value 1000000000000000000

# Set guidance level
htcli config set --key ui.guidance_level --value detailed
htcli config set --key ui.guidance_level --value basic
htcli config set --key ui.guidance_level --value minimal
```

## 🔍 Filtering Configuration

### Personal Asset Filtering
```bash
# Enable default mine filtering
htcli config set --key filtering.default_mine --value true

# Set mine filter behavior
htcli config set --key filtering.mine --value true
htcli config set --key filtering.mine --value false
```

### Filter Preferences
```bash
# Set default filtering
htcli config set --key filtering.default_filters --value "mine,active"

# Set filter display
htcli config set --key filtering.show_filter_info --value true
htcli config set --key filtering.show_filter_info --value false
```

## 📝 Logging Configuration

### Log Settings
```bash
# Set log level
htcli config set --key logging.level --value DEBUG
htcli config set --key logging.level --value INFO
htcli config set --key logging.level --value WARNING
htcli config set --key logging.level --value ERROR

# Set log file
htcli config set --key logging.file --value ~/.htcli/logs/htcli.log

# Set log rotation
htcli config set --key logging.max_size --value 10485760
htcli config set --key logging.backup_count --value 5
```

### Log Format
```bash
# Set log format
htcli config set --key logging.format --value "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Enable/disable timestamps
htcli config set --key logging.timestamps --value true
htcli config set --key logging.timestamps --value false
```

## 🔄 Environment Management

### Multiple Environments
```bash
# Create environment configurations
htcli config set --key environments.mainnet.endpoint --value wss://mainnet.hypertensor.ai
htcli config set --key environments.mainnet.timeout --value 60
htcli config set --key environments.mainnet.default_key --value mainnet-key

htcli config set --key environments.testnet.endpoint --value wss://testnet.hypertensor.ai
htcli config set --key environments.testnet.timeout --value 30
htcli config set --key environments.testnet.default_key --value testnet-key

htcli config set --key environments.local.endpoint --value ws://localhost:9944
htcli config set --key environments.local.timeout --value 10
htcli config set --key environments.local.default_key --value local-key
```

### Environment Switching
```bash
# Switch to mainnet
htcli config switch-environment mainnet

# Switch to testnet
htcli config switch-environment testnet

# Switch to local
htcli config switch-environment local

# List available environments
htcli config list-environments
```

### Environment Templates
```bash
# Create environment template
htcli config create-template --name production --environment mainnet

# Apply environment template
htcli config apply-template --name production

# List templates
htcli config list-templates
```

## 🔒 Security Configuration

### Encryption Settings
```bash
# Enable key encryption
htcli config set --key security.encrypt_keys --value true

# Set encryption algorithm
htcli config set --key security.encryption_algorithm --value AES-256

# Set key derivation
htcli config set --key security.key_derivation --value PBKDF2
```

### Access Control
```bash
# Set file permissions
htcli config set --key security.file_permissions --value 600

# Enable access logging
htcli config set --key security.access_logging --value true

# Set session timeout
htcli config set --key security.session_timeout --value 3600
```

## 📊 Configuration Validation

### Validate Configuration
```bash
# Validate entire configuration
htcli config validate

# Validate specific section
htcli config validate --section network
htcli config validate --section wallet

# Validate with custom schema
htcli config validate --schema /path/to/schema.yaml
```

### Configuration Testing
```bash
# Test network connection
htcli config test-connection

# Test wallet access
htcli config test-wallet

# Test all configurations
htcli config test-all
```

## 🔄 Configuration Backup and Restore

### Backup Configuration
```bash
# Backup entire configuration
htcli config backup --output config-backup.yaml

# Backup specific sections
htcli config backup --sections network,wallet --output network-wallet-backup.yaml

# Backup with encryption
htcli config backup --encrypt --password my-password --output encrypted-backup.yaml
```

### Restore Configuration
```bash
# Restore from backup
htcli config restore --input config-backup.yaml

# Restore specific sections
htcli config restore --input config-backup.yaml --sections network,wallet

# Restore with decryption
htcli config restore --input encrypted-backup.yaml --password my-password
```

## 🎯 Configuration Best Practices

### Security Best Practices
- **Encrypt Keys**: Always enable key encryption
- **Secure Permissions**: Use appropriate file permissions
- **Regular Backups**: Regular configuration backups
- **Access Control**: Limit access to configuration files

### Performance Best Practices
- **Optimize Timeouts**: Set appropriate timeouts
- **Connection Pooling**: Use connection pooling
- **Caching**: Enable caching where appropriate
- **Resource Limits**: Set appropriate resource limits

### Usability Best Practices
- **Default Values**: Set sensible default values
- **Environment Separation**: Separate environments clearly
- **Documentation**: Document custom configurations
- **Validation**: Regular configuration validation

## 🔧 Advanced Configuration

### Custom Configuration Files
```bash
# Use custom configuration file
htcli --config /path/to/custom-config.yaml subnet list

# Merge configurations
htcli --config /path/to/base-config.yaml --config /path/to/override-config.yaml subnet list
```

### Environment Variables
```bash
# Override with environment variables
export HTCLI_NETWORK_ENDPOINT=wss://custom.hypertensor.ai
export HTCLI_WALLET_DEFAULT_KEY=custom-key
htcli subnet list
```

### Configuration Inheritance
```yaml
# Base configuration
base:
  network:
    timeout: 30
    retry_attempts: 3

# Environment-specific overrides
environments:
  mainnet:
    network:
      endpoint: wss://mainnet.hypertensor.ai
      timeout: 60
  testnet:
    network:
      endpoint: wss://testnet.hypertensor.ai
      timeout: 15
```

## 📈 Configuration Monitoring

### Configuration Health
```bash
# Check configuration health
htcli config health

# Monitor configuration changes
htcli config monitor --watch

# Configuration statistics
htcli config stats
```

### Configuration Analytics
```bash
# Configuration usage analytics
htcli config analytics --period daily

# Configuration performance metrics
htcli config metrics --section network

# Configuration optimization suggestions
htcli config optimize
```

---

**The Hypertensor CLI provides comprehensive configuration management with support for multiple environments, secure key management, and extensive customization options for optimal user experience and security.** 🚀
