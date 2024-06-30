"""D4Utils command-line interface."""

import click

from d4utils.count import count
from d4utils.sum import sum


@click.group(help=__doc__)
@click.version_option()
def main() -> None:
    """D4Utils."""


main.add_command(sum)
main.add_command(count)


if __name__ == "__main__":
    main(prog_name="d4utils")  # pragma: no cover
