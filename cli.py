import click
from server import launch_server
from utils import cli_args
import colorama

@click.group()
@click.version_option()
def cli():
    pass


@cli.command()
@cli_args.HOST
@cli_args.PORT
@cli_args.WORKERS
def ui(host, port, workers):
    """This command launches the web interface for Algoz."""
    colorama.init()
    launch_server(host, port, workers)

if __name__ == '__main__':
    cli()