import typer
from typing import Any, Optional
from substrateinterface import SubstrateInterface, Keypair, ExtrinsicReceipt
from substrateinterface.exceptions import SubstrateRequestException
from tenacity import retry, stop_after_attempt, wait_fixed
from htcli.core.constants import BLOCK_SECS
from rich.console import Console
from htcli.utils.helpers import check_balance
console = Console()
retry_counter = 0





def register_subnet(
    substrate: SubstrateInterface,
    keypair: Keypair,
    path: str,
    max_node_registration_epochs: int,
    node_registration_interval: int,
    node_activation_interval: int,
    node_queue_period: int,
    max_node_penalties: int,
    coldkey_whitelist: set[str],
) -> ExtrinsicReceipt:
    """
    Registers a new subnet on the blockchain.

    :param substrate: Substrate interface instance connected to the chain.
    :param keypair: Keypair of the caller (must be authorized to register a subnet).
    :param path: Model path to be downloaded by subnet participants.
    :param max_node_registration_epochs: Number of epochs allowed for node registration.
    :param node_registration_interval: Block interval between node registrations.
    :param node_activation_interval: Block interval for node activation.
    :param node_queue_period: Block window for queued node participation.
    :param max_node_penalties: Maximum number of penalties before node ejection.
    :param coldkey_whitelist: Set of SS58 coldkey addresses allowed to participate.
    :return: ExtrinsicReceipt containing the result of the transaction.
    """

    # Compose the call payload
    call = substrate.compose_call(
        call_module="Network",
        call_function="register_subnet",
        call_params={
            "subnet_data": {
                "path": path,
                "max_node_registration_epochs": max_node_registration_epochs,
                "node_registration_interval": node_registration_interval,
                "node_activation_interval": node_activation_interval,
                "node_queue_period": node_queue_period,
                "max_node_penalties": max_node_penalties,
                "coldkey_whitelist": list(coldkey_whitelist),
            }
        },
    )
    # Check if the call can be paid
    check_balance(substrate, call, keypair)
    # Create the signed extrinsic
    extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)

    @retry(wait=wait_fixed(BLOCK_SECS + 1), stop=stop_after_attempt(4))
    def submit_extrinsic() -> ExtrinsicReceipt:
        try:
            with substrate as _substrate:
                receipt = _substrate.submit_extrinsic(
                    extrinsic, wait_for_inclusion=True
                )
                return receipt
        except SubstrateRequestException as e:
            console.print(f"[Retry] Failed to submit extrinsic: {e}")
            raise

    with console.status(
        "[bold green]Registering subnet...[/bold green]", spinner="dots"
    ):
        return submit_extrinsic()




def get_subnets_list(substrate: SubstrateInterface):
    """
    Get a list of all registered subnets with their data.

    :param substrate: interface to blockchain
    :return: list of (subnet_id, subnet_data)
    """

    @retry(wait=wait_fixed(BLOCK_SECS + 1), stop=stop_after_attempt(4))
    def query_all():
        try:
            with substrate as _substrate:
                max_subnets = int(str(_substrate.query("Network", "TotalSubnetUids")))
                subnets = []
                for subnet_id in range(max_subnets + 1):
                    result = _substrate.query("Network", "SubnetsData", [subnet_id])
                    if result.value is not None:  # Means the subnet exists
                        total_active_nodes = _substrate.query(
                            "Network", "TotalActiveSubnetNodes", [subnet_id]
                        )
                        subnet_owner = _substrate.query(
                            "Network", "SubnetOwner", [subnet_id]
                        )
                        result.value["total_active_nodes"] = (
                            total_active_nodes.value if total_active_nodes else 0
                        )
                        result.value["subnet_owner"] = (
                            subnet_owner.value if subnet_owner else None
                        )
                        subnets.append(result.value)
                return subnets
        except SubstrateRequestException as e:
            console.print(f"Failed to get subnets list: {e}")
            raise

    return query_all()


def activate_subnet(
    substrate: SubstrateInterface,
    keypair: Keypair,
    subnet_id: str,
) -> ExtrinsicReceipt:
    """
    Activate a registered subnet node

    :param substrate: interface to blockchain
    :param keypair: keypair of extrinsic caller. Must be a subnet_node in the subnet
    """

    # compose call
    call = substrate.compose_call(
        call_module="Network",
        call_function="activate_subnet",
        call_params={
            "subnet_id": subnet_id,
        },
    )

    # @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(4))
    @retry(wait=wait_fixed(BLOCK_SECS + 1), stop=stop_after_attempt(4))
    def submit_extrinsic():
        try:
            with substrate as _substrate:
                # get none on retries
                nonce = _substrate.get_account_nonce(keypair.ss58_address)

                # create signed extrinsic
                extrinsic = _substrate.create_signed_extrinsic(
                    call=call, keypair=keypair, nonce=nonce
                )

                receipt = _substrate.submit_extrinsic(
                    extrinsic, wait_for_inclusion=True
                )
                return receipt
        except SubstrateRequestException as e:
            console.print("Failed to send: {}".format(e))

    return submit_extrinsic()


def remove_subnet(
    substrate: SubstrateInterface,
    keypair: Keypair,
    subnet_id: str,
) -> ExtrinsicReceipt:
    """
    Remove a subnet

    :param substrate: interface to blockchain
    :param keypair: keypair of extrinsic caller. Must be a subnet_node in the subnet
    :param subnet_id: subnet ID
    """

    # compose call
    call = substrate.compose_call(
        call_module="Network",
        call_function="remove_subnet",
        call_params={
            "subnet_id": subnet_id,
        },
    )

    # create signed extrinsic
    extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)

    @retry(wait=wait_fixed(BLOCK_SECS + 1), stop=stop_after_attempt(4))
    def submit_extrinsic():
        try:
            with substrate as _substrate:
                receipt = _substrate.submit_extrinsic(
                    extrinsic, wait_for_inclusion=True
                )
                return receipt
        except SubstrateRequestException as e:
            console.print("Failed to send: {}".format(e))

    return submit_extrinsic()

def get_subnet_info(substrate: SubstrateInterface, subnet_id: int):
    """
    Query subnet info by subnet ID
    :param SubstrateInterface: substrate interface from blockchain url
    :param subnet_id: subnet ID
    :returns: subnet info
    """
    return_data = {}
    try:
        with substrate as _substrate:
            subnet_meatainfo = _substrate.query("Network", "SubnetsData", [subnet_id])
            return_data["meta"] = subnet_meatainfo.value
            subnet_nodes_data = _substrate.rpc_request(
                method="network_getSubnetNodes", params=[subnet_id]
            )
            total_active_nodes = _substrate.query(
                "Network", "TotalActiveSubnetNodes", [subnet_id]
            )
            subnet_owner = _substrate.query("Network", "SubnetOwner", [subnet_id])

            return_data["meta"]["owner"] = subnet_owner.value
            return_data["meta"]["total_active_nodes"] = total_active_nodes.value
            return_data["nodes"] = subnet_nodes_data
            return_data["is_success"] = True
            return_data["error_message"] = None

            return return_data
    except SubstrateRequestException as e:
        console.print("Failed to get rpc request: {}".format(e))
        return None
