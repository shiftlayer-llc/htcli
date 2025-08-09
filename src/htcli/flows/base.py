"""
Base Flow Implementation

Provides the foundation for all automated flows with common functionality,
error handling, and user interaction patterns.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.prompt import Confirm

from ..dependencies import get_client
from ..utils.formatting import print_error, print_info


class FlowStatus(Enum):
    """Flow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class FlowStep:
    """Individual step within a flow"""
    name: str
    description: str
    function: Callable
    required: bool = True
    timeout: int = 30
    retry_count: int = 3
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class FlowResult:
    """Result of flow execution"""
    status: FlowStatus
    completed_steps: List[str]
    failed_step: Optional[str] = None
    error_message: Optional[str] = None
    data: Dict[str, Any] = None
    execution_time: float = 0.0

    def __post_init__(self):
        if self.data is None:
            self.data = {}


class BaseFlow(ABC):
    """
    Base class for all automated flows.

    Provides common functionality for:
    - Step management and execution
    - Error handling and recovery
    - User interaction and feedback
    - Progress tracking and reporting
    """

    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
        self.client = get_client()
        self.steps: List[FlowStep] = []
        self.context: Dict[str, Any] = {}
        self.start_time: float = 0.0

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable flow name"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Detailed flow description"""
        pass

    @abstractmethod
    def setup_steps(self) -> List[FlowStep]:
        """Define the steps for this flow"""
        pass

    @abstractmethod
    def collect_inputs(self) -> Dict[str, Any]:
        """Collect required inputs from user"""
        pass

    def initialize(self) -> bool:
        """Initialize the flow with user inputs"""
        try:
            self.console.print(f"\n{self.name}", style="bold blue")
            self.console.print(f"{self.description}\n")

            # Collect user inputs
            inputs = self.collect_inputs()
            self.context.update(inputs)

            # Setup steps
            self.steps = self.setup_steps()

            # Show flow summary
            self.show_flow_summary()

            return Confirm.ask("Do you want to proceed with this flow?")

        except KeyboardInterrupt:
            print_info("Flow cancelled by user")
            return False
        except Exception as e:
            print_error(f"Failed to initialize flow: {str(e)}")
            return False

    def execute(self) -> FlowResult:
        """Execute the complete flow"""
        if not self.initialize():
            return FlowResult(
                status=FlowStatus.CANCELLED,
                completed_steps=[],
                error_message="Flow cancelled during initialization"
            )

        self.start_time = time.time()
        completed_steps = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:

            for step in self.steps:
                if not self.check_dependencies(step, completed_steps):
                    return FlowResult(
                        status=FlowStatus.FAILED,
                        completed_steps=completed_steps,
                        failed_step=step.name,
                        error_message=f"Dependencies not met for step: {step.name}",
                        execution_time=time.time() - self.start_time
                    )

                task = progress.add_task(f"Executing: {step.description}", total=None)

                try:
                    # Execute step with retries
                    success = self.execute_step_with_retry(step)

                    if success:
                        completed_steps.append(step.name)
                        progress.update(task, description=f"Completed: {step.description}")
                        time.sleep(0.5)  # Brief pause for user feedback
                    else:
                        if step.required:
                            return FlowResult(
                                status=FlowStatus.FAILED,
                                completed_steps=completed_steps,
                                failed_step=step.name,
                                error_message=f"Required step failed: {step.name}",
                                execution_time=time.time() - self.start_time
                            )
                        else:
                            print_info(f"Optional step skipped: {step.name}")

                except KeyboardInterrupt:
                    return FlowResult(
                        status=FlowStatus.CANCELLED,
                        completed_steps=completed_steps,
                        failed_step=step.name,
                        error_message="Flow cancelled by user",
                        execution_time=time.time() - self.start_time
                    )

                progress.remove_task(task)

        # Flow completed successfully
        execution_time = time.time() - self.start_time
        result = FlowResult(
            status=FlowStatus.COMPLETED,
            completed_steps=completed_steps,
            data=self.context,
            execution_time=execution_time
        )

        self.show_completion_summary(result)
        return result

    def execute_step_with_retry(self, step: FlowStep) -> bool:
        """Execute a step with retry logic"""
        for attempt in range(step.retry_count):
            try:
                return step.function(self.context)
            except Exception as e:
                if attempt == step.retry_count - 1:
                    print_error(f"Step '{step.name}' failed after {step.retry_count} attempts: {str(e)}")
                    return False
                else:
                    print_info(f"Step '{step.name}' failed, retrying... (attempt {attempt + 1}/{step.retry_count})")
                    time.sleep(2 ** attempt)  # Exponential backoff

        return False

    def check_dependencies(self, step: FlowStep, completed_steps: List[str]) -> bool:
        """Check if step dependencies are satisfied"""
        for dependency in step.dependencies:
            if dependency not in completed_steps:
                return False
        return True

    def show_flow_summary(self):
        """Display flow summary to user"""
        table = Table(title=f"{self.name} - Execution Plan")
        table.add_column("Step", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Required", style="yellow")

        for i, step in enumerate(self.steps, 1):
            required = "Yes" if step.required else "No"
            table.add_row(f"{i}. {step.name}", step.description, required)

        self.console.print(table)
        self.console.print()

    def show_completion_summary(self, result: FlowResult):
        """Display completion summary"""
        if result.status == FlowStatus.COMPLETED:
            panel_content = f"""
Flow completed successfully!

Execution time: {result.execution_time:.2f} seconds
Steps completed: {len(result.completed_steps)}/{len(self.steps)}

Your resources are now ready for use.
            """
            panel = Panel(panel_content, title="Flow Completed", border_style="green")
        else:
            panel_content = f"""
Flow failed or was cancelled.

Status: {result.status.value}
Steps completed: {len(result.completed_steps)}/{len(self.steps)}
Failed step: {result.failed_step or 'N/A'}
Error: {result.error_message or 'N/A'}
            """
            panel = Panel(panel_content, title="Flow Failed", border_style="red")

        self.console.print(panel)

    def add_to_context(self, key: str, value: Any):
        """Add data to flow context"""
        self.context[key] = value

    def get_from_context(self, key: str, default: Any = None) -> Any:
        """Get data from flow context"""
        return self.context.get(key, default)
