#!/usr/bin/env python3
"""
Wallet operations client module.
Handles all wallet and staking-related blockchain operations.
"""

import logging
from substrateinterface import SubstrateInterface
from ..models.requests import StakeAddRequest, StakeRemoveRequest
from ..models.responses import *

logger = logging.getLogger(__name__)


class WalletClient:
    """Client for wallet and staking operations."""

    def __init__(self, substrate: SubstrateInterface):
        self.substrate = substrate

    def add_to_stake(self, request: StakeAddRequest, keypair=None):
        """Add stake using Network.add_to_stake with real transaction submission."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="add_to_stake",
                call_params={
                    "subnet_id": request.subnet_id,
                    "subnet_node_id": request.node_id,  # Fixed: use subnet_node_id as expected by blockchain
                    "hotkey": request.hotkey,
                    "stake_to_be_added": request.stake_to_be_added,
                },
            )

            # If keypair provided, submit real transaction
            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                # Return real transaction details
                return StakeAddResponse(
                    success=True,
                    message="Stake added successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return StakeAddResponse(
                    success=True,
                    message="Stake addition call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to add stake: {str(e)}")
            raise

    def remove_stake(self, request: StakeRemoveRequest, keypair=None):
        """Remove stake using Network.remove_stake with real transaction submission."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Compose the call using Network pallet
            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="remove_stake",
                call_params={
                    "subnet_id": request.subnet_id,
                    "hotkey": request.hotkey,
                    "stake_to_be_removed": request.stake_to_be_removed,
                },
            )

            # If keypair provided, submit real transaction
            if keypair:
                # Create and submit transaction
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                # Submit and wait for confirmation
                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                # Return real transaction details
                return StakeRemoveResponse(
                    success=True,
                    message="Stake removed successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                # Return composed call data for manual submission
                return StakeRemoveResponse(
                    success=True,
                    message="Stake removal call composed successfully",
                    transaction_hash=None,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to remove stake: {str(e)}")
            raise

    def get_account_subnet_stake(self, account: str, subnet_id: int):
        """Get account stake for a subnet using storage query."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Validate account address format
            if not account or len(account) < 10:
                raise Exception("Invalid account address format")

            # Query account stake from storage
            stake_data = self.substrate.query(
                module="Network",
                storage_function="AccountSubnetStake",
                params=[account, subnet_id],
            )

            return StakeInfoResponse(
                success=True,
                message="Stake information retrieved successfully",
                data={
                    "account": account,
                    "subnet_id": subnet_id,
                    "stake": stake_data.value if stake_data else 0,
                },
            )
        except Exception as e:
            logger.error(f"Failed to get account subnet stake: {str(e)}")
            raise

    def get_balance(self, address: str):
        """Get account balance using System.Account storage query."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            # Validate address format
            if not address or len(address) < 10:
                raise Exception("Invalid address format")

            # Query account balance using the System pallet
            account_info = self.substrate.query(
                module="System", storage_function="Account", params=[address]
            )

            balance = (
                account_info.value["data"]["free"]
                if account_info and account_info.value
                else 0
            )

            return BalanceResponse(
                success=True,
                message="Balance retrieved successfully",
                data={
                    "address": address,
                    "balance": balance,
                    "formatted_balance": f"{balance / 1e12:.6f} TENSOR",
                },
            )
        except Exception as e:
            logger.error(f"Failed to get balance: {str(e)}")
            raise

    # Additional wallet operations based on discovered Network pallet methods
    def claim_unbondings(self, keypair=None):
        """Claim unbondings using Network.claim_unbondings."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            call_data = self.substrate.compose_call(
                call_module="Network", call_function="claim_unbondings", call_params={}
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return UnbondingClaimResponse(
                    success=True,
                    message="Unbondings claimed successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return UnbondingClaimResponse(
                    success=True,
                    message="Unbonding claim call composed successfully",
                    transaction_hash="0x" + "0" * 64,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to claim unbondings: {str(e)}")
            raise

    def add_to_delegate_stake(
        self, subnet_id: int, stake_to_be_added: int, keypair=None
    ):
        """Add to delegate stake using Network.add_to_delegate_stake."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="add_to_delegate_stake",
                call_params={
                    "subnet_id": subnet_id,
                    "stake_to_be_added": stake_to_be_added,
                },
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return DelegateStakeAddResponse(
                    success=True,
                    message="Delegate stake added successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return DelegateStakeAddResponse(
                    success=True,
                    message="Delegate stake addition call composed successfully",
                    transaction_hash="0x" + "0" * 64,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to add delegate stake: {str(e)}")
            raise

    def transfer_delegate_stake(
        self,
        from_subnet_id: int,
        to_subnet_id: int,
        delegate_stake_shares_to_be_switched: int,
        keypair=None,
    ):
        """Transfer delegate stake using Network.transfer_delegate_stake."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="transfer_delegate_stake",
                call_params={
                    "from_subnet_id": from_subnet_id,
                    "to_subnet_id": to_subnet_id,
                    "delegate_stake_shares_to_be_switched": delegate_stake_shares_to_be_switched,
                },
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return DelegateStakeTransferResponse(
                    success=True,
                    message="Delegate stake transferred successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return DelegateStakeTransferResponse(
                    success=True,
                    message="Delegate stake transfer call composed successfully",
                    transaction_hash="0x" + "0" * 64,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to transfer delegate stake: {str(e)}")
            raise

    def remove_delegate_stake(
        self, subnet_id: int, shares_to_be_removed: int, keypair=None
    ):
        """Remove delegate stake using Network.remove_delegate_stake."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="remove_delegate_stake",
                call_params={
                    "subnet_id": subnet_id,
                    "shares_to_be_removed": shares_to_be_removed,
                },
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return DelegateStakeRemoveResponse(
                    success=True,
                    message="Delegate stake removed successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return DelegateStakeRemoveResponse(
                    success=True,
                    message="Delegate stake removal call composed successfully",
                    transaction_hash="0x" + "0" * 64,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to remove delegate stake: {str(e)}")
            raise

    def update_coldkey(self, hotkey: str, new_coldkey: str, keypair=None):
        """Update coldkey using Network.update_coldkey."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="update_coldkey",
                call_params={"hotkey": hotkey, "new_coldkey": new_coldkey},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return ColdkeyUpdateResponse(
                    success=True,
                    message="Coldkey updated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return ColdkeyUpdateResponse(
                    success=True,
                    message="Coldkey update call composed successfully",
                    transaction_hash="0x" + "0" * 64,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to update coldkey: {str(e)}")
            raise

    def update_hotkey(self, old_hotkey: str, new_hotkey: str, keypair=None):
        """Update hotkey using Network.update_hotkey."""
        try:
            if not self.substrate:
                raise Exception("Not connected to blockchain")

            call_data = self.substrate.compose_call(
                call_module="Network",
                call_function="update_hotkey",
                call_params={"old_hotkey": old_hotkey, "new_hotkey": new_hotkey},
            )

            if keypair:
                extrinsic = self.substrate.create_signed_extrinsic(
                    call=call_data, keypair=keypair
                )

                receipt = self.substrate.submit_extrinsic(
                    extrinsic=extrinsic, wait_for_inclusion=True
                )

                return HotkeyUpdateResponse(
                    success=True,
                    message="Hotkey updated successfully",
                    transaction_hash=receipt.extrinsic_hash,
                    block_number=receipt.block_number,
                    data={"receipt": receipt},
                )
            else:
                return HotkeyUpdateResponse(
                    success=True,
                    message="Hotkey update call composed successfully",
                    transaction_hash="0x" + "0" * 64,
                    block_number=None,
                    data={"call_data": call_data},
                )
        except Exception as e:
            logger.error(f"Failed to update hotkey: {str(e)}")
            raise
