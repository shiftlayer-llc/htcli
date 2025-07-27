"""
Unit tests for chain information commands (Fixed Version).
"""

import pytest
from unittest.mock import Mock, patch
from typer.testing import CliRunner

from src.htcli.commands.chain.info import app


class TestChainInfoFixed:
    """Test chain information commands with correct implementation."""

    def test_network_stats_success(self, cli_runner, mock_client):
        """Test successful network stats retrieval."""
        with patch('src.htcli.commands.chain.info.get_client', return_value=mock_client):
            # Mock successful network stats with proper response object
            from src.htcli.models.responses import NetworkStatsResponse
            mock_response = NetworkStatsResponse(
                success=True,
                message="Network stats retrieved successfully",
                data={
                    "total_subnets": 10,
                    "active_subnets": 8,
                    "total_nodes": 150,
                    "total_stake": 5000000000000,
                    "current_epoch": 1234,
                    "block_height": 567890
                }
            )
            mock_client.get_network_stats.return_value = mock_response

            result = cli_runner.invoke(app, ["network"])

            assert result.exit_code == 0
            assert "Network Statistics" in result.stdout

    def test_account_info_success(self, cli_runner, mock_client):
        """Test successful account info retrieval."""
        with patch('src.htcli.commands.chain.info.get_client', return_value=mock_client):
            # Mock successful account info with proper response object
            from src.htcli.models.responses import AccountInfoResponse
            mock_response = AccountInfoResponse(
                success=True,
                message="Account info retrieved successfully",
                data={
                    "address": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                    "balance": 1000000000000,
                    "nonce": 0,
                    "free": 1000000000000,
                    "reserved": 0,
                    "misc_frozen": 0,
                    "fee_frozen": 0
                }
            )
            mock_client.get_account_info.return_value = mock_response

            result = cli_runner.invoke(app, [
                "account", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])

            assert result.exit_code == 0
            assert "Account Information" in result.stdout

    def test_account_info_invalid_address(self, cli_runner, mock_client):
        """Test account info with invalid address."""
        with patch('src.htcli.commands.chain.info.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, ["account", "invalid-address"])

            assert result.exit_code != 0
            # The command will fail due to invalid address format
            assert result.exit_code != 0

    def test_epoch_info_success(self, cli_runner, mock_client):
        """Test successful epoch info retrieval."""
        with patch('src.htcli.commands.chain.info.get_client', return_value=mock_client):
            # Mock successful epoch info with proper response object
            from src.htcli.models.responses import EpochInfoResponse
            mock_response = EpochInfoResponse(
                success=True,
                message="Epoch info retrieved successfully",
                data={
                    "current_epoch": 1234,
                    "epoch_length": 1000,
                    "epoch_start": 1234000,
                    "epoch_end": 1235000
                }
            )
            mock_client.get_current_epoch.return_value = mock_response

            result = cli_runner.invoke(app, ["epoch"])

            assert result.exit_code == 0
            assert "Epoch Information" in result.stdout

    def test_network_help_output(self, cli_runner):
        """Test help output for network command."""
        result = cli_runner.invoke(app, ["network", "--help"])
        assert result.exit_code == 0

    def test_account_help_output(self, cli_runner):
        """Test help output for account command."""
        result = cli_runner.invoke(app, ["account", "--help"])
        assert result.exit_code == 0
        assert "ADDRESS" in result.stdout

    def test_epoch_help_output(self, cli_runner):
        """Test help output for epoch command."""
        result = cli_runner.invoke(app, ["epoch", "--help"])
        assert result.exit_code == 0

    def test_help_output(self, cli_runner):
        """Test help output for info commands."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "network" in result.stdout
        assert "account" in result.stdout
        assert "epoch" in result.stdout
