# Hypertensor CLI Staking Guide

This comprehensive guide covers all aspects of staking operations using the Hypertensor CLI, from basic concepts to advanced strategies.

## 📋 **Table of Contents**

1. [Staking Overview](#staking-overview)
2. [Staking Concepts](#staking-concepts)
3. [Getting Started](#getting-started)
4. [Basic Staking Operations](#basic-staking-operations)
5. [Delegate Staking](#delegate-staking)
6. [Staking Management](#staking-management)
7. [Unbonding and Claims](#unbonding-and-claims)
8. [Staking Strategies](#staking-strategies)
9. [Risk Management](#risk-management)
10. [Troubleshooting](#troubleshooting)

## 🎯 **Staking Overview**

Staking in the Hypertensor network allows TENSOR token holders to:

- **Earn Rewards**: Generate passive income from network participation
- **Secure the Network**: Contribute to network security and consensus
- **Support Nodes**: Help fund and incentivize node operators
- **Participate in Governance**: Have a voice in network decisions

### **Key Benefits**

- **Passive Income**: Earn rewards proportional to stake amount
- **Network Growth**: Benefit from network expansion and adoption
- **Flexible Management**: Add, remove, and transfer stakes as needed
- **Multiple Options**: Direct staking and delegate staking available
- **🆕 Personal Portfolio Management**: Use `--mine` to track all your stakes across multiple addresses

## 🧠 **Staking Concepts**

### **Direct Node Staking**

Staking directly to specific nodes in subnets:

- **Higher Control**: Choose specific nodes to support
- **Direct Rewards**: Earn rewards based on node performance
- **Node Selection**: Research and select high-performing nodes
- **Risk/Reward**: Higher potential rewards with node-specific risks

### **Delegate Staking**

Staking to subnet pools without choosing specific nodes:

- **Simplified Management**: Stake to entire subnet pools
- **Diversified Risk**: Spread risk across multiple nodes
- **Lower Maintenance**: Less research and monitoring required
- **Balanced Returns**: Steady returns with reduced volatility

### **TENSOR Token Precision**

All staking operations use **18-digit precision**:

- **Smallest Unit**: 1 wei = 0.000000000000000001 TENSOR
- **1 TENSOR**: 1,000,000,000,000,000,000 wei
- **Precision Matters**: Always specify amounts in smallest units

### **🆕 Personal Staking Portfolio Management**

The CLI provides powerful tools to manage your staking portfolio across multiple addresses:

#### **Network View vs Personal View**

```bash
# 📊 NETWORK VIEW: See stakes for specific address
htcli stake info --address 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY

# 👤 PERSONAL VIEW: See ALL your stakes across ALL your addresses
htcli --mine stake info
```

#### **Automatic Multi-Address Management**

- **Smart Detection**: Automatically finds all your wallet addresses from `~/.htcli/wallets/`
- **Comprehensive View**: Shows stakes across all your addresses in one command
- **Clear Ownership**: Distinguishes your stakes from network-wide data
- **Portfolio Summary**: Provides totals and summaries for your entire staking portfolio

### **Unbonding Period**

When removing stake:

- **Unbonding Period**: Tokens are locked for a specific period
- **No Rewards**: Unbonding tokens don't earn rewards
- **Claim Process**: Must claim tokens after unbonding period
- **Security Feature**: Prevents rapid stake movements

## 🚀 **Getting Started**

### **Prerequisites**

Before staking, ensure you have:

1. **Configured CLI**: Run `htcli config init`
2. **Generated Keys**: Create keys with `htcli wallet generate-key`
3. **TENSOR Tokens**: Sufficient balance for staking
4. **Network Access**: Connection to Hypertensor network

### **Check Your Balance**

```bash
# Check your current balance
htcli chain balance --address 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY

# Expected output shows 18-digit precision
Free Balance: 100.000000000000000000 TENSOR
Reserved Balance: 0.000000000000000000 TENSOR
Total Balance: 100.000000000000000000 TENSOR
```

### **Explore Available Subnets**

```bash
# List all subnets
htcli subnet list

# Get detailed subnet information
htcli subnet info --subnet-id 1

# Check nodes in subnet
htcli node list --subnet-id 1
```

### **Research Nodes**

```bash
# Get detailed node status
htcli node status --subnet-id 1 --node-id 2

# Check node performance history
htcli node list --subnet-id 1 --format json
```

## 💰 **Basic Staking Operations**

### **Adding Stake to a Node**

#### **With Comprehensive Guidance**

```bash
htcli stake add \
  --subnet-id 1 \
  --node-id 2 \
  --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY \
  --amount 1000000000000000000
```

This will show comprehensive guidance:

```
╭────────────────────── 💰 Adding Stake to Node ──────────────────────────╮
│ This operation will stake TENSOR tokens to support a node in a subnet.   │
│                                                                          │
│ 📋 Requirements:                                                         │
│ • Valid subnet ID and node ID                                            │
│ • Sufficient TENSOR balance in your account                              │
│ • Node must be active and accepting stake                                │
│                                                                          │
│ 💡 Tips & Warnings:                                                      │
│ 💡 Staked tokens are locked and earn rewards                             │
│ ⚠️ Unstaking has an unbonding period before tokens are available        │
╰──────────────────────────────────────────────────────────────────────────╯
```

#### **For Scripting (No Guidance)**

```bash
htcli stake add \
  --subnet-id 1 \
  --node-id 2 \
  --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY \
  --amount 1000000000000000000 \
  --no-guidance
```

#### **Common Stake Amounts**

```bash
# 1 TENSOR (1 with 18 zeros)
--amount 1000000000000000000

# 10 TENSOR
--amount 10000000000000000000

# 100 TENSOR
--amount 100000000000000000000

# 0.1 TENSOR (100 with 15 zeros)
--amount 100000000000000000
```

### **Checking Stake Information**

#### **Your Stake Positions**

```bash
# Check all stakes for an address
htcli stake info --address 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY

# Check stake for specific subnet
htcli stake info \
  --address 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY \
  --subnet-id 1

# Get stake data as JSON for processing
htcli stake info \
  --address 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY \
  --format json
```

#### **Stake Information Includes**

- **Current Stake Positions**: Active stakes per subnet/node
- **Earned Rewards**: Accumulated rewards and rates
- **Unbonding Positions**: Tokens in unbonding period
- **Total Staked**: Sum of all staking positions

### **Removing Stake**

#### **Partial Stake Removal**

```bash
htcli stake remove \
  --subnet-id 1 \
  --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY \
  --amount 500000000000000000
```

#### **What Happens When Removing Stake**

1. **Warning Displayed**: Shows unbonding period information
2. **Confirmation Required**: User must confirm the operation
3. **Unbonding Initiated**: Tokens enter unbonding period
4. **Rewards Stop**: No more rewards on removed amount
5. **Claim Later**: Must claim tokens after unbonding period

## 🤝 **Delegate Staking**

Delegate staking allows you to stake to subnet pools without selecting specific nodes.

### **Adding Delegate Stake**

```bash
htcli stake delegate-add \
  --subnet-id 1 \
  --amount 5000000000000000000
```

### **Benefits of Delegate Staking**

- **Simplified Management**: No need to research individual nodes
- **Risk Distribution**: Stake distributed across multiple nodes
- **Automatic Rebalancing**: Pool automatically optimizes distribution
- **Lower Maintenance**: Less monitoring required

### **Removing Delegate Stake**

```bash
htcli stake delegate-remove \
  --subnet-id 1 \
  --shares 1000
```

**Note**: Delegate staking uses "shares" rather than exact token amounts.

### **Transferring Between Subnets**

```bash
htcli stake delegate-transfer \
  --from-subnet 1 \
  --to-subnet 2 \
  --shares 500
```

This allows you to move delegate stakes between subnets without unbonding.

## 📊 **Staking Management**

### **Monitoring Your Stakes**

#### **Regular Monitoring Script**

```bash
#!/bin/bash
# stake-monitor.sh

ADDRESS="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"

echo "=== Current Balance ==="
htcli chain balance --address $ADDRESS

echo -e "\n=== Stake Positions ==="
htcli stake info --address $ADDRESS --format table

echo -e "\n=== Network Status ==="
htcli chain network
```

#### **JSON Data Processing**

```bash
#!/bin/bash
# Process stake data with jq

ADDRESS="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"

# Get total staked amount
TOTAL_STAKED=$(htcli stake info --address $ADDRESS --format json | jq '.total_staked')

# Get rewards earned
REWARDS=$(htcli stake info --address $ADDRESS --format json | jq '.total_rewards')

echo "Total Staked: $TOTAL_STAKED wei"
echo "Total Rewards: $REWARDS wei"
```

### **Performance Tracking**

#### **Node Performance Monitoring**

```bash
# Check performance of nodes you're staking to
for node_id in 1 2 3; do
    echo "Node $node_id Status:"
    htcli node status --subnet-id 1 --node-id $node_id --format json | jq '.performance'
done
```

#### **Subnet Performance Comparison**

```bash
# Compare different subnets
for subnet_id in 1 2 3; do
    echo "Subnet $subnet_id Info:"
    htcli subnet info --subnet-id $subnet_id --format json | jq '.statistics'
done
```

### **Portfolio Rebalancing**

#### **Rebalancing Strategy**

```bash
#!/bin/bash
# rebalance-stakes.sh

ADDRESS="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"

# Get current stake distribution
STAKE_DATA=$(htcli stake info --address $ADDRESS --format json)

# Analyze performance and rebalance
# (Add your rebalancing logic here)

# Example: Move stake from underperforming node
htcli stake remove --subnet-id 1 --hotkey $ADDRESS --amount 1000000000000000000

# Add stake to better performing node
htcli stake add --subnet-id 2 --node-id 3 --hotkey $ADDRESS --amount 1000000000000000000
```

## ⏰ **Unbonding and Claims**

### **Understanding Unbonding**

When you remove stake:

1. **Unbonding Period Starts**: Tokens are locked for a specific period
2. **No Rewards**: Unbonding tokens don't earn rewards
3. **Cannot Use**: Tokens are not available for transactions
4. **Must Claim**: After period ends, must claim to access tokens

### **Checking Unbonding Status**

```bash
# Check your stake info to see unbonding positions
htcli stake info --address 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
```

Look for unbonding information in the output:

- **Unbonding Amount**: How many tokens are unbonding
- **Unbonding Period**: When tokens will be available
- **Claimable Amount**: Tokens ready to claim

### **Claiming Unbonded Tokens**

```bash
htcli stake claim --hotkey 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
```

This will:

1. Check for completed unbondings
2. Claim all available tokens
3. Return tokens to your free balance
4. Display transaction confirmation

### **Automated Claiming Script**

```bash
#!/bin/bash
# auto-claim.sh

HOTKEY="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"

# Check if there are claimable tokens
STAKE_INFO=$(htcli stake info --address $HOTKEY --format json)
CLAIMABLE=$(echo $STAKE_INFO | jq '.claimable_amount')

if [ "$CLAIMABLE" != "0" ]; then
    echo "Claiming $CLAIMABLE tokens..."
    htcli stake claim --hotkey $HOTKEY --no-guidance
else
    echo "No tokens available to claim"
fi
```

## 📈 **Staking Strategies**

### **Conservative Strategy**

**Goal**: Steady returns with minimal risk

```bash
# Diversify across multiple high-performing subnets
htcli stake delegate-add --subnet-id 1 --amount 2000000000000000000
htcli stake delegate-add --subnet-id 2 --amount 2000000000000000000
htcli stake delegate-add --subnet-id 3 --amount 1000000000000000000

# Monitor and rebalance quarterly
# Focus on established subnets with consistent performance
```

### **Growth Strategy**

**Goal**: Higher returns with moderate risk

```bash
# Mix of delegate and direct staking
# 60% delegate staking for stability
htcli stake delegate-add --subnet-id 1 --amount 3000000000000000000

# 40% direct staking to high-performing nodes
htcli stake add --subnet-id 2 --node-id 5 --hotkey $HOTKEY --amount 2000000000000000000
```

### **Aggressive Strategy**

**Goal**: Maximum returns with higher risk

```bash
# Direct staking to carefully selected high-performance nodes
htcli stake add --subnet-id 1 --node-id 3 --hotkey $HOTKEY --amount 2500000000000000000
htcli stake add --subnet-id 2 --node-id 7 --hotkey $HOTKEY --amount 2500000000000000000

# Active monitoring and frequent rebalancing
# Quick response to performance changes
```

### **Dollar-Cost Averaging**

**Goal**: Reduce timing risk through regular investments

```bash
#!/bin/bash
# dca-staking.sh - Run weekly

WEEKLY_AMOUNT="500000000000000000"  # 0.5 TENSOR per week
HOTKEY="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"

# Rotate between different subnets
WEEK=$(date +%V)
SUBNET_ID=$((($WEEK % 3) + 1))

htcli stake delegate-add --subnet-id $SUBNET_ID --amount $WEEKLY_AMOUNT --no-guidance
```

## ⚠️ **Risk Management**

### **Understanding Risks**

#### **Node Performance Risk**

- **Poor Performance**: Nodes may underperform expectations
- **Slashing**: Nodes may be penalized for bad behavior
- **Downtime**: Nodes may go offline and miss rewards

#### **Market Risk**

- **Token Price**: TENSOR price volatility affects returns
- **Network Changes**: Protocol updates may affect rewards
- **Competition**: New nodes may reduce existing rewards

#### **Liquidity Risk**

- **Unbonding Period**: Tokens locked during unstaking
- **Market Timing**: May need to unstake during poor conditions
- **Opportunity Cost**: Staked tokens can't be used elsewhere

### **Risk Mitigation Strategies**

#### **Diversification**

```bash
# Spread stakes across multiple subnets
htcli stake delegate-add --subnet-id 1 --amount 1000000000000000000
htcli stake delegate-add --subnet-id 2 --amount 1000000000000000000
htcli stake delegate-add --subnet-id 3 --amount 1000000000000000000
htcli stake delegate-add --subnet-id 4 --amount 1000000000000000000
```

#### **Position Sizing**

```bash
# Never stake more than you can afford to lose
# Example: 50% of holdings maximum in staking
TOTAL_BALANCE=$(htcli chain balance --address $ADDRESS --format json | jq '.free')
MAX_STAKE=$(echo "$TOTAL_BALANCE * 0.5" | bc)

echo "Maximum recommended stake: $MAX_STAKE wei"
```

#### **Regular Monitoring**

```bash
#!/bin/bash
# risk-monitor.sh

ADDRESS="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"

# Check for underperforming positions
STAKE_INFO=$(htcli stake info --address $ADDRESS --format json)

# Alert if any position is underperforming
# (Add your alerting logic here)

# Consider rebalancing if needed
```

### **Emergency Procedures**

#### **Rapid Unstaking**

```bash
#!/bin/bash
# emergency-unstake.sh

HOTKEY="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"

echo "Emergency unstaking initiated..."

# Remove all direct stakes
htcli stake remove --subnet-id 1 --hotkey $HOTKEY --amount 1000000000000000000 --no-guidance
htcli stake remove --subnet-id 2 --hotkey $HOTKEY --amount 1000000000000000000 --no-guidance

# Remove delegate stakes
htcli stake delegate-remove --subnet-id 1 --shares 1000 --no-guidance
htcli stake delegate-remove --subnet-id 2 --shares 1000 --no-guidance

echo "Emergency unstaking complete. Tokens will be available after unbonding period."
```

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Insufficient Balance**

```bash
# Error: Insufficient balance for staking
# Solution: Check your balance and ensure sufficient funds

htcli chain balance --address $ADDRESS
# Ensure you have enough for staking + transaction fees
```

#### **Node Not Accepting Stake**

```bash
# Error: Node not accepting stake
# Solution: Check node status and capacity

htcli node status --subnet-id 1 --node-id 2
# Look for node capacity and acceptance status
```

#### **Unbonding Period Not Complete**

```bash
# Error: Cannot claim, unbonding period not complete
# Solution: Check unbonding status

htcli stake info --address $ADDRESS
# Check when unbonding period ends
```

### **Performance Issues**

#### **Low Rewards**

```bash
# Check node performance
htcli node status --subnet-id 1 --node-id 2

# Compare with other nodes
htcli node list --subnet-id 1 --format json | jq '.[] | {node_id, performance}'

# Consider moving stake to better performing nodes
```

#### **Stake Not Showing**

```bash
# Verify transaction was successful
htcli stake info --address $ADDRESS

# Check transaction hash in block explorer
# Wait for blockchain confirmation (may take a few blocks)
```

### **Recovery Procedures**

#### **Lost Transaction**

```bash
# Check recent transactions
htcli chain account --address $ADDRESS --format json

# Verify stake positions
htcli stake info --address $ADDRESS

# If stake is missing, check transaction status
```

#### **Configuration Issues**

```bash
# Reset configuration
htcli config init --force

# Test connection
htcli chain network

# Retry staking operation
```

This comprehensive staking guide covers all aspects of staking with the Hypertensor CLI, from basic concepts to advanced strategies and risk management. Use this guide to maximize your staking rewards while managing risks effectively.
