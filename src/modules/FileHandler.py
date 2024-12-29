from typing import Any
from pprint import pprint
from dataclasses import dataclass
from json import JSONDecodeError

import random
import json
import traceback
import os
import sys
import dataclasses
import datetime

# "bssid": "00:11:22:33:44:55",
# "essid": "NetworkName1",
# "inRange": True,
# "lastConnected": "2024-12-28 12:34:56",
# "gotIP": True,
# "actionExecuted": True,

@dataclass_json
@dataclass
class WifiNetworks:
    bssid: str = ""
    essid: str = ""
    inRange: bool = False
    lastConnected: datetime = datetime.MINYEAR #should work?
    gotIP: bool = False
    actionExecuted: bool = False


class FileHandler:
    def __init__(self, path : str) -> None:
        self.path : str = path
        
        try:
            file = open(path, "r")
            self.networks : list[WifiNetworks] = WifiNetworks.from_dict(json.load(file))

        except FileNotFoundError as e:
            self.app.logger.error(f"FILE file not found! ❌")
            self.app.logger.info(f"FILE create file! ✏️")
            file = open(file, "x")
            json.dump(dataclasses.asdict(self.networks), file, sort_keys=True, indent=2)
            file.close()

            file = open(file, "r")
            self.config = WifiNetworks(**json.load(file))
        except JSONDecodeError as e:
            self.app.logger.error(
                f"FILE Json decoding error! Please check file and restart. If config is empty delete config/config.json! EXIT ❌"
            )
            sys.exit("FILE DECODING ERROR 💣💥")
        except:
            self.app.logger.error(f"FILE error see stack trace ❌:\n")
            traceback.print_exc()

    def getNetworks(self) -> list[WifiNetworks]:
        return self.networks