"""Options for the CLI."""

import logging
import os
from typing import Callable
from typing import Union

import click
import numpy as np
import pandas as pd
from click.decorators import FC

from d4utils.d4 import parse_region


def verbose_option(expose_value: bool = False) -> Callable[[FC], FC]:
    """Add verbose option with callback."""

    def verbose_callback(
        ctx: click.core.Context, param: click.core.Option, value: int
    ) -> int:  # pylint: disable=unused-argument
        """Verbose callback."""
        log_level = max(3 - value, 0) * 10
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s; %(levelname)s [%(name)s:%(funcName)s]: %(message)s",
        )
        return log_level

    return click.option(
        "--verbose",
        "-v",
        "logger",
        help="Set the verbosity level",
        count=True,
        callback=verbose_callback,
        expose_value=expose_value,
        is_eager=True,
        default=0,
    )


def cores_option() -> Callable[[FC], FC]:
    """Add cores option."""

    def cores_callback(
        ctx: click.core.Context, param: click.core.Option, value: int
    ) -> int:  # pylint: disable=unused-argument
        """Cores callback."""
        if value < 1:
            logging.error("Cores must be greater than 0")
            raise ValueError("Cores must be greater than 0")
        return value

    return click.option("-j", "--cores", help="number of cores", default=1, type=int)


def chunk_size_option() -> Callable[[FC], FC]:
    """Add chunk size option."""

    def chunk_size_callback(
        ctx: click.core.Context, param: click.core.Option, value: int
    ) -> int:  # pylint: disable=unused-argument
        """Chunk size callback."""
        if value < 1:
            logging.error("Chunk size must be greater than 0")
            raise ValueError("Chunk size must be greater than 0")
        return value

    return click.option(
        "--chunk-size", help="region chunk size", default=1000000, type=int
    )


def regions_option() -> Callable[[FC], FC]:
    """Add regions option and parse arguments to a pandas DataFrame."""

    def regions_callback(
        ctx: click.core.Context, param: click.core.Option, value: Union[str, None]
    ) -> pd.DataFrame:
        """Regions callback."""
        if value is None:
            return None
        if os.path.isfile(value):
            return pd.read_table(
                value, names=["chrom", "begin", "end"], usecols=[0, 1, 2], header=None
            )

        chrom, begin, end = parse_region(value)
        return pd.DataFrame({"chrom": [chrom], "begin": [begin], "end": [end]})

    return click.option(
        "-R",
        "regions",
        help="Operate on region STR or bed file",
        callback=regions_callback,
    )


def min_coverage_option() -> Callable[[FC], FC]:
    """Add min coverage option."""

    def min_coverage_callback(
        ctx: click.core.Context, param: click.core.Option, value: int
    ) -> int:  # pylint: disable=unused-argument
        """Min coverage callback."""
        if value < 0:
            logging.error("Min coverage must be greater than 0")
            raise ValueError("Min coverage must be greater than 0")
        return value

    return click.option(
        "--min-coverage",
        help="min coverage",
        default=0,
        type=int,
        callback=min_coverage_callback,
    )


def max_coverage_option() -> Callable[[FC], FC]:
    """Add max coverage option."""

    def max_coverage_callback(
        ctx: click.core.Context, param: click.core.Option, value: Union[int, None]
    ) -> Union[int, float]:  # pylint: disable=unused-argument
        """Max coverage callback."""
        if value is None:
            return np.inf
        if value < 0:
            logging.error("Max coverage must be greater than 0")
            raise ValueError("Max coverage must be greater than 0")
        return value

    return click.option(
        "--max-coverage", help="max coverage", type=int, callback=max_coverage_callback
    )
