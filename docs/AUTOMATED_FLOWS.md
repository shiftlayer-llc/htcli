# Automated Flows Guide

Complete guide to using automated workflows in the Hypertensor CLI for streamlined multi-step operations and guided processes.

## 🎯 Overview

The Hypertensor CLI provides automated flows that guide users through complex multi-step operations with interactive prompts, progress tracking, and comprehensive guidance.

## 🔄 Available Flows

### 1. Subnet Deployment Flow

**Purpose**: Complete subnet deployment from registration to activation
**Steps**: Registration → Configuration → Node Setup → Activation

### 2. Node Onboarding Flow

**Purpose**: Complete node onboarding from registration to validation
**Steps**: Registration → Activation → Performance Optimization → Monitoring

### 3. Staking Portfolio Flow

**Purpose**: Comprehensive staking portfolio setup and management
**Steps**: Research → Diversification → Optimization → Monitoring

### 4. Development Setup Flow

**Purpose**: Complete development environment setup
**Steps**: Environment Setup → Key Generation → Network Connection → Testing

### 5. Migration Recovery Flow

**Purpose**: Node migration and recovery procedures
**Steps**: Backup → Migration → Verification → Recovery

## 🚀 Using Automated Flows

### List Available Flows

```bash
htcli flow list --format table
```

### Get Flow Information

```bash
htcli flow info subnet-deployment --format table
```

### Run Automated Flow

```bash
htcli flow run subnet-deployment --interactive
```

## 📋 Flow Details

### Subnet Deployment Flow

#### Purpose

Complete subnet deployment from initial registration to full activation with comprehensive setup and optimization.

#### Steps

1. **Subnet Registration**
   - Name and description setup
   - Repository configuration
   - Stake limits and parameters
   - Initial coldkey configuration

2. **Subnet Configuration**
   - Churn limit optimization
   - Epoch configuration
   - Penalty system setup
   - Key type configuration

3. **Node Setup**
   - Initial node registration
   - Bootnode configuration
   - Stake allocation
   - Performance optimization

4. **Subnet Activation**
   - Activation requirements verification
   - Stake validation
   - Network integration
   - Performance monitoring

#### Usage

```bash
# Run subnet deployment flow
htcli flow run subnet-deployment --interactive

# Run with custom parameters
htcli flow run subnet-deployment --name "My AI Subnet" --repo "https://github.com/my/ai-subnet"
```

### Node Onboarding Flow

#### Purpose

Complete node onboarding process from registration to active validation with performance optimization and monitoring.

#### Steps

1. **Node Registration**
   - Hotkey and coldkey setup
   - Peer ID configuration
   - Stake allocation
   - Bootnode setup

2. **Node Activation**
   - Activation window monitoring
   - Performance verification
   - Network integration
   - Status validation

3. **Performance Optimization**
   - Reward rate optimization
   - Performance monitoring
   - Strategy adjustment
   - Risk management

4. **Ongoing Monitoring**
   - Status tracking
   - Performance metrics
   - Alert configuration
   - Maintenance planning

#### Usage

```bash
# Run node onboarding flow
htcli flow run node-onboarding --interactive

# Run with specific subnet
htcli flow run node-onboarding --subnet-id 1 --hotkey <hotkey>
```

### Staking Portfolio Flow

#### Purpose

Comprehensive staking portfolio setup with diversification, optimization, and ongoing management.

#### Steps

1. **Portfolio Research**
   - Subnet analysis
   - Node performance research
   - Rate comparison
   - Risk assessment

2. **Portfolio Diversification**
   - Subnet allocation
   - Node selection
   - Amount distribution
   - Risk balancing

3. **Portfolio Optimization**
   - Performance monitoring
   - Rate adjustment
   - Rebalancing
   - Strategy refinement

4. **Ongoing Management**
   - Performance tracking
   - Portfolio monitoring
   - Strategy updates
   - Risk management

#### Usage

```bash
# Run staking portfolio flow
htcli flow run staking-portfolio --interactive

# Run with specific budget
htcli flow run staking-portfolio --budget 10000000000000000000
```

### Development Setup Flow

#### Purpose

Complete development environment setup for Hypertensor network development and testing.

#### Steps

1. **Environment Setup**
   - CLI installation
   - Configuration setup
   - Network connection
   - Development tools

2. **Key Generation**
   - Development keys
   - Test keys
   - Key management
   - Security setup

3. **Network Connection**
   - Testnet connection
   - Mainnet connection
   - Network validation
   - Performance testing

4. **Testing and Validation**
   - Command testing
   - API validation
   - Performance testing
   - Security validation

#### Usage

```bash
# Run development setup flow
htcli flow run development-setup --interactive

# Run with specific environment
htcli flow run development-setup --environment testnet
```

### Migration Recovery Flow

#### Purpose

Node migration and recovery procedures for maintenance, upgrades, and disaster recovery.

#### Steps

1. **Backup and Preparation**
   - Data backup
   - Configuration backup
   - Stake verification
   - Migration planning

2. **Migration Execution**
   - Node deactivation
   - Data migration
   - Configuration transfer
   - Network reconnection

3. **Verification and Testing**
   - Node verification
   - Performance testing
   - Stake validation
   - Network integration

4. **Recovery and Optimization**
   - Node reactivation
   - Performance optimization
   - Monitoring setup
   - Documentation update

#### Usage

