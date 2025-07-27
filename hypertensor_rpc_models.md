# Hypertensor RPC Endpoint Models

## Complete RPC API Reference

This document provides detailed information about all RPC endpoints, their request/response models, error codes, and data structures for the Hypertensor blockchain.

## RPC Endpoint Categories

### 1. Subnet Operations

#### 1.1 Subnet Registration

**Endpoint**: `network_registerSubnet`
**Method**: POST
**Description**: Register a new subnet on the blockchain

**Request Model**:

```json
{
  "subnet_data": {
    "path": "string",                    // Subnet path/name
    "memory_mb": "number",               // Memory requirement in MB
    "registration_blocks": "number",     // Registration period in blocks
    "entry_interval": "number"           // Entry interval in blocks
  }
}
```

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "transaction_hash": "string",          // Transaction hash
  "block_number": "number",              // Block number
  "data": {
    "subnet_id": "number",               // Generated subnet ID
    "registration_cost": "string",       // Registration cost in smallest unit
    "status": "string"                   // Registration status
  }
}
```

**Error Codes**:

- `1001`: Invalid subnet path
- `1002`: Insufficient memory allocation
- `1003`: Invalid registration period
- `1004`: Duplicate subnet path
- `1005`: Insufficient balance for registration

#### 1.2 Subnet Activation

**Endpoint**: `network_activateSubnet`
**Method**: POST
**Description**: Activate a registered subnet

**Request Model**:

```json
{
  "subnet_id": "number"                 // Subnet ID to activate
}
```

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "transaction_hash": "string",
  "block_number": "number",
  "data": {
    "subnet_id": "number",
    "activation_block": "number",
    "status": "string"                   // "activated"
  }
}
```

**Error Codes**:

- `2001`: Subnet not found
- `2002`: Subnet already activated
- `2003`: Insufficient nodes for activation
- `2004`: Registration period not completed

#### 1.3 Subnet Information

**Endpoint**: `network_getSubnetData`
**Method**: GET
**Description**: Get detailed subnet information

**Request Model**:

```json
{
  "subnet_id": "number"                 // Subnet ID
}
```

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "data": {
    "subnet_id": "number",
    "path": "string",
    "memory_mb": "number",
    "registration_blocks": "number",
    "entry_interval": "number",
    "activated": "number",               // Activation block number
    "registration_cost": "string",
    "node_count": "number",
    "total_stake": "string",
    "status": "string"                   // "registering", "activated", "inactive"
  }
}
```

**Error Codes**:

- `3001`: Subnet not found

#### 1.4 Subnet List

**Endpoint**: `network_getSubnetsData`
**Method**: GET
**Description**: Get list of all subnets

**Request Model**:

```json
{
  "active_only": "boolean"              // Optional: filter active subnets only
}
```

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "data": {
    "subnets": [
      {
        "subnet_id": "number",
        "path": "string",
        "memory_mb": "number",
        "activated": "number",
        "node_count": "number",
        "total_stake": "string",
        "status": "string"
      }
    ],
    "total_count": "number",
    "active_count": "number"
  }
}
```

### 2. Subnet Node Operations

#### 2.1 Add Subnet Node

**Endpoint**: `network_addSubnetNode`
**Method**: POST
**Description**: Add a node to a subnet

**Request Model**:

```json
{
  "subnet_id": "number",                // Subnet ID
  "peer_id": "string",                  // Peer ID
  "hotkey": "string"                    // Hotkey account
}
```

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "transaction_hash": "string",
  "block_number": "number",
  "data": {
    "subnet_id": "number",
    "node_id": "number",                 // Generated node ID
    "peer_id": "string",
    "hotkey": "string",
    "status": "string"                   // "active"
  }
}
```

**Error Codes**:

- `4001`: Subnet not found
- `4002`: Subnet not activated
- `4003`: Node already exists
- `4004`: Invalid peer ID format
- `4005`: Insufficient stake for node

#### 2.2 Get Subnet Nodes

**Endpoint**: `network_getSubnetNodes`
**Method**: GET
**Description**: Get all nodes in a subnet

**Request Model**:

```json
{
  "subnet_id": "number"                 // Subnet ID
}
```

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "data": {
    "subnet_id": "number",
    "nodes": [
      {
        "node_id": "number",
        "peer_id": "string",
        "hotkey": "string",
        "stake": "string",
        "status": "string",
        "registration_block": "number"
      }
    ],
    "total_nodes": "number",
    "total_stake": "string"
  }
}
```

