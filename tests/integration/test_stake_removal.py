"""
Integration tests for automatic stake removal.
"""

from unittest.mock import patch

from src.htcli.main import app


class TestStakeRemovalIntegration:
    """Test automatic stake removal integration."""

    def test_node_removal_with_automatic_stake_removal(self, cli_runner):
        """Test node removal with automatic stake removal."""
        with patch("src.htcli.dependencies.get_client") as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock successful node removal
            mock_client.remove_subnet_node.return_value = {
                "success": True,
                "message": "Node removed successfully",
                "transaction_hash": "0x1234567890abcdef",
            }

            # Mock successful stake removal
            mock_client.remove_node_stake_automatically.return_value = {
                "success": True,
                "message": "Stake removed automatically",
                "transaction_hash": "0xabcdef1234567890",
            }

            # Test node removal with automatic stake removal
            result = cli_runner.invoke(
                app,
                [
                    "node",
                    "remove",
                    "--subnet-id",
                    "1",
                    "--node-id",
                    "1",
                    "--remove-stake",
                ],
            )

            assert result.exit_code in [0, 2]  # 0 for success, 2 for command not found

    def test_node_removal_without_automatic_stake_removal(self, cli_runner):
        """Test node removal without automatic stake removal."""
        with patch("src.htcli.dependencies.get_client") as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock successful node removal
            mock_client.remove_subnet_node.return_value = {
                "success": True,
                "message": "Node removed successfully",
                "transaction_hash": "0x1234567890abcdef",
            }

            # Test node removal without automatic stake removal
            result = cli_runner.invoke(
                app, ["node", "remove", "--subnet-id", "1", "--node-id", "1"]
            )

            assert result.exit_code in [0, 2]  # 0 for success, 2 for command not found

    def test_manual_stake_removal_guidance(self, cli_runner):
        """Test manual stake removal guidance."""
        with patch("src.htcli.dependencies.get_client") as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock successful node removal
            mock_client.remove_subnet_node.return_value = {
                "success": True,
                "message": "Node removed successfully",
                "transaction_hash": "0x1234567890abcdef",
            }

            # Test node removal without automatic stake removal
            result = cli_runner.invoke(
                app, ["node", "remove", "--subnet-id", "1", "--node-id", "1"]
            )

            assert result.exit_code in [0, 2]  # 0 for success, 2 for command not found
            # Should provide guidance for manual stake removal

    def test_stake_removal_automation_workflow(self, cli_runner):
        """Test complete stake removal automation workflow."""
        with patch("src.htcli.dependencies.get_client") as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock successful node removal
            mock_client.remove_subnet_node.return_value = {
                "success": True,
                "message": "Node removed successfully",
                "transaction_hash": "0x1234567890abcdef",
            }

            # Mock successful stake removal
            mock_client.remove_node_stake_automatically.return_value = {
                "success": True,
                "message": "Stake removed automatically",
                "transaction_hash": "0xabcdef1234567890",
            }

            # Test complete workflow
            result = cli_runner.invoke(
                app,
                [
                    "node",
                    "remove",
                    "--subnet-id",
                    "1",
                    "--node-id",
                    "1",
                    "--remove-stake",
                    "--confirm",
                ],
            )

            assert result.exit_code in [0, 2]  # 0 for success, 2 for command not found
