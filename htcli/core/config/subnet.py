import typer
from htcli.core.constants import (
    DEFAULT_SUBNET_ID,
    DEFAULT_SUBNET_NAME,
)


class subnet_config:
    id = typer.Option(
        DEFAULT_SUBNET_ID,
        "--subnet.id",
        "--subnet-id",
        "--netuid",
        help="Unique ID for the subnetwork",
    )
    name = typer.Option(
        DEFAULT_SUBNET_NAME,
        "--subnet.name",
        "--subnet-name",
        help="Name of the subnetwork",
    )
