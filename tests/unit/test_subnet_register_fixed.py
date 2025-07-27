"""
Unit tests for subnet registration commands (Fixed Version).
"""

import pytest
from unittest.mock import Mock, patch
from typer.testing import CliRunner

from src.htcli.commands.subnet.register import app


class TestSubnetRegisterFixed:
    """Test subnet registration commands with correct implementation."""

    def test_create_subnet_success(self, cli_runner, mock_client):
        """Test successful subnet creation."""
        with patch('src.htcli.commands.subnet.register.get_client', return_value=mock_client):
            # Mock successful registration with proper response object
            from src.htcli.models.responses import SubnetRegisterResponse
            mock_response = SubnetRegisterResponse(
                success=True,
                message="Subnet registered successfully",
                transaction_hash="0x1234567890abcdef",
                data={"subnet_id": 1}
            )
            mock_client.register_subnet.return_value = mock_response

            result = cli_runner.invoke(app, [
                "create", "test-subnet",
                "--memory", "1024",
                "--blocks", "1000",
                "--interval", "100"
            ])

            assert result.exit_code == 0
            assert "Subnet registered successfully" in result.stdout

    def test_create_subnet_invalid_memory(self, cli_runner, mock_client):
        """Test subnet creation with invalid memory."""
        with patch('src.htcli.commands.subnet.register.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, [
                "create", "test-subnet",
                "--memory", "0",  # Invalid memory
                "--blocks", "1000",
                "--interval", "100"
            ])

            assert result.exit_code != 0
            # Typer will handle validation and show usage
            assert result.exit_code != 0

    def test_create_subnet_invalid_blocks(self, cli_runner, mock_client):
        """Test subnet creation with invalid registration blocks."""
        with patch('src.htcli.commands.subnet.register.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, [
                "create", "test-subnet",
                "--memory", "1024",
                "--blocks", "0",  # Invalid blocks
                "--interval", "100"
            ])

            assert result.exit_code != 0

    def test_create_subnet_invalid_interval(self, cli_runner, mock_client):
        """Test subnet creation with invalid entry interval."""
        with patch('src.htcli.commands.subnet.register.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, [
                "create", "test-subnet",
                "--memory", "1024",
                "--blocks", "1000",
                "--interval", "0"  # Invalid interval
            ])

            assert result.exit_code != 0

    def test_create_subnet_missing_required_args(self, cli_runner):
        """Test subnet creation with missing required arguments."""
        result = cli_runner.invoke(app, ["create"])
        assert result.exit_code != 0

    def test_activate_subnet_success(self, cli_runner, mock_client):
        """Test successful subnet activation."""
        with patch('src.htcli.commands.subnet.register.get_client', return_value=mock_client):
            # Mock successful activation with proper response object
            from src.htcli.models.responses import SubnetRegisterResponse
            mock_response = SubnetRegisterResponse(
                success=True,
                message="Subnet activated successfully",
                transaction_hash="0xabcdef1234567890"
            )
            mock_client.activate_subnet.return_value = mock_response

            result = cli_runner.invoke(app, ["activate", "1"])

            assert result.exit_code == 0
            assert "Subnet 1 activated successfully!" in result.stdout

    def test_activate_subnet_invalid_id(self, cli_runner, mock_client):
        """Test subnet activation with invalid subnet ID."""
        with patch('src.htcli.commands.subnet.register.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, ["activate", "invalid"])

            assert result.exit_code != 0
            assert "Usage:" in result.stdout

    def test_activate_subnet_not_found(self, cli_runner, mock_client):
        """Test subnet activation when subnet doesn't exist."""
        with patch('src.htcli.commands.subnet.register.get_client', return_value=mock_client):
            # Mock subnet not found error
            mock_client.activate_subnet.side_effect = Exception("Subnet not found")

            result = cli_runner.invoke(app, ["activate", "999"])

            assert result.exit_code != 0
            assert "Failed to activate subnet" in result.stdout

    def test_activate_subnet_already_active(self, cli_runner, mock_client):
        """Test subnet activation when subnet is already active."""
        with patch('src.htcli.commands.subnet.register.get_client', return_value=mock_client):
            # Mock already active error
            mock_client.activate_subnet.side_effect = Exception("Subnet already active")

            result = cli_runner.invoke(app, ["activate", "1"])

            assert result.exit_code != 0
            assert "Failed to activate subnet" in result.stdout

    def test_help_output(self, cli_runner):
        """Test help output for register commands."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "create" in result.stdout
        assert "activate" in result.stdout

    def test_create_help_output(self, cli_runner):
        """Test help output for create command."""
        result = cli_runner.invoke(app, ["create", "--help"])
        assert result.exit_code == 0
        assert "PATH" in result.stdout
        assert "--memory" in result.stdout
        assert "--blocks" in result.stdout
        assert "--interval" in result.stdout

    def test_activate_help_output(self, cli_runner):
        """Test help output for activate command."""
        result = cli_runner.invoke(app, ["activate", "--help"])
        assert result.exit_code == 0
        assert "SUBNET_ID" in result.stdout
