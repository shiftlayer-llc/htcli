import typer

app = typer.Typer(name="node", help="node commands")


@app.command()
def info():
    """
    Get the info of the node
    """
    typer.echo("Getting info of the node...")
    # Here you would implement the logic to get the info of the node
    # For now, we'll just print a message
    # This is a placeholder for the actual implementation
