import time
import subprocess
import dataclasses
import os

from dataclasses import dataclass
from pprint import pprint
from winwifi import WinWiFi, WiFiAp

@dataclass
class Network:
    essid: str
    bssid: str | None = None
    encryption: bool | None = None


def scan_wifi():

    try:
        networks: list[{str, str, str}] = []
        
        WinWiFi.scan()
        
        result = subprocess.run(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            capture_output=True,
            text=True,
            check=True,
        )
        output = result.stdout.split("\n")
        # pprint(output)

        if " " not in output[0]:
            return

        if "Schnittstellenname : " not in output[1]:
            return

        # network_adapter_name = output[1].split(' ')[2].strip()
        # essid_count = output[2].split(' ')[2].strip()

        network: Network

        for line in output[4:]:
            if "SSID" in line and "BSSID" not in line:
                essid = line.split(" ")[3:]
                network = Network(" ".join(essid))
            if "Authentifizierung" in line:
                enc = line.split(" ")[-1]
                if enc == "Offen":
                    network.encryption = False
                    continue
                network.encryption = True
            if "BSSID" in line:
                bssid = line.split(" ")[-1]
                network.bssid = bssid
                if network.essid != "":
                    networks.append(dataclasses.asdict(network))
        # pprint(networks)
        return networks
    except subprocess.CalledProcessError as e:
        print("Error occurred while scanning WiFi networks:", e)

def connect_wifi(essid, bssid, password=None):
    
    config_string_open = f"<?xml version=\"1.0\"?>\
        <WLANProfile xmlns=\"http://www.microsoft.com/networking/WLAN/profile/v1\">\
            <name>tmp</name>\
            <SSIDConfig>\
                <SSID>\
                    <name>{essid}</name>\
                </SSID>\
            </SSIDConfig>\
            <connectionType>ESS</connectionType>\
            <connectionMode>manual</connectionMode>\
            <MSM>\
                <security>\
                    <authEncryption>\
                        <authentication>open</authentication>\
                        <encryption>none</encryption>\
                        <useOneX>false</useOneX>\
                    </authEncryption>\
                </security>\
            </MSM>\
            <MacRandomization xmlns=\"http://www.microsoft.com/networking/WLAN/profile/v3\">\
                <enableRandomization>false</enableRandomization>\
            </MacRandomization>\
        </WLANProfile>"
    
    config_string_wap2 = f"<?xml version=\"1.0\"?>\
        <WLANProfile xmlns=\"http://www.microsoft.com/networking/WLAN/profile/v1\">\
            <name>tmp</name>\
            <SSIDConfig>\
                <SSID>\
                    <name>{essid}</name>\
                </SSID>\
            </SSIDConfig>\
            <connectionType>ESS</connectionType>\
            <connectionMode>auto</connectionMode>\
            <MSM>\
                <security>\
                    <authEncryption>\
                        <authentication>WPA2PSK</authentication>\
                        <encryption>AES</encryption>\
                        <useOneX>false</useOneX>\
                    </authEncryption>\
                    <sharedKey>\
                        <keyType>passPhrase</keyType>\
                        <protected>false</protected>\
                        <keyMaterial>wled1234</keyMaterial>\
                    </sharedKey>\
                </security>\
            </MSM>\
            <MacRandomization xmlns=\"http://www.microsoft.com/networking/WLAN/profile/v3\">\
                <enableRandomization>false</enableRandomization>\
            </MacRandomization>\
        </WLANProfile>"

    file = open("tmp.xml", "w")
    if password:
        file.write(config_string_wap2)
    else:
        file.write(config_string_open)
    file.close()
        
    try:
        result = subprocess.run(
                ["netsh", "wlan", "add", "profile", "filename=tmp.xml"],
                capture_output=True,
                text=True,
                check=True,
            )
        print(result.stdout)        
    except subprocess.CalledProcessError as e:
        print("Error occurred while creating profile:", e)
    
    os.remove("tmp.xml")
    
    try:
        result = subprocess.run(
                ["netsh", "wlan", "connect", "name=tmp"],
                capture_output=True,
                text=True,
                check=True,
            )        
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error occurred while connecting to wifi:", e)
    
    # try:
    #     # netsh wlan delete profile name=tmp
    #     result = subprocess.run(
    #             ["netsh", "wlan", "delete", "profile", "name=tmp"],
    #             capture_output=True,
    #             text=True,
    #             check=True,
    #         )        
    #     print(result.stdout)
    # except subprocess.CalledProcessError as e:
    #     print("Error occurred while deleting profile:", e)
    

if __name__ == "__main__":
    # scan_wifi()
    connect_wifi("38C3-open", "", False)
