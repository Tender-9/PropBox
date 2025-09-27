from math import nan
from ._module import Module

from datetime import datetime
import tempfile
import json
import os

class Parameters(Module):
    def __init__(self, file:str) -> None:
        super().__init__()
        self._file:             str = file
        self.time_period:      str = ""
        self.min_temperature: float = nan
        self.max_temperature: float = nan
        self.min_humidity:    float = nan
        self.max_humidity:    float = nan
        self._update()        
    
    def set_parameter(self, time_period:str, key:str, value) -> bool:
        try:
            with open(self._file, "r") as file:
                config = json.load(file)
        except(OSError, json.JSONDecodeError):
            return False 
        
        if time_period not in config: return False
        if key not in config[time_period]: return False
        
        config[time_period][key] = value

        directory = os.path.dirname(self._file)
        fd, temp_path = tempfile.mkstemp(dir=directory)

        try:
            with os.fdopen(fd, "w") as temp_file:
                json.dump(config, temp_file, indent=2)
            os.replace(temp_path, self._file)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
        self._update()    
        return True 

    
    def _update(self):
        with self._lock:
            try:
                with open(self._file, "r") as file:
                    config = json.load(file)
            except (OSError, json.JSONDecodeError):
                return

            now = datetime.now().time()

            day_start = datetime.strptime(config["day"]["start_time"], "%H:%M").time()
            night_start = datetime.strptime(config["night"]["start_time"], "%H:%M").time()

            if day_start <= now < night_start: self.time_period = "day"
            else: self.time_period = "night"

            self.min_temperature = config[self.time_period]["min_temperature"]
            self.max_temperature = config[self.time_period]["max_temperature"]
            self.min_humidity    = config[self.time_period]["min_humidity"]
            self.max_humidity    = config[self.time_period]["max_humidity"]

