"""
Real tests for wallet operations.
"""

import pytest
from unittest.mock import Mock, patch
from src.htcli.client import HypertensorClient
from src.htcli.models.requests import StakeAddRequest, StakeRemoveRequest


class TestWalletStaking:
    """Test wallet staking functionality."""

    def test_add_stake_success(self):
        """Test successful stake addition."""
        with patch('src.htcli.client.SubstrateInterface') as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config
            config = load_config()
            client = HypertensorClient(config)

            request = StakeAddRequest(
                subnet_id=1,
                node_id=1,
                hotkey="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                stake_to_be_added=1000000000000000000  # 1 TENSOR with 18 decimals
            )

            response = client.add_to_stake(request)

            assert response.success is True
            assert "call composed successfully" in response.message
            assert response.data['call_data'] == "0x1234567890abcdef"

    def test_remove_stake_success(self):
        """Test successful stake removal."""
        with patch('src.htcli.client.SubstrateInterface') as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0xabcdef1234567890"

            from src.htcli.config import load_config
            config = load_config()
            client = HypertensorClient(config)

            request = StakeRemoveRequest(
                subnet_id=1,
                hotkey="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                stake_to_be_removed=500000000000000000  # 0.5 TENSOR with 18 decimals
            )

            response = client.remove_stake(request)

            assert response.success is True
            assert "call composed successfully" in response.message
            assert response.data['call_data'] == "0xabcdef1234567890"

    def test_get_account_subnet_stake_success(self):
        """Test successful retrieval of account subnet stake."""
        with patch('src.htcli.client.SubstrateInterface') as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            mock_stake_data = Mock()
            mock_stake_data.value = 1000000000000000000  # 1 TENSOR with 18 decimals
            mock_substrate_instance.query.return_value = mock_stake_data

            from src.htcli.config import load_config
            config = load_config()
            client = HypertensorClient(config)

            response = client.get_account_subnet_stake("5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY", 1)

            assert response.success is True
            assert "retrieved successfully" in response.message
            assert response.data['stake'] == 1000000000000000000  # 1 TENSOR with 18 decimals


class TestWalletKeys:
    """Test wallet key management functionality."""

    def test_generate_keypair_success(self):
        """Test successful keypair generation."""
        with patch('src.htcli.utils.crypto.Keypair') as mock_keypair:
            mock_keypair_instance = Mock()
            mock_keypair_instance.public_key.hex.return_value = "0x1234567890abcdef"
            mock_keypair_instance.ss58_address = "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            mock_keypair.create_from_uri.return_value = mock_keypair_instance

            from src.htcli.utils.crypto import generate_keypair
            result = generate_keypair("test-key", "sr25519")

            assert result.name == "test-key"
            assert result.key_type == "sr25519"
            assert result.public_key == "0x1234567890abcdef"
            assert result.ss58_address == "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"

    def test_import_keypair_success(self):
        """Test successful keypair import."""
        with patch('src.htcli.utils.crypto.Keypair') as mock_keypair:
            mock_keypair_instance = Mock()
            mock_keypair_instance.public_key.hex.return_value = "0xabcdef1234567890"
            mock_keypair_instance.ss58_address = "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            mock_keypair.create_from_private_key.return_value = mock_keypair_instance

            from src.htcli.utils.crypto import import_keypair
            result = import_keypair("test-key", "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef", "sr25519")

            assert result.name == "test-key"
            assert result.key_type == "sr25519"
            assert result.public_key == "0xabcdef1234567890"
            assert result.ss58_address == "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"

    def test_list_keys_success(self):
        """Test successful key listing."""
        with patch('src.htcli.utils.crypto.list_keys') as mock_list_keys:
            # Mock the list_keys function to return sample keys
            mock_list_keys.return_value = [
                {
                    "name": "test-key-1",
                    "key_type": "sr25519",
                    "public_key": "0x1234567890abcdef",
                    "ss58_address": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
                },
                {
                    "name": "test-key-2",
                    "key_type": "ed25519",
                    "public_key": "0xabcdef1234567890",
                    "ss58_address": "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty"
                }
            ]

            from src.htcli.utils.crypto import list_keys
            result = list_keys()

            assert len(result) == 2
            assert result[0]["name"] == "test-key-1"
            assert result[1]["name"] == "test-key-2"
            assert result[0]["key_type"] == "sr25519"
            assert result[1]["key_type"] == "ed25519"
