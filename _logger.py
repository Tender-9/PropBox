from ._parameters import Parameters
from ._module     import Module
from ._sensor     import Sensor
from ._fan        import Fan

from datetime import datetime
import sqlite3

class Logger(Module):
    def __init__(self, parameters:Parameters, sensor:Sensor, fan:Fan, terminal=True ,file="") -> None:
        super().__init__()
        self._parameters: Parameters = parameters
        self._sensor:     Sensor     = sensor
        self._fan:        Fan        = fan
        self._terminal:   bool       = terminal
        self._file:       str        = file
        self._data:       dict       = {}

        if self._file:
            conn = sqlite3.connect(self._file)
            cursor = conn.cursor() 
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS sensor_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    date TEXT,
                    time TEXT,
                    temperature REAL,
                    humidity REAL,
                    fan_pwm INTEGER,
                    fan_rpm INTEGER,
                    time_period TEXT,
                    min_temperature REAL,
                    max_temperature REAL,
                    min_humidity REAL,
                    max_humidity REAL)
                '''
            )
            conn.commit()
            conn.close()


    def _update(self):
        now = datetime.now() 
        self._data = {
            "date"            : now.strftime("%y:%m:%d"),
            "time"            : now.strftime("%H:%M:%S"), 
            "temperature"     : self._sensor.temperature,
            "humidity"        : self._sensor.humidity,
            "fan_pwm"         : self._fan.pwm,
            "fan_rpm"         : self._fan.rpm,
            "time_period"     : self._parameters.time_period,
            "min_temperature" : self._parameters.min_temperature,
            "max_temperature" : self._parameters.max_temperature,
            "min_humidity"    : self._parameters.min_humidity,
            "max_humidity"    : self._parameters.max_humidity 
        }
        self._print()
        self._db_print() 


    def _print(self):
        if self._terminal == False: return
        fields = [
            f"{self._data["date"]}",
            f"{self._data["time"]}",
            f"\033[94m{self._data["temperature"]:.1f}°C\033[0m",
            f"\033[94m{self._data["humidity"]:.1f}%\033[0m",
            f"{self._data["fan_pwm"]}%",
            f"{self._data["fan_rpm"]:.0f} RPM",
            f"{self._data["time_period"]}",
            f"{self._data["min_temperature"]:.1f}°C",
            f"{self._data["max_temperature"]:.1f}°C",
            f"{self._data["min_humidity"]:.1f}%",
            f"{self._data["max_humidity"]:.1f}%"
        ] 
        print("\033[90m | \033[0m".join(fields))

    
    def _db_print(self):
        if self._file == "": return
        with sqlite3.connect(self._file) as connection:
            cursor = connection.cursor()
            cursor.execute(
                '''
                INSERT INTO sensor_logs (date, time, temperature, humidity, fan_pwm, 
                                         fan_rpm, time_period, min_temperature, 
                                         max_temperature, min_humidity, max_humidity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', 
                tuple(self._data.values())
            )    
            connection.commit()
