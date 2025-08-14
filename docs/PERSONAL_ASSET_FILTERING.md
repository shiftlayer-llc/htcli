# Personal Asset Filtering Guide

Complete guide to using the universal `--mine` flag for filtering commands to show only your personal assets across the Hypertensor network.

## 🎯 Overview

The Hypertensor CLI provides a universal `--mine` flag that works across all commands to filter results and show only assets owned by your locally stored wallet addresses. This feature enables personalized portfolio management and asset tracking.

## 🔍 Universal --mine Flag

### Basic Usage
```bash
# View only your subnets
htcli subnet list --mine

# View only your stakes
htcli stake info --mine

# View only your nodes
htcli node list --mine
```

### Works Across All Commands
The `--mine` flag works with any command that returns asset lists:
```bash
# Subnet operations
htcli subnet list --mine
htcli subnet info --subnet-id 1 --mine

# Node operations
htcli node list --mine
htcli node status --subnet-id 1 --node-id 5 --mine

# Staking operations
htcli stake info --mine
htcli stake delegate-add --subnet-id 1 --amount 1000000000000000000 --key-name my-key --mine

# Chain queries
htcli chain balance --address <your-address> --mine
```

## 💼 Personal Asset Management

### Subnet Portfolio
```bash
# View all subnets you own
htcli subnet list --mine

# Get detailed info about your subnets
htcli subnet info --subnet-id 1 --mine
htcli subnet info --subnet-id 2 --mine
htcli subnet info --subnet-id 3 --mine
```

### Node Portfolio
```bash
# View all nodes you operate
htcli node list --mine

# Get status of your nodes
htcli node status --subnet-id 1 --node-id 5 --mine
htcli node status --subnet-id 1 --node-id 10 --mine
```

### Staking Portfolio
```bash
# View all your stakes
htcli stake info --mine

# View stakes in specific subnets
htcli stake info --subnet-id 1 --mine
htcli stake info --subnet-id 2 --mine

# View stakes in specific nodes
htcli stake info --subnet-id 1 --node-id 5 --mine
```

## 🔧 How It Works

### Address Detection
The `--mine` flag automatically detects your locally stored wallet addresses:
1. **Key Storage**: Reads from your local key storage
2. **Address Extraction**: Extracts SS58 addresses from stored keys
3. **Asset Filtering**: Filters results to show only assets owned by these addresses
4. **Real-time Updates**: Updates as you add/remove keys

### Supported Asset Types
- **Subnets**: Subnets you own or have ownership stake in
- **Nodes**: Nodes you operate or have registered
- **Stakes**: All your staking positions (subnet and node)
- **Balances**: Account balances for your addresses
- **Transactions**: Transactions involving your addresses

## 📊 Portfolio Management

### Complete Portfolio Overview
```bash
# Get complete portfolio overview
echo "=== MY HYPERTENSOR PORTFOLIO ==="
echo "Subnets:"
htcli subnet list --mine --format table

echo "Nodes:"
htcli node list --mine --format table

echo "Stakes:"
htcli stake info --mine --format table

echo "Balances:"
htcli chain balance --mine --format table
```

### Portfolio Analysis
```bash
# Analyze subnet portfolio
echo "=== SUBNET PORTFOLIO ANALYSIS ==="
htcli subnet list --mine --format json | jq '.[] | {id: .id, name: .name, status: .status}'

# Analyze node portfolio
echo "=== NODE PORTFOLIO ANALYSIS ==="
htcli node list --mine --format json | jq '.[] | {id: .id, subnet_id: .subnet_id, status: .status, stake: .stake_amount}'

# Analyze staking portfolio
echo "=== STAKING PORTFOLIO ANALYSIS ==="
htcli stake info --mine --format json | jq '.[] | {type: .type, amount: .amount, reward_rate: .reward_rate}'
```

