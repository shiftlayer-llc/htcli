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
        """Get subnet data using Network storage query."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Query subnet data from storage
            subnet_data = self.substrate.query(
                module='Network',
                storage_function='SubnetsData',
                params=[subnet_id]
            )

            return SubnetInfoResponse(
                success=True,
                message="Subnet data retrieved successfully",
                data={
                    'subnet_id': subnet_id,
                    'subnet_data': subnet_data.value if subnet_data else None
                }
            )
        except Exception as e:
            logger.error(f"Failed to get subnet data: {str(e)}")
            raise

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
