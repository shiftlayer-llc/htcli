import typer
from htcli.core.config import subnet_config

app = typer.Typer(name="subnet", help="Subnet commands")


@app.command()
def info(subnet_id: int = subnet_config.id, subnet_name: str = subnet_config.name):
    """
    Get the info of the subnet
    """
    typer.echo(f"Getting info of subnet {subnet_name} with {subnet_id} ...")
    # Here you would implement the logic to get the info of the subnet
    # For now, we'll just print a message
    # This is a placeholder for the actual implementation
