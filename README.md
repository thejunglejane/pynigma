# pynigma

pynigma is a simple Python client for the [Enigma API](https://app.enigma.io/api).

[![Code Climate](https://codeclimate.com/github/thejunglejane/pynigma/badges/gpa.svg)](https://codeclimate.com/github/thejunglejane/pynigma)

+ [Installation](#installation)
+ [Setup](#setup)
    + [Tests](#tests)
+ [Usage](#usage)
    + [Parameters](#parameters)
+ [Endponts](#endpoints)
    + [Data](#data-endpoint)
    + [Metadata](#metadata-endpoint)
    + [Stats](#stats-endpoint)
    + [Export](#export-endpoint)
    + [Limits](#limits-endpoint)

# Installation

pynigma can be installed using pip
```bash
$ pip install pynigma
```

Or, you can clone this repository and run the setup script
```bash
$ git clone git@github.com:thejunglejane/pynigma.git
$ cd pynigma
$ python setup.py install
```

# Setup

There is no setup required, but I recommend creating a .env that creates an environment variable with your Enigma API key. An example .env is included in this repository. You can copy the .env-example to a .env and fill in your API key, or `echo` the export statement to a .env file from the command line.
```bash
$ cp .env-example .env
$ # or
$ echo `export ENIGMA_API_KEY='<YOUR API KEY HERE>'` >> .env
```

You will need to source the .env file for the `ENIGMA_API_KEY` environment variable to be available in a Terminal session.

### Tests

The [tests](https://www.github.com/thejunglejane/pynigma/tests) for pynigma expect an environment variable named `ENIGMA_API_KEY` to be present. If you don't intend to use an `ENIGMA_API_KEY` environment variable when using pynigma, but would like to run the tests, you can create the environment variable in your current session to enable the tests.
```bash
$ export ENIGMA_API_KEY='<YOUR API KEY HERE>'
```
This variable will not be available in later sessions.

pynigma uses `unittest`. To run the tests
```bash
$ python -m unittest discovery tests/
```

# Usage

```python
from pynigma import client

# Load the ENIGMA_API_KEY environment variable
ENIGMA_API_KEY = os.environ['ENIGMA_API_KEY']

# Create a new instance of the EnigmaAPI class
api = client.EnigmaApi(client_key=ENIGMA_API_KEY)
```

### Parameters

Query parameters are accepted by each endpoint method as `**kwargs`.
```python
params = {'search': '@visitee_lastname=FLOTUS'}
flotus_visitors = api.get_data(
    datapath='us.gov.whitehouse.visitor-list', **params)
```
Check the official [API documentation](https://app.enigma.io/api) for valid parameters and parameter formats for each endpoint. If an invalid parameter for an endpoint is passed, pynigma will throw a nice `ValueError`.


## Endpoints

Each API endpoint is accessed in pretty much the same way. All you need to provide are a datapath (if applicable) and any query parameters.

### Data Endpoint

The [data endpoint](https://app.enigma.io/api#data) provides the actual data associated with table datapaths. The data endpoint is accessed via the `get_data()` method.

```python
from pynigma import client

# Load the ENIGMA_API_KEY environment variable
ENIGMA_API_KEY = os.environ['ENIGMA_API_KEY']

api = client.EnigmaApi(client_key=ENIGMA_API_KEY)

# Get the data on White House salaries in 2011
data = api.get_data(datapath='us.gov.whitehouse.salaries.2011')

data['result'][0]  # the first salary in the dataset
```
### Metadata Endpoint

The [metadata endpoint](https://app.enigma.io/api#metadata) provides the metadata associated with table datapaths. The metadata endpoint is accessed via the `get_metadata()` method.

```python
from pynigma import client

# Load the ENIGMA_API_KEY environment variable
ENIGMA_API_KEY = os.environ['ENIGMA_API_KEY']

api = client.EnigmaApi(client_key=ENIGMA_API_KEY)

# Get the metadata associated with the White House visitors dataset
metadata = api.get_metadata(datapath='us.gov.whitehouse.visitor-list')

# Print the column names in this dataset
for column in metadata['result']['columns']:
    print column['label']
```

### Stats Endpoint

The [stats endpoint](https://app.enigma.io/api#stats) provides statistics on columns within table datapaths. The stats endpoint is accessed via the `get_stats()` method.

```python
from pynigma import client

# Load the ENIGMA_API_KEY environment variable
ENIGMA_API_KEY = os.environ['ENIGMA_API_KEY']

api = client.EnigmaApi(client_key=ENIGMA_API_KEY)

# Get statistics for the type_of_access column in the White House visitors
# dataset
stats = api.get_stats(
    datapath='us.gov.whitehouse.visitor-list', **{'select': 'type_of_access'})

# Print the number of visitors for each type of access
for type in stats['result']['frequency']:
    print type['type_of_access'], type['count']
```
### Export Endpoint

The [export endpoint](https://app.enigma.io/export) provides URLs to gzipped CSV files of table datapaths. The export endpoint is accessed via the `get_export()` method.

```python
from pynigma import client

# Load the ENIGMA_API_KEY environment variable
ENIGMA_API_KEY = os.environ['ENIGMA_API_KEY']

api = client.EnigmaApi(client_key=ENIGMA_API_KEY)

# Get URL for a gzipped CSV of the White House visitors dataset
export = api.get_export(datapath='us.gov.whitehouse.visitor-list')

print export['head_url']  # print the URL
```

### Limits Endpoint

The [limits endpoint](https://app.enigma.io/limits) provides current limits for the API key provided.

```python
from pynigma import client

# Load the ENIGMA_API_KEY environment variable
ENIGMA_API_KEY = os.environ['ENIGMA_API_KEY']

api = client.EnigmaApi(client_key=ENIGMA_API_KEY)

# Get limits for ENIGMA_API_KEY
limits = api.get_limits()
print limits['data']  # remaining data API calls this month
```
