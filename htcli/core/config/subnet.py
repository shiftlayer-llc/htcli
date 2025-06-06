import typer
from htcli.core.constants import (
    DEFAULT_SUBNET_ID,
    DEFAULT_SUBNET_NAME,
    DEFAULT_NODE_REGISTRATION_EPOCHS,
    DEFAULT_NODE_REGISTRATION_INTERVAL,
    DEFAULT_NODE_AACTIVATION_INTERVAL,
    DEFAULT_NODE_QUEUE_PERIOD,
    DEFAULT_MAX_NODE_PENALTIES,
)
from typing import Optional, List


class subnet_config:
    id = typer.Option(
        None,
        "--subnet.id",
        "--subnet-id",
        "--netuid",
        help="Unique ID for the subnetwork",
    )

    path = typer.Option(
        None,
        "--subnet.path",
        "--subnet-path",
        "--path",
        help="Path to download the model",
    )

    coldkey_whitelist: Optional[List[str]] = typer.Option(
        [],
        "--subnet.coldkey_whitelist",
        "--coldkey-whitelist",
        help="List of coldkeys to whitelist",
    )

    max_node_registration_epochs = typer.Option(
        DEFAULT_NODE_REGISTRATION_EPOCHS,
        "--subnet.max-node-registration-epochs",
        "--max-node-registration-epochs",
        help="Maximum number of epochs for node registration",
    )
    node_registration_interval = typer.Option(
        DEFAULT_NODE_REGISTRATION_INTERVAL,
        "--subnet.node-registration-interval",
        "--node-registration-interval",
        help="How frequently (in blocks) new nodes can be registered to the subnet",
    )
    node_activation_interval = typer.Option(
        DEFAULT_NODE_AACTIVATION_INTERVAL,
        "--subnet.node-activation-interval",
        "--node-activation-interval",
        help="How frequently (in blocks) registered nodes are activated into the network for participation",
    )
    node_queue_period = typer.Option(
        DEFAULT_NODE_QUEUE_PERIOD,
        "--subnet.node-queue-period",
        "--node-queue-period",
        help="How many epochs a node spends in the Queue class (a waiting area) before being considered for consensus",
    )
    max_node_penalties = typer.Option(
        DEFAULT_MAX_NODE_PENALTIES,
        "--subnet.max-node-penalties",
        "--max-node-penalties",
        help="Maximum number of penalties a node can receive before being kicked from the subnet",
    )

    def __repr__(self):
        return f"subnet_config(id={self.id}, path={self.path}, coldkey_whitelist={self.coldkey_whitelist}, max_node_registration_epochs={self.max_node_registration_epochs}, node_registration_interval={self.node_registration_interval}, node_activation_interval={self.node_activation_interval}, node_queue_period={self.node_queue_period}, max_node_penalties={self.max_node_penalties})"

    def __str__(self):
        return f"subnet_config(id={self.id}, path={self.path}, coldkey_whitelist={self.coldkey_whitelist}, max_node_registration_epochs={self.max_node_registration_epochs}, node_registration_interval={self.node_registration_interval}, node_activation_interval={self.node_activation_interval}, node_queue_period={self.node_queue_period}, max_node_penalties={self.max_node_penalties})"

    def __hash__(self):
        return hash(
            (
                self.id,
                self.path,
                self.coldkey_whitelist,
                self.max_node_registration_epochs,
                self.node_registration_interval,
                self.node_activation_interval,
                self.node_queue_period,
                self.max_node_penalties,
            )
        )

    def __eq__(self, other):
        if not isinstance(other, subnet_config):
            return False
        return self.__hash__() == other.__hash__()
