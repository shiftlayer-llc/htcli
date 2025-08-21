"""
Pytest configuration and fixtures for htcli tests.
"""

import os
from pathlib import Path
from unittest.mock import Mock

import pytest
from typer.testing import CliRunner

from src.htcli.config import Config, NetworkConfig


@pytest.fixture
def cli_runner():
    """Create a CLI runner for testing commands."""
    return CliRunner()


@pytest.fixture
def mock_config():
    """Create a mock configuration for testing."""
    config = Config(
        network=NetworkConfig(
            endpoint="wss://hypertensor.duckdns.org",
            ws_endpoint="wss://hypertensor.duckdns.org",
            timeout=30,
            retry_attempts=3,
        )
    )
    return config


@pytest.fixture
def mock_client(mock_config):
    """Create a mock HypertensorClient for testing."""
    client = Mock()
    client.config = mock_config

    # Mock all the methods that tests expect
    client.connect.return_value = True
    client.disconnect.return_value = None
    client.connect_websocket.return_value = True

    # Subnet operations
    client.register_subnet.return_value = {"success": True, "message": "Success"}
    client.activate_subnet.return_value = {"success": True, "message": "Success"}
    client.pause_subnet.return_value = {"success": True, "message": "Success"}
    client.unpause_subnet.return_value = {"success": True, "message": "Success"}
    client.list_subnets.return_value = {"success": True, "data": []}
    client.get_subnet_info.return_value = {"success": True, "data": {}}

    # Subnet owner operations
    client.owner_update_name.return_value = {"success": True, "message": "Success"}
    client.owner_update_repo.return_value = {"success": True, "message": "Success"}
    client.owner_update_description.return_value = {
        "success": True,
        "message": "Success",
    }
    client.transfer_subnet_ownership.return_value = {
        "success": True,
        "message": "Success",
    }
    client.accept_subnet_ownership.return_value = {
        "success": True,
        "message": "Success",
    }
    client.undo_subnet_ownership_transfer.return_value = {
        "success": True,
        "message": "Success",
    }
    client.owner_remove_subnet_node.return_value = {
        "success": True,
        "message": "Success",
    }
    client.owner_update_churn_limit.return_value = {
        "success": True,
        "message": "Success",
    }
    client.owner_update_min_stake.return_value = {"success": True, "message": "Success"}
    client.owner_update_max_stake.return_value = {"success": True, "message": "Success"}
    client.owner_update_registration_epochs.return_value = {
        "success": True,
        "message": "Success",
    }
    client.owner_update_activation_grace_epochs.return_value = {
        "success": True,
        "message": "Success",
    }
    client.owner_update_idle_epochs.return_value = {
        "success": True,
        "message": "Success",
    }
    client.owner_update_included_epochs.return_value = {
        "success": True,
        "message": "Success",
    }
    client.owner_update_max_penalties.return_value = {
        "success": True,
        "message": "Success",
    }
    client.owner_add_initial_coldkeys.return_value = {
        "success": True,
        "message": "Success",
    }
    client.owner_remove_initial_coldkeys.return_value = {
        "success": True,
        "message": "Success",
    }

    # Node operations
    client.register_subnet_node.return_value = {"success": True, "message": "Success"}
    client.activate_subnet_node.return_value = {"success": True, "message": "Success"}
    client.deactivate_subnet_node.return_value = {"success": True, "message": "Success"}
    client.reactivate_subnet_node.return_value = {"success": True, "message": "Success"}
    client.remove_subnet_node.return_value = {"success": True, "message": "Success"}
    client.cleanup_expired_node.return_value = {"success": True, "message": "Success"}
    client.update_node_delegate_reward_rate.return_value = {
        "success": True,
        "message": "Success",
    }
    client.update_node_coldkey.return_value = {"success": True, "message": "Success"}
    client.update_node_hotkey.return_value = {"success": True, "message": "Success"}
    client.add_node.return_value = {"success": True, "message": "Success"}
    client.list_nodes.return_value = {"success": True, "data": []}

    # Staking operations
    client.add_to_stake.return_value = {"success": True, "message": "Success"}
    client.remove_stake.return_value = {"success": True, "message": "Success"}
    client.claim_unbondings.return_value = {"success": True, "message": "Success"}
    client.add_to_delegate_stake.return_value = {"success": True, "message": "Success"}
    client.remove_delegate_stake.return_value = {"success": True, "message": "Success"}
    client.transfer_delegate_stake.return_value = {
        "success": True,
        "message": "Success",
    }
    client.increase_delegate_stake.return_value = {
        "success": True,
        "message": "Success",
    }
    client.add_to_node_delegate_stake.return_value = {
        "success": True,
        "message": "Success",
    }
    client.remove_node_delegate_stake.return_value = {
        "success": True,
        "message": "Success",
    }
    client.transfer_node_delegate_stake.return_value = {
        "success": True,
        "message": "Success",
    }
    client.increase_node_delegate_stake.return_value = {
        "success": True,
        "message": "Success",
    }
    client.get_stake_info.return_value = {"success": True, "data": {}}
    client.get_node_staking_info.return_value = {"success": True, "data": {}}
    client.get_subnet_staking_info.return_value = {"success": True, "data": {}}
    client.get_general_staking_info.return_value = {"success": True, "data": {}}

    # Chain operations
    client.get_network_stats.return_value = {"success": True, "data": {}}
    client.get_account_info.return_value = {"success": True, "data": {}}
    client.get_epoch_info.return_value = {"success": True, "data": {}}
    client.get_balance.return_value = {"success": True, "data": {}}
    client.get_peers.return_value = {"success": True, "data": []}
    client.get_block_info.return_value = {"success": True, "data": {}}

    # Subnet activation requirements
    client.check_subnet_activation_requirements.return_value = {
        "success": True,
        "data": {},
    }

    return client


