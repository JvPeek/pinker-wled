import urllib.request
from urllib.error import HTTPError, URLError
import config
import socket
import logging
import time

def make_request():

    url = config.get_url()
    success = False
    count = 0
    print (f"accessing {url}")
    while success == False and count < 5:
        try:
            contents = urllib.request.urlopen(url, timeout=10).read().decode('utf-8')
            # logging.info('Access successful.')
            success = True
        except (urllib.error.URLError, socket.timeout) as e:
            # logging.warning(f"Request failed: {e}")
            contents = None  # Handle as needed, e.g., set contents to None
            count = count + 1
        except Exception as e:
            # logging.error(f"An unexpected error occurred: {e}")
            contents = None
            count = count + 1
        time.sleep(2)
            

    if contents is not None:
        print (contents)
    return