### Performance Tracking
```bash
# Track portfolio performance over time
#!/bin/bash
DATE=$(date +"%Y-%m-%d %H:%M:%S")
echo "=== PORTFOLIO STATUS - $DATE ===" >> portfolio.log

echo "Subnets:" >> portfolio.log
htcli subnet list --mine --format json >> portfolio.log

echo "Nodes:" >> portfolio.log
htcli node list --mine --format json >> portfolio.log

echo "Stakes:" >> portfolio.log
htcli stake info --mine --format json >> portfolio.log

echo "---" >> portfolio.log
```

## 🎯 Use Cases

### Personal Dashboard
```bash
#!/bin/bash
# Personal Hypertensor Dashboard

echo "🚀 HYPERTENSOR PERSONAL DASHBOARD"
echo "=================================="

echo "📊 NETWORK STATUS"
htcli chain info --format table

echo ""
echo "🔑 MY SUBNETS"
htcli subnet list --mine --format table

echo ""
echo "🔗 MY NODES"
htcli node list --mine --format table

echo ""
echo "💰 MY STAKES"
htcli stake info --mine --format table

echo ""
echo "💳 MY BALANCES"
htcli chain balance --mine --format table
```

### Portfolio Monitoring
```bash
#!/bin/bash
# Portfolio monitoring script

while true; do
    clear
    echo "=== PORTFOLIO MONITOR ==="
    echo "Time: $(date)"
    echo ""
    
    echo "Subnets: $(htcli subnet list --mine --format json | jq length)"
    echo "Nodes: $(htcli node list --mine --format json | jq length)"
    echo "Stakes: $(htcli stake info --mine --format json | jq length)"
    
    sleep 30
done
```

### Asset Tracking
```bash
#!/bin/bash
# Asset tracking script

echo "=== ASSET TRACKING REPORT ==="
echo "Generated: $(date)"
echo ""

# Track subnets
echo "SUBNETS:"
htcli subnet list --mine --format json | jq -r '.[] | "  - \(.name) (ID: \(.id))"'

# Track nodes
echo ""
echo "NODES:"
htcli node list --mine --format json | jq -r '.[] | "  - Node \(.id) in Subnet \(.subnet_id)"'

# Track stakes
echo ""
echo "STAKES:"
htcli stake info --mine --format json | jq -r '.[] | "  - \(.amount) in \(.type)"'
```

## 🔧 Advanced Filtering

### Combined Filtering
```bash
# Filter by subnet and ownership
htcli node list --subnet-id 1 --mine

# Filter by node and ownership
htcli stake info --subnet-id 1 --node-id 5 --mine

# Filter by address and ownership
htcli chain balance --address <specific-address> --mine
```

### Custom Filtering Scripts
```bash
#!/bin/bash
# Custom filtering script

# Get only active subnets you own
htcli subnet list --mine --format json | jq '[.[] | select(.status == "Active")]'

# Get only validator nodes you operate
htcli node list --mine --format json | jq '[.[] | select(.classification == "Validator")]'

# Get only high-value stakes
htcli stake info --mine --format json | jq '[.[] | select(.amount > 1000000000000000000)]'
```

## 📈 Portfolio Analytics

### Performance Metrics
```bash
#!/bin/bash
# Portfolio performance analysis

echo "=== PORTFOLIO PERFORMANCE ANALYSIS ==="

# Calculate total staked
TOTAL_STAKED=$(htcli stake info --mine --format json | jq 'map(.amount) | add')
echo "Total Staked: $TOTAL_STAKED"

# Calculate average reward rate
AVG_RATE=$(htcli stake info --mine --format json | jq 'map(.reward_rate) | add / length')
echo "Average Reward Rate: $AVG_RATE"

# Count active nodes
ACTIVE_NODES=$(htcli node list --mine --format json | jq '[.[] | select(.status == "Active")] | length')
echo "Active Nodes: $ACTIVE_NODES"

# Count owned subnets
OWNED_SUBNETS=$(htcli subnet list --mine --format json | jq '[.[] | select(.owner == $ADDRESS)] | length')
echo "Owned Subnets: $OWNED_SUBNETS"
```

