"""D4 utility classes."""

import logging
import re
from pathlib import Path
from typing import Any, Iterable, Union

import numpy as np
import pyd4
from pandas import DataFrame
from tqdm import tqdm

logger = logging.getLogger(__name__)


def parse_region(
    region: str,
) -> tuple[Union[str, Any], int, Union[int, float]]:
    """Parse region string."""
    m = re.match(r"([\w]+):([\d]+)-([\d]+)$", region)
    if m:
        chrom, begin, end = m.groups()
        assert int(begin) < int(end), "begin must be less than end"
        return chrom, int(begin), int(end)
    m = re.match(r"([\w]+)$", region)
    if m:
        chrom = m.groups()[0]
        return chrom, 0, np.inf
    logger.error("Invalid region argument: %s", region)
    raise ValueError("Invalid region argument: %s" % region)


def make_chunks(begin: int, end: int, size: int) -> Iterable[tuple[int, int]]:
    """Make chunks of a given size."""
    pos = np.arange(begin, end, size)
    begin_list = pos
    end_list = pos[1 : len(pos)]  # noqa: E203
    end_list = np.append(end_list, end)
    for begin, end in zip(begin_list, end_list):
        yield begin, end


def iter_chunks(
    chroms: list[tuple[str, int]], chunk_size: int, tqdm_disable: bool
) -> Iterable[str]:
    """Iterate over chunks."""
    for chrom_name, end in (pbar := tqdm(chroms, disable=tqdm_disable)):
        pbar.set_description(f"Processing chromosome {chrom_name}")
        for rbegin, rend in make_chunks(0, end, chunk_size):
            rname = f"{chrom_name}:{rbegin}-{rend}"
            yield rname


class D4Container:
    """D4 container for multiple d4 paths."""

    def __init__(
        self,
        path: list[Path],
        *,
        outfile: Path,
        chunk_size: Union[Any, int] = None,
        regions: Union[Any, DataFrame] = None,
        concat: bool = False,
    ):
        """Create a D4Container."""
        self._path = path
        self._outfile = outfile
        self._min_coverage = 0
        self._max_coverage = np.inf
        self._chunk_size = chunk_size
        self._writer = None
        self._set_chroms(regions, concat)

    def _set_chroms(
        self, regions: Union[None, DataFrame], concat: bool
    ) -> None:
        """Set chroms."""
        self._chroms = []
        if concat:
            chroms = [pyd4.D4File(x).chroms() for x in self.path]
        else:
            chroms = pyd4.D4File(self.path[0]).chroms()
        chromlen = {k: v for k, v in chroms}
        if regions is None:
            self._chroms = chroms
        else:
            for _, row in regions.iterrows():
                chrom_name, begin, end = row
                if chrom_name not in chromlen:
                    logger.warning(
                        "region %s:%s-%s not in chromosome list; skipping",
                        chrom_name,
                        begin,
                        end,
                    )
                    continue
                if (begin != 0) or (end < chromlen[chrom_name]):
                    s = (
                        "Region %s:%s-%s smaller than / outside "
                        + "reference chromosome (0-%s). "
                        + "This is currently unsupported; "
                        + "using entire chromosome."
                    )
                    logger.warning(
                        s, chrom_name, begin, end, chromlen[chrom_name]
                    )
                    begin = 0
                    end = chromlen[chrom_name]
                if end > chromlen[chrom_name]:
                    logger.warning(
                        "region %s:%s-%s end larger than reference "
                        + "chromosome length (%s); resetting",
                        chrom_name,
                        begin,
                        end,
                        chromlen[chrom_name],
                    )
                    end = chromlen[chrom_name]
                self._chroms.append((chrom_name, end))

    @property
    def path(self) -> list[Path]:
        """Return path."""
        return self._path

    @property
    def outfile(self) -> Path:
        """Return outfile."""
        return self._outfile

    @property
    def chroms(self) -> list[tuple[str, int]]:
        """Return chroms as chromosome name and reference chromosome length."""
        return self._chroms

    @property
    def min_coverage(self) -> int:
        """Return min coverage."""
        return self._min_coverage

    @min_coverage.setter
    def min_coverage(self, value: int) -> None:
        """Set min coverage."""
        self._min_coverage = value

    @property
    def max_coverage(self) -> Union[float, int]:
        """Return max coverage."""
        return self._max_coverage

    @max_coverage.setter
    def max_coverage(self, value: Union[float, int]) -> None:
        """Set max coverage."""
        self._max_coverage = value

    @property
    def chunk_size(self) -> Union[Any, int]:
        """Return chunk size."""
        return self._chunk_size

    @property
    def writer(self) -> pyd4.D4Writer:
        """Return writer."""
        return (
            pyd4.D4Builder(str(self.outfile))
            .add_chroms(self.chroms)
            .get_writer()
        )
