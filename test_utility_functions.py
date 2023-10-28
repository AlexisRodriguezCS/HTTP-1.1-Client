# File: test_utility_functions.py
# Description:
# This is a test file for the utility functions defined in utility_functions.py.

import unittest
from utility_functions import parse_response_headers, basic_auth, is_valid_url, retry_request

class TestUtilityFunctions(unittest.TestCase):

    def test_parse_response_headers(self):
        response = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 123\r\n"
        headers = parse_response_headers(response)
        self.assertEqual(headers, {'Content-Type': 'text/html', 'Content-Length': '123'})

    def test_basic_auth(self):
        username = "user"
        password = "password"
        auth_header = basic_auth(username, password)
        expected_auth_header = "Basic dXNlcjpwYXNzd29yZA=="
        self.assertEqual(auth_header, expected_auth_header)

    def test_is_valid_url(self):
        valid_url = "http://example.com"
        invalid_url = "example.com"
        self.assertTrue(is_valid_url(valid_url))
        self.assertFalse(is_valid_url(invalid_url))

    def test_retry_request(self):
        # Test a successful request
        url = "http://example.com"
        max_retries = 3
        timeout = 1
        backoff_factor = 1
        response = retry_request(url, max_retries, timeout, backoff_factor)
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()
