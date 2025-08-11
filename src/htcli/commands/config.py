"""
Configuration management commands for the Hypertensor CLI.
"""

import typer
import yaml
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel

from ..config import Config, NetworkConfig, OutputConfig, WalletConfig
from ..utils.formatting import print_success, print_error, print_info
from ..utils.validation import validate_url, validate_path

app = typer.Typer(name="config", help="Configuration management")
console = Console()

# Default configuration file path
DEFAULT_CONFIG_DIR = Path.home() / ".htcli"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.yaml"


def get_config_path(custom_path: Optional[str] = None) -> Path:
    """Get the configuration file path."""
    if custom_path:
        return Path(custom_path).expanduser()
    return DEFAULT_CONFIG_FILE


def create_config_dir(config_path: Path):
    """Create configuration directory if it doesn't exist."""
    config_dir = config_path.parent
    if not config_dir.exists():
        config_dir.mkdir(parents=True, exist_ok=True)
        print_info(f"Created configuration directory: {config_dir}")


def format_yaml_with_comments(config: Config) -> str:
    """Format configuration as YAML with comments."""
    yaml_content = f"""# Hypertensor CLI Configuration
# This file contains the configuration settings for the Hypertensor CLI tool.
# You can edit this file directly or use 'htcli config init' to regenerate it.

# Network Configuration
# Settings for connecting to the Hypertensor blockchain network
network:
  # RPC endpoint for blockchain communication
  endpoint: "{config.network.endpoint}"

  # WebSocket endpoint for real-time communication
  ws_endpoint: "{config.network.ws_endpoint}"

  # Connection timeout in seconds
  timeout: {config.network.timeout}

  # Number of retry attempts for failed connections
  retry_attempts: {config.network.retry_attempts}

# Output Configuration
# Settings for CLI output formatting and display
output:
  # Default output format (table, json, csv)
  format: "{config.output.format}"

  # Enable verbose output with detailed information
  verbose: {str(config.output.verbose).lower()}

  # Enable colored output in terminal
  color: {str(config.output.color).lower()}

# Wallet Configuration
# Settings for wallet and key management
wallet:
  # Path where wallets and keys are stored
  path: "{config.wallet.path}"

  # Default wallet name to use
  default_name: "{config.wallet.default_name}"

  # Enable wallet encryption for security
  encryption_enabled: {str(config.wallet.encryption_enabled).lower()}
"""
    return yaml_content


def load_existing_config(config_path: Path) -> Optional[Config]:
    """Load existing configuration file."""
    try:
        if config_path.exists():
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)
            return Config(**config_data)
    except Exception as e:
        print_error(f"Error loading existing config: {str(e)}")
    return None


def save_config(config: Config, config_path: Path):
    """Save configuration to YAML file."""
    try:
        create_config_dir(config_path)

        # Format with comments
        yaml_content = format_yaml_with_comments(config)

        with open(config_path, 'w') as f:
            f.write(yaml_content)

        print_success(f"Configuration saved to: {config_path}")
    except Exception as e:
        print_error(f"Failed to save configuration: {str(e)}")
        raise typer.Exit(1)


def prompt_network_config(existing: Optional[NetworkConfig] = None) -> NetworkConfig:
    """Prompt user for network configuration."""
    console.print("\n[bold blue]Network Configuration[/bold blue]")
    console.print("Configure how the CLI connects to the Hypertensor blockchain.\n")

    # RPC Endpoint
    default_endpoint = existing.endpoint if existing else "wss://hypertensor.duckdns.org"
    endpoint = Prompt.ask(
        "RPC Endpoint (WebSocket URL for blockchain communication)",
        default=default_endpoint
    )

    while not validate_url(endpoint):
        print_error("Invalid URL format. Please enter a valid WebSocket URL (wss://).")
        endpoint = Prompt.ask("RPC Endpoint", default=default_endpoint)

    # WebSocket Endpoint
    default_ws = existing.ws_endpoint if existing else endpoint
    ws_endpoint = Prompt.ask(
        "WebSocket Endpoint (for real-time communication)",
        default=default_ws
    )

    while not validate_url(ws_endpoint):
        print_error("Invalid URL format. Please enter a valid WebSocket URL (wss://).")
        ws_endpoint = Prompt.ask("WebSocket Endpoint", default=default_ws)

    # Timeout
    default_timeout = existing.timeout if existing else 30
    timeout_str = Prompt.ask(
        "Connection timeout (seconds)",
        default=str(default_timeout)
    )

    try:
        timeout = int(timeout_str)
        if timeout <= 0:
            raise ValueError()
    except ValueError:
        print_error("Invalid timeout. Using default value of 30 seconds.")
        timeout = 30

    # Retry attempts
    default_retry = existing.retry_attempts if existing else 3
    retry_str = Prompt.ask(
        "Retry attempts for failed connections",
        default=str(default_retry)
    )

    try:
        retry_attempts = int(retry_str)
        if retry_attempts < 0:
            raise ValueError()
    except ValueError:
        print_error("Invalid retry attempts. Using default value of 3.")
        retry_attempts = 3

    return NetworkConfig(
        endpoint=endpoint,
        ws_endpoint=ws_endpoint,
        timeout=timeout,
        retry_attempts=retry_attempts
    )


