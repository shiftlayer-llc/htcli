from htcli.hypertensor.substrate.chain_functions import update_hotkey
from htcli.hypertensor.substrate.config import SubstrateConfigwithKeypair

substrate = SubstrateConfigwithKeypair("node1", "wss://hypertensor.duckdns.org")
receipt = update_hotkey(substrate.interface, substrate.keypair, "0xfa8180d137b00905c369bcd5ea808a63654b754413327f6e894b19f61d931561", "0x3ed9589733869b344f39460c315900c5c0838dbf8eb9b2f135dc4d5d686cfb19")
print(receipt)