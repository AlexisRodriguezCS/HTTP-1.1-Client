"""
File: main.py
Author: Alexis Rodriguez

Description:
This script defines functions to retrieve the body of a document from a given URL using HTTP/HTTPS protocol.
It forms a GET request and establishes a socket connection to retrieve the response.

Usage:
python main.py <url>
"""

# Import necessary modules
import logging
import socket
import sys

# Function to retrieve the body of the document at the given URL
def retrieve_url(url):
    """
    Retrieve the body of the document at the given URL.
    
    Args:
        url (str): The URL of the document.
    
    Returns:
        bytes or None: The body of the document as bytes, or None if retrieval fails.
    """
    # Extract protocol, host, path, and port information from the URL
    index_of_protocol = url.find(":")  # Find the index of protocol separator ":"
    protocol = url[0:index_of_protocol]  # Extract the protocol
    host = ""  # Initialize host as an empty string
    path = ""  # Initialize path as an empty string
    port = 0   # Initialize port as 0
    
    index_of_protocol = url.find("//")  # Find the index of "//" after protocol
    temp_string = url[index_of_protocol + 2:len(url)]  # Extract the string after "//"
    has_path = False  # Initialize has_path as False
    
    if temp_string.find("/") != -1:
        has_path = True  # Set has_path to True if '/' is found in temp_string
        temp_string = temp_string[0:temp_string.find("/")]  # Extract host part of URL
    
    has_port = False  # Initialize has_port as False
    if temp_string.find(':') != -1:
        has_port = True  # Set has_port to True if ':' is found in temp_string
        index = temp_string.find(':')  # Find the index of port separator ":"
        port = temp_string[index + 1: len(temp_string)]  # Extract port
    
    if has_port is True:
        index = temp_string.find(":")  # Find the index of port separator ":"
        host = temp_string[0: index]   # Extract host
    else:
        host = temp_string  # If no port, host is the entire temp_string
    
    if has_port is False:
        if protocol == "http":
            port = "80"  # Set default port 80 for HTTP
        elif protocol == "https":
            port = "443"  # Set default port 443 for HTTPS
    
    if has_path is False:
        path = "/"  # Set default path as "/"
    elif has_path is True:
        temp = url[index_of_protocol + 2:len(url)]  # Extract the string after "//"
        index = temp.find('/')  # Find the index of path separator "/"
        path = temp[index + 1: len(url)]  # Extract path
        if len(path) == 0:
            path = "/"  # If path is empty, set it to "/"
    
    # Form the GET request
    get = get_request(host, port, path)
    
    response = b""  # Initialize response as bytes
    # Create a socket and retrieve the response
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, int(port)))  # Connect to host and port
            sock.sendall(get.encode())  # Send the GET request
            response = sock.recv(1024)  # Receive initial response
            while True:
                current_data = sock.recv(1024)  # Receive data in chunks of 1024 bytes
                response = response + current_data  # Append received data to response
                if not current_data:  # If no more data is received, break the loop
                    break
    except socket.gaierror:
        return None  # Return None if there's a socket error
    
    # Check if we received a "200 OK" response from the server
    if response.find(b'200 OK') != -1:
        # Find the starting point of the body of the document in the response
        index = response.find(b"\r\n\r\n") + 4
        return response[index:]  # Return the body of the document
    return None  # Return None if response is not "200 OK"

# Function to form a GET request
def get_request(host, port, path):
    """
    Form a GET request for the specified host, port, and path.
    
    Args:
        host (str): The host of the request.
        port (str): The port for the request.
        path (str): The path of the request.
    
    Returns:
        str: The formed GET request as a string.
    """
    if path == "/":
        get_rq = "GET / HTTP/1.1\r\n"  # Form GET request with root path
    else:
        get_rq = "GET /" + path + " HTTP/1.1\r\n"  # Form GET request with specified path
    
    host_rq = "Host: " + host + ":" + port + "\r\n"  # Form host header
    conn = "Connection: close\r\n\r\n"  # Close connection after response
    
    request = get_rq + host_rq + conn  # Concatenate all parts to form the request
    return request  # Return the formed GET request as a string

# Entry point of the script
if __name__ == "__main__":
    Retrieve and write the URL content to standard output buffer
    sys.stdout.buffer.write(retrieve_url(sys.argv[1]))
