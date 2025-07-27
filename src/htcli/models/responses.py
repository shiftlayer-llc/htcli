"""
Pydantic models for response structures.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class BaseResponse(BaseModel):
    """Base response model."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    transaction_hash: Optional[str] = Field(None, description="Transaction hash")
    block_number: Optional[int] = Field(None, description="Block number")


class SubnetRegisterResponse(BaseResponse):
    """Response model for subnet registration."""
    data: Optional[Dict[str, Any]] = Field(None, description="Registration data")


class SubnetInfoResponse(BaseResponse):
    """Response model for subnet information."""
    data: Optional[Dict[str, Any]] = Field(None, description="Subnet information")


class SubnetListResponse(BaseResponse):
    """Response model for subnet list."""
    data: Optional[Dict[str, Any]] = Field(None, description="Subnet list data")


class NodeAddResponse(BaseResponse):
    """Response model for adding a node."""
    data: Optional[Dict[str, Any]] = Field(None, description="Node addition data")


class NodeListResponse(BaseResponse):
    """Response model for node list."""
    data: Optional[Dict[str, Any]] = Field(None, description="Node list data")


class StakeAddResponse(BaseResponse):
    """Response model for adding stake."""
    data: Optional[Dict[str, Any]] = Field(None, description="Stake addition data")


class StakeRemoveResponse(BaseResponse):
    """Response model for removing stake."""
    data: Optional[Dict[str, Any]] = Field(None, description="Stake removal data")


class StakeInfoResponse(BaseResponse):
    """Response model for stake information."""
    data: Optional[Dict[str, Any]] = Field(None, description="Stake information")


class ValidationSubmitResponse(BaseResponse):
    """Response model for validation submission."""
    data: Optional[Dict[str, Any]] = Field(None, description="Validation submission data")


class GovernanceProposeResponse(BaseResponse):
    """Response model for governance proposal."""
    data: Optional[Dict[str, Any]] = Field(None, description="Proposal data")


class GovernanceVoteResponse(BaseResponse):
    """Response model for governance vote."""
    data: Optional[Dict[str, Any]] = Field(None, description="Vote data")


class NetworkStatsResponse(BaseResponse):
    """Response model for network statistics."""
    data: Optional[Dict[str, Any]] = Field(None, description="Network statistics")


class AccountInfoResponse(BaseResponse):
    """Response model for account information."""
    data: Optional[Dict[str, Any]] = Field(None, description="Account information")


class EpochInfoResponse(BaseResponse):
    """Response model for epoch information."""
    data: Optional[Dict[str, Any]] = Field(None, description="Epoch information")


class BalanceResponse(BaseResponse):
    """Response model for balance query."""
    data: Optional[Dict[str, Any]] = Field(None, description="Balance data")


class PeersResponse(BaseResponse):
    """Response model for peers query."""
    data: Optional[Dict[str, Any]] = Field(None, description="Peers data")


class BlockInfoResponse(BaseResponse):
    """Response model for block information."""
    data: Optional[Dict[str, Any]] = Field(None, description="Block information")


class KeyGenerateResponse(BaseResponse):
    """Response model for key generation."""
    data: Optional[Dict[str, Any]] = Field(None, description="Key generation data")


class KeyListResponse(BaseResponse):
    """Response model for key list."""
    data: Optional[Dict[str, Any]] = Field(None, description="Key list data")


class TransferResponse(BaseResponse):
    """Response model for token transfer."""
    data: Optional[Dict[str, Any]] = Field(None, description="Transfer data")