def prompt_output_config(existing: Optional[OutputConfig] = None) -> OutputConfig:
    """Prompt user for output configuration."""
    console.print("\n[bold green]Output Configuration[/bold green]")
    console.print("Configure how the CLI displays information.\n")

    # Output format
    default_format = existing.format if existing else "table"
    format_choice = Prompt.ask(
        "Default output format",
        choices=["table", "json", "csv"],
        default=default_format
    )

    # Verbose output
    default_verbose = existing.verbose if existing else False
    verbose = Confirm.ask(
        "Enable verbose output by default?",
        default=default_verbose
    )

    # Colored output
    default_color = existing.color if existing else True
    color = Confirm.ask(
        "Enable colored output in terminal?",
        default=default_color
    )

    return OutputConfig(
        format=format_choice,
        verbose=verbose,
        color=color
    )


def prompt_wallet_config(existing: Optional[WalletConfig] = None) -> WalletConfig:
    """Prompt user for wallet configuration."""
    console.print("\n[bold yellow]Wallet Configuration[/bold yellow]")
    console.print("Configure wallet and key management settings.\n")

    # Wallet path
    default_path = existing.path if existing else "~/.htcli/wallets"
    wallet_path = Prompt.ask(
        "Wallet storage path (where keys will be stored)",
        default=default_path
    )

    # Expand and validate path
    expanded_path = Path(wallet_path).expanduser()
    if not validate_path(str(expanded_path.parent)):
        print_error("Invalid path. Using default path.")
        wallet_path = "~/.htcli/wallets"

    # Default wallet name
    default_name = existing.default_name if existing else "default"
    wallet_name = Prompt.ask(
        "Default wallet name",
        default=default_name
    )

    # Encryption
    default_encryption = existing.encryption_enabled if existing else True
    encryption = Confirm.ask(
        "Enable wallet encryption for security?",
        default=default_encryption
    )

    return WalletConfig(
        path=wallet_path,
        default_name=wallet_name,
        encryption_enabled=encryption
    )


@app.command()
def init(
    config_file: Optional[str] = typer.Option(
        None,
        "--config",
        "-c",
        help="Custom configuration file path"
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite existing configuration"
    )
):
    """Initialize Hypertensor CLI configuration interactively."""
    config_path = get_config_path(config_file)

    # Check if config exists
    existing_config = None
    if config_path.exists() and not force:
        console.print(f"\n[yellow]⚠️  Configuration file already exists: {config_path}[/yellow]")

        if not Confirm.ask("Do you want to update the existing configuration?"):
            print_info("Configuration initialization cancelled.")
            return

        existing_config = load_existing_config(config_path)

    # Welcome message
    console.print(Panel.fit(
        "[bold cyan]Hypertensor CLI Configuration Setup[/bold cyan]\n\n"
        "This wizard will help you configure the Hypertensor CLI.\n"
        "Press [bold]Enter[/bold] to use default values or type your preferred settings.",
        title="Welcome",
        border_style="cyan"
    ))

    try:
        # Collect configuration
        network_config = prompt_network_config(
            existing_config.network if existing_config else None
        )

        output_config = prompt_output_config(
            existing_config.output if existing_config else None
        )

        wallet_config = prompt_wallet_config(
            existing_config.wallet if existing_config else None
        )

        # Create final configuration
        config = Config(
            network=network_config,
            output=output_config,
            wallet=wallet_config
        )

        # Show summary
        console.print("\n[bold cyan]Configuration Summary[/bold cyan]")
        show_config_summary(config)

        # Confirm and save
        console.print(f"\nConfiguration will be saved to: [bold]{config_path}[/bold]")

        if Confirm.ask("\nSave this configuration?", default=True):
            save_config(config, config_path)

            # Show next steps
            console.print(Panel.fit(
                "[bold green]Configuration Complete![/bold green]\n\n"
                f"Your configuration has been saved to:\n[bold]{config_path}[/bold]\n\n"
                "You can now use the Hypertensor CLI with your custom settings.\n"
                "Use [bold]htcli config show[/bold] to view your current configuration.",
                title="Success",
                border_style="green"
            ))
        else:
            print_info("Configuration not saved.")

    except KeyboardInterrupt:
        print_info("\nConfiguration initialization cancelled.")
        raise typer.Exit(0)
    except Exception as e:
        print_error(f"Configuration initialization failed: {str(e)}")
        raise typer.Exit(1)


