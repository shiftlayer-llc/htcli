"""
Pydantic models for request structures.
"""

from pydantic import BaseModel, Field
from typing import Optional


class SubnetRegisterRequest(BaseModel):
    """Request model for subnet registration."""
    path: str = Field(..., description="Subnet path")
    memory_mb: int = Field(..., description="Memory in MB")
    registration_blocks: int = Field(..., description="Registration blocks")
    entry_interval: int = Field(..., description="Entry interval")
    max_node_registration_epochs: int = Field(..., description="Maximum node registration epochs")
    node_registration_interval: int = Field(..., description="Node registration interval")
    node_activation_interval: int = Field(..., description="Node activation interval")
    node_queue_period: int = Field(..., description="Node queue period")
    max_node_penalties: int = Field(..., description="Maximum node penalties")
    coldkey_whitelist: list = Field(default_factory=list, description="Coldkey whitelist")


class SubnetNodeAddRequest(BaseModel):
    """Request model for adding a node to a subnet."""
    subnet_id: int = Field(..., description="Subnet ID")
    peer_id: str = Field(..., description="Peer ID")
    hotkey: str = Field(..., description="Hotkey")
    delegate_reward_rate: int = Field(..., description="Delegate reward rate")
    stake_to_be_added: int = Field(..., description="Stake to be added")


class StakeAddRequest(BaseModel):
    """Request model for adding stake."""
    subnet_id: int = Field(..., description="Subnet ID")
    node_id: int = Field(..., description="Node ID")
    hotkey: str = Field(..., description="Hotkey")
    stake_to_be_added: int = Field(..., description="Stake amount to add")


class StakeRemoveRequest(BaseModel):
    """Request model for removing stake."""
    subnet_id: int = Field(..., description="Subnet ID")
    hotkey: str = Field(..., description="Hotkey")
    stake_to_be_removed: int = Field(..., description="Stake amount to remove")


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
