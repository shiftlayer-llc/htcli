"""
Modular client structure for Hypertensor CLI.
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from substrateinterface import SubstrateInterface
from ..models.requests import *
from ..models.responses import *
from .subnet import SubnetClient
from .wallet import WalletClient
from .chain import ChainClient

logger = logging.getLogger(__name__)


class HypertensorClient:
    """Main client for interacting with Hypertensor blockchain."""

    def __init__(self, config):
        self.config = config
        self.substrate = None
        self.ws_connection = None

        # Initialize modular clients
        self.subnet = None
        self.wallet = None
        self.chain = None

        self.connect()

    def connect(self, rpc_url: Optional[str] = None) -> bool:
        """Connect to the Hypertensor blockchain."""
        try:
            url = rpc_url or self.config.network.endpoint
            self.substrate = SubstrateInterface(url=url, ss58_format=0)
            logger.info(f"Connected to blockchain at {url}")

            # Initialize modular clients
            self.subnet = SubnetClient(self.substrate)
            self.wallet = WalletClient(self.substrate)
            self.chain = ChainClient(self.substrate)

            return True
        except Exception as e:
            logger.error(f"Failed to connect to blockchain: {e}")
            # Initialize modular clients with None substrate for testing
            self.subnet = SubnetClient(None)
            self.wallet = WalletClient(None)
            self.chain = ChainClient(None)
            return False

    async def connect_websocket(self, ws_url: Optional[str] = None):
        """Connect to WebSocket endpoint."""
        try:
            url = ws_url or self.config.network.ws_endpoint
            import websockets

            self.ws_connection = await websockets.connect(url)
            logger.info(f"Connected to WebSocket at {url}")
        except Exception as e:
            logger.error(f"Failed to connect to WebSocket: {e}")

    def disconnect(self):
        """Disconnect from blockchain."""
        if self.substrate:
            self.substrate.close()
        if self.ws_connection:
            asyncio.create_task(self.ws_connection.close())

    # ===== DELEGATION METHODS TO MODULAR CLIENTS =====

    # Subnet operations
    def register_subnet(self, request: SubnetRegisterRequest, keypair=None):
        """Register a new subnet."""
        return self.subnet.register_subnet(request, keypair)

    def activate_subnet(self, subnet_id: int, keypair=None):
        """Activate a subnet."""
        return self.subnet.activate_subnet(subnet_id, keypair)

    def get_subnet_data(self, subnet_id: int):
        """Get subnet data."""
        return self.subnet.get_subnet_data(subnet_id)

    def get_subnets_data(self, active_only: bool = False):
        """Get all subnets data."""
        return self.subnet.get_subnets_data(active_only)

    def add_subnet_node(self, request: SubnetNodeAddRequest, keypair=None):
        """Add a node to a subnet."""
        return self.subnet.add_subnet_node(request, keypair)

    def register_subnet_node(
        self,
        subnet_id: int,
        hotkey: str,
        peer_id: str,
        bootnode_peer_id: str,
        client_peer_id: str,
        stake_amount: int,
        delegate_reward_rate: int,
        bootnode: str = None,
        keypair=None,
    ):
        """Register a subnet node with all required parameters."""
        return self.subnet.register_subnet_node(
            subnet_id,
            hotkey,
            peer_id,
            bootnode_peer_id,
            client_peer_id,
            stake_amount,
            delegate_reward_rate,
            bootnode,
            keypair,
        )

    def activate_subnet_node(self, subnet_id: int, node_id: int, keypair=None):
        """Activate a subnet node."""
        return self.subnet.activate_subnet_node(subnet_id, node_id, keypair)

    def deactivate_subnet_node(self, subnet_id: int, node_id: int, keypair=None):
        """Deactivate a subnet node."""
        return self.subnet.deactivate_subnet_node(subnet_id, node_id, keypair)

    def reactivate_subnet_node(self, subnet_id: int, node_id: int, keypair=None):
        """Reactivate a subnet node."""
        return self.subnet.reactivate_subnet_node(subnet_id, node_id, keypair)

    def cleanup_expired_node(
        self, subnet_id: int, node_id: int, cleanup_type: str, keypair=None
    ):
        """Cleanup expired nodes that failed to activate or reactivate."""
        return self.subnet.cleanup_expired_node(
            subnet_id, node_id, cleanup_type, keypair
        )

    def update_node_delegate_reward_rate(
        self, subnet_id: int, node_id: int, new_delegate_reward_rate: int, keypair=None
    ):
        """Update subnet node delegate reward rate."""
        return self.subnet.update_node_delegate_reward_rate(
            subnet_id, node_id, new_delegate_reward_rate, keypair
        )

    def update_node_coldkey(
        self, subnet_id: int, hotkey: str, new_coldkey: str, keypair=None
    ):
        """Update subnet node coldkey."""
        return self.subnet.update_node_coldkey(subnet_id, hotkey, new_coldkey, keypair)

    def update_node_hotkey(
        self, subnet_id: int, old_hotkey: str, new_hotkey: str, keypair=None
    ):
        """Update subnet node hotkey."""
        return self.subnet.update_node_hotkey(
            subnet_id, old_hotkey, new_hotkey, keypair
        )

    def add_to_node_delegate_stake(
        self, subnet_id: int, node_id: int, amount: int, keypair=None
    ):
        """Add stake to a specific subnet node."""
        return self.subnet.add_to_node_delegate_stake(
            subnet_id, node_id, amount, keypair
        )

    def remove_node_delegate_stake(
        self, subnet_id: int, node_id: int, shares: int, keypair=None
    ):
        """Remove stake from a specific subnet node."""
        return self.subnet.remove_node_delegate_stake(
            subnet_id, node_id, shares, keypair
        )

    def transfer_node_delegate_stake(
        self, subnet_id: int, node_id: int, to_account: str, shares: int, keypair=None
    ):
        """Transfer node delegate stake shares to another account."""
        return self.subnet.transfer_node_delegate_stake(
            subnet_id, node_id, to_account, shares, keypair
        )

    def increase_node_delegate_stake(
        self, subnet_id: int, node_id: int, amount: int, keypair=None
    ):
        """Increase node delegate stake pool."""
        return self.subnet.increase_node_delegate_stake(
            subnet_id, node_id, amount, keypair
        )

    def get_subnet_node_status(self, subnet_id: int, node_id: int):
        """Get detailed status of a specific subnet node."""
        return self.subnet.get_subnet_node_status(subnet_id, node_id)

    def get_subnet_nodes(self, subnet_id: int):
        """Get subnet nodes."""
        return self.subnet.get_subnet_nodes(subnet_id)

    def remove_subnet(self, subnet_id: int, keypair=None):
        """Remove a subnet."""
        return self.subnet.remove_subnet(subnet_id, keypair)

    def remove_subnet_node(self, subnet_id: int, subnet_node_id: int, keypair=None):
        """Remove a subnet node."""
        return self.subnet.remove_subnet_node(subnet_id, subnet_node_id, keypair)

    # Wallet operations
    def add_to_stake(self, request: StakeAddRequest, keypair=None):
        """Add stake."""
        return self.wallet.add_to_stake(request, keypair)

    def remove_stake(self, request: StakeRemoveRequest, keypair=None):
        """Remove stake."""
        return self.wallet.remove_stake(request, keypair)

    def get_account_subnet_stake(self, account: str, subnet_id: int):
        """Get account stake for a subnet."""
        return self.wallet.get_account_subnet_stake(account, subnet_id)

    def get_balance(self, address: str):
        """Get account balance."""
        return self.wallet.get_balance(address)

    def claim_unbondings(self, keypair=None):
        """Claim unbondings."""
        return self.wallet.claim_unbondings(keypair)

    def add_to_delegate_stake(
        self, subnet_id: int, stake_to_be_added: int, keypair=None
    ):
        """Add to delegate stake."""
        return self.wallet.add_to_delegate_stake(subnet_id, stake_to_be_added, keypair)

    def transfer_delegate_stake(
        self,
        from_subnet_id: int,
        to_subnet_id: int,
        delegate_stake_shares_to_be_switched: int,
        keypair=None,
    ):
        """Transfer delegate stake."""
        return self.wallet.transfer_delegate_stake(
            from_subnet_id, to_subnet_id, delegate_stake_shares_to_be_switched, keypair
        )

    def remove_delegate_stake(
        self, subnet_id: int, shares_to_be_removed: int, keypair=None
    ):
        """Remove delegate stake."""
        return self.wallet.remove_delegate_stake(
            subnet_id, shares_to_be_removed, keypair
        )

    def update_coldkey(self, hotkey: str, new_coldkey: str, keypair=None):
        """Update coldkey."""
        return self.wallet.update_coldkey(hotkey, new_coldkey, keypair)

    def update_hotkey(self, old_hotkey: str, new_hotkey: str, keypair=None):
        """Update hotkey."""
        return self.wallet.update_hotkey(old_hotkey, new_hotkey, keypair)

    # Chain operations
    def get_network_stats(self):
        """Get network statistics."""
        return self.chain.get_network_stats()

    def get_current_epoch(self):
        """Get current epoch."""
        return self.chain.get_current_epoch()

    def get_peers(self):
        """Get network peers."""
        return self.chain.get_peers()

    def get_block_info(self, block_number: Optional[int] = None):
        """Get block information."""
        return self.chain.get_block_info(block_number)

    def validate(self, subnet_id: int, data: str, args: str = None, keypair=None):
        """Validate."""
        return self.chain.validate(subnet_id, data, args, keypair)

    def attest(self, subnet_id: int, keypair=None):
        """Attest."""
        return self.chain.attest(subnet_id, keypair)

    def propose(
        self, subnet_id: int, subnet_node_id: int, peer_id: str, data: str, keypair=None
    ):
        """Propose."""
        return self.chain.propose(subnet_id, subnet_node_id, peer_id, data, keypair)

    def vote(
        self,
        subnet_id: int,
        subnet_node_id: int,
        proposal_id: int,
        vote: str,
        keypair=None,
    ):
        """Vote."""
        return self.chain.vote(subnet_id, subnet_node_id, proposal_id, vote, keypair)

    def get_account_info(self, address: str):
        """Get detailed account information."""
        return self.chain.get_account_info(address)

    def get_chain_head(self):
        """Get the current chain head."""
        return self.chain.get_chain_head()

    def get_runtime_version(self):
        """Get the runtime version."""
        return self.chain.get_runtime_version()

    # ===== LEGACY METHODS (for backward compatibility) =====

    def list_subnets(self, active_only: bool = False):
        """Legacy method - use get_subnets_data instead."""
        return self.get_subnets_data(active_only)

    def get_subnet_info(self, subnet_id: int):
        """Legacy method - use get_subnet_data instead."""
        return self.get_subnet_data(subnet_id)

    def add_stake(self, request):
        """Legacy method - use add_to_stake instead."""
        return self.add_to_stake(request)

    def get_stake_info(self, subnet_id: int, hotkey: str):
        """Legacy method - use get_account_subnet_stake instead."""
        return self.get_account_subnet_stake(hotkey, subnet_id)


__all__ = ["HypertensorClient", "SubnetClient", "WalletClient", "ChainClient"]
