"""
Error handling functions for htcli.
"""

from .base import HTCLIError, TransferError, KeyGenerationError, KeyDeletionError, BalanceError, WalletError


def handle_blockchain_error(error_msg: str) -> HTCLIError:
    """Handle blockchain-specific errors and return appropriate error objects."""

    # Transfer-related errors
    if "Inability to pay some fees" in error_msg or "account balance too low" in error_msg:
        return TransferError(
            "Insufficient balance to complete the transfer. Please ensure you have enough funds to cover both the transfer amount and transaction fees.",
            [
                "Check your current balance: htcli wallet balance --wallet <wallet-name>",
                "Try transferring a smaller amount",
                "Ensure you have enough funds to cover both the transfer and transaction fees",
                "Transaction fees are typically around 0.001-0.01 TENSOR"
            ]
        )

    # Common blockchain error codes
    error_handlers = {
        "1010": ("Transaction failed due to insufficient funds. Please check your balance and ensure you have enough to cover the transfer amount plus fees.", [
            "Check your current balance: htcli wallet balance --wallet <wallet-name>",
            "Try transferring a smaller amount",
            "Transaction fees are typically around 0.001-0.01 TENSOR"
        ]),
        "1014": ("Invalid transaction origin. Please ensure you're using the correct wallet and it has permission to transfer funds.", [
            "Verify you're using the correct wallet name",
            "Check wallet permissions: htcli wallet list",
            "Ensure the wallet exists and is properly configured"
        ]),
        "1015": ("Too many transaction attempts. Please wait a moment before trying again.", [
            "Wait a few seconds before retrying",
            "Check if there are pending transactions",
            "Try again in a moment"
        ]),
        "1016": ("No transaction providers available. Please check your network connection.", [
            "Check your internet connection",
            "Verify the blockchain node is accessible",
            "Try connecting to a different node"
        ]),
        "1017": ("Unsupported transaction version. Please update your client.", [
            "Update your htcli client to the latest version",
            "Check for any available updates",
            "Contact support if the issue persists"
        ]),
        "1018": ("Transaction weight calculation error. Please try with a different amount.", [
            "Try transferring a smaller amount",
            "Check if the amount is within valid limits",
            "Try again with a different amount"
        ]),
        "1019": ("Invalid transaction format. Please check your input parameters.", [
            "Verify the destination address is correct",
            "Check that the amount is a valid number",
            "Ensure all parameters are properly formatted"
        ]),
        "1020": ("Invalid transaction proof. Please ensure your wallet is properly configured.", [
            "Verify your wallet is properly set up",
            "Check wallet configuration: htcli wallet list",
            "Try regenerating your wallet if needed"
        ]),
        "1021": ("Transaction is too old. Please try again with a fresh transaction.", [
            "Try the transaction again",
            "Check your system clock is correct",
            "Wait a moment and retry"
        ]),
        "1022": ("Transaction would exhaust available resources. Please try with a smaller amount.", [
            "Try transferring a smaller amount",
            "Check available resources on the network",
            "Wait and try again later"
        ]),
        "1023": ("Invalid transaction parameters. Please check your destination address and amount.", [
            "Verify the destination address is valid",
            "Check that the amount is reasonable",
            "Ensure all parameters are correct"
        ]),
        "1024": ("Invalid transaction signer. Please ensure you're using the correct wallet and password.", [
            "Verify you're using the correct wallet",
            "Check that your password is correct",
            "Ensure the wallet is properly loaded"
        ]),
        "1025": ("Transaction is stale. Please try again.", [
            "Try the transaction again",
            "Check network conditions",
            "Wait a moment and retry"
        ]),
        "1026": ("Transaction is from the future. Please check your system clock.", [
            "Check your system clock is correct",
            "Synchronize your system time",
            "Try again after fixing the clock"
        ]),
        "1027": ("Transaction would exhaust available resources. Please try with a smaller amount.", [
            "Try transferring a smaller amount",
            "Check network capacity",
            "Wait and try again later"
        ]),
        "1028": ("Invalid transaction signature. Please check your wallet credentials.", [
            "Verify your wallet password is correct",
            "Check that the wallet is properly loaded",
            "Try reloading the wallet"
        ]),
        "1029": ("Invalid transaction nonce. Please try again.", [
            "Try the transaction again",
            "Check for pending transactions",
            "Wait a moment and retry"
        ]),
        "1030": ("Invalid transaction format. Please check your input parameters.", [
            "Verify all parameters are correct",
            "Check the destination address format",
            "Ensure the amount is valid"
        ]),
        "1031": ("Transaction fee is too low. Please try with a higher fee or different amount.", [
            "Try transferring a smaller amount",
            "Wait for network conditions to improve",
            "Try again later"
        ]),
        "1032": ("Transaction fee is too high. Please try with a lower fee or different amount.", [
            "Try transferring a smaller amount",
            "Wait for network conditions to improve",
            "Try again later"
        ]),
        "1033": ("Transaction tip is too high. Please try with a lower tip.", [
            "Try without a tip or with a lower tip",
            "Wait for network conditions to improve",
            "Try again later"
        ]),
        "1034": ("Transaction priority is too low. Please try with a higher fee.", [
            "Try transferring a smaller amount",
            "Wait for network conditions to improve",
            "Try again later"
        ]),
        "1035": ("Invalid transaction. Please check all parameters and try again.", [
            "Verify all input parameters",
            "Check destination address and amount",
            "Ensure wallet is properly configured"
        ]),
        "1036": ("Invalid transaction origin. Please ensure you're using the correct wallet.", [
            "Verify you're using the correct wallet",
            "Check wallet permissions",
            "Ensure the wallet exists"
        ]),
        "1037": ("Invalid transaction call. Please check your destination address.", [
            "Verify the destination address is correct",
            "Check address format",
            "Ensure the address exists"
        ]),
        "1038": ("Transaction service unavailable. Please try again later.", [
            "Wait a moment and try again",
            "Check network connectivity",
            "Try again later"
        ]),
        "1039": ("Custom transaction error. Please check your parameters and try again.", [
            "Verify all parameters are correct",
            "Check wallet configuration",
            "Try again with different parameters"
        ]),
        "1040": ("Bad transaction. Please check your input and try again.", [
            "Verify all input parameters",
            "Check wallet configuration",
            "Try again with correct parameters"
        ]),
        "1041": ("Cannot lookup account information. Please check your destination address.", [
            "Verify the destination address is correct",
            "Check if the address exists",
            "Try a different destination address"
        ]),
        "1042": ("No permission to perform this transaction. Please check your wallet permissions.", [
            "Verify wallet permissions",
            "Check if the wallet can perform this action",
            "Ensure you have the correct wallet"
        ]),
        "1043": ("Unknown transaction error. Please try again or contact support.", [
            "Try the transaction again",
            "Check all parameters",
            "Contact support if the issue persists"
        ]),
        "1044": ("Wrong transaction parameters. Please check your input and try again.", [
            "Verify all parameters are correct",
            "Check input format",
            "Try again with correct parameters"
        ]),
        "1045": ("Invalid transaction. Please check all parameters.", [
            "Verify all input parameters",
            "Check parameter format",
            "Ensure all required fields are provided"
        ]),
        "1046": ("Bad transaction. Please check your input.", [
            "Verify input parameters",
            "Check parameter format",
            "Try again with correct input"
        ]),
        "1047": ("Transaction amount overflow. Please try with a smaller amount.", [
            "Try transferring a smaller amount",
            "Check amount limits",
            "Use a smaller transfer amount"
        ]),
        "1048": ("Transaction amount underflow. Please try with a larger amount.", [
            "Try transferring a larger amount",
            "Check minimum amount requirements",
            "Use a larger transfer amount"
        ]),
        "1049": ("Transaction calculation error. Please try with different parameters.", [
            "Try with different parameters",
            "Check parameter values",
            "Use different input values"
        ]),
        "1050": ("Out of memory error. Please try with a smaller transaction.", [
            "Try transferring a smaller amount",
            "Check system resources",
            "Use a smaller transaction"
        ])
    }

    # Check for specific error codes
    for code, (message, suggestions) in error_handlers.items():
        if code in error_msg:
            return TransferError(message, suggestions)

    # Generic error handling
    if "code" in error_msg and "message" in error_msg:
        return TransferError(
            "Transaction failed with error code. Please check your balance and try again.",
            [
                "Check your current balance: htcli wallet balance --wallet <wallet-name>",
                "Verify all parameters are correct",
                "Try again with different parameters"
            ]
        )

    # Fallback
    return TransferError(f"Transfer failed: {error_msg}")


