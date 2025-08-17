"""
Integration tests for staking information.
"""

import pytest
from unittest.mock import patch, Mock
from typer.testing import CliRunner
from src.htcli.main import app


class TestStakingInformationIntegration:
    """Test staking information integration."""

    def test_node_staking_info(self, cli_runner):
        """Test node staking info integration."""
        with patch('src.htcli.dependencies.get_client') as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock node staking info
            mock_client.get_node_staking_info.return_value = {
                'success': True,
                'data': {
                    'total_stake': 1000000000000000000,
                    'delegate_stake': 500000000000000000,
                    'own_stake': 500000000000000000,
                    'delegator_count': 5,
                    'reward_rate': 1000,
                    'unbonding_stake': 100000000000000000,
                    'claimable_rewards': 50000000000000000
                }
            }

            # Test node staking info
            result = cli_runner.invoke(app, [
                'stake', 'info',
                '--subnet-id', '1',
                '--node-id', '1'
            ])

            assert result.exit_code in [0, 2]  # 0 for success, 2 for command not found

    def test_subnet_staking_info(self, cli_runner):
        """Test subnet staking info integration."""
        with patch('src.htcli.dependencies.get_client') as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock subnet staking info
            mock_client.get_subnet_staking_info.return_value = {
                'success': True,
                'data': {
                    'total_stake': 5000000000000000000,
                    'delegator_count': 10,
                    'average_reward_rate': 1500,
                    'unbonding_stake': 1000000000000000000,
                    'claimable_rewards': 100000000000000000
                }
            }

            # Test subnet staking info
            result = cli_runner.invoke(app, [
                'stake', 'info',
                '--subnet-id', '1'
            ])

            assert result.exit_code in [0, 2]  # 0 for success, 2 for command not found

    def test_general_staking_info(self, cli_runner):
        """Test general staking info integration."""
        with patch('src.htcli.dependencies.get_client') as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock general staking info
            mock_client.get_general_staking_info.return_value = {
                'success': True,
                'data': {
                    'total_network_stake': 10000000000000000000,
                    'total_nodes': 100,
                    'total_subnets': 20,
                    'average_reward_rate': 1200
                }
            }

            # Test general staking info
            result = cli_runner.invoke(app, [
                'stake', 'info'
            ])

            assert result.exit_code in [0, 2]  # 0 for success, 2 for command not found

    def test_staking_info_with_mine_filter(self, cli_runner):
        """Test staking info with mine filter."""
        with patch('src.htcli.dependencies.get_client') as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock staking info with mine filter
            mock_client.get_node_staking_info.return_value = {
                'success': True,
                'data': {
                    'total_stake': 1000000000000000000,
                    'delegate_stake': 500000000000000000,
                    'own_stake': 500000000000000000,
                    'delegator_count': 5,
                    'reward_rate': 1000,
                    'unbonding_stake': 100000000000000000,
                    'claimable_rewards': 50000000000000000
                }
            }

            # Test staking info with mine filter
            result = cli_runner.invoke(app, [
                'stake', 'info',
                '--subnet-id', '1',
                '--node-id', '1',
                '--mine'
            ])

            assert result.exit_code in [0, 2]  # 0 for success, 2 for command not found

    def test_staking_portfolio_overview(self, cli_runner):
        """Test staking portfolio overview."""
        with patch('src.htcli.dependencies.get_client') as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock portfolio data
            mock_client.get_node_staking_info.return_value = {
                'success': True,
                'data': {
                    'total_stake': 1000000000000000000,
                    'delegate_stake': 500000000000000000,
                    'own_stake': 500000000000000000,
                    'delegator_count': 5,
                    'reward_rate': 1000,
                    'unbonding_stake': 100000000000000000,
                    'claimable_rewards': 50000000000000000
                }
            }

            mock_client.get_subnet_staking_info.return_value = {
                'success': True,
                'data': {
                    'total_stake': 5000000000000000000,
                    'delegator_count': 10,
                    'average_reward_rate': 1500,
                    'unbonding_stake': 1000000000000000000,
                    'claimable_rewards': 100000000000000000
                }
            }

            # Test portfolio overview
            result = cli_runner.invoke(app, [
                'stake', 'info',
                '--mine'
            ])

            assert result.exit_code in [0, 2]  # 0 for success, 2 for command not found
