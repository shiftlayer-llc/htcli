"""
Integration tests for the htcli application.
"""

import pytest
import os
from typer.testing import CliRunner
from unittest.mock import patch

from src.htcli.main import app


class TestCLIIntegration:
    """Integration tests for the CLI application."""

    def test_main_help_output(self, cli_runner):
        """Test main CLI help output."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Hypertensor Blockchain CLI" in result.stdout
        assert "register" in result.stdout
        assert "manage" in result.stdout
        assert "nodes" in result.stdout
        assert "keys" in result.stdout
        assert "stake" in result.stdout
        assert "info" in result.stdout
        assert "query" in result.stdout

    def test_subnet_help_output(self, cli_runner):
        """Test subnet command help output."""
        result = cli_runner.invoke(app, ["register", "--help"])
        assert result.exit_code == 0
        assert "create" in result.stdout
        assert "activate" in result.stdout

        result = cli_runner.invoke(app, ["manage", "--help"])
        assert result.exit_code == 0
        assert "list" in result.stdout
        assert "info" in result.stdout

        result = cli_runner.invoke(app, ["nodes", "--help"])
        assert result.exit_code == 0
        assert "add" in result.stdout
        assert "list" in result.stdout

    def test_wallet_help_output(self, cli_runner):
        """Test wallet command help output."""
        result = cli_runner.invoke(app, ["keys", "--help"])
        assert result.exit_code == 0
        assert "generate" in result.stdout
        assert "list" in result.stdout
        assert "import-key" in result.stdout
        assert "delete" in result.stdout

        result = cli_runner.invoke(app, ["stake", "--help"])
        assert result.exit_code == 0
        assert "add" in result.stdout
        assert "remove" in result.stdout
        assert "info" in result.stdout

    def test_chain_help_output(self, cli_runner):
        """Test chain command help output."""
        result = cli_runner.invoke(app, ["info", "--help"])
        assert result.exit_code == 0
        assert "network" in result.stdout
        assert "account" in result.stdout
        assert "epoch" in result.stdout

        result = cli_runner.invoke(app, ["query", "--help"])
        assert result.exit_code == 0
        assert "balance" in result.stdout
        assert "peers" in result.stdout
        assert "block" in result.stdout

    def test_configuration_options(self, cli_runner):
        """Test CLI configuration options."""
        result = cli_runner.invoke(app, [
            "--config", "/path/to/config.yaml",
            "--endpoint", "ws://custom.endpoint:9944",
            "--verbose",
            "--format", "json",
            "--help"
        ])
        assert result.exit_code == 0

    def test_invalid_command(self, cli_runner):
        """Test invalid command handling."""
        result = cli_runner.invoke(app, ["invalid-command"])
        assert result.exit_code != 0

    def test_invalid_option(self, cli_runner):
        """Test invalid option handling."""
        result = cli_runner.invoke(app, ["--invalid-option"])
        assert result.exit_code != 0

    @pytest.mark.integration
    def test_end_to_end_subnet_workflow(self, cli_runner):
        """Test end-to-end subnet workflow."""
        with patch('src.htcli.dependencies.get_client') as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock successful subnet creation
            mock_client.register_subnet.return_value = {
                "success": True,
                "message": "Subnet registered successfully",
                "transaction_hash": "0x1234567890abcdef",
                "data": {"subnet_id": 1}
            }

            # Test subnet creation
            result = cli_runner.invoke(app, [
                "register", "create", "test-subnet",
                "--memory", "1024",
                "--blocks", "1000",
                "--interval", "100"
            ])
            assert result.exit_code == 0
            assert "Subnet registered successfully" in result.stdout

            # Mock successful subnet activation
            mock_client.activate_subnet.return_value = {
                "success": True,
                "message": "Subnet activated successfully",
                "transaction_hash": "0xabcdef1234567890"
            }

            # Test subnet activation
            result = cli_runner.invoke(app, ["register", "activate", "1"])
            assert result.exit_code == 0
            assert "Subnet activated successfully" in result.stdout

    @pytest.mark.integration
    def test_end_to_end_wallet_workflow(self, cli_runner, test_wallet_dir):
        """Test end-to-end wallet workflow."""
        with patch('src.htcli.commands.wallet.keys.get_wallet_path', return_value=test_wallet_dir):
            # Test key generation
            result = cli_runner.invoke(app, [
                "keys", "generate", "test-key",
                "--type", "sr25519"
            ])
            assert result.exit_code == 0
            assert "Key generated successfully" in result.stdout

            # Test key listing
            result = cli_runner.invoke(app, ["keys", "list"])
            assert result.exit_code == 0
            assert "test-key" in result.stdout

            # Test key deletion
            result = cli_runner.invoke(app, ["keys", "delete", "test-key"])
            assert result.exit_code == 0
            assert "Key deleted successfully" in result.stdout

    @pytest.mark.integration
    def test_end_to_end_chain_workflow(self, cli_runner):
        """Test end-to-end chain workflow."""
        with patch('src.htcli.dependencies.get_client') as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock network stats
            mock_client.get_network_stats.return_value = {
                "success": True,
                "message": "Network stats retrieved successfully",
                "data": {
                    "total_subnets": 10,
                    "active_subnets": 8,
                    "total_nodes": 150
                }
            }

            # Test network info
            result = cli_runner.invoke(app, ["info", "network"])
            assert result.exit_code == 0
            assert "Network stats retrieved successfully" in result.stdout

            # Mock balance query
            mock_client.get_balance.return_value = {
                "success": True,
                "message": "Balance retrieved successfully",
                "data": {
                    "address": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                    "balance": 1000000000000
                }
            }

            # Test balance query
            result = cli_runner.invoke(app, [
                "query", "balance", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])
            assert result.exit_code == 0
            assert "Balance retrieved successfully" in result.stdout
