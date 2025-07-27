"""
Pydantic models for request structures.
"""

from pydantic import BaseModel, Field
from typing import Optional


class SubnetRegisterRequest(BaseModel):
    """Request model for subnet registration."""
    path: str = Field(..., description="Subnet path/name")
    memory_mb: int = Field(..., description="Memory requirement in MB")
    registration_blocks: int = Field(..., description="Registration period in blocks")
    entry_interval: int = Field(..., description="Entry interval in blocks")


class SubnetNodeAddRequest(BaseModel):
    """Request model for adding a node to a subnet."""
    subnet_id: int = Field(..., description="Subnet ID")
    peer_id: str = Field(..., description="Peer ID")
    hotkey: str = Field(..., description="Hotkey account")


class StakeAddRequest(BaseModel):
    """Request model for adding stake."""
    subnet_id: int = Field(..., description="Subnet ID")
    subnet_node_id: int = Field(..., description="Subnet node ID")
    hotkey: str = Field(..., description="Hotkey account")
    stake_to_be_added: int = Field(..., description="Stake amount in smallest unit")


class StakeRemoveRequest(BaseModel):
    """Request model for removing stake."""
    subnet_id: int = Field(..., description="Subnet ID")
    hotkey: str = Field(..., description="Hotkey account")
    stake_to_be_removed: int = Field(..., description="Stake amount to remove")


class ValidationSubmitRequest(BaseModel):
    """Request model for submitting validation."""
    subnet_id: int = Field(..., description="Subnet ID")
    data: str = Field(..., description="Validation data")
    args: Optional[str] = Field(None, description="Optional arguments")


class GovernanceProposeRequest(BaseModel):
    """Request model for creating a governance proposal."""
    subnet_id: int = Field(..., description="Subnet ID")
    subnet_node_id: int = Field(..., description="Subnet node ID")
    peer_id: str = Field(..., description="Peer ID")
    data: str = Field(..., description="Proposal data")


class GovernanceVoteRequest(BaseModel):
    """Request model for voting on a governance proposal."""
    subnet_id: int = Field(..., description="Subnet ID")
    subnet_node_id: int = Field(..., description="Subnet node ID")
    proposal_id: int = Field(..., description="Proposal ID")
    vote: str = Field(..., description="Vote type: 'yay' or 'nay'")


class TransferRequest(BaseModel):
    """Request model for token transfer."""
    to_address: str = Field(..., description="Destination address")
    amount: int = Field(..., description="Amount in smallest unit")
    from_address: Optional[str] = Field(None, description="Source address")


class KeyGenerateRequest(BaseModel):
    """Request model for key generation."""
    name: str = Field(..., description="Key name")
    key_type: str = Field("sr25519", description="Key type (sr25519/ed25519)")
    password: Optional[str] = Field(None, description="Key password")


class KeyImportRequest(BaseModel):
    """Request model for key import."""
    name: str = Field(..., description="Key name")
    private_key: str = Field(..., description="Private key")
    key_type: str = Field("sr25519", description="Key type")
    password: Optional[str] = Field(None, description="Key password")
