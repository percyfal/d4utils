"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """D4Utils."""


if __name__ == "__main__":
    main(prog_name="d4utils")  # pragma: no cover
