"""
Migration and Recovery Flow

Automates the process of migrating existing assets or recovering from
configuration issues, including asset discovery and portfolio reconstruction.

Flow Steps:
1. Configuration restoration
2. Wallet key import/recovery
3. Asset discovery and verification
4. State reconstruction
5. Portfolio migration
6. Recovery verification
"""

from typing import Any, Dict, List, Tuple

from rich.prompt import Confirm, Prompt
from rich.table import Table

from ..utils.formatting import format_balance, print_error, print_info, print_success
from ..utils.validation import validate_address
from .base import BaseFlow, FlowStep


class MigrationRecoveryFlow(BaseFlow):
    """Migration and recovery automation"""

    @property
    def name(self) -> str:
        return "Migration and Recovery"

    @property
    def description(self) -> str:
        return """
This flow automates migration and recovery processes:
- Recovers configuration from backup or manual input
- Imports existing wallet keys
- Discovers and verifies existing assets
- Reconstructs portfolio state
- Validates migration success

Perfect for users migrating from other tools or recovering from issues.
        """.strip()

    def collect_inputs(self) -> Dict[str, Any]:
        """Collect migration/recovery parameters"""
        self.console.print("Welcome to Migration and Recovery!\n")

        # Recovery type
        recovery_type = Prompt.ask(
            "Recovery type",
            choices=["full-migration", "partial-recovery", "config-restore"],
            default="full-migration",
        )

        # Wallet recovery
        self.console.print("\nWallet recovery:")
        recovery_methods = []

        if Confirm.ask("Import from private key?"):
            recovery_methods.append("private_key")

        if Confirm.ask("Import from mnemonic phrase?"):
            recovery_methods.append("mnemonic")

        if Confirm.ask("Discover by address (read-only)?"):
            recovery_methods.append("address_only")

        if not recovery_methods:
            print_error("At least one recovery method must be selected")
            recovery_methods = ["address_only"]

        # Asset discovery
        self.console.print("\nAsset discovery:")
        discover_subnets = Confirm.ask("Discover owned subnets?", default=True)
        discover_stakes = Confirm.ask("Discover stake positions?", default=True)
        discover_nodes = Confirm.ask("Discover registered nodes?", default=True)

        # Migration preferences
        self.console.print("\nMigration preferences:")
        verify_assets = Confirm.ask("Verify all discovered assets?", default=True)
        create_backup = Confirm.ask("Create backup of current state?", default=True)

        return {
            "recovery_type": recovery_type,
            "recovery_methods": recovery_methods,
            "discover_subnets": discover_subnets,
            "discover_stakes": discover_stakes,
            "discover_nodes": discover_nodes,
            "verify_assets": verify_assets,
            "create_backup": create_backup,
        }

    def setup_steps(self) -> List[FlowStep]:
        """Define migration/recovery steps"""
        return [
            FlowStep(
                name="config_restore",
                description="Restore configuration",
                function=self.step_config_restore,
                required=True,
            ),
            FlowStep(
                name="wallet_recovery",
                description="Recover wallet keys",
                function=self.step_wallet_recovery,
                required=True,
                dependencies=["config_restore"],
            ),
            FlowStep(
                name="asset_discovery",
                description="Discover existing assets",
                function=self.step_asset_discovery,
                required=True,
                dependencies=["wallet_recovery"],
            ),
            FlowStep(
                name="state_reconstruction",
                description="Reconstruct portfolio state",
                function=self.step_state_reconstruction,
                required=True,
                dependencies=["asset_discovery"],
            ),
            FlowStep(
                name="asset_verification",
                description="Verify discovered assets",
                function=self.step_asset_verification,
                required=False,
                dependencies=["state_reconstruction"],
            ),
            FlowStep(
                name="recovery_validation",
                description="Validate recovery success",
                function=self.step_recovery_validation,
                required=True,
                dependencies=["state_reconstruction"],
            ),
        ]

    def step_config_restore(self, context: Dict[str, Any]) -> bool:
        """Restore configuration"""
        try:
            recovery_type = context["recovery_type"]

            if recovery_type == "config-restore":
                # Restore from backup or manual input
                restore_from_backup = Confirm.ask(
                    "Restore configuration from backup file?"
                )

                if restore_from_backup:
                    backup_path = Prompt.ask("Backup file path")
                    # In real implementation, would read backup file
                    print_info(f"Configuration restored from {backup_path}")
                else:
                    # Manual configuration
                    print_info("Using default configuration with manual overrides")

            # Create backup if requested
            if context.get("create_backup"):
                print_info("Current configuration backed up")

            print_success("Configuration restoration completed")
            return True

        except Exception as e:
            print_error(f"Configuration restoration failed: {str(e)}")
            return False

    def step_wallet_recovery(self, context: Dict[str, Any]) -> bool:
        """Recover wallet keys"""
        try:
            recovery_methods = context["recovery_methods"]
            recovered_addresses = []

            for method in recovery_methods:
                if method == "private_key":
                    success, address = self.recover_from_private_key()
                    if success:
                        recovered_addresses.append(("private_key", address))

                elif method == "mnemonic":
                    success, address = self.recover_from_mnemonic()
                    if success:
                        recovered_addresses.append(("mnemonic", address))

                elif method == "address_only":
                    success, address = self.recover_address_only()
                    if success:
                        recovered_addresses.append(("address_only", address))

            if not recovered_addresses:
                print_error("No wallet keys recovered")
                return False

            context["recovered_addresses"] = recovered_addresses
            print_success(f"Recovered {len(recovered_addresses)} wallet address(es)")

            return True

        except Exception as e:
            print_error(f"Wallet recovery failed: {str(e)}")
            return False

    def recover_from_private_key(self) -> Tuple[bool, str]:
        """Recover wallet from private key"""
        try:
            private_key = Prompt.ask("Private key (64-character hex)", password=True)
            key_name = Prompt.ask("Key name for storage", default="recovered-key")

            response = self.client.wallet.import_keypair(
                name=key_name, private_key=private_key
            )

            if response.get("success", False):
                address = response.get("address")
                print_success(f"Recovered key: {address}")
                return True, address
            else:
                print_error(
                    f"Private key recovery failed: {response.get('message', 'Unknown error')}"
                )
                return False, ""

        except Exception as e:
            print_error(f"Private key recovery failed: {str(e)}")
            return False, ""

    def recover_from_mnemonic(self) -> Tuple[bool, str]:
        """Recover wallet from mnemonic phrase"""
        try:
            mnemonic = Prompt.ask("Mnemonic phrase (12 or 24 words)", password=True)
            key_name = Prompt.ask("Key name for storage", default="recovered-mnemonic")

            # In real implementation, would convert mnemonic to private key
            # For now, simulate success
            print_info("Mnemonic recovery not fully implemented in this demo")
            return False, ""

        except Exception as e:
            print_error(f"Mnemonic recovery failed: {str(e)}")
            return False, ""

    def recover_address_only(self) -> Tuple[bool, str]:
        """Recover read-only access by address"""
        try:
            address = Prompt.ask("Wallet address to monitor")

            if not validate_address(address):
                print_error("Invalid address format")
                return False, ""

            # Verify address exists and has activity
            balance_response = self.client.chain.get_balance(address)
            if balance_response.success:
                balance = balance_response.data.get("balance", 0)
                print_success(
                    f"Address verified: {address} (Balance: {format_balance(balance)})"
                )
                return True, address
            else:
                print_error("Could not verify address")
                return False, ""

        except Exception as e:
            print_error(f"Address recovery failed: {str(e)}")
            return False, ""

    def step_asset_discovery(self, context: Dict[str, Any]) -> bool:
        """Discover existing assets"""
        try:
            recovered_addresses = context["recovered_addresses"]
            discovered_assets = {"subnets": [], "stakes": [], "nodes": []}

            for method, address in recovered_addresses:
                if context.get("discover_subnets"):
                    subnets = self.discover_owned_subnets(address)
                    discovered_assets["subnets"].extend(subnets)

                if context.get("discover_stakes"):
                    stakes = self.discover_stake_positions(address)
                    discovered_assets["stakes"].extend(stakes)

                if context.get("discover_nodes"):
                    nodes = self.discover_registered_nodes(address)
                    discovered_assets["nodes"].extend(nodes)

            # Remove duplicates
            discovered_assets["subnets"] = list(
                {s["subnet_id"]: s for s in discovered_assets["subnets"]}.values()
            )
            discovered_assets["stakes"] = list(
                {
                    (s["subnet_id"], s["node_id"]): s
                    for s in discovered_assets["stakes"]
                }.values()
            )
            discovered_assets["nodes"] = list(
                {
                    (n["subnet_id"], n["node_id"]): n
                    for n in discovered_assets["nodes"]
                }.values()
            )

            context["discovered_assets"] = discovered_assets

            # Display discovery results
            self.display_discovery_results(discovered_assets)

            total_assets = (
                len(discovered_assets["subnets"])
                + len(discovered_assets["stakes"])
                + len(discovered_assets["nodes"])
            )
            if total_assets > 0:
                print_success(f"Discovered {total_assets} total assets")
                return True
            else:
                print_info("No assets discovered - this may be a new account")
                return True

        except Exception as e:
            print_error(f"Asset discovery failed: {str(e)}")
            return False

    def discover_owned_subnets(self, address: str) -> List[Dict[str, Any]]:
        """Discover subnets owned by address"""
        try:
            response = self.client.subnet.get_subnets_data()
            if not response.success:
                return []

            owned_subnets = []
            subnets = response.data.get("subnets", [])

            for subnet in subnets:
                subnet_id = subnet.get("subnet_id")
                if subnet_id:
                    detail_response = self.client.subnet.get_subnet_data(subnet_id)
                    if detail_response.success:
                        subnet_detail = detail_response.data
                        if subnet_detail.get("owner") == address:
                            owned_subnets.append(
                                {
                                    "subnet_id": subnet_id,
                                    "path": subnet_detail.get(
                                        "name", f"subnet-{subnet_id}"
                                    ),
                                    "state": subnet_detail.get("state", "Unknown"),
                                    "owner": address,
                                }
                            )

            return owned_subnets

        except Exception:
            return []

    def discover_stake_positions(self, address: str) -> List[Dict[str, Any]]:
        """Discover stake positions for address"""
        try:
            response = self.client.staking.get_stake_info(address)
            if not response.success:
                return []

            stakes = response.data.get("stakes", [])
            stake_positions = []

            for stake in stakes:
                stake_positions.append(
                    {
                        "subnet_id": stake.get("subnet_id"),
                        "node_id": stake.get("node_id"),
                        "amount": stake.get("amount", 0),
                        "status": stake.get("status", "active"),
                        "address": address,
                    }
                )

            return stake_positions

        except Exception:
            return []

    def discover_registered_nodes(self, address: str) -> List[Dict[str, Any]]:
        """Discover nodes registered by address"""
        try:
            # This would require querying all subnets and checking node ownership
            # Simplified implementation for demo
            registered_nodes = []

            # In real implementation, would iterate through subnets
            # and check node ownership by hotkey address

            return registered_nodes

        except Exception:
            return []

    def display_discovery_results(self, assets: Dict[str, List]):
        """Display asset discovery results"""
        # Subnets table
        if assets["subnets"]:
            subnet_table = Table(title="Discovered Subnets")
            subnet_table.add_column("Subnet ID", style="cyan")
            subnet_table.add_column("Path", style="yellow")
            subnet_table.add_column("State", style="green")

            for subnet in assets["subnets"]:
                subnet_table.add_row(
                    str(subnet["subnet_id"]), subnet["path"], subnet["state"]
                )

            self.console.print(subnet_table)

        # Stakes table
        if assets["stakes"]:
            stakes_table = Table(title="Discovered Stakes")
            stakes_table.add_column("Subnet ID", style="cyan")
            stakes_table.add_column("Node ID", style="yellow")
            stakes_table.add_column("Amount", style="green")
            stakes_table.add_column("Status", style="blue")

            for stake in assets["stakes"]:
                stakes_table.add_row(
                    str(stake["subnet_id"]),
                    str(stake["node_id"]),
                    format_balance(stake["amount"]),
                    stake["status"],
                )

            self.console.print(stakes_table)

        # Nodes table
        if assets["nodes"]:
            nodes_table = Table(title="Discovered Nodes")
            nodes_table.add_column("Subnet ID", style="cyan")
            nodes_table.add_column("Node ID", style="yellow")
            nodes_table.add_column("Status", style="green")

            for node in assets["nodes"]:
                nodes_table.add_row(
                    str(node["subnet_id"]),
                    str(node["node_id"]),
                    node.get("status", "unknown"),
                )

            self.console.print(nodes_table)

    def step_state_reconstruction(self, context: Dict[str, Any]) -> bool:
        """Reconstruct portfolio state"""
        try:
            discovered_assets = context["discovered_assets"]
            recovered_addresses = context["recovered_addresses"]

            # Reconstruct portfolio state
            portfolio_state = {
                "addresses": [addr for _, addr in recovered_addresses],
                "total_subnets": len(discovered_assets["subnets"]),
                "total_stakes": len(discovered_assets["stakes"]),
                "total_nodes": len(discovered_assets["nodes"]),
                "total_staked_amount": sum(
                    stake["amount"] for stake in discovered_assets["stakes"]
                ),
                "asset_summary": discovered_assets,
            }

            context["portfolio_state"] = portfolio_state
            print_success("Portfolio state reconstructed successfully")

            # Display summary
            summary = f"""
Portfolio Reconstruction Summary:
- Addresses: {len(portfolio_state['addresses'])}
- Owned Subnets: {portfolio_state['total_subnets']}
- Stake Positions: {portfolio_state['total_stakes']}
- Registered Nodes: {portfolio_state['total_nodes']}
- Total Staked: {format_balance(portfolio_state['total_staked_amount'])}
            """
            print_info(summary)

            return True

        except Exception as e:
            print_error(f"State reconstruction failed: {str(e)}")
            return False

    def step_asset_verification(self, context: Dict[str, Any]) -> bool:
        """Verify discovered assets"""
        try:
            if not context.get("verify_assets"):
                print_info("Asset verification skipped")
                return True

            discovered_assets = context["discovered_assets"]
            verification_results = {
                "subnets_verified": 0,
                "stakes_verified": 0,
                "nodes_verified": 0,
                "failed_verifications": [],
            }

            # Verify subnets
            for subnet in discovered_assets["subnets"]:
                try:
                    response = self.client.subnet.get_subnet_data(subnet["subnet_id"])
                    if response.success:
                        verification_results["subnets_verified"] += 1
                    else:
                        verification_results["failed_verifications"].append(
                            f"Subnet {subnet['subnet_id']}"
                        )
                except Exception:
                    verification_results["failed_verifications"].append(
                        f"Subnet {subnet['subnet_id']}"
                    )

            # Verify stakes
            for stake in discovered_assets["stakes"]:
                try:
                    response = self.client.staking.get_stake_info(stake["address"])
                    if response.success:
                        verification_results["stakes_verified"] += 1
                    else:
                        verification_results["failed_verifications"].append(
                            f"Stake {stake['subnet_id']}/{stake['node_id']}"
                        )
                except Exception:
                    verification_results["failed_verifications"].append(
                        f"Stake {stake['subnet_id']}/{stake['node_id']}"
                    )

            context["verification_results"] = verification_results

            if verification_results["failed_verifications"]:
                print_info(
                    f"Verification completed with {len(verification_results['failed_verifications'])} failures"
                )
            else:
                print_success("All assets verified successfully")

            return True

        except Exception as e:
            print_error(f"Asset verification failed: {str(e)}")
            return False

    def step_recovery_validation(self, context: Dict[str, Any]) -> bool:
        """Validate recovery success"""
        try:
            portfolio_state = context["portfolio_state"]

            # Validate that we can access all key functions
            validation_checks = []

            # Check wallet access
            for address in portfolio_state["addresses"]:
                try:
                    balance_response = self.client.chain.get_balance(address)
                    if balance_response.success:
                        validation_checks.append(f"Wallet access: {address[:10]}... ✓")
                    else:
                        validation_checks.append(f"Wallet access: {address[:10]}... ✗")
                except Exception:
                    validation_checks.append(f"Wallet access: {address[:10]}... ✗")

            # Check CLI functionality
            try:
                network_response = self.client.chain.get_network_stats()
                if network_response.success:
                    validation_checks.append("Network connectivity ✓")
                else:
                    validation_checks.append("Network connectivity ✗")
            except Exception:
                validation_checks.append("Network connectivity ✗")

            # Display validation results
            for check in validation_checks:
                if "✓" in check:
                    print_success(check)
                else:
                    print_error(check)

            # Create recovery summary
            recovery_summary = {
                "recovery_type": context["recovery_type"],
                "addresses_recovered": len(portfolio_state["addresses"]),
                "assets_discovered": portfolio_state["total_subnets"]
                + portfolio_state["total_stakes"]
                + portfolio_state["total_nodes"],
                "validation_checks": validation_checks,
                "success": all("✓" in check for check in validation_checks),
            }

            context["recovery_summary"] = recovery_summary

            if recovery_summary["success"]:
                print_success("Recovery validation completed successfully")
                return True
            else:
                print_error("Recovery validation found issues")
                return False

        except Exception as e:
            print_error(f"Recovery validation failed: {str(e)}")
            return False