### 3. Staking Operations

#### 3.1 Add Stake

**Endpoint**: `network_addToStake`
**Method**: POST
**Description**: Add stake to a subnet node

**Request Model**:

```json
{
  "subnet_id": "number",                // Subnet ID
  "subnet_node_id": "number",           // Subnet node ID
  "hotkey": "string",                   // Hotkey account
  "stake_to_be_added": "string"         // Stake amount in smallest unit
}
```

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "transaction_hash": "string",
  "block_number": "number",
  "data": {
    "subnet_id": "number",
    "node_id": "number",
    "hotkey": "string",
    "stake_added": "string",
    "total_stake": "string",
    "timestamp": "number"
  }
}
```

**Error Codes**:

- `5001`: Subnet not found
- `5002`: Node not found
- `5003`: Insufficient balance
- `5004`: Invalid stake amount
- `5005`: Stake limit exceeded

#### 3.2 Remove Stake

**Endpoint**: `network_removeStake`
**Method**: POST
**Description**: Remove stake from a subnet

**Request Model**:

```json
{
  "subnet_id": "number",                // Subnet ID
  "hotkey": "string",                   // Hotkey account
  "stake_to_be_removed": "string"       // Stake amount to remove
}
```

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "transaction_hash": "string",
  "block_number": "number",
  "data": {
    "subnet_id": "number",
    "hotkey": "string",
    "stake_removed": "string",
    "remaining_stake": "string",
    "unbonding_period": "number",
    "timestamp": "number"
  }
}
```

**Error Codes**:

- `6001`: Subnet not found
- `6002`: Insufficient stake to remove
- `6003`: Stake still in unbonding period
- `6004`: Invalid stake amount

#### 3.3 Get Stake Information

**Endpoint**: `network_getAccountSubnetStake`
**Method**: GET
**Description**: Get stake information for an account

**Request Model**:

```json
{
  "account": "string",                  // Account address
  "subnet_id": "number"                 // Subnet ID
}
```

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "data": {
    "account": "string",
    "subnet_id": "number",
    "stake": "string",                  // Current stake amount
    "unbonding": "string",              // Unbonding stake amount
    "total_stake": "string",            // Total stake (stake + unbonding)
    "stake_history": [
      {
        "block_number": "number",
        "amount": "string",
        "type": "string"                 // "add", "remove"
      }
    ]
  }
}
```

### 4. Validation Operations

#### 4.1 Submit Validation

**Endpoint**: `network_validate`
**Method**: POST
**Description**: Submit validation data to a subnet

**Request Model**:

```json
{
  "subnet_id": "number",                // Subnet ID
  "data": "string",                     // Validation data
  "args": "string"                      // Optional arguments
}
```

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "transaction_hash": "string",
  "block_number": "number",
  "data": {
    "subnet_id": "number",
    "validation_id": "string",
    "timestamp": "number",
    "status": "string"                  // "submitted", "processing"
  }
}
```

**Error Codes**:

- `7001`: Subnet not found
- `7002`: Subnet not active
- `7003`: Invalid validation data
- `7004`: Validation rate limit exceeded

#### 4.2 Submit Attestation

**Endpoint**: `network_attest`
**Method**: POST
**Description**: Submit attestation for a subnet

**Request Model**:

