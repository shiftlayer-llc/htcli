import typer
from htcli.core.constants import (
    CHAIN_ENV_URLS,
    DEFAULT_WALLET_PATH,
    DEFAULT_MODEL_PATH
)
def get_rpc(rpc_url, rpc_network):
    if rpc_url:
        rpc = rpc_url
    else:
        rpc = CHAIN_ENV_URLS[rpc_network]
    return rpc
def check_name(name: str):
    if not name:
        name = typer.prompt(
            "Enter wallet name",
            show_default=True,
        )
    return name
def check_path(path: str):
    if not path:
        path = typer.prompt(
            "Enter subnet model path",
            default=DEFAULT_MODEL_PATH,
            show_default=True,
        )
    return path
def check_wallet_path(wallet_path: str):
    if not wallet_path:
        wallet_path = typer.prompt(
            "Enter wallet path",
            default=DEFAULT_WALLET_PATH,
            show_default=True,
        )
    return wallet_path
def check_password(wallet_password: str):
    if not wallet_password:
        wallet_password = typer.prompt(
            "Enter wallet password",
            hide_input=True
        )
    return wallet_password