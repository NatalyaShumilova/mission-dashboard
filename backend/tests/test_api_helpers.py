import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from flask import Flask

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.utils.api_helpers import (
    api_response, api_error_response, 
    validate_json_request
)


class TestAPIHelpers(unittest.TestCase):
    """Unit tests for API helper functions"""
    
    def setUp(self):
        """Set up test Flask app for request context"""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
    
    def test_api_response_success(self):
        """Test successful API response formatting"""
        with self.app.test_request_context():
            with patch('app.utils.api_helpers.request') as mock_request:
                mock_request.request_id = 'test123'
                
                with patch('app.utils.api_helpers.datetime') as mock_datetime:
                    mock_datetime.utcnow.return_value.isoformat.return_value = '2023-01-01T12:00:00'
                    
                    response = api_response(data={'test': 'data'}, message='Success')
                    
                    self.assertEqual(response.status_code, 200)
                    response_data = response.get_json()
                    
                    self.assertTrue(response_data['success'])
                    self.assertEqual(response_data['data'], {'test': 'data'})
                    self.assertEqual(response_data['message'], 'Success')
                    self.assertEqual(response_data['request_id'], 'test123')
                    self.assertEqual(response_data['timestamp'], '2023-01-01T12:00:00Z')
    
    def test_api_error_response(self):
        """Test error response formatting"""
        with self.app.test_request_context():
            with patch('app.utils.api_helpers.request') as mock_request:
                mock_request.request_id = 'test123'
                
                with patch('app.utils.api_helpers.datetime') as mock_datetime:
                    mock_datetime.utcnow.return_value.isoformat.return_value = '2023-01-01T12:00:00'
                    
                    response = api_error_response('Test error', status_code=400, details={'field': 'invalid'})
                    
                    self.assertEqual(response.status_code, 400)
                    response_data = response.get_json()
                    
                    self.assertFalse(response_data['success'])
                    self.assertEqual(response_data['error']['message'], 'Test error')
                    self.assertEqual(response_data['error']['code'], 400)
                    self.assertEqual(response_data['error']['details'], {'field': 'invalid'})
                    self.assertEqual(response_data['request_id'], 'test123')
    
    
    def test_validate_json_request_success(self):
        """Test successful JSON request validation"""
        with self.app.test_request_context():
            with patch('app.utils.api_helpers.request') as mock_request:
                mock_request.is_json = True
                # Mock get_json as a callable that returns the data
                mock_request.get_json = MagicMock(return_value={
                    'name': 'Test Mission',
                    'description': 'Test description'
                })
                
                result = validate_json_request(
                    required_fields=['name'],
                    optional_fields=['description']
                )
                
                expected = {
                    'name': 'Test Mission',
                    'description': 'Test description'
                }
                
                self.assertEqual(result, expected)
    
    def test_validate_json_request_missing_required_fields(self):
        """Test validation fails when required fields are missing"""
        with self.app.test_request_context():
            with patch('app.utils.api_helpers.request') as mock_request:
                mock_request.is_json = True
                mock_request.get_json = MagicMock(return_value={'description': 'Test'})
                
                with self.assertRaises(ValueError) as context:
                    validate_json_request(required_fields=['name', 'type'])
                
                self.assertIn('Missing required fields: name, type', str(context.exception))
    
    def test_validate_json_request_unexpected_fields(self):
        """Test validation fails when unexpected fields are present"""
        with self.app.test_request_context():
            with patch('app.utils.api_helpers.request') as mock_request:
                mock_request.is_json = True
                mock_request.get_json = MagicMock(return_value={
                    'name': 'Test',
                    'unexpected_field': 'value'
                })
                
                with self.assertRaises(ValueError) as context:
                    validate_json_request(required_fields=['name'])
                
                self.assertIn('Unexpected fields: unexpected_field', str(context.exception))


if __name__ == '__main__':
    unittest.main(verbosity=2)
