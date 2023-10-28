# File: test_http_utils.py
# Description:
# This is a test file for the utility functions defined in http_utils.py.

import unittest
from http_utils import retrieve_url, rate_limited_request, retrieve_https_url, is_successful_response

class TestHTTPUtils(unittest.TestCase):

    def test_retrieve_url(self):
        # Test a successful request
        url = "http://example.com"
        timeout = 1
        response = retrieve_url(url, timeout)
        self.assertIsNotNone(response)

    def test_rate_limited_request(self):
        # Test a rate-limited request
        url = "http://example.com"
        max_requests_per_minute = 1
        response = rate_limited_request(url, max_requests_per_minute)
        self.assertIsNotNone(response)

    def test_retrieve_https_url(self):
        # Test a successful HTTPS request
        url = "https://example.com"
        timeout = 1
        response = retrieve_https_url(url, timeout)
        self.assertIsNotNone(response)

    def test_is_successful_response(self):
        # Test a successful response with the default status code (200)
        response = b"HTTP/1.1 200 OK\r\nContent-Length: 123\r\n"
        self.assertTrue(is_successful_response(response))

        # Test a successful response with a custom status code (201)
        response = b"HTTP/1.1 201 Created\r\nContent-Length: 123\r\n"
        self.assertTrue(is_successful_response(response, 201))

        # Test an unsuccessful response with a status code (404)
        response = b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n"
        self.assertFalse(is_successful_response(response, 200))

if __name__ == '__main__':
    unittest.main()
