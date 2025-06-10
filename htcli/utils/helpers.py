import json
from pathlib import Path
import typer
from substrateinterface import SubstrateInterface, Keypair
from decimal import Decimal
from rich.console import Console

console = Console()

def read_wallet_data_for_verification(file_path: Path, is_json: bool, password: str):
    """
    Read and deobfuscate wallet data from a file.

    Args:
        file_path (Path): Path to the wallet file
        is_json (bool): Whether the file is in JSON format
        password (str): Password for deobfuscation

    Returns:
        bytes: Deobfuscated private key bytes
    """
    if is_json:
        with open(file_path, "r") as f:
            wallet_data = json.load(f)
            obfuscated_private_key_hex = wallet_data.get("privateKey", "").replace(
                "0x", ""
            )
            obfuscated_private_key_bytes = bytes.fromhex(obfuscated_private_key_hex)
            # De-obfuscate the private key bytes
            return deobfuscate_bytes(obfuscated_private_key_bytes, password)
    else:
        with open(file_path, "rb") as f:
            saved_obfuscated_private_key = f.read()
            # De-obfuscate the private key bytes
            return deobfuscate_bytes(saved_obfuscated_private_key, password)


def deobfuscate_bytes(data: bytes, key: str) -> bytes:
    """
    Deobfuscate bytes using a key.

    Args:
        data (bytes): The obfuscated data
        key (str): The key to use for deobfuscation

    Returns:
        bytes: The deobfuscated data
    """
    if not key:
        return data
    key_bytes = key.encode("utf-8")
    return bytes(data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data)))


def check_balance(substrate: SubstrateInterface, call, keypair: Keypair) -> bool:
    """
    Check if the account has enough balance to pay the transaction fee
    and ask the user to confirm the transaction.

    :param substrate: Substrate interface
    :param call: Composed call object
    :param keypair: Keypair of the sender
    :return: True if the user confirms to proceed, False otherwise
    """

    # Get estimated fee
    payment_info = substrate.get_payment_info(call=call, keypair=keypair)
    fee_planck = int(payment_info["partialFee"])
    fee_token = Decimal(fee_planck) / Decimal(10**12)
    console.print(f"[yellow]Estimated transaction fee: {fee_token:.6f} tokens[/yellow]")

    # Get account balance
    account_info = substrate.query("System", "Account", [keypair.ss58_address])
    free_balance = int(account_info.value["data"]["free"])
    free_balance_token = Decimal(free_balance) / Decimal(10**12)

    if free_balance < fee_planck:
        raise ValueError(
            f"❌ Insufficient balance ({free_balance_token:.6f}) tokens to cover the fee ({fee_token:.6f}) tokens."
        )
    else:
        projected_balance = free_balance_token - fee_token
        console.print(
            f"[green]✅ Sufficient balance. Your balance will be approximately {projected_balance:.6f} tokens after the transaction.[/green]"
        )

    # Ask for user confirmation
    confirm = typer.confirm("Do you want to proceed with the registration?")
    return confirm
