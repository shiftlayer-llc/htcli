"""
Pydantic models for request structures.
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class SubnetRegisterRequest(BaseModel):
    """Request model for subnet registration based on official RegistrationSubnetData."""

    # Required fields from official spec
    name: str = Field(..., description="Unique name of the subnet")
    repo: str = Field(..., description="GitHub or similar link to source code")
    description: str = Field(..., description="Description of the subnet")
    misc: Dict[str, Any] = Field(
        default_factory=dict, description="Miscellaneous information"
    )

    # Stake configuration
    min_stake: int = Field(
        ..., description="Minimum required stake balance to register a node"
    )
    max_stake: int = Field(
        ..., description="Maximum allowable stake balance for a subnet node"
    )
    delegate_stake_percentage: int = Field(
        ..., description="Percentage ratio of emissions given to delegate stakers"
    )

    # Epoch and timing configuration
    churn_limit: int = Field(..., description="Number of subnet activations per epoch")
    registration_queue_epochs: int = Field(
        ...,
        description="Number of epochs for registered nodes to be in queue before activation",
    )
    activation_grace_epochs: int = Field(
        ..., description="Grace period epochs during which nodes can activate"
    )
    queue_classification_epochs: int = Field(
        ..., description="Number of epochs for queue classification"
    )
    included_classification_epochs: int = Field(
        ..., description="Number of epochs for included classification"
    )

    # Node configuration
    max_node_penalties: int = Field(
        default=3, description="Maximum penalties a node can have before removal"
    )
    max_registered_nodes: int = Field(
        ..., description="Maximum number of nodes in registration queue"
    )
    initial_coldkeys: list = Field(
        default_factory=list,
        description="List of whitelisted coldkeys for initial registration",
    )

    # Key types (supported: RSA, Ed25519, Secp256k1, ECDSA)
    key_types: list = Field(
        default=["Ed25519"],
        description="Supported key types for signature authentication",
    )

    # Node removal system (simplified for now)
    node_removal_system: str = Field("default", description="Node removal system type")


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
