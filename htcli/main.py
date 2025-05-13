import typer

from htcli.commands import chain, subnet, wallet

app = typer.Typer(name="htcli", help="Hypertensor CLI Tool")


app.add_typer(chain.app, name="chain", help="Chain commands")
app.add_typer(subnet.app, name="subnet", help="Subnet commands")
app.add_typer(wallet.app, name="wallet", help="Wallet commands")

if __name__ == "__main__":
    app()
