import logging
import os
import pytest
from substrateinterface import Keypair
from htcli.utils import wallet


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="htcli.log",
    filemode="a",
)
logger = logging.getLogger(__name__)


# Test generate_mnemonic
def test_generate_mnemonic():
    mnemonic = wallet.generate_mnemonic()
    assert isinstance(mnemonic, str)
    assert len(mnemonic.split()) >= 12


# Test create_keypair_from_mnemonic
def test_create_keypair_from_mnemonic():
    mnemonic = wallet.generate_mnemonic()
    keypair = wallet.create_keypair_from_mnemonic(mnemonic)
    assert isinstance(keypair, Keypair)
    assert hasattr(keypair, "ss58_address")


# Test get_account_id
def test_get_account_id():
    mnemonic = wallet.generate_mnemonic()
    keypair = wallet.create_keypair_from_mnemonic(mnemonic)
    account_id = wallet.get_account_id(keypair.public_key)
    assert isinstance(account_id, str)
    assert account_id.startswith("0x")
    assert len(account_id) == 66  # 64-bit address + "0x" prefix


# Test encrypt_data and decrypt_data
def test_encrypt_decrypt_data():
    data = b"testdata123"
    password = "securepass"
    encrypted = wallet.encrypt_data(data, password)
    assert encrypted != data
    decrypted = wallet.decrypt_data(encrypted, password)
    assert decrypted == data


# Test create_wallet and import_wallet
def test_create_and_import_wallet(tmp_path):
    name = "testwallet"
    wallet_dir = tmp_path
    password = "testpass"
    main_wallet_file_path, ss58_address, mnemonic = wallet.create_wallet(
        name=name,
        wallet_dir=wallet_dir,
        is_hotkey=True,
        password=password,
        owner_address="5F3sa2TJAWMqDhXG6jhV4N8ko9rTGbTMnQw3j6QGz5oP9Y3N",
    )
    assert os.path.exists(main_wallet_file_path)
    assert ss58_address.startswith("5")
    assert isinstance(mnemonic, str)
    # Import wallet
    keypair = wallet.import_wallet(name, wallet_dir, password=password)
    assert isinstance(keypair, Keypair)
    assert keypair.ss58_address == ss58_address
    # Clean up
    os.remove(main_wallet_file_path)


# Test error on duplicate wallet creation
def test_create_wallet_duplicate(tmp_path):
    name = "dupwallet"
    wallet_dir = tmp_path
    wallet.create_wallet(name=name, wallet_dir=wallet_dir, is_hotkey=False)
    with pytest.raises(ValueError):
        wallet.create_wallet(name=name, wallet_dir=wallet_dir, is_hotkey=False)


# Test import_wallet with wrong password
def test_import_wallet_wrong_password(tmp_path):
    name = "wrongpasswallet"
    wallet_dir = tmp_path
    right_password = "rightpass"
    wrong_password = "wrongpass"
    wallet.create_wallet(
        name=name, wallet_dir=wallet_dir, is_hotkey=False, password=right_password
    )
    with pytest.raises(RuntimeError):
        wallet.import_wallet(name, wallet_dir, password=wrong_password)
