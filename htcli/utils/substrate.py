"""
Substrate config file for storing blockchain configuration and parameters in a pickle
to avoid remote blockchain calls
"""
from substrateinterface import SubstrateInterface, Keypair
from htcli.utils.wallet import import_wallet


class SubstrateConfigCustom:
  def __init__(self, phrase, url):
    self.url = url
    self.interface: SubstrateInterface = SubstrateInterface(url=url)
    self.keypair = Keypair.create_from_uri(phrase)

class SubstrateConfigwithKeypair:
  def __init__(self, name, url, wallet_dir, password):
    self.url = url
    self.interface: SubstrateInterface = SubstrateInterface(url=url)
    self.keypair = import_wallet(name=name, wallet_dir=wallet_dir, password=password)
    