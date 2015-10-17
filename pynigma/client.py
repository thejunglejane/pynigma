from datetime import date, datetime
import decimal
import requests
import warnings

API_ENDPOINT = 'https://api.enigma.io'
API_VERSION = 'v2'


# Data type mappings are based on PL/Python PostgreSQL to Python mappings
# http://www.postgresql.org/docs/9.4/static/plpython-data.html
_data_type_mapping = {
    'bigint': long,
    'boolean': bool,
    'bytea': str,
    'character varying': str,
    'date': date,
    'double': float,
    'double precision': float,
    'int': int,
    'integer': int,
    'numeric': decimal.Decimal,
    'oid': long,
    'real': float,
    'smallint': int,
    'text': str,
    'timestamp without time zone': datetime,
    'timestamp': datetime,
    'varcahr': str
}


class EnigmaAPI(object):

    '''The EnigmaAPI provides access to the five different endpoints of the
    Enigma API: meta, data, stats, export, and limits.

    ARGUMENTS
    ---------
    client_key      : a string corresponding to a valid API key

    EXAMPLE 
    -------
    >>> from pynigma import client
    >>> import os
    >>> ENIGMA_API_KEY = os.environ['ENIGMA_API_KEY']
    >>> api = client.EnigmaAPI(ENIGMA_API_KEY)
    >>> api
    <EnigmaAPI(endpoint=https://api.enigma.io, version=v2)>
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
        return '<EnigmaAPI(endpoint={endpoint}, version={version})>'.format(
            endpoint=self.endpoint, version=self.version)

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
                params = ['='.join([k, v]) for k, v in kwargs.iteritems()]
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
        '''Returns an HTTP response from the data endpoint as decoded JSON.

        ARGUMENTS
        ---------
        datapath            : a string corresponding to the dataset requested
        **kwargs            : a dictionary of keyword arguments corresponding
                              to the provided query parameters and values

        EXAMPLE
        -------
        >>> data = api.get_data(datapath='us.gov.whitehouse.salaries.2011')
        >>> data['result'][0]  # the first salary in the dataset
        {u'status': u'Employee', u'salary': u'70000.00',
        u'name': u'Abrams, Adam W. ', u'pay_basis': u'Per Annum',
        u'position_title': u'REGIONAL COMMUNICATIONS DIRECTOR', u'serialid': 1}
        '''
        return self._request(resource='data', datapath=datapath, **kwargs)

    def get_metadata(self, datapath, **kwargs):
        '''Returns an HTTP response from the metadata endpoint as decoded JSON.
        The column metadata will include an additional key, 'python_type',
        representing the corresponding Python data type. If the Python data
        type can't be determined, it will default to str.

        ARGUMENTS
        ---------
        datapath            : a string corresponding to the dataset requested
        **kwargs            : a dictionary of keyword arguments corresponding
                              to the provided query parameters and values

        EXAMPLE
        -------
        >>> metadata = api.get_metadata(
                datapath='us.gov.whitehouse.visitor-list')
        >>> for column in metadata['result']['columns'][:5]:
        ...     print column['label']
        Last Name
        First Name
        Middle Initial
        Full Name
        Appointment Number
        '''
        metadata_res =  self._request(
            resource='meta', datapath=datapath, **kwargs)
        # Map returned type strings to Python data types
        for column in metadata_res['result']['columns']:
            column['python_type'] = _data_type_mapping.get(
                column['type'].split('_')[1], str)
        return metadata_res

    def get_stats(self, datapath, **kwargs):
        '''Returns an HTTP response from the stats endpoint as decoded JSON.

        ARGUMENTS
        ---------
        datapath            : a string corresponding to the dataset requested
        **kwargs            : a dictionary of keyword arguments corresponding
                              to the provided query parameters and values

        EXAMPLE
        -------
        >>> stats = api.get_stats(datapath='us.gov.whitehouse.visitor-list',
                                  **{'select': 'type_of_access'})
        >>> for type in stats['result']['frequency']:
        ...     print type['type_of_access'], type['count']
        VA 4368369
        AL 32278
        PE 12
        WO 8
        None 0
        '''
        return self._request(resource='stats', datapath=datapath, **kwargs)

    def get_export(self, datapath, **kwargs):
        '''Returns an HTTP response from the export endpoint as decoded JSON.

        ARGUMENTS
        ---------
        datapath            : a string corresponding to the dataset requested
        **kwargs            : a dictionary of keyword arguments corresponding
                              to the provided query parameters and values

        EXAMPLE
        -------
        >>> export = api.get_export(datapath='us.gov.whitehouse.visitor-list')
        >>> print export['head_url']
        https://enigma-api-export...
        '''
        return self._request(resource='export', datapath=datapath, **kwargs)

    def get_limits(self, resource='limits'):
        '''Returns an HTTP response from the limits endpoint as decoded JSON.
        EXAMPLE
        -------
        >>> api.get_limits()
        {u'seconds_remaining': 1305446, u'stats': 9999, u'period': u'monthly',
        u'meta': 9996, u'export': 48, u'data': 9891}
        '''
        return self._request(resource='limits', datapath=None)
