import typer
import os


class chain_config:
    rpc_url = typer.Option(
        None,
        "--chain.rpc_url",
        "--rpc_url",
        "--chain.url",
        help="RPC URL for the chain",
    )
    rpc_network = typer.Option(
        "mainnet",
        "--chain.rpc_network",
        "--rpc_network",
        help="Environment for the chain (local/testnet/mainnet)",
    )

    def __repr__(self):
        return f"chain_config(rpc_url={self.rpc_url}, env={self.env})"


class subnet_config:
    id = typer.Option(
        0,
        "--subnet.id",
        "--subnet_id",
        "--netuid",
        help="Unique ID for the subnetwork",
    )
    name = typer.Option(
        "default",
        "--subnet.name",
        "--subnet_name",
        help="Name of the subnetwork",
    )

    path = typer.Option(
        "",
        "--subnet.path",
        "--subnet_path",
        "--path",
        help="Path to download the model",
    )
    memory_mb = typer.Option(
        4096,
        "--subnet.memory_mb",
        "--subnet_memory_mb",
        "--memory_mb",
        help="Memory requirements to host entire model one time",
    )


class wallet_config:
    path = typer.Option(
        os.path.expanduser("~/.hypertensor/wallets"),
        "--wallet.path",
        "--wallet_path",
        help="Path to the wallets directory",
    )
    name = typer.Option(
        None,
        "--wallet.name",
        "--wallet_name",
        help="Name of the wallet",
    )
    password = typer.Option(
        None,
        "--wallet.password",
        "--wallet_password",
        help="Password for the wallet",
    )
    mnemonic = typer.Option(
        None,
        "--wallet.mnemonic",
        "--wallet_mnemonic",
        help="Mnemonic for the wallet",
    )

    def __repr__(self):
        return f"wallet_config(wallet_path={self.path}, name={self.name}"

    def __str__(self):
        return f"wallet_config(wallet_path={self.path}, name={self.name}"

class options_config:
    registration_blocks = typer.Option(
        14400,
        "--subnet.registration_blocks",
        "--subnet_registration_blocks",
        "--registration_blocks",
        help="blocks to keep subnet in registration period",
    )
    entry_interval = typer.Option(
        0,
        "--subnet.entry_interval",
        "--subnet_entry_interval",
        "--entry_interval",
        help="blocks required between each subnet node entry",
    )

class htcli_config:
    def __init__(
        self, chain: chain_config, subnet: subnet_config, wallet: wallet_config
    ):
        self.chain = chain
        self.subnet = subnet
        self.wallet = wallet

    def __repr__(self):
        return f"htcli_config(chain={self.chain}, subnet={self.subnet}, wallet={self.wallet})"

    def __str__(self):
        return f"htcli_config(chain={self.chain}, subnet={self.subnet}, wallet={self.wallet})"

    def __hash__(self):
        return hash((self.chain, self.subnet, self.wallet))

    def __eq__(self, other):
        if not isinstance(other, htcli_config):
            return False
        return (
            self.chain == other.chain
            and self.subnet == other.subnet
            and self.wallet == other.wallet
        )
