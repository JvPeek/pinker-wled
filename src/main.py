import platform
import json
import time
from threading import Thread  # Import the threading module
from modules import FileHandler
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
        time.sleep(10)

def main():
    
      # Start the exampleFunction as a thread
    scanThread = Thread(target=scanThreadFunction)
    scanThread.start()

    # Join the thread if you want to wait for it to finish
    scanThread.join()

if __name__ == "__main__":
    main()

