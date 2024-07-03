# D4Utils

[![PyPI](https://img.shields.io/pypi/v/d4utils.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/d4utils.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/d4utils)][python version]
[![License](https://img.shields.io/pypi/l/d4utils)][license]

[![Read the documentation at https://d4utils.readthedocs.io/](https://img.shields.io/readthedocs/d4utils/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/percyfal/d4utils/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/percyfal/d4utils/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/d4utils/
[status]: https://pypi.org/project/d4utils/
[python version]: https://pypi.org/project/d4utils
[read the docs]: https://d4utils.readthedocs.io/
[tests]: https://github.com/percyfal/d4utils/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/percyfal/d4utils
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

_D4Utils_ summarizes per-base coverages from multiple D4 files in
parallel.

### sum

Sum per-base coverages over all files to generate a global coverage
distribution for setting coverage-based accessibility mask thresholds.

### count

Count files with coverages within a user-defined range for setting accessibility mask thresholds based on number of individuals with sufficient coverage.

## Requirements

- click
- pyd4
- tqdm
- pandas

## Installation

You can install _D4Utils_ via [pip] from the GitHub repository:

```console
$ pip install git+https://github.com/percyfal/d4utils
```

## Usage

Please see the [Command-line Reference] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_D4Utils_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/percyfal/d4utils/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/percyfal/d4utils/blob/main/LICENSE
[contributor guide]: https://github.com/percyfal/d4utils/blob/main/CONTRIBUTING.md
[command-line reference]: https://d4utils.readthedocs.io/en/latest/usage.html
