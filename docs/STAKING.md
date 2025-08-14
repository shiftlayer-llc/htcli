# Staking Guide

Complete guide to staking operations in the Hypertensor network, including subnet delegate staking, node delegate staking, and comprehensive portfolio management.

## 🎯 Overview

The Hypertensor CLI provides comprehensive staking capabilities for complete portfolio management:

- **Subnet Delegate Staking**: Stake to entire subnet pools
- **Node Delegate Staking**: Stake to specific nodes
- **Portfolio Management**: Diversify across multiple options
- **Reward Optimization**: Strategic rate management
- **Risk Management**: Comprehensive risk mitigation
- **Performance Monitoring**: Track staking performance

## 💰 Staking Types

### Subnet Delegate Staking
- **Pool Staking**: Stake to entire subnet pool
- **Subnet-Wide Rewards**: Rewards based on subnet performance
- **Lower Risk**: Diversified across all subnet nodes
- **Stable Returns**: Less affected by individual node performance
- **Simpler Strategy**: No need to select specific nodes

### Node Delegate Staking
- **Targeted Staking**: Stake to specific nodes
- **Node-Specific Rewards**: Rewards based on node's delegate reward rate
- **Higher Potential Returns**: Can offer better rates than subnet staking
- **Higher Risk**: Node performance directly affects returns
- **Node Selection**: Choose nodes based on performance

## 🔗 Subnet Delegate Staking

### Add Subnet Delegate Stake
```bash
htcli stake delegate-add \
  --subnet-id 1 \
  --amount 1000000000000000000 \
  --key-name my-staking-key
```

### Remove Subnet Delegate Stake
```bash
htcli stake delegate-remove \
  --subnet-id 1 \
  --shares 500000000000000000 \
  --key-name my-staking-key
```

### Transfer Subnet Delegate Stake
```bash
htcli stake delegate-transfer \
  --subnet-id 1 \
  --to-account 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu \
  --shares 100000000000000000 \
  --key-name my-staking-key
```

### Increase Subnet Delegate Stake Pool
```bash
htcli stake delegate-increase \
  --subnet-id 1 \
  --amount 500000000000000000 \
  --key-name my-staking-key
```

### Subnet Staking Benefits
- **Diversification**: Stake across all subnet nodes
- **Lower Risk**: Reduced exposure to individual node performance
- **Stable Returns**: Consistent reward streams
- **Simpler Management**: No need to monitor individual nodes
- **Network Support**: Support entire subnet ecosystem

## 🎯 Node Delegate Staking

### Add Node Delegate Stake
```bash
htcli stake node-add \
  --subnet-id 1 \
  --node-id 5 \
  --amount 1000000000000000000 \
  --key-name my-staking-key
```

### Remove Node Delegate Stake
```bash
htcli stake node-remove \
  --subnet-id 1 \
  --node-id 5 \
  --shares 500000000000000000 \
  --key-name my-staking-key
```

### Transfer Node Delegate Stake
```bash
htcli stake node-transfer \
  --subnet-id 1 \
  --node-id 5 \
  --to-account 5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK9iYqurHh9Qu \
  --shares 100000000000000000 \
  --key-name my-staking-key
```

### Increase Node Delegate Stake Pool
```bash
htcli stake node-increase \
  --subnet-id 1 \
  --node-id 5 \
  --amount 500000000000000000 \
  --key-name my-staking-key
```

### Node Staking Benefits
- **Higher Returns**: Potential for better rates than subnet staking
- **Node Selection**: Choose high-performing nodes
- **Rate Optimization**: Find nodes with competitive rates
- **Performance Tracking**: Monitor node performance
- **Strategic Positioning**: Target specific node strategies

## 📊 Staking Strategy

### Portfolio Diversification
```bash
# Diversify across subnets
htcli stake delegate-add --subnet-id 1 --amount 1000000000000000000 --key-name my-staking-key
htcli stake delegate-add --subnet-id 2 --amount 500000000000000000 --key-name my-staking-key
htcli stake delegate-add --subnet-id 3 --amount 500000000000000000 --key-name my-staking-key

# Diversify across nodes
htcli stake node-add --subnet-id 1 --node-id 5 --amount 500000000000000000 --key-name my-staking-key
htcli stake node-add --subnet-id 1 --node-id 10 --amount 300000000000000000 --key-name my-staking-key
htcli stake node-add --subnet-id 2 --node-id 3 --amount 200000000000000000 --key-name my-staking-key
```

