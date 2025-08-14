# Node Management Guide

Complete guide to managing subnet nodes in the Hypertensor network, including registration, activation, updates, and lifecycle management.

## 🎯 Overview

The Hypertensor CLI provides comprehensive node management capabilities for the complete node lifecycle:

- **Registration**: Register nodes with comprehensive parameters
- **Activation**: Activate nodes within time windows
- **Updates**: Update reward rates and keys
- **Lifecycle Management**: Deactivate, reactivate, and remove nodes
- **Status Monitoring**: Track node performance and classification
- **Key Management**: Update coldkeys and hotkeys securely

## 🔗 Complete Node Lifecycle

### Node Lifecycle Stages
```
Register → Activate → Update → Deactivate → Reactivate → Remove
    ↓         ↓         ↓         ↓           ↓         ↓
  Queue    Active    Active   Deactivated  Active   Removed
  State    State     State      State      State    State
```

### Node Classifications
- **Registered**: Node is in registration queue
- **Idle**: Node is active but not yet included
- **Included**: Node participates in consensus
- **Validator**: Node is a validator (highest level)

## 📝 Node Registration

### Basic Registration
```bash
htcli node register \
  --subnet-id 1 \
  --hotkey 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu \
  --peer-id 12D3KooWABC123DEF456 \
  --bootnode-peer-id 12D3KooWXYZ789GHI012 \
  --client-peer-id 12D3KooWJKL345MNO678 \
  --stake 1000000000000000000 \
  --reward-rate 50000000000000000 \
  --key-name my-node-key
```

### Advanced Registration with Bootnode
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

### Registration Parameters

#### Required Parameters
- `--subnet-id`: Target subnet ID
- `--hotkey`: Node's hotkey address (SS58 format)
- `--peer-id`: Node's peer ID for networking
- `--bootnode-peer-id`: Bootstrap peer ID for bootnode
- `--client-peer-id`: Client peer ID for client-side operations
- `--stake`: Initial stake amount (minimum 100 TENSOR)
- `--reward-rate`: Delegate reward rate (in smallest units)
- `--key-name`: Key name for signing

#### Optional Parameters
- `--bootnode`: Bootnode multiaddress for DHT connection

### Registration Process
1. **Validation**: All parameters are validated
2. **Queue Placement**: Node enters registration queue
3. **Start Epoch**: Node gets activation start epoch
4. **Grace Period**: Node can activate within grace period
5. **Classification**: Node starts as Registered classification

## 🚀 Node Activation

### Basic Activation
```bash
htcli node activate --subnet-id 1 --node-id 5 --key-name my-node-key
```

### Activation Requirements
- Node must be in registration queue
- Current epoch must be within activation window
- Node must not be current epoch validator
- Valid signing key required

### Activation Process
1. **Validation**: Check activation eligibility
2. **State Change**: Move from Registered to Active
3. **Storage Update**: Update SubnetNodesData
4. **Count Update**: Increment TotalSubnetNodes
5. **Classification**: Set to Idle classification

### Activation Timeline
```
Registration → Queue Period → Activation Window → Grace Period
     ↓              ↓              ↓                ↓
  Registered    Registered    Can Activate    Can Activate
  State         State         (Start Epoch)   (Grace Period)
```

## 🔄 Node Updates

### Update Delegate Reward Rate
```bash
htcli node update \
  --subnet-id 1 \
  --node-id 5 \
  --delegate-reward-rate 60000000000000000 \
  --key-name my-node-key
```

### Rate Update Rules
- **Increase**: No limitations, can increase anytime
- **Decrease**: Limited to 1% decrease per 24 hours
- **Strategic Planning**: Plan rate changes carefully
- **Market Impact**: Rate affects delegation attractiveness

### Rate Strategy
- **Competitive Rates**: Balance operator and delegator interests
- **Market Conditions**: Adjust based on network conditions
- **Delegation Growth**: Higher rates attract more delegators
- **Revenue Optimization**: Find optimal rate for strategy

## 🔑 Key Management

### Update Coldkey
```bash
htcli node update-coldkey \
  --subnet-id 1 \
  --node-id 5 \
  --new-coldkey 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu \
  --key-name my-node-key
```

### Update Hotkey
```bash
htcli node update-hotkey \
  --subnet-id 1 \
  --node-id 5 \
  --new-hotkey 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu \
  --key-name my-node-key
```

### Key Security Requirements
- **Coldkey ≠ Hotkey**: Keys must be different (enforced)
- **Valid Addresses**: New keys must be valid SS58 format
- **Proper Signing**: Current key must sign update transaction
- **Secure Storage**: Store keys securely (hardware wallet for coldkey)

