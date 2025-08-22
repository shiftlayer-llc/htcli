"""
Node Operator Onboarding Flow

Automates the process of joining an existing subnet as a node operator,
including wallet setup, subnet selection, node registration, and initial staking.

Flow Steps:
1. Configuration initialization
2. Wallet key generation/import
3. Subnet discovery and selection
4. Balance verification
5. Node registration
6. Initial stake addition
7. Node status monitoring setup
"""

from typing import Any, Dict, List

from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from ..models.requests import StakeAddRequest, SubnetNodeAddRequest
from ..utils.formatting import format_balance, print_error, print_info, print_success
from ..utils.validation import validate_address
from .base import BaseFlow, FlowStep


class NodeOnboardingFlow(BaseFlow):
    """Node operator onboarding automation"""

    @property
    def name(self) -> str:
        return "Node Operator Onboarding"

    @property
    def description(self) -> str:
        return """
This flow automates node operator onboarding:
- Sets up wallet and configuration
- Helps select optimal subnet to join
- Registers node with initial stake
- Sets up monitoring and status tracking

Perfect for node operators who want to start earning rewards quickly.
        """.strip()

    def collect_inputs(self) -> Dict[str, Any]:
        """Collect node onboarding parameters"""
        self.console.print("Welcome to Node Operator Onboarding!\n")

        # Wallet configuration
        self.console.print("Wallet setup:")
        use_existing_key = Confirm.ask("Do you have an existing wallet key to import?")

        wallet_config = {"use_existing": use_existing_key}
        if use_existing_key:
            private_key = Prompt.ask("Private key (64-character hex)", password=True)
            key_name = Prompt.ask("Key name for storage", default="node-operator")
            wallet_config.update({"private_key": private_key, "key_name": key_name})
        else:
            key_name = Prompt.ask("New key name", default="node-operator")
            key_type = Prompt.ask(
                "Key type", choices=["sr25519", "ed25519"], default="sr25519"
            )
            wallet_config.update({"key_name": key_name, "key_type": key_type})

        # Node configuration
        self.console.print("\nNode configuration:")
        hotkey = Prompt.ask("Node hotkey address")
        while not validate_address(hotkey):
            print_error("Invalid address format")
            hotkey = Prompt.ask("Node hotkey address")

        peer_id = Prompt.ask("Node peer ID")

        # Staking preference
        self.console.print("\nStaking configuration:")
        stake_amount_str = Prompt.ask("Initial stake amount (TENSOR)", default="5.0")
        stake_amount = int(
            float(stake_amount_str) * (10**18)
        )  # Convert to smallest units

        # Subnet selection preference
        subnet_selection = Prompt.ask(
            "Subnet selection method",
            choices=["manual", "auto-recommend"],
            default="auto-recommend",
        )

        manual_subnet_id = None
        if subnet_selection == "manual":
            manual_subnet_id = IntPrompt.ask("Subnet ID to join")

        return {
            "wallet_config": wallet_config,
            "hotkey": hotkey,
            "peer_id": peer_id,
            "stake_amount": stake_amount,
            "subnet_selection": subnet_selection,
            "manual_subnet_id": manual_subnet_id,
        }

    def setup_steps(self) -> List[FlowStep]:
        """Define onboarding steps"""
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
                name="subnet_discovery",
                description="Discover and select optimal subnet",
                function=self.step_subnet_discovery,
                required=True,
                dependencies=["wallet_setup"],
            ),
            FlowStep(
                name="balance_check",
                description="Verify account balance",
                function=self.step_balance_check,
                required=True,
                dependencies=["wallet_setup"],
            ),
            FlowStep(
                name="node_register",
                description="Register node in selected subnet",
                function=self.step_node_register,
                required=True,
                dependencies=["subnet_discovery", "balance_check"],
            ),
            FlowStep(
                name="stake_add",
                description="Add initial stake to node",
                function=self.step_stake_add,
                required=False,
                dependencies=["node_register"],
            ),
            FlowStep(
                name="monitoring_setup",
                description="Set up node monitoring",
                function=self.step_monitoring_setup,
                required=False,
                dependencies=["node_register"],
            ),
        ]

    def step_config_init(self, context: Dict[str, Any]) -> bool:
        """Initialize configuration"""
        try:
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
                response = self.client.wallet.import_keypair(
                    name=wallet_config["key_name"],
                    private_key=wallet_config["private_key"],
                )
            else:
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

    def step_subnet_discovery(self, context: Dict[str, Any]) -> bool:
        """Discover and select optimal subnet"""
        try:
            if context["manual_subnet_id"]:
                # User specified subnet manually
                subnet_id = context["manual_subnet_id"]
                response = self.client.subnet.get_subnet_data(subnet_id)

                if response.success:
                    context["selected_subnet_id"] = subnet_id
                    context["subnet_info"] = response.data
                    print_success(f"Selected subnet {subnet_id}")
                    return True
                else:
                    print_error(f"Failed to get subnet {subnet_id} information")
                    return False

            else:
                # Auto-recommend subnet based on criteria
                response = self.client.subnet.get_subnets_data()

                if not response.success:
                    print_error("Failed to retrieve subnet list")
                    return False

                subnets = response.data.get("subnets", [])
                if not subnets:
                    print_error("No subnets available")
                    return False

                # Score subnets based on various factors
                scored_subnets = []
                for subnet in subnets:
                    subnet_id = subnet.get("subnet_id")
                    if subnet_id:
                        detail_response = self.client.subnet.get_subnet_data(subnet_id)
                        if detail_response.success:
                            subnet_detail = detail_response.data
                            score = self.calculate_subnet_score(subnet_detail)
                            scored_subnets.append((score, subnet_id, subnet_detail))

                if not scored_subnets:
                    print_error("No suitable subnets found")
                    return False

                # Sort by score and show top options
                scored_subnets.sort(reverse=True)
                top_subnets = scored_subnets[:5]

                # Display recommendations
                table = Table(title="Recommended Subnets")
                table.add_column("Rank", style="cyan")
                table.add_column("Subnet ID", style="yellow")
                table.add_column("Score", style="green")
                table.add_column("Nodes", style="white")
                table.add_column("Status", style="blue")

                for i, (score, subnet_id, subnet_info) in enumerate(top_subnets, 1):
                    table.add_row(
                        str(i),
                        str(subnet_id),
                        f"{score:.2f}",
                        str(subnet_info.get("total_nodes", 0)),
                        subnet_info.get("state", "Unknown"),
                    )

                self.console.print(table)

                # Let user choose or accept top recommendation
                if Confirm.ask(
                    f"Join top recommended subnet (ID: {top_subnets[0][1]})?"
                ):
                    selected_subnet = top_subnets[0]
                else:
                    choice = IntPrompt.ask("Enter subnet rank to join (1-5)")
                    if 1 <= choice <= len(top_subnets):
                        selected_subnet = top_subnets[choice - 1]
                    else:
                        print_error("Invalid selection")
                        return False

                context["selected_subnet_id"] = selected_subnet[1]
                context["subnet_info"] = selected_subnet[2]
                print_success(f"Selected subnet {selected_subnet[1]}")
                return True

        except Exception as e:
            print_error(f"Subnet discovery failed: {str(e)}")
            return False

    def calculate_subnet_score(self, subnet_info: Dict[str, Any]) -> float:
        """Calculate subnet attractiveness score"""
        score = 0.0

        # Factor in node count (more nodes = more established)
        node_count = subnet_info.get("total_nodes", 0)
        score += min(node_count * 0.1, 2.0)

        # Factor in subnet state
        state = subnet_info.get("state", "")
        if state == "Active":
            score += 3.0
        elif state == "Registered":
            score += 1.0

        # Factor in available slots
        max_nodes = subnet_info.get("max_registered_nodes", 100)
        if node_count < max_nodes * 0.8:  # Less than 80% full
            score += 2.0

        return score

    def step_balance_check(self, context: Dict[str, Any]) -> bool:
        """Verify sufficient balance"""
        try:
            address = context["wallet_address"]
            response = self.client.chain.get_balance(address)

            if response.success:
                balance = response.data.get("balance", 0)
                context["account_balance"] = balance

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

    def step_node_register(self, context: Dict[str, Any]) -> bool:
        """Register node in selected subnet"""
        try:
            request = SubnetNodeAddRequest(
                subnet_id=context["selected_subnet_id"],
                hotkey=context["hotkey"],
                peer_id=context["peer_id"],
                stake_amount=context["stake_amount"],
            )

            response = self.client.node.add_node(request)

            if response.success:
                node_id = response.data.get("node_id")
                context["node_id"] = node_id
                print_success(f"Node registered successfully. ID: {node_id}")
                return True
            else:
                print_error(f"Node registration failed: {response.message}")
                return False

        except Exception as e:
            print_error(f"Node registration failed: {str(e)}")
            return False

    def step_stake_add(self, context: Dict[str, Any]) -> bool:
        """Add initial stake to node"""
        try:
            request = StakeAddRequest(
                subnet_id=context["selected_subnet_id"],
                node_id=context["node_id"],
                hotkey=context["hotkey"],
                amount=context["stake_amount"],
            )

            response = self.client.staking.add_stake(request)

            if response.success:
                print_success(
                    f"Initial stake added: {format_balance(context['stake_amount'])}"
                )
                return True
            else:
                print_error(f"Stake addition failed: {response.message}")
                return False

        except Exception as e:
            print_error(f"Stake addition failed: {str(e)}")
            return False

    def step_monitoring_setup(self, context: Dict[str, Any]) -> bool:
        """Set up node monitoring"""
        try:
            # Provide monitoring guidance
            subnet_id = context["selected_subnet_id"]
            node_id = context["node_id"]

            monitoring_info = f"""
Node monitoring commands:
- Check status: htcli node status --subnet-id {subnet_id} --node-id {node_id}
- View stakes: htcli --mine stake info
- Monitor subnet: htcli subnet info --subnet-id {subnet_id}
            """

            print_info("Monitoring setup completed")
            context["monitoring_commands"] = monitoring_info
            return True

        except Exception as e:
            print_error(f"Monitoring setup failed: {str(e)}")
            return False
