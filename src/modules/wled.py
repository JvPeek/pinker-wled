import urllib.request
from urllib.error import HTTPError, URLError
import config
import socket
import logging

def make_request():

    url = config.get_url()
    
    print (f"accessing {url}")
    try:
        contents = urllib.request.urlopen(url, timeout=10).read().decode('utf-8')
        logging.info('Access successful.')
    except (urllib.error.URLError, socket.timeout) as e:
        logging.warning(f"Request failed: {e}")
        contents = None  # Handle as needed, e.g., set contents to None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        contents = None

    
    print (contents)
    return

