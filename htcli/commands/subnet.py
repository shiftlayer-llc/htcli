import typer

app = typer.Typer()


@app.command()
def info():
    """
    Get the info of the subnet
    """
    typer.echo("Getting info of the subnet...")
    # Here you would implement the logic to get the info of the subnet
    # For now, we'll just print a message
    # This is a placeholder for the actual implementation