def show_config_summary(config: Config):
    """Display configuration summary in a nice table format."""

    # Network table
    network_table = Table(title="Network", show_header=True, header_style="bold blue")
    network_table.add_column("Setting", style="cyan")
    network_table.add_column("Value", style="white")

    network_table.add_row("RPC Endpoint", config.network.endpoint)
    network_table.add_row("WebSocket Endpoint", config.network.ws_endpoint)
    network_table.add_row("Timeout", f"{config.network.timeout}s")
    network_table.add_row("Retry Attempts", str(config.network.retry_attempts))

    console.print(network_table)

    # Output table
    network_table.add_row("Retry Attempts", str(config.network.retry_attempts))

    console.print(network_table)

    # Output table
    output_table = Table(title="Output", show_header=True, header_style="bold green")
    output_table.add_column("Setting", style="cyan")
    output_table.add_column("Value", style="white")

    output_table.add_row("Default Format", config.output.format)
    output_table.add_row("Verbose", "Yes" if config.output.verbose else "No")
    output_table.add_row("Colored Output", "Yes" if config.output.color else "No")

    console.print(output_table)

    # Wallet table
    wallet_table = Table(title="Wallet", show_header=True, header_style="bold yellow")
    wallet_table.add_column("Setting", style="cyan")
    wallet_table.add_column("Value", style="white")

    wallet_table.add_row("Storage Path", config.wallet.path)
    wallet_table.add_row("Default Name", config.wallet.default_name)
    wallet_table.add_row("Encryption", "Enabled" if config.wallet.encryption_enabled else "Disabled")

    console.print(wallet_table)


@app.command()
def show(
    config_file: Optional[str] = typer.Option(
        None,
        "--config",
        "-c",
        help="Custom configuration file path"
    ),
    format_type: str = typer.Option(
        "table",
        "--format",
        "-f",
        help="Output format (table/yaml/json)"
    )
):
    """Show current configuration."""
    config_path = get_config_path(config_file)

    if not config_path.exists():
        print_error(f"Configuration file not found: {config_path}")
        console.print("\nRun [bold]htcli config init[/bold] to create a configuration file.")
        raise typer.Exit(1)

    try:
        config = load_existing_config(config_path)
        if not config:
            print_error("Failed to load configuration file.")
            raise typer.Exit(1)

        console.print(f"\n[bold]Configuration file: {config_path}[/bold]\n")

        if format_type == "table":
            show_config_summary(config)
        elif format_type == "yaml":
            console.print(format_yaml_with_comments(config))
        elif format_type == "json":
            console.print_json(data=config.dict())
        else:
            print_error("Invalid format. Use: table, yaml, or json")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"Failed to show configuration: {str(e)}")
        raise typer.Exit(1)


@app.command()
def path(
    config_file: Optional[str] = typer.Option(
        None,
        "--config",
        "-c",
        help="Custom configuration file path"
    )
):
    """Show configuration file path."""
    config_path = get_config_path(config_file)

    console.print(f"Configuration file path: [bold]{config_path}[/bold]")

    if config_path.exists():
        console.print("File exists")
    else:
        console.print("File does not exist")
        console.print("\nRun [bold]htcli config init[/bold] to create the configuration file.")


