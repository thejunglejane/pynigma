'''This module provides a client for the `Engima API`_.

.. _Engima API: https://app.enigma.io/api

Example:

.. code-block:: python

   >>> import os
   >>> from pynigma import client

   >>> ENIGMA_API_KEY = os.environ['ENIGMA_API_KEY']
   >>> api = client.EnigmaAPI(ENIGMA_API_KEY)
   >>> api
   EnigmaAPI(endpoint=https://api.enigma.io, version=v2)
'''

import decimal
import requests
import warnings
from datetime import date, datetime

API_ENDPOINT = 'https://api.enigma.io'
API_VERSION = 'v2'


def _map_metadata_data_type(metadata_columns):
    # Data type mappings are based on PL/Python
    # PostgreSQL to Python mappings:
    #     http://www.postgresql.org/docs/9.4/static/plpython-data.html
    data_type_codec = {
        'bigint': int,
        'boolean': bool,
        'bytea': str,
        'character varying': str,
        'date': date,
        'double': float,
        'double precision': float,
        'int': int,
        'integer': int,
        'numeric': decimal.Decimal,
        'oid': int,
        'real': float,
        'smallint': int,
        'text': str,
        'timestamp without time zone': datetime,
        'timestamp': datetime,
        'varcahr': str
    }

    for column in metadata_columns:
        # Data types returned by the MetaData endpoint
        # are prefixed with type_
        column['python_type'] = data_type_codec.get(
                ' '.join(column['type'].split('_')[1:]), str)
    return metadata_columns


