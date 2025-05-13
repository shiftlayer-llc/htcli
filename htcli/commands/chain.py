import typer

app = typer.Typer(name="chain", help="Chain commands")


@app.command()
def info():
    """
    Get the info of the chain
    """
    typer.echo("Getting info of the chain...")
    # Here you would implement the logic to get the info of the chain
    # For now, we'll just print a message
    # This is a placeholder for the actual implementation
