"""
Unit tests for node operations.
"""

from unittest.mock import Mock, patch
from src.htcli.client import HypertensorClient


class TestNodeRegistration:
    """Test node registration functionality."""

    def test_register_subnet_node_success(self):
        """Test successful node registration."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            from src.htcli.models.requests import SubnetNodeAddRequest

            request = SubnetNodeAddRequest(
                subnet_id=1,
                hotkey="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                peer_id="QmTestPeerId1234567890abcdef",
                delegate_reward_rate=1000,
                stake_to_be_added=1000000000000000000,
            )
            response = client.add_subnet_node(request)

            assert response.success is True
            assert "call composed successfully" in response.message
            assert response.data["call_data"] == "0x1234567890abcdef"

    def test_register_subnet_node_with_keypair(self):
        """Test node registration with keypair submission."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            mock_receipt = Mock()
            mock_receipt.extrinsic_hash = "0x1234567890abcdef"
            mock_receipt.block_number = 12345
            mock_substrate_instance.submit_extrinsic.return_value = mock_receipt

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            mock_keypair = Mock()
            mock_keypair.ss58_address = (
                "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            )

            from src.htcli.models.requests import SubnetNodeAddRequest

            request = SubnetNodeAddRequest(
                subnet_id=1,
                hotkey="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                peer_id="QmTestPeerId1234567890abcdef",
                delegate_reward_rate=1000,
                stake_to_be_added=1000000000000000000,
            )
            response = client.add_subnet_node(request, keypair=mock_keypair)

            assert response.success is True
            assert response.transaction_hash == "0x1234567890abcdef"
            assert response.block_number == 12345


class TestNodeActivation:
    """Test node activation functionality."""

    def test_activate_subnet_node_success(self):
        """Test successful node activation."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0xabcdef1234567890"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.activate_subnet_node(subnet_id=1, node_id=1)

            assert response.success is True
            assert "call composed successfully" in response.message
            assert response.data["call_data"] == "0xabcdef1234567890"

    def test_activate_subnet_node_with_keypair(self):
        """Test node activation with keypair submission."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            mock_receipt = Mock()
            mock_receipt.extrinsic_hash = "0xabcdef1234567890"
            mock_receipt.block_number = 12346
            mock_substrate_instance.submit_extrinsic.return_value = mock_receipt

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            mock_keypair = Mock()
            mock_keypair.ss58_address = (
                "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            )

            response = client.activate_subnet_node(
                subnet_id=1, node_id=1, keypair=mock_keypair
            )

            assert response.success is True
            assert response.transaction_hash == "0xabcdef1234567890"
            assert response.block_number == 12346


class TestNodeDeactivation:
    """Test node deactivation functionality."""

    def test_deactivate_subnet_node_success(self):
        """Test successful node deactivation."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.deactivate_subnet_node(subnet_id=1, node_id=1)

            assert response.success is True
            assert "call composed successfully" in response.message

    def test_reactivate_subnet_node_success(self):
        """Test successful node reactivation."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.reactivate_subnet_node(subnet_id=1, node_id=1)

            assert response.success is True
            assert "call composed successfully" in response.message


class TestNodeRemoval:
    """Test node removal functionality."""

    def test_remove_subnet_node_success(self):
        """Test successful node removal."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.remove_subnet_node(subnet_id=1, subnet_node_id=1)

            assert response.success is True
            assert "call composed successfully" in response.message

    def test_remove_subnet_node_with_stake_removal(self):
        """Test node removal with automatic stake removal."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.remove_subnet_node(subnet_id=1, subnet_node_id=1)

            assert response.success is True
            assert "call composed successfully" in response.message


class TestNodeUpdates:
    """Test node update functionality."""

    def test_update_node_delegate_reward_rate(self):
        """Test updating node delegate reward rate."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.update_node_delegate_reward_rate(
                subnet_id=1, node_id=1, new_delegate_reward_rate=2000
            )

            assert response.success is True
            assert "call composed successfully" in response.message

    def test_update_node_coldkey(self):
        """Test updating node coldkey."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.update_node_coldkey(
                subnet_id=1,
                hotkey="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                new_coldkey="5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty",
            )

            assert response.success is True
            assert "call composed successfully" in response.message

    def test_update_node_hotkey(self):
        """Test updating node hotkey."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.update_node_hotkey(
                subnet_id=1,
                old_hotkey="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                new_hotkey="5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty",
            )

            assert response.success is True
            assert "call composed successfully" in response.message


class TestNodeCleanup:
    """Test node cleanup functionality."""

    def test_cleanup_expired_node_success(self):
        """Test successful expired node cleanup."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.cleanup_expired_node(
                subnet_id=1, node_id=1, cleanup_type="registered"
            )

            assert response.success is True
            assert "call composed successfully" in response.message
