#!/usr/bin/env python3
"""
Response models for Hypertensor CLI.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

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
    pass

class SubnetActivateResponse(BaseResponse):
    """Response for subnet activation."""
    pass

class SubnetInfoResponse(BaseResponse):
    """Response for subnet information."""
    pass

class SubnetsListResponse(BaseResponse):
    """Response for subnets list."""
    pass

class SubnetRemoveResponse(BaseResponse):
    """Response for subnet removal."""
    pass

# Node responses
class NodeAddResponse(BaseResponse):
    """Response for node addition."""
    pass

class NodesListResponse(BaseResponse):
    """Response for nodes list."""
    pass

class NodeDeactivateResponse(BaseResponse):
    """Response for node deactivation."""
    pass

class NodeRemoveResponse(BaseResponse):
    """Response for node removal."""
    pass

# Staking responses
class StakeAddResponse(BaseResponse):
    """Response for stake addition."""
    pass

class StakeRemoveResponse(BaseResponse):
    """Response for stake removal."""
    pass

class StakeInfoResponse(BaseResponse):
    """Response for stake information."""
    pass

class UnbondingClaimResponse(BaseResponse):
    """Response for unbonding claim."""
    pass

class DelegateStakeAddResponse(BaseResponse):
    """Response for delegate stake addition."""
    pass

class DelegateStakeTransferResponse(BaseResponse):
    """Response for delegate stake transfer."""
    pass

class DelegateStakeRemoveResponse(BaseResponse):
    """Response for delegate stake removal."""
    pass

# Key management responses
class ColdkeyUpdateResponse(BaseResponse):
    """Response for coldkey update."""
    pass

class HotkeyUpdateResponse(BaseResponse):
    """Response for hotkey update."""
    pass

# Chain responses
class NetworkStatsResponse(BaseResponse):
    """Response for network statistics."""
    pass

class EpochInfoResponse(BaseResponse):
    """Response for epoch information."""
    pass

class BalanceResponse(BaseResponse):
    """Response for balance information."""
    pass

class PeersResponse(BaseResponse):
    """Response for peers information."""
    pass

class BlockInfoResponse(BaseResponse):
    """Response for block information."""
    pass

class AccountInfoResponse(BaseResponse):
    """Response for account information."""
    pass

class ChainHeadResponse(BaseResponse):
    """Response for chain head information."""
    pass

class RuntimeVersionResponse(BaseResponse):
    """Response for runtime version information."""
    pass

# Validation responses
class ValidationResponse(BaseResponse):
    """Response for validation submission."""
    pass

class AttestationResponse(BaseResponse):
    """Response for attestation submission."""
    pass

class ProposalResponse(BaseResponse):
    """Response for proposal submission."""
    pass

class VoteResponse(BaseResponse):
    """Response for vote submission."""
    pass
