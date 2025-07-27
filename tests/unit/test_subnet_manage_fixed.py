"""
Unit tests for subnet management commands (Fixed Version).
"""

import pytest
from unittest.mock import Mock, patch
from typer.testing import CliRunner

from src.htcli.commands.subnet.manage import app


class TestSubnetManageFixed:
    """Test subnet management commands with correct implementation."""

    def test_list_subnets_success(self, cli_runner, mock_client, sample_subnet_data):
        """Test successful subnet listing."""
        with patch('src.htcli.commands.subnet.manage.get_client', return_value=mock_client):
            # Mock successful listing with proper response object
            from src.htcli.models.responses import SubnetListResponse
            mock_response = SubnetListResponse(
                success=True,
                message="Subnets retrieved successfully",
                data={"subnets": [sample_subnet_data]}
            )
            mock_client.list_subnets.return_value = mock_response

            result = cli_runner.invoke(app, ["list"])

            assert result.exit_code == 0

    def test_list_subnets_active_only(self, cli_runner, mock_client, sample_subnet_data):
        """Test subnet listing with active only filter."""
        with patch('src.htcli.commands.subnet.manage.get_client', return_value=mock_client):
            # Mock successful listing with active filter
            from src.htcli.models.responses import SubnetListResponse
            mock_response = SubnetListResponse(
                success=True,
                message="Active subnets retrieved successfully",
                data={"subnets": [sample_subnet_data]}
            )
            mock_client.list_subnets.return_value = mock_response

            result = cli_runner.invoke(app, ["list", "--active"])

            assert result.exit_code == 0

    def test_list_subnets_empty(self, cli_runner, mock_client):
        """Test subnet listing when no subnets exist."""
        with patch('src.htcli.commands.subnet.manage.get_client', return_value=mock_client):
            # Mock empty listing
            from src.htcli.models.responses import SubnetListResponse
            mock_response = SubnetListResponse(
                success=True,
                message="No subnets found",
                data={"subnets": []}
            )
            mock_client.list_subnets.return_value = mock_response

            result = cli_runner.invoke(app, ["list"])

            assert result.exit_code == 0

    def test_list_subnets_error(self, cli_runner, mock_client):
        """Test subnet listing with error."""
        with patch('src.htcli.commands.subnet.manage.get_client', return_value=mock_client):
            # Mock error
            mock_client.list_subnets.side_effect = Exception("Network error")

            result = cli_runner.invoke(app, ["list"])

            assert result.exit_code != 0
            assert "Failed to list subnets" in result.stdout

    def test_info_subnet_success(self, cli_runner, mock_client, sample_subnet_data):
        """Test successful subnet info retrieval."""
        with patch('src.htcli.commands.subnet.manage.get_client', return_value=mock_client):
            # Mock successful info retrieval
            from src.htcli.models.responses import SubnetInfoResponse
            mock_response = SubnetInfoResponse(
                success=True,
                message="Subnet info retrieved successfully",
                data=sample_subnet_data
            )
            mock_client.get_subnet_info.return_value = mock_response

            result = cli_runner.invoke(app, ["info", "1"])

            assert result.exit_code == 0

    def test_info_subnet_invalid_id(self, cli_runner, mock_client):
        """Test subnet info with invalid subnet ID."""
        with patch('src.htcli.commands.subnet.manage.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, ["info", "invalid"])

            assert result.exit_code != 0
            # Typer will handle validation
            assert result.exit_code != 0

    def test_info_subnet_not_found(self, cli_runner, mock_client):
        """Test subnet info when subnet doesn't exist."""
        with patch('src.htcli.commands.subnet.manage.get_client', return_value=mock_client):
            # Mock subnet not found error
            mock_client.get_subnet_info.side_effect = Exception("Subnet not found")

            result = cli_runner.invoke(app, ["info", "999"])

            assert result.exit_code != 0
            assert "Failed to get subnet info" in result.stdout

    def test_info_subnet_missing_id(self, cli_runner):
        """Test subnet info with missing subnet ID."""
        result = cli_runner.invoke(app, ["info"])
        assert result.exit_code != 0

    def test_help_output(self, cli_runner):
        """Test help output for manage commands."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "list" in result.stdout
        assert "info" in result.stdout

    def test_list_help_output(self, cli_runner):
        """Test help output for list command."""
        result = cli_runner.invoke(app, ["list", "--help"])
        assert result.exit_code == 0
        assert "--active" in result.stdout

    def test_info_help_output(self, cli_runner):
        """Test help output for info command."""
        result = cli_runner.invoke(app, ["info", "--help"])
        assert result.exit_code == 0
        assert "SUBNET_ID" in result.stdout