class EnigmaAPI(object):
    '''This class provides access to Enigma API endpoints.
    
    The available endpoints are:

        * data
        * meta
        * stats
        * export
        * limits

    Each endpoint has a dedicated method that can be used to request
    data from it:

        * :meth:`get_data`
        * :meth:`get_meta`
        * :meth:`get_stats`
        * :meth:`get_export`
        * :meth:`get_limits`

    Query parameters are accepted by each endpoint method as `**kwargs`.

    Example:

    .. code-block:: python

       params = {'search': '@visitee_namelast=FLOTUS'}
       flotus_visitors = api.get_data(
           datapath='us.gov.whitehouse.visitor-list', **params)

    Check the `Enigma API documentation`_ for valid parameters and
    parameter formats for each endpoint.

    .. _Enigma API documentation: https://app.enigma.io/api

    Parameters
    ----------
    client_key : str
        API key

    Returns
    -------
    :class:`EnigmaAPI`
    '''
    _param_mapping = {
        'meta': ['page'],
        'data': ['limit', 'select', 'search',
                 'where', 'conjunction', 'sort', 'page'],
        'stats': ['select', 'operation', 'by', 'of', 'limit',
                  'search', 'where', 'conjunction', 'sort', 'page'],
        'export': ['select', 'search', 'where', 'conjunction', 'sort'],
        'limits': []
    }

    def __init__(self, client_key):
        self.client_key = client_key
        self._endpoint = API_ENDPOINT
        self._version = API_VERSION

        self.request_url = None

    def __repr__(self):
        return 'EnigmaAPI(endpoint={endpoint}, version={version})'.format(
            endpoint=self._endpoint, version=self._version)

    def _check_query_params(self, resource, **kwargs):
        invalid_params = set(
            kwargs.keys()) - set(self._param_mapping[resource])
        if invalid_params:
            raise ValueError(
                'Invalid parameters for the {0} endpoint passed: {1}'.format(
                    resource, invalid_params))
        return True

    def _url_for_datapath(self, resource, datapath, **kwargs):
        if self._check_query_params(resource=resource, **kwargs):
            base_url = '/'.join(
                [self._endpoint, self._version, resource, self.client_key])
            # There is no datapath associated with the limits endpoint.
            if datapath:
                params = ['='.join([k, v]) for k, v in kwargs.items()]
                return '/'.join([base_url, datapath, '?' + '&'.join(params)])
            return base_url

    def _request(self, resource, datapath, **kwargs):
        self.request_url = self._url_for_datapath(
            resource, datapath, **kwargs)
        try:
            res = requests.get(self.request_url)
        except res.status_code != 200:
            warnings.warn('Request returned with status code: {0}.'.format(
                res.status_code))
        finally:
            return res.json()

    def get_data(self, datapath, **kwargs):
        '''Request data from the `data endpoint`_.

        .. _data endpoint: https://app.enigma.io/api#data

        The data endpoint provides the actual data associated with
        table datapaths.  

        Example:
        
        .. code-block:: python

           >>> data = api.get_data(datapath='us.gov.whitehouse.salaries.2011')
           >>> data['result'][0]  # the first salary in the dataset
           {u'status': u'Employee', u'salary': u'70000.00',
           u'name': u'Abrams, Adam W. ', u'pay_basis': u'Per Annum',
           u'position_title': u'REGIONAL COMMUNICATIONS DIRECTOR', u'serialid': 1}

        Parameters
        ----------
        datapath : str
        **kwargs : collections.Mapping
            Optional query parameters

        Returns
        -------
        json

        Raises
        ------
        ValueError
            if an invalid ``datapath`` is provided
        '''
        return self._request(resource='data', datapath=datapath, **kwargs)

    def get_metadata(self, datapath, **kwargs):
        '''Request data from the `metadata endpoint`_.

        .. _metadata endpoint: https://app.enigma.io/api#metadata

        The metadata endpoint provides the metadata associated with
        table datapaths. The column metadata will include an additional
        key, 'python_type', representing the corresponding python data
        type. Data types are based on the `PL/Python PostgreSQL to
        Python mappings`_. If the python data type can't be determined,
        it will default to str.

        .. _PL/Python PostgreSQL to Python mappings: http://www.postgresql.org/docs/9.4/static/plpython-data.html

        Example:

        ..code-block:: python

           >>> metadata = api.get_metadata(datapath='us.gov.whitehouse.visitor-list')
           >>> for column in metadata['result']['columns'][:5]:
           ...     column['label']
           Last Name
           First Name
           Middle Initial
           Full Name
           Appointment Number

        Parameters
        ----------
        datapath : str
        **kwargs : collections.Mapping
            Optional query parameters

        Returns
        -------
        json
        '''
        metadata_res = self._request(
            resource='meta', datapath=datapath, **kwargs)
        metadata_res['result']['columns'] = _map_metadata_data_type(
            metadata_res['result']['columns'])
        return metadata_res

    def get_stats(self, datapath, **kwargs):
        '''Request data from the `stats endpoint`_.

        .. _stats endpoint: https://app.enigma.io/api#stats

        The stats endpoint provides statistics on columns within table
        datapaths.

        Example:

        .. code-block:: python

           >>> stats = api.get_stats(datapath='us.gov.whitehouse.visitor-list',
                                     **{'select': 'type_of_access'})
           >>> for type in stats['result']['frequency']:
           ...     print(type['type_of_access'], type['count'])
           VA 4368369
           AL 32278
           PE 12
           WO 8
           None 0

        Parameters
        ----------
        datapath : str
        **kwargs : collections.Mapping
            Optional query parameters

        Returns
        -------
        json

        Raises
        ------
        ValueError
            if an invalid ``datapath`` is provided
        '''
        return self._request(resource='stats', datapath=datapath, **kwargs)

    def get_export(self, datapath, **kwargs):
        '''Request data from the `export endpoint`_.

        .. _export endpoint: https://app.enigma.io/export

        The export endpoint provides URLs to gzipped CSV files of table
        datapaths.

        Example:

        .. code-block:: python

           >>> export = api.get_export(datapath='us.gov.whitehouse.visitor-list')
           >>> export['head_url']
           https://enigma-api-export...

        Parameters
        ----------
        datapath : str
        **kwargs : collections.Mapping
            Optional query parameters

        Returns
        -------
        json

        Raises
        ------
        ValueError
            if an invalid ``datapath`` is provided
        '''
        return self._request(resource='export', datapath=datapath, **kwargs)

    def get_limits(self):
        '''Request data from the `limits endpoint`_.

        .. _limits endpoint: https://app.enigma.io/limits

        The limits endpoint provides current limits for the API key
        provided to the client.

        Example:

        .. code-block:: python

           >>> api.get_limits()
           {u'seconds_remaining': 1305446, u'stats': 9999, u'period': u'monthly',
           u'meta': 9996, u'export': 48, u'data': 9891}

        Returns
        -------
        json

        Raises
        ------
        ValueError
            if an invalid ``datapath`` is provided
        '''
        return self._request(resource='limits', datapath=None)
