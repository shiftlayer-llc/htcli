# Automated Flows Documentation

The Hypertensor CLI includes powerful automated workflows that combine multiple related operations into streamlined, user-friendly processes. These flows significantly improve developer experience by reducing manual steps and providing guided processes with comprehensive validation.

## Overview

Automated flows address common sequences of operations that users typically perform when working with the Hypertensor network. Instead of running multiple commands manually, flows provide:

- **Guided Setup**: Interactive prompts collect necessary information
- **Automated Execution**: Multiple operations run automatically with progress tracking
- **Error Handling**: Robust error handling with retry logic and recovery
- **Comprehensive Validation**: Built-in verification of results
- **Clear Feedback**: Rich terminal output with progress indicators and summaries

## Available Flows

### 1. Complete Subnet Deployment Flow

**Command**: `htcli flow run subnet-deployment`

**Purpose**: Automates the entire process of creating and deploying a subnet with initial node.

**Target Users**: Subnet creators, infrastructure providers

**Automated Steps**:
1. Configuration initialization
2. Wallet key generation/import
3. Balance verification
4. Subnet registration
5. Subnet activation
6. Initial node addition
7. Initial stake addition
8. Deployment verification

**Example Usage**:
```bash
htcli flow run subnet-deployment
```

**What You'll Need**:
- Sufficient TENSOR balance for registration and staking
- Node hotkey address and peer ID
- Subnet configuration parameters (memory, blocks, intervals)

**Typical Completion Time**: 3-5 minutes

### 2. Node Operator Onboarding Flow

**Command**: `htcli flow run node-onboarding`

**Purpose**: Automates joining an existing subnet as a node operator with initial stake.

**Target Users**: Node operators, miners

**Automated Steps**:
1. Configuration initialization
2. Wallet key generation/import
3. Subnet discovery and selection
4. Balance verification
5. Node registration
6. Initial stake addition
7. Node status monitoring setup

**Example Usage**:
```bash
htcli flow run node-onboarding
```

**What You'll Need**:
- Node infrastructure (hotkey, peer ID)
- Initial stake amount in TENSOR
- Choice of subnet to join (or let the system recommend)

**Features**:
- **Smart Subnet Recommendation**: Analyzes available subnets and recommends optimal choices
- **Automatic Scoring**: Evaluates subnets based on node count, activity, and available slots
- **Manual Override**: Option to manually select specific subnet

**Typical Completion Time**: 2-4 minutes

### 3. Staking Portfolio Setup Flow

**Command**: `htcli flow run staking-portfolio`

**Purpose**: Sets up diversified staking portfolio across multiple subnets and nodes.

**Target Users**: Investors, stakers

**Automated Steps**:
1. Configuration and wallet setup
2. Portfolio strategy definition
3. Subnet analysis and selection
4. Balance verification and allocation
5. Stake distribution execution
6. Portfolio monitoring setup

**Example Usage**:
```bash
htcli flow run staking-portfolio
```

**What You'll Need**:
- Total amount to stake (minimum recommended: 50 TENSOR)
- Portfolio strategy preference (conservative/balanced/aggressive)
- Risk tolerance settings

**Features**:
- **Intelligent Allocation**: Analyzes opportunities and calculates optimal stake distribution
- **Risk Management**: Strategy-based filtering and diversification
- **Performance Scoring**: Evaluates nodes based on multiple performance metrics
- **Subnet Diversification**: Ensures stakes are spread across different subnets

**Portfolio Strategies**:
- **Conservative**: Lower risk, established subnets and nodes
- **Balanced**: Mix of established and emerging opportunities
- **Aggressive**: Higher risk/reward, includes newer subnets

**Typical Completion Time**: 5-10 minutes

### 4. Development Environment Setup Flow

**Command**: `htcli flow run development-setup`

**Purpose**: Creates development environment for testing applications on Hypertensor.

**Target Users**: Developers, testers

**Automated Steps**:
1. Configuration initialization
2. Development wallet setup
3. Test subnet registration and activation
4. Development node setup
5. Testing environment verification
6. Development tools configuration

**Example Usage**:
```bash
htcli flow run development-setup
```

**What You'll Need**:
- Project name for subnet naming
- Environment type (local/testnet/staging)
- Choice between mock or real node setup

**Features**:
- **Minimal Resource Requirements**: Optimized for development with low memory and fast intervals
- **Mock Node Support**: Option to use mock nodes for pure development testing
- **Development Tools**: Automated creation of monitoring commands and test scripts
- **Quick Activation**: Fast subnet activation for immediate development

**Development Benefits**:
- Isolated testing environment
- Minimal resource consumption
- Automated monitoring setup
- Test script generation

**Typical Completion Time**: 2-3 minutes

### 5. Migration and Recovery Flow

**Command**: `htcli flow run migration-recovery`

**Purpose**: Migrates existing assets or recovers from configuration issues.

**Target Users**: Existing users, system administrators, users migrating from other tools

**Automated Steps**:
1. Configuration restoration
2. Wallet key import/recovery
3. Asset discovery and verification
4. State reconstruction
5. Portfolio migration
6. Recovery verification

**Example Usage**:
```bash
htcli flow run migration-recovery
```

**What You'll Need**:
- Existing wallet keys (private keys, mnemonic phrases, or addresses)
- Recovery method preference
- Asset discovery preferences

