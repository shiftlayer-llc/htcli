"""
Real tests for subnet operations.
"""

import pytest
from unittest.mock import Mock, patch
from src.htcli.client import HypertensorClient
from src.htcli.models.requests import SubnetRegisterRequest, SubnetNodeAddRequest
from src.htcli.models.responses import SubnetRegisterResponse, SubnetInfoResponse, SubnetsListResponse, NodeAddResponse, NodesListResponse


class TestSubnetRegister:
    """Test subnet registration functionality."""

    def test_register_subnet_success(self):
        """Test successful subnet registration."""
        with patch('src.htcli.client.SubstrateInterface') as mock_substrate:
            # Mock the substrate interface
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            # Mock compose_call to return a call data
            mock_substrate_instance.compose_call.return_value = "0x1234567890abcdef"

            # Create client
            from src.htcli.config import load_config
            config = load_config()
            client = HypertensorClient(config)

            # Create request
            request = SubnetRegisterRequest(
                path="test-subnet",
                memory_mb=1024,
                registration_blocks=1000,
                entry_interval=100,
                max_node_registration_epochs=50,
                node_registration_interval=20,
                node_activation_interval=30,
                node_queue_period=40,
                max_node_penalties=5,
                coldkey_whitelist=[]
            )

            # Test registration
            response = client.register_subnet(request)

            # Verify response
            assert response.success is True
            assert "call composed successfully" in response.message
            assert response.data['call_data'] == "0x1234567890abcdef"

            # Verify compose_call was called with correct parameters
            mock_substrate_instance.compose_call.assert_called_once_with(
                call_module='Network',
                call_function='register_subnet',
                call_params={
                    'subnet_data': {
                        'path': 'test-subnet',
                        'memory_mb': 1024,
                        'registration_blocks': 1000,
                        'entry_interval': 100,
                        'max_node_registration_epochs': 50,
                        'node_registration_interval': 20,
                        'node_activation_interval': 30,
                        'node_queue_period': 40,
                        'max_node_penalties': 5,
                        'coldkey_whitelist': []
                    }
                }
            )

    def test_register_subnet_connection_error(self):
        """Test subnet registration with connection error."""
        with patch('src.htcli.client.SubstrateInterface') as mock_substrate:
            # Mock connection failure
            mock_substrate.side_effect = Exception("Connection failed")

            # Create client
            from src.htcli.config import load_config
            config = load_config()
            client = HypertensorClient(config)

            # Create request
            request = SubnetRegisterRequest(
                path="test-subnet",
                memory_mb=1024,
                registration_blocks=1000,
                entry_interval=100,
                max_node_registration_epochs=50,
                node_registration_interval=20,
                node_activation_interval=30,
                node_queue_period=40,
                max_node_penalties=5,
                coldkey_whitelist=[]
            )

            # Test registration should raise exception
            with pytest.raises(Exception):
                client.register_subnet(request)


class TestSubnetManage:
    """Test subnet management functionality."""

    def test_get_subnets_data_success(self):
        """Test successful retrieval of subnets data."""
        with patch('src.htcli.client.SubstrateInterface') as mock_substrate:
            # Mock the substrate interface
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            # Mock storage queries
            mock_total_subnets = Mock()
            mock_total_subnets.value = 2
            mock_substrate_instance.query.side_effect = [
                mock_total_subnets,  # TotalSubnetUids
                Mock(value={'path': 'subnet1', 'activated': 1}),  # SubnetsData for subnet 1
                Mock(value={'path': 'subnet2', 'activated': 0})   # SubnetsData for subnet 2
            ]

            # Create client
            from src.htcli.config import load_config
            config = load_config()
            client = HypertensorClient(config)

            # Test get subnets data
            response = client.get_subnets_data()

            # Verify response
            assert response.success is True
            assert "Retrieved 2 subnets" in response.message
            assert len(response.data['subnets']) == 2

            # Verify storage queries were called
            assert mock_substrate_instance.query.call_count == 3

    def test_get_subnet_data_success(self):
        """Test successful retrieval of specific subnet data."""
        with patch('src.htcli.client.SubstrateInterface') as mock_substrate:
            # Mock the substrate interface
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            # Mock storage query
            mock_subnet_data = Mock()
            mock_subnet_data.value = {'path': 'test-subnet', 'activated': 1}
            mock_substrate_instance.query.return_value = mock_subnet_data

            # Create client
            from src.htcli.config import load_config
            config = load_config()
            client = HypertensorClient(config)

            # Test get subnet data
            response = client.get_subnet_data(1)

            # Verify response
            assert response.success is True
            assert "retrieved successfully" in response.message
            assert response.data['subnet_id'] == 1
            assert response.data['subnet_data']['path'] == 'test-subnet'

            # Verify storage query was called
            mock_substrate_instance.query.assert_called_once_with(
                module='Network',
                storage_function='SubnetsData',
                params=[1]
            )


class TestSubnetNodes:
    """Test subnet node operations."""

    def test_add_subnet_node_success(self):
        """Test successful node addition to subnet."""
        with patch('src.htcli.client.SubstrateInterface') as mock_substrate:
            # Mock the substrate interface
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            # Mock compose_call to return a call data
            mock_substrate_instance.compose_call.return_value = "0xabcdef1234567890"

            # Create client
            from src.htcli.config import load_config
            config = load_config()
            client = HypertensorClient(config)

            # Create request
            request = SubnetNodeAddRequest(
                subnet_id=1,
                peer_id="QmTestPeerId123456789",
                hotkey="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                delegate_reward_rate=1000,
                stake_to_be_added=1000000000000
            )

            # Test node addition
            response = client.add_subnet_node(request)

            # Verify response
            assert response.success is True
            assert "call composed successfully" in response.message
            assert response.data['call_data'] == "0xabcdef1234567890"

            # Verify compose_call was called with correct parameters
            mock_substrate_instance.compose_call.assert_called_once_with(
                call_module='Network',
                call_function='add_subnet_node',
                call_params={
                    'subnet_id': 1,
                    'hotkey': '5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY',
                    'peer_id': 'QmTestPeerId123456789',
                    'bootstrap_peer_id': 'QmTestPeerId123456789',
                    'delegate_reward_rate': 1000,
                    'stake_to_be_added': 1000000000000,
                    'a': '1000000000000',
                    'b': '1000',
                    'c': '1'
                }
            )

    def test_get_subnet_nodes_success(self):
        """Test successful retrieval of subnet nodes."""
        with patch('src.htcli.client.SubstrateInterface') as mock_substrate:
            # Mock the substrate interface
            mock_substrate_instance = Mock()
            mock_substrate.return_value = mock_substrate_instance

            # Mock storage queries
            mock_total_nodes = Mock()
            mock_total_nodes.value = 2
            mock_substrate_instance.query.side_effect = [
                mock_total_nodes,  # TotalSubnetNodes
                Mock(value={'peer_id': 'QmNode1', 'hotkey': '5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY'}),  # SubnetNodesData for node 1
                Mock(value={'peer_id': 'QmNode2', 'hotkey': '5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY'})   # SubnetNodesData for node 2
            ]

            # Create client
            from src.htcli.config import load_config
            config = load_config()
            client = HypertensorClient(config)

            # Test get subnet nodes
            response = client.get_subnet_nodes(1)

            # Verify response
            assert response.success is True
            assert "Retrieved 2 nodes for subnet 1" in response.message
            assert len(response.data['nodes']) == 2

            # Verify storage queries were called
            assert mock_substrate_instance.query.call_count == 3
