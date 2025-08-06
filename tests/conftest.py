"""
Pytest configuration and fixtures for htcli tests.
"""

import os
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from typer.testing import CliRunner

from src.htcli.config import Config, NetworkConfig
from src.htcli.client import HypertensorClient


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
            retry_attempts=3
        )
    )
    return config


@pytest.fixture
def mock_client(mock_config):
    """Create a mock HypertensorClient for testing."""
    from unittest.mock import Mock
    client = Mock()
    client.config = mock_config

    # Mock all the methods that tests expect
    client.connect.return_value = True
    client.disconnect.return_value = None
    client.connect_websocket.return_value = True
    client.register_subnet.return_value = {"success": True, "message": "Success"}
    client.activate_subnet.return_value = {"success": True, "message": "Success"}
    client.list_subnets.return_value = {"success": True, "data": []}
    client.get_subnet_info.return_value = {"success": True, "data": {}}
    client.add_node.return_value = {"success": True, "message": "Success"}
    client.list_nodes.return_value = {"success": True, "data": []}
    client.add_stake.return_value = {"success": True, "message": "Success"}
    client.remove_stake.return_value = {"success": True, "message": "Success"}
    client.get_stake_info.return_value = {"success": True, "data": {}}
    client.get_network_stats.return_value = {"success": True, "data": {}}
    client.get_account_info.return_value = {"success": True, "data": {}}
    client.get_epoch_info.return_value = {"success": True, "data": {}}
    client.get_balance.return_value = {"success": True, "data": {}}
    client.get_peers.return_value = {"success": True, "data": []}
    client.get_block_info.return_value = {"success": True, "data": {}}

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
        "key_type": "sr25519"
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
                "stake": 1000
            }
        ]
    }


@pytest.fixture
def sample_account_data():
    """Sample account data for testing."""
    return {
        "address": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
        "balance": 1000000000000,  # 1 TENSOR in smallest unit
        "nonce": 0,
        "free": 1000000000000,
        "reserved": 0,
        "misc_frozen": 0,
        "fee_frozen": 0
    }


@pytest.fixture
def sample_network_stats():
    """Sample network statistics for testing."""
    return {
        "total_subnets": 10,
        "active_subnets": 8,
        "total_nodes": 150,
        "total_stake": 5000000000000,
        "current_epoch": 1234,
        "block_height": 567890
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
        "HTCLI_WALLET_ENCRYPTION_ENABLED": "true"
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
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )
    config.addinivalue_line(
        "markers", "network: marks tests as network tests"
    )


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
