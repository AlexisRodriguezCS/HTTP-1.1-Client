# File: utility_functions.py
# Description:
# This module contains various utility functions for parsing response headers, implementing basic authentication,
# validating URLs, and retrying HTTP requests.
from http_utils import retrieve_url

# Other utility functions

def parse_response_headers(response):
    """
    Parse and extract HTTP response headers.

    Args:
        response (bytes): The HTTP response from the server.

    Returns:
        dict: A dictionary containing the parsed response headers.
    """
    headers = {}
    lines = response.split(b"\r\n")
    for line in lines[1:]:  # Skip the first line (status line)
        if not line:
            break  # Empty line marks the end of headers
        key, value = line.split(b": ", 1)
        headers[key.decode()] = value.decode()
    return headers

def basic_auth(username, password):
    """
    Generate a Basic Authentication header.

    Args:
        username (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        str: The Basic Authentication header as a string.
    """
    import base64
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded_credentials}"

def is_valid_url(url):
    """
    Check if a URL is valid.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    from urllib.parse import urlparse
    result = urlparse(url)
    return all([result.scheme, result.netloc])

def retry_request(url, max_retries=3, timeout=10, backoff_factor=2):
    """
    Retry an HTTP request with a backoff mechanism.

    Args:
        url (str): The URL to request.
        max_retries (int): The maximum number of retry attempts.
        timeout (int): The timeout for the HTTP request in seconds.
        backoff_factor (int): The factor by which to back off between retries.

    Returns:
        bytes or None: The body of the document as bytes, or None if retrieval fails.
    """
    import time

    for attempt in range(max_retries + 1):
        if attempt > 0:
            delay = (2 ** (attempt - 1)) * backoff_factor
            time.sleep(delay)
        response = retrieve_url(url, timeout)
        if response:
            return response
    return None
