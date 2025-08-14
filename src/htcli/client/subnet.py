#!/usr/bin/env python3
"""
Subnet operations client module.
Handles all subnet-related blockchain operations.
"""

import logging
from substrateinterface import SubstrateInterface
from ..models.requests import SubnetRegisterRequest, SubnetNodeAddRequest
from ..models.responses import *
from ..utils.password import get_secure_password

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

                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair for subnet activation",
                    allow_default=True
                )
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

                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair for subnet pause",
                    allow_default=True
                )
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

                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair for subnet unpause",
                    allow_default=True
                )
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

    def add_to_node_delegate_stake(
        self,
        subnet_id: int,
        node_id: int,
        amount: int,
        keypair=None
    ):
        """Add stake to a specific subnet node using Network.add_to_node_delegate_stake."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Prepare call parameters according to official specification
            call_params = {
                "subnet_id": subnet_id,
                "subnet_node_id": node_id,
                "node_delegate_stake_to_be_added": amount,
            }

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="add_to_node_delegate_stake",
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
                    message="Node delegate stake added successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return NodeAddResponse(
                    success=True,
                    message="Node delegate stake addition call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to add node delegate stake: {str(e)}")
            raise

    def remove_node_delegate_stake(
        self,
        subnet_id: int,
        node_id: int,
        shares: int,
        keypair=None
    ):
        """Remove stake from a specific subnet node using Network.remove_node_delegate_stake."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Prepare call parameters according to official specification
            call_params = {
                "subnet_id": subnet_id,
                "subnet_node_id": node_id,
                "node_delegate_stake_shares_to_be_removed": shares,
            }

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="remove_node_delegate_stake",
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
                    message="Node delegate stake removed successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return NodeAddResponse(
                    success=True,
                    message="Node delegate stake removal call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to remove node delegate stake: {str(e)}")
            raise

    def transfer_node_delegate_stake(
        self,
        subnet_id: int,
        node_id: int,
        to_account: str,
        shares: int,
        keypair=None
    ):
        """Transfer node delegate stake shares to another account using Network.transfer_node_delegate_stake."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Prepare call parameters according to official specification
            call_params = {
                "subnet_id": subnet_id,
                "subnet_node_id": node_id,
                "to_account_id": to_account,
                "node_delegate_stake_shares_to_transfer": shares,
            }

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="transfer_node_delegate_stake",
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
                    message="Node delegate stake transferred successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return NodeAddResponse(
                    success=True,
                    message="Node delegate stake transfer call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to transfer node delegate stake: {str(e)}")
            raise

    def increase_node_delegate_stake(
        self,
        subnet_id: int,
        node_id: int,
        amount: int,
        keypair=None
    ):
        """Increase node delegate stake pool using Network.increase_node_delegate_stake."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Prepare call parameters according to official specification
            call_params = {
                "subnet_id": subnet_id,
                "subnet_node_id": node_id,
                "amount": amount,
            }

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="increase_node_delegate_stake",
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
                    message="Node delegate stake pool increased successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return NodeAddResponse(
                    success=True,
                    message="Node delegate stake pool increase call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to increase node delegate stake pool: {str(e)}")
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
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair for subnet owner update",
                    allow_default=True
                )
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
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair for subnet owner update",
                    allow_default=True
                )
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
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair for subnet owner update",
                    allow_default=True
                )
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
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair",
                    allow_default=True
                )
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
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair",
                    allow_default=True
                )
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
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair",
                    allow_default=True
                )
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
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair",
                    allow_default=True
                )
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
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair for subnet owner update",
                    allow_default=True
                )
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
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair for subnet owner update",
                    allow_default=True
                )
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
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair for subnet owner update",
                    allow_default=True
                )
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
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair for subnet owner update",
                    allow_default=True
                )
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
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair for subnet owner update",
                    allow_default=True
                )
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
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair for subnet owner update",
                    allow_default=True
                )
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
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair for subnet owner update",
                    allow_default=True
                )
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
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair",
                    allow_default=True
                )
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
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair",
                    allow_default=True
                )
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
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair",
                    allow_default=True
                )
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

    # ============================================================================
    # Staking Information Methods
    # ============================================================================

    def get_node_staking_info(self, subnet_id: int, node_id: int, user_address: str = None):
        """Get comprehensive staking information for a specific node."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Get node delegate stake balance
            node_delegate_stake = self._safe_query_value(
                "NodeDelegateStakeBalance", subnet_id, node_id, 0
            )

            # Get node delegate reward rate
            node_reward_rate = self._safe_query_value(
                "NodeDelegateRewardRate", subnet_id, node_id, 0
            )

            # Get user's node delegate stake shares (if address provided)
            user_node_shares = 0
            if user_address:
                user_node_shares = self._safe_query_value(
                    "NodeDelegateStakeShares", subnet_id, node_id, user_address, 0
                )

            # Get node performance data
            node_performance = self._safe_query_value(
                "SubnetNodePerformance", subnet_id, node_id, {}
            )

            # Get node classification
            node_classification = self._safe_query_value(
                "SubnetNodeClassification", subnet_id, node_id, {}
            )

            # Get node penalties
            node_penalties = self._safe_query_value(
                "SubnetNodePenalties", subnet_id, node_id, 0
            )

            # Calculate user's stake value (if shares available)
            user_stake_value = 0
            if user_node_shares > 0 and node_delegate_stake > 0:
                # Calculate proportional stake value
                user_stake_value = (user_node_shares / node_delegate_stake) * node_delegate_stake

            staking_info = {
                "subnet_id": subnet_id,
                "node_id": node_id,
                "node_delegate_stake": node_delegate_stake,
                "node_reward_rate": node_reward_rate,
                "user_node_shares": user_node_shares,
                "user_stake_value": user_stake_value,
                "node_performance": node_performance,
                "node_classification": node_classification,
                "node_penalties": node_penalties,
                "total_delegators": self._get_node_delegator_count(subnet_id, node_id),
                "estimated_rewards": self._calculate_node_rewards(node_delegate_stake, node_reward_rate),
            }

            return StakeInfoResponse(
                success=True,
                message="Node staking information retrieved successfully",
                data=staking_info
            )

        except Exception as e:
            logger.error(f"Failed to get node staking info: {str(e)}")
            return StakeInfoResponse(
                success=False,
                message=f"Failed to get node staking info: {str(e)}",
                data={}
            )

    def get_subnet_staking_info(self, subnet_id: int, user_address: str = None):
        """Get comprehensive staking information for a subnet."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Get subnet delegate stake balance
            subnet_delegate_stake = self._safe_query_value(
                "TotalSubnetDelegateStakeBalance", subnet_id, 0
            )

            # Get subnet delegate reward rate
            subnet_reward_rate = self._safe_query_value(
                "SubnetDelegateRewardRate", subnet_id, 0
            )

            # Get user's subnet delegate stake shares (if address provided)
            user_subnet_shares = 0
            if user_address:
                user_subnet_shares = self._safe_query_value(
                    "SubnetDelegateStakeShares", subnet_id, user_address, 0
                )

            # Get subnet performance data
            subnet_performance = self._safe_query_value(
                "SubnetPerformance", subnet_id, {}
            )

            # Get subnet statistics
            subnet_stats = self._safe_query_value(
                "SubnetStatistics", subnet_id, {}
            )

            # Calculate user's stake value (if shares available)
            user_stake_value = 0
            if user_subnet_shares > 0 and subnet_delegate_stake > 0:
                # Calculate proportional stake value
                user_stake_value = (user_subnet_shares / subnet_delegate_stake) * subnet_delegate_stake

            # Get subnet nodes for additional context
            subnet_nodes = self._get_subnet_nodes(subnet_id)

            staking_info = {
                "subnet_id": subnet_id,
                "subnet_delegate_stake": subnet_delegate_stake,
                "subnet_reward_rate": subnet_reward_rate,
                "user_subnet_shares": user_subnet_shares,
                "user_stake_value": user_stake_value,
                "subnet_performance": subnet_performance,
                "subnet_stats": subnet_stats,
                "total_delegators": self._get_subnet_delegator_count(subnet_id),
                "total_nodes": len(subnet_nodes),
                "active_nodes": len([n for n in subnet_nodes if n.get("classification", {}).get("class") == "Validator"]),
                "estimated_rewards": self._calculate_subnet_rewards(subnet_delegate_stake, subnet_reward_rate),
                "nodes": subnet_nodes,
            }

            return StakeInfoResponse(
                success=True,
                message="Subnet staking information retrieved successfully",
                data=staking_info
            )

        except Exception as e:
            logger.error(f"Failed to get subnet staking info: {str(e)}")
            return StakeInfoResponse(
                success=False,
                message=f"Failed to get subnet staking info: {str(e)}",
                data={}
            )

    def get_general_staking_info(self, user_address: str = None):
        """Get general staking information across all subnets."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Get all subnets
            subnets_response = self.get_subnets_data()
            if not subnets_response.success:
                return StakeInfoResponse(
                    success=False,
                    message="Failed to retrieve subnets data",
                    data={}
                )

            subnets = subnets_response.data.get("subnets", [])
            
            # Collect staking information for all subnets
            all_staking_info = []
            total_user_stake = 0
            total_network_stake = 0

            for subnet in subnets:
                subnet_id = subnet.get("subnet_id")
                if subnet_id:
                    # Get subnet staking info
                    subnet_staking = self.get_subnet_staking_info(subnet_id, user_address)
                    if subnet_staking.success:
                        subnet_data = subnet_staking.data
                        all_staking_info.append(subnet_data)
                        
                        # Accumulate totals
                        total_network_stake += subnet_data.get("subnet_delegate_stake", 0)
                        if user_address:
                            total_user_stake += subnet_data.get("user_stake_value", 0)

            # Get network-wide statistics
            network_stats = {
                "total_subnets": len(subnets),
                "total_network_stake": total_network_stake,
                "total_user_stake": total_user_stake,
                "user_stake_percentage": (total_user_stake / total_network_stake * 100) if total_network_stake > 0 else 0,
                "average_reward_rate": self._calculate_average_reward_rate(all_staking_info),
                "top_performing_subnets": self._get_top_performing_subnets(all_staking_info),
                "recommendations": self._generate_staking_recommendations(all_staking_info, user_address),
            }

            general_info = {
                "network_stats": network_stats,
                "subnet_staking": all_staking_info,
                "user_address": user_address,
            }

            return StakeInfoResponse(
                success=True,
                message="General staking information retrieved successfully",
                data=general_info
            )

        except Exception as e:
            logger.error(f"Failed to get general staking info: {str(e)}")
            return StakeInfoResponse(
                success=False,
                message=f"Failed to get general staking info: {str(e)}",
                data={}
            )

    # ============================================================================
    # Helper Methods for Staking Information
    # ============================================================================

    def _get_node_delegator_count(self, subnet_id: int, node_id: int) -> int:
        """Get the number of delegators for a specific node."""
        try:
            # This would query the actual delegator count from the blockchain
            # For now, return a placeholder value
            return 0
        except Exception:
            return 0

    def _get_subnet_delegator_count(self, subnet_id: int) -> int:
        """Get the number of delegators for a subnet."""
        try:
            # This would query the actual delegator count from the blockchain
            # For now, return a placeholder value
            return 0
        except Exception:
            return 0

    def _get_subnet_nodes(self, subnet_id: int) -> list:
        """Get all nodes for a subnet."""
        try:
            # Query subnet nodes from storage
            nodes_data = self.substrate.query(
                module="Network", 
                storage_function="SubnetNodesData", 
                params=[subnet_id]
            )
            
            if nodes_data and nodes_data.value:
                return nodes_data.value
            return []
        except Exception:
            return []

    def _calculate_node_rewards(self, stake_amount: int, reward_rate: int) -> float:
        """Calculate estimated rewards for a node."""
        try:
            # Simple reward calculation (this would be more complex in reality)
            if stake_amount > 0 and reward_rate > 0:
                return (stake_amount * reward_rate) / 1000000  # Assuming 6 decimal precision
            return 0.0
        except Exception:
            return 0.0

    def _calculate_subnet_rewards(self, stake_amount: int, reward_rate: int) -> float:
        """Calculate estimated rewards for a subnet."""
        try:
            # Simple reward calculation (this would be more complex in reality)
            if stake_amount > 0 and reward_rate > 0:
                return (stake_amount * reward_rate) / 1000000  # Assuming 6 decimal precision
            return 0.0
        except Exception:
            return 0.0

    def _calculate_average_reward_rate(self, staking_info: list) -> float:
        """Calculate average reward rate across subnets."""
        try:
            if not staking_info:
                return 0.0
            
            total_rate = sum(info.get("subnet_reward_rate", 0) for info in staking_info)
            return total_rate / len(staking_info)
        except Exception:
            return 0.0

    def _get_top_performing_subnets(self, staking_info: list, limit: int = 5) -> list:
        """Get top performing subnets based on reward rates."""
        try:
            # Sort by reward rate and return top performers
            sorted_subnets = sorted(
                staking_info, 
                key=lambda x: x.get("subnet_reward_rate", 0), 
                reverse=True
            )
            return sorted_subnets[:limit]
        except Exception:
            return []

    def _generate_staking_recommendations(self, staking_info: list, user_address: str = None) -> list:
        """Generate staking recommendations based on current data."""
        try:
            recommendations = []
            
            if not staking_info:
                recommendations.append("No subnets available for staking")
                return recommendations

            # Find subnets with high reward rates
            high_reward_subnets = [
                info for info in staking_info 
                if info.get("subnet_reward_rate", 0) > 5000  # Example threshold
            ]
            
            if high_reward_subnets:
                recommendations.append(f"Consider staking in {len(high_reward_subnets)} high-reward subnets")

            # Find subnets with low user stake (diversification opportunity)
            if user_address:
                low_stake_subnets = [
                    info for info in staking_info 
                    if info.get("user_stake_value", 0) < 1000  # Example threshold
                ]
                
                if low_stake_subnets:
                    recommendations.append(f"Diversify by staking in {len(low_stake_subnets)} additional subnets")

            # Performance-based recommendations
            active_subnets = [
                info for info in staking_info 
                if info.get("active_nodes", 0) > 0
            ]
            
            if active_subnets:
                recommendations.append(f"Focus on {len(active_subnets)} subnets with active nodes")

            if not recommendations:
                recommendations.append("Monitor subnets for staking opportunities")

            return recommendations

        except Exception:
            return ["Unable to generate recommendations"]

    # ============================================================================
    # Automatic Stake Removal Methods
    # ============================================================================

    def remove_node_stake_automatically(self, subnet_id: int, node_id: int, key_name: str = None, keypair=None):
        """Automatically remove all stake from a node after node removal."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair for automatic stake removal",
                    allow_default=True
                )
                keypair = load_keypair(key_name, password)

            # First, get the current stake amount for this node
            node_stake_info = self.get_node_staking_info(subnet_id, node_id)
            if not node_stake_info.success:
                return StakeRemoveResponse(
                    success=False,
                    message="Failed to get node stake information for automatic removal",
                    data={}
                )

            stake_data = node_stake_info.data
            user_node_shares = stake_data.get("user_node_shares", 0)

            if user_node_shares <= 0:
                return StakeRemoveResponse(
                    success=True,
                    message="No stake to remove from this node",
                    data={"removed_amount": 0, "shares_removed": 0}
                )

            # Remove all stake shares from the node
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="remove_node_delegate_stake",
                call_params={
                    "subnet_id": subnet_id,
                    "subnet_node_id": node_id,
                    "node_delegate_stake_shares_to_be_removed": user_node_shares
                }
            )

            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                # Calculate the estimated stake value that was removed
                node_delegate_stake = stake_data.get("node_delegate_stake", 0)
                estimated_removed_value = 0
                if node_delegate_stake > 0:
                    estimated_removed_value = (user_node_shares / node_delegate_stake) * node_delegate_stake

                return StakeRemoveResponse(
                    success=True,
                    message="Automatic stake removal completed successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={
                        "receipt": receipt,
                        "removed_amount": estimated_removed_value,
                        "shares_removed": user_node_shares,
                        "subnet_id": subnet_id,
                        "node_id": node_id,
                        "unbonding_started": True
                    }
                )
            else:
                # Return composed call data for manual submission
                return StakeRemoveResponse(
                    success=True,
                    message="Automatic stake removal call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={
                        "call_data": call_data,
                        "removed_amount": 0,
                        "shares_removed": user_node_shares,
                        "subnet_id": subnet_id,
                        "node_id": node_id,
                        "unbonding_started": False
                    }
                )

        except Exception as e:
            logger.error(f"Failed to remove node stake automatically: {str(e)}")
            return StakeRemoveResponse(
                success=False,
                message=f"Failed to remove node stake automatically: {str(e)}",
                data={}
            )

    def remove_subnet_stake_automatically(self, subnet_id: int, key_name: str = None, keypair=None):
        """Automatically remove all stake from a subnet after subnet removal."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Load keypair if key_name provided
            if key_name and not keypair:
                from ..utils.crypto import load_keypair
                # Get secure password for keypair
                password = get_secure_password(
                    key_name,
                    prompt_message="Enter password to unlock keypair for automatic subnet stake removal",
                    allow_default=True
                )
                keypair = load_keypair(key_name, password)

            # First, get the current stake amount for this subnet
            subnet_stake_info = self.get_subnet_staking_info(subnet_id)
            if not subnet_stake_info.success:
                return StakeRemoveResponse(
                    success=False,
                    message="Failed to get subnet stake information for automatic removal",
                    data={}
                )

            stake_data = subnet_stake_info.data
            user_subnet_shares = stake_data.get("user_subnet_shares", 0)

            if user_subnet_shares <= 0:
                return StakeRemoveResponse(
                    success=True,
                    message="No stake to remove from this subnet",
                    data={"removed_amount": 0, "shares_removed": 0}
                )

            # Remove all stake shares from the subnet
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="remove_delegate_stake",
                call_params={
                    "subnet_id": subnet_id,
                    "shares_to_be_removed": user_subnet_shares
                }
            )

            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                # Calculate the estimated stake value that was removed
                subnet_delegate_stake = stake_data.get("subnet_delegate_stake", 0)
                estimated_removed_value = 0
                if subnet_delegate_stake > 0:
                    estimated_removed_value = (user_subnet_shares / subnet_delegate_stake) * subnet_delegate_stake

                return StakeRemoveResponse(
                    success=True,
                    message="Automatic subnet stake removal completed successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={
                        "receipt": receipt,
                        "removed_amount": estimated_removed_value,
                        "shares_removed": user_subnet_shares,
                        "subnet_id": subnet_id,
                        "node_id": None,
                        "unbonding_started": True
                    }
                )
            else:
                # Return composed call data for manual submission
                return StakeRemoveResponse(
                    success=True,
                    message="Automatic subnet stake removal call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={
                        "call_data": call_data,
                        "removed_amount": 0,
                        "shares_removed": user_subnet_shares,
                        "subnet_id": subnet_id,
                        "node_id": None,
                        "unbonding_started": False
                    }
                )

        except Exception as e:
            logger.error(f"Failed to remove subnet stake automatically: {str(e)}")
            return StakeRemoveResponse(
                success=False,
                message=f"Failed to remove subnet stake automatically: {str(e)}",
                data={}
            )

    # ============================================================================
    # Subnet Activation Requirements Methods
    # ============================================================================

    def check_subnet_activation_requirements(self, subnet_id: int):
        """Check if a subnet meets all activation requirements."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Get subnet data to check current status
            subnet_data_response = self.get_subnet_data(subnet_id)
            if not subnet_data_response.success:
                return {
                    "can_activate": False,
                    "requirements_met": False,
                    "errors": [f"Failed to get subnet data: {subnet_data_response.message}"],
                    "warnings": [],
                    "details": {}
                }

            subnet_data = subnet_data_response.data
            requirements = {
                "can_activate": True,
                "requirements_met": True,
                "errors": [],
                "warnings": [],
                "details": {}
            }

            # Check 1: Subnet must be in registration phase
            subnet_status = subnet_data.get("status", "Unknown")
            if subnet_status != "Registration":
                requirements["can_activate"] = False
                requirements["requirements_met"] = False
                requirements["errors"].append(f"Subnet must be in registration phase, current status: {subnet_status}")

            # Check 2: Minimum nodes requirement
            min_nodes = self._get_minimum_nodes_requirement(subnet_id)
            current_nodes = self._get_current_registered_nodes(subnet_id)
            
            requirements["details"]["min_nodes"] = min_nodes
            requirements["details"]["current_nodes"] = current_nodes
            
            if current_nodes < min_nodes:
                requirements["can_activate"] = False
                requirements["requirements_met"] = False
                requirements["errors"].append(f"Minimum {min_nodes} nodes required, current: {current_nodes}")
            elif current_nodes == min_nodes:
                requirements["warnings"].append(f"Exactly minimum nodes ({current_nodes}), consider adding more for stability")

            # Check 3: Minimum delegate stake requirement
            min_delegate_stake = self._get_minimum_delegate_stake_requirement(subnet_id)
            current_delegate_stake = self._get_current_delegate_stake(subnet_id)
            
            requirements["details"]["min_delegate_stake"] = min_delegate_stake
            requirements["details"]["current_delegate_stake"] = current_delegate_stake
            
            if current_delegate_stake < min_delegate_stake:
                requirements["can_activate"] = False
                requirements["requirements_met"] = False
                requirements["errors"].append(f"Minimum {min_delegate_stake} TENSOR delegate stake required, current: {current_delegate_stake}")
            elif current_delegate_stake == min_delegate_stake:
                requirements["warnings"].append(f"Exactly minimum delegate stake ({current_delegate_stake}), consider adding more for stability")

            # Check 4: Stake factor requirements
            stake_factor_requirements = self._check_stake_factor_requirements(subnet_id)
            requirements["details"]["stake_factor"] = stake_factor_requirements
            
            if not stake_factor_requirements["met"]:
                requirements["can_activate"] = False
                requirements["requirements_met"] = False
                requirements["errors"].extend(stake_factor_requirements["errors"])

            # Check 5: Initial coldkeys requirement
            initial_coldkeys = self._get_initial_coldkeys(subnet_id)
            requirements["details"]["initial_coldkeys"] = len(initial_coldkeys)
            
            if len(initial_coldkeys) == 0:
                requirements["warnings"].append("No initial coldkeys found - this may be expected for some subnets")

            # Check 6: Network consensus requirements
            consensus_requirements = self._check_network_consensus_requirements(subnet_id)
            requirements["details"]["consensus"] = consensus_requirements
            
            if not consensus_requirements["met"]:
                requirements["can_activate"] = False
                requirements["requirements_met"] = False
                requirements["errors"].extend(consensus_requirements["errors"])

            return requirements

        except Exception as e:
            logger.error(f"Failed to check subnet activation requirements: {str(e)}")
            return {
                "can_activate": False,
                "requirements_met": False,
                "errors": [f"Failed to check requirements: {str(e)}"],
                "warnings": [],
                "details": {}
            }

    def _get_minimum_nodes_requirement(self, subnet_id: int) -> int:
        """Get the minimum number of nodes required for subnet activation."""
        try:
            # Query the minimum nodes requirement from the blockchain
            # This would typically come from subnet configuration or network parameters
            min_nodes = self._safe_query_value("SubnetMinNodes", subnet_id, 1)
            return max(min_nodes, 1)  # Ensure at least 1 node
        except Exception:
            return 1  # Default minimum

    def _get_current_registered_nodes(self, subnet_id: int) -> int:
        """Get the current number of registered nodes for a subnet."""
        try:
            # Query registered nodes count
            registered_nodes = self._safe_query_value("RegisteredSubnetNodesCount", subnet_id, 0)
            return registered_nodes
        except Exception:
            return 0

    def _get_minimum_delegate_stake_requirement(self, subnet_id: int) -> int:
        """Get the minimum delegate stake required for subnet activation."""
        try:
            # Query the minimum delegate stake requirement
            min_stake = self._safe_query_value("SubnetMinDelegateStake", subnet_id, 1000000)  # Default 1 TENSOR
            return max(min_stake, 1000000)  # Ensure reasonable minimum
        except Exception:
            return 1000000  # Default minimum

    def _get_current_delegate_stake(self, subnet_id: int) -> int:
        """Get the current delegate stake for a subnet."""
        try:
            # Query current delegate stake
            delegate_stake = self._safe_query_value("TotalSubnetDelegateStakeBalance", subnet_id, 0)
            return delegate_stake
        except Exception:
            return 0

    def _check_stake_factor_requirements(self, subnet_id: int) -> dict:
        """Check if stake factor requirements are met."""
        try:
            # Get subnet configuration
            subnet_data = self._safe_query_value("SubnetsData", subnet_id, {})
            
            if not subnet_data:
                return {
                    "met": False,
                    "errors": ["Subnet data not found"],
                    "details": {}
                }

            min_stake = subnet_data.get("min_stake", 0)
            max_stake = subnet_data.get("max_stake", 0)
            current_delegate_stake = self._get_current_delegate_stake(subnet_id)

            requirements = {
                "met": True,
                "errors": [],
                "details": {
                    "min_stake": min_stake,
                    "max_stake": max_stake,
                    "current_delegate_stake": current_delegate_stake
                }
            }

            # Check minimum stake factor
            if min_stake > 0 and current_delegate_stake < min_stake:
                requirements["met"] = False
                requirements["errors"].append(f"Current delegate stake ({current_delegate_stake}) below minimum ({min_stake})")

            # Check maximum stake factor (if applicable)
            if max_stake > 0 and current_delegate_stake > max_stake:
                requirements["warnings"] = [f"Current delegate stake ({current_delegate_stake}) above maximum ({max_stake})"]

            return requirements

        except Exception as e:
            return {
                "met": False,
                "errors": [f"Failed to check stake factor requirements: {str(e)}"],
                "details": {}
            }

    def _get_initial_coldkeys(self, subnet_id: int) -> list:
        """Get the initial coldkeys for a subnet."""
        try:
            # Query initial coldkeys
            initial_coldkeys = self._safe_query_value("SubnetRegistrationInitialColdkeys", subnet_id, [])
            return initial_coldkeys if initial_coldkeys else []
        except Exception:
            return []

    def _check_network_consensus_requirements(self, subnet_id: int) -> dict:
        """Check network consensus requirements for subnet activation."""
        try:
            # Get network consensus parameters
            consensus_params = self._safe_query_value("NetworkConsensusParams", None, {})
            
            requirements = {
                "met": True,
                "errors": [],
                "details": consensus_params
            }

            # Check if network is ready for new subnet activation
            # This would typically check network load, consensus state, etc.
            network_load = consensus_params.get("network_load", 0)
            max_network_load = consensus_params.get("max_network_load", 100)

            if network_load > max_network_load * 0.9:  # 90% threshold
                requirements["warnings"] = [f"Network load is high ({network_load}%), activation may be delayed"]

            # Check consensus state
            consensus_state = consensus_params.get("consensus_state", "Unknown")
            if consensus_state != "Ready":
                requirements["met"] = False
                requirements["errors"].append(f"Network consensus not ready: {consensus_state}")

            return requirements

        except Exception as e:
            return {
                "met": False,
                "errors": [f"Failed to check consensus requirements: {str(e)}"],
                "details": {}
            }
