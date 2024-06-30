"""Arguments for the CLI."""

import logging
import pathlib
import sys
from typing import Callable

import click
from click.decorators import FC


def outfile() -> Callable[[FC], FC]:
    """Add outfile argument."""

    def outfile_callback(
        ctx: click.core.Context, param: click.core.Option, value: pathlib.Path
    ) -> pathlib.Path:  # pylint: disable=unused-argument
        """Outfile callback."""
        if pathlib.Path(value).exists():
            logging.error(
                f"{value} exists! Make sure to provide "
                "a non-existing output file name"
            )
            sys.exit(1)
        return value

    return click.argument(
        "outfile", type=click.Path(exists=False), callback=outfile_callback
    )
