import logging
import socket
import sys


def retrieve_url(url):
    """
    return bytes of the body of the document at url
    """
    # Get the protocol (http or https)
    index_of_protocol = url.find(":")
    protocol = url[0:index_of_protocol]
    host = ""
    path = ""
    port = 0

    # Get String without protocol
    # 'http://www.example.com' -> 'www.example.com' or
    # 'http://wonderousshinyinnerspell.neverssl.com/online'
    # -> 'wonderousshinyinnerspell.neverssl.com/online'
    index_of_protocol = url.find("//")
    temp_string = url[index_of_protocol + 2:len(url)]
    has_path = False

    # Check for '/'
    if temp_string.find("/") != -1:
        # Get string up to path
        has_path = True
        temp_string = temp_string[0:temp_string.find("/")]
    # Check for Port
    has_port = False
    if temp_string.find(':') != -1:
        # Get port
        has_port = True
        index = temp_string.find(':')
        port = temp_string[index + 1: len(temp_string)]

    # Get the Host
    if has_port is True:
        index = temp_string.find(":")
        host = temp_string[0: index]
    else:
        host = temp_string

    # Check if there is a port, if not set default depending on protocol
    if has_port is False:
        if protocol == "http":
            port = "80"
        elif protocol == "https":
            port = "443"
    # Check if there is a path, if not set it to "/"
    if has_path is False:
        path = "/"
    elif has_path is True:
        temp = url[index_of_protocol + 2:len(url)]
        index = temp.find('/')
        path = temp[index + 1: len(url)]
        # Check if path was just '/'
        if len(path) == 0:
            path = "/"

    # call formGetRequest and get GET request
    get = get_request(host, port, path)
    response = b""
    # create socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, int(port)))
            sock.sendall(get.encode())
            response = sock.recv(1024)
            while True:
                current_data = sock.recv(1024)
                response = response + current_data
                if not current_data:
                    break
    except socket.gaierror:
        return None

    # Check if we received a "200" OK response from the server
    if response.find(b'200 OK') != -1:
        # Look for starting point of body of the document at url
        index = response.find(b"\r\n\r\n") + 4
        return response[index:]
    return None


def get_request(host, port, path):
    """Form the get request."""
    # Get /Path HTTP/1.1
    # Host: www.example.com:80
    # Connection: close
    # Blank line
    request = ""
    if path == "/":
        # Get / HTTP/1.1
        get_rq = "GET / HTTP/1.1\r\n"
        host_rq = "Host: " + host + ":" + port + "\r\n"
        conn = "Connection: close\r\n\r\n"
        request = get_rq + host_rq + conn
    else:
        # Get /path HTTP/1.1
        get_rq = "GET /" + path + " HTTP/1.1\r\n"
        host_rq = "Host: " + host + ":" + port + "\r\n"
        conn = "Connection: close\r\n\r\n"
        request = get_rq + host_rq + conn
    return request

# if __name__ == "__main__":
#     sys.stdout.buffer.write(retrieve_url(sys.argv[1]))
# pylint: disable=no-member