```bash
# Run migration recovery flow
htcli flow run migration-recovery --interactive

# Run with specific node
htcli flow run migration-recovery --subnet-id 1 --node-id 5
```

## 🎯 Flow Features

### Interactive Prompts

- **User Input**: Collect required information
- **Validation**: Validate user inputs
- **Confirmation**: Confirm critical actions
- **Guidance**: Provide helpful guidance

### Progress Tracking

- **Step Progress**: Show current step and total steps
- **Status Updates**: Real-time status updates
- **Error Handling**: Graceful error handling
- **Recovery**: Automatic recovery from errors

### Comprehensive Guidance

- **Step Explanations**: Explain each step
- **Best Practices**: Provide best practices
- **Risk Warnings**: Warn about risks
- **Success Criteria**: Define success criteria

### Customization Options

- **Parameter Override**: Override default parameters
- **Skip Steps**: Skip optional steps
- **Custom Configuration**: Use custom configurations
- **Integration**: Integrate with existing workflows

## 🔧 Flow Configuration

### Flow Parameters

```bash
# Subnet deployment parameters
htcli flow run subnet-deployment \
  --name "My Subnet" \
  --repo "https://github.com/my/subnet" \
  --description "A great subnet" \
  --min-stake 1000000000000000000 \
  --max-stake 10000000000000000000

# Node onboarding parameters
htcli flow run node-onboarding \
  --subnet-id 1 \
  --hotkey <hotkey> \
  --peer-id <peer-id> \
  --stake 1000000000000000000

# Staking portfolio parameters
htcli flow run staking-portfolio \
  --budget 10000000000000000000 \
  --risk-tolerance medium \
  --diversification high
```

### Flow Customization

```bash
# Custom flow configuration
htcli flow run subnet-deployment \
  --config /path/to/custom-config.yaml \
  --skip-steps "node-setup" \
  --custom-params "custom-params.json"
```

## 📊 Flow Monitoring

### Progress Tracking

```bash
# Monitor flow progress
htcli flow status <flow-id>

# Get flow logs
htcli flow logs <flow-id>

# Cancel running flow
htcli flow cancel <flow-id>
```

### Flow History

```bash
# View flow history
htcli flow history --format table

# Get specific flow details
htcli flow history --flow-id <flow-id> --format json
```

## 🛡️ Flow Security

### Input Validation

- **Parameter Validation**: Validate all input parameters
- **Security Checks**: Perform security checks
- **Confirmation Prompts**: Confirm critical actions
- **Error Recovery**: Graceful error recovery

### Access Control

- **Key Management**: Secure key handling
- **Permission Checks**: Check user permissions
- **Audit Logging**: Log all actions
- **Rollback Capability**: Ability to rollback changes

## 🔄 Flow Integration

### Script Integration

```bash
#!/bin/bash
# Integrate flows into scripts

# Run subnet deployment
htcli flow run subnet-deployment --name "My Subnet" --non-interactive

# Wait for completion
while [ "$(htcli flow status <flow-id> | jq -r '.status')" != "completed" ]; do
  sleep 30
done

# Run node onboarding
htcli flow run node-onboarding --subnet-id 1 --non-interactive
```

### API Integration

```python
from src.htcli.flows import FlowManager

# Initialize flow manager
flow_manager = FlowManager()

# Run flow programmatically
flow_id = flow_manager.run_flow(
    "subnet-deployment",
    parameters={
        "name": "My Subnet",
        "repo": "https://github.com/my/subnet"
    }
)

# Monitor flow
status = flow_manager.get_flow_status(flow_id)
print(f"Flow status: {status}")
```

## 📈 Flow Optimization

### Performance Optimization

- **Parallel Execution**: Execute steps in parallel where possible
- **Resource Management**: Optimize resource usage
- **Caching**: Cache frequently used data
- **Batch Operations**: Use batch operations for efficiency

### Error Handling

- **Retry Logic**: Automatic retry for transient errors
- **Fallback Strategies**: Fallback strategies for failures
- **Rollback Capability**: Ability to rollback changes
- **Error Reporting**: Comprehensive error reporting

## 🎯 Best Practices

### Flow Design

- **Modular Steps**: Design flows with modular steps
- **Clear Dependencies**: Define clear step dependencies
- **Error Recovery**: Include error recovery mechanisms
- **Documentation**: Document flow behavior and requirements

### Flow Usage

- **Testing**: Test flows in development environment
- **Validation**: Validate flow parameters
- **Monitoring**: Monitor flow execution
- **Documentation**: Document flow usage and results

### Flow Maintenance

- **Regular Updates**: Update flows regularly
- **Version Control**: Use version control for flows
- **Testing**: Regular testing of flows
- **Documentation**: Keep documentation updated

## 🔧 Advanced Features

### Custom Flows

```python
from src.htcli.flows import BaseFlow

class CustomFlow(BaseFlow):
    def __init__(self):
        super().__init__("custom-flow", "Custom Flow Description")

    def execute(self, parameters):
        # Custom flow logic
        pass
```

### Flow Templates

```bash
# Create flow template
htcli flow create-template --name "my-template" --flow-id <flow-id>

# Use flow template
htcli flow run --template "my-template" --parameters "params.json"
```

### Flow Scheduling

```bash
# Schedule flow execution
htcli flow schedule --flow-id subnet-deployment --schedule "0 0 * * *"

# List scheduled flows
htcli flow schedule --list

# Cancel scheduled flow
htcli flow schedule --cancel <schedule-id>
```
