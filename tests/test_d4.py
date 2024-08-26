"""Test basic d4 functions."""

import numpy as np
import pyd4
import pytest
from d4utils.count import count
from d4utils.sum import sum


@pytest.fixture
def d4_factory(tmpdir_factory):
    """Return a d4 file."""

    def _d4_factory(
        chroms,
        coverage,
        prefix="data",
        outdir=None,
    ):
        if outdir is None:
            outdir = tmpdir_factory.mktemp("d4")
        fn = outdir / f"{prefix}.d4"
        for chrom, length in chroms:
            writer = (
                pyd4.D4Builder(str(fn))
                .add_chroms([(chrom, length)])
                .set_dict_bits(2)
                .get_writer()
            )
            writer.write_np_array(chrom, 0, coverage[chrom])
        writer.close()
        return fn

    return _d4_factory


@pytest.fixture
def d1(d4_factory, tmpdir_factory):
    """Return a d4 file."""
    outdir = tmpdir_factory.mktemp("d4")
    d1 = d4_factory(
        chroms=[("chr1", 1000)],
        coverage={"chr1": np.ones(1000)},
        prefix="d1",
        outdir=outdir,
    )
    return d1


@pytest.fixture
def d2(d4_factory, tmpdir_factory):
    """Return a d4 file."""
    outdir = tmpdir_factory.mktemp("d4")
    d2 = d4_factory(
        chroms=[("chr1", 1000)],
        coverage={"chr1": np.zeros(1000)},
        prefix="d2",
        outdir=outdir,
    )
    return d2


@pytest.fixture
def d3(d4_factory, tmpdir_factory):
    """Return a d4 file."""
    outdir = tmpdir_factory.mktemp("d4")
    d3 = d4_factory(
        chroms=[("chr1", 1000)],
        coverage={"chr1": np.concatenate([np.zeros(500), np.ones(500)])},
        prefix="d3",
        outdir=outdir,
    )
    return d3


@pytest.fixture
def d4(d4_factory, tmpdir_factory):
    """Return a d4 file."""
    outdir = tmpdir_factory.mktemp("d4")
    d4 = d4_factory(
        chroms=[("chr1", 1000)],
        coverage={"chr1": np.concatenate([np.zeros(500), 2 * np.ones(500)])},
        prefix="d3",
        outdir=outdir,
    )
    return d4


def test_sum(runner, d1, d2, d3) -> None:
    """Test sum."""
    out = d1.dirpath() / "out.d4"
    result = runner.invoke(sum, [str(d1), str(d2), str(d3), str(out)])
    assert result.exit_code == 0
    file = pyd4.D4File(str(out))
    x = file.load_to_np("chr1")
    assert np.all(x[0:500] == 1)
    assert np.all(x[500:1000] == 2)


def test_sum_fail(runner, d1, d2, d3) -> None:
    """Test sum fail."""
    result = runner.invoke(sum, [str(d1), str(d2), str(d1)])
    assert result.exit_code != 0


testdata = [
    (
        ["--min-coverage", "1"],
        np.concat([np.ones(500, dtype=int), 3 * np.ones(500, dtype=int)]),
    ),
    (
        ["--min-coverage", "1", "-j", "2"],
        np.concat([np.ones(500, dtype=int), 3 * np.ones(500, dtype=int)]),
    ),
    (
        ["--max-coverage", "1"],
        np.concat([4 * np.ones(500, dtype=int), 3 * np.ones(500, dtype=int)]),
    ),
    (
        ["--max-coverage", "1", "-j", "2"],
        np.concat([4 * np.ones(500, dtype=int), 3 * np.ones(500, dtype=int)]),
    ),
]


@pytest.mark.parametrize("options,expected", testdata)
def test_count(runner, d1, d2, d3, d4, options, expected) -> None:
    """Test count."""
    out = d1.dirpath() / "count.d4"
    arglist = [str(d1), str(d2), str(d3), str(d4), str(out)] + options
    result = runner.invoke(count, arglist)
    assert result.exit_code == 0
    file = pyd4.D4File(str(out))
    x = file.load_to_np("chr1")
    assert np.all(x == expected)
