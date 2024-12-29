import platform
if platform.system() == 'Linux':
    from linux import wifi
elif platform.system() == 'Windows':
    from windows import wifi
elif platform.system() == 'MacOS':
    print ("MacOS is not supported. Maybe you can pay someone to implement it or whatever it is you people do")
    exit()

def main():
    
    print (wifi.scan_wifi())

if __name__ == "__main__":
    main()

