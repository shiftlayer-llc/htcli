"""
Staking Portfolio Setup Flow

Automates the setup of a diversified staking portfolio across multiple
subnets and nodes, with intelligent allocation and risk management.

Flow Steps:
1. Configuration and wallet setup
2. Portfolio strategy definition
3. Subnet analysis and selection
4. Balance verification and allocation
5. Stake distribution execution
6. Portfolio monitoring setup
"""

from typing import Dict, Any, List
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table

from .base import BaseFlow, FlowStep
from ..models.requests import StakeAddRequest
from ..utils.formatting import print_success, print_error, print_info, format_balance


class StakingPortfolioFlow(BaseFlow):
    """Staking portfolio setup automation"""

    @property
    def name(self) -> str:
        return "Staking Portfolio Setup"

    @property
    def description(self) -> str:
        return """
This flow automates staking portfolio creation:
- Analyzes available subnets and nodes
- Creates diversified staking strategy
- Distributes stakes across multiple targets
- Sets up portfolio monitoring and management

Perfect for investors who want to maximize returns through diversification.
        """.strip()

    def collect_inputs(self) -> Dict[str, Any]:
        """Collect portfolio setup parameters"""
        self.console.print("Welcome to Staking Portfolio Setup!\n")

        # Wallet configuration
        self.console.print("Wallet setup:")
        use_existing_key = Confirm.ask("Do you have an existing wallet key to import?")

        wallet_config = {"use_existing": use_existing_key}
        if use_existing_key:
            private_key = Prompt.ask("Private key (64-character hex)", password=True)
            key_name = Prompt.ask("Key name for storage", default="portfolio-manager")
            wallet_config.update({"private_key": private_key, "key_name": key_name})
        else:
            key_name = Prompt.ask("New key name", default="portfolio-manager")
            key_type = Prompt.ask("Key type", choices=["sr25519", "ed25519"], default="sr25519")
            wallet_config.update({"key_name": key_name, "key_type": key_type})

        # Portfolio strategy
        self.console.print("\nPortfolio strategy:")
        total_stake_str = Prompt.ask("Total amount to stake (TENSOR)", default="100.0")
        total_stake = int(float(total_stake_str) * (10 ** 18))

        strategy = Prompt.ask(
            "Portfolio strategy",
            choices=["conservative", "balanced", "aggressive"],
            default="balanced"
        )

        max_positions = IntPrompt.ask("Maximum number of staking positions", default=5)
        min_stake_per_position_str = Prompt.ask("Minimum stake per position (TENSOR)", default="10.0")
        min_stake_per_position = int(float(min_stake_per_position_str) * (10 ** 18))

        # Risk preferences
        diversify_subnets = Confirm.ask("Diversify across multiple subnets?", default=True)
        include_new_subnets = Confirm.ask("Include newer subnets (higher risk/reward)?", default=False)

        return {
            "wallet_config": wallet_config,
            "total_stake": total_stake,
            "strategy": strategy,
            "max_positions": max_positions,
            "min_stake_per_position": min_stake_per_position,
            "diversify_subnets": diversify_subnets,
            "include_new_subnets": include_new_subnets
        }

    def setup_steps(self) -> List[FlowStep]:
        """Define portfolio setup steps"""
        return [
            FlowStep(
                name="config_init",
                description="Initialize CLI configuration",
                function=self.step_config_init,
                required=True
            ),
            FlowStep(
                name="wallet_setup",
                description="Set up wallet keys",
                function=self.step_wallet_setup,
                required=True,
                dependencies=["config_init"]
            ),
            FlowStep(
                name="balance_check",
                description="Verify account balance",
                function=self.step_balance_check,
                required=True,
                dependencies=["wallet_setup"]
            ),
            FlowStep(
                name="market_analysis",
                description="Analyze staking opportunities",
                function=self.step_market_analysis,
                required=True,
                dependencies=["balance_check"]
            ),
            FlowStep(
                name="portfolio_allocation",
                description="Calculate optimal stake allocation",
                function=self.step_portfolio_allocation,
                required=True,
                dependencies=["market_analysis"]
            ),
            FlowStep(
                name="execute_stakes",
                description="Execute stake distribution",
                function=self.step_execute_stakes,
                required=True,
                dependencies=["portfolio_allocation"]
            ),
            FlowStep(
                name="monitoring_setup",
                description="Set up portfolio monitoring",
                function=self.step_monitoring_setup,
                required=False,
                dependencies=["execute_stakes"]
            )
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
                    private_key=wallet_config["private_key"]
                )
            else:
                response = self.client.wallet.generate_keypair(
                    name=wallet_config["key_name"],
                    key_type=wallet_config["key_type"]
                )

            if response.get("success", False):
                context["wallet_address"] = response.get("address")
                print_success(f"Wallet key ready: {response.get('address')}")
                return True
            else:
                print_error(f"Wallet setup failed: {response.get('message', 'Unknown error')}")
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

                required_amount = context["total_stake"] + (10 ** 18)  # Stakes + fees
                if balance >= required_amount:
                    print_success(f"Sufficient balance: {format_balance(balance)}")
                    return True
                else:
                    print_error(f"Insufficient balance. Required: {format_balance(required_amount)}, Available: {format_balance(balance)}")
                    return False
            else:
                print_error(f"Balance check failed: {response.message}")
                return False

        except Exception as e:
            print_error(f"Balance check failed: {str(e)}")
            return False

    def step_market_analysis(self, context: Dict[str, Any]) -> bool:
        """Analyze staking opportunities"""
        try:
            # Get all subnets
            response = self.client.subnet.get_subnets_data()
            if not response.success:
                print_error("Failed to retrieve subnet data")
                return False

            subnets = response.data.get("subnets", [])
            staking_opportunities = []

            for subnet in subnets:
                subnet_id = subnet.get("subnet_id")
                if not subnet_id:
                    continue

                # Get detailed subnet info
                detail_response = self.client.subnet.get_subnet_data(subnet_id)
                if not detail_response.success:
                    continue

                subnet_detail = detail_response.data

                # Get nodes in subnet
                nodes_response = self.client.node.get_subnet_nodes(subnet_id)
                if not nodes_response.success:
                    continue

                nodes = nodes_response.data.get("nodes", [])

                # Analyze each node as potential staking target
                for node in nodes:
                    opportunity = self.analyze_staking_opportunity(subnet_detail, node)
                    if opportunity:
                        staking_opportunities.append(opportunity)

            if not staking_opportunities:
                print_error("No suitable staking opportunities found")
                return False

            # Filter and rank opportunities based on strategy
            filtered_opportunities = self.filter_opportunities_by_strategy(
                staking_opportunities, context
            )

            context["staking_opportunities"] = filtered_opportunities
            print_success(f"Found {len(filtered_opportunities)} staking opportunities")
            return True

        except Exception as e:
            print_error(f"Market analysis failed: {str(e)}")
            return False

    def analyze_staking_opportunity(self, subnet_info: Dict[str, Any], node_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze individual staking opportunity"""
        opportunity = {
            "subnet_id": subnet_info.get("subnet_id"),
            "node_id": node_info.get("node_id"),
            "subnet_state": subnet_info.get("state"),
            "node_status": node_info.get("status"),
            "current_stake": node_info.get("total_stake", 0),
            "performance_score": node_info.get("performance_score", 0.5),
            "reward_rate": node_info.get("reward_rate", 0.1),
            "risk_score": 0.5  # Default risk score
        }

        # Calculate risk score based on various factors
        risk_score = 0.5

        # Subnet maturity factor
        if subnet_info.get("state") == "Active":
            risk_score -= 0.1
        elif subnet_info.get("state") == "Registered":
            risk_score += 0.1

        # Node performance factor
        performance = opportunity["performance_score"]
        if performance > 0.8:
            risk_score -= 0.2
        elif performance < 0.3:
            risk_score += 0.2

        # Stake concentration factor
        total_nodes = subnet_info.get("total_nodes", 1)
        if total_nodes > 10:  # More distributed = lower risk
            risk_score -= 0.1

        opportunity["risk_score"] = max(0.0, min(1.0, risk_score))
        opportunity["attractiveness_score"] = self.calculate_attractiveness(opportunity)

        return opportunity

    def calculate_attractiveness(self, opportunity: Dict[str, Any]) -> float:
        """Calculate overall attractiveness score"""
        # Weighted scoring based on multiple factors
        performance_weight = 0.3
        reward_weight = 0.3
        risk_weight = 0.2
        stake_weight = 0.2

        performance_score = opportunity["performance_score"]
        reward_score = min(opportunity["reward_rate"] * 10, 1.0)  # Normalize to 0-1
        risk_score = 1.0 - opportunity["risk_score"]  # Lower risk = higher score

        # Stake size factor (prefer moderate stakes)
        stake = opportunity["current_stake"]
        if stake < 10 * (10 ** 18):  # Less than 10 TENSOR
            stake_score = 0.8  # Slightly lower for very low stakes
        elif stake > 1000 * (10 ** 18):  # More than 1000 TENSOR
            stake_score = 0.6  # Lower for very high stakes
        else:
            stake_score = 1.0

        total_score = (
            performance_score * performance_weight +
            reward_score * reward_weight +
            risk_score * risk_weight +
            stake_score * stake_weight
        )

        return total_score

    def filter_opportunities_by_strategy(self, opportunities: List[Dict[str, Any]], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter opportunities based on user strategy"""
        strategy = context["strategy"]
        include_new = context["include_new_subnets"]

        filtered = []

        for opp in opportunities:
            # Filter by subnet maturity
            if not include_new and opp["subnet_state"] != "Active":
                continue

            # Strategy-based filtering
            if strategy == "conservative":
                if opp["risk_score"] > 0.6:  # Skip high-risk
                    continue
            elif strategy == "aggressive":
                if opp["risk_score"] < 0.3:  # Skip low-risk (potentially low-reward)
                    continue

            # Only include opportunities with reasonable performance
            if opp["performance_score"] < 0.2:
                continue

            filtered.append(opp)

        # Sort by attractiveness
        filtered.sort(key=lambda x: x["attractiveness_score"], reverse=True)

        return filtered

    def step_portfolio_allocation(self, context: Dict[str, Any]) -> bool:
        """Calculate optimal stake allocation"""
        try:
            opportunities = context["staking_opportunities"]
            total_stake = context["total_stake"]
            max_positions = context["max_positions"]
            min_stake = context["min_stake_per_position"]
            diversify_subnets = context["diversify_subnets"]

            # Select top opportunities
            selected_opportunities = opportunities[:max_positions]

            if diversify_subnets:
                # Ensure subnet diversity
                selected_opportunities = self.ensure_subnet_diversity(selected_opportunities)

            # Calculate allocation
            allocations = self.calculate_allocations(
                selected_opportunities, total_stake, min_stake
            )

            if not allocations:
                print_error("Could not create viable allocation")
                return False

            # Display allocation plan
            self.display_allocation_plan(allocations)

            if not Confirm.ask("Proceed with this allocation?"):
                print_info("Portfolio allocation cancelled")
                return False

            context["stake_allocations"] = allocations
            return True

        except Exception as e:
            print_error(f"Portfolio allocation failed: {str(e)}")
            return False

    def ensure_subnet_diversity(self, opportunities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ensure diversity across subnets"""
        seen_subnets = set()
        diverse_opportunities = []

        # First pass: one opportunity per subnet
        for opp in opportunities:
            subnet_id = opp["subnet_id"]
            if subnet_id not in seen_subnets:
                diverse_opportunities.append(opp)
                seen_subnets.add(subnet_id)

        # Second pass: fill remaining slots with best remaining
        remaining_slots = len(opportunities) - len(diverse_opportunities)
        for opp in opportunities:
            if len(diverse_opportunities) >= len(opportunities):
                break
            if opp not in diverse_opportunities and remaining_slots > 0:
                diverse_opportunities.append(opp)
                remaining_slots -= 1

        return diverse_opportunities

    def calculate_allocations(self, opportunities: List[Dict[str, Any]], total_stake: int, min_stake: int) -> List[Dict[str, Any]]:
        """Calculate stake allocations"""
        if not opportunities:
            return []

        # Calculate total attractiveness score
        total_attractiveness = sum(opp["attractiveness_score"] for opp in opportunities)

        allocations = []
        remaining_stake = total_stake

        for opp in opportunities:
            # Proportional allocation based on attractiveness
            proportion = opp["attractiveness_score"] / total_attractiveness
            allocated_amount = int(total_stake * proportion)

            # Ensure minimum stake
            if allocated_amount < min_stake:
                allocated_amount = min_stake

            # Ensure we don't exceed remaining stake
            if allocated_amount > remaining_stake:
                allocated_amount = remaining_stake

            if allocated_amount > 0:
                allocation = {
                    "subnet_id": opp["subnet_id"],
                    "node_id": opp["node_id"],
                    "amount": allocated_amount,
                    "percentage": (allocated_amount / total_stake) * 100,
                    "risk_score": opp["risk_score"],
                    "expected_reward": opp["reward_rate"]
                }
                allocations.append(allocation)
                remaining_stake -= allocated_amount

            if remaining_stake <= 0:
                break

        return allocations

    def display_allocation_plan(self, allocations: List[Dict[str, Any]]):
        """Display allocation plan to user"""
        table = Table(title="Stake Allocation Plan")
        table.add_column("Subnet ID", style="cyan")
        table.add_column("Node ID", style="yellow")
        table.add_column("Amount", style="green")
        table.add_column("Percentage", style="blue")
        table.add_column("Risk", style="red")
        table.add_column("Expected Reward", style="magenta")

        for allocation in allocations:
            table.add_row(
                str(allocation["subnet_id"]),
                str(allocation["node_id"]),
                format_balance(allocation["amount"]),
                f"{allocation['percentage']:.1f}%",
                f"{allocation['risk_score']:.2f}",
                f"{allocation['expected_reward']*100:.1f}%"
            )

        self.console.print(table)

    def step_execute_stakes(self, context: Dict[str, Any]) -> bool:
        """Execute stake distribution"""
        try:
            allocations = context["stake_allocations"]
            wallet_address = context["wallet_address"]

            executed_stakes = []

            for allocation in allocations:
                request = StakeAddRequest(
                    subnet_id=allocation["subnet_id"],
                    node_id=allocation["node_id"],
                    hotkey=wallet_address,
                    amount=allocation["amount"]
                )

                response = self.client.staking.add_stake(request)

                if response.success:
                    executed_stakes.append(allocation)
                    print_success(f"Staked {format_balance(allocation['amount'])} to subnet {allocation['subnet_id']}, node {allocation['node_id']}")
                else:
                    print_error(f"Failed to stake to subnet {allocation['subnet_id']}: {response.message}")
                    # Continue with other stakes even if one fails

            if executed_stakes:
                context["executed_stakes"] = executed_stakes
                print_success(f"Successfully executed {len(executed_stakes)} stake positions")
                return True
            else:
                print_error("No stakes were executed successfully")
                return False

        except Exception as e:
            print_error(f"Stake execution failed: {str(e)}")
            return False

    def step_monitoring_setup(self, context: Dict[str, Any]) -> bool:
        """Set up portfolio monitoring"""
        try:
            executed_stakes = context.get("executed_stakes", [])

            monitoring_info = """
Portfolio monitoring commands:
- View all your stakes: htcli --mine stake info
- Check specific subnet: htcli subnet info --subnet-id <ID>
- Monitor node performance: htcli node status --subnet-id <ID> --node-id <ID>
- Check account balance: htcli chain balance --address <your-address>
            """

            print_info("Portfolio monitoring setup completed")
            context["monitoring_info"] = monitoring_info
            context["portfolio_summary"] = {
                "total_positions": len(executed_stakes),
                "total_staked": sum(stake["amount"] for stake in executed_stakes),
                "diversification": len(set(stake["subnet_id"] for stake in executed_stakes))
            }

            return True

        except Exception as e:
            print_error(f"Monitoring setup failed: {str(e)}")
            return False
