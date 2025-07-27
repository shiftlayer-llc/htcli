"""
Unit tests for wallet key management commands (Fixed Version).
"""

import pytest
from unittest.mock import Mock, patch
from typer.testing import CliRunner
from pathlib import Path

from src.htcli.commands.wallet.keys import app


class TestWalletKeysFixed:
    """Test wallet key management commands with correct implementation."""

    def test_generate_key_success(self, cli_runner):
        """Test successful key generation."""
        with patch('src.htcli.commands.wallet.keys.generate_keypair') as mock_generate:
            # Mock successful key generation
            mock_keypair = Mock()
            mock_keypair.public_key = "0x1234567890abcdef"
            mock_keypair.ss58_address = "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            mock_generate.return_value = mock_keypair

            result = cli_runner.invoke(app, [
                "generate", "test-key",
                "--type", "sr25519"
            ])

            assert result.exit_code == 0
            assert "Keypair 'test-key' generated successfully!" in result.stdout
            assert "0x1234567890abcdef" in result.stdout

    def test_generate_key_with_password(self, cli_runner):
        """Test key generation with password."""
        with patch('src.htcli.commands.wallet.keys.generate_keypair') as mock_generate:
            mock_keypair = Mock()
            mock_keypair.public_key = "0x1234567890abcdef"
            mock_keypair.ss58_address = "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            mock_generate.return_value = mock_keypair

            result = cli_runner.invoke(app, [
                "generate", "test-key",
                "--type", "sr25519",
                "--password", "test-password"
            ])

            assert result.exit_code == 0
            assert "Keypair 'test-key' generated successfully!" in result.stdout

    def test_generate_key_invalid_type(self, cli_runner):
        """Test key generation with invalid key type."""
        result = cli_runner.invoke(app, [
            "generate", "test-key",
            "--type", "invalid-type"
        ])

        assert result.exit_code != 0
        assert "Invalid key type" in result.stdout

    def test_generate_key_missing_name(self, cli_runner):
        """Test key generation with missing name."""
        result = cli_runner.invoke(app, ["generate"])
        assert result.exit_code != 0

    def test_list_keys_success(self, cli_runner):
        """Test successful key listing."""
        with patch('src.htcli.commands.wallet.keys.list_keys') as mock_list:
            # Mock successful key listing
            mock_key1 = Mock()
            mock_key1.name = "test-key-1"
            mock_key1.key_type = "sr25519"
            mock_key1.ss58_address = "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"

            mock_key2 = Mock()
            mock_key2.name = "test-key-2"
            mock_key2.key_type = "ed25519"
            mock_key2.ss58_address = "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty"

            mock_list.return_value = [mock_key1, mock_key2]

            result = cli_runner.invoke(app, ["list"])

            assert result.exit_code == 0
            assert "test-key-1" in result.stdout
            assert "test-key-2" in result.stdout

    def test_list_keys_empty(self, cli_runner):
        """Test key listing when no keys exist."""
        with patch('src.htcli.commands.wallet.keys.list_keys') as mock_list:
            mock_list.return_value = []

            result = cli_runner.invoke(app, ["list"])

            assert result.exit_code == 0
            assert "No keys found" in result.stdout

    def test_import_key_success(self, cli_runner):
        """Test successful key import."""
        with patch('src.htcli.commands.wallet.keys.import_keypair') as mock_import:
            mock_keypair = Mock()
            mock_keypair.ss58_address = "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
            mock_import.return_value = mock_keypair

            result = cli_runner.invoke(app, [
                "import-key", "imported-key",
                "--private-key", "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                "--type", "sr25519"
            ])

            assert result.exit_code == 0
            assert "Keypair 'imported-key' imported successfully!" in result.stdout

    def test_import_key_invalid_private_key(self, cli_runner):
        """Test key import with invalid private key."""
        result = cli_runner.invoke(app, [
            "import-key", "imported-key",
            "--private-key", "invalid-private-key",
            "--type", "sr25519"
        ])

        assert result.exit_code != 0
        assert "Invalid private key format" in result.stdout

    def test_import_key_invalid_type(self, cli_runner):
        """Test key import with invalid key type."""
        result = cli_runner.invoke(app, [
            "import-key", "imported-key",
            "--private-key", "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            "--type", "invalid-type"
        ])

        assert result.exit_code != 0
        assert "Invalid key type" in result.stdout

    def test_import_key_missing_required_args(self, cli_runner):
        """Test key import with missing required arguments."""
        result = cli_runner.invoke(app, ["import-key", "test-key"])
        assert result.exit_code != 0

    def test_delete_key_success(self, cli_runner):
        """Test successful key deletion."""
        with patch('src.htcli.commands.wallet.keys.delete_keypair') as mock_delete:
            mock_delete.return_value = None

            result = cli_runner.invoke(app, ["delete", "test-key"])

            assert result.exit_code == 0
            assert "Keypair 'test-key' deleted successfully!" in result.stdout

    def test_delete_key_not_found(self, cli_runner):
        """Test key deletion when key doesn't exist."""
        with patch('src.htcli.commands.wallet.keys.delete_keypair') as mock_delete:
            mock_delete.side_effect = Exception("Key not found")

            result = cli_runner.invoke(app, ["delete", "non-existent-key"])

            assert result.exit_code != 0
            assert "Failed to delete keypair" in result.stdout

    def test_delete_key_missing_name(self, cli_runner):
        """Test key deletion with missing name."""
        result = cli_runner.invoke(app, ["delete"])
        assert result.exit_code != 0

    def test_help_output(self, cli_runner):
        """Test help output for keys commands."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "generate" in result.stdout
        assert "list" in result.stdout
        assert "import-key" in result.stdout
        assert "delete" in result.stdout

    def test_generate_help_output(self, cli_runner):
        """Test help output for generate command."""
        result = cli_runner.invoke(app, ["generate", "--help"])
        assert result.exit_code == 0
        assert "NAME" in result.stdout
        assert "--type" in result.stdout
        assert "--password" in result.stdout

    def test_list_help_output(self, cli_runner):
        """Test help output for list command."""
        result = cli_runner.invoke(app, ["list", "--help"])
        assert result.exit_code == 0

    def test_import_help_output(self, cli_runner):
        """Test help output for import-key command."""
        result = cli_runner.invoke(app, ["import-key", "--help"])
        assert result.exit_code == 0
        assert "NAME" in result.stdout
        assert "--private-key" in result.stdout
        assert "--type" in result.stdout
        assert "--password" in result.stdout

    def test_delete_help_output(self, cli_runner):
        """Test help output for delete command."""
        result = cli_runner.invoke(app, ["delete", "--help"])
        assert result.exit_code == 0
        assert "NAME" in result.stdout
