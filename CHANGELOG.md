# Hypertensor CLI Changelog

All notable changes to the Hypertensor CLI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2025-01-08

### 🎯 Major Features Added

#### Universal --mine Filtering System

- **Added universal `--mine` flag** that works across all relevant commands
- **Smart ownership detection** automatically identifies your assets vs. network-wide data
- **Multi-address support** manages assets across all your wallet addresses simultaneously
- **Clear data separation** distinguishes between network data and personal assets
- **Intelligent feedback** provides guidance when filtering results

**Supported Commands:**

- `htcli --mine subnet list` - Shows only subnets you own
- `htcli --mine stake info` - Shows stakes for ALL your addresses
- `htcli --mine node list` - Shows only nodes you registered

#### Interactive Configuration System

- **Added `htcli config init`** - Interactive configuration wizard
- **YAML output format** with human-readable structure
- **Custom configuration paths** support
- **Environment variable integration** for overrides
- **Configuration validation** with detailed error messages

### 🔧 Major Fixes

#### Wallet Key Storage System

- **Fixed persistent key storage** - Keys are now always saved to `~/.htcli/wallets/`
- **Corrected crypto type constants** - Fixed sr25519 (1) and ed25519 (0) mappings
- **Default password handling** - Uses secure default when no password provided
- **Immediate availability** - Generated keys work immediately with `--mine` filtering

#### Command Parameter Issues

- **Fixed `htcli chain block`** - Resolved parameter mismatch causing crashes
- **Fixed `htcli wallet claim-unbondings`** - Removed extraneous parameter
- **Fixed circular import** in `htcli wallet list-keys` command
- **Resolved subnet info data retrieval** - Handles partial blockchain data gracefully

#### Blockchain Data Integration

- **Enhanced subnet info handling** - Works with new Rust blockchain structure
- **Partial data support** - Gracefully handles incomplete subnet registration data
- **Robust storage queries** - Multiple fallback mechanisms for data retrieval
- **Clear data completeness indicators** - Shows when data is partial vs. complete

### 🏗️ Architecture Improvements

#### Command Structure Optimization

- **Flattened from 4-level to 3-level hierarchy** for better usability
- **Consistent switch-based arguments** - All commands use `--switches` format
- **Organized into 6 logical categories**:
  - `config` (5 commands) - Configuration management
  - `subnet` (5 commands) - Subnet operations
  - `node` (5 commands) - Node management
  - `stake` (7 commands) - Staking operations
  - `wallet` (4 commands) - Key management
  - `chain` (8 commands) - Blockchain queries

#### Enhanced User Experience

- **Comprehensive guidance panels** for complex operations
- **Interactive confirmation prompts** for safety
- **Rich terminal output** with colors, tables, and panels
- **Multiple output formats** - table, JSON, CSV support
- **Clear error messages** with actionable solutions

### 📊 Token Precision Implementation

- **18-digit TENSOR precision** implemented across all commands
- **Accurate balance formatting** with proper decimal handling
- **Validation functions** for token amounts and calculations
- **Updated test suites** with correct precision values

### 🧪 Testing & Quality Assurance

- **100% command success rate** - All 34 commands now working correctly
- **Updated integration tests** for new command structure
- **Fixed test data** with correct 18-digit precision values
- **Comprehensive test coverage** across all command categories

### 📚 Documentation Overhaul

#### New Documentation Files

- **Personal Asset Filtering Guide** - Comprehensive `--mine` usage documentation
- **Enhanced README** with universal filtering examples
- **Updated command reference** with latest syntax and options
- **Category-specific guides** updated with new features

#### Documentation Improvements

- **Command tree visualization** showing complete hierarchy
- **Usage examples** for all major features
- **Troubleshooting guides** for common issues
- **Best practices** for portfolio management

### 🔐 Security Enhancements

- **Encrypted key storage** using Fernet encryption
- **Secure default passwords** when none provided
- **Local-only key access** - no network exposure
- **Safe command defaults** - network-wide view by default, personal filtering explicit

### 🚀 Performance Optimizations

- **Efficient ownership checking** with minimal blockchain queries
- **Smart caching** for repeated address lookups
- **Optimized data structures** for multi-address operations
- **Reduced redundant API calls** through intelligent batching

---

## Previous Versions

### [1.0.0] - Initial Release

- Basic CLI structure with subnet, wallet, and chain operations
- WebSocket blockchain connectivity
- Initial command hierarchy
- Basic configuration management

---

## Migration Guide

### From Previous Versions

#### Command Structure Changes

```bash
# OLD (4-level hierarchy)
htcli subnet register create --path my-subnet
htcli wallet stake add --amount 1000

# NEW (3-level hierarchy)
htcli subnet register --path my-subnet
htcli stake add --amount 1000000000000000000  # 18-digit precision
```

#### Personal Asset Filtering

```bash
# OLD (separate commands or manual filtering)
htcli subnet list  # had to manually check ownership

# NEW (universal --mine flag)
htcli --mine subnet list  # automatically shows only your assets
```

#### Configuration Management

```bash
# OLD (manual configuration)
# Edit YAML files manually

# NEW (interactive setup)
htcli config init  # Interactive wizard with validation
```

### Breaking Changes

- **Token amounts** now require 18-digit precision
- **Command hierarchy** changed from 4-level to 3-level
- **Argument format** all arguments now use switches (`--arg value`)
- **Key storage** location changed to `~/.htcli/wallets/`

### Upgrade Steps

1. **Backup existing configuration** and wallet files
2. **Update command calls** to new 3-level hierarchy
3. **Regenerate wallet keys** to ensure proper storage
4. **Update token amounts** to 18-digit precision format
5. **Test --mine filtering** with your assets

---

## Support

### Getting Help

- **Command help**: `htcli <category> <command> --help`
- **Configuration issues**: `htcli config validate`
- **Key problems**: `htcli wallet list-keys`
- **Connectivity issues**: `htcli chain network`

### Common Issues

- **Keys not found**: Regenerate with `htcli wallet generate-key`
- **Command not found**: Check new command hierarchy
- **Precision errors**: Use 18-digit token amounts
- **Config issues**: Run `htcli config init`

### Documentation

- **Main README**: Project overview and quick start
- **docs/COMMANDS.md**: Complete command reference
- **docs/PERSONAL_ASSET_FILTERING.md**: --mine flag usage guide
- **docs/CONFIGURATION.md**: Configuration management guide