@pytest.fixture
def test_wallet_dir(tmp_path):
    """Create a temporary wallet directory for testing."""
    wallet_dir = tmp_path / "wallets"
    wallet_dir.mkdir()
    return wallet_dir


@pytest.fixture
def sample_keypair():
    """Sample keypair data for testing."""
    return {
        "name": "test-key",
        "public_key": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
        "private_key": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "key_type": "sr25519",
    }


@pytest.fixture
def sample_subnet_data():
    """Sample subnet data for testing."""
    return {
        "subnet_id": 1,
        "path": "test-subnet",
        "memory_mb": 1024,
        "registration_blocks": 1000,
        "entry_interval": 100,
        "active": True,
        "nodes": [
            {
                "node_id": 1,
                "peer_id": "QmTestPeerId1234567890abcdef",
                "hotkey": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                "stake": 1000,
            }
        ],
    }


@pytest.fixture
def sample_subnet_register_request():
    """Sample subnet registration request for testing."""
    return {
        "name": "Test Subnet",
        "repo": "https://github.com/test/subnet",
        "description": "A test subnet for testing purposes",
        "misc": {"version": "1.0.0"},
        "min_stake": 1000000000000000000,  # 1 TENSOR
        "max_stake": 10000000000000000000,  # 10 TENSOR
        "delegate_stake_percentage": 10,
        "churn_limit": 5,
        "registration_queue_epochs": 10,
        "activation_grace_epochs": 5,
        "queue_classification_epochs": 3,
        "included_classification_epochs": 2,
        "max_registered_nodes": 100,
        "initial_coldkeys": ["5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"],
        "key_types": ["sr25519"],
        "node_removal_system": "manual",
    }


@pytest.fixture
def sample_node_data():
    """Sample node data for testing."""
    return {
        "subnet_id": 1,
        "node_id": 1,
        "peer_id": "QmTestPeerId1234567890abcdef",
        "hotkey": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
        "coldkey": "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty",
        "delegate_reward_rate": 1000,
        "stake": 1000000000000000000,  # 1 TENSOR
        "classification": "Registered",
        "activation_epoch": 100,
        "registration_epoch": 95,
    }


@pytest.fixture
def sample_staking_data():
    """Sample staking data for testing."""
    return {
        "node_id": 1,
        "subnet_id": 1,
        "total_stake": 1000000000000000000,  # 1 TENSOR
        "delegate_stake": 500000000000000000,  # 0.5 TENSOR
        "own_stake": 500000000000000000,  # 0.5 TENSOR
        "delegator_count": 5,
        "reward_rate": 1000,
        "unbonding_stake": 100000000000000000,  # 0.1 TENSOR
        "claimable_rewards": 50000000000000000,  # 0.05 TENSOR
    }


@pytest.fixture
def sample_account_data():
    """Sample account data for testing."""
    return {
        "address": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
        "balance": 1000000000000000000,  # 1 TENSOR with 18 decimals
        "nonce": 0,
        "free": 1000000000000,
        "reserved": 0,
        "misc_frozen": 0,
        "fee_frozen": 0,
    }