```json
{
  "subnet_id": "number"                 // Subnet ID
}
```

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "transaction_hash": "string",
  "block_number": "number",
  "data": {
    "subnet_id": "number",
    "attestation_id": "string",
    "timestamp": "number",
    "status": "string"                  // "attested"
  }
}
```

#### 4.3 Get Consensus Data

**Endpoint**: `network_getConsensusData`
**Method**: GET
**Description**: Get consensus data for a subnet

**Request Model**:

```json
{
  "subnet_id": "number",                // Subnet ID
  "epoch": "number"                     // Epoch number
}
```

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "data": {
    "subnet_id": "number",
    "epoch": "number",
    "consensus_data": {
      "total_validations": "number",
      "total_attestations": "number",
      "consensus_reached": "boolean",
      "consensus_threshold": "number",
      "participating_nodes": "number"
    },
    "validations": [
      {
        "node_id": "number",
        "validation_data": "string",
        "timestamp": "number"
      }
    ],
    "attestations": [
      {
        "node_id": "number",
        "attestation_data": "string",
        "timestamp": "number"
      }
    ]
  }
}
```

### 5. Governance Operations

#### 5.1 Create Proposal

**Endpoint**: `network_propose`
**Method**: POST
**Description**: Create a governance proposal

**Request Model**:

```json
{
  "subnet_id": "number",                // Subnet ID
  "subnet_node_id": "number",           // Subnet node ID
  "peer_id": "string",                  // Peer ID
  "data": "string"                      // Proposal data
}
```

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "transaction_hash": "string",
  "block_number": "number",
  "data": {
    "proposal_id": "number",
    "subnet_id": "number",
    "creator": "string",
    "data": "string",
    "status": "string",                 // "active", "passed", "rejected"
    "created_at": "number"
  }
}
```

**Error Codes**:

- `8001`: Subnet not found
- `8002`: Node not found
- `8003`: Invalid proposal data
- `8004`: Insufficient stake for proposal

#### 5.2 Vote on Proposal

**Endpoint**: `network_vote`
**Method**: POST
**Description**: Vote on a governance proposal

**Request Model**:

```json
{
  "subnet_id": "number",                // Subnet ID
  "subnet_node_id": "number",           // Subnet node ID
  "proposal_id": "number",              // Proposal ID
  "vote": "string"                      // Vote type: "yay" or "nay"
}
```

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "transaction_hash": "string",
  "block_number": "number",
  "data": {
    "proposal_id": "number",
    "voter": "string",
    "vote": "string",
    "timestamp": "number"
  }
}
```

**Error Codes**:

- `9001`: Proposal not found
- `9002`: Invalid vote type
- `9003`: Already voted
- `9004`: Voting period ended

#### 5.3 Get Proposals

**Endpoint**: `network_getProposals`
**Method**: GET
**Description**: Get all proposals for a subnet

**Request Model**:

```json
{
  "subnet_id": "number",                // Subnet ID
  "status": "string"                    // Optional: filter by status
}
```

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "data": {
    "subnet_id": "number",
    "proposals": [
      {
        "proposal_id": "number",
        "creator": "string",
        "data": "string",
        "status": "string",
        "yay_votes": "number",
        "nay_votes": "number",
        "total_votes": "number",
        "created_at": "number",
        "end_at": "number"
      }
    ],
    "total_proposals": "number"
  }
}
```

### 6. Chain Information

#### 6.1 Network Statistics

**Endpoint**: `network_getNetworkStats`
**Method**: GET
**Description**: Get overall network statistics

**Request Model**: `{}`

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "data": {
    "total_subnets": "number",
    "active_subnets": "number",
    "total_nodes": "number",
    "total_stake": "string",
    "current_epoch": "number",
    "total_validations": "number",
    "total_attestations": "number",
    "network_uptime": "number",
    "average_block_time": "number"
  }
}
```

#### 6.2 Account Information

**Endpoint**: `system_getAccountInfo`
**Method**: GET
**Description**: Get account information and balance

**Request Model**:

