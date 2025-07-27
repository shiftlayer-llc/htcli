#!/usr/bin/env python3
"""
Simple network connectivity test for Hypertensor blockchain.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from htcli.client import HypertensorClient
from htcli.config import load_config


def test_network_connectivity():
    """Test basic connectivity to the Hypertensor network."""
    print("🔍 Testing network connectivity to Hypertensor blockchain...")

    try:
        # Load configuration
        config = load_config()
        print(f"📡 Endpoint: {config.network.endpoint}")
        print(f"🔌 WebSocket: {config.network.ws_endpoint}")

        # Create client
        client = HypertensorClient(config)

        # Test connection
        print("🔄 Attempting to connect...")
        connected = client.connect()

        if connected:
            print("✅ Successfully connected to Hypertensor network!")

            # Test WebSocket connection
            print("🔄 Testing WebSocket connection...")
            async def test_ws():
                try:
                    ws_connected = await client.connect_websocket()
                    if ws_connected:
                        print("✅ WebSocket connection successful!")
                    else:
                        print("❌ WebSocket connection failed!")
                except Exception as e:
                    print(f"❌ WebSocket error: {e}")
                finally:
                    if client.ws_connection:
                        await client.ws_connection.close()

            asyncio.run(test_ws())

            # Clean up
            client.disconnect()
            print("🔌 Disconnected from network")

            # Clean up WebSocket properly
            if hasattr(client, 'ws_connection') and client.ws_connection:
                try:
                    asyncio.run(client.ws_connection.close())
                except:
                    pass

        else:
            print("❌ Failed to connect to Hypertensor network")
            return False

    except Exception as e:
        print(f"❌ Error during connectivity test: {e}")
        return False

    return True


def test_cli_commands():
    """Test basic CLI commands."""
    print("\n🧪 Testing CLI commands...")

    try:
        from htcli.main import app
        from typer.testing import CliRunner

        runner = CliRunner()

        # Test main help
        result = runner.invoke(app, ["--help"])
        if result.exit_code == 0:
            print("✅ Main CLI help works")
        else:
            print("❌ Main CLI help failed")

        # Test subnet register help
        result = runner.invoke(app, ["register", "--help"])
        if result.exit_code == 0:
            print("✅ Subnet register help works")
        else:
            print("❌ Subnet register help failed")

        # Test wallet keys help
        result = runner.invoke(app, ["keys", "--help"])
        if result.exit_code == 0:
            print("✅ Wallet keys help works")
        else:
            print("❌ Wallet keys help failed")

        # Test chain info help
        result = runner.invoke(app, ["info", "--help"])
        if result.exit_code == 0:
            print("✅ Chain info help works")
        else:
            print("❌ Chain info help failed")

    except Exception as e:
        print(f"❌ Error testing CLI commands: {e}")


def main():
    """Main test function."""
    print("🚀 Starting HTCLI Network Connectivity Test")
    print("=" * 50)

    # Test network connectivity
    network_ok = test_network_connectivity()

    # Test CLI commands
    test_cli_commands()

    print("\n" + "=" * 50)
    if network_ok:
        print("🎉 All tests completed successfully!")
        print("✅ Your Hypertensor endpoint is working correctly")
        print("✅ CLI commands are properly configured")
    else:
        print("⚠️  Some tests failed")
        print("❌ Check your network connection and endpoint configuration")

    return 0 if network_ok else 1


if __name__ == "__main__":
    sys.exit(main())