@pytest.fixture
def sample_network_stats():
    """Sample network statistics for testing."""
    return {
        "total_subnets": 10,
        "active_subnets": 8,
        "total_nodes": 150,
        "total_stake": 5000000000000000000,  # 5 TENSOR with 18 decimals
        "current_epoch": 1234,
        "block_height": 567890,
    }


@pytest.fixture
def sample_password_data():
    """Sample password data for testing."""
    return {
        "key_name": "test-key",
        "password": "test_password_123",
        "encrypted_password": "gAAAAABk...",  # Mock encrypted password
        "cached_password": "test_password_123",
    }


@pytest.fixture
def sample_flow_data():
    """Sample flow data for testing."""
    return {
        "flow_name": "Subnet Deployment",
        "flow_description": "Complete subnet deployment workflow",
        "steps": [
            {"name": "Validate Requirements", "status": "pending"},
            {"name": "Register Subnet", "status": "pending"},
            {"name": "Activate Subnet", "status": "pending"},
            {"name": "Add Initial Nodes", "status": "pending"},
        ],
        "context": {
            "subnet_name": "Test Subnet",
            "subnet_id": None,
            "nodes": [],
        },
    }


@pytest.fixture
def sample_activation_requirements():
    """Sample subnet activation requirements for testing."""
    return {
        "minimum_nodes": 3,
        "current_nodes": 2,
        "minimum_delegate_stake": 1000000000000000000,  # 1 TENSOR
        "current_delegate_stake": 800000000000000000,  # 0.8 TENSOR
        "stake_factor_requirements": {
            "min_stake_factor": 1.0,
            "current_stake_factor": 0.8,
        },
        "initial_coldkeys": ["5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"],
        "network_consensus": True,
        "all_requirements_met": False,
        "missing_requirements": [
            "Insufficient nodes (2/3 required)",
            "Insufficient delegate stake (0.8/1.0 TENSOR required)",
        ],
    }


@pytest.fixture
def env_vars():
    """Set up environment variables for testing."""
    # Store original environment variables
    original_env = os.environ.copy()

    # Set test environment variables
    test_env = {
        "HTCLI_NETWORK_ENDPOINT": "wss://hypertensor.duckdns.org",
        "HTCLI_NETWORK_WS_ENDPOINT": "wss://hypertensor.duckdns.org",
        "HTCLI_NETWORK_TIMEOUT": "30",
        "HTCLI_NETWORK_RETRY_ATTEMPTS": "3",
        "HTCLI_OUTPUT_FORMAT": "table",
        "HTCLI_OUTPUT_VERBOSE": "false",
        "HTCLI_OUTPUT_COLOR": "true",
        "HTCLI_WALLET_PATH": str(Path.home() / ".htcli" / "wallets"),
        "HTCLI_WALLET_DEFAULT_NAME": "default",
        "HTCLI_WALLET_ENCRYPTION_ENABLED": "true",
        "HTCLI_PASSWORD_TEST_KEY": "test_password_123",
        "HTCLI_MASTER_KEY": "test-master-key-2024",
    }

    # Update environment
    for key, value in test_env.items():
        os.environ[key] = value

    yield test_env

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "slow: marks tests as slow running")
    config.addinivalue_line("markers", "network: marks tests as network tests")
    config.addinivalue_line(
        "markers", "password: marks tests as password management tests"
    )
    config.addinivalue_line(
        "markers", "staking: marks tests as staking operation tests"
    )
    config.addinivalue_line("markers", "subnet: marks tests as subnet operation tests")
    config.addinivalue_line("markers", "node: marks tests as node operation tests")
    config.addinivalue_line("markers", "flow: marks tests as flow operation tests")


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their location."""
    for item in items:
        # Mark unit tests
        if "unit" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        # Mark integration tests
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        # Mark network tests
        if "network" in item.nodeid:
            item.add_marker(pytest.mark.network)
        # Mark password tests
        if "password" in item.nodeid:
            item.add_marker(pytest.mark.password)
        # Mark staking tests
        if "staking" in item.nodeid:
            item.add_marker(pytest.mark.staking)
        # Mark subnet tests
        if "subnet" in item.nodeid:
            item.add_marker(pytest.mark.subnet)
        # Mark node tests
        if "node" in item.nodeid:
            item.add_marker(pytest.mark.node)
        # Mark flow tests
        if "flow" in item.nodeid:
            item.add_marker(pytest.mark.flow)
