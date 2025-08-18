"""
Sample test data for HTCLI tests.
Provides realistic test data for various scenarios.
"""

# Sample blockchain addresses
SAMPLE_ADDRESSES = {
    "alice": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
    "bob": "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty",
    "charlie": "5FLSigC9HGRKVhB9FiEo4Y3koPsNmBmLJbpXg2mp1hXcS59Y",
}

# Sample subnet data
SAMPLE_SUBNET_DATA = {
    "subnet_1": {
        "subnet_id": 1,
        "path": "/test/subnet1",
        "memory_mb": 1024,
        "registration_blocks": 1000,
        "entry_interval": 100,
        "max_node_registration_epochs": 50,
        "node_registration_interval": 20,
        "node_activation_interval": 30,
        "node_queue_period": 40,
        "max_node_penalties": 5,
        "coldkey_whitelist": [],
        "active": True,
    },
    "subnet_2": {
        "subnet_id": 2,
        "path": "/test/subnet2",
        "memory_mb": 2048,
        "registration_blocks": 2000,
        "entry_interval": 200,
        "max_node_registration_epochs": 100,
        "node_registration_interval": 40,
        "node_activation_interval": 60,
        "node_queue_period": 80,
        "max_node_penalties": 10,
        "coldkey_whitelist": [],
        "active": False,
    },
}

# Sample node data
SAMPLE_NODE_DATA = {
    "node_1": {
        "subnet_id": 1,
        "node_id": 1,
        "peer_id": "QmTestPeerId1234567890abcdef",
        "hotkey": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
        "bootstrap_peer_id": "QmTestPeerId1234567890abcdef",
        "delegate_reward_rate": 1000,
        "stake_to_be_added": 1000000000000000000,  # 1 TENSOR with 18 decimals
        "a": "1000000000000",
        "b": "1000",
        "c": "1",
    },
    "node_2": {
        "subnet_id": 1,
        "node_id": 2,
        "peer_id": "QmTestPeerId9876543210fedcba",
        "hotkey": "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty",
        "bootstrap_peer_id": "QmTestPeerId9876543210fedcba",
        "delegate_reward_rate": 2000,
        "stake_to_be_added": 2000000000000000000,  # 2 TENSOR with 18 decimals
        "a": "2000000000000",
        "b": "2000",
        "c": "1",
    },
}

# Sample stake data
SAMPLE_STAKE_DATA = {
    "stake_1": {
        "subnet_id": 1,
        "node_id": 1,
        "hotkey": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
        "stake_to_be_added": 1000000000000000000,  # 1 TENSOR with 18 decimals
        "stake_to_be_removed": 500000000000000000,  # 0.5 TENSOR with 18 decimals
    },
    "stake_2": {
        "subnet_id": 2,
        "node_id": 1,
        "hotkey": "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty",
        "stake_to_be_added": 2000000000000000000,  # 2 TENSOR with 18 decimals
        "stake_to_be_removed": 1000000000000000000,  # 1 TENSOR with 18 decimals
    },
}

# Sample network statistics
SAMPLE_NETWORK_STATS = {
    "total_subnets": 10,
    "total_active_subnets": 8,
    "total_active_nodes": 150,
    "total_stake": 5000000000000000000,  # 5 TENSOR with 18 decimals
    "current_epoch": 1234,
    "block_height": 567890,
}

# Sample account data
SAMPLE_ACCOUNT_DATA = {
    "alice_account": {
        "address": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
        "balance": 31662054793350007812500,  # Balance with 18 decimals
        "nonce": 0,
        "free": 31662054793350007812500,
        "reserved": 0,
        "misc_frozen": 0,
        "fee_frozen": 0,
        "formatted_balance": "31.6621 TENSOR",
    },
    "bob_account": {
        "address": "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty",
        "balance": 1000000000000000000,  # 1 TENSOR with 18 decimals
        "nonce": 5,
        "free": 1000000000000,
        "reserved": 0,
        "misc_frozen": 0,
        "fee_frozen": 0,
        "formatted_balance": "1.0000 TENSOR",
    },
}

# Sample block data
SAMPLE_BLOCK_DATA = {
    "block_number": 12345,
    "block_hash": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
    "parent_hash": "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
    "state_root": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
    "extrinsics_root": "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
    "extrinsics_count": 5,
    "timestamp": 1640995200000,
}

# Sample peers data
SAMPLE_PEERS_DATA = [
    {"peer_id": "QmPeer1", "address": "127.0.0.1:30333", "protocol": "substrate"},
    {"peer_id": "QmPeer2", "address": "127.0.0.2:30333", "protocol": "substrate"},
    {"peer_id": "QmPeer3", "address": "127.0.0.3:30333", "protocol": "substrate"},
]

# Sample runtime version data
SAMPLE_RUNTIME_VERSION = {
    "spec_name": "hypertensor",
    "impl_name": "hypertensor-node",
    "authoring_version": 1,
    "spec_version": 1,
    "impl_version": 1,
    "apis": [],
    "transaction_version": 1,
    "state_version": 1,
}

# Sample keypair data
SAMPLE_KEYPAIR_DATA = {
    "sr25519": {
        "name": "test-key-sr25519",
        "key_type": "sr25519",
        "public_key": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "private_key": "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
        "ss58_address": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
        "mnemonic": "test test test test test test test test test test test junk",
    },
    "ed25519": {
        "name": "test-key-ed25519",
        "key_type": "ed25519",
        "public_key": "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
        "private_key": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "ss58_address": "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty",
        "mnemonic": "test test test test test test test test test test test junk",
    },
}

# Sample error responses
SAMPLE_ERROR_RESPONSES = {
    "connection_error": {
        "success": False,
        "message": "Failed to connect to blockchain",
        "error": "Connection timeout",
    },
    "invalid_address": {
        "success": False,
        "message": "Invalid address format",
        "error": "Invalid character l",
    },
    "subnet_not_found": {
        "success": False,
        "message": "Subnet not found",
        "error": "Subnet with ID 999999 does not exist",
    },
    "insufficient_balance": {
        "success": False,
        "message": "Insufficient balance",
        "error": "Account balance too low for transaction",
    },
}

# Sample success responses
SAMPLE_SUCCESS_RESPONSES = {
    "subnet_registered": {
        "success": True,
        "message": "Subnet registered successfully",
        "transaction_hash": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "data": {"subnet_id": 1, "call_data": "0x1234567890abcdef"},
    },
    "stake_added": {
        "success": True,
        "message": "Stake added successfully",
        "transaction_hash": "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
        "data": {"call_data": "0xabcdef1234567890"},
    },
    "node_added": {
        "success": True,
        "message": "Node added successfully",
        "transaction_hash": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "data": {"call_data": "0x1234567890abcdef"},
    },
}
