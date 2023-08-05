# rtorrent-migrate
rtorrent-migrate is a command-line utility used to bulk-convert your data and/or session directory of torrents in rTorrent

It also includes a class that can be used in Python scripts

Usage documentation and examples are available [here](https://adralioh.gitlab.io/rtorrent-migrate)

## Requirements
- [Python 3.6+](https://www.python.org/)
- [benparse](https://gitlab.com/adralioh/benparse)

## Installation
Install from PyPI:
```shell
pip3 install rtorrent-migrate
```

Install from source:
```shell
git clone https://gitlab.com/adralioh/rtorrent-migrate.git
pip3 install ./rtorrent-migrate
```

If you don't want to install, you can also run the module directly:
```shell
# Run from within the git repo
python3 -m rtorrent_migrate --help
```

## Tests
Tests are run using the built-in `unittest` module, and [Coverage.py](https://coverage.readthedocs.io/) is used to measure code coverage

Run tests without measuring coverage:
```shell
python3 -m unittest discover -s tests -t .
```

Run tests and measure coverage:
```shell
coverage run -m unittest discover -s tests -t .
```

View the results:
```shell
coverage report
```

Generate a detailed report, outputted to `./htmlcov`:
```shell
coverage html
```

## Building documentation
Sphinx is used to build documentation

Build requirements:
- [Sphinx](https://www.sphinx-doc.org/)
- [sphinx-argparse](https://github.com/alex-rudakov/sphinx-argparse)

How to build:
```shell
cd docs
make html
```
