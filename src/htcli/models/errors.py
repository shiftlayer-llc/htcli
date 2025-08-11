"""
Pydantic models for error structures.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ErrorResponse(BaseModel):
    """Standard error response model."""

    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    code: int = Field(..., description="Error code")
    details: Optional[Dict[str, Any]] = Field(
        None, description="Optional error details"
    )
    timestamp: str = Field(..., description="ISO timestamp")


class ValidationError(BaseModel):
    """Validation error model."""

    field: str = Field(..., description="Field name")
    value: Any = Field(..., description="Invalid value")
    constraint: str = Field(..., description="Constraint that was violated")


class NetworkError(BaseModel):
    """Network error model."""

    endpoint: str = Field(..., description="Failed endpoint")
    status_code: Optional[int] = Field(None, description="HTTP status code")
    timeout: bool = Field(False, description="Whether the error was due to timeout")


class RPCError(BaseModel):
    """RPC error model."""

    method: str = Field(..., description="RPC method that failed")
    params: Optional[Dict[str, Any]] = Field(None, description="RPC parameters")
    error_code: Optional[int] = Field(None, description="RPC error code")


class BusinessLogicError(BaseModel):
    """Business logic error model."""

    operation: str = Field(..., description="Operation that failed")
    reason: str = Field(..., description="Reason for failure")
    recoverable: bool = Field(True, description="Whether the error is recoverable")


# Error code ranges
ERROR_CODES = {
    "AuthenticationFailed": (1001, 1999),
    "ValidationError": (2001, 2999),
    "NetworkError": (3001, 3999),
    "RPCError": (4001, 4999),
    "BusinessLogicError": (5001, 5999),
    "SubnetError": (6001, 6999),
    "StakingError": (7001, 7999),
    "ValidationError": (8001, 8999),
    "GovernanceError": (9001, 9999),
}

# Specific error codes
SPECIFIC_ERROR_CODES = {
    # Subnet errors
    "INVALID_SUBNET_PATH": 1001,
    "INSUFFICIENT_MEMORY": 1002,
    "INVALID_REGISTRATION_PERIOD": 1003,
    "DUPLICATE_SUBNET_PATH": 1004,
    "INSUFFICIENT_BALANCE_FOR_REGISTRATION": 1005,
    "SUBNET_NOT_FOUND": 2001,
    "SUBNET_ALREADY_ACTIVATED": 2002,
    "INSUFFICIENT_NODES_FOR_ACTIVATION": 2003,
    "REGISTRATION_PERIOD_NOT_COMPLETED": 2004,
    # Node errors
    "SUBNET_NOT_ACTIVATED": 4002,
    "NODE_ALREADY_EXISTS": 4003,
    "INVALID_PEER_ID_FORMAT": 4004,
    "INSUFFICIENT_STAKE_FOR_NODE": 4005,
    # Staking errors
    "NODE_NOT_FOUND": 5002,
    "INSUFFICIENT_BALANCE": 5003,
    "INVALID_STAKE_AMOUNT": 5004,
    "STAKE_LIMIT_EXCEEDED": 5005,
    "INSUFFICIENT_STAKE_TO_REMOVE": 6002,
    "STAKE_STILL_IN_UNBONDING_PERIOD": 6003,
    # Validation errors
    "SUBNET_NOT_ACTIVE": 7002,
    "INVALID_VALIDATION_DATA": 7003,
    "VALIDATION_RATE_LIMIT_EXCEEDED": 7004,
    # Governance errors
    "INVALID_PROPOSAL_DATA": 8003,
    "INSUFFICIENT_STAKE_FOR_PROPOSAL": 8004,
    "PROPOSAL_NOT_FOUND": 9001,
    "INVALID_VOTE_TYPE": 9002,
    "ALREADY_VOTED": 9003,
    "VOTING_PERIOD_ENDED": 9004,
}
