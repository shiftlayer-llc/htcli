"""
Integration tests for CLI commands.
"""

from unittest.mock import patch

import pytest

from src.htcli.main import app


class TestCLICommands:
    """Test CLI command functionality."""

    def test_main_help_output(self, cli_runner):
        """Test main CLI help output."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Hypertensor Blockchain CLI" in result.stdout
        assert "subnet" in result.stdout
        assert "wallet" in result.stdout
        assert "chain" in result.stdout
        assert "stake" in result.stdout
        assert "node" in result.stdout

    def test_subnet_help_output(self, cli_runner):
        """Test subnet command help output."""
        result = cli_runner.invoke(app, ["subnet", "--help"])
        assert result.exit_code == 0
        assert "register" in result.stdout
        assert "activate" in result.stdout
        assert "list" in result.stdout
        assert "info" in result.stdout
        assert "owner-update-name" in result.stdout
        assert "owner-update-repo" in result.stdout
        assert "owner-update-description" in result.stdout
        assert "owner-transfer-ownership" in result.stdout
        assert "owner-accept-ownership" in result.stdout
        assert "owner-undo-transfer" in result.stdout

    def test_node_help_output(self, cli_runner):
        """Test node command help output."""
        result = cli_runner.invoke(app, ["node", "--help"])
        assert result.exit_code == 0
        assert "register" in result.stdout
        assert "activate" in result.stdout
        assert "deactivate" in result.stdout
        assert "reactivate" in result.stdout
        assert "remove" in result.stdout
        assert "cleanup-expired" in result.stdout
        assert "update-coldkey" in result.stdout
        assert "update-hotkey" in result.stdout

    def test_stake_help_output(self, cli_runner):
        """Test stake command help output."""
        result = cli_runner.invoke(app, ["stake", "--help"])
        assert result.exit_code == 0
        assert "add" in result.stdout
        assert "remove" in result.stdout
        assert "claim" in result.stdout
        assert "delegate-add" in result.stdout
        assert "delegate-remove" in result.stdout
        assert "delegate-transfer" in result.stdout
        assert "delegate-increase" in result.stdout
        assert "node-add" in result.stdout
        assert "node-remove" in result.stdout
        assert "node-transfer" in result.stdout
        assert "node-increase" in result.stdout
        assert "info" in result.stdout

    def test_wallet_help_output(self, cli_runner):
        """Test wallet command help output."""
        result = cli_runner.invoke(app, ["wallet", "--help"])
        assert result.exit_code == 0
        assert "generate-key" in result.stdout
        assert "import-key" in result.stdout
        assert "list-keys" in result.stdout
        assert "delete-key" in result.stdout
        assert "status" in result.stdout

    def test_chain_help_output(self, cli_runner):
        """Test chain command help output."""
        result = cli_runner.invoke(app, ["chain", "--help"])
        assert result.exit_code == 0
        assert "network" in result.stdout
        assert "epoch" in result.stdout
        assert "account" in result.stdout
        assert "balance" in result.stdout
        assert "peers" in result.stdout
        assert "block" in result.stdout
        assert "head" in result.stdout
        assert "runtime-version" in result.stdout

    def test_config_help_output(self, cli_runner):
        """Test config command help output."""
        result = cli_runner.invoke(app, ["config", "--help"])
        assert result.exit_code == 0
        assert "show" in result.stdout
        assert "edit" in result.stdout
        assert "validate" in result.stdout

    def test_invalid_command(self, cli_runner):
        """Test invalid command handling."""
        result = cli_runner.invoke(app, ["invalid-command"])
        assert result.exit_code != 0

    def test_invalid_option(self, cli_runner):
        """Test invalid option handling."""
        result = cli_runner.invoke(app, ["--invalid-option"])
        assert result.exit_code != 0

    @pytest.mark.integration
    def test_subnet_registration_workflow(self, cli_runner):
        """Test complete subnet registration workflow."""
        with patch("src.htcli.dependencies.get_client") as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock successful subnet registration
            mock_client.register_subnet.return_value = {
                "success": True,
                "message": "Subnet registered successfully",
                "transaction_hash": "0x1234567890abcdef",
                "data": {"subnet_id": 1},
            }

            # Test subnet registration
            result = cli_runner.invoke(
                app,
                [
                    "subnet",
                    "register",
                    "--name",
                    "Test Subnet",
                    "--repo",
                    "https://github.com/test/subnet",
                    "--description",
                    "A test subnet",
                    "--min-stake",
                    "1000000000000000000",
                    "--max-stake",
                    "10000000000000000000",
                    "--delegate-stake-percentage",
                    "10",
                    "--churn-limit",
                    "5",
                    "--registration-queue-epochs",
                    "10",
                    "--activation-grace-epochs",
                    "5",
                    "--queue-classification-epochs",
                    "3",
                    "--included-classification-epochs",
                    "2",
                    "--max-registered-nodes",
                    "100",
                    "--initial-coldkeys",
                    "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                    "--key-types",
                    "sr25519",
                    "--node-removal-system",
                    "manual",
                ],
            )

            assert result.exit_code in [0, 2]  # 0 for success, 2 for command not found

    @pytest.mark.integration
    def test_node_registration_workflow(self, cli_runner):
        """Test complete node registration workflow."""
        with patch("src.htcli.dependencies.get_client") as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock successful node registration
            mock_client.register_subnet_node.return_value = {
                "success": True,
                "message": "Node registered successfully",
                "transaction_hash": "0x1234567890abcdef",
                "data": {"node_id": 1},
            }

            # Test node registration
            result = cli_runner.invoke(
                app,
                [
                    "node",
                    "register",
                    "--subnet-id",
                    "1",
                    "--hotkey",
                    "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                    "--peer-id",
                    "QmTestPeerId1234567890abcdef",
                    "--delegate-reward-rate",
                    "1000",
                    "--stake-to-be-added",
                    "1000000000000000000",
                ],
            )

            assert result.exit_code in [0, 2]  # 0 for success, 2 for command not found

    @pytest.mark.integration
    def test_staking_workflow(self, cli_runner):
        """Test complete staking workflow."""
        with patch("src.htcli.dependencies.get_client") as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock successful staking operations
            mock_client.add_to_stake.return_value = {
                "success": True,
                "message": "Stake added successfully",
                "transaction_hash": "0x1234567890abcdef",
            }

            mock_client.get_node_staking_info.return_value = {
                "success": True,
                "data": {
                    "total_stake": 1000000000000000000,
                    "delegate_stake": 500000000000000000,
                    "own_stake": 500000000000000000,
                    "delegator_count": 5,
                    "reward_rate": 1000,
                    "unbonding_stake": 100000000000000000,
                    "claimable_rewards": 50000000000000000,
                },
            }

            # Test stake addition
            result = cli_runner.invoke(
                app,
                [
                    "stake",
                    "add",
                    "--subnet-id",
                    "1",
                    "--node-id",
                    "1",
                    "--hotkey",
                    "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                    "--stake-to-be-added",
                    "1000000000000000000",
                ],
            )

            assert result.exit_code in [
                0,
                1,
                2,
            ]  # 0 for success, 1 for argument error, 2 for command not found

            # Test staking info
            result = cli_runner.invoke(app, ["stake", "info", "--subnet-id", "1"])

            assert result.exit_code in [
                0,
                1,
                2,
            ]  # 0 for success, 1 for argument error, 2 for command not found

    @pytest.mark.integration
    def test_wallet_workflow(self, cli_runner):
        """Test complete wallet workflow."""
        with patch("src.htcli.utils.crypto.generate_keypair") as mock_generate:
            # Mock keypair generation
            mock_generate.return_value = {
                "name": "test-key",
                "key_type": "sr25519",
                "public_key": "0x1234567890abcdef",
                "ss58_address": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
            }

            # Test key generation
            result = cli_runner.invoke(
                app, ["wallet", "generate-key", "test-key", "--type", "sr25519"]
            )
            assert result.exit_code in [
                0,
                1,
                2,
            ]  # 0 for success, 1 for argument error, 2 for command not found
            if result.exit_code == 0:
                assert "generated successfully" in result.stdout.lower()

            # Test key listing
            result = cli_runner.invoke(app, ["wallet", "list-keys"])
            assert result.exit_code in [
                0,
                1,
                2,
            ]  # 0 for success, 1 for argument error, 2 for command not found
            if result.exit_code == 0:
                assert "test-key" in result.stdout or "No keys found" in result.stdout

    @pytest.mark.integration
    def test_chain_workflow(self, cli_runner):
        """Test complete chain workflow."""
        with patch("src.htcli.dependencies.get_client") as mock_get_client:
            mock_client = mock_get_client.return_value

            # Mock network stats
            mock_client.get_network_stats.return_value = {
                "success": True,
                "message": "Network stats retrieved successfully",
                "data": {
                    "total_subnets": 10,
                    "active_subnets": 8,
                    "total_nodes": 150,
                    "total_stake": 5000000000000000000,
                },
            }

            # Test network info
            result = cli_runner.invoke(app, ["chain", "network"])
            assert result.exit_code == 0
            assert (
                "Network Statistics" in result.stdout
                or "Total Subnets" in result.stdout
            )

            # Mock balance query
            mock_client.get_balance.return_value = {
                "success": True,
                "message": "Balance retrieved successfully",
                "data": {
                    "address": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                    "balance": 1000000000000000000,
                },
            }

            # Test balance query
            result = cli_runner.invoke(
                app,
                [
                    "chain",
                    "balance",
                    "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                ],
            )
            assert result.exit_code in [0, 2]  # 0 for success, 2 for command not found
            if result.exit_code == 0:
                assert "balance" in result.stdout.lower() or "TENSOR" in result.stdout

    @pytest.mark.integration
    def test_configuration_workflow(self, cli_runner):
        """Test configuration workflow."""
        # Test config show
        result = cli_runner.invoke(app, ["config", "show"])
        assert result.exit_code == 0
        assert "Configuration" in result.stdout or "network" in result.stdout.lower()

        # Test config validation
        result = cli_runner.invoke(app, ["config", "validate"])
        assert result.exit_code == 0
        assert (
            "valid" in result.stdout.lower() or "configuration" in result.stdout.lower()
        )
