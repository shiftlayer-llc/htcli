"""
Chain operations command group.
"""

import typer
from . import info, query

app = typer.Typer(name="chain", help="Chain operations")

# Add all chain commands to the group
app.add_typer(info.app, name="info", help="Chain information")
app.add_typer(query.app, name="query", help="Data queries")