### Risk Analysis
```bash
#!/bin/bash
# Portfolio risk analysis

echo "=== PORTFOLIO RISK ANALYSIS ==="

# Check for underperforming nodes
UNDERPERFORMING=$(htcli node list --mine --format json | jq '[.[] | select(.attestation_ratio < 0.8)] | length')
echo "Underperforming Nodes: $UNDERPERFORMING"

# Check for low-reward stakes
LOW_REWARD=$(htcli stake info --mine --format json | jq '[.[] | select(.reward_rate < 50000000000000000)] | length')
echo "Low-Reward Stakes: $LOW_REWARD"

# Check for high-concentration risks
HIGH_CONCENTRATION=$(htcli stake info --mine --format json | jq 'group_by(.subnet_id) | map(select(length > 3)) | length')
echo "High-Concentration Subnets: $HIGH_CONCENTRATION"
```

## 🔄 Automation Examples

### Automated Portfolio Monitoring
```bash
#!/bin/bash
# Automated portfolio monitoring

while true; do
    # Check for new assets
    NEW_SUBNETS=$(htcli subnet list --mine --format json | jq length)
    NEW_NODES=$(htcli node list --mine --format json | jq length)
    NEW_STAKES=$(htcli stake info --mine --format json | jq length)
    
    # Alert if portfolio changes
    if [ "$NEW_SUBNETS" != "$PREV_SUBNETS" ]; then
        echo "Alert: Subnet count changed from $PREV_SUBNETS to $NEW_SUBNETS"
    fi
    
    if [ "$NEW_NODES" != "$PREV_NODES" ]; then
        echo "Alert: Node count changed from $PREV_NODES to $NEW_NODES"
    fi
    
    if [ "$NEW_STAKES" != "$PREV_STAKES" ]; then
        echo "Alert: Stake count changed from $PREV_STAKES to $NEW_STAKES"
    fi
    
    # Update previous values
    PREV_SUBNETS=$NEW_SUBNETS
    PREV_NODES=$NEW_NODES
    PREV_STAKES=$NEW_STAKES
    
    sleep 300  # Check every 5 minutes
done
```

### Portfolio Rebalancing
```bash
#!/bin/bash
# Portfolio rebalancing script

# Get current portfolio
CURRENT_STAKES=$(htcli stake info --mine --format json)

# Calculate target allocation
TOTAL_STAKED=$(echo $CURRENT_STAKES | jq 'map(.amount) | add')
TARGET_PER_SUBNET=$((TOTAL_STAKED / 5))  # Equal allocation across 5 subnets

# Rebalance if needed
echo $CURRENT_STAKES | jq -r '.[] | select(.amount > $TARGET_PER_SUBNET) | "Rebalance: \(.subnet_id) has \(.amount)"'
```

## 🛡️ Security Considerations

### Key Management
- **Secure Storage**: Ensure keys are stored securely
- **Access Control**: Limit access to keys used for filtering
- **Backup Strategy**: Regular backup of key storage
- **Monitoring**: Monitor for unauthorized key access

### Privacy Protection
- **Local Processing**: All filtering happens locally
- **No Data Transmission**: No personal data sent to external services
- **Key Encryption**: Keys are encrypted at rest
- **Access Logging**: Log access to personal asset data

## 📊 Best Practices

### Regular Monitoring
```bash
# Daily portfolio check
htcli subnet list --mine
htcli node list --mine
htcli stake info --mine

# Weekly performance review
htcli node status --mine
htcli stake info --mine --format json | jq 'map(.performance) | add / length'
```

### Portfolio Optimization
```bash
# Identify optimization opportunities
htcli stake info --mine --format json | jq 'group_by(.reward_rate) | sort_by(.[0].reward_rate) | reverse'

# Track performance trends
htcli node list --mine --format json | jq 'map(.attestation_ratio) | sort'
```

### Documentation
```bash
# Document portfolio changes
echo "$(date): Portfolio Update" >> portfolio_changes.log
htcli subnet list --mine --format json >> portfolio_changes.log
htcli node list --mine --format json >> portfolio_changes.log
htcli stake info --mine --format json >> portfolio_changes.log
```

---

**The universal `--mine` flag provides powerful personal asset filtering capabilities, enabling comprehensive portfolio management, monitoring, and optimization across all Hypertensor network assets.** 🚀