```json
{
  "account": "string"                   // Account address
}
```

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "data": {
    "account": "string",
    "balance": "string",                // Balance in smallest unit
    "nonce": "number",                  // Transaction nonce
    "reserved": "string",               // Reserved balance
    "misc_frozen": "string",            // Frozen balance
    "fee_frozen": "string"              // Fee frozen balance
  }
}
```

#### 6.3 Current Epoch

**Endpoint**: `network_getCurrentEpoch`
**Method**: GET
**Description**: Get current epoch information

**Request Model**: `{}`

**Response Model**:

```json
{
  "success": "boolean",
  "message": "string",
  "data": {
    "epoch": "number",
    "start_block": "number",
    "end_block": "number",
    "blocks_remaining": "number",
    "epoch_duration": "number",
    "timestamp": "number"
  }
}
```

### 7. Error Response Models

#### 7.1 Standard Error Response

```json
{
  "success": false,
  "error": "string",                    // Error type
  "message": "string",                  // Human-readable message
  "code": "number",                     // Error code
  "details": {                          // Optional error details
    "field": "string",
    "value": "any",
    "constraint": "string"
  },
  "timestamp": "string"                 // ISO timestamp
}
```

#### 7.2 Common Error Types

| Error Type | Code Range | Description |
|------------|------------|-------------|
| `AuthenticationFailed` | 1001-1999 | Authentication and authorization errors |
| `ValidationError` | 2001-2999 | Input validation errors |
| `NetworkError` | 3001-3999 | Network and connection errors |
| `RPCError` | 4001-4999 | RPC-specific errors |
| `BusinessLogicError` | 5001-5999 | Business logic and state errors |
| `SubnetError` | 6001-6999 | Subnet-specific errors |
| `StakingError` | 7001-7999 | Staking-related errors |
| `ValidationError` | 8001-8999 | Validation and attestation errors |
| `GovernanceError` | 9001-9999 | Governance and proposal errors |

### 8. Data Types

#### 8.1 Account Address

- **Format**: SS58 encoded string
- **Length**: 42-48 characters
- **Example**: `5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY`

#### 8.2 Balance Amount

- **Format**: String representing amount in smallest unit
- **Precision**: 9 decimal places
- **Example**: `1000000000` (1 TAO)

#### 8.3 Block Number

- **Format**: Unsigned 32-bit integer
- **Range**: 0 to 4,294,967,295

#### 8.4 Subnet ID

- **Format**: Unsigned 32-bit integer
- **Range**: 1 to 4,294,967,295

#### 8.5 Node ID

- **Format**: Unsigned 32-bit integer
- **Range**: 1 to 4,294,967,295

#### 8.6 Peer ID

- **Format**: MultiHash encoded string
- **Example**: `QmYyQSo1c1Ym7orWxLYvCrM2EmxFTANf8wXvvEKPtgL8Vu`

#### 8.7 Transaction Hash

- **Format**: Hex string (32 bytes)
- **Example**: `0x1234567890abcdef...`

### 9. Rate Limits

| Endpoint Category | Rate Limit | Window |
|------------------|------------|---------|
| Read Operations | 100 requests/minute | 1 minute |
| Write Operations | 10 requests/minute | 1 minute |
| Staking Operations | 5 requests/minute | 1 minute |
| Validation Operations | 20 requests/minute | 1 minute |
| Governance Operations | 2 requests/minute | 1 minute |

### 10. WebSocket Events

#### 10.1 Subnet Events

```json
{
  "event": "subnet_registered",
  "data": {
    "subnet_id": "number",
    "path": "string",
    "account": "string",
    "block_number": "number"
  }
}
```

#### 10.2 Staking Events

```json
{
  "event": "stake_added",
  "data": {
    "subnet_id": "number",
    "node_id": "number",
    "hotkey": "string",
    "amount": "string",
    "block_number": "number"
  }
}
```

#### 10.3 Validation Events

```json
{
  "event": "validation_submitted",
  "data": {
    "subnet_id": "number",
    "node_id": "number",
    "validation_id": "string",
    "block_number": "number"
  }
}
```

This comprehensive RPC model documentation provides all the information needed to properly handle requests and responses in the Hypertensor CLI implementation. Each endpoint includes detailed request/response models, error codes, and data type specifications.
