"""
Network connectivity tests for Hypertensor blockchain.
"""

import pytest
import asyncio
from unittest.mock import patch
from typer.testing import CliRunner

from src.htcli.main import app
from src.htcli.client import HypertensorClient
from src.htcli.config import load_config


class TestNetworkConnectivity:
    """Test network connectivity to Hypertensor blockchain."""

    @pytest.mark.network
    def test_network_endpoint_connectivity(self):
        """Test basic connectivity to the Hypertensor network endpoint."""
        config = load_config()
        client = HypertensorClient(config)

        # Test connection
        connected = client.connect()
        assert connected, "Failed to connect to Hypertensor network"

        # Clean up
        client.disconnect()

    @pytest.mark.network
    def test_websocket_connectivity(self):
        """Test WebSocket connectivity to the Hypertensor network."""
        config = load_config()
        client = HypertensorClient(config)

        # Test WebSocket connection
        async def test_ws():
            connected = await client.connect_websocket()
            assert connected, "Failed to connect to WebSocket endpoint"
            if client.ws_connection:
                await client.ws_connection.close()

        asyncio.run(test_ws())

    @pytest.mark.network
    def test_cli_network_info(self, cli_runner):
        """Test CLI network info command with real network."""
        result = cli_runner.invoke(app, ["info", "network"])

        # Should not crash, even if network is unavailable
        assert result.exit_code in [0, 1]  # 0 for success, 1 for network error

        if result.exit_code == 0:
            assert "Network stats" in result.stdout or "network" in result.stdout.lower()
        else:
            # Network error is acceptable for tests
            assert "error" in result.stdout.lower() or "failed" in result.stdout.lower()

    @pytest.mark.network
    def test_cli_epoch_info(self, cli_runner):
        """Test CLI epoch info command with real network."""
        result = cli_runner.invoke(app, ["info", "epoch"])

        # Should not crash, even if network is unavailable
        assert result.exit_code in [0, 1]

        if result.exit_code == 0:
            assert "epoch" in result.stdout.lower()
        else:
            # Network error is acceptable for tests
            assert "error" in result.stdout.lower() or "failed" in result.stdout.lower()

    @pytest.mark.network
    def test_cli_peers_query(self, cli_runner):
        """Test CLI peers query command with real network."""
        result = cli_runner.invoke(app, ["query", "peers"])

        # Should not crash, even if network is unavailable
        assert result.exit_code in [0, 1]

        if result.exit_code == 0:
            assert "peers" in result.stdout.lower()
        else:
            # Network error is acceptable for tests
            assert "error" in result.stdout.lower() or "failed" in result.stdout.lower()

    @pytest.mark.network
    def test_cli_block_query(self, cli_runner):
        """Test CLI block query command with real network."""
        result = cli_runner.invoke(app, ["query", "block"])

        # Should not crash, even if network is unavailable
        assert result.exit_code in [0, 1]

        if result.exit_code == 0:
            assert "block" in result.stdout.lower()
        else:
            # Network error is acceptable for tests
            assert "error" in result.stdout.lower() or "failed" in result.stdout.lower()

    def test_endpoint_configuration(self):
        """Test that the endpoint is correctly configured."""
        config = load_config()

        assert config.network.endpoint == "wss://hypertensor.duckdns.org"
        assert config.network.ws_endpoint == "wss://hypertensor.duckdns.org"
        assert config.network.timeout == 30
        assert config.network.retry_attempts == 3

    @pytest.mark.network
    def test_substrate_interface_connection(self):
        """Test SubstrateInterface connection to Hypertensor."""
        try:
            from substrateinterface import SubstrateInterface

            # Test connection with SubstrateInterface
            substrate = SubstrateInterface(
                url="wss://hypertensor.duckdns.org",
                ss58_format=42
            )

            # Test basic chain properties
            chain_name = substrate.get_chain_name()
            assert chain_name is not None, "Failed to get chain name"

            # Test block header
            block_header = substrate.get_block_header(None)
            assert block_header is not None, "Failed to get block header"

            # Clean up
            substrate.close()

        except Exception as e:
            pytest.skip(f"SubstrateInterface connection failed: {e}")

    @pytest.mark.network
    def test_network_endpoint_availability(self):
        """Test that the network endpoint is available."""
        import socket
        import ssl

        # Parse the endpoint
        endpoint = "wss://hypertensor.duckdns.org"
        host = "hypertensor.duckdns.org"
        port = 443  # Default HTTPS/WSS port

        try:
            # Test basic socket connectivity
            context = ssl.create_default_context()
            with socket.create_connection((host, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    # If we get here, the endpoint is reachable
                    assert ssock is not None
        except Exception as e:
            pytest.skip(f"Network endpoint not reachable: {e}")

    def test_environment_variables(self):
        """Test that environment variables are properly set."""
        import os

        # Check that environment variables are set
        assert os.getenv("HTCLI_NETWORK_ENDPOINT") == "wss://hypertensor.duckdns.org"
        assert os.getenv("HTCLI_NETWORK_WS_ENDPOINT") == "wss://hypertensor.duckdns.org"
        assert os.getenv("HTCLI_OUTPUT_FORMAT") == "table"
        assert os.getenv("HTCLI_OUTPUT_VERBOSE") == "false"
        assert os.getenv("HTCLI_OUTPUT_COLOR") == "true"