### Risk Management
- **Subnet Diversification**: Spread stakes across multiple subnets
- **Node Diversification**: Spread stakes across multiple nodes
- **Amount Limits**: Set maximum stakes per subnet/node
- **Performance Monitoring**: Regular performance reviews
- **Exit Strategies**: Plan for stake removal scenarios

### Performance Optimization
- **Rate Comparison**: Compare reward rates across options
- **Performance Tracking**: Monitor node and subnet performance
- **Market Analysis**: Analyze competitive landscape
- **Strategic Adjustments**: Adjust stakes based on performance
- **Rebalancing**: Regular portfolio rebalancing

## 🔄 Stake Management

### Share vs Balance
- **Shares**: Your stake representation in the pool/node
- **Balance**: Actual tokens you receive back
- **Conversion**: Shares converted to balance automatically
- **Value**: Balance value depends on performance
- **Timing**: Conversion happens at current rates

### Transfer vs Removal
- **Transfer**: Shares move to another account (no conversion)
- **Removal**: Shares converted to balance for you
- **Ownership**: Transfer changes ownership, removal returns tokens
- **Earnings**: Transfer continues earning for destination, removal stops earning
- **Use Cases**: Transfer for gifting, removal for liquidity

### Pool Increase (Airdrop)
- **Community Benefits**: All delegators benefit proportionally
- **Immediate Distribution**: Rewards distributed immediately
- **Pool Value Growth**: Increases total pool value for everyone
- **Community Building**: Incentivizes delegation and loyalty
- **Marketing Tool**: Attracts new delegators

## 📈 Portfolio Management

### Monitor Portfolio
```bash
# View all your stakes
htcli stake info --mine

# View specific subnet stakes
htcli stake info --subnet-id 1 --mine

# View specific node stakes
htcli stake info --subnet-id 1 --node-id 5 --mine
```

### Portfolio Analysis
- **Total Staked**: Sum of all stakes across subnets and nodes
- **Reward Rates**: Current reward rates for each stake
- **Performance**: Historical performance of stakes
- **Risk Assessment**: Risk profile of portfolio
- **Optimization Opportunities**: Areas for improvement

### Rebalancing Strategy
```bash
# Remove underperforming stakes
htcli stake delegate-remove --subnet-id 1 --shares 200000000000000000 --key-name my-staking-key
htcli stake node-remove --subnet-id 1 --node-id 5 --shares 100000000000000000 --key-name my-staking-key

# Add to high-performing options
htcli stake delegate-add --subnet-id 2 --amount 300000000000000000 --key-name my-staking-key
htcli stake node-add --subnet-id 2 --node-id 8 --amount 200000000000000000 --key-name my-staking-key
```

## 🎯 Strategic Planning

### Research Phase
1. **Subnet Analysis**: Research subnet performance and stability
2. **Node Analysis**: Research individual node performance
3. **Rate Comparison**: Compare reward rates across options
4. **Risk Assessment**: Assess risk profiles of different options
5. **Market Analysis**: Analyze competitive landscape

### Planning Phase
1. **Portfolio Allocation**: Plan stake allocation across options
2. **Risk Limits**: Set maximum stakes per option
3. **Performance Targets**: Set performance targets and benchmarks
4. **Exit Strategies**: Plan exit strategies for different scenarios
5. **Monitoring Plan**: Plan regular monitoring and review

### Execution Phase
1. **Staged Entry**: Enter positions gradually
2. **Performance Monitoring**: Monitor performance regularly
3. **Strategic Adjustments**: Adjust based on performance
4. **Rebalancing**: Regular portfolio rebalancing
5. **Optimization**: Continuous optimization of portfolio

## 🛡️ Risk Management

### Diversification Risk
- **Subnet Diversification**: Spread stakes across multiple subnets
- **Node Diversification**: Spread stakes across multiple nodes
- **Amount Limits**: Set maximum stakes per option
- **Geographic Diversification**: Consider geographic distribution
- **Strategy Diversification**: Mix different staking strategies

### Performance Risk
- **Regular Monitoring**: Monitor performance regularly
- **Performance Benchmarks**: Set performance benchmarks
- **Exit Triggers**: Define exit triggers for underperformance
- **Recovery Plans**: Plan for performance recovery
- **Alternative Options**: Identify alternative staking options

