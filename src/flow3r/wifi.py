import network

def scan_wifi():
    wlan = network.WLAN()
    wlan.active(True)
    nets = wlan.scan()

    return [{"essid": net[0],
             "bssid": net[1],
             "encryption": net[4] != 0}
            for net in nets]
