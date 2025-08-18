#!/usr/bin/env python3
"""
Response models for Hypertensor CLI.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List


class BaseResponse(BaseModel):
    """Base response model."""

    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    transaction_hash: Optional[str] = Field(None, description="Transaction hash")
    block_number: Optional[int] = Field(None, description="Block number")
    data: Dict[str, Any] = Field(default_factory=dict, description="Response data")


# Subnet responses
class SubnetRegisterResponse(BaseResponse):
    """Response for subnet registration."""

    subnet_id: Optional[int] = Field(None, description="Registered subnet ID")
    registration_data: Optional[Dict[str, Any]] = Field(
        None, description="Registration data"
    )
    estimated_cost: Optional[int] = Field(
        None, description="Estimated registration cost"
    )


class SubnetActivateResponse(BaseResponse):
    """Response for subnet activation."""

    subnet_id: Optional[int] = Field(None, description="Activated subnet ID")
    activation_epoch: Optional[int] = Field(None, description="Activation epoch")
    requirements_met: Optional[bool] = Field(
        None, description="Whether all requirements were met"
    )


class SubnetInfoResponse(BaseResponse):
    """Response for subnet information."""

    subnet_id: Optional[int] = Field(None, description="Subnet ID")
    subnet_data: Optional[Dict[str, Any]] = Field(None, description="Subnet data")
    node_count: Optional[int] = Field(None, description="Number of nodes")
    total_stake: Optional[int] = Field(None, description="Total stake")
    status: Optional[str] = Field(None, description="Subnet status")


class SubnetsListResponse(BaseResponse):
    """Response for subnets list."""

    subnets: Optional[List[Dict[str, Any]]] = Field(None, description="List of subnets")
    total_count: Optional[int] = Field(None, description="Total number of subnets")
    filtered_count: Optional[int] = Field(
        None, description="Number of subnets after filtering"
    )


class SubnetRemoveResponse(BaseResponse):
    """Response for subnet removal."""

    subnet_id: Optional[int] = Field(None, description="Removed subnet ID")
    removal_epoch: Optional[int] = Field(None, description="Removal epoch")
    stake_returned: Optional[int] = Field(None, description="Amount of stake returned")


class SubnetPauseResponse(BaseModel):
    """Response model for subnet pause operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    transaction_hash: Optional[str] = Field(None, description="Transaction hash")
    block_number: Optional[int] = Field(None, description="Block number")
    data: Dict[str, Any] = Field(default_factory=dict, description="Additional data")


class SubnetUnpauseResponse(BaseModel):
    """Response model for subnet unpause operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    transaction_hash: Optional[str] = Field(None, description="Transaction hash")
    block_number: Optional[int] = Field(None, description="Block number")
    data: Dict[str, Any] = Field(default_factory=dict, description="Additional data")


class SubnetOwnershipTransferResponse(BaseModel):
    """Response model for subnet ownership transfer operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    transaction_hash: Optional[str] = Field(None, description="Transaction hash")
    block_number: Optional[int] = Field(None, description="Block number")
    data: Dict[str, Any] = Field(default_factory=dict, description="Additional data")


