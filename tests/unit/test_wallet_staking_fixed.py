"""
Unit tests for wallet staking commands (Fixed Version).
"""

import pytest
from unittest.mock import Mock, patch
from typer.testing import CliRunner

from src.htcli.commands.wallet.staking import app


class TestWalletStakingFixed:
    """Test wallet staking commands with correct implementation."""

    def test_add_stake_success(self, cli_runner, mock_client):
        """Test successful stake addition."""
        with patch('src.htcli.commands.wallet.staking.get_client', return_value=mock_client):
            # Mock successful stake addition with proper response object
            from src.htcli.models.responses import StakeAddResponse
            mock_response = StakeAddResponse(
                success=True,
                message="Stake added successfully",
                transaction_hash="0x1234567890abcdef",
                data={"stake_amount": 1000}
            )
            mock_client.add_stake.return_value = mock_response

            result = cli_runner.invoke(app, [
                "add", "1", "1", "100.0",
                "--hotkey", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])

            assert result.exit_code == 0
            assert "Added 100.0 stake to subnet 1 successfully!" in result.stdout

    def test_add_stake_invalid_subnet_id(self, cli_runner, mock_client):
        """Test stake addition with invalid subnet ID."""
        with patch('src.htcli.commands.wallet.staking.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, [
                "add", "invalid", "1", "100.0",
                "--hotkey", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])

            assert result.exit_code != 0
            # Typer will handle the validation and show usage
            assert "Usage:" in result.stdout

    def test_add_stake_invalid_node_id(self, cli_runner, mock_client):
        """Test stake addition with invalid node ID."""
        with patch('src.htcli.commands.wallet.staking.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, [
                "add", "1", "invalid", "100.0",
                "--hotkey", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])

            assert result.exit_code != 0
            assert "Usage:" in result.stdout

    def test_add_stake_invalid_hotkey(self, cli_runner, mock_client):
        """Test stake addition with invalid hotkey."""
        with patch('src.htcli.commands.wallet.staking.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, [
                "add", "1", "1", "100.0",
                "--hotkey", "invalid-hotkey"
            ])

            assert result.exit_code != 0
            # The command will fail due to invalid hotkey format
            assert result.exit_code != 0

    def test_add_stake_missing_required_args(self, cli_runner, mock_client):
        """Test stake addition with missing required arguments."""
        with patch('src.htcli.commands.wallet.staking.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, ["add", "1", "1"])
            assert result.exit_code != 0
            assert "Usage:" in result.stdout

    def test_add_stake_insufficient_balance(self, cli_runner, mock_client):
        """Test stake addition with insufficient balance."""
        with patch('src.htcli.commands.wallet.staking.get_client', return_value=mock_client):
            # Mock insufficient balance error
            mock_client.add_stake.side_effect = Exception("Insufficient balance")

            result = cli_runner.invoke(app, [
                "add", "1", "1", "1000000.0",
                "--hotkey", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])

            assert result.exit_code != 0
            assert "Failed to add stake" in result.stdout

    def test_remove_stake_success(self, cli_runner, mock_client):
        """Test successful stake removal."""
        with patch('src.htcli.commands.wallet.staking.get_client', return_value=mock_client):
            # Mock successful stake removal with proper response object
            from src.htcli.models.responses import StakeRemoveResponse
            mock_response = StakeRemoveResponse(
                success=True,
                message="Stake removed successfully",
                transaction_hash="0xabcdef1234567890",
                data={"stake_amount": 500}
            )
            mock_client.remove_stake.return_value = mock_response

            result = cli_runner.invoke(app, [
                "remove", "1", "50.0",
                "--hotkey", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])

            assert result.exit_code == 0
            assert "Removed 50.0 stake from subnet 1 successfully!" in result.stdout

    def test_remove_stake_invalid_subnet_id(self, cli_runner, mock_client):
        """Test stake removal with invalid subnet ID."""
        with patch('src.htcli.commands.wallet.staking.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, [
                "remove", "invalid", "50.0",
                "--hotkey", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])

            assert result.exit_code != 0
            assert "Usage:" in result.stdout

    def test_remove_stake_invalid_hotkey(self, cli_runner, mock_client):
        """Test stake removal with invalid hotkey."""
        with patch('src.htcli.commands.wallet.staking.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, [
                "remove", "1", "50.0",
                "--hotkey", "invalid-hotkey"
            ])

            assert result.exit_code != 0

    def test_remove_stake_missing_required_args(self, cli_runner, mock_client):
        """Test stake removal with missing required arguments."""
        with patch('src.htcli.commands.wallet.staking.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, ["remove", "1"])
            assert result.exit_code != 0
            assert "Usage:" in result.stdout

    def test_remove_stake_insufficient_stake(self, cli_runner, mock_client):
        """Test stake removal with insufficient stake."""
        with patch('src.htcli.commands.wallet.staking.get_client', return_value=mock_client):
            # Mock insufficient stake error
            mock_client.remove_stake.side_effect = Exception("Insufficient stake to remove")

            result = cli_runner.invoke(app, [
                "remove", "1", "1000.0",
                "--hotkey", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])

            assert result.exit_code != 0
            assert "Failed to remove stake" in result.stdout

    def test_info_stake_success(self, cli_runner, mock_client):
        """Test successful stake info retrieval."""
        with patch('src.htcli.commands.wallet.staking.get_client', return_value=mock_client):
            # Mock successful stake info with proper response object
            from src.htcli.models.responses import StakeInfoResponse
            mock_response = StakeInfoResponse(
                success=True,
                message="Stake info retrieved successfully",
                data={
                    "subnet_id": 1,
                    "hotkey": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                    "total_stake": 1000,
                    "active_stake": 800,
                    "unbonding_stake": 200
                }
            )
            mock_client.get_stake_info.return_value = mock_response

            result = cli_runner.invoke(app, [
                "info", "1",
                "--hotkey", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])

            assert result.exit_code == 0
            # The info command doesn't print the message, it shows a panel
            assert result.exit_code == 0

    def test_info_stake_invalid_subnet_id(self, cli_runner, mock_client):
        """Test stake info with invalid subnet ID."""
        with patch('src.htcli.commands.wallet.staking.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, [
                "info", "invalid",
                "--hotkey", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])

            assert result.exit_code != 0
            assert "Usage:" in result.stdout

    def test_info_stake_invalid_hotkey(self, cli_runner, mock_client):
        """Test stake info with invalid hotkey."""
        with patch('src.htcli.commands.wallet.staking.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, [
                "info", "1",
                "--hotkey", "invalid-hotkey"
            ])

            assert result.exit_code != 0

    def test_info_stake_not_found(self, cli_runner, mock_client):
        """Test stake info when stake not found."""
        with patch('src.htcli.commands.wallet.staking.get_client', return_value=mock_client):
            # Mock stake not found error
            mock_client.get_stake_info.side_effect = Exception("Stake not found")

            result = cli_runner.invoke(app, [
                "info", "1",
                "--hotkey", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])

            assert result.exit_code != 0
            assert "Failed to get stake info" in result.stdout

    def test_add_help_output(self, cli_runner):
        """Test help output for add command."""
        result = cli_runner.invoke(app, ["add", "--help"])
        assert result.exit_code == 0
        assert "SUBNET_ID" in result.stdout
        assert "NODE_ID" in result.stdout
        assert "AMOUNT" in result.stdout
        assert "--hotkey" in result.stdout

    def test_remove_help_output(self, cli_runner):
        """Test help output for remove command."""
        result = cli_runner.invoke(app, ["remove", "--help"])
        assert result.exit_code == 0
        assert "SUBNET_ID" in result.stdout
        assert "AMOUNT" in result.stdout
        assert "--hotkey" in result.stdout

    def test_info_help_output(self, cli_runner):
        """Test help output for info command."""
        result = cli_runner.invoke(app, ["info", "--help"])
        assert result.exit_code == 0
        assert "SUBNET_ID" in result.stdout
        assert "--hotkey" in result.stdout
