"""
Complete Subnet Deployment Flow

Automates the entire process of creating and deploying a subnet with initial node,
from configuration setup to monitoring activation.

Flow Steps:
1. Configuration initialization
2. Wallet key generation/import
3. Balance verification
4. Subnet registration
5. Subnet activation
6. Initial node addition
7. Initial stake addition
8. Deployment verification
"""

from typing import Dict, Any, List
from rich.prompt import Prompt, IntPrompt, Confirm

from .base import BaseFlow, FlowStep
from ..models.requests import (
    SubnetRegisterRequest,
    SubnetNodeAddRequest,
    StakeAddRequest,
)
from ..utils.formatting import print_success, print_error, print_info, format_balance
from ..utils.validation import validate_address, validate_path


class SubnetDeploymentFlow(BaseFlow):
    """Complete subnet deployment automation"""

    @property
    def name(self) -> str:
        return "Complete Subnet Deployment"

    @property
    def description(self) -> str:
        return """
This flow automates the complete subnet deployment process:
- Sets up configuration and wallet
- Registers and activates a new subnet
- Adds initial node with stake
- Verifies deployment success

Perfect for subnet creators who want to go from zero to operational subnet quickly.
        """.strip()

    def collect_inputs(self) -> Dict[str, Any]:
        """Collect subnet deployment parameters"""
        self.console.print(
            "Please provide the following information for your subnet deployment:\n"
        )

        # Subnet configuration
        subnet_path = Prompt.ask("Subnet path (unique identifier)")
        while not validate_path(subnet_path):
            print_error(
                "Invalid subnet path. Please use alphanumeric characters and hyphens only."
            )
            subnet_path = Prompt.ask("Subnet path")

        memory_mb = IntPrompt.ask("Memory requirement (MB)", default=2048)
        registration_blocks = IntPrompt.ask(
            "Registration period (blocks)", default=1000
        )
        entry_interval = IntPrompt.ask("Entry interval (blocks)", default=100)

        # Node configuration
        self.console.print("\nNode configuration:")
        hotkey = Prompt.ask("Node hotkey address")
        while not validate_address(hotkey):
            print_error("Invalid address format")
            hotkey = Prompt.ask("Node hotkey address")

        peer_id = Prompt.ask("Node peer ID")

        # Staking configuration
        self.console.print("\nStaking configuration:")
        stake_amount_str = Prompt.ask("Initial stake amount (TENSOR)", default="10.0")
        stake_amount = int(
            float(stake_amount_str) * (10**18)
        )  # Convert to smallest units

        # Wallet configuration
        self.console.print("\nWallet configuration:")
        use_existing_key = Confirm.ask("Do you have an existing wallet key to import?")

        wallet_config = {"use_existing": use_existing_key}
        if use_existing_key:
            private_key = Prompt.ask("Private key (64-character hex)", password=True)
            key_name = Prompt.ask("Key name for storage", default="subnet-owner")
            wallet_config.update({"private_key": private_key, "key_name": key_name})
        else:
            key_name = Prompt.ask("New key name", default="subnet-owner")
            key_type = Prompt.ask(
                "Key type", choices=["sr25519", "ed25519"], default="sr25519"
            )
            wallet_config.update({"key_name": key_name, "key_type": key_type})

        return {
            "subnet_path": subnet_path,
            "memory_mb": memory_mb,
            "registration_blocks": registration_blocks,
            "entry_interval": entry_interval,
            "hotkey": hotkey,
            "peer_id": peer_id,
            "stake_amount": stake_amount,
            "wallet_config": wallet_config,
        }

    def setup_steps(self) -> List[FlowStep]:
        """Define deployment steps"""
        return [
            FlowStep(
                name="config_init",
                description="Initialize CLI configuration",
                function=self.step_config_init,
                required=True,
            ),
            FlowStep(
                name="wallet_setup",
                description="Set up wallet keys",
                function=self.step_wallet_setup,
                required=True,
                dependencies=["config_init"],
            ),
            FlowStep(
                name="balance_check",
                description="Verify account balance",
                function=self.step_balance_check,
                required=True,
                dependencies=["wallet_setup"],
            ),
            FlowStep(
                name="subnet_register",
                description="Register new subnet",
                function=self.step_subnet_register,
                required=True,
                dependencies=["balance_check"],
            ),
            FlowStep(
                name="subnet_activate",
                description="Activate registered subnet",
                function=self.step_subnet_activate,
                required=True,
                dependencies=["subnet_register"],
            ),
            FlowStep(
                name="node_add",
                description="Add initial node to subnet",
                function=self.step_node_add,
                required=True,
                dependencies=["subnet_activate"],
            ),
            FlowStep(
                name="stake_add",
                description="Add initial stake to node",
                function=self.step_stake_add,
                required=False,
                dependencies=["node_add"],
            ),
            FlowStep(
                name="verify_deployment",
                description="Verify deployment success",
                function=self.step_verify_deployment,
                required=True,
                dependencies=["node_add"],
            ),
        ]

    def step_config_init(self, context: Dict[str, Any]) -> bool:
        """Initialize configuration"""
        try:
            # Use existing config or create minimal config
            print_info("Configuration initialized")
            return True
        except Exception as e:
            print_error(f"Configuration initialization failed: {str(e)}")
            return False

    def step_wallet_setup(self, context: Dict[str, Any]) -> bool:
        """Set up wallet keys"""
        try:
            wallet_config = context["wallet_config"]

            if wallet_config["use_existing"]:
                # Import existing key
                response = self.client.wallet.import_keypair(
                    name=wallet_config["key_name"],
                    private_key=wallet_config["private_key"],
                )
            else:
                # Generate new key
                response = self.client.wallet.generate_keypair(
                    name=wallet_config["key_name"], key_type=wallet_config["key_type"]
                )

            if response.get("success", False):
                context["wallet_address"] = response.get("address")
                print_success(f"Wallet key ready: {response.get('address')}")
                return True
            else:
                print_error(
                    f"Wallet setup failed: {response.get('message', 'Unknown error')}"
                )
                return False

        except Exception as e:
            print_error(f"Wallet setup failed: {str(e)}")
            return False

    def step_balance_check(self, context: Dict[str, Any]) -> bool:
        """Verify sufficient balance"""
        try:
            address = context["wallet_address"]
            response = self.client.chain.get_balance(address)

            if response.success:
                balance = response.data.get("balance", 0)
                context["account_balance"] = balance

                # Check if balance is sufficient for operations
                min_required = context["stake_amount"] + (10**18)  # Stake + fees
                if balance >= min_required:
                    print_success(f"Sufficient balance: {format_balance(balance)}")
                    return True
                else:
                    print_error(
                        f"Insufficient balance. Required: {format_balance(min_required)}, Available: {format_balance(balance)}"
                    )
                    return False
            else:
                print_error(f"Balance check failed: {response.message}")
                return False

        except Exception as e:
            print_error(f"Balance check failed: {str(e)}")
            return False

    def step_subnet_register(self, context: Dict[str, Any]) -> bool:
        """Register new subnet"""
        try:
            request = SubnetRegisterRequest(
                path=context["subnet_path"],
                memory_mb=context["memory_mb"],
                registration_blocks=context["registration_blocks"],
                entry_interval=context["entry_interval"],
            )

            response = self.client.subnet.register_subnet(request)

            if response.success:
                subnet_id = response.data.get("subnet_id")
                context["subnet_id"] = subnet_id
                print_success(f"Subnet registered successfully. ID: {subnet_id}")
                return True
            else:
                print_error(f"Subnet registration failed: {response.message}")
                return False

        except Exception as e:
            print_error(f"Subnet registration failed: {str(e)}")
            return False

    def step_subnet_activate(self, context: Dict[str, Any]) -> bool:
        """Activate registered subnet"""
        try:
            subnet_id = context["subnet_id"]
            response = self.client.subnet.activate_subnet(subnet_id)

            if response.success:
                print_success(f"Subnet {subnet_id} activated successfully")
                return True
            else:
                print_error(f"Subnet activation failed: {response.message}")
                return False

        except Exception as e:
            print_error(f"Subnet activation failed: {str(e)}")
            return False

    def step_node_add(self, context: Dict[str, Any]) -> bool:
        """Add initial node to subnet"""
        try:
            request = SubnetNodeAddRequest(
                subnet_id=context["subnet_id"],
                hotkey=context["hotkey"],
                peer_id=context["peer_id"],
                stake_amount=context["stake_amount"],
            )

            response = self.client.node.add_node(request)

            if response.success:
                node_id = response.data.get("node_id")
                context["node_id"] = node_id
                print_success(f"Node added successfully. ID: {node_id}")
                return True
            else:
                print_error(f"Node addition failed: {response.message}")
                return False

        except Exception as e:
            print_error(f"Node addition failed: {str(e)}")
            return False

    def step_stake_add(self, context: Dict[str, Any]) -> bool:
        """Add initial stake to node"""
        try:
            request = StakeAddRequest(
                subnet_id=context["subnet_id"],
                node_id=context["node_id"],
                hotkey=context["hotkey"],
                amount=context["stake_amount"],
            )

            response = self.client.staking.add_stake(request)

            if response.success:
                print_success(
                    f"Stake added successfully: {format_balance(context['stake_amount'])}"
                )
                return True
            else:
                print_error(f"Stake addition failed: {response.message}")
                return False

        except Exception as e:
            print_error(f"Stake addition failed: {str(e)}")
            return False

    def step_verify_deployment(self, context: Dict[str, Any]) -> bool:
        """Verify deployment success"""
        try:
            subnet_id = context["subnet_id"]

            # Check subnet status
            subnet_response = self.client.subnet.get_subnet_data(subnet_id)
            if not subnet_response.success:
                print_error("Failed to verify subnet status")
                return False

            # Check node status
            node_response = self.client.node.get_node_status(
                subnet_id, context.get("node_id")
            )
            if not node_response.success:
                print_error("Failed to verify node status")
                return False

            print_success("Deployment verification completed successfully")

            # Store deployment summary
            context["deployment_summary"] = {
                "subnet_id": subnet_id,
                "subnet_path": context["subnet_path"],
                "node_id": context.get("node_id"),
                "wallet_address": context["wallet_address"],
                "stake_amount": context["stake_amount"],
            }

            return True

        except Exception as e:
            print_error(f"Deployment verification failed: {str(e)}")
            return False
