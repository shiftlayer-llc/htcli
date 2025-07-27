"""
Unit tests for subnet node operations (Fixed Version).
"""

import pytest
from unittest.mock import Mock, patch
from typer.testing import CliRunner

from src.htcli.commands.subnet.nodes import app


class TestSubnetNodesFixed:
    """Test subnet node operations with correct implementation."""

    def test_add_node_success(self, cli_runner, mock_client):
        """Test successful node addition."""
        with patch('src.htcli.commands.subnet.nodes.get_client', return_value=mock_client):
            # Mock successful node addition with proper response object
            from src.htcli.models.responses import NodeAddResponse
            mock_response = NodeAddResponse(
                success=True,
                message="Node added successfully",
                transaction_hash="0x1234567890abcdef",
                data={"node_id": 1}
            )
            mock_client.add_subnet_node.return_value = mock_response

            result = cli_runner.invoke(app, [
                "add", "1", "QmYyQSo1c1Ym7orWxLYvCrM2EmxFTkfDDo5MKKsFYUdBkX",
                "--hotkey", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])

            assert result.exit_code == 0

    def test_add_node_invalid_subnet_id(self, cli_runner, mock_client):
        """Test node addition with invalid subnet ID."""
        with patch('src.htcli.commands.subnet.nodes.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, [
                "add", "invalid", "QmYyQSo1c1Ym7orWxLYvCrM2EmxFTkfDDo5MKKsFYUdBkX",
                "--hotkey", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])

            assert result.exit_code != 0
            # Typer will handle validation
            assert result.exit_code != 0

    def test_add_node_invalid_peer_id(self, cli_runner, mock_client):
        """Test node addition with invalid peer ID."""
        with patch('src.htcli.commands.subnet.nodes.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, [
                "add", "1", "invalid-peer-id",
                "--hotkey", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])

            assert result.exit_code != 0

    def test_add_node_invalid_hotkey(self, cli_runner, mock_client):
        """Test node addition with invalid hotkey."""
        with patch('src.htcli.commands.subnet.nodes.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, [
                "add", "1", "QmYyQSo1c1Ym7orWxLYvCrM2EmxFTkfDDo5MKKsFYUdBkX",
                "--hotkey", "invalid-hotkey"
            ])

            assert result.exit_code != 0

    def test_add_node_subnet_not_found(self, cli_runner, mock_client):
        """Test node addition when subnet not found."""
        with patch('src.htcli.commands.subnet.nodes.get_client', return_value=mock_client):
            # Mock subnet not found error
            mock_client.add_subnet_node.side_effect = Exception("Subnet not found")

            result = cli_runner.invoke(app, [
                "add", "999", "QmYyQSo1c1Ym7orWxLYvCrM2EmxFTkfDDo5MKKsFYUdBkX",
                "--hotkey", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])

            assert result.exit_code != 0
            assert "Failed to add node" in result.stdout

    def test_add_node_already_exists(self, cli_runner, mock_client):
        """Test node addition when node already exists."""
        with patch('src.htcli.commands.subnet.nodes.get_client', return_value=mock_client):
            # Mock node already exists error
            mock_client.add_subnet_node.side_effect = Exception("Node already exists")

            result = cli_runner.invoke(app, [
                "add", "1", "QmYyQSo1c1Ym7orWxLYvCrM2EmxFTkfDDo5MKKsFYUdBkX",
                "--hotkey", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])

            assert result.exit_code != 0
            assert "Failed to add node" in result.stdout

    def test_list_nodes_success(self, cli_runner, mock_client, sample_subnet_data):
        """Test successful node listing."""
        with patch('src.htcli.commands.subnet.nodes.get_client', return_value=mock_client):
            # Mock successful node listing with proper response object
            from src.htcli.models.responses import NodeListResponse
            mock_response = NodeListResponse(
                success=True,
                message="Nodes retrieved successfully",
                data={"nodes": sample_subnet_data["nodes"]}
            )
            mock_client.get_subnet_nodes.return_value = mock_response

            result = cli_runner.invoke(app, ["list", "1"])

            assert result.exit_code == 0

    def test_list_nodes_invalid_subnet_id(self, cli_runner, mock_client):
        """Test node listing with invalid subnet ID."""
        with patch('src.htcli.commands.subnet.nodes.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, ["list", "invalid"])

            assert result.exit_code != 0
            # Typer will handle validation
            assert result.exit_code != 0

    def test_list_nodes_empty(self, cli_runner, mock_client):
        """Test node listing when no nodes exist."""
        with patch('src.htcli.commands.subnet.nodes.get_client', return_value=mock_client):
            # Mock empty node listing
            from src.htcli.models.responses import NodeListResponse
            mock_response = NodeListResponse(
                success=True,
                message="No nodes found",
                data={"nodes": []}
            )
            mock_client.get_subnet_nodes.return_value = mock_response

            result = cli_runner.invoke(app, ["list", "1"])

            assert result.exit_code == 0

    def test_add_help_output(self, cli_runner):
        """Test help output for add command."""
        result = cli_runner.invoke(app, ["add", "--help"])
        assert result.exit_code == 0
        assert "SUBNET_ID" in result.stdout
        assert "PEER_ID" in result.stdout

    def test_list_help_output(self, cli_runner):
        """Test help output for list command."""
        result = cli_runner.invoke(app, ["list", "--help"])
        assert result.exit_code == 0
        assert "SUBNET_ID" in result.stdout

    def test_help_output(self, cli_runner):
        """Test help output for nodes commands."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "add" in result.stdout
        assert "list" in result.stdout
