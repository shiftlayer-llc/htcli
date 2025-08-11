"""
Development Environment Setup Flow

Automates the setup of a development environment for testing applications
on the Hypertensor network, including test subnet creation and basic tooling.

Flow Steps:
1. Configuration initialization
2. Development wallet setup
3. Test subnet registration and activation
4. Development node setup
5. Testing environment verification
6. Development tools configuration
"""

from typing import Dict, Any, List
from rich.prompt import Prompt, IntPrompt, Confirm

from .base import BaseFlow, FlowStep
from ..models.requests import SubnetRegisterRequest, SubnetNodeAddRequest
from ..utils.formatting import print_success, print_error, print_info
from ..utils.validation import validate_path


class DevelopmentSetupFlow(BaseFlow):
    """Development environment setup automation"""

    @property
    def name(self) -> str:
        return "Development Environment Setup"

    @property
    def description(self) -> str:
        return """
This flow automates development environment setup:
- Creates development-specific configuration
- Sets up test subnet with minimal requirements
- Configures development node for testing
- Provides testing tools and guidelines

Perfect for developers who need a quick testing environment.
        """.strip()

    def collect_inputs(self) -> Dict[str, Any]:
        """Collect development setup parameters"""
        self.console.print("Welcome to Development Environment Setup!\n")

        # Project information
        self.console.print("Project information:")
        project_name = Prompt.ask(
            "Project name (for subnet naming)", default="dev-project"
        )

        # Development configuration
        environment_type = Prompt.ask(
            "Environment type", choices=["local", "testnet", "staging"], default="local"
        )

        # Subnet configuration (minimal for development)
        self.console.print("\nTest subnet configuration:")
        memory_mb = IntPrompt.ask(
            "Memory requirement (MB)", default=512
        )  # Minimal for testing

        # Node configuration
        self.console.print("\nDevelopment node configuration:")
        use_mock_node = Confirm.ask("Use mock node for testing?", default=True)

        node_config = {"use_mock": use_mock_node}
        if not use_mock_node:
            hotkey = Prompt.ask("Real node hotkey address")
            peer_id = Prompt.ask("Real node peer ID")
            node_config.update({"hotkey": hotkey, "peer_id": peer_id})

        # Development tools
        self.console.print("\nDevelopment tools:")
        setup_monitoring = Confirm.ask("Set up development monitoring?", default=True)
        create_test_scripts = Confirm.ask(
            "Create test automation scripts?", default=True
        )

        return {
            "project_name": project_name,
            "environment_type": environment_type,
            "memory_mb": memory_mb,
            "node_config": node_config,
            "setup_monitoring": setup_monitoring,
            "create_test_scripts": create_test_scripts,
        }

    def setup_steps(self) -> List[FlowStep]:
        """Define development setup steps"""
        return [
            FlowStep(
                name="config_init",
                description="Initialize development configuration",
                function=self.step_config_init,
                required=True,
            ),
            FlowStep(
                name="dev_wallet_setup",
                description="Set up development wallet",
                function=self.step_dev_wallet_setup,
                required=True,
                dependencies=["config_init"],
            ),
            FlowStep(
                name="test_subnet_create",
                description="Create test subnet",
                function=self.step_test_subnet_create,
                required=True,
                dependencies=["dev_wallet_setup"],
            ),
            FlowStep(
                name="dev_node_setup",
                description="Set up development node",
                function=self.step_dev_node_setup,
                required=True,
                dependencies=["test_subnet_create"],
            ),
            FlowStep(
                name="testing_verification",
                description="Verify testing environment",
                function=self.step_testing_verification,
                required=True,
                dependencies=["dev_node_setup"],
            ),
            FlowStep(
                name="dev_tools_setup",
                description="Configure development tools",
                function=self.step_dev_tools_setup,
                required=False,
                dependencies=["testing_verification"],
            ),
        ]

    def step_config_init(self, context: Dict[str, Any]) -> bool:
        """Initialize development configuration"""
        try:
            # Create development-specific configuration
            env_type = context["environment_type"]

            dev_config = {
                "environment": env_type,
                "debug_mode": True,
                "verbose_logging": True,
                "test_mode": True,
            }

            context["dev_config"] = dev_config
            print_success(
                f"Development configuration initialized for {env_type} environment"
            )
            return True

        except Exception as e:
            print_error(f"Configuration initialization failed: {str(e)}")
            return False

    def step_dev_wallet_setup(self, context: Dict[str, Any]) -> bool:
        """Set up development wallet"""
        try:
            # Generate development wallet
            dev_key_name = f"dev-{context['project_name']}"

            response = self.client.wallet.generate_keypair(
                name=dev_key_name, key_type="sr25519"  # Standard for development
            )

            if response.get("success", False):
                context["dev_wallet_address"] = response.get("address")
                context["dev_key_name"] = dev_key_name
                print_success(f"Development wallet created: {response.get('address')}")

                # For development, we might need test tokens
                print_info(
                    "Note: For testing, ensure this address has sufficient test tokens"
                )
                return True
            else:
                print_error(
                    f"Development wallet setup failed: {response.get('message', 'Unknown error')}"
                )
                return False

        except Exception as e:
            print_error(f"Development wallet setup failed: {str(e)}")
            return False

    def step_test_subnet_create(self, context: Dict[str, Any]) -> bool:
        """Create test subnet"""
        try:
            project_name = context["project_name"]
            subnet_path = f"test-{project_name}"

            # Validate subnet path
            if not validate_path(subnet_path):
                subnet_path = f"test-subnet-{hash(project_name) % 10000}"

            request = SubnetRegisterRequest(
                path=subnet_path,
                memory_mb=context["memory_mb"],
                registration_blocks=100,  # Minimal for testing
                entry_interval=10,  # Fast for development
                max_node_registration_epochs=10,
                node_registration_interval=10,
                node_activation_interval=10,
                node_queue_period=10,
                max_node_penalties=3,
            )

            response = self.client.subnet.register_subnet(request)

            if response.success:
                subnet_id = response.data.get("subnet_id")
                context["test_subnet_id"] = subnet_id
                context["subnet_path"] = subnet_path
                print_success(
                    f"Test subnet created: ID {subnet_id}, Path: {subnet_path}"
                )

                # Activate immediately for development
                activate_response = self.client.subnet.activate_subnet(subnet_id)
                if activate_response.success:
                    print_success(f"Test subnet {subnet_id} activated")
                    return True
                else:
                    print_error(
                        f"Test subnet activation failed: {activate_response.message}"
                    )
                    return False
            else:
                print_error(f"Test subnet creation failed: {response.message}")
                return False

        except Exception as e:
            print_error(f"Test subnet creation failed: {str(e)}")
            return False

    def step_dev_node_setup(self, context: Dict[str, Any]) -> bool:
        """Set up development node"""
        try:
            node_config = context["node_config"]

            if node_config["use_mock"]:
                # Set up mock node for testing
                mock_node_config = {
                    "node_id": "mock-dev-node",
                    "type": "mock",
                    "hotkey": context["dev_wallet_address"],
                    "peer_id": f"QmMockDev{hash(context['project_name']) % 10000}",
                    "status": "active",
                }

                context["dev_node_config"] = mock_node_config
                print_success("Mock development node configured")
                return True
            else:
                # Set up real node
                request = SubnetNodeAddRequest(
                    subnet_id=context["test_subnet_id"],
                    hotkey=node_config["hotkey"],
                    peer_id=node_config["peer_id"],
                    stake_amount=10**18,  # Minimal stake for development
                )

                response = self.client.node.add_node(request)

                if response.success:
                    node_id = response.data.get("node_id")
                    context["dev_node_id"] = node_id
                    print_success(f"Development node added: ID {node_id}")
                    return True
                else:
                    print_error(f"Development node setup failed: {response.message}")
                    return False

        except Exception as e:
            print_error(f"Development node setup failed: {str(e)}")
            return False

    def step_testing_verification(self, context: Dict[str, Any]) -> bool:
        """Verify testing environment"""
        try:
            subnet_id = context["test_subnet_id"]

            # Verify subnet status
            subnet_response = self.client.subnet.get_subnet_data(subnet_id)
            if not subnet_response.success:
                print_error("Failed to verify test subnet")
                return False

            subnet_data = subnet_response.data

            # Verify basic connectivity
            network_response = self.client.chain.get_network_stats()
            if not network_response.success:
                print_error("Failed to verify network connectivity")
                return False

            # Create testing summary
            testing_summary = {
                "subnet_id": subnet_id,
                "subnet_path": context["subnet_path"],
                "wallet_address": context["dev_wallet_address"],
                "environment_type": context["environment_type"],
                "node_type": "mock" if context["node_config"]["use_mock"] else "real",
            }

            context["testing_summary"] = testing_summary
            print_success("Testing environment verification completed")
            return True

        except Exception as e:
            print_error(f"Testing environment verification failed: {str(e)}")
            return False

    def step_dev_tools_setup(self, context: Dict[str, Any]) -> bool:
        """Configure development tools"""
        try:
            project_name = context["project_name"]
            subnet_id = context["test_subnet_id"]
            wallet_address = context["dev_wallet_address"]

            dev_tools = {}

            # Set up monitoring if requested
            if context.get("setup_monitoring"):
                monitoring_commands = f"""
# Development Monitoring Commands
# Subnet status
htcli subnet info --subnet-id {subnet_id}

# Account balance
htcli chain balance --address {wallet_address}

# Network status
htcli chain network

# Your assets
htcli --mine subnet list
htcli --mine stake info
                """.strip()

                dev_tools["monitoring"] = monitoring_commands

            # Create test scripts if requested
            if context.get("create_test_scripts"):
                test_scripts = {
                    "basic_test": f"""
#!/bin/bash
# Basic connectivity test for {project_name}
echo "Testing Hypertensor CLI connectivity..."
htcli chain network
echo "Testing subnet access..."
htcli subnet info --subnet-id {subnet_id}
echo "Testing wallet access..."
htcli chain balance --address {wallet_address}
                    """.strip(),
                    "stake_test": f"""
#!/bin/bash
# Staking test script for {project_name}
echo "Testing stake operations..."
htcli stake info --address {wallet_address}
echo "Checking portfolio..."
htcli --mine stake info
                    """.strip(),
                }

                dev_tools["test_scripts"] = test_scripts

            # Development guidelines
            dev_guidelines = f"""
Development Environment Setup Complete!

Project: {project_name}
Environment: {context['environment_type']}
Test Subnet ID: {subnet_id}
Development Wallet: {wallet_address}

Quick Start Commands:
1. Check your environment: htcli chain network
2. View your test subnet: htcli subnet info --subnet-id {subnet_id}
3. Check your balance: htcli chain balance --address {wallet_address}
4. View your assets: htcli --mine subnet list

Development Best Practices:
- Use the test subnet for all development work
- Monitor your test token balance regularly
- Test all operations before moving to production
- Use the --mine flag to filter your assets
            """.strip()

            dev_tools["guidelines"] = dev_guidelines
            context["dev_tools"] = dev_tools

            print_success("Development tools configured successfully")
            print_info("Development environment is ready for use!")

            return True

        except Exception as e:
            print_error(f"Development tools setup failed: {str(e)}")
            return False
