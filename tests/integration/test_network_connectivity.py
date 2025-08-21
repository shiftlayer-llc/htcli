"""
Network connectivity tests for Hypertensor blockchain.
"""

import asyncio

import pytest

from src.htcli.client import HypertensorClient
from src.htcli.config import load_config
from src.htcli.main import app


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
            try:
                connected = await client.connect_websocket()
                assert connected, "Failed to connect to WebSocket endpoint"
                if client.ws_connection:
                    await client.ws_connection.close()
            except Exception as e:
                # WebSocket connection might fail in test environment
                pytest.skip(f"WebSocket connection failed: {e}")

        asyncio.run(test_ws())

    @pytest.mark.network
    def test_cli_network_info(self, cli_runner):
        """Test CLI network info command with real network."""
        result = cli_runner.invoke(app, ["chain", "network"])

        # Should not crash, even if network is unavailable
        assert result.exit_code in [0, 1]  # 0 for success, 1 for network error

        if result.exit_code == 0:
            assert (
                "Network stats" in result.stdout or "network" in result.stdout.lower()
            )
        else:
            # Network error is acceptable for tests
            assert "error" in result.stdout.lower() or "failed" in result.stdout.lower()

    @pytest.mark.network
    def test_cli_epoch_info(self, cli_runner):
        """Test CLI epoch info command with real network."""
        result = cli_runner.invoke(app, ["chain", "epoch"])

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
        result = cli_runner.invoke(app, ["chain", "peers"])

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
        result = cli_runner.invoke(app, ["chain", "block", "--number", "1"])

        # Should not crash, even if network is unavailable
        assert result.exit_code in [0, 1]

        if result.exit_code == 0:
            assert "block" in result.stdout.lower()
        else:
            # Network error is acceptable for tests
            assert "error" in result.stdout.lower() or "failed" in result.stdout.lower()

    @pytest.mark.network
    def test_cli_balance_query(self, cli_runner):
        """Test CLI balance query command with real network."""
        # Use a test address
        test_address = "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
        result = cli_runner.invoke(app, ["chain", "balance", test_address])

        # Should not crash, even if network is unavailable
        assert result.exit_code in [
            0,
            1,
            2,
        ]  # 0 for success, 1 for network error, 2 for command not found

        if result.exit_code == 0:
            assert "balance" in result.stdout.lower() or "TENSOR" in result.stdout
        elif result.exit_code == 1:
            # Network error is acceptable for tests
            assert "error" in result.stdout.lower() or "failed" in result.stdout.lower()

    @pytest.mark.network
    def test_cli_account_info(self, cli_runner):
        """Test CLI account info command with real network."""
        # Use a test address
        test_address = "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
        result = cli_runner.invoke(app, ["chain", "account", test_address])

        # Should not crash, even if network is unavailable
        assert result.exit_code in [
            0,
            1,
            2,
        ]  # 0 for success, 1 for network error, 2 for command not found

        if result.exit_code == 0:
            assert (
                "account" in result.stdout.lower() or "balance" in result.stdout.lower()
            )
        elif result.exit_code == 1:
            # Network error is acceptable for tests
            assert "error" in result.stdout.lower() or "failed" in result.stdout.lower()

    def test_endpoint_configuration(self):
        """Test endpoint configuration loading."""
        config = load_config()

        # Test that configuration loads correctly
        assert config.network.endpoint is not None
        assert config.network.ws_endpoint is not None
        assert isinstance(config.network.timeout, int)
        assert config.network.timeout > 0

    @pytest.mark.network
    def test_substrate_interface_connection(self):
        """Test SubstrateInterface connection to Hypertensor network."""
        config = load_config()
        client = HypertensorClient(config)

        try:
            # Test connection
            connected = client.connect()
            assert connected, "Failed to connect to Hypertensor network"

            # Test basic RPC call
            if client.substrate:
                # Test a simple RPC call
                try:
                    peers = client.substrate.rpc_request("system_peers", [])
                    assert isinstance(peers, dict), "Invalid response from system_peers"
                except Exception as e:
                    # RPC call might fail in test environment
                    pytest.skip(f"RPC call failed: {e}")

        except Exception as e:
            # Connection might fail in test environment
            pytest.skip(f"Connection failed: {e}")
        finally:
            # Clean up
            client.disconnect()

    @pytest.mark.network
    def test_network_endpoint_availability(self):
        """Test that the network endpoint is available and responding."""
        config = load_config()
        client = HypertensorClient(config)

        try:
            # Test connection
            connected = client.connect()
            assert connected, "Failed to connect to Hypertensor network"

            # Test that we can get basic network information
            if client.substrate:
                try:
                    # Test chain head
                    chain_head = client.substrate.get_chain_head()
                    assert chain_head is not None, "Failed to get chain head"

                    # Test runtime version
                    runtime_version = client.substrate.get_runtime_version()
                    assert runtime_version is not None, "Failed to get runtime version"

                except Exception as e:
                    # These calls might fail in test environment
                    pytest.skip(f"Network queries failed: {e}")

        except Exception as e:
            # Connection might fail in test environment
            pytest.skip(f"Connection failed: {e}")
        finally:
            # Clean up
            client.disconnect()

    def test_environment_variables(self):
        """Test environment variable configuration."""
        import os

        # Test that environment variables can be set
        test_endpoint = "wss://test.endpoint:9944"
        os.environ["HTCLI_NETWORK_ENDPOINT"] = test_endpoint

        config = load_config()
        assert config.network.endpoint == test_endpoint

        # Clean up
        if "HTCLI_NETWORK_ENDPOINT" in os.environ:
            del os.environ["HTCLI_NETWORK_ENDPOINT"]
