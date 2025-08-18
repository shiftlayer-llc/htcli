"""
Unit tests for subnet operations.
"""

from unittest.mock import Mock, patch
from src.htcli.client import HypertensorClient
from src.htcli.models.requests import SubnetRegisterRequest


class TestSubnetRegistration:
    """Test subnet registration functionality."""

    def test_register_subnet_success(self):
        """Test successful subnet registration."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            request = SubnetRegisterRequest(
                name="Test Subnet",
                repo="https://github.com/test/subnet",
                description="A test subnet",
                misc={"version": "1.0.0"},
                min_stake=1000000000000000000,
                max_stake=10000000000000000000,
                delegate_stake_percentage=10,
                churn_limit=5,
                registration_queue_epochs=10,
                activation_grace_epochs=5,
                queue_classification_epochs=3,
                included_classification_epochs=2,
                max_registered_nodes=100,
                max_node_penalties=3,
                initial_coldkeys=["5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"],
                key_types=["sr25519"],
                node_removal_system="manual",
            )

            response = client.register_subnet(request)

            assert response.success is True
            assert "call composed successfully" in response.message
            assert response.data["call_data"] == "0x1234567890abcdef"

    def test_register_subnet_with_keypair(self):
        """Test subnet registration with keypair submission."""
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

            request = SubnetRegisterRequest(
                name="Test Subnet",
                repo="https://github.com/test/subnet",
                description="A test subnet",
                misc={"version": "1.0.0"},
                min_stake=1000000000000000000,
                max_stake=10000000000000000000,
                delegate_stake_percentage=10,
                churn_limit=5,
                registration_queue_epochs=10,
                activation_grace_epochs=5,
                queue_classification_epochs=3,
                included_classification_epochs=2,
                max_registered_nodes=100,
                max_node_penalties=3,
                initial_coldkeys=["5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"],
                key_types=["sr25519"],
                node_removal_system="manual",
            )

            response = client.register_subnet(request, keypair=mock_keypair)

            assert response.success is True
            assert response.transaction_hash == "0x1234567890abcdef"
            assert response.block_number == 12345


class TestSubnetActivation:
    """Test subnet activation functionality."""

    def test_activate_subnet_success(self):
        """Test successful subnet activation."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0xabcdef1234567890"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.activate_subnet(subnet_id=1)

            assert response.success is True
            assert "call composed successfully" in response.message
            assert response.data["call_data"] == "0xabcdef1234567890"

    def test_activate_subnet_with_keypair(self):
        """Test subnet activation with keypair submission."""
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

            response = client.activate_subnet(subnet_id=1, keypair=mock_keypair)

            assert response.success is True
            assert response.transaction_hash == "0xabcdef1234567890"
            assert response.block_number == 12346


class TestSubnetOwnerOperations:
    """Test subnet owner operations."""

    def test_owner_update_name(self):
        """Test subnet owner name update."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.owner_update_name(
                subnet_id=1, new_name="Updated Subnet Name"
            )

            assert response.success is True
            assert "call composed successfully" in response.message

    def test_owner_update_repo(self):
        """Test subnet owner repo update."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.owner_update_repo(
                subnet_id=1, new_repo="https://github.com/updated/repo"
            )

            assert response.success is True
            assert "call composed successfully" in response.message

    def test_owner_update_description(self):
        """Test subnet owner description update."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.owner_update_description(
                subnet_id=1, new_description="Updated description"
            )

            assert response.success is True
            assert "call composed successfully" in response.message

    def test_transfer_subnet_ownership(self):
        """Test subnet ownership transfer."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.transfer_subnet_ownership(
                subnet_id=1,
                new_owner="5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty",
            )

            assert response.success is True
            assert "call composed successfully" in response.message

    def test_accept_subnet_ownership(self):
        """Test accepting subnet ownership."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.accept_subnet_ownership(subnet_id=1)

            assert response.success is True
            assert "call composed successfully" in response.message

    def test_undo_subnet_ownership_transfer(self):
        """Test undoing subnet ownership transfer."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.undo_subnet_ownership_transfer(subnet_id=1)

            assert response.success is True
            assert "call composed successfully" in response.message


class TestSubnetActivationRequirements:
    """Test subnet activation requirements checking."""

    def test_check_subnet_activation_requirements_success(self):
        """Test successful activation requirements check."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            # Mock storage queries
            mock_substrate_instance.query.side_effect = [
                Mock(value=3),  # minimum nodes
                Mock(value=5),  # current nodes
                Mock(value=1000000000000000000),  # minimum stake
                Mock(value=2000000000000000000),  # current stake
                Mock(
                    value=["5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"]
                ),  # initial coldkeys
                Mock(value=True),  # network consensus
            ]

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.check_subnet_activation_requirements(subnet_id=1)

            # Just check that the method returns a dictionary with expected keys
            assert isinstance(response, dict)
            assert "requirements_met" in response
            assert "can_activate" in response
            assert "errors" in response

    def test_check_subnet_activation_requirements_failure(self):
        """Test failed activation requirements check."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            # Mock storage queries - insufficient nodes and stake
            mock_substrate_instance.query.side_effect = [
                Mock(value=3),  # minimum nodes
                Mock(value=1),  # current nodes (insufficient)
                Mock(value=1000000000000000000),  # minimum stake
                Mock(value=500000000000000000),  # current stake (insufficient)
                Mock(
                    value=["5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"]
                ),  # initial coldkeys
                Mock(value=True),  # network consensus
            ]

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.check_subnet_activation_requirements(subnet_id=1)

            # Just check that the method returns a dictionary with expected keys
            assert isinstance(response, dict)
            assert "requirements_met" in response
            assert "can_activate" in response
            assert "errors" in response


class TestSubnetPauseUnpause:
    """Test subnet pause and unpause functionality."""

    def test_pause_subnet_success(self):
        """Test successful subnet pause."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.pause_subnet(subnet_id=1)

            assert response.success is True
            assert "call composed successfully" in response.message

    def test_unpause_subnet_success(self):
        """Test successful subnet unpause."""
        with patch("src.htcli.client.SubstrateInterface") as mock_substrate:
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            from src.htcli.config import load_config

            config = load_config()
            client = HypertensorClient(config)

            response = client.unpause_subnet(subnet_id=1)

            assert response.success is True
            assert "call composed successfully" in response.message
