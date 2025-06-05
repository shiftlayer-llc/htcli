import subprocess
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="htcli.log",
    filemode="a",
)
logger = logging.getLogger(__name__)


def test_wallet_cli_create(tmp_path):
    def with_password(password):
        logger.info(f"Running test with password: {password}")
        # Run the CLI command with the provided password
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "htcli.main",
                "wallet",
                "create",
                "--name",
                "cli_test_wallet",
                "--path",
                str(tmp_path),
                "--password",
                password,
            ],
            capture_output=True,
            text=True,
        )
        logger.info(f"CLI output: {result.stdout}")
        logger.error(f"CLI error: {result.stderr}")
        assert result.returncode == 0
        assert "Created wallet" in result.stdout
        return result.stdout

    def without_password():
        logger.info("Running test without password")
        # Run the CLI command without a password
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "htcli.main",
                "wallet",
                "create",
                "--name",
                "cli_test_wallet",
                "--path",
                str(tmp_path),
                "--password",
                "",
                "--force",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Created wallet" in result.stdout
        return result.stdout

    with_password("password")
    without_password()


def test_wallet_cli_list(tmp_path):
    wallets_to_create = 3
    # Create wallets
    for i in range(wallets_to_create):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "htcli.main",
                "wallet",
                "create",
                "--name",
                f"cli_test_wallet_{i}",
                "--path",
                str(tmp_path),
                "--password",
                "password",
            ]
        )
    assert result.returncode == 0
    # List wallets
    result = subprocess.run(
        [sys.executable, "-m", "htcli.main", "wallet", "list", "--path", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    logger.info(f"CLI output: {result.stdout}")
    assert result.returncode == 0
    assert f"Available Wallets ({wallets_to_create})" in result.stdout
