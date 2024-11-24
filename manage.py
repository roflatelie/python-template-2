import click
import uvicorn


@click.group()
def cli():
    """Init event loop, logging config etc."""


@cli.command(short_help="start app")
def start():
    """Start REST API application."""
    from src.interface.rest.litestar import app

    uvicorn.run(app, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    cli()
