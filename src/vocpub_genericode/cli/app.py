from typing import Annotated
from pathlib import Path

import typer

from vocpub_genericode import __version__
from vocpub_genericode.cli.console import console
from vocpub_genericode.utils import RDF_FILE_EXTENSIONS

app = typer.Typer(
    invoke_without_command=True,
    context_settings={
        "help_option_names": ["-h", "--help"],
    },
)


@app.callback(invoke_without_command=True)
def main(
    version: Annotated[bool, typer.Option("--version", "-v", is_eager=True)] = False,
):
    """Main callback for the CLI app"""
    if version:
        console.print(__version__)
        raise typer.Exit()


@app.command(name="r", help="Convert a Genericode file to VocPub SKOS RDF")
def to_rdf(
    file: Path,
):
    if not file.is_file():
        raise ValueError(f"{file} is not a file")
    elif not file.name.endswith(".gc"):
        raise ValueError(f"{file} does not end with '.gc', the Genericode file extension")

    console.print("to rdf")


@app.command(name="g", help="Convert a ocPub SKOS RDF to Genericode")
def to_genericode(
        file: Path,
):
    if not file.is_file():
        raise ValueError(f"{file} is not a file")
    elif not file.name.endswith(tuple(RDF_FILE_EXTENSIONS)):
        raise ValueError(f"{file} does not end with a known RDF file extension. Must be one of {', '.join(RDF_FILE_EXTENSIONS)}")

    console.print("to genericode")