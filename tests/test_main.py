"""Test cases for the __main__ module."""

from click.testing import CliRunner
from d4utils import __main__


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0
