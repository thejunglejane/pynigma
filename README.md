# pynigma

`pynigma` is a Python client for the [Enigma API](https://app.enigma.io/api).

[![Code Climate](https://codeclimate.com/github/thejunglejane/pynigma/badges/gpa.svg)](https://codeclimate.com/github/thejunglejane/pynigma)

# Installation

`pynigma` can be installed using pip

```bash
pip install pynigma
```

## Setup

There is no setup required, but I recommend creating a .env that creates an environment variable with your Enigma API key. An example .env is included in this repository. You can copy the .env-example to a .env and fill in your API key, or `echo` the export statement to a .env file from the command line.

```bash
cp .env-example .env
# or
echo `export ENIGMA_API_KEY='<YOUR API KEY HERE>'` >> .env
```

You will need to source the .env file to make `$ENIGMA_API_KEY` available in your environment.

# Documentation

Documentation can be built with

```bash
python setup.py build_sphinx
cd build/html/sphinx; python -m http.server 6969
```


# Tests

`pynigma` is tested with `unittest`. To run the tests

```bash
python -m unittest discover tests/
```

To run tests with coverage

```bash
coverage run setup.py test
coverage report
```

To see an HTML coverage report

```bash
coverage html
cd build/html/coverage; python -m http.server 6969
```
