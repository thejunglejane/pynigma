from pynigma import client
import decimal
import mock
import random
import string
import unittest


class TestClient(unittest.TestCase):

    def setUp(self):
        self.new_client = client.EnigmaAPI(
            ''.join(random.choice(string.ascii_lowercase) for _ in range(32)))

    def tearDown(self):
        del self.new_client

    def test_check_query_params_valid_param(self):
        '''Does _check_query_params() return True for a valid parameter?
        '''
        self.assertTrue(
            self.new_client._check_query_params(
                resource='data', **{'search': ''}))

    def test_check_query_params_valid_params(self):
        '''Does _check_query_params() return True for valid parameters?
        '''
        self.assertTrue(
            self.new_client._check_query_params(
                resource='data', **{'search': '', 'limit': ''}))

    def test_check_query_params_invalid_param(self):
        '''Does _check_query_params() raise a ValueError for am invalid
        parameter?
        '''
        with self.assertRaises(ValueError):
            self.new_client._check_query_params(
                resource='meta', **{'limit': ''})

    def test_check_query_params_invalid_params(self):
        '''Does _check_query_params() raise a ValueError for invalid
        parameters?
        '''
        with self.assertRaises(ValueError):
            self.new_client._check_query_params(
                resource='meta', **{'where': '', 'conjunction': ''})

    def test_check_query_params_no_params(self):
        '''Does _check_query_params() return True when no parameters are
        passed?
        '''
        self.assertTrue(self.new_client._check_query_params(resource='stats'))

    def test_url_for_datapath_no_params(self):
        '''Does _url_for_datapath() return a string when no parameters are
        passed?
        '''
        self.assertIsInstance(self.new_client._url_for_datapath(
            resource='stats', datapath='us.gov.whitehouse.salaries.2011'), str)

    def test_url_for_datapath_valid_params(self):
        '''Does _url_for_datapath() return a string when valid parameters are
        passed?
        '''
        self.assertIsInstance(self.new_client._url_for_datapath(
            resource='stats', datapath='us.gov.whitehouse.salaries.2011', **{'operation': ''}), str)

    def test_request_invalid_params(self):
        '''Does _request() raise a ValueError when invalid parameters are
        passed, and NOT set the attribute request_url?
        '''
        with self.assertRaises(ValueError):
            self.new_client._request(
                resource='stats', datapath='us.gov.whitehouse.salaries.2011', **{'invalid': ''})
        self.assertIsNone(self.new_client.request_url)

    def test_get_limits_datapath_failure(self):
        '''Does get_limits() raise a TypeError when a datapath is passed?
        '''
        with self.assertRaises(TypeError):
            self.new_client.get_limits(
                datapath='us.gov.whitehouse.salaries.2011')

    @mock.patch.object(client.EnigmaAPI, '_request', autospec=True)
    def test_get_limits(self, mock_method):
        '''Does get_limits() call _request with resource='limits'?
        '''
        self.new_client.get_limits()
        mock_method.assert_called_with(
            self.new_client, datapath=None, resource='limits')

    def test_get_data_no_datapath_failure(self):
        '''Does get_data() raise a TypeError when no datapath is passed?
        '''
        with self.assertRaises(TypeError):
            self.new_client.get_data()

    @mock.patch.object(client.EnigmaAPI, '_request', autospec=True)
    def test_get_data(self, mock_method):
        '''Does get_data() call _request with resource='data'?
        '''
        self.new_client.get_data(datapath='us.gov.whitehouse.salaries.2011')
        mock_method.assert_called_with(
            self.new_client, datapath='us.gov.whitehouse.salaries.2011', resource='data')

    def test_get_metadata_no_datapath_failure(self):
        '''Does get_metadata() raise a TypeError when no datapath is passed?
        '''
        with self.assertRaises(TypeError):
            self.new_client.get_metadata()

    @mock.patch.object(client.EnigmaAPI, '_request', autospec=True)
    def test_get_metadata(self, mock_method):
        '''Does get_metadata() call _request with resource='metadata'?
        '''
        self.new_client.get_metadata(datapath='us.gov.whitehouse.salaries.2011')
        mock_method.assert_called_with(
            self.new_client, datapath='us.gov.whitehouse.salaries.2011', resource='meta')

    def test_map_metadata_data_type_python_data_type(self):
        '''Does _map_metadata_data_type() return a dictionary key corresponding
        to the Python data type of a column?
        '''
        metadata = self.new_client.get_metadata(
            datapath='us.gov.whitehouse.visitor-list')
        self.assertIsNotNone(
            metadata['result']['columns'][0].get('python_type'))

    def test_get_metadata_correct_python_data_type(self):
        '''Does get_metadata() return the correct Python data type for the type
        string returned?
        '''
        metadata = self.new_client.get_metadata(
            datapath='us.gov.whitehouse.salaries.2011')
        self.assertEquals(
            metadata['result']['columns'][2]['python_type'], decimal.Decimal)

    def test_get_stats_no_datapath_failure(self):
        '''Does get_stats() raise a TypeError when no datapath is passed?
        '''
        with self.assertRaises(TypeError):
            self.new_client.get_stats()

    @mock.patch.object(client.EnigmaAPI, '_request', autospec=True)
    def test_get_stats(self, mock_method):
        '''Does get_stats() call _request with resource='stats'?
        '''
        self.new_client.get_stats(datapath='us.gov.whitehouse.salaries.2011')
        mock_method.assert_called_with(
            self.new_client, datapath='us.gov.whitehouse.salaries.2011', resource='stats')

    def test_get_export_no_datapath_failure(self):
        '''Does get_export() raise a TypeError when no datapath is passed?
        '''
        with self.assertRaises(TypeError):
            self.new_client.get_export()

    @mock.patch.object(client.EnigmaAPI, '_request', autospec=True)
    def test_get_export(self, mock_method):
        '''Does get_export() call _request with resource='export'?
        '''
        self.new_client.get_export(datapath='us.gov.whitehouse.salaries.2011')
        mock_method.assert_called_with(
            self.new_client, datapath='us.gov.whitehouse.salaries.2011', resource='export')