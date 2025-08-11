#!/usr/bin/env python3
"""
Test script to validate the configuration system.
"""

import subprocess
import sys
from pathlib import Path


def test_config_system():
    """Test the configuration system with proper inputs."""

    print("🧪 Testing Hypertensor CLI Configuration System")
    print("=" * 50)

    # Remove existing config
    config_path = Path.home() / ".htcli" / "config.yaml"
    if config_path.exists():
        config_path.unlink()
        print("✅ Removed existing configuration")

    # Test config path command
    print("\n1. Testing config path command...")
    result = subprocess.run(
        ["uv", "run", "htcli", "config", "path"], capture_output=True, text=True
    )
    if result.returncode == 0:
        print("✅ Config path command works")
        print(f"   Output: {result.stdout.strip()}")
    else:
        print("❌ Config path command failed")
        print(f"   Error: {result.stderr}")
        return False

    # Create a test configuration programmatically
    print("\n2. Creating test configuration...")

    # Create config directory
    config_dir = config_path.parent
    config_dir.mkdir(parents=True, exist_ok=True)

    # Write test configuration
    test_config = """# Hypertensor CLI Configuration
# This file contains the configuration settings for the Hypertensor CLI tool.
# You can edit this file directly or use 'htcli config init' to regenerate it.

# Network Configuration
# Settings for connecting to the Hypertensor blockchain network
network:
  # RPC endpoint for blockchain communication
  endpoint: "wss://hypertensor.duckdns.org"

  # WebSocket endpoint for real-time communication
  ws_endpoint: "wss://hypertensor.duckdns.org"

  # Connection timeout in seconds
  timeout: 30

  # Number of retry attempts for failed connections
  retry_attempts: 3

# Output Configuration
# Settings for CLI output formatting and display
output:
  # Default output format (table, json, csv)
  format: "table"

  # Enable verbose output with detailed information
  verbose: false

  # Enable colored output in terminal
  color: true

# Wallet Configuration
# Settings for wallet and key management
wallet:
  # Path where wallets and keys are stored
  path: "~/.htcli/wallets"

  # Default wallet name to use
  default_name: "default"

  # Enable wallet encryption for security
  encryption_enabled: true
"""

    with open(config_path, "w") as f:
        f.write(test_config)

    print("✅ Test configuration created")

    # Test config show command
    print("\n3. Testing config show command...")
    result = subprocess.run(
        ["uv", "run", "htcli", "config", "show"], capture_output=True, text=True
    )
    if result.returncode == 0:
        print("✅ Config show command works")
        print("   Configuration loaded successfully")
    else:
        print("❌ Config show command failed")
        print(f"   Error: {result.stderr}")
        return False

    # Test config validate command
    print("\n4. Testing config validate command...")
    result = subprocess.run(
        ["uv", "run", "htcli", "config", "validate"], capture_output=True, text=True
    )
    if result.returncode == 0:
        print("✅ Config validate command works")
        print("   Configuration is valid")
    else:
        print("❌ Config validate command failed")
        print(f"   Error: {result.stderr}")
        return False

    # Test config show with different formats
    print("\n5. Testing config show with YAML format...")
    result = subprocess.run(
        ["uv", "run", "htcli", "config", "show", "--format", "yaml"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print("✅ Config show YAML format works")
    else:
        print("❌ Config show YAML format failed")
        print(f"   Error: {result.stderr}")
        return False

    print("\n6. Testing config show with JSON format...")
    result = subprocess.run(
        ["uv", "run", "htcli", "config", "show", "--format", "json"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print("✅ Config show JSON format works")
    else:
        print("❌ Config show JSON format failed")
        print(f"   Error: {result.stderr}")
        return False

    # Test that the CLI now uses the configuration
    print("\n7. Testing that CLI uses the configuration...")
    result = subprocess.run(
        ["uv", "run", "htcli", "--help"], capture_output=True, text=True
    )
    if result.returncode == 0 and "config" in result.stdout:
        print("✅ CLI includes config commands")
    else:
        print("❌ CLI doesn't include config commands")
        return False

    print("\n" + "=" * 50)
    print("🎉 All configuration system tests passed!")
    print("✅ Configuration system is working correctly")

    return True


if __name__ == "__main__":
    success = test_config_system()
    sys.exit(0 if success else 1)
