from pynigma import client
import decimal
import unittest
import os


class TestClient(unittest.TestCase):

    def setUp(self):
        self.new_client = client.EnigmaAPI(os.environ['ENIGMA_API_KEY'])

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

    def test_request_success(self):
        '''Does _request() return decoded JSON when the request is valid?
        '''
        self.assertIsInstance(self.new_client.get_data(
            datapath='us.gov.whitehouse.salaries.2011'), dict)

    def test_request_success_keys(self):
        '''Does _request() return decoded JSON with the expected keys when the
        request is valid?
        '''
        self.assertEquals(self.new_client.get_data(
            datapath='us.gov.whitehouse.salaries.2011').keys(), ['info', 'datapath', 'success', 'result'])

    def test_get_limits_datapath_failure(self):
        '''Does get_limits() raise a TypeError when a datapath is passed?
        '''
        with self.assertRaises(TypeError):
            self.new_client.get_limits(
                datapath='us.gov.whitehouse.salaries.2011')

    def test_get_data_no_datapath_failure(self):
        '''Does get_data() raise a TypeError when no datapath is passed?
        '''
        with self.assertRaises(TypeError):
            self.new_client.get_data()

    def test_get_metadata_no_datapath_failure(self):
        '''Does get_metadata() raise a TypeError when no datapath is passed?
        '''
        with self.assertRaises(TypeError):
            self.new_client.get_metadata()

    def test_get_metadata_python_data_type(self):
        '''Does get_metadata() return a dictionary key corresponding to the
        Python data type of a column?
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

    def test_get_export_no_datapath_failure(self):
        '''Does get_export() raise a TypeError when no datapath is passed?
        '''
        with self.assertRaises(TypeError):
            self.new_client.get_export()
