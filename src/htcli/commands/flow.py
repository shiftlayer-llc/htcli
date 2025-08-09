"""
Automated Flow Commands

Provides access to automated workflows that combine multiple CLI operations
into streamlined, user-friendly processes.
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..flows import AVAILABLE_FLOWS
from ..utils.formatting import print_success, print_error, print_info

app = typer.Typer(name="flow", help="Automated workflows for common tasks")
console = Console()


@app.command()
def list():
    """List all available automated flows"""
    table = Table(title="Available Automated Flows")
    table.add_column("Flow Name", style="cyan", width=25)
    table.add_column("Description", style="white", width=60)
    table.add_column("Use Case", style="yellow", width=25)

    flow_info = [
        ("subnet-deployment", "Complete subnet creation with node and stake", "Subnet creators"),
        ("node-onboarding", "Join existing subnet as node operator", "Node operators"),
        ("staking-portfolio", "Set up diversified staking across multiple targets", "Investors"),
        ("development-setup", "Create development environment for testing", "Developers"),
        ("migration-recovery", "Migrate assets or recover from configuration issues", "Migration/Recovery")
    ]

    for flow_key, description, use_case in flow_info:
        table.add_row(flow_key, description, use_case)

    console.print(table)

    console.print("\nTo run a flow:")
    console.print("htcli flow run <flow-name>")
    console.print("\nTo get detailed information about a flow:")
    console.print("htcli flow info <flow-name>")


@app.command()
def info(
    flow_name: str = typer.Argument(..., help="Flow name to get information about")
):
    """Get detailed information about a specific flow"""
    if flow_name not in AVAILABLE_FLOWS:
        available = ", ".join(AVAILABLE_FLOWS.keys())
        print_error(f"Flow '{flow_name}' not found. Available flows: {available}")
        raise typer.Exit(1)

    flow_class = AVAILABLE_FLOWS[flow_name]

    # Create temporary instance to get info
    flow_instance = flow_class()

    info_content = f"""
{flow_instance.description}

This flow automates multiple related operations to provide a seamless
user experience with minimal manual intervention.

Steps Overview:
The flow consists of multiple automated steps that handle:
- Configuration and setup
- Wallet and key management
- Blockchain operations
- Verification and monitoring

Benefits:
- Saves time by automating repetitive tasks
- Reduces errors through guided processes
- Provides comprehensive validation
- Includes helpful guidance and feedback

Usage:
htcli flow run {flow_name}
    """.strip()

    panel = Panel(
        info_content,
        title=f"Flow Information: {flow_instance.name}",
        border_style="blue"
    )

    console.print(panel)


@app.command()
def run(
    flow_name: str = typer.Argument(..., help="Flow name to execute"),
    skip_confirmation: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompts where possible")
):
    """Execute an automated flow"""
    if flow_name not in AVAILABLE_FLOWS:
        available = ", ".join(AVAILABLE_FLOWS.keys())
        print_error(f"Flow '{flow_name}' not found. Available flows: {available}")
        raise typer.Exit(1)

    flow_class = AVAILABLE_FLOWS[flow_name]

    try:
        # Create and execute flow
        flow_instance = flow_class(console=console)

        # Add skip confirmation to context if specified
        if skip_confirmation:
            flow_instance.add_to_context("skip_confirmation", True)

        # Execute the flow
        result = flow_instance.execute()

        # Handle result
        if result.status.value == "completed":
            print_success(f"Flow '{flow_name}' completed successfully!")

            # Show any relevant output data
            if result.data:
                summary_data = result.data.get("deployment_summary") or \
                              result.data.get("portfolio_summary") or \
                              result.data.get("testing_summary") or \
                              result.data.get("recovery_summary")

                if summary_data:
                    console.print("\nFlow Results:")
                    for key, value in summary_data.items():
                        console.print(f"  {key}: {value}")

        elif result.status.value == "cancelled":
            print_info(f"Flow '{flow_name}' was cancelled by user")
            raise typer.Exit(0)

        else:
            print_error(f"Flow '{flow_name}' failed: {result.error_message}")
            if result.failed_step:
                print_error(f"Failed at step: {result.failed_step}")
            raise typer.Exit(1)

    except KeyboardInterrupt:
        print_info("Flow interrupted by user")
        raise typer.Exit(0)
    except Exception as e:
        print_error(f"Flow execution failed: {str(e)}")
        raise typer.Exit(1)


@app.command()
def status():
    """Show status of flow system"""
    status_info = f"""
Automated Flow System Status

Available Flows: {len(AVAILABLE_FLOWS)}
System Status: Operational

Flow Categories:
- Infrastructure: subnet-deployment, node-onboarding
- Investment: staking-portfolio
- Development: development-setup
- Operations: migration-recovery

Usage Statistics:
- Total flows available: {len(AVAILABLE_FLOWS)}
- Average steps per flow: ~6-8
- Typical completion time: 2-10 minutes

For help with flows:
- List flows: htcli flow list
- Flow info: htcli flow info <name>
- Run flow: htcli flow run <name>
    """.strip()

    panel = Panel(
        status_info,
        title="Flow System Status",
        border_style="green"
    )

    console.print(panel)


if __name__ == "__main__":
    app()