class SubnetOwnerUpdateResponse(BaseModel):
    """Response model for subnet owner update operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    transaction_hash: Optional[str] = Field(None, description="Transaction hash")
    block_number: Optional[int] = Field(None, description="Block number")
    data: Dict[str, Any] = Field(default_factory=dict, description="Additional data")


# Node responses
class NodeAddResponse(BaseResponse):
    """Response for node addition."""

    node_id: Optional[int] = Field(None, description="Added node ID")
    subnet_id: Optional[int] = Field(None, description="Subnet ID")
    registration_epoch: Optional[int] = Field(None, description="Registration epoch")
    activation_epoch: Optional[int] = Field(
        None, description="Epoch when node can activate"
    )
    stake_amount: Optional[int] = Field(None, description="Stake amount")


class NodesListResponse(BaseResponse):
    """Response for nodes list."""

    nodes: Optional[List[Dict[str, Any]]] = Field(None, description="List of nodes")
    total_count: Optional[int] = Field(None, description="Total number of nodes")
    active_count: Optional[int] = Field(None, description="Number of active nodes")
    registered_count: Optional[int] = Field(
        None, description="Number of registered nodes"
    )


class NodeDeactivateResponse(BaseResponse):
    """Response for node deactivation."""

    node_id: Optional[int] = Field(None, description="Deactivated node ID")
    subnet_id: Optional[int] = Field(None, description="Subnet ID")
    deactivation_epoch: Optional[int] = Field(None, description="Deactivation epoch")
    reactivation_deadline: Optional[int] = Field(
        None, description="Deadline for reactivation"
    )
    stake_locked: Optional[bool] = Field(None, description="Whether stake is locked")


class NodeRemoveResponse(BaseResponse):
    """Response for node removal."""

    node_id: Optional[int] = Field(None, description="Removed node ID")
    subnet_id: Optional[int] = Field(None, description="Subnet ID")
    removal_epoch: Optional[int] = Field(None, description="Removal epoch")
    stake_removed: Optional[bool] = Field(None, description="Whether stake was removed")
    stake_amount: Optional[int] = Field(None, description="Amount of stake removed")


# Staking responses
class StakeAddResponse(BaseResponse):
    """Response for stake addition."""

    stake_amount: Optional[int] = Field(None, description="Amount of stake added")
    shares_received: Optional[int] = Field(None, description="Shares received")
    node_id: Optional[int] = Field(None, description="Node ID")
    subnet_id: Optional[int] = Field(None, description="Subnet ID")
    reward_rate: Optional[float] = Field(None, description="Current reward rate")


class StakeRemoveResponse(BaseResponse):
    """Response for stake removal."""

    stake_amount: Optional[int] = Field(None, description="Amount of stake removed")
    shares_removed: Optional[int] = Field(None, description="Shares removed")
    node_id: Optional[int] = Field(None, description="Node ID")
    subnet_id: Optional[int] = Field(None, description="Subnet ID")
    unbonding_started: Optional[bool] = Field(
        None, description="Whether unbonding started"
    )
    unbonding_period: Optional[int] = Field(
        None, description="Unbonding period in epochs"
    )


class StakeInfoResponse(BaseResponse):
    """Response for stake information."""

    total_stake: Optional[int] = Field(None, description="Total stake amount")
    shares_owned: Optional[int] = Field(None, description="Shares owned")
    reward_rate: Optional[float] = Field(None, description="Current reward rate")
    estimated_rewards: Optional[float] = Field(None, description="Estimated rewards")
    unbonding_amount: Optional[int] = Field(None, description="Amount in unbonding")
    unbonding_epochs: Optional[int] = Field(
        None, description="Epochs until unbonding complete"
    )


class UnbondingClaimResponse(BaseResponse):
    """Response for unbonding claim."""

    claimed_amount: Optional[int] = Field(None, description="Amount claimed")
    remaining_unbonding: Optional[int] = Field(
        None, description="Remaining unbonding amount"
    )
    claim_epoch: Optional[int] = Field(None, description="Epoch when claimed")


class DelegateStakeAddResponse(BaseResponse):
    """Response for delegate stake addition."""

    stake_amount: Optional[int] = Field(
        None, description="Amount of delegate stake added"
    )
    shares_received: Optional[int] = Field(None, description="Shares received")
    subnet_id: Optional[int] = Field(None, description="Subnet ID")
    reward_rate: Optional[float] = Field(
        None, description="Current delegate reward rate"
    )
    total_subnet_stake: Optional[int] = Field(
        None, description="Total subnet delegate stake"
    )


class DelegateStakeTransferResponse(BaseResponse):
    """Response for delegate stake transfer."""

    shares_transferred: Optional[int] = Field(None, description="Shares transferred")
    from_address: Optional[str] = Field(None, description="Source address")
    to_address: Optional[str] = Field(None, description="Destination address")
    subnet_id: Optional[int] = Field(None, description="Subnet ID")
    transfer_value: Optional[int] = Field(
        None, description="Value of transferred shares"
    )


class DelegateStakeRemoveResponse(BaseResponse):
    """Response for delegate stake removal."""

    shares_removed: Optional[int] = Field(None, description="Shares removed")
    stake_amount: Optional[int] = Field(None, description="Stake amount returned")
    subnet_id: Optional[int] = Field(None, description="Subnet ID")
    unbonding_started: Optional[bool] = Field(
        None, description="Whether unbonding started"
    )
    unbonding_period: Optional[int] = Field(
        None, description="Unbonding period in epochs"
    )


class DelegateStakeIncreaseResponse(BaseModel):
    """Response model for delegate stake pool increase operations."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    transaction_hash: Optional[str] = Field(None, description="Transaction hash")
    block_number: Optional[int] = Field(None, description="Block number")
    data: Dict[str, Any] = Field(default_factory=dict, description="Additional data")


# Key management responses
class ColdkeyUpdateResponse(BaseResponse):
    """Response for coldkey update."""

    old_coldkey: Optional[str] = Field(None, description="Previous coldkey")
    new_coldkey: Optional[str] = Field(None, description="New coldkey")
    node_id: Optional[int] = Field(None, description="Node ID")
    subnet_id: Optional[int] = Field(None, description="Subnet ID")
    update_epoch: Optional[int] = Field(None, description="Update epoch")


class HotkeyUpdateResponse(BaseResponse):
    """Response for hotkey update."""

    old_hotkey: Optional[str] = Field(None, description="Previous hotkey")
    new_hotkey: Optional[str] = Field(None, description="New hotkey")
    node_id: Optional[int] = Field(None, description="Node ID")
    subnet_id: Optional[int] = Field(None, description="Subnet ID")
    update_epoch: Optional[int] = Field(None, description="Update epoch")


