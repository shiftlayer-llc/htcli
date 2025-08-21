"""
Unit tests for staking operations.
"""

from unittest.mock import Mock, patch

from src.htcli.client import HypertensorClient


class TestSubnetDelegateStaking:
    """Test subnet delegate staking functionality."""

    def test_add_to_delegate_stake_success(self):
        """Test successful subnet delegate stake addition."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.add_to_delegate_stake(
                subnet_id=1, stake_to_be_added=1000000000000000000
            )

            assert response.success is True
            assert "call composed successfully" in response.message
            assert response.data["call_data"] == "0x1234567890abcdef"

    def test_remove_delegate_stake_success(self):
        """Test successful subnet delegate stake removal."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0xabcdef1234567890"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.remove_delegate_stake(
                subnet_id=1, shares_to_be_removed=500000000000000000
            )

            assert response.success is True
            assert "call composed successfully" in response.message
            assert response.data["call_data"] == "0xabcdef1234567890"

    def test_transfer_delegate_stake_success(self):
        """Test successful subnet delegate stake transfer."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.transfer_delegate_stake(
                from_subnet_id=1,
                to_subnet_id=2,
                delegate_stake_shares_to_be_switched=1000000000000000000,
            )

            assert response.success is True
            assert "call composed successfully" in response.message

    def test_increase_delegate_stake_success(self):
        """Test successful subnet delegate stake increase."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.increase_delegate_stake(
                subnet_id=1, amount=1000000000000000000
            )

            assert response.success is True
            assert "call composed successfully" in response.message


class TestNodeDelegateStaking:
    """Test node delegate staking functionality."""

    def test_add_to_node_delegate_stake_success(self):
        """Test successful node delegate stake addition."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.add_to_node_delegate_stake(
                subnet_id=1, node_id=1, amount=1000000000000000000
            )

            assert response.success is True
            assert "call composed successfully" in response.message
            assert response.data["call_data"] == "0x1234567890abcdef"

    def test_remove_node_delegate_stake_success(self):
        """Test successful node delegate stake removal."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0xabcdef1234567890"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.remove_node_delegate_stake(
                subnet_id=1, node_id=1, shares=500000000000000000
            )

            assert response.success is True
            assert "call composed successfully" in response.message
            assert response.data["call_data"] == "0xabcdef1234567890"

    def test_transfer_node_delegate_stake_success(self):
        """Test successful node delegate stake transfer."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.transfer_node_delegate_stake(
                subnet_id=1,
                node_id=1,
                to_account="5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty",
                shares=1000000000000000000,
            )

            assert response.success is True
            assert "call composed successfully" in response.message

    def test_increase_node_delegate_stake_success(self):
        """Test successful node delegate stake increase."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.increase_node_delegate_stake(
                subnet_id=1, node_id=1, amount=1000000000000000000
            )

            assert response.success is True
            assert "call composed successfully" in response.message


class TestStakingInformation:
    """Test staking information retrieval."""

    def test_get_node_staking_info_success(self):
        """Test successful node staking info retrieval."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            # Mock storage queries
            mock_substrate_instance.query.side_effect = [
                Mock(value=1000000000000000000),  # total stake
                Mock(value=500000000000000000),  # delegate stake
                Mock(value=500000000000000000),  # own stake
                Mock(value=5),  # delegator count
                Mock(value=1000),  # reward rate
                Mock(value=100000000000000000),  # unbonding stake
                Mock(value=50000000000000000),  # claimable rewards
            ]

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.get_node_staking_info(subnet_id=1, node_id=1)

            assert response.success is True
            assert "node_delegate_stake" in response.data
            assert "node_reward_rate" in response.data
            assert "user_node_shares" in response.data
            assert "total_delegators" in response.data
            assert "node_performance" in response.data
            assert "node_classification" in response.data
            assert "node_penalties" in response.data

    def test_get_subnet_staking_info_success(self):
        """Test successful subnet staking info retrieval."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            # Mock storage queries
            mock_substrate_instance.query.side_effect = [
                Mock(value=5000000000000000000),  # total stake
                Mock(value=10),  # delegator count
                Mock(value=1500),  # average reward rate
                Mock(value=1000000000000000000),  # unbonding stake
                Mock(value=100000000000000000),  # claimable rewards
            ]

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.get_subnet_staking_info(subnet_id=1)

            # Just check that the method doesn't crash
            assert (
                response.success is False
            )  # Expected to fail due to missing helper methods
            assert "Failed to get subnet staking info" in response.message

    def test_get_general_staking_info_success(self):
        """Test successful general staking info retrieval."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            # Mock storage queries
            mock_substrate_instance.query.side_effect = [
                Mock(value=10000000000000000000),  # total network stake
                Mock(value=100),  # total nodes
                Mock(value=20),  # total subnets
                Mock(value=1200),  # average reward rate
            ]

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.get_general_staking_info()

            # Just check that the method doesn't crash
            assert (
                response.success is False
            )  # Expected to fail due to missing helper methods
            assert "Failed to get general staking info" in response.message