**Recovery Methods**:
- **Private Key Import**: Import from 64-character hex private key
- **Mnemonic Recovery**: Import from 12/24-word mnemonic phrase
- **Address-Only**: Read-only monitoring by address

**Features**:
- **Comprehensive Asset Discovery**: Finds owned subnets, stake positions, and registered nodes
- **State Reconstruction**: Rebuilds complete portfolio view
- **Verification System**: Validates all discovered assets
- **Backup Creation**: Creates backup of current state before migration

**Typical Completion Time**: 3-8 minutes (depending on asset count)

## General Usage

### Listing Available Flows

```bash
htcli flow list
```

Shows all available flows with descriptions and target user types.

### Getting Flow Information

```bash
htcli flow info <flow-name>
```

Displays detailed information about a specific flow, including steps and requirements.

### Running a Flow

```bash
htcli flow run <flow-name>
```

Executes the specified flow with interactive prompts and progress tracking.

### Checking Flow System Status

```bash
htcli flow status
```

Shows the status of the flow system and usage statistics.

## Flow Execution Process

### 1. Initialization Phase
- Flow displays name, description, and overview
- Collects required inputs through interactive prompts
- Shows execution plan with all steps
- Requests user confirmation to proceed

### 2. Execution Phase
- Progress tracking with real-time updates
- Step-by-step execution with retry logic
- Error handling with detailed error messages
- Dependency checking between steps

### 3. Completion Phase
- Results summary with key information
- Success/failure status with details
- Execution time and performance metrics
- Next steps and monitoring guidance

## Best Practices

### Before Running Flows

1. **Ensure Sufficient Balance**: Check that your wallet has enough TENSOR for the intended operations
2. **Prepare Required Information**: Gather node details, addresses, and configuration parameters
3. **Choose Appropriate Environment**: Select the right network (mainnet/testnet) for your needs
4. **Backup Important Data**: Create backups of existing configurations and keys

### During Flow Execution

1. **Read Prompts Carefully**: Pay attention to input validation and requirements
2. **Don't Interrupt**: Allow flows to complete fully for best results
3. **Monitor Progress**: Watch for any error messages or warnings
4. **Keep Information Handy**: Have wallet addresses, node IDs, and other details ready

### After Flow Completion

1. **Verify Results**: Use the provided monitoring commands to check status
2. **Save Important Information**: Record subnet IDs, node IDs, and addresses
3. **Set Up Monitoring**: Use the suggested monitoring commands regularly
4. **Plan Next Steps**: Consider additional operations based on flow results

## Error Handling and Recovery

### Common Issues and Solutions

**Insufficient Balance**:
- Solution: Add more TENSOR to your wallet before retrying
- Prevention: Check balance requirements in flow information

**Network Connectivity Issues**:
- Solution: Check internet connection and endpoint configuration
- Prevention: Verify network status with `htcli chain network`

**Invalid Input Parameters**:
- Solution: Ensure addresses, amounts, and IDs are in correct format
- Prevention: Use the CLI's validation hints during input

**Step Failures**:
- Solution: Flows include retry logic for transient failures
- Prevention: Ensure all prerequisites are met before starting

### Recovery Options

If a flow fails partway through:

1. **Check Error Messages**: Review the specific error and failed step
2. **Verify Prerequisites**: Ensure balance, connectivity, and inputs are correct
3. **Retry Flow**: Most flows can be safely retried after addressing issues
4. **Manual Completion**: Complete remaining steps manually if needed
5. **Seek Support**: Contact support with error details if issues persist

## Advanced Usage

### Skipping Confirmations

For automated environments, use the `--yes` flag to skip confirmation prompts:

```bash
htcli flow run subnet-deployment --yes
```

### Custom Configuration

Flows respect your CLI configuration settings:

```bash
# Use custom config file
htcli --config /path/to/config.yaml flow run node-onboarding

# Use different endpoint
htcli --endpoint wss://custom-endpoint.com flow run staking-portfolio
```

### Integration with Other Tools

Flows can be integrated into larger automation systems:

```bash
#!/bin/bash
# Automated deployment script
htcli flow run subnet-deployment --yes
if [ $? -eq 0 ]; then
    echo "Subnet deployment successful"
    # Continue with additional automation
else
    echo "Subnet deployment failed"
    exit 1
fi
```

## Flow Development

The flow system is extensible. Future versions will include:

- **Custom Flow Creation**: Ability to create user-defined flows
- **Flow Templates**: Pre-built templates for common patterns
- **Flow Sharing**: Share flows with the community
- **Advanced Scheduling**: Time-based and event-driven flow execution

## Support and Feedback

For flow-related issues or feature requests:

1. **Check Documentation**: Review this guide and command help
2. **Use Flow Info**: Get detailed information with `htcli flow info <name>`
3. **Check Status**: Verify system status with `htcli flow status`
4. **Report Issues**: Submit bug reports with flow name and error details
5. **Request Features**: Suggest new flows or improvements

The automated flow system significantly improves the Hypertensor CLI user experience by providing guided, error-resistant processes for common operations. Whether you're a subnet creator, node operator, investor, or developer, there's a flow designed to streamline your workflow and reduce the complexity of blockchain operations.
