import typer

app = typer.Typer()


@app.command()
def info():
    """
    Get the info of the wallet
    """
    typer.echo("Getting info of the wallet...")
    # Here you would implement the logic to get the info of the wallet
    # For now, we'll just print a message
    # This is a placeholder for the actual implementation
