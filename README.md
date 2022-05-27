# archiveis

A simple Python wrapper for the [archive.is](http://archive.is/) capturing service.

![Tests](https://github.com/pastpages/archiveis/workflows/Tests/badge.svg)

### Installation

```bash
pipenv install archiveis
```

### Python Usage

Import it.

```python
import archiveis
```

Capture a URL.

```python
archive_url = archiveis.capture("http://www.example.com/")
```

If a URL has been recently cached, archive.is may return the URL to that page rather
than conduct a new capture.

### Command-line usage

The Python library is also installed as a command-line interface. You can run it from your terminal like so:

```bash
archiveis http://www.example.com/
```

The command has the same options as the Python API, which you can learn about from its help output.

```bash
$ archiveis --help
Usage: archiveis [OPTIONS] URL

  Archives the provided URL using the archive.is capturing service.

Options:
  -ua, --user-agent TEXT  User-Agent header for the web request
  --help                  Show this message and exit.
```

### Contributing

Install dependencies for development.

```bash
pipenv install --dev
```

Run tests.

```bash
make test
```

Ship new version to PyPI

```bash
make ship
```

### Developing the CLI

The command-line interface is implemented using Click and setuptools. To install it locally for development inside your virtual environment, run the following installation command, as [prescribed by the Click documentation](https://click.palletsprojects.com/en/7.x/setuptools/#setuptools-integration).

```bash
pip install --editable .
```
