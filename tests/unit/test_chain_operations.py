"""
Real tests for chain operations.
"""

from unittest.mock import Mock, patch

from src.htcli.client import HypertensorClient


class TestChainInfo:
    """Test chain information functionality."""

    def test_get_network_stats_success(self):
        """Test successful network statistics retrieval."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            # Mock storage queries
            mock_total_subnets = Mock()
            mock_total_subnets.value = 2
            mock_total_active_subnets = Mock()
            mock_total_active_subnets.value = 1
            mock_total_active_nodes = Mock()
            mock_total_active_nodes.value = 5
            mock_total_stake = Mock()
            mock_total_stake.value = 1000000000000000000  # 1 TENSOR with 18 decimals

            mock_substrate_instance.query.side_effect = [
                mock_total_subnets,
                mock_total_active_subnets,
                mock_total_active_nodes,
                mock_total_stake,
            ]

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.get_network_stats()

            assert response.success is True
            assert "retrieved successfully" in response.message
            assert response.data["total_subnets"] == 2
            assert response.data["total_active_subnets"] == 1
            assert response.data["total_active_nodes"] == 5
            assert (
                response.data["total_stake"] == 1000000000000000000
            )  # 1 TENSOR with 18 decimals

    def test_get_current_epoch_success(self):
        """Test successful epoch information retrieval."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            # Mock storage query
            mock_current_epoch = Mock()
            mock_current_epoch.value = 42
            mock_substrate_instance.query.return_value = mock_current_epoch

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.get_current_epoch()

            assert response.success is True
            assert "retrieved successfully" in response.message
            assert response.data["current_epoch"] == 42

    def test_get_balance_success(self):
        """Test successful balance retrieval."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            # Mock account info query
            mock_account_info = Mock()
            mock_account_info.value = {
                "data": {
                    "free": 31662054793350007812500,
                    "reserved": 0,
                    "misc_frozen": 0,
                    "fee_frozen": 0,
                }
            }
            mock_substrate_instance.query.return_value = mock_account_info

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.get_balance(
                "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            )

            assert response.success is True
            assert "retrieved successfully" in response.message
            assert (
                response.data["address"]
                == "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            )
            assert (
                response.data["balance"] == 31662054793350007812500
            )  # Balance with 18 decimals
            assert "TENSOR" in response.data["formatted_balance"]


class TestChainQuery:
    """Test chain query functionality."""

    def test_get_peers_success(self):
        """Test successful peers retrieval."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            # Mock RPC request
            mock_peers_response = {
                "result": [
                    {"peer_id": "QmPeer1", "address": "127.0.0.1:30333"},
                    {"peer_id": "QmPeer2", "address": "127.0.0.2:30333"},
                ]
            }
            mock_substrate_instance.rpc_request.return_value = mock_peers_response

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.get_peers()

            assert response.success is True
            assert "retrieved successfully" in response.message
            assert len(response.data["peers"]) == 2
            assert response.data["peers"][0]["peer_id"] == "QmPeer1"

    def test_get_block_info_success(self):
        """Test successful block information retrieval."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            # Mock block operations
            mock_substrate_instance.get_chain_head.return_value = "0x1234567890abcdef"
            mock_substrate_instance.get_block_hash.return_value = "0x1234567890abcdef"
            mock_substrate_instance.get_block_header.return_value = {
                "number": 12345,
                "parentHash": "0xabcdef1234567890",
                "stateRoot": "0x1234567890abcdef",
                "extrinsicsRoot": "0xabcdef1234567890",
            }
            mock_substrate_instance.get_block.return_value = {
                "extrinsics": ["extrinsic1", "extrinsic2"]
            }

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.get_block_info()

            assert response.success is True
            assert "retrieved successfully" in response.message
            assert response.data["block_number"] == 12345
            assert response.data["extrinsics_count"] == 2
            assert "0x1234567890abcdef" in response.data["block_hash"]
