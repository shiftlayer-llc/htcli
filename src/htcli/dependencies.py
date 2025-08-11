"""
Dependencies for the Hypertensor CLI.
"""

from typing import Optional
from .client import HypertensorClient
from .config import Config

# Global client instance and config
_client: Optional[HypertensorClient] = None
_config: Optional[Config] = None


def set_client(client: HypertensorClient):
    """Set the global client instance."""
    global _client
    _client = client


def set_config(config: Config):
    """Set the global config instance for lazy client initialization."""
    global _config
    _config = config


def get_client() -> HypertensorClient:
    """Get the global client instance, initializing it lazily if needed."""
    global _client, _config

    if _client is None:
        if _config is None:
            raise RuntimeError(
                "Configuration not set. Please ensure config is loaded before using client."
            )

        # Initialize client only when first requested
        _client = HypertensorClient(_config)

    return _client


def get_config() -> Optional[Config]:
    """Get the global config instance."""
    return _config
