import platform
import json
import time
from threading import Thread  # Import the threading module
from modules import FileHandler
from modules import wled


if platform.system() == 'Linux':
    from linux import wifi
elif platform.system() == 'Windows':
    from windows import wifi
elif platform.system() == 'MacOS':
    print ("MacOS is not supported. Maybe you can pay someone to implement it or whatever it is you people do")
    sys.exit()

def scanThreadFunction():
    while True:
        print(wifi.scan_wifi())
        time.sleep(1)


def connectorThreadFunction():
    while True:
        wifi.connect_wifi("WLED-AP-Penis","EA:9F:6D:93:C1:2F", "wled1234")
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

