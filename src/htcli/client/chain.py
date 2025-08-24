#!/usr/bin/env python3
"""
Chain operations client module.
Handles all chain-related blockchain operations.
"""

import logging
from typing import Optional

from substrateinterface import SubstrateInterface

from ..models.responses import *

logger = logging.getLogger(__name__)


class ChainClient:
    """Client for chain operations."""

    def __init__(self, substrate: SubstrateInterface):
        self.substrate = substrate

    def get_network_stats(self):
        """Get network statistics using storage queries."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Query various network statistics
            total_subnets = self.substrate.query(
                module="Network", storage_function="TotalSubnetUids", params=[]
            )

            total_active_subnets = self.substrate.query(
                module="Network", storage_function="TotalActiveSubnets", params=[]
            )

            total_active_nodes = self.substrate.query(
                module="Network", storage_function="TotalActiveNodes", params=[]
            )

            total_stake = self.substrate.query(
                module="Network", storage_function="TotalStake", params=[]
            )

            return NetworkStatsResponse(
                success=True,
                message="Network statistics retrieved successfully",
                data={
                    # "total_subnets": total_subnets.value if total_subnets else 0,
                    # "total_active_subnets": (
                    #     total_active_subnets.value if total_active_subnets else 0
                    # ),
                    # "total_active_nodes": (
                    #     total_active_nodes.value if total_active_nodes else 0
                    # ),
                    # "total_stake": total_stake.value if total_stake else 0,
                    "total_subnets": total_subnets.value,
                    "total_active_subnets": (total_active_subnets.value),
                    "total_active_nodes": (total_active_nodes.value),
                    "total_stake": total_stake.value,
                },
            )
        except Exception as e:
            logger.error(f"Failed to get network stats: {str(e)}")
            raise

    def get_current_epoch(self):
        """Get current epoch using storage query."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Try different storage functions for epoch
            try:
                # Try Network.CurrentEpoch first
                current_epoch = self.substrate.query(
                    module="Network", storage_function="CurrentEpoch", params=[]
                )
                epoch_value = current_epoch.value if current_epoch else 0
            except:
                # Fallback to a default value if storage function doesn't exist
                epoch_value = 0

            return EpochInfoResponse(
                success=True,
                message="Current epoch retrieved successfully",
                data={"current_epoch": epoch_value},
            )
        except Exception as e:
            logger.error(f"Failed to get current epoch: {str(e)}")
            raise

    def get_balance(self, address: str):
        """Get account balance using System.Account storage query."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Query account balance using the System pallet
            account_info = self.substrate.query(
                module="System", storage_function="Account", params=[address]
            )

            balance = (
                account_info.value["data"]["free"]
                if account_info and account_info.value
                else 0
            )

            return BalanceResponse(
                success=True,
                message="Balance retrieved successfully",
                data={
                    "address": address,
                    "balance": balance,
                    "formatted_balance": f"{balance / 1e18:.6f} TENSOR",
                    "unit": "TENSOR",
                },
            )
        except Exception as e:
            logger.error(f"Failed to get balance: {str(e)}")
            raise

    def get_peers(self):
        """Get network peers using system_peers RPC."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Query network peers using RPC
            peers = self.substrate.rpc_request("system_peers", [])

            return PeersResponse(
                success=True,
                message="Peers retrieved successfully",
                data={"peers": peers.get("result", [])},
            )
        except Exception as e:
            logger.error(f"Failed to get peers: {str(e)}")
            raise

    def get_block_info(self, block_number: Optional[int] = None):
        """Get block information using SubstrateInterface methods."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Get block hash
            if block_number is None:
                block_hash = self.substrate.get_chain_head()
            else:
                block_hash = self.substrate.get_block_hash(block_number)

            # Get block header
            block_header = self.substrate.get_block_header(block_hash)

            # Get block details
            block = self.substrate.get_block(block_hash)

            return BlockInfoResponse(
                success=True,
                message="Block info retrieved successfully",
                data={
                    "block_number": block_header.get(
                        "number", 0
                    ),  # Use get() for safety
                    "block_hash": str(block_hash),
                    "parent_hash": str(block_header.get("parentHash", "")),
                    "state_root": str(block_header.get("stateRoot", "")),
                    "extrinsics_root": str(block_header.get("extrinsicsRoot", "")),
                    "timestamp": block_header.get("timestamp", 0),
                    "extrinsics_count": (
                        len(block.get("extrinsics", [])) if block else 0
                    ),
                },
            )
        except Exception as e:
            logger.error(f"Failed to get block info: {str(e)}")
            raise

    # Additional chain operations based on discovered Network pallet methods
    def validate(self, subnet_id: int, data: str, args: str = None, keypair=None):
        """Validate using Network.validate."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            call_params = {"subnet_id": subnet_id, "data": data}
            if args:
                call_params["args"] = args

            call_data = self.substrate.compose_call(
                call_module="Network", call_function="validate", call_params=call_params
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return ValidationResponse(
                    success=True,
                    message="Validation submitted successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return ValidationResponse(
                    success=True,
                    message="Validation call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to validate: {str(e)}")
            raise

    def attest(self, subnet_id: int, keypair=None):
        """Attest using Network.attest."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="attest",
                call_params={"subnet_id": subnet_id},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return AttestationResponse(
                    success=True,
                    message="Attestation submitted successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return AttestationResponse(
                    success=True,
                    message="Attestation call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to attest: {str(e)}")
            raise

    def propose(
        self, subnet_id: int, subnet_node_id: int, peer_id: str, data: str, keypair=None
    ):
        """Propose using Network.propose."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="propose",
                call_params={
                    "subnet_id": subnet_id,
                    "subnet_node_id": subnet_node_id,
                    "peer_id": peer_id,
                    "data": data,
                },
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return ProposalResponse(
                    success=True,
                    message="Proposal submitted successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return ProposalResponse(
                    success=True,
                    message="Proposal call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to propose: {str(e)}")
            raise

    def vote(
        self,
        subnet_id: int,
        subnet_node_id: int,
        proposal_id: int,
        vote: str,
        keypair=None,
    ):
        """Vote using Network.vote."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="vote",
                call_params={
                    "subnet_id": subnet_id,
                    "subnet_node_id": subnet_node_id,
                    "proposal_id": proposal_id,
                    "vote": vote,
                },
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return VoteResponse(
                    success=True,
                    message="Vote submitted successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return VoteResponse(
                    success=True,
                    message="Vote call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to vote: {str(e)}")
            raise

    def get_account_info(self, address: str):
        """Get detailed account information."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Get account balance
            account_info = self.substrate.query(
                module="System", storage_function="Account", params=[address]
            )

            # Try to get account nonce - handle missing storage function
            try:
                nonce = self.substrate.query(
                    module="System", storage_function="AccountNonce", params=[address]
                )
                nonce_value = nonce.value if nonce else 0
            except Exception:
                # If AccountNonce doesn't exist, use a default value
                nonce_value = 0

            balance = (
                account_info.value["data"]["free"]
                if account_info and account_info.value
                else 0
            )

            return AccountInfoResponse(
                success=True,
                message="Account information retrieved successfully",
                data={
                    "address": address,
                    "balance": balance,
                    "nonce": nonce_value,
                    "formatted_balance": (
                        f"{(balance / 1e18):.6f} TENSOR" if balance > 0 else "0 TENSOR"
                    ),
                },
            )
        except Exception as e:
            logger.error(f"Failed to get account info: {str(e)}")
            raise

    def get_chain_head(self):
        """Get the current chain head."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            block_hash = self.substrate.get_chain_head()
            block_header = self.substrate.get_block_header(block_hash)

            return ChainHeadResponse(
                success=True,
                message="Chain head retrieved successfully",
                data={
                    "block_number": block_header.get("number", 0),
                    "block_hash": str(block_hash),
                    "parent_hash": str(block_header.get("parentHash", "")),
                },
            )
        except Exception as e:
            logger.error(f"Failed to get chain head: {str(e)}")
            raise

    def get_runtime_version(self):
        """Get the runtime version."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Use the correct method to get runtime version
            runtime_version = self.substrate.runtime_version

            # Handle different runtime_version formats
            if isinstance(runtime_version, dict):
                version_data = runtime_version
            else:
                # If it's not a dict, create a default structure
                version_data = {
                    "spec_name": "unknown",
                    "impl_name": "unknown",
                    "authoring_version": 0,
                    "spec_version": 0,
                    "impl_version": 0,
                    "transaction_version": 0,
                }

            return RuntimeVersionResponse(
                success=True,
                message="Runtime version retrieved successfully",
                data={
                    "spec_name": version_data.get("spec_name", ""),
                    "impl_name": version_data.get("impl_name", ""),
                    "authoring_version": version_data.get("authoring_version", 0),
                    "spec_version": version_data.get("spec_version", 0),
                    "impl_version": version_data.get("impl_version", 0),
                    "transaction_version": version_data.get("transaction_version", 0),
                },
            )
        except Exception as e:
            logger.error(f"Failed to get runtime version: {str(e)}")
            raise