### Key Roles
- **Coldkey**: High-security key for ownership operations
- **Hotkey**: Frequent-use key for daily operations
- **Separation**: Clear separation of security and operational keys

## ⏸️ Node Deactivation

### Temporary Deactivation
```bash
htcli node deactivate --subnet-id 1 --node-id 5 --key-name my-node-key
```

### Deactivation Requirements
- Node must be Validator classification
- Valid signing key required
- Must last at least one epoch
- Cannot exceed MaxDeactivationEpochs

### Deactivation Process
1. **Validation**: Check deactivation eligibility
2. **State Change**: Move from Active to Deactivated
3. **Storage Update**: Update DeactivatedSubnetNodesData
4. **Count Update**: Decrement TotalSubnetNodes
5. **Stake Locked**: Stake remains locked during deactivation

### Deactivation vs Removal
- **Deactivation**: Temporary, reversible, stake locked
- **Removal**: Permanent, irreversible, stake must be removed separately

## 🔄 Node Reactivation

### Reactivate Deactivated Node
```bash
htcli node reactivate --subnet-id 1 --node-id 5 --key-name my-node-key
```

### Reactivation Requirements
- Node must be in deactivated state
- Must reactivate within MaxDeactivationEpochs
- Valid signing key required
- Node must not have exceeded time limit

### Reactivation Process
1. **Validation**: Check reactivation eligibility
2. **State Change**: Move from Deactivated to Active
3. **Classification**: Set to Validator classification
4. **Storage Update**: Update SubnetNodesData
5. **Count Update**: Increment TotalSubnetNodes

### Time Limits
- **MaxDeactivationEpochs**: Maximum deactivation duration
- **Grace Period**: Time window for reactivation
- **Expiration**: Node must be removed if time limit exceeded

## 🗑️ Node Removal

### Remove Node with Automatic Stake Removal
```bash
htcli node remove \
  --subnet-id 1 \
  --node-id 5 \
  --remove-stake \
  --key-name my-node-key
```

### Remove Node with Manual Stake Removal
```bash
htcli node remove \
  --subnet-id 1 \
  --node-id 5 \
  --key-name my-node-key
```

### Removal Requirements
- Node must not be current epoch validator
- Valid signing key required
- Node must be owned by your hotkey
- Any staked tokens will remain locked until removed

### Removal Process
1. **Validation**: Check removal eligibility
2. **Node Removal**: Remove from subnet participation
3. **Data Cleanup**: Clear peer ID and hotkey mappings
4. **Count Update**: Update total node counts
5. **Stake Management**: Handle stake removal (automatic or manual)

### Beautiful Stake Management
- **Automatic Removal**: One-step process, immediate stake removal
- **Manual Removal**: Two-step process, remove stake separately
- **Clear Guidance**: Comprehensive instructions and next steps
- **Status Tracking**: Clear status updates and progress indication

## 🧹 Node Cleanup

### Cleanup Expired Nodes
```bash
htcli node cleanup-expired \
  --subnet-id 1 \
  --node-id 5 \
  --cleanup-type deactivated \
  --key-name my-node-key
```

### Cleanup Types
- **deactivated**: Clean up expired deactivated nodes
- **registered**: Clean up expired registered nodes

### Cleanup Benefits
- **Network Efficiency**: Free up network resources
- **Resource Management**: Clean up expired nodes
- **Anyone Can Call**: Public cleanup functions
- **Stake Recovery**: Recover locked stakes

## 📊 Node Status Monitoring

### Get Node Status
```bash
htcli node status --subnet-id 1 --node-id 5 --format table
```

### Status Information
- **Current Classification**: Registered, Idle, Included, Validator
- **Activation Eligibility**: Can activate, activation window
- **Stake Information**: Current stake and reward rate
- **Performance Metrics**: Attestation ratios and penalties
- **Network Participation**: Active status and participation

### List Nodes
```bash
htcli node list --subnet-id 1 --format table --limit 10
```

### Personal Node Filtering
```bash
# View only your nodes
htcli node list --mine

# View your nodes in specific subnet
htcli node list --subnet-id 1 --mine
```

## 🎯 Node Management Strategy

### Registration Strategy
1. **Research Subnet**: Understand subnet requirements and performance
2. **Prepare Infrastructure**: Set up node server and networking
3. **Generate Keys**: Create secure hotkey and coldkey
4. **Plan Stake**: Determine appropriate stake amount
5. **Set Reward Rate**: Choose competitive reward rate

