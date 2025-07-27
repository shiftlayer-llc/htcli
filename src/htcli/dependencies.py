"""
Dependencies for the Hypertensor CLI.
"""

from typing import Optional
from .client import HypertensorClient

# Global client instance
_client: Optional[HypertensorClient] = None


def set_client(client: HypertensorClient):
    """Set the global client instance."""
    global _client
    _client = client


def get_client() -> Optional[HypertensorClient]:
    """Get the global client instance."""
    return _client
