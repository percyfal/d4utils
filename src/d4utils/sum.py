# type: ignore
"""Sum d4 coverage tracks.

Sum first track from multiple d4 files to a single-track file.

"""

import logging
import pathlib

import click
import numpy as np
import numpy.typing as npt
import pandas as pd
import pyd4
from tqdm import tqdm

from d4utils.arguments import outfile
from d4utils.d4 import D4Container, iter_chunks, parse_region
from d4utils.options import chunk_size_option, cores_option, regions_option
from d4utils.options import verbose_option as verbose
from d4utils.queue import init_pool

logger = logging.getLogger(__name__)


@click.command(help=__doc__)
@verbose()
@click.argument("path", nargs=-1, type=click.Path(exists=True))
@outfile()
@regions_option()
@chunk_size_option()
@cores_option()
def sum(  # noqa
    path: list[pathlib.Path],
    outfile: pathlib.Path,
    regions: pd.DataFrame,
    chunk_size: int,
    cores: int,
) -> None:
    """Sum coverages."""
    d4container = D4Container(
        path, outfile=outfile, chunk_size=chunk_size, regions=regions
    )

    tqdm_disable = logger.getEffectiveLevel() > logging.INFO

    pool = init_pool(cores)
    futures = []
    logger.info("Making chunks...")
    for rname in iter_chunks(d4container.chroms, chunk_size, tqdm_disable):
        args = d4container, rname
        futures.append(pool.submit(process_region_chunk, args))

    logger.info("Processing futures...")
    writer = d4container.writer
    for x in tqdm(futures, disable=tqdm_disable):
        rname, y = x.result()
        chrom_name, begin, end = parse_region(rname)
        writer.write_np_array(chrom_name, begin, y)


def process_region_chunk(
    args: tuple[D4Container, str],
) -> tuple[str, npt.NDArray[np.int_]]:
    """Process region chunk."""
    d4c, rname = args
    for i, p in enumerate(d4c.path):
        fh = pyd4.D4File(p)
        x = fh.load_to_np(rname)
        if i == 0:
            data = x
        else:
            data = data + x
    return rname, data
