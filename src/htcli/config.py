"""
Configuration management for the Hypertensor CLI.
"""

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class NetworkConfig(BaseModel):
    """Network configuration."""

    endpoint: str = Field("wss://hypertensor.duckdns.org", description="RPC endpoint")
    ws_endpoint: str = Field(
        "wss://hypertensor.duckdns.org", description="WebSocket endpoint"
    )
    timeout: int = Field(30, description="Connection timeout in seconds")
    retry_attempts: int = Field(3, description="Number of retry attempts")


class OutputConfig(BaseModel):
    """Output configuration."""

    format: str = Field("table", description="Output format (table/json/csv)")
    verbose: bool = Field(False, description="Verbose output")
    color: bool = Field(True, description="Enable colored output")
    color_scheme: str = Field(
        "default", description="Color scheme (default/dark/light/high_contrast/soft)"
    )


class FilterConfig(BaseModel):
    """Filter configuration."""

    mine: bool = Field(False, description="Filter results to show only user assets")


class WalletConfig(BaseModel):
    """Wallet configuration."""

    path: str = Field("~/.htcli/wallets", description="Wallet storage path")
    default_name: str = Field("default", description="Default wallet name")
    encryption_enabled: bool = Field(True, description="Enable wallet encryption")


class Config(BaseModel):
    """Main configuration."""

    network: NetworkConfig = Field(default_factory=NetworkConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    wallet: WalletConfig = Field(default_factory=WalletConfig)
    filter: FilterConfig = Field(default_factory=FilterConfig)


def load_config(config_file: Optional[Path] = None) -> Config:
    """Load configuration from file or use defaults."""
    if config_file and config_file.exists():
        # Load from file
        import yaml

        with open(config_file, "r") as f:
            config_data = yaml.safe_load(f)
        return Config(**config_data)
    else:
        # Use environment variables or defaults
        network_config = NetworkConfig(
            endpoint=os.getenv(
                "HTCLI_NETWORK_ENDPOINT", "wss://hypertensor.duckdns.org"
            ),
            ws_endpoint=os.getenv(
                "HTCLI_NETWORK_WS_ENDPOINT", "wss://hypertensor.duckdns.org"
            ),
            timeout=int(os.getenv("HTCLI_NETWORK_TIMEOUT", "30")),
            retry_attempts=int(os.getenv("HTCLI_NETWORK_RETRY_ATTEMPTS", "3")),
        )

        output_config = OutputConfig(
            format=os.getenv("HTCLI_OUTPUT_FORMAT", "table"),
            verbose=os.getenv("HTCLI_OUTPUT_VERBOSE", "false").lower() == "true",
            color=os.getenv("HTCLI_OUTPUT_COLOR", "true").lower() == "true",
            color_scheme=os.getenv("HTCLI_OUTPUT_COLOR_SCHEME", "default"),
        )

        wallet_config = WalletConfig(
            path=os.getenv("HTCLI_WALLET_PATH", "~/.htcli/wallets"),
            default_name=os.getenv("HTCLI_WALLET_DEFAULT_NAME", "default"),
            encryption_enabled=os.getenv(
                "HTCLI_WALLET_ENCRYPTION_ENABLED", "true"
            ).lower()
            == "true",
        )

        filter_config = FilterConfig(
            mine=os.getenv("HTCLI_FILTER_MINE", "false").lower() == "true"
        )

        return Config(
            network=network_config,
            output=output_config,
            wallet=wallet_config,
            filter=filter_config,
        )


# Global configuration instance
config_instance = load_config()
