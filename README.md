# D4Utils

[![Status](https://img.shields.io/pypi/status/d4utils.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/d4utils)][python version]
[![License](https://img.shields.io/pypi/l/d4utils)][license]

[![Tests](https://github.com/percyfal/d4utils/workflows/Tests/badge.svg)][tests]

[status]: https://pypi.org/project/d4utils/
[python version]: https://pypi.org/project/d4utils
[tests]: https://github.com/percyfal/d4utils/actions?workflow=Tests

## Features

_D4Utils_ summarizes per-base coverages from multiple D4 files in
parallel.

### sum

Sum per-base coverages over all files to generate a global coverage
distribution for setting coverage-based accessibility mask thresholds.

### count

Count files with coverages within a user-defined range for setting
accessibility mask thresholds based on number of individuals with
sufficient coverage.

## Requirements

- click
- pyd4
- tqdm
- pandas

## Installation

You can install _D4Utils_ via [pip] from the GitHub repository:

```console
pip install git+https://github.com/percyfal/d4utils
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

If you encounter any problems, please [file an issue] along with a
detailed description.

## Credits

[file an issue]: https://github.com/percyfal/d4utils/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/percyfal/d4utils/blob/main/LICENSE
[contributor guide]: https://github.com/percyfal/d4utils/blob/main/CONTRIBUTING.md
[command-line reference]: https://d4utils.readthedocs.io/en/latest/usage.html
