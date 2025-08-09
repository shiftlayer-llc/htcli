#!/usr/bin/env python3
"""
Subnet operations client module.
Handles all subnet-related blockchain operations.
"""

import logging
from typing import Optional
from substrateinterface import SubstrateInterface
from ..models.requests import SubnetRegisterRequest, SubnetNodeAddRequest
from ..models.responses import *

logger = logging.getLogger(__name__)

class SubnetClient:
    """Client for subnet operations."""

    def __init__(self, substrate: SubstrateInterface):
        self.substrate = substrate

    def register_subnet(self, request: SubnetRegisterRequest, keypair=None):
        """Register a new subnet using Network.register_subnet with real transaction submission."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module='Network',
                call_function='register_subnet',
                call_params={
                    'subnet_data': {
                        'path': request.path,
                        'memory_mb': request.memory_mb,
                        'registration_blocks': request.registration_blocks,
                        'entry_interval': request.entry_interval,
                        'max_node_registration_epochs': request.max_node_registration_epochs,
                        'node_registration_interval': request.node_registration_interval,
                        'node_activation_interval': request.node_activation_interval,
                        'node_queue_period': request.node_queue_period,
                        'max_node_penalties': request.max_node_penalties,
                        'coldkey_whitelist': request.coldkey_whitelist
                    }
                }
            )

            # If keypair provided, submit real transaction
            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data,
                    keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic,
                    wait_for_inclusion=True
                )

                # Return real transaction details
                return SubnetRegisterResponse(
                    success=True,
                    message="Subnet registered successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={'receipt': receipt}
                )
            else:
                # Return composed call data for manual submission
                return SubnetRegisterResponse(
                    success=True,
                    message="Subnet registration call composed successfully",
                    transaction_hash="0x" + "0" * 64,  # Mock hash
                    block_number=None,
                    data={'call_data': call_data}
                )
        except Exception as e:
            logger.error(f"Failed to register subnet: {str(e)}")
            raise

    def activate_subnet(self, subnet_id: int, keypair=None):
        """Activate a subnet using Network.activate_subnet with real transaction submission."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module='Network',
                call_function='activate_subnet',
                call_params={'subnet_id': subnet_id}
            )

            # If keypair provided, submit real transaction
            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data,
                    keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic,
                    wait_for_inclusion=True
                )

                # Return real transaction details
                return SubnetActivateResponse(
                    success=True,
                    message="Subnet activated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={'receipt': receipt}
                )
            else:
                # Return composed call data for manual submission
                return SubnetActivateResponse(
                    success=True,
                    message="Subnet activation call composed successfully",
                    transaction_hash="0x" + "0" * 64,  # Mock hash
                    block_number=None,
                    data={'call_data': call_data}
                )
        except Exception as e:
            logger.error(f"Failed to activate subnet: {str(e)}")
            raise

    def get_subnet_data(self, subnet_id: int):
        """Get subnet data using Network storage query with updated structure."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # First check if subnet UID exists by checking various subnet-specific storage
            subnet_exists = False
            
            # Check if subnet has an owner (indicates it exists)
            owner = self._safe_query_value('SubnetOwner', subnet_id, None)
            if owner:
                subnet_exists = True
            
            # Check if subnet has delegate stake (indicates it exists)
            delegate_stake = self._safe_query_value('TotalSubnetDelegateStakeBalance', subnet_id, 0)
            if delegate_stake > 0:
                subnet_exists = True
            
            # Check if subnet has node activation interval (indicates it exists)
            activation_interval = self._safe_query_value('SubnetNodeActivationInterval', subnet_id, None)
            if activation_interval:
                subnet_exists = True

            if not subnet_exists:
                return SubnetInfoResponse(
                    success=False,
                    message=f"Subnet {subnet_id} not found",
                    data={}
                )

            # Query subnet data from storage (might be empty for new subnets)
            subnet_data = self.substrate.query(
                module='Network',
                storage_function='SubnetsData',
                params=[subnet_id]
            )

            # Parse the subnet data - handle both full data and partial data
            raw_data = subnet_data.value if subnet_data else {}
            
            # Ensure raw_data is a dict
            if raw_data is None:
                raw_data = {}
            
            # Build comprehensive subnet info based on available data
            parsed_data = {
                'subnet_id': subnet_id,
                'id': raw_data.get('id', subnet_id) if isinstance(raw_data, dict) else subnet_id,
                'name': raw_data.get('name', f'Subnet-{subnet_id}') if isinstance(raw_data, dict) else f'Subnet-{subnet_id}',
                'repo': raw_data.get('repo', '') if isinstance(raw_data, dict) else '',
                'description': raw_data.get('description', '') if isinstance(raw_data, dict) else '',
                'misc': raw_data.get('misc', '') if isinstance(raw_data, dict) else '',
                'state': raw_data.get('state', 'Registered') if isinstance(raw_data, dict) and raw_data else 'Partial',
                'start_epoch': raw_data.get('start_epoch', 0) if isinstance(raw_data, dict) else 0,
                'churn_limit': self._safe_query_value('ChurnDenominator', subnet_id, 0),
                'min_stake': self._safe_query_value('MinStakeBalance', None, 0),  # Global value
                'max_stake': self._safe_query_value('MaxStakeBalance', None, 0),  # Global value
                'delegate_stake_percentage': self._safe_query_value('DelegateStakeRewardsPercentage', None, 0),  # Global value
                'registration_queue_epochs': self._safe_query_value('SubnetNodeRegistrationEpochs', subnet_id, 0),
                'activation_grace_epochs': 0,  # Not available in current storage
                'queue_classification_epochs': 0,  # Not available in current storage
                'included_classification_epochs': 0,  # Not available in current storage
                'max_node_penalties': self._safe_query_value('MaxSubnetNodePenalties', subnet_id, 0),
                'initial_coldkeys': [],  # Not available in current storage
                'max_registered_nodes': self._safe_query_value('MaxRegisteredSubnetNodes', subnet_id, 0),
                'owner': owner or '',
                'registration_epoch': self._safe_query_value('SubnetRegistrationEpoch', subnet_id, 0),
                'node_removal_system': '',  # Not available in current storage
                'key_types': [],  # Not available in current storage
                'slot_index': 0,  # Not available in current storage
                'penalty_count': self._safe_query_value('SubnetPenaltyCount', subnet_id, 0),
                'total_nodes': self._safe_query_value('TotalSubnetNodes', subnet_id, 0),
                'total_active_nodes': self._safe_query_value('TotalActiveSubnetNodes', subnet_id, 0),
                'total_electable_nodes': 0,  # Not available in current storage
                'node_activation_interval': activation_interval or 0,
                'node_registration_epochs': self._safe_query_value('SubnetNodeRegistrationEpochs', subnet_id, 0),
                'total_delegate_stake_balance': delegate_stake,
                'total_delegate_stake_shares': self._safe_query_value('TotalSubnetDelegateStakeShares', subnet_id, 0),
                'data_completeness': 'full' if raw_data else 'partial',
                'raw_data': raw_data  # Keep raw data for debugging
            }

            return SubnetInfoResponse(
                success=True,
                message="Subnet data retrieved successfully" + (" (partial data - subnet exists but not fully registered)" if not raw_data else ""),
                data=parsed_data
            )
        except Exception as e:
            logger.error(f"Failed to get subnet data: {str(e)}")
            raise

    def _safe_query_value(self, storage_function: str, subnet_id, default_value):
        """Safely query a storage value with fallback to default."""
        try:
            if subnet_id is None:
                # Global storage query (no parameters)
                result = self.substrate.query(
                    module='Network',
                    storage_function=storage_function,
                    params=[]
                )
            else:
                # Subnet-specific storage query
                result = self.substrate.query(
                    module='Network',
                    storage_function=storage_function,
                    params=[subnet_id]
                )
            return result.value if result and result.value is not None else default_value
        except Exception as e:
            logger.debug(f"Failed to query {storage_function} for subnet {subnet_id}: {e}")
            return default_value

    def get_subnets_data(self, active_only: bool = False):
        """Get all subnets data using storage queries."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Get total subnet count
            total_subnets = self.substrate.query(
                module='Network',
                storage_function='TotalSubnetUids',
                params=[]
            )

            total_count = total_subnets.value if total_subnets else 0
            subnets = []

            # Query each subnet
            for subnet_id in range(1, total_count + 1):
                subnet_data = self.substrate.query(
                    module='Network',
                    storage_function='SubnetsData',
                    params=[subnet_id]
                )

                if subnet_data and subnet_data.value:
                    subnets.append({
                        'subnet_id': subnet_id,
                        'data': subnet_data.value
                    })

            return SubnetsListResponse(
                success=True,
                message=f"Retrieved {len(subnets)} subnets",
                data={'subnets': subnets}
            )
        except Exception as e:
            logger.error(f"Failed to get subnets data: {str(e)}")
            raise

    def add_subnet_node(self, request: SubnetNodeAddRequest, keypair=None):
        """Add a node to a subnet using Network.add_subnet_node with real transaction submission."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module='Network',
                call_function='add_subnet_node',
                call_params={
                    'subnet_id': request.subnet_id,
                    'hotkey': request.hotkey,
                    'peer_id': request.peer_id,
                    'bootstrap_peer_id': request.peer_id,  # Use peer_id as bootstrap_peer_id
                    'delegate_reward_rate': request.delegate_reward_rate,
                    'stake_to_be_added': request.stake_to_be_added,
                    'a': str(request.stake_to_be_added),  # Parameter 'a' as string
                    'b': str(request.delegate_reward_rate),  # Parameter 'b' as string
                    'c': str(request.subnet_id)  # Parameter 'c' as string (subnet_id)
                }
            )

            # If keypair provided, submit real transaction
            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data,
                    keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic,
                    wait_for_inclusion=True
                )

                # Return real transaction details
                return NodeAddResponse(
                    success=True,
                    message="Node added successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={'receipt': receipt}
                )
            else:
                # Return composed call data for manual submission
                return NodeAddResponse(
                    success=True,
                    message="Node addition call composed successfully",
                    transaction_hash="0x" + "0" * 64,  # Mock hash
                    block_number=None,
                    data={'call_data': call_data}
                )
        except Exception as e:
            logger.error(f"Failed to add subnet node: {str(e)}")
            raise

    def get_subnet_nodes(self, subnet_id: int):
        """Get subnet nodes using storage queries."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Get total nodes for this subnet
            total_nodes = self.substrate.query(
                module='Network',
                storage_function='TotalSubnetNodes',
                params=[subnet_id]
            )

            total_count = total_nodes.value if total_nodes else 0
            nodes = []

            # Query each node
            for node_id in range(1, total_count + 1):
                node_data = self.substrate.query(
                    module='Network',
                    storage_function='SubnetNodesData',
                    params=[subnet_id, node_id]
                )

                if node_data and node_data.value:
                    nodes.append({
                        'node_id': node_id,
                        'data': node_data.value
                    })

            return NodesListResponse(
                success=True,
                message=f"Retrieved {len(nodes)} nodes for subnet {subnet_id}",
                data={'nodes': nodes}
            )
        except Exception as e:
            logger.error(f"Failed to get subnet nodes: {str(e)}")
            raise

    # Additional subnet operations based on discovered Network pallet methods
    def remove_subnet(self, subnet_id: int, keypair=None):
        """Remove a subnet using Network.remove_subnet."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            call_data = self.substrate.compose_call(
                call_module='Network',
                call_function='remove_subnet',
                call_params={'subnet_id': subnet_id}
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data,
                    keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic,
                    wait_for_inclusion=True
                )

                return SubnetRemoveResponse(
                    success=True,
                    message="Subnet removed successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={'receipt': receipt}
                )
            else:
                return SubnetRemoveResponse(
                    success=True,
                    message="Subnet removal call composed successfully",
                    transaction_hash="0x" + "0" * 64,
                    block_number=None,
                    data={'call_data': call_data}
                )
        except Exception as e:
            logger.error(f"Failed to remove subnet: {str(e)}")
            raise

    def deactivate_subnet_node(self, subnet_id: int, subnet_node_id: int, keypair=None):
        """Deactivate a subnet node using Network.deactivate_subnet_node."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            call_data = self.substrate.compose_call(
                call_module='Network',
                call_function='deactivate_subnet_node',
                call_params={
                    'subnet_id': subnet_id,
                    'subnet_node_id': subnet_node_id
                }
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data,
                    keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic,
                    wait_for_inclusion=True
                )

                return NodeDeactivateResponse(
                    success=True,
                    message="Subnet node deactivated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={'receipt': receipt}
                )
            else:
                return NodeDeactivateResponse(
                    success=True,
                    message="Subnet node deactivation call composed successfully",
                    transaction_hash="0x" + "0" * 64,
                    block_number=None,
                    data={'call_data': call_data}
                )
        except Exception as e:
            logger.error(f"Failed to deactivate subnet node: {str(e)}")
            raise

    def remove_subnet_node(self, subnet_id: int, subnet_node_id: int, keypair=None):
        """Remove a subnet node using Network.remove_subnet_node."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            call_data = self.substrate.compose_call(
                call_module='Network',
                call_function='remove_subnet_node',
                call_params={
                    'subnet_id': subnet_id,
                    'subnet_node_id': subnet_node_id
                }
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data,
                    keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic,
                    wait_for_inclusion=True
                )

                return NodeRemoveResponse(
                    success=True,
                    message="Subnet node removed successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={'receipt': receipt}
                )
            else:
                return NodeRemoveResponse(
                    success=True,
                    message="Subnet node removal call composed successfully",
                    transaction_hash="0x" + "0" * 64,
                    block_number=None,
                    data={'call_data': call_data}
                )
        except Exception as e:
            logger.error(f"Failed to remove subnet node: {str(e)}")
            raise
