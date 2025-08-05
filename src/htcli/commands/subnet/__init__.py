"""
Subnet operations command group.
"""

import typer
from . import register, manage, nodes

app = typer.Typer(name="subnet", help="Subnet operations")

# Add all subnet commands to the group
app.add_typer(register.app, name="register", help="Subnet registration")
app.add_typer(manage.app, name="manage", help="Subnet management")
app.add_typer(nodes.app, name="nodes", help="Subnet node operations")
