import platform
import json
import time
import sys
import queue
from threading import Thread  # Import the threading module
from modules import FileHandler
from modules import wled
from pprint import pprint

if platform.system() == 'Linux':
    from linux import wifi
elif platform.system() == 'Windows':
    from windows import wifi
elif platform.system() == 'MacOS':
    print ("MacOS is not supported. Maybe you can pay someone to implement it or whatever it is you people do")
    sys.exit()

networks_queue = queue.Queue()

def scanThreadFunction():
    while True:
        if networks_queue.qsize() == 0:
            networks : list[str, str, str] = wifi.scan_wifi()
            if len(networks) > 0:
                for net in networks:
                    ssid : str = net['essid']
                    if "wled" in ssid.lower() or "l3on" in ssid.lower():
                        networks_queue.put(net)
                print(networks_queue.queue)            
        time.sleep(1)


def connectorThreadFunction():
    while True:
        if networks_queue.qsize() == 0:
            time.sleep(1)
            continue
        
        net = networks_queue.get()
        print(f"connect to: {net}")
        wifi.connect_wifi(net['essid'],net['bssid'], net['encryption'])
        wled.make_request()
        time.sleep(1)

def main():
      
    scanThread = Thread(target=scanThreadFunction)
    scanThread.daemon = True
    scanThread.start()


    connectorThread = Thread(target=connectorThreadFunction)
    connectorThread.daemon = True
    connectorThread.start()
    while True:

        continue

if __name__ == "__main__":
    main()

