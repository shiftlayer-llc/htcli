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


def test_wallet_cli_remove(tmp_path):
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

    def test_for_non_existing_wallet():
        # Remove not-existing wallet
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "htcli.main",
                "wallet",
                "remove",
                "--name",
                f"wallet_not_exist",
                "--path",
                str(tmp_path),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Wallet 'wallet_not_exist' not found" in result.stdout

    def test_remove_one():
        # Remove one wallet
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "htcli.main",
                "wallet",
                "remove",
                "--name",
                f"cli_test_wallet_0",
                "--path",
                str(tmp_path),
                "--force",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Successfully removed wallet: cli_test_wallet_0" in result.stdout
        # List wallets
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "htcli.main",
                "wallet",
                "list",
                "--path",
                str(tmp_path),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert f"Available Wallets ({wallets_to_create - 1})" in result.stdout

    def test_remove_all():
        # Remove all wallets
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "htcli.main",
                "wallet",
                "remove",
                "--all",
                "--path",
                str(tmp_path),
                "--force",
            ]
        )
        assert result.returncode == 0
        # List wallets
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "htcli.main",
                "wallet",
                "list",
                "--path",
                str(tmp_path),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert f"No wallets found" in result.stdout

    test_for_non_existing_wallet()
    test_remove_one()
    test_remove_all()


def test_wallet_cli_restore(tmp_path):
    # Create wallet
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "htcli.main",
            "wallet",
            "create",
            "--name",
            f"cli_test_wallet",
            "--path",
            str(tmp_path),
            "--password",
            "password",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Created wallet" in result.stdout

    # Extract ss58-address of the newly generated wallet (example log: "📍 Address: 5EU54k9snjsgumiVMZdknE9dZWviexS5RB7u7R9xY7DRkjq5")
    ss58_address_start_index = result.stdout.index("📍 Address:") + 11
    ss58_address = result.stdout[ss58_address_start_index:].split()[0]

    # Extract mnemonic from result.stdout (mnemonic starts with "🔑 " followed by 12 English words separated by a space)
    mnemonic_start_index = result.stdout.index("🔑") + 2
    mnemonic = result.stdout[mnemonic_start_index:].split(" ")[0:12]
    mnemonic_str = " ".join(mnemonic)
    logger.info(mnemonic_str)

    # Restore wallet
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "htcli.main",
            "wallet",
            "restore",
            "--name",
            f"another_cli_test_wallet",
            "--mnemonic",
            mnemonic_str,
            "--path",
            str(tmp_path),
            "--password",
            "password",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Successfully restored wallet" in result.stdout

    # Extract ss58-address of the re-generated wallet (example log: "📍 Address: 5EU54k9snjsgumiVMZdknE9dZWviexS5RB7u7R9xY7DRkjq5")
    new_ss58_address_start_index = result.stdout.index("📍 Address:") + 11
    new_ss58_address = result.stdout[new_ss58_address_start_index:].split()[0]
    assert ss58_address == new_ss58_address
