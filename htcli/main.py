# Import the 'typer' module which is used to create command-line interfaces (CLI)
import typer

# Import the command modules for chain, subnet, and wallet functionalities
# These modules contain the specific commands related to each functionality
from htcli.commands import chain, subnet, wallet

# Create a Typer application instance named 'app'
# This instance will serve as the main entry point for the CLI tool
app = typer.Typer(name="htcli", help="Hypertensor CLI Tool")

# Add the 'chain' command group to the main Typer application
# The 'chain.app' is a Typer instance that contains commands related to blockchain operations
app.add_typer(chain.app, name="chain", help="Chain commands")

# Add the 'subnet' command group to the main Typer application
# The 'subnet.app' is a Typer instance that contains commands related to subnet operations
app.add_typer(subnet.app, name="subnet", help="Subnet commands")

# Add the 'wallet' command group to the main Typer application
# The 'wallet.app' is a Typer instance that contains commands related to wallet operations
app.add_typer(wallet.app, name="wallet", help="Wallet commands")

# Check if the script is being run directly (not imported as a module)
# If true, execute the Typer application to start the CLI
if __name__ == "__main__":
    app()
