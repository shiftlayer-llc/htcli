"""
Unit tests for chain query commands (Fixed Version).
"""

import pytest
from unittest.mock import Mock, patch
from typer.testing import CliRunner

from src.htcli.commands.chain.query import app


class TestChainQueryFixed:
    """Test chain query commands with correct implementation."""

    def test_balance_success(self, cli_runner, mock_client):
        """Test successful balance retrieval."""
        with patch('src.htcli.commands.chain.query.get_client', return_value=mock_client):
            # Mock successful balance retrieval with proper response object
            from src.htcli.models.responses import BalanceResponse
            mock_response = BalanceResponse(
                success=True,
                message="Balance retrieved successfully",
                data={
                    "address": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                    "balance": 1000000000000,
                    "free": 1000000000000,
                    "reserved": 0,
                    "misc_frozen": 0,
                    "fee_frozen": 0
                }
            )
            mock_client.get_balance.return_value = mock_response

            result = cli_runner.invoke(app, [
                "balance", "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            ])

            assert result.exit_code == 0

    def test_balance_invalid_address(self, cli_runner, mock_client):
        """Test balance retrieval with invalid address."""
        with patch('src.htcli.commands.chain.query.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, ["balance", "invalid-address"])

            assert result.exit_code != 0

    def test_peers_success(self, cli_runner, mock_client):
        """Test successful peers retrieval."""
        with patch('src.htcli.commands.chain.query.get_client', return_value=mock_client):
            # Mock successful peers retrieval with proper response object
            from src.htcli.models.responses import PeersResponse
            mock_response = PeersResponse(
                success=True,
                message="Peers retrieved successfully",
                data={
                    "peers": [
                        {"peer_id": "QmPeer1", "address": "127.0.0.1:30333"},
                        {"peer_id": "QmPeer2", "address": "127.0.0.2:30333"}
                    ],
                    "total_peers": 2
                }
            )
            mock_client.get_peers.return_value = mock_response

            result = cli_runner.invoke(app, ["peers"])

            assert result.exit_code == 0

    def test_block_info_success(self, cli_runner, mock_client):
        """Test successful block info retrieval."""
        with patch('src.htcli.commands.chain.query.get_client', return_value=mock_client):
            # Mock successful block info retrieval with proper response object
            from src.htcli.models.responses import BlockInfoResponse
            mock_response = BlockInfoResponse(
                success=True,
                message="Block info retrieved successfully",
                data={
                    "block_number": 12345,
                    "block_hash": "0x1234567890abcdef",
                    "parent_hash": "0xabcdef1234567890",
                    "timestamp": 1640995200,
                    "extrinsics": 10,
                    "events": 25
                }
            )
            mock_client.get_block_info.return_value = mock_response

            result = cli_runner.invoke(app, ["block", "12345"])

            assert result.exit_code == 0

    def test_block_info_latest(self, cli_runner, mock_client):
        """Test latest block info retrieval."""
        with patch('src.htcli.commands.chain.query.get_client', return_value=mock_client):
            # Mock successful latest block info retrieval
            from src.htcli.models.responses import BlockInfoResponse
            mock_response = BlockInfoResponse(
                success=True,
                message="Latest block info retrieved successfully",
                data={
                    "block_number": 56789,
                    "block_hash": "0xabcdef1234567890",
                    "parent_hash": "0x1234567890abcdef",
                    "timestamp": 1640995200,
                    "extrinsics": 15,
                    "events": 30
                }
            )
            mock_client.get_block_info.return_value = mock_response

            result = cli_runner.invoke(app, ["block"])

            assert result.exit_code == 0

    def test_block_info_invalid_number(self, cli_runner, mock_client):
        """Test block info with invalid block number."""
        with patch('src.htcli.commands.chain.query.get_client', return_value=mock_client):
            result = cli_runner.invoke(app, ["block", "invalid"])

            assert result.exit_code != 0
            # Typer will handle validation
            assert result.exit_code != 0

    def test_balance_help_output(self, cli_runner):
        """Test help output for balance command."""
        result = cli_runner.invoke(app, ["balance", "--help"])
        assert result.exit_code == 0
        assert "ADDRESS" in result.stdout

    def test_peers_help_output(self, cli_runner):
        """Test help output for peers command."""
        result = cli_runner.invoke(app, ["peers", "--help"])
        assert result.exit_code == 0

    def test_block_help_output(self, cli_runner):
        """Test help output for block command."""
        result = cli_runner.invoke(app, ["block", "--help"])
        assert result.exit_code == 0
        assert "BLOCK_NUMBER" in result.stdout

    def test_help_output(self, cli_runner):
        """Test help output for query commands."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "balance" in result.stdout
        assert "peers" in result.stdout
        assert "block" in result.stdout
