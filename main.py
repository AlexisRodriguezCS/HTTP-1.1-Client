# File: main.py
# Description:
# This script serves as the entry point for the project, allowing users to retrieve the body of a document
# from a specified URL using HTTP/HTTPS protocols. It also demonstrates the use of utility functions
# for making HTTP requests.

# Import necessary modules
import sys
from http_utils import retrieve_url, rate_limited_request

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]

    # Retrieve the URL with rate limiting (e.g., 10 requests per minute)
    result = rate_limited_request(url)

    if result:
        sys.stdout.buffer.write(result)
    else:
        print("Failed to retrieve the URL.")
