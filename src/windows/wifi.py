import time
import subprocess
import dataclasses

from dataclasses import dataclass
from pprint import pprint

@dataclass
class Network:
    essid : str
    bssid : str | None = None
    encryption : bool | None = None
    
networks : list[{str, str, str}]= []


def scan_wifi():

    try:
    
        result = subprocess.run(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            capture_output=True,
            text=True,
            check=True,
        )
        output = result.stdout.split("\n")
        # pprint(output)
        
        if ' ' not in output[0]:
            return
        
        if 'Schnittstellenname : ' not in output[1]:
            return
        
        # network_adapter_name = output[1].split(' ')[2].strip()
        # essid_count = output[2].split(' ')[2].strip()
        
        network : Network
        
        for line in output[4:]:
            if 'SSID' in line and 'BSSID' not in line:
                essid = line.split(' ')[3:]
                network = Network(' '.join(essid))
            if 'Authentifizierung' in line:
                enc = line.split(' ')[-1]
                if enc == 'Offen': 
                    network.encryption = False
                    continue
                network.encryption = True
            if 'BSSID' in line:
                bssid = line.split(' ')[-1]
                network.bssid = bssid
                if network.essid != '':
                    networks.append(dataclasses.asdict(network))
        # pprint(networks)
        return networks
    except subprocess.CalledProcessError as e:
        print("Error occurred while scanning WiFi networks:", e)


if __name__ == "__main__":
    scan_wifi()
