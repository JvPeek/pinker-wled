import subprocess

wifi_networks = [
    {
        "bssid": "00:11:22:33:44:55",
        "essid": "NetworkName1",
        "inRange": True,
        "lastConnected": "2024-12-28 12:34:56",
        "gotIP": True,
        "actionExecuted": True,
    },
    {
        "bssid": "66:77:88:99:AA:BB",
        "essid": "NetworkName2",
        "inRange": False,
        "lastConnected": "2024-12-25 09:45:12",
        "gotIP": False,
        "actionExecuted": False,
    }

]

def scan_wifi():
    result = subprocess.run(["nmcli", "-t", "-f", "SSID,BSSID,SECURITY", "dev", "wifi"], capture_output=True, text=True)
    networks = result.stdout.strip().splitlines()
    parsed_networks = []
    for network in networks:
        # Handle the delimiter properly
        parts = network.split(":")
        
        if len(parts) >= 2:
            ssid = parts[0]
            bssid = ":".join(parts[1:7]).replace("\\:", ":")  # Ensure full BSSID is reconstructed
            encryption = parts[7]
            
            parsed_networks.append({"essid": ssid, "bssid": bssid, "encryption": encryption})
            
    return parsed_networks
    
def getWifiList():
    
    return wifi_networks