@app.command()
def edit(
    config_file: Optional[str] = typer.Option(
        None,
        "--config",
        "-c",
        help="Custom configuration file path"
    )
):
    """Edit configuration interactively in the terminal."""
    config_path = get_config_path(config_file)

    if not config_path.exists():
        print_error(f"Configuration file not found: {config_path}")
        console.print("\nRun [bold]htcli config init[/bold] to create a configuration file.")
        raise typer.Exit(1)

    try:
        # Load existing configuration
        existing_config = load_existing_config(config_path)
        if not existing_config:
            print_error("Failed to load existing configuration.")
            raise typer.Exit(1)

        console.print(Panel.fit(
            "[bold cyan]Configuration Editor[/bold cyan]\n\n"
            "You can edit your configuration settings interactively.\n"
            "Press [bold]Enter[/bold] to keep current values or type new values.",
            title="Welcome",
            border_style="cyan"
        ))

        # Edit configuration sections
        console.print("\n[bold blue]Network Configuration[/bold blue]")
        network_config = prompt_network_config(existing_config.network)

        console.print("\n[bold green]Output Configuration[/bold green]")
        output_config = prompt_output_config(existing_config.output)

        console.print("\n[bold yellow]Wallet Configuration[/bold yellow]")
        wallet_config = prompt_wallet_config(existing_config.wallet)

        # Create updated configuration
        updated_config = Config(
            network=network_config,
            output=output_config,
            wallet=wallet_config
        )

        # Show changes summary
        console.print("\n[bold cyan]Configuration Changes Summary[/bold cyan]")
        show_config_changes(existing_config, updated_config)

        # Confirm and save
        if Confirm.ask("\nSave these changes?", default=True):
            save_config(updated_config, config_path)
            print_success("Configuration updated successfully!")
        else:
            print_info("Changes not saved.")

    except KeyboardInterrupt:
        print_info("\nConfiguration editing cancelled.")
        raise typer.Exit(0)
    except Exception as e:
        print_error(f"Configuration editing failed: {str(e)}")
        raise typer.Exit(1)


def show_config_changes(old_config: Config, new_config: Config):
    """Display configuration changes in a comparison table."""
    
    # Network changes
    network_table = Table(title="Network Configuration Changes", show_header=True, header_style="bold blue")
    network_table.add_column("Setting", style="cyan")
    network_table.add_column("Old Value", style="red")
    network_table.add_column("New Value", style="green")
    network_table.add_column("Changed", style="yellow")

    network_changes = [
        ("RPC Endpoint", old_config.network.endpoint, new_config.network.endpoint),
        ("WebSocket Endpoint", old_config.network.ws_endpoint, new_config.network.ws_endpoint),
        ("Timeout", f"{old_config.network.timeout}s", f"{new_config.network.timeout}s"),
        ("Retry Attempts", str(old_config.network.retry_attempts), str(new_config.network.retry_attempts))
    ]

    for setting, old_val, new_val in network_changes:
        changed = "Yes" if old_val != new_val else "No"
        network_table.add_row(setting, old_val, new_val, changed)

    console.print(network_table)

    # Output changes
    output_table = Table(title="Output Configuration Changes", show_header=True, header_style="bold green")
    output_table.add_column("Setting", style="cyan")
    output_table.add_column("Old Value", style="red")
    output_table.add_column("New Value", style="green")
    output_table.add_column("Changed", style="yellow")

    output_changes = [
        ("Default Format", old_config.output.format, new_config.output.format),
        ("Verbose", "Yes" if old_config.output.verbose else "No", "Yes" if new_config.output.verbose else "No"),
        ("Colored Output", "Yes" if old_config.output.color else "No", "Yes" if new_config.output.color else "No")
    ]

    for setting, old_val, new_val in output_changes:
        changed = "Yes" if old_val != new_val else "No"
        output_table.add_row(setting, old_val, new_val, changed)

    console.print(output_table)

    # Wallet changes
    wallet_table = Table(title="Wallet Configuration Changes", show_header=True, header_style="bold yellow")
    wallet_table.add_column("Setting", style="cyan")
    wallet_table.add_column("Old Value", style="red")
    wallet_table.add_column("New Value", style="green")
    wallet_table.add_column("Changed", style="yellow")

    wallet_changes = [
        ("Storage Path", old_config.wallet.path, new_config.wallet.path),
        ("Default Name", old_config.wallet.default_name, new_config.wallet.default_name),
        ("Encryption", "Enabled" if old_config.wallet.encryption_enabled else "Disabled", 
         "Enabled" if new_config.wallet.encryption_enabled else "Disabled")
    ]

    for setting, old_val, new_val in wallet_changes:
        changed = "Yes" if old_val != new_val else "No"
        wallet_table.add_row(setting, old_val, new_val, changed)

    console.print(wallet_table)


@app.command()
def validate(
    config_file: Optional[str] = typer.Option(
        None,
        "--config",
        "-c",
        help="Custom configuration file path"
    )
):
    """Validate configuration file."""
    config_path = get_config_path(config_file)

    if not config_path.exists():
        print_error(f"Configuration file not found: {config_path}")
        raise typer.Exit(1)

    try:
        config = load_existing_config(config_path)
        if config:
            print_success("Configuration file is valid!")
            console.print(f"Configuration loaded successfully from: [bold]{config_path}[/bold]")
        else:
            print_error("Configuration file is invalid!")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"Configuration validation failed: {str(e)}")
        raise typer.Exit(1)