### Market Risk
- **Market Analysis**: Regular market analysis
- **Trend Monitoring**: Monitor market trends
- **Adaptation**: Adapt strategies to market changes
- **Hedging**: Consider hedging strategies
- **Liquidity Management**: Maintain adequate liquidity

### Operational Risk
- **Key Security**: Secure key management
- **Infrastructure**: Reliable infrastructure
- **Monitoring**: Comprehensive monitoring
- **Backup Plans**: Backup and recovery plans
- **Incident Response**: Incident response procedures

## 📊 Performance Monitoring

### Key Metrics
- **Total Staked**: Total amount staked across all options
- **Reward Rates**: Current reward rates for each stake
- **Performance**: Historical performance of stakes
- **Risk Metrics**: Risk metrics for portfolio
- **Market Position**: Position relative to market

### Monitoring Commands
```bash
# Monitor portfolio performance
htcli stake info --mine

# Monitor specific subnet performance
htcli chain subnet --subnet-id 1

# Monitor specific node performance
htcli node status --subnet-id 1 --node-id 5

# Monitor network performance
htcli chain info
```

### Performance Analysis
- **Return on Investment**: Calculate ROI for each stake
- **Risk-Adjusted Returns**: Risk-adjusted return metrics
- **Performance Comparison**: Compare performance across options
- **Trend Analysis**: Analyze performance trends
- **Optimization Opportunities**: Identify optimization opportunities

## 🔄 Advanced Staking Strategies

### Yield Farming
```bash
# Stake in high-yield subnets
htcli stake delegate-add --subnet-id 1 --amount 1000000000000000000 --key-name my-staking-key

# Monitor and rotate to higher yields
htcli stake delegate-remove --subnet-id 1 --shares 500000000000000000 --key-name my-staking-key
htcli stake delegate-add --subnet-id 2 --amount 500000000000000000 --key-name my-staking-key
```

### Node Operator Strategy
```bash
# Stake in your own nodes
htcli stake node-add --subnet-id 1 --node-id 5 --amount 1000000000000000000 --key-name my-staking-key

# Increase pool for community rewards
htcli stake node-increase --subnet-id 1 --node-id 5 --amount 500000000000000000 --key-name my-staking-key
```

### Arbitrage Strategy
```bash
# Identify rate differences
htcli stake info --mine

# Move stakes to higher rates
htcli stake delegate-transfer --subnet-id 1 --to-account <higher-rate-subnet> --shares 100000000000000000 --key-name my-staking-key
```

## 🎯 Best Practices

### Security
- **Key Management**: Secure key generation and storage
- **Access Control**: Limit access to staking keys
- **Monitoring**: Monitor for unauthorized activity
- **Backup**: Regular backup of critical data
- **Incident Response**: Plan for security incidents

### Performance
- **Regular Monitoring**: Monitor performance regularly
- **Performance Optimization**: Optimize for better returns
- **Risk Management**: Manage risks effectively
- **Strategic Planning**: Plan strategically for long-term success
- **Adaptation**: Adapt to changing market conditions

### Strategy
- **Diversification**: Diversify across multiple options
- **Research**: Research before staking
- **Monitoring**: Monitor performance regularly
- **Adjustment**: Adjust strategies based on performance
- **Long-term Planning**: Plan for long-term success

## 📈 Automation and Scripts

### Automated Monitoring
```bash
#!/bin/bash
# Automated portfolio monitoring script

while true; do
  echo "=== Portfolio Status ==="
  htcli stake info --mine --format json
  
  echo "=== Network Status ==="
  htcli chain info --format json
  
  sleep 3600  # Check every hour
done
```

### Performance Tracking
```bash
#!/bin/bash
# Performance tracking script

# Track daily performance
date >> performance.log
htcli stake info --mine --format json >> performance.log
echo "---" >> performance.log
```

### Rebalancing Script
```bash
#!/bin/bash
# Automated rebalancing script

# Check performance and rebalance if needed
PERFORMANCE=$(htcli stake info --mine --format json | jq '.performance')

if [ "$PERFORMANCE" -lt 0.05 ]; then
  echo "Performance below threshold, rebalancing..."
  # Add rebalancing logic here
fi
```

---

**This comprehensive staking guide covers all aspects of staking operations, from basic staking to advanced portfolio management, with strategic planning, risk management, and performance optimization for successful staking in the Hypertensor network.** 🚀
