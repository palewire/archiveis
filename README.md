# archiveis

A simple Python wrapper for the [archive.is](http://archive.is/) capturing service.

[![PyPI version](https://badge.fury.io/py/archiveis.png)](http://badge.fury.io/py/archiveis)
[![Build Status](https://travis-ci.org/pastpages/archiveis.svg?branch=master)](https://travis-ci.org/pastpages/archiveis)
[![Versions supported](https://img.shields.io/pypi/pyversions/archiveis.svg)](https://pypi.org/project/archiveis)
[![Coverage Status](https://coveralls.io/repos/github/pastpages/archiveis/badge.svg?branch=master)](https://coveralls.io/github/pastpages/archiveis?branch=master)

### Installation

```bash
$ pip install archiveis
```

### Python Usage

Import it.

```python
>>> import archiveis
```

Capture a URL.

```python
>>> archive_url = archiveis.capture("http://www.example.com/")
```

See where it's stored.

```python
>>> print archive_url[0]
http://archive.fo/WxlRK
```

If a URL has been recently cached, archive.is may return the URL to that page rather
than conduct a new capture.

To download the screenshot and/or the zip file corresponding to the archived page:

```python
>>> archive_url, image, zipdata = archiveis.capture("http://www.example.com/", screenshot=True, zip_file=True)
```

### Command-line usage

The Python library is also installed as a command-line interface. You can run it from your terminal like so:

```bash
$ archiveis http://www.example.com/
```

In case you want to download a screenshot of the page, you can use the following option:

```bash
$ archiveis --screenshot http://www.example.com/
```

The command has the same options as the Python API, which you can learn about from its help output.

```bash
$ archiveis --help
Usage: archiveis [OPTIONS] URL

  Archives the provided URL using the archive.is capturing service.

Options:
  -ua, --user-agent TEXT  User-Agent header for the web request
  -s, --screenshot        Download a rendered screenshot (defaults to 'snapshot name'.png)
  -z, --zip-file          Download a ZIP-file containing the webpage (defaults to 'snapshot name'.zip)
  --help                  Show this message and exit.
```
