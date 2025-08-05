"""
Wallet operations command group.
"""

import typer
from . import keys, staking

app = typer.Typer(name="wallet", help="Wallet operations")

# Add all wallet commands to the group
app.add_typer(keys.app, name="keys", help="Key management")
app.add_typer(staking.app, name="stake", help="Staking operations")
