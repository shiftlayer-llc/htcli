from .chain import chain_config
from .subnet import subnet_config
from .wallet import wallet_config

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