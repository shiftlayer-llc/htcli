import logging
from substrateinterface import SubstrateInterface, Keypair
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class BlockchainInterface:
    """
    Interface for interacting with the Hypertensor blockchain.
    Handles transaction creation, signing, and submission.
    """

    def __init__(self, rpc_url: str, ss58_format: int = 42):
        """
        Initialize blockchain interface.

        Args:
            rpc_url: RPC URL for the chain
            ss58_format: SS58 format for address encoding
        """
        self.substrate = SubstrateInterface(url=rpc_url, ss58_format=ss58_format)
        self.ss58_format = ss58_format

    def get_balance(self, address: str) -> Optional[float]:
        """
        Get balance for an address.

        Args:
            address: SS58 address

        Returns:
            Balance in TENSOR tokens
        """
        try:
            # Query account info
            account_info = self.substrate.query_runtime_state(
                "System", "Account", [address]
            )

            if account_info and 'data' in account_info:
                balance = account_info['data']['free']
                # Convert from raw units to TENSOR (assuming 10^9 decimals)
                return float(balance) / 1_000_000_000
            return 0.0

        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return None

    def create_transfer_call(self, to_address: str, amount: float) -> Dict[str, Any]:
        """
        Create a transfer call.

        Args:
            to_address: Destination address
            amount: Amount in TENSOR tokens

        Returns:
            Call data for the transfer
        """
        # Convert TENSOR to raw units
        amount_raw = int(amount * 1_000_000_000)

        call = self.substrate.compose_call(
            call_module="Balances",
            call_function="transfer",
            call_params={
                'dest': to_address,
                'value': amount_raw
            }
        )

        return call

    def create_stake_call(self, subnet_id: int, amount: float) -> Dict[str, Any]:
        """
        Create a stake call.

        Args:
            subnet_id: Subnet ID to stake on
            amount: Amount in TENSOR tokens

        Returns:
            Call data for the stake
        """
        # Convert TENSOR to raw units
        amount_raw = int(amount * 1_000_000_000)

        call = self.substrate.compose_call(
            call_module="SubnetRegistry",
            call_function="stake",
            call_params={
                'subnet_id': subnet_id,
                'amount': amount_raw
            }
        )

        return call

    def create_delegate_call(self, subnet_id: int, validator: str, amount: float) -> Dict[str, Any]:
        """
        Create a delegate call.

        Args:
            subnet_id: Subnet ID
            validator: Validator address
            amount: Amount in TENSOR tokens

        Returns:
            Call data for the delegation
        """
        # Convert TENSOR to raw units
        amount_raw = int(amount * 1_000_000_000)

        call = self.substrate.compose_call(
            call_module="SubnetRegistry",
            call_function="delegate",
            call_params={
                'subnet_id': subnet_id,
                'validator': validator,
                'amount': amount_raw
            }
        )

        return call

    def sign_and_submit_transaction(self, keypair: Keypair, call: Dict[str, Any]) -> Optional[str]:
        """
        Sign and submit a transaction.

        Args:
            keypair: Keypair for signing
            call: Call data to submit

        Returns:
            Transaction hash if successful, None otherwise
        """
        try:
            # Create extrinsic
            extrinsic = self.substrate.create_signed_extrinsic(
                call=call,
                keypair=keypair
            )

            # Submit transaction
            result = self.substrate.submit_extrinsic(
                extrinsic=extrinsic,
                wait_for_inclusion=True
            )

            if result.is_success:
                return result.extrinsic_hash
            else:
                logger.error(f"Transaction failed: {result.error_message}")
                return None

        except Exception as e:
            logger.error(f"Error submitting transaction: {e}")
            return None

    def get_transaction_history(self, address: str, limit: int = 10) -> list:
        """
        Get transaction history for an address.

        Args:
            address: Address to query
            limit: Maximum number of transactions

        Returns:
            List of transactions
        """
        try:
            # This is a placeholder - actual implementation depends on
            # how Hypertensor stores transaction history
            # You might need to query events or use a different approach

            # Example implementation:
            events = self.substrate.query_runtime_state(
                "System", "Events", []
            )

            # Filter events for the address
            address_transactions = []
            for event in events[:limit]:
                # Filter logic depends on event structure
                if hasattr(event, 'address') and event.address == address:
                    address_transactions.append({
                        'hash': event.extrinsic_hash,
                        'block': event.block_number,
                        'type': event.event_type,
                        'data': event.data
                    })

            return address_transactions

        except Exception as e:
            logger.error(f"Error getting transaction history: {e}")
            return []

    def get_subnet_info(self, subnet_id: int) -> Optional[Dict[str, Any]]:
        """
        Get information about a subnet.

        Args:
            subnet_id: Subnet ID

        Returns:
            Subnet information
        """
        try:
            subnet_info = self.substrate.query_runtime_state(
                "SubnetRegistry", "SubnetInfo", [subnet_id]
            )
            return subnet_info

        except Exception as e:
            logger.error(f"Error getting subnet info: {e}")
            return None

    def get_subnet_validators(self, subnet_id: int) -> list:
        """
        Get validators for a subnet.

        Args:
            subnet_id: Subnet ID

        Returns:
            List of validators
        """
        try:
            validators = self.substrate.query_runtime_state(
                "SubnetRegistry", "SubnetValidators", [subnet_id]
            )
            return validators or []

        except Exception as e:
            logger.error(f"Error getting subnet validators: {e}")
            return []

    def get_all_subnets(self) -> list:
        """
        Get all available subnets.

        Returns:
            List of all subnets
        """
        try:
            subnets = self.substrate.query_runtime_state(
                "SubnetRegistry", "Subnets", []
            )
            return subnets or []

        except Exception as e:
            logger.error(f"Error getting subnets: {e}")
            return []
