# 🔍 Blockchain Commands Discovery Summary

## 📊 Overview

- **Total Pallets**: 20
- **Network Pallet Calls**: 45 functions
- **Network Pallet Storage**: 102 items
- **Network Pallet Events**: 35 types

## 🏗️ Available Pallets

### 1. **System** (11 calls, 19 storage, 7 events)

- Core blockchain functionality
- Account management, block information, events

### 2. **Balances** (9 calls, 8 storage, 22 events)

- Token balance management
- Transfer functions, account operations

### 3. **Network** (45 calls, 102 storage, 35 events) ⭐

- **Hypertensor-specific functionality**
- Subnet management, staking, validation

### 4. **Treasury** (6 calls, 7 storage, 12 events)

- Treasury management, proposals, approvals

### 5. **Utility** (6 calls, 6 events)

- Batch operations, multisig

### 6. **Proxy** (10 calls, 3 storage, 5 events)

- Proxy account management

### 7. **Scheduler** (10 calls, 5 storage, 9 events)

- Scheduled operations

### 8. **Collective** (6 calls, 7 storage, 7 events)

- Collective decision making

### 9. **Rewards** (1 call, 2 storage, 2 events)

- Reward distribution

### 10. **Grandpa** (3 calls, 8 storage, 3 events)

- Finality gadget

### 11. **Aura** (3 storage)

- Block production

### 12. **Timestamp** (1 call, 3 storage)

- Time management

### 13. **Sudo** (5 calls, 2 storage, 4 events)

- Administrative functions

### 14. **Multisig** (4 calls, 2 storage, 4 events)

- Multi-signature operations

### 15. **Preimage** (5 calls, 4 storage, 3 events)

- Preimage management

### 16. **AtomicSwap** (3 calls, 2 storage, 3 events)

- Atomic swap operations

### 17. **TxPause** (2 calls, 2 storage, 2 events)

- Transaction pausing

### 18. **Authorship** (2 storage)

- Block authorship

### 19. **InsecureRandomnessCollectiveFlip** (2 storage)

- Randomness generation

### 20. **TransactionPayment** (3 storage, 1 event)

- Transaction fee management

## 🌐 Network Pallet - Available Functions

### 📞 Subnet Management (8 functions)

1. `register_subnet` - Register a new subnet
2. `activate_subnet` - Activate a subnet
3. `remove_subnet` - Remove a subnet
4. `owner_deactivate_subnet` - Owner deactivate subnet
5. `owner_update_registration_interval` - Update registration interval
6. `owner_update_activation_interval` - Update activation interval
7. `owner_remove_subnet_node` - Owner remove subnet node
8. `set_subnet_owner_percentage` - Set subnet owner percentage

### 📞 Node Management (8 functions)

9. `add_subnet_node` - Add node to subnet
10. `register_subnet_node` - Register subnet node
11. `activate_subnet_node` - Activate subnet node
12. `deactivate_subnet_node` - Deactivate subnet node
13. `remove_subnet_node` - Remove subnet node
14. `register_subnet_node_a_parameter` - Register node parameter
15. `set_subnet_node_non_unique_parameter` - Set node parameter
16. `set_max_subnet_nodes` - Set max subnet nodes

### 📞 Staking Operations (8 functions)

17. `add_to_stake` - Add stake to subnet
18. `remove_stake` - Remove stake from subnet
19. `claim_unbondings` - Claim unbonded stakes
20. `add_to_delegate_stake` - Add delegate stake
21. `transfer_delegate_stake` - Transfer delegate stake
22. `remove_delegate_stake` - Remove delegate stake
23. `increase_delegate_stake` - Increase delegate stake
24. `set_min_subnet_delegate_stake_factor` - Set min delegate stake factor

### 📞 Node Delegation (6 functions)

25. `add_to_node_delegate_stake` - Add node delegate stake
26. `transfer_node_delegate_stake` - Transfer node delegate stake
27. `remove_node_delegate_stake` - Remove node delegate stake
28. `increase_node_delegate_stake` - Increase node delegate stake
29. `transfer_from_node_to_subnet` - Transfer from node to subnet
30. `transfer_from_subnet_to_node` - Transfer from subnet to node

### 📞 Validation & Consensus (6 functions)

31. `validate` - Validate subnet
32. `attest` - Attest to subnet
33. `propose` - Propose subnet changes
34. `attest_proposal` - Attest to proposal
35. `cancel_proposal` - Cancel proposal
36. `challenge_proposal` - Challenge proposal

### 📞 Voting & Governance (2 functions)

37. `vote` - Vote on proposal
38. `finalize_proposal` - Finalize proposal

### 📞 Key Management (4 functions)

39. `update_coldkey` - Update cold key
40. `update_hotkey` - Update hot key
41. `update_peer_id` - Update peer ID
42. `update_bootstrap_peer_id` - Update bootstrap peer ID

### 📞 Network Control (3 functions)

43. `pause` - Pause network operations
44. `unpause` - Unpause network operations
45. `update_delegate_reward_rate` - Update delegate reward rate

## 💾 Key Storage Items

### Subnet Data

- `SubnetsData` - All subnet information
- `SubnetPaths` - Subnet path mappings
- `SubnetOwner` - Subnet ownership
- `TotalSubnetUids` - Total subnet count
- `TotalActiveSubnets` - Active subnet count

### Node Data

- `SubnetNodesData` - Subnet node information
- `HotkeyOwner` - Hotkey ownership
- `HotkeySubnetNodeId` - Hotkey to node mapping
- `TotalSubnetNodes` - Total nodes per subnet
- `TotalActiveSubnetNodes` - Active nodes per subnet

### Staking Data

- `AccountSubnetStake` - Account stake per subnet
- `TotalStake` - Total network stake
- `TotalSubnetStake` - Total stake per subnet
- `StakeUnbondingLedger` - Unbonding stake information

### Network Statistics

- `TotalActiveNodes` - Total active nodes
- `StakeVaultBalance` - Stake vault balance
- `MaxStakeBalance` - Maximum stake balance
- `MinStakeBalance` - Minimum stake balance

## 🚨 Important Findings

### ✅ What Works

- **Real blockchain connection** to `wss://hypertensor.duckdns.org`
- **Standard Substrate RPC calls** (`system_peers`, `chain_getHeader`, etc.)
- **Storage queries** (`System.Account`, `Balances.TotalIssuance`, etc.)
- **Network pallet calls** (45 functions available)
- **Network pallet storage** (102 storage items available)

### ❌ What Doesn't Work

- **Custom RPC methods** from `hypertensor_rpc_models.md`:
  - `network_registerSubnet` ❌
  - `network_activateSubnet` ❌
  - `network_getSubnetData` ❌
  - `network_addToStake` ❌
  - `network_getNetworkStats` ❌
  - All other custom RPCs ❌

## 🎯 Recommendation

**Use Network Pallet Calls Instead of Custom RPCs**

Instead of the custom RPC methods that don't exist, use the actual Network pallet calls:

```python
# Instead of: network_registerSubnet RPC
# Use: Network.register_subnet call

# Instead of: network_addToStake RPC
# Use: Network.add_to_stake call

# Instead of: network_getNetworkStats RPC
# Use: Network storage queries for statistics
```

The Network pallet provides all the functionality needed for Hypertensor operations, just through the standard Substrate call mechanism rather than custom RPC endpoints.