# Chain responses
class NetworkStatsResponse(BaseResponse):
    """Response for network statistics."""

    total_subnets: Optional[int] = Field(None, description="Total number of subnets")
    total_nodes: Optional[int] = Field(None, description="Total number of nodes")
    total_stake: Optional[int] = Field(None, description="Total network stake")
    current_epoch: Optional[int] = Field(None, description="Current epoch")
    network_load: Optional[float] = Field(None, description="Network load percentage")


class EpochInfoResponse(BaseResponse):
    """Response for epoch information."""

    current_epoch: Optional[int] = Field(None, description="Current epoch number")
    epoch_start: Optional[int] = Field(None, description="Epoch start block")
    epoch_end: Optional[int] = Field(None, description="Epoch end block")
    blocks_per_epoch: Optional[int] = Field(None, description="Blocks per epoch")
    epoch_duration: Optional[int] = Field(None, description="Epoch duration in seconds")


class BalanceResponse(BaseResponse):
    """Response for balance information."""

    address: Optional[str] = Field(None, description="Account address")
    balance: Optional[int] = Field(None, description="Account balance")
    locked_balance: Optional[int] = Field(None, description="Locked balance")
    available_balance: Optional[int] = Field(None, description="Available balance")
    reserved_balance: Optional[int] = Field(None, description="Reserved balance")


class PeersResponse(BaseResponse):
    """Response for peers information."""

    peers: Optional[List[Dict[str, Any]]] = Field(None, description="List of peers")
    total_peers: Optional[int] = Field(None, description="Total number of peers")
    connected_peers: Optional[int] = Field(
        None, description="Number of connected peers"
    )
    syncing_peers: Optional[int] = Field(None, description="Number of syncing peers")


class BlockInfoResponse(BaseResponse):
    """Response for block information."""

    block_number: Optional[int] = Field(None, description="Block number")
    block_hash: Optional[str] = Field(None, description="Block hash")
    parent_hash: Optional[str] = Field(None, description="Parent block hash")
    timestamp: Optional[int] = Field(None, description="Block timestamp")
    extrinsics_count: Optional[int] = Field(None, description="Number of extrinsics")
    events_count: Optional[int] = Field(None, description="Number of events")


class AccountInfoResponse(BaseResponse):
    """Response for account information."""

    address: Optional[str] = Field(None, description="Account address")
    nonce: Optional[int] = Field(None, description="Account nonce")
    ref_count: Optional[int] = Field(None, description="Reference count")
    data: Optional[Dict[str, Any]] = Field(None, description="Account data")


class ChainHeadResponse(BaseResponse):
    """Response for chain head information."""

    head_block: Optional[int] = Field(None, description="Head block number")
    head_hash: Optional[str] = Field(None, description="Head block hash")
    finalized_block: Optional[int] = Field(None, description="Finalized block number")
    finalized_hash: Optional[str] = Field(None, description="Finalized block hash")
    sync_status: Optional[str] = Field(None, description="Sync status")


class RuntimeVersionResponse(BaseResponse):
    """Response for runtime version information."""

    spec_name: Optional[str] = Field(None, description="Specification name")
    impl_name: Optional[str] = Field(None, description="Implementation name")
    authoring_version: Optional[int] = Field(None, description="Authoring version")
    spec_version: Optional[int] = Field(None, description="Specification version")
    impl_version: Optional[int] = Field(None, description="Implementation version")
    transaction_version: Optional[int] = Field(None, description="Transaction version")


# Validation responses
class ValidationResponse(BaseResponse):
    """Response for validation submission."""

    validation_hash: Optional[str] = Field(None, description="Validation hash")
    subnet_id: Optional[int] = Field(None, description="Subnet ID")
    node_id: Optional[int] = Field(None, description="Node ID")
    validation_epoch: Optional[int] = Field(None, description="Validation epoch")
    reward_amount: Optional[int] = Field(None, description="Reward amount")


class AttestationResponse(BaseResponse):
    """Response for attestation submission."""

    attestation_hash: Optional[str] = Field(None, description="Attestation hash")
    subnet_id: Optional[int] = Field(None, description="Subnet ID")
    node_id: Optional[int] = Field(None, description="Node ID")
    attestation_epoch: Optional[int] = Field(None, description="Attestation epoch")
    attestation_score: Optional[float] = Field(None, description="Attestation score")


class ProposalResponse(BaseResponse):
    """Response for proposal submission."""

    proposal_hash: Optional[str] = Field(None, description="Proposal hash")
    proposal_id: Optional[int] = Field(None, description="Proposal ID")
    proposal_type: Optional[str] = Field(None, description="Proposal type")
    voting_period: Optional[int] = Field(None, description="Voting period")
    required_votes: Optional[int] = Field(
        None, description="Required votes for approval"
    )


class VoteResponse(BaseResponse):
    """Response for vote submission."""

    vote_hash: Optional[str] = Field(None, description="Vote hash")
    proposal_id: Optional[int] = Field(None, description="Proposal ID")
    vote_value: Optional[bool] = Field(None, description="Vote value (true/false)")
    voter_address: Optional[str] = Field(None, description="Voter address")
    voting_power: Optional[int] = Field(None, description="Voting power used")