### Activation Strategy
1. **Monitor Queue**: Track registration queue position
2. **Plan Timing**: Plan activation within time window
3. **Prepare Resources**: Ensure node is ready for activation
4. **Execute Activation**: Activate within grace period
5. **Monitor Progress**: Track classification upgrades

### Performance Optimization
1. **Monitor Status**: Regular status checks
2. **Track Metrics**: Monitor attestation ratios and penalties
3. **Update Rates**: Adjust reward rates strategically
4. **Maintain Infrastructure**: Keep node server optimized
5. **Plan Maintenance**: Schedule deactivation for maintenance

### Key Management Strategy
1. **Secure Storage**: Store coldkey in hardware wallet
2. **Regular Updates**: Update keys for security
3. **Backup Strategy**: Multiple secure backups
4. **Access Control**: Limit access to operational keys
5. **Monitoring**: Monitor key usage and security

## 🛡️ Security Best Practices

### Key Security
- **Hardware Wallets**: Use hardware wallets for coldkeys
- **Key Separation**: Keep hotkeys and coldkeys separate
- **Regular Updates**: Update keys regularly for security
- **Secure Storage**: Store keys in secure locations
- **Access Control**: Limit access to critical keys

### Operational Security
- **Server Security**: Secure node server infrastructure
- **Network Security**: Protect network connections
- **Monitoring**: Monitor node performance and security
- **Backup Strategy**: Regular backups of critical data
- **Incident Response**: Plan for security incidents

### Stake Management
- **Diversification**: Diversify stakes across multiple nodes
- **Risk Management**: Understand stake risks and rewards
- **Monitoring**: Monitor stake performance regularly
- **Strategic Planning**: Plan stake allocation strategically
- **Emergency Procedures**: Plan for emergency stake removal

## 📈 Performance Monitoring

### Key Metrics
- **Attestation Ratio**: Percentage of successful attestations
- **Penalty Count**: Number of penalties received
- **Reward Rate**: Current delegate reward rate
- **Stake Amount**: Total stake in node
- **Classification**: Current node classification

### Monitoring Commands
```bash
# Check node status
htcli node status --subnet-id 1 --node-id 5

# Monitor classification changes
htcli node list --subnet-id 1 --mine

# Track performance over time
htcli chain node --subnet-id 1 --node-id 5
```

### Performance Optimization
- **Infrastructure**: Optimize server performance
- **Networking**: Ensure stable network connections
- **Monitoring**: Regular performance monitoring
- **Maintenance**: Schedule regular maintenance
- **Updates**: Keep software and configurations updated

## 🔄 Maintenance Procedures

### Regular Maintenance
1. **Status Check**: Regular node status monitoring
2. **Performance Review**: Review performance metrics
3. **Infrastructure Check**: Check server and network health
4. **Security Review**: Review security configurations
5. **Update Planning**: Plan necessary updates

### Emergency Procedures
1. **Deactivation**: Deactivate node for emergency maintenance
2. **Stake Protection**: Ensure stake is protected during maintenance
3. **Quick Recovery**: Plan for quick recovery procedures
4. **Communication**: Communicate maintenance to delegators
5. **Documentation**: Document maintenance procedures

### Planned Maintenance
1. **Schedule**: Plan maintenance during low-activity periods
2. **Notification**: Notify delegators of planned maintenance
3. **Preparation**: Prepare all necessary resources
4. **Execution**: Execute maintenance procedures
5. **Verification**: Verify node is operating correctly

## 🎯 Advanced Node Management

### Multi-Node Management
```bash
# Manage multiple nodes
for node_id in {1..5}; do
  htcli node status --subnet-id 1 --node-id $node_id
done
```

### Automated Monitoring
```bash
# Automated status monitoring script
#!/bin/bash
while true; do
  htcli node status --subnet-id 1 --node-id 5 --format json
  sleep 300  # Check every 5 minutes
done
```

### Performance Optimization
```bash
# Update reward rates based on performance
htcli node update --subnet-id 1 --node-id 5 --delegate-reward-rate 55000000000000000 --key-name my-node-key
```

### Strategic Planning
- **Market Analysis**: Analyze competitive landscape
- **Rate Strategy**: Plan reward rate changes
- **Stake Optimization**: Optimize stake allocation
- **Risk Management**: Manage operational risks
- **Growth Planning**: Plan for network growth

---

**This comprehensive node management guide covers all aspects of node lifecycle management, from registration to removal, with security best practices, performance monitoring, and strategic planning for successful node operation in the Hypertensor network.** 🚀
