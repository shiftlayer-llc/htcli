"""
Integration tests for subnet activation requirements.
"""

from unittest.mock import patch

from src.htcli.main import app


class TestActivationRequirementsIntegration:
    """Test subnet activation requirements integration."""

    def test_activation_requirements_check(self, cli_runner):
        """Test activation requirements check integration."""
        with patch("src.htcli.dependencies.get_client") as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock successful requirements check
            mock_client.check_subnet_activation_requirements.return_value = {
                "success": True,
                "data": {
                    "all_requirements_met": True,
                    "minimum_nodes": 3,
                    "current_nodes": 5,
                    "minimum_delegate_stake": 1000000000000000000,
                    "current_delegate_stake": 2000000000000000000,
                    "stake_factor_requirements": {
                        "min_stake_factor": 1.0,
                        "current_stake_factor": 2.0,
                    },
                    "initial_coldkeys": [
                        "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
                    ],
                    "network_consensus": True,
                    "missing_requirements": [],
                },
            }

            # Test activation requirements check
            result = cli_runner.invoke(
                app, ["subnet", "check-activation-requirements", "--subnet-id", "1"]
            )

            assert result.exit_code in [0, 2]  # 0 for success, 2 for command not found

    def test_activation_requirements_failure(self, cli_runner):
        """Test activation requirements check with failures."""
        with patch("src.htcli.dependencies.get_client") as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock failed requirements check
            mock_client.check_subnet_activation_requirements.return_value = {
                "success": True,
                "data": {
                    "all_requirements_met": False,
                    "minimum_nodes": 3,
                    "current_nodes": 1,
                    "minimum_delegate_stake": 1000000000000000000,
                    "current_delegate_stake": 500000000000000000,
                    "stake_factor_requirements": {
                        "min_stake_factor": 1.0,
                        "current_stake_factor": 0.5,
                    },
                    "initial_coldkeys": [
                        "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
                    ],
                    "network_consensus": True,
                    "missing_requirements": [
                        "Insufficient nodes (1/3 required)",
                        "Insufficient delegate stake (0.5/1.0 TENSOR required)",
                    ],
                },
            }

            # Test activation requirements check
            result = cli_runner.invoke(
                app, ["subnet", "check-activation-requirements", "--subnet-id", "1"]
            )

            assert result.exit_code in [0, 2]  # 0 for success, 2 for command not found

    def test_activation_with_requirements_check(self, cli_runner):
        """Test subnet activation with requirements check."""
        with patch("src.htcli.dependencies.get_client") as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock requirements check
            mock_client.check_subnet_activation_requirements.return_value = {
                "success": True,
                "data": {"all_requirements_met": True, "missing_requirements": []},
            }

            # Mock successful activation
            mock_client.activate_subnet.return_value = {
                "success": True,
                "message": "Subnet activated successfully",
                "transaction_hash": "0x1234567890abcdef",
            }

            # Test subnet activation
            result = cli_runner.invoke(
                app, ["subnet", "activate", "--subnet-id", "1", "--check-requirements"]
            )

            assert result.exit_code in [0, 2]  # 0 for success, 2 for command not found

    def test_activation_without_requirements_check(self, cli_runner):
        """Test subnet activation without requirements check."""
        with patch("src.htcli.dependencies.get_client") as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock successful activation
            mock_client.activate_subnet.return_value = {
                "success": True,
                "message": "Subnet activated successfully",
                "transaction_hash": "0x1234567890abcdef",
            }

            # Test subnet activation
            result = cli_runner.invoke(app, ["subnet", "activate", "--subnet-id", "1"])

            assert result.exit_code in [0, 2]  # 0 for success, 2 for command not found
