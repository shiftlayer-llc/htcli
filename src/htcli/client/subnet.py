#!/usr/bin/env python3
"""
Subnet operations client module.
Handles all subnet-related blockchain operations.
"""

import logging
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

            # Compose the call using Network pallet with official RegistrationSubnetData structure
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="register_subnet",
                call_params={
                    "subnet_data": {
                        "name": request.name,
                        "repo": request.repo,
                        "description": request.description,
                        "misc": request.misc,
                        "churn_limit": request.churn_limit,
                        "min_stake": request.min_stake,
                        "max_stake": request.max_stake,
                        "delegate_stake_percentage": request.delegate_stake_percentage,
                        "registration_queue_epochs": request.registration_queue_epochs,
                        "activation_grace_epochs": request.activation_grace_epochs,
                        "queue_classification_epochs": request.queue_classification_epochs,
                        "included_classification_epochs": request.included_classification_epochs,
                        "max_node_penalties": request.max_node_penalties,
                        "initial_coldkeys": request.initial_coldkeys,
                        "max_registered_nodes": request.max_registered_nodes,
                        "node_removal_system": request.node_removal_system,
                        "key_types": request.key_types,
                    }
                },
            )

            # If keypair provided, submit real transaction
            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                # Return real transaction details
                return SubnetRegisterResponse(
                    success=True,
                    message="Subnet registered successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return SubnetRegisterResponse(
                    success=True,
                    message="Subnet registration call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to register subnet: {str(e)}")
            raise

    def activate_subnet(self, subnet_id: int, key_name: str = None, keypair=None):
        """Activate a subnet using Network.activate_subnet with real transaction submission."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair

                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="activate_subnet",
                call_params={"subnet_id": subnet_id},
            )

            # If keypair provided, submit real transaction
            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                # Return real transaction details
                return SubnetActivateResponse(
                    success=True,
                    message="Subnet activated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return SubnetActivateResponse(
                    success=True,
                    message="Subnet activation call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to activate subnet: {str(e)}")
            raise

    def pause_subnet(self, subnet_id: int, key_name: str = None, keypair=None):
        """Pause a subnet using Network.pause_subnet with real transaction submission."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair

                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="pause_subnet",
                call_params={"subnet_id": subnet_id},
            )

            # If keypair provided, submit real transaction
            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                # Return real transaction details
                return SubnetPauseResponse(
                    success=True,
                    message="Subnet paused successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return SubnetPauseResponse(
                    success=True,
                    message="Subnet pause call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to pause subnet: {str(e)}")
            raise

    def unpause_subnet(self, subnet_id: int, key_name: str = None, keypair=None):
        """Unpause a subnet using Network.unpause_subnet with real transaction submission."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair

                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="unpause_subnet",
                call_params={"subnet_id": subnet_id},
            )

            # If keypair provided, submit real transaction
            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                # Return real transaction details
                return SubnetUnpauseResponse(
                    success=True,
                    message="Subnet unpaused successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return SubnetUnpauseResponse(
                    success=True,
                    message="Subnet unpause call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to unpause subnet: {str(e)}")
            raise

    def get_subnet_data(self, subnet_id: int):
        """Get subnet data using Network storage query with updated structure."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # First check if subnet UID exists by checking various subnet-specific storage
            subnet_exists = False

            # Check if subnet has an owner (indicates it exists)
            owner = self._safe_query_value("SubnetOwner", subnet_id, None)
            if owner:
                subnet_exists = True

            # Check if subnet has delegate stake (indicates it exists)
            delegate_stake = self._safe_query_value(
                "TotalSubnetDelegateStakeBalance", subnet_id, 0
            )
            if delegate_stake > 0:
                subnet_exists = True

            # Check if subnet has node activation interval (indicates it exists)
            activation_interval = self._safe_query_value(
                "SubnetNodeActivationInterval", subnet_id, None
            )
            if activation_interval:
                subnet_exists = True

            if not subnet_exists:
                return SubnetInfoResponse(
                    success=False, message=f"Subnet {subnet_id} not found", data={}
                )

            # Query subnet data from storage (might be empty for new subnets)
            subnet_data = self.substrate.query(
                module="Network", storage_function="SubnetsData", params=[subnet_id]
            )

            # Parse the subnet data - handle both full data and partial data
            raw_data = subnet_data.value if subnet_data else {}

            # Ensure raw_data is a dict
            if raw_data is None:
                raw_data = {}

            # Build comprehensive subnet info based on available data
            parsed_data = {
                "subnet_id": subnet_id,
                "id": (
                    raw_data.get("id", subnet_id)
                    if isinstance(raw_data, dict)
                    else subnet_id
                ),
                "name": (
                    raw_data.get("name", f"Subnet-{subnet_id}")
                    if isinstance(raw_data, dict)
                    else f"Subnet-{subnet_id}"
                ),
                "repo": raw_data.get("repo", "") if isinstance(raw_data, dict) else "",
                "description": (
                    raw_data.get("description", "")
                    if isinstance(raw_data, dict)
                    else ""
                ),
                "misc": raw_data.get("misc", "") if isinstance(raw_data, dict) else "",
                "state": (
                    raw_data.get("state", "Registered")
                    if isinstance(raw_data, dict) and raw_data
                    else "Partial"
                ),
                "start_epoch": (
                    raw_data.get("start_epoch", 0) if isinstance(raw_data, dict) else 0
                ),
                "churn_limit": self._safe_query_value("ChurnDenominator", subnet_id, 0),
                "min_stake": self._safe_query_value(
                    "MinStakeBalance", None, 0
                ),  # Global value
                "max_stake": self._safe_query_value(
                    "MaxStakeBalance", None, 0
                ),  # Global value
                "delegate_stake_percentage": self._safe_query_value(
                    "DelegateStakeRewardsPercentage", None, 0
                ),  # Global value
                "registration_queue_epochs": self._safe_query_value(
                    "SubnetNodeRegistrationEpochs", subnet_id, 0
                ),
                "activation_grace_epochs": 0,  # Not available in current storage
                "queue_classification_epochs": 0,  # Not available in current storage
                "included_classification_epochs": 0,  # Not available in current storage
                "max_node_penalties": self._safe_query_value(
                    "MaxSubnetNodePenalties", subnet_id, 0
                ),
                "initial_coldkeys": [],  # Not available in current storage
                "max_registered_nodes": self._safe_query_value(
                    "MaxRegisteredSubnetNodes", subnet_id, 0
                ),
                "owner": owner or "",
                "registration_epoch": self._safe_query_value(
                    "SubnetRegistrationEpoch", subnet_id, 0
                ),
                "node_removal_system": "",  # Not available in current storage
                "key_types": [],  # Not available in current storage
                "slot_index": 0,  # Not available in current storage
                "penalty_count": self._safe_query_value(
                    "SubnetPenaltyCount", subnet_id, 0
                ),
                "total_nodes": self._safe_query_value("TotalSubnetNodes", subnet_id, 0),
                "total_active_nodes": self._safe_query_value(
                    "TotalActiveSubnetNodes", subnet_id, 0
                ),
                "total_electable_nodes": 0,  # Not available in current storage
                "node_activation_interval": activation_interval or 0,
                "node_registration_epochs": self._safe_query_value(
                    "SubnetNodeRegistrationEpochs", subnet_id, 0
                ),
                "total_delegate_stake_balance": delegate_stake,
                "total_delegate_stake_shares": self._safe_query_value(
                    "TotalSubnetDelegateStakeShares", subnet_id, 0
                ),
                "data_completeness": "full" if raw_data else "partial",
                "raw_data": raw_data,  # Keep raw data for debugging
            }

            return SubnetInfoResponse(
                success=True,
                message="Subnet data retrieved successfully"
                + (
                    " (partial data - subnet exists but not fully registered)"
                    if not raw_data
                    else ""
                ),
                data=parsed_data,
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
                    module="Network", storage_function=storage_function, params=[]
                )
            else:
                # Subnet-specific storage query
                result = self.substrate.query(
                    module="Network",
                    storage_function=storage_function,
                    params=[subnet_id],
                )
            return (
                result.value if result and result.value is not None else default_value
            )
        except Exception as e:
            logger.debug(
                f"Failed to query {storage_function} for subnet {subnet_id}: {e}"
            )
            return default_value

    def get_subnets_data(self, active_only: bool = False):
        """Get all subnets data using storage queries."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Get total subnet count
            total_subnets = self.substrate.query(
                module="Network", storage_function="TotalSubnetUids", params=[]
            )

            total_count = total_subnets.value if total_subnets else 0
            subnets = []

            # Query each subnet
            for subnet_id in range(1, total_count + 1):
                subnet_data = self.substrate.query(
                    module="Network", storage_function="SubnetsData", params=[subnet_id]
                )

                if subnet_data and subnet_data.value:
                    subnets.append({"subnet_id": subnet_id, "data": subnet_data.value})

            return SubnetsListResponse(
                success=True,
                message=f"Retrieved {len(subnets)} subnets",
                data={"subnets": subnets},
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
                call_module="Network",
                call_function="add_subnet_node",
                call_params={
                    "subnet_id": request.subnet_id,
                    "hotkey": request.hotkey,
                    "peer_id": request.peer_id,
                    "bootstrap_peer_id": request.peer_id,  # Use peer_id as bootstrap_peer_id
                    "delegate_reward_rate": request.delegate_reward_rate,
                    "stake_to_be_added": request.stake_to_be_added,
                    "a": str(request.stake_to_be_added),  # Parameter 'a' as string
                    "b": str(request.delegate_reward_rate),  # Parameter 'b' as string
                    "c": str(request.subnet_id),  # Parameter 'c' as string (subnet_id)
                },
            )

            # If keypair provided, submit real transaction
            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                # Return real transaction details
                return NodeAddResponse(
                    success=True,
                    message="Node added successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return NodeAddResponse(
                    success=True,
                    message="Node addition call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to add subnet node: {str(e)}")
            raise

    def activate_subnet_node(
        self,
        subnet_id: int,
        node_id: int,
        keypair=None
    ):
        """Activate a subnet node using Network.activate_subnet_node with real transaction submission."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Prepare call parameters according to official specification
            call_params = {
                "subnet_id": subnet_id,
                "subnet_node_id": node_id,
            }

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="activate_subnet_node",
                call_params=call_params,
            )

            # If keypair provided, submit real transaction
            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                # Return real transaction details
                return NodeAddResponse(
                    success=True,
                    message="Node activated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return NodeAddResponse(
                    success=True,
                    message="Node activation call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to activate subnet node: {str(e)}")
            raise

    def deactivate_subnet_node(
        self,
        subnet_id: int,
        node_id: int,
        keypair=None
    ):
        """Deactivate a subnet node using Network.deactivate_subnet_node with real transaction submission."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Prepare call parameters according to official specification
            call_params = {
                "subnet_id": subnet_id,
                "subnet_node_id": node_id,
            }

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="deactivate_subnet_node",
                call_params=call_params,
            )

            # If keypair provided, submit real transaction
            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                # Return real transaction details
                return NodeAddResponse(
                    success=True,
                    message="Node deactivated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return NodeAddResponse(
                    success=True,
                    message="Node deactivation call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to deactivate subnet node: {str(e)}")
            raise

    def reactivate_subnet_node(
        self,
        subnet_id: int,
        node_id: int,
        keypair=None
    ):
        """Reactivate a subnet node using Network.reactivate_subnet_node with real transaction submission."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Prepare call parameters according to official specification
            call_params = {
                "subnet_id": subnet_id,
                "subnet_node_id": node_id,
            }

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="reactivate_subnet_node",
                call_params=call_params,
            )

            # If keypair provided, submit real transaction
            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                # Return real transaction details
                return NodeAddResponse(
                    success=True,
                    message="Node reactivated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return NodeAddResponse(
                    success=True,
                    message="Node reactivation call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to reactivate subnet node: {str(e)}")
            raise

    def cleanup_expired_node(
        self,
        subnet_id: int,
        node_id: int,
        cleanup_type: str,
        keypair=None
    ):
        """Cleanup expired nodes that failed to activate or reactivate."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Determine the cleanup function based on type
            if cleanup_type == "deactivated":
                call_function = "cleanup_expired_deactivated_node"
            elif cleanup_type == "registered":
                call_function = "cleanup_expired_registered_node"
            else:
                raise ValueError(f"Invalid cleanup type: {cleanup_type}")

            # Prepare call parameters
            call_params = {
                "subnet_id": subnet_id,
                "subnet_node_id": node_id,
            }

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function=call_function,
                call_params=call_params,
            )

            # If keypair provided, submit real transaction
            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                # Return real transaction details
                return NodeAddResponse(
                    success=True,
                    message=f"Expired {cleanup_type} node cleaned up successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return NodeAddResponse(
                    success=True,
                    message=f"Expired {cleanup_type} node cleanup call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to cleanup expired {cleanup_type} node: {str(e)}")
            raise

    def update_node_delegate_reward_rate(
        self,
        subnet_id: int,
        node_id: int,
        new_delegate_reward_rate: int,
        keypair=None
    ):
        """Update subnet node delegate reward rate using Network.update_delegate_reward_rate."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Prepare call parameters according to official specification
            call_params = {
                "subnet_id": subnet_id,
                "subnet_node_id": node_id,
                "new_delegate_reward_rate": new_delegate_reward_rate,
            }

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="update_delegate_reward_rate",
                call_params=call_params,
            )

            # If keypair provided, submit real transaction
            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                # Return real transaction details
                return NodeAddResponse(
                    success=True,
                    message="Node delegate reward rate updated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return NodeAddResponse(
                    success=True,
                    message="Node delegate reward rate update call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to update node delegate reward rate: {str(e)}")
            raise

    def update_node_coldkey(
        self,
        subnet_id: int,
        hotkey: str,
        new_coldkey: str,
        keypair=None
    ):
        """Update subnet node coldkey using Network.update_coldkey."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Prepare call parameters according to official specification
            call_params = {
                "hotkey": hotkey,
                "new_coldkey": new_coldkey,
            }

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="update_coldkey",
                call_params=call_params,
            )

            # If keypair provided, submit real transaction
            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                # Return real transaction details
                return NodeAddResponse(
                    success=True,
                    message="Node coldkey updated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return NodeAddResponse(
                    success=True,
                    message="Node coldkey update call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to update node coldkey: {str(e)}")
            raise

    def update_node_hotkey(
        self,
        subnet_id: int,
        old_hotkey: str,
        new_hotkey: str,
        keypair=None
    ):
        """Update subnet node hotkey using Network.update_hotkey."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Prepare call parameters according to official specification
            call_params = {
                "old_hotkey": old_hotkey,
                "new_hotkey": new_hotkey,
            }

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="update_hotkey",
                call_params=call_params,
            )

            # If keypair provided, submit real transaction
            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                # Return real transaction details
                return NodeAddResponse(
                    success=True,
                    message="Node hotkey updated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return NodeAddResponse(
                    success=True,
                    message="Node hotkey update call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to update node hotkey: {str(e)}")
            raise

    def get_subnet_node_status(self, subnet_id: int, node_id: int):
        """Get detailed status of a specific subnet node."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Get current epoch
            current_epoch = self.substrate.query(
                module="Network",
                storage_function="CurrentEpoch",
            )
            current_epoch_value = current_epoch.value if current_epoch else 0

            # Try to get node from active nodes first
            node_data = self.substrate.query(
                module="Network",
                storage_function="SubnetNodesData",
                params=[subnet_id, node_id],
            )

            if node_data and node_data.value:
                # Node is active
                raw_data = node_data.value
                if not isinstance(raw_data, dict):
                    raw_data = {}

                node_info = {
                    "node_id": node_id,
                    "subnet_id": subnet_id,
                    "classification": "Active",  # Will be refined based on data
                    "hotkey": raw_data.get("hotkey", ""),
                    "peer_id": raw_data.get("peer_id", ""),
                    "stake": raw_data.get("stake", 0),
                    "delegate_reward_rate": raw_data.get("delegate_reward_rate", 0),
                    "registration_epoch": raw_data.get("registration_epoch", 0),
                    "start_epoch": raw_data.get("start_epoch", 0),
                    "current_epoch": current_epoch_value,
                    "attestation_ratio": raw_data.get("attestation_ratio", 0),
                    "penalties": raw_data.get("penalties", 0),
                    "grace_epochs": raw_data.get("grace_epochs", 0),
                    "idle_epochs": raw_data.get("idle_epochs", 0),
                    "status": "Active",
                }

                # Determine classification based on attestation ratio
                attestation_ratio = raw_data.get("attestation_ratio", 0)
                if attestation_ratio >= 66:
                    node_info["classification"] = "Included"
                else:
                    node_info["classification"] = "Idle"

            else:
                # Try to get from registered nodes
                registered_node_data = self.substrate.query(
                    module="Network",
                    storage_function="RegisteredSubnetNodesData",
                    params=[subnet_id, node_id],
                )

                if registered_node_data and registered_node_data.value:
                    # Node is registered but not active
                    raw_data = registered_node_data.value
                    if not isinstance(raw_data, dict):
                        raw_data = {}

                    node_info = {
                        "node_id": node_id,
                        "subnet_id": subnet_id,
                        "classification": "Registered",
                        "hotkey": raw_data.get("hotkey", ""),
                        "peer_id": raw_data.get("peer_id", ""),
                        "stake": raw_data.get("stake", 0),
                        "delegate_reward_rate": raw_data.get("delegate_reward_rate", 0),
                        "registration_epoch": raw_data.get("registration_epoch", 0),
                        "start_epoch": raw_data.get("start_epoch", 0),
                        "current_epoch": current_epoch_value,
                        "attestation_ratio": 0,
                        "penalties": 0,
                        "grace_epochs": raw_data.get("grace_epochs", 0),
                        "idle_epochs": raw_data.get("idle_epochs", 0),
                        "status": "Registered",
                    }
                else:
                    # Node not found
                    return NodeAddResponse(
                        success=False,
                        message=f"Node {node_id} not found in subnet {subnet_id}",
                        data={},
                    )

            return NodeAddResponse(
                success=True,
                message=f"Node {node_id} status retrieved successfully",
                data={"node": node_info},
            )

        except Exception as e:
            logger.error(f"Failed to get subnet node status: {str(e)}")
            raise

    def get_subnet_nodes(self, subnet_id: int):
        """Get subnet nodes using storage queries."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Get total nodes for this subnet
            total_nodes = self.substrate.query(
                module="Network",
                storage_function="TotalSubnetNodes",
                params=[subnet_id],
            )

            total_count = total_nodes.value if total_nodes else 0
            nodes = []

            # Query each node
            for node_id in range(1, total_count + 1):
                node_data = self.substrate.query(
                    module="Network",
                    storage_function="SubnetNodesData",
                    params=[subnet_id, node_id],
                )

                if node_data and node_data.value:
                    nodes.append({"node_id": node_id, "data": node_data.value})

            return NodesListResponse(
                success=True,
                message=f"Retrieved {len(nodes)} nodes for subnet {subnet_id}",
                data={"nodes": nodes},
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
                call_module="Network",
                call_function="remove_subnet",
                call_params={"subnet_id": subnet_id},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return SubnetRemoveResponse(
                    success=True,
                    message="Subnet removed successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return SubnetRemoveResponse(
                    success=True,
                    message="Subnet removal call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
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
                call_module="Network",
                call_function="deactivate_subnet_node",
                call_params={"subnet_id": subnet_id, "subnet_node_id": subnet_node_id},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return NodeDeactivateResponse(
                    success=True,
                    message="Subnet node deactivated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return NodeDeactivateResponse(
                    success=True,
                    message="Subnet node deactivation call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
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
                call_module="Network",
                call_function="remove_subnet_node",
                call_params={"subnet_id": subnet_id, "subnet_node_id": subnet_node_id},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return NodeRemoveResponse(
                    success=True,
                    message="Subnet node removed successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return NodeRemoveResponse(
                    success=True,
                    message="Subnet node removal call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to remove subnet node: {str(e)}")
            raise

    # ============================================================================
    # SUBNET OWNER OPERATIONS
    # ============================================================================

    def owner_update_name(self, subnet_id: int, name: str, key_name: str = None, keypair=None):
        """Update subnet name using Network.owner_update_name."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="owner_update_name",
                call_params={"subnet_id": subnet_id, "value": name},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet name updated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet name update call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to update subnet name: {str(e)}")
            raise

    def owner_update_repo(self, subnet_id: int, repo: str, key_name: str = None, keypair=None):
        """Update subnet repository using Network.owner_update_repo."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="owner_update_repo",
                call_params={"subnet_id": subnet_id, "value": repo},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet repository updated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet repository update call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to update subnet repository: {str(e)}")
            raise

    def owner_update_description(self, subnet_id: int, description: str, key_name: str = None, keypair=None):
        """Update subnet description using Network.owner_update_description."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="owner_update_description",
                call_params={"subnet_id": subnet_id, "value": description},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet description updated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet description update call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to update subnet description: {str(e)}")
            raise

    def transfer_subnet_ownership(self, subnet_id: int, new_owner: str, key_name: str = None, keypair=None):
        """Transfer subnet ownership using Network.transfer_subnet_ownership."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="transfer_subnet_ownership",
                call_params={"subnet_id": subnet_id, "new_owner": new_owner},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return SubnetOwnershipTransferResponse(
                    success=True,
                    message="Subnet ownership transfer initiated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return SubnetOwnershipTransferResponse(
                    success=True,
                    message="Subnet ownership transfer call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to transfer subnet ownership: {str(e)}")
            raise

    def accept_subnet_ownership(self, subnet_id: int, key_name: str = None, keypair=None):
        """Accept subnet ownership using Network.accept_subnet_ownership."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="accept_subnet_ownership",
                call_params={"subnet_id": subnet_id},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return SubnetOwnershipTransferResponse(
                    success=True,
                    message="Subnet ownership accepted successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return SubnetOwnershipTransferResponse(
                    success=True,
                    message="Subnet ownership acceptance call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to accept subnet ownership: {str(e)}")
            raise

    def undo_subnet_ownership_transfer(self, subnet_id: int, key_name: str = None, keypair=None):
        """Undo subnet ownership transfer using Network.transfer_subnet_ownership with zero address."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            # Use zero address to undo transfer
            zero_address = "5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM"

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="transfer_subnet_ownership",
                call_params={"subnet_id": subnet_id, "new_owner": zero_address},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return SubnetOwnershipTransferResponse(
                    success=True,
                    message="Subnet ownership transfer undone successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return SubnetOwnershipTransferResponse(
                    success=True,
                    message="Subnet ownership transfer undo call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to undo subnet ownership transfer: {str(e)}")
            raise

    def owner_remove_subnet_node(self, subnet_id: int, node_id: int, key_name: str = None, keypair=None):
        """Remove a subnet node using Network.owner_remove_subnet_node."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="owner_remove_subnet_node",
                call_params={"subnet_id": subnet_id, "subnet_node_id": node_id},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return NodeRemoveResponse(
                    success=True,
                    message="Subnet node removed successfully by owner",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return NodeRemoveResponse(
                    success=True,
                    message="Subnet node removal call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to remove subnet node: {str(e)}")
            raise

    def owner_update_churn_limit(self, subnet_id: int, churn_limit: int, key_name: str = None, keypair=None):
        """Update churn limit using Network.owner_update_churn_limit."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="owner_update_churn_limit",
                call_params={"subnet_id": subnet_id, "value": churn_limit},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet churn limit updated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet churn limit update call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to update churn limit: {str(e)}")
            raise

    def owner_update_min_stake(self, subnet_id: int, min_stake: int, key_name: str = None, keypair=None):
        """Update minimum stake using Network.owner_update_min_stake."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="owner_update_min_stake",
                call_params={"subnet_id": subnet_id, "value": min_stake},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet minimum stake updated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet minimum stake update call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to update minimum stake: {str(e)}")
            raise

    def owner_update_max_stake(self, subnet_id: int, max_stake: int, key_name: str = None, keypair=None):
        """Update maximum stake using Network.owner_update_max_stake."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="owner_update_max_stake",
                call_params={"subnet_id": subnet_id, "value": max_stake},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet maximum stake updated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet maximum stake update call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to update maximum stake: {str(e)}")
            raise

    def owner_update_registration_epochs(self, subnet_id: int, epochs: int, key_name: str = None, keypair=None):
        """Update registration queue epochs using Network.owner_update_registration_classification_epochs."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="owner_update_registration_classification_epochs",
                call_params={"subnet_id": subnet_id, "value": epochs},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet registration epochs updated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet registration epochs update call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to update registration epochs: {str(e)}")
            raise

    def owner_update_activation_grace_epochs(self, subnet_id: int, epochs: int, key_name: str = None, keypair=None):
        """Update activation grace epochs using Network.owner_update_activation_grace_epochs."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="owner_update_activation_grace_epochs",
                call_params={"subnet_id": subnet_id, "value": epochs},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet activation grace epochs updated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet activation grace epochs update call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to update activation grace epochs: {str(e)}")
            raise

    def owner_update_idle_epochs(self, subnet_id: int, epochs: int, key_name: str = None, keypair=None):
        """Update idle classification epochs using Network.owner_update_idle_classification_epochs."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="owner_update_idle_classification_epochs",
                call_params={"subnet_id": subnet_id, "value": epochs},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet idle classification epochs updated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet idle classification epochs update call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to update idle classification epochs: {str(e)}")
            raise

    def owner_update_included_epochs(self, subnet_id: int, epochs: int, key_name: str = None, keypair=None):
        """Update included classification epochs using Network.owner_update_included_classification_epochs."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="owner_update_included_classification_epochs",
                call_params={"subnet_id": subnet_id, "value": epochs},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet included classification epochs updated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet included classification epochs update call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to update included classification epochs: {str(e)}")
            raise

    def owner_update_max_penalties(self, subnet_id: int, max_penalties: int, key_name: str = None, keypair=None):
        """Update maximum node penalties using Network.owner_max_node_penalties."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="owner_max_node_penalties",
                call_params={"subnet_id": subnet_id, "value": max_penalties},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet maximum node penalties updated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Subnet maximum node penalties update call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to update maximum node penalties: {str(e)}")
            raise

    def owner_add_initial_coldkeys(self, subnet_id: int, coldkeys: list, key_name: str = None, keypair=None):
        """Add initial coldkeys using Network.owner_add_initial_coldkeys."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="owner_add_initial_coldkeys",
                call_params={"subnet_id": subnet_id, "coldkeys": coldkeys},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Initial coldkeys added successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Initial coldkeys addition call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to add initial coldkeys: {str(e)}")
            raise

    def owner_remove_initial_coldkeys(self, subnet_id: int, coldkeys: list, key_name: str = None, keypair=None):
        """Remove initial coldkeys using Network.owner_remove_initial_coldkeys."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # TODO: Get password from user or config
                password = "default_password_12345"  # This should be improved
                keypair = load_keypair(key_name, password)

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="owner_remove_initial_coldkeys",
                call_params={"subnet_id": subnet_id, "coldkeys": coldkeys},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Initial coldkeys removed successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return SubnetOwnerUpdateResponse(
                    success=True,
                    message="Initial coldkeys removal call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to remove initial coldkeys: {str(e)}")
            raise
