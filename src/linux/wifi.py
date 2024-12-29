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
def connect_wifi(essid, bssid, password=None):
    subprocess.run(["nmcli", "con", "delete", essid ], capture_output=True, text=True)

    command = ["nmcli", "dev", "wifi", "connect", essid, "bssid", bssid]
    if password:
        command.extend(["password", password])

    print (" ".join(command))
    result = subprocess.run(command, capture_output=True, text=True)
    print (result)
    return result.returncode == 0


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
            
            if ("WLED" in ssid):
                parsed_networks.append({"essid": ssid, "bssid": bssid, "encryption": encryption != "OWE-TM"})
            
    return parsed_networks
    
def getWifiList():
    
    return wifi_networks