def handle_wallet_error(error_msg: str, operation: str = "wallet") -> HTCLIError:
    """Handle wallet-related errors and return appropriate error objects."""

    error_msg_lower = error_msg.lower()

    # Key generation errors
    if operation in ["generate", "generate-hotkey", "generate-coldkey"]:
        if "already exists" in error_msg_lower:
            return KeyGenerationError(
                f"Failed to generate {operation.replace('generate-', '')}: {error_msg}",
                [
                    "Use a different name for your key",
                    "Check existing keys: htcli wallet list",
                    f"Delete the existing key first: htcli wallet delete <key-name>"
                ]
            )
        elif "invalid" in error_msg_lower and "name" in error_msg_lower:
            return KeyGenerationError(
                f"Failed to generate {operation.replace('generate-', '')}: {error_msg}",
                [
                    "Use only letters, numbers, hyphens, and underscores",
                    "Avoid special characters and spaces",
                    "Keep the name between 1-32 characters"
                ]
            )
        elif "owner" in error_msg_lower and "not found" in error_msg_lower:
            return KeyGenerationError(
                f"Failed to generate {operation.replace('generate-', '')}: {error_msg}",
                [
                    "Ensure the owner coldkey exists: htcli wallet list",
                    "Create the coldkey first: htcli wallet generate-coldkey",
                    "Check the exact spelling of the owner name"
                ]
            )
        else:
            return KeyGenerationError(f"Failed to generate {operation.replace('generate-', '')}: {error_msg}")

    # Key deletion errors
    elif operation == "delete":
        if "not found" in error_msg_lower:
            return KeyDeletionError(
                f"Failed to delete key: {error_msg}",
                [
                    "Check existing keys: htcli wallet list",
                    "Verify the exact spelling of the key name",
                    "Use quotes around names with spaces: htcli wallet delete \"my key\""
                ]
            )
        elif "permission" in error_msg_lower or "access" in error_msg_lower:
            return KeyDeletionError(
                f"Failed to delete key: {error_msg}",
                [
                    "Ensure you have the correct password",
                    "Check file permissions in your wallet directory",
                    "Try running the command again"
                ]
            )
        else:
            return KeyDeletionError(f"Failed to delete key: {error_msg}")

    # Balance errors
    elif operation == "balance":
        return BalanceError(f"Failed to get balance: {error_msg}")

    # Generic wallet errors
    else:
        return WalletError(f"Wallet operation failed: {error_msg}")


def handle_and_display_error(error: Exception, operation: str = "operation") -> None:
    """Handle and display errors with appropriate formatting."""

    error_msg = str(error)

    # Handle blockchain errors
    if any(keyword in error_msg.lower() for keyword in ["transfer", "transaction", "blockchain", "1010", "1014", "1015"]):
        blockchain_error = handle_blockchain_error(error_msg)
        blockchain_error.display()
    else:
        # Handle wallet errors
        wallet_error = handle_wallet_error(error_msg, operation)
        wallet_error.display()
