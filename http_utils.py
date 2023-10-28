# File: http_utils.py
# Description:
# This module contains utility functions for making HTTP requests, including retrieving the body of a
# document from a given URL, handling rate limiting, and retrieving content from HTTPS URLs.

import socket
import ssl
from urllib.parse import urlparse

# Function to retrieve the body of the document at the given URL
def retrieve_url(url, timeout=10):
    """
    Retrieve the body of the document at the given URL.

    Args:
        url (str): The URL of the document.
        timeout (int): The timeout for the HTTP request in seconds.

    Returns:
        bytes or None: The body of the document as bytes, or None if retrieval fails.
    """
    # Parse the URL to get protocol, host, path, and port information
    parsed_url = urlparse(url)
    protocol = parsed_url.scheme
    host = parsed_url.hostname
    path = parsed_url.path or "/"
    port = parsed_url.port or (80 if protocol == "http" else 443 if protocol == "https" else None)

    if not host or not port:
        return None

    # Form the GET request
    get = get_request_with_user_agent(host, port, path)

    response = b""  # Initialize response as bytes

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)  # Set a timeout for socket operations
            sock.connect((host, port))  # Connect to host and port
            sock.sendall(get.encode())  # Send the GET request
            while True:
                current_data = sock.recv(1024)  # Receive data in chunks of 1024 bytes
                response += current_data  # Append received data to response
                if not current_data:  # If no more data is received, break the loop
                    break
    except socket.error as e:
        return None  # Return None on socket error

    # Check if we received a "200 OK" response from the server
    if is_successful_response(response, 200):
        # Find the starting point of the body of the document in the response
        index = response.find(b"\r\n\r\n") + 4
        return response[index:]  # Return the body of the document
    return None  # Return None if response is not "200 OK"

# Function to limit the rate of HTTP requests
def rate_limited_request(url, max_requests_per_minute=10):
    """
    Limit the rate of HTTP requests.

    Args:
        url (str): The URL to request.
        max_requests_per_minute (int): Maximum number of requests allowed per minute.

    Returns:
        bytes or None: The body of the document as bytes, or None if retrieval fails.
    """
    # Implement rate limiting logic here
    return retrieve_url(url)

# Function to retrieve content from HTTPS URLs
def retrieve_https_url(url, timeout=10):
    """
    Retrieve the body of the document from an HTTPS URL.

    Args:
        url (str): The URL of the document.
        timeout (int): The timeout for the HTTP request in seconds.

    Returns:
        bytes or None: The body of the document as bytes, or None if retrieval fails.
    """
    # Parse the URL and set the default HTTPS port (443)
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    path = parsed_url.path or "/"
    port = parsed_url.port or 443

    if not host:
        return None

    # Form the GET request with a User-Agent header
    get = get_request_with_user_agent(host, port, path, user_agent="MyUserAgent")

    response = b""  # Initialize response as bytes

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)  # Set a timeout for socket operations
            context = ssl.create_default_context()
            with context.wrap_socket(sock, server_hostname=host) as secure_sock:
                secure_sock.connect((host, port))  # Connect securely to host and port
                secure_sock.sendall(get.encode())  # Send the GET request
                while True:
                    current_data = secure_sock.recv(1024)  # Receive data in chunks of 1024 bytes
                    response += current_data  # Append received data to response
                    if not current_data:  # If no more data is received, break the loop
                        break
    except (socket.error, ssl.SSLError) as e:
        return None  # Return None on socket/SSL error

    # Check if we received a "200 OK" response from the server
    if is_successful_response(response, 200):
        # Find the starting point of the body of the document in the response
        index = response.find(b"\r\n\r\n") + 4
        return response[index:]  # Return the body of the document
    return None  # Return None if response is not "200 OK"

def get_request_with_user_agent(host, port, path, user_agent="MyUserAgent"):
    """
    Form a GET request with a User-Agent header.

    Args:
        host (str): The host of the request.
        port (int): The port for the request.
        path (str): The path of the request.
        user_agent (str): The User-Agent header value.

    Returns:
        str: The formed GET request as a string.
    """
    get_rq = f"GET {path} HTTP/1.1\r\n"
    host_rq = f"Host: {host}:{port}\r\n"
    user_agent_header = f"User-Agent: {user_agent}\r\n"
    conn = "Connection: close\r\n\r\n"
    return get_rq + host_rq + user_agent_header + conn  # Concatenate all parts to form the request

def is_successful_response(response, expected_code=200):
    """
    Check if the response has a successful HTTP status code.

    Args:
        response (bytes): The HTTP response from the server.
        expected_code (int): The expected HTTP status code.

    Returns:
        bool: True if the response has the expected status code, False otherwise.
    """
    status_code = response.split(b' ')[1]
    return status_code == str(expected_code).encode()
