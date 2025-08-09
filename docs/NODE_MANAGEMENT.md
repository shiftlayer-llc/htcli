# Hypertensor CLI Node Management Guide

This comprehensive guide covers all aspects of node management using the Hypertensor CLI, from node deployment to lifecycle management and optimization.

## 📋 **Table of Contents**

1. [Node Management Overview](#node-management-overview)
2. [Node Concepts](#node-concepts)
3. [Node Lifecycle](#node-lifecycle)
4. [Adding Nodes to Subnets](#adding-nodes-to-subnets)
5. [Node Monitoring](#node-monitoring)
6. [Node Maintenance](#node-maintenance)
7. [Performance Optimization](#performance-optimization)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

## 🎯 **Node Management Overview**

Node management in the Hypertensor network involves:

- **Node Registration**: Adding nodes to subnets
- **Lifecycle Management**: Activation, deactivation, and removal
- **Performance Monitoring**: Tracking node health and performance
- **Stake Management**: Managing stake positions for nodes
- **Network Participation**: Ensuring optimal network contribution
- **🆕 Personal Node Portfolio**: Track and manage all your nodes across multiple addresses

### **Key Responsibilities**

- **Infrastructure Management**: Maintaining node hardware and software
- **Network Participation**: Ensuring nodes contribute effectively
- **Stake Optimization**: Managing stake for optimal returns
- **Performance Monitoring**: Tracking and improving node performance
- **🆕 Portfolio Management**: Use `--mine` to view only your nodes across all addresses

## 🧠 **Node Concepts**

### **Node Types**

In the Hypertensor network, nodes serve different roles:

#### **Validator Nodes**

- **Consensus Participation**: Participate in network consensus
- **Block Production**: Help produce and validate blocks
- **High Requirements**: Require significant stake and resources
- **High Rewards**: Earn substantial rewards for participation

#### **Compute Nodes**

- **AI Workloads**: Execute AI/ML computations
- **Resource Provision**: Provide computational resources
- **Flexible Requirements**: Various resource configurations
- **Performance-Based Rewards**: Rewards based on computation quality

### **Node Identity**

Each node has unique identifiers:

#### **Hotkey**

- **Node Identity**: Unique address identifying the node
- **Reward Destination**: Where node rewards are sent
- **Stake Target**: Address where others can stake
- **Public Key**: Derived from cryptographic keypair

#### **Peer ID**

- **Network Identity**: Unique identifier for network communication
- **P2P Networking**: Used for peer-to-peer connections
- **Discovery**: Helps other nodes find and connect
- **MultiHash Format**: Standard format for distributed networks

### **Node States**

Nodes can be in various states:

#### **Registered**

- **Initial State**: Node registered but not yet active
- **Queue Position**: Waiting for activation slot
- **Stake Required**: Must meet minimum stake requirements
- **Pending Activation**: Awaiting network approval

#### **Active**

- **Operational State**: Node actively participating
- **Earning Rewards**: Receiving rewards for participation
- **Network Contribution**: Contributing to network operations
- **Full Functionality**: All node features available

#### **Inactive**

- **Temporary State**: Node temporarily not participating
- **Stake Preserved**: Stake remains locked
- **No Rewards**: Not earning rewards while inactive
- **Reactivation Possible**: Can be reactivated when ready

#### **Removed**

- **Final State**: Node permanently removed from subnet
- **Stake Unbonding**: All stake enters unbonding period
- **No Recovery**: Cannot be reactivated (must re-register)
- **Clean Slate**: All node history cleared

## 🆕 **Personal Node Portfolio Management**

The CLI provides powerful tools to manage your node portfolio across multiple addresses:

### **Network View vs Personal View**

```bash
# 📊 NETWORK VIEW: See all nodes in a subnet
htcli node list --subnet-id 1

# 👤 PERSONAL VIEW: See only YOUR nodes in the subnet
htcli --mine node list --subnet-id 1

# 📊 NETWORK VIEW: Check status of specific node
htcli node status --subnet-id 1 --node-id 5

# 👤 PERSONAL VIEW: Check status of your nodes only
htcli --mine node status --subnet-id 1
```

### **Automatic Multi-Address Management**

- **Smart Detection**: Automatically finds nodes registered by any of your addresses
- **Comprehensive View**: Shows your nodes across all your wallet addresses
- **Clear Ownership**: Distinguishes your nodes from network-wide data
- **Portfolio Summary**: Track performance across your entire node portfolio

### **Benefits of Personal Node Management**

- **Simplified Monitoring**: Focus only on nodes you actually own
- **Portfolio Overview**: See all your nodes in one command
- **Multi-Address Support**: Manage nodes from different wallet addresses
- **Clear Data Separation**: Never confuse your nodes with others'

## 🔄 **Node Lifecycle**

The complete node lifecycle follows this pattern:

```
Register → Activate → Monitor → Maintain → Deactivate/Remove
```

### **1. Registration Phase**

```bash
# Register node to subnet with initial stake
htcli node add \
  --subnet-id 1 \
  --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY \
  --peer-id QmYwAPJzv5CZsnA625s3ofHtUyJ9eykQZ6d3s5hgcEAuSo \
  --stake 5000000000000000000 \
  --reward-rate 0.10
```

### **2. Activation Phase**

After registration, nodes enter an activation queue:

- **Queue Processing**: Network processes activation requests
- **Validation**: Node parameters and stake are validated
- **Slot Assignment**: Node receives operational slot
- **Status Change**: Node status changes to "Active"

### **3. Operational Phase**

Once active, nodes participate in network operations:

- **Work Assignment**: Receive tasks from the network
- **Performance Tracking**: Network monitors node performance
- **Reward Distribution**: Earn rewards based on contribution
- **Continuous Operation**: Maintain uptime and availability

### **4. Maintenance Phase**

Regular maintenance ensures optimal performance:

- **Performance Monitoring**: Track metrics and health
- **Stake Management**: Adjust stake levels as needed
- **Configuration Updates**: Update node parameters
- **Issue Resolution**: Address performance or connectivity issues

### **5. Deactivation/Removal Phase**

When ending node operation:

- **Graceful Deactivation**: Temporarily disable node
- **Permanent Removal**: Remove node from subnet permanently
- **Stake Recovery**: Claim unbonded stake after waiting period

## 🚀 **Adding Nodes to Subnets**

### **Prerequisites**

Before adding a node, ensure you have:

1. **Running Node Software**: Node must be operational
2. **Sufficient Stake**: Meet minimum staking requirements
3. **Valid Credentials**: Hotkey and peer ID ready
4. **Network Access**: Node can connect to subnet network
5. **Resource Requirements**: Meet subnet's resource needs

### **Basic Node Addition**

```bash
htcli node add \
  --subnet-id 1 \
  --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY \
  --peer-id QmYwAPJzv5CZsnA625s3ofHtUyJ9eykQZ6d3s5hgcEAuSo \
  --stake 1000000000000000000
```

This command will:

1. Show comprehensive guidance about the operation
2. Validate all parameters (subnet, hotkey, peer ID, stake)
3. Check subnet capacity and requirements
4. Submit node registration transaction
5. Place node in activation queue

### **Advanced Node Configuration**

```bash
htcli node add \
  --subnet-id 1 \
  --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY \
  --peer-id QmYwAPJzv5CZsnA625s3ofHtUyJ9eykQZ6d3s5hgcEAuSo \
  --stake 10000000000000000000 \
  --reward-rate 0.15 \
  --key-name production-key
```

**Advanced Parameters**:

- `--reward-rate`: Percentage of rewards shared with delegators (0.0-1.0)
- `--key-name`: Specific key to use for transaction signing
- `--no-guidance`: Skip interactive guidance for scripting

### **Node Addition with Guidance**

The CLI provides comprehensive guidance for node addition:

```
╭─────────────────────── 🔗 Adding Node to Subnet ───────────────────────────╮
│ This operation will register your node to participate in a subnet.          │
│                                                                             │
│ 📋 Requirements:                                                            │
│ • Valid subnet ID (must exist and be active)                                │
│ • Hotkey address (your node's identity)                                     │
│ • Peer ID (your node's network identifier)                                  │
│ • Sufficient TENSOR balance for staking                                     │
│ • Node must meet subnet's hardware requirements                             │
│                                                                             │
│ ⚙️ Process:                                                                 │
│ 1. Validates all input parameters                                           │
│ 2. Checks subnet exists and is accepting nodes                              │
│ 3. Verifies your balance is sufficient                                      │
│ 4. Submits node registration transaction                                    │
│ 5. Node enters queue for activation                                         │
│                                                                             │
│ 💡 Tips & Warnings:                                                         │
│ 💡 Check subnet requirements with: htcli subnet info --subnet-id <ID>       │
│ 💡 Verify your balance with: htcli chain balance <address>                  │
│ 💡 Generate peer ID with your node software                                 │
│ 💡 Keep your hotkey secure - it identifies your node                        │
╰─────────────────────────────────────────────────────────────────────────────╯
```

### **Batch Node Registration**

For multiple nodes:

```bash
#!/bin/bash
# batch-node-registration.sh

SUBNET_ID=1
BASE_STAKE="5000000000000000000"

# Array of node configurations
declare -a NODES=(
    "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY:QmYwAPJzv5CZsnA625s3ofHtUyJ9eykQZ6d3s5hgcEAuSo"
    "5HGjWAeFDfqNSFeQYdpzrQnJ8Z2Q7KqJMvLvHc9Y8N3k2L1:QmXyZ123ABC456DEF789GHI012JKL345MNO678PQR901STU"
    "5FpqN2X8Y9K3L6M4B7V1C5D2E8F9G3H6I0J2K5L8M1N4O7P:QmABC789XYZ012DEF345GHI678JKL901MNO234PQR567STU"
)

for node_config in "${NODES[@]}"; do
    IFS=':' read -r hotkey peer_id <<< "$node_config"

    echo "Registering node: $hotkey"
    htcli node add \
        --subnet-id $SUBNET_ID \
        --hotkey $hotkey \
        --peer-id $peer_id \
        --stake $BASE_STAKE \
        --no-guidance

    echo "Node registration submitted. Waiting before next..."
    sleep 5
done
```

## 📊 **Node Monitoring**

### **Individual Node Status**

```bash
# Get detailed status for specific node
htcli node status --subnet-id 1 --node-id 2

# Get status as JSON for processing
htcli node status --subnet-id 1 --node-id 2 --format json
```

**Status Information Includes**:

- **Node Configuration**: Basic parameters and settings
- **Current State**: Active, inactive, or transitioning
- **Stake Information**: Current stake amount and delegators
- **Performance Metrics**: Success rates, uptime, response times
- **Network Connectivity**: Peer connections and network health
- **Reward History**: Recent reward distributions

### **Subnet Node Overview**

```bash
# List all nodes in subnet
htcli node list --subnet-id 1

# Get detailed node data as JSON
htcli node list --subnet-id 1 --format json
```

**Node List Includes**:

- **Node ID and Hotkey**: Unique identifiers
- **Status**: Current operational state
- **Stake Amount**: Total staked tokens
- **Performance Score**: Network-calculated performance
- **Last Activity**: Most recent network participation

### **Monitoring Scripts**

#### **Basic Monitoring Script**

```bash
#!/bin/bash
# node-monitor.sh

SUBNET_ID=1
NODE_ID=2

echo "=== Node Status Report ==="
echo "Date: $(date)"
echo "Subnet: $SUBNET_ID, Node: $NODE_ID"
echo

# Get node status
echo "--- Node Status ---"
htcli node status --subnet-id $SUBNET_ID --node-id $NODE_ID

# Get subnet overview
echo -e "\n--- Subnet Overview ---"
htcli node list --subnet-id $SUBNET_ID

# Get network stats
echo -e "\n--- Network Stats ---"
htcli chain network
```

#### **Performance Tracking Script**

```bash
#!/bin/bash
# performance-tracker.sh

SUBNET_ID=1
NODE_ID=2
LOG_FILE="node-performance.log"

# Get current timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Get node performance data
PERFORMANCE_DATA=$(htcli node status --subnet-id $SUBNET_ID --node-id $NODE_ID --format json)

# Extract key metrics
UPTIME=$(echo $PERFORMANCE_DATA | jq -r '.uptime // "N/A"')
SUCCESS_RATE=$(echo $PERFORMANCE_DATA | jq -r '.success_rate // "N/A"')
STAKE_AMOUNT=$(echo $PERFORMANCE_DATA | jq -r '.stake // "N/A"')

# Log performance data
echo "$TIMESTAMP,$SUBNET_ID,$NODE_ID,$UPTIME,$SUCCESS_RATE,$STAKE_AMOUNT" >> $LOG_FILE

echo "Performance logged: Uptime=$UPTIME, Success Rate=$SUCCESS_RATE"
```

#### **Multi-Node Dashboard**

```bash
#!/bin/bash
# multi-node-dashboard.sh

SUBNET_ID=1

echo "=== Multi-Node Dashboard ==="
echo "Subnet: $SUBNET_ID"
echo "Generated: $(date)"
echo

# Get all nodes in subnet
NODES_DATA=$(htcli node list --subnet-id $SUBNET_ID --format json)

# Parse and display each node
echo $NODES_DATA | jq -r '.[] |
    "Node ID: \(.node_id) | Status: \(.status) | Stake: \(.stake) | Performance: \(.performance_score // "N/A")"'

# Summary statistics
TOTAL_NODES=$(echo $NODES_DATA | jq 'length')
ACTIVE_NODES=$(echo $NODES_DATA | jq '[.[] | select(.status == "active")] | length')
TOTAL_STAKE=$(echo $NODES_DATA | jq '[.[] | .stake] | add')

echo
echo "=== Summary ==="
echo "Total Nodes: $TOTAL_NODES"
echo "Active Nodes: $ACTIVE_NODES"
echo "Total Stake: $TOTAL_STAKE wei"
```

### **Automated Alerting**

```bash
#!/bin/bash
# node-alerting.sh

SUBNET_ID=1
NODE_ID=2
ALERT_EMAIL="admin@example.com"
MIN_PERFORMANCE=0.95

# Get node status
NODE_STATUS=$(htcli node status --subnet-id $SUBNET_ID --node-id $NODE_ID --format json)
PERFORMANCE=$(echo $NODE_STATUS | jq -r '.performance_score // 0')
STATUS=$(echo $NODE_STATUS | jq -r '.status')

# Check if node is underperforming
if (( $(echo "$PERFORMANCE < $MIN_PERFORMANCE" | bc -l) )); then
    echo "ALERT: Node $NODE_ID performance below threshold: $PERFORMANCE" | \
        mail -s "Node Performance Alert" $ALERT_EMAIL
fi

# Check if node is inactive
if [ "$STATUS" != "active" ]; then
    echo "ALERT: Node $NODE_ID is not active. Current status: $STATUS" | \
        mail -s "Node Status Alert" $ALERT_EMAIL
fi
```

## 🔧 **Node Maintenance**

### **Temporary Deactivation**

For maintenance or troubleshooting:

```bash
# Deactivate node temporarily
htcli node deactivate --subnet-id 1 --node-id 2
```

**What happens during deactivation**:

- Node stops receiving new tasks
- Existing tasks complete normally
- Stake remains locked (no unbonding)
- Node can be reactivated later
- No rewards earned while inactive

**Use cases for deactivation**:

- **Maintenance Windows**: Scheduled maintenance or updates
- **Troubleshooting**: Investigating performance issues
- **Resource Constraints**: Temporary resource limitations
- **Network Issues**: Connectivity problems

### **Node Reactivation**

After maintenance is complete:

```bash
# Reactivate node (if deactivation feature exists)
# Note: This command may not be available yet
htcli node activate --subnet-id 1 --node-id 2
```

### **Permanent Removal**

When permanently shutting down a node:

```bash
# Remove node permanently
htcli node remove --subnet-id 1 --node-id 2
```

**What happens during removal**:

1. **Warning Display**: Shows consequences of permanent removal
2. **Confirmation Required**: Must explicitly confirm operation
3. **Immediate Deactivation**: Node stops all operations
4. **Stake Unbonding**: All stake enters unbonding period
5. **Permanent Deletion**: Node record permanently removed

**Cannot be reversed**: Once removed, the node must be re-registered as a new node.

### **Stake Management for Nodes**

Node operators can manage stake on their nodes:

```bash
# Add more stake to your node
htcli stake add \
  --subnet-id 1 \
  --node-id 2 \
  --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY \
  --amount 2000000000000000000

# Remove stake from your node
htcli stake remove \
  --subnet-id 1 \
  --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY \
  --amount 1000000000000000000

# Check stake information
htcli stake info --address 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY --subnet-id 1
```

## 🚀 **Performance Optimization**

### **Performance Factors**

Several factors affect node performance:

#### **Hardware Resources**

- **CPU Performance**: Processing power for computations
- **Memory Capacity**: RAM for handling large datasets
- **Storage Speed**: Fast SSD for data access
- **Network Bandwidth**: High-speed internet connection

#### **Software Configuration**

- **Node Software Version**: Keep updated to latest version
- **Configuration Tuning**: Optimize settings for workload
- **Resource Allocation**: Proper CPU and memory allocation
- **Monitoring Tools**: Use performance monitoring

#### **Network Factors**

- **Connectivity**: Stable, high-speed internet connection
- **Peer Connections**: Good connectivity to other nodes
- **Latency**: Low latency to network infrastructure
- **Uptime**: Consistent availability and reliability

### **Performance Monitoring**

```bash
#!/bin/bash
# performance-optimization.sh

SUBNET_ID=1
NODE_ID=2

echo "=== Performance Analysis ==="

# Get current performance
CURRENT_PERF=$(htcli node status --subnet-id $SUBNET_ID --node-id $NODE_ID --format json | jq -r '.performance_score')
echo "Current Performance Score: $CURRENT_PERF"

# Compare with subnet average
SUBNET_DATA=$(htcli node list --subnet-id $SUBNET_ID --format json)
AVG_PERF=$(echo $SUBNET_DATA | jq '[.[] | .performance_score] | add / length')
echo "Subnet Average Performance: $AVG_PERF"

# Performance ranking
RANK=$(echo $SUBNET_DATA | jq --arg node_id "$NODE_ID" '
    sort_by(.performance_score) | reverse |
    map(.node_id) | index($node_id | tonumber) + 1'
)
TOTAL_NODES=$(echo $SUBNET_DATA | jq 'length')
echo "Performance Rank: $RANK out of $TOTAL_NODES"

# Recommendations
if (( $(echo "$CURRENT_PERF < $AVG_PERF" | bc -l) )); then
    echo "⚠️ Performance below average. Consider:"
    echo "   - Check node resource utilization"
    echo "   - Verify network connectivity"
    echo "   - Update node software"
    echo "   - Review configuration settings"
fi
```

### **Optimization Strategies**

#### **Resource Optimization**

```bash
#!/bin/bash
# resource-check.sh

echo "=== Resource Utilization Check ==="

# CPU usage
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | sed 's/%us,//')
echo "CPU Usage: $CPU_USAGE%"

# Memory usage
MEMORY_USAGE=$(free | grep Mem | awk '{printf("%.1f%%", $3/$2 * 100.0)}')
echo "Memory Usage: $MEMORY_USAGE"

# Disk usage
DISK_USAGE=$(df -h / | awk 'NR==2{printf "%s", $5}')
echo "Disk Usage: $DISK_USAGE"

# Network connectivity test
echo "Testing network connectivity..."
if ping -c 3 hypertensor.duckdns.org > /dev/null 2>&1; then
    echo "✅ Network connectivity: OK"
else
    echo "❌ Network connectivity: FAILED"
fi
```

#### **Configuration Tuning**

```bash
#!/bin/bash
# optimize-config.sh

echo "=== Configuration Optimization ==="

# Check node configuration
echo "Current node configuration:"
# (Add commands to check your specific node software configuration)

echo "Optimization recommendations:"
echo "1. Ensure adequate CPU allocation"
echo "2. Configure memory limits appropriately"
echo "3. Set proper connection limits"
echo "4. Enable performance monitoring"
echo "5. Configure automatic restarts"
```

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Node Not Appearing in Subnet**

```bash
# Check if node registration was successful
htcli node list --subnet-id 1 | grep "your-node-id"

# Verify transaction was confirmed
htcli chain account --address 5GrwvaEF... --format json

# Check if node is in queue
htcli subnet info --subnet-id 1
```

**Possible causes**:

- Transaction not confirmed
- Insufficient stake
- Subnet capacity full
- Invalid parameters

#### **Poor Performance Scores**

```bash
# Check node status and metrics
htcli node status --subnet-id 1 --node-id 2

# Compare with other nodes
htcli node list --subnet-id 1 --format json | jq '.[] | {node_id, performance_score}'

# Check network connectivity
ping -c 10 hypertensor.duckdns.org
```

**Possible causes**:

- Insufficient resources
- Network connectivity issues
- Outdated node software
- Configuration problems

#### **Node Stuck in Inactive State**

```bash
# Check node status
htcli node status --subnet-id 1 --node-id 2

# Verify stake requirements
htcli subnet info --subnet-id 1

# Check for any penalties or issues
htcli stake info --address 5GrwvaEF... --subnet-id 1
```

**Possible solutions**:

- Add more stake if below minimum
- Check for network penalties
- Verify node software is running
- Contact network support

### **Diagnostic Scripts**

#### **Node Health Check**

```bash
#!/bin/bash
# node-health-check.sh

SUBNET_ID=1
NODE_ID=2
HOTKEY="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"

echo "=== Node Health Check ==="
echo "Subnet: $SUBNET_ID, Node: $NODE_ID"
echo "Timestamp: $(date)"
echo

# 1. Check node exists and status
echo "1. Checking node existence..."
NODE_EXISTS=$(htcli node list --subnet-id $SUBNET_ID --format json | jq --arg node_id "$NODE_ID" '.[] | select(.node_id == ($node_id | tonumber))')

if [ -z "$NODE_EXISTS" ]; then
    echo "❌ Node not found in subnet"
    exit 1
else
    echo "✅ Node found in subnet"
fi

# 2. Check node status
echo -e "\n2. Checking node status..."
NODE_STATUS=$(echo $NODE_EXISTS | jq -r '.status')
echo "Status: $NODE_STATUS"

if [ "$NODE_STATUS" != "active" ]; then
    echo "⚠️ Node is not active"
fi

# 3. Check stake amount
echo -e "\n3. Checking stake..."
STAKE_AMOUNT=$(echo $NODE_EXISTS | jq -r '.stake')
echo "Current Stake: $STAKE_AMOUNT wei"

# 4. Check performance
echo -e "\n4. Checking performance..."
PERFORMANCE=$(echo $NODE_EXISTS | jq -r '.performance_score // "N/A"')
echo "Performance Score: $PERFORMANCE"

# 5. Network connectivity
echo -e "\n5. Testing network connectivity..."
if ping -c 3 hypertensor.duckdns.org > /dev/null 2>&1; then
    echo "✅ Network connectivity: OK"
else
    echo "❌ Network connectivity: FAILED"
fi

echo -e "\n=== Health Check Complete ==="
```

## 💡 **Best Practices**

### **Node Operation Best Practices**

#### **Security**

1. **Secure Key Management**: Store hotkeys securely
2. **Regular Updates**: Keep node software updated
3. **Access Control**: Limit access to node infrastructure
4. **Monitoring**: Implement comprehensive monitoring
5. **Backup**: Regular backup of critical data

#### **Performance**

1. **Resource Monitoring**: Track CPU, memory, disk, network
2. **Regular Maintenance**: Schedule maintenance windows
3. **Performance Tuning**: Optimize configuration regularly
4. **Capacity Planning**: Plan for growth and scaling
5. **Redundancy**: Consider backup nodes for critical operations

#### **Financial Management**

1. **Stake Optimization**: Maintain optimal stake levels
2. **Reward Monitoring**: Track reward generation
3. **Cost Analysis**: Monitor operational costs
4. **ROI Calculation**: Calculate return on investment
5. **Risk Management**: Diversify across multiple subnets

### **Operational Procedures**

#### **Daily Operations**

```bash
#!/bin/bash
# daily-operations.sh

echo "=== Daily Node Operations Check ==="

# Check all nodes status
for subnet_id in 1 2 3; do
    echo "Checking subnet $subnet_id nodes..."
    htcli node list --subnet-id $subnet_id
done

# Check stake positions
echo "Checking stake positions..."
htcli stake info --address $HOTKEY

# Check overall network health
echo "Checking network health..."
htcli chain network
```

#### **Weekly Maintenance**

```bash
#!/bin/bash
# weekly-maintenance.sh

echo "=== Weekly Maintenance ==="

# Performance analysis
echo "Analyzing performance trends..."
# (Add your performance analysis logic)

# Stake rebalancing check
echo "Checking stake rebalancing needs..."
# (Add your rebalancing logic)

# Update checks
echo "Checking for updates..."
# (Add your update checking logic)
```

#### **Monthly Review**

```bash
#!/bin/bash
# monthly-review.sh

echo "=== Monthly Node Review ==="

# Generate performance report
echo "Generating performance report..."
# (Add comprehensive reporting logic)

# Financial analysis
echo "Analyzing financial performance..."
# (Add ROI and cost analysis)

# Strategic planning
echo "Strategic planning recommendations..."
# (Add strategic recommendations)
```

This comprehensive node management guide covers all aspects of operating nodes in the Hypertensor network, from initial registration through ongoing optimization and maintenance.
