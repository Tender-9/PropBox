from propbox._module import Module
from propbox.inputs import Sensor, Fan, Parameters

from collections import deque
from datetime import datetime

class DataManager(Module):
    def __init__(self, parameters:Parameters, sensor:Sensor, fan:Fan, output=True) -> None:
        super().__init__()
        self._parameters: Parameters = parameters
        self._sensor:     Sensor     = sensor
        self._fan:        Fan        = fan
        self._output:     bool       = output
        self.data = deque(maxlen=3600)


    def _update(self):
        with self._lock:
            now = datetime.now()            
        
            data_point = {
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
                "max_humidity"    : self._parameters.max_humidity,
            }
        
            self.data.append(data_point)

            if not self._output: return

            fields = [
                f"{data_point['date']}",
                f"{data_point['time']}",
                f"\033[94m{data_point['temperature']:.1f}°C\033[0m",
                f"\033[94m{data_point['humidity']:.1f}%\033[0m",
                f"{data_point['fan_pwm']}%",
                f"{data_point['fan_rpm']:.0f} RPM",
                f"{data_point['time_period']}",
                f"{data_point['min_temperature']:.1f}°C",
                f"{data_point['max_temperature']:.1f}°C",
                f"{data_point['min_humidity']:.1f}%",
                f"{data_point['max_humidity']:.1f}%"
            ]

            print("\033[90m | \033[0m".join(fields))


    @property
    def date(self):
        with self._lock:
            return self.data[-1]["date"] if self.data else None


    @property
    def time(self):
        with self._lock:
            return self.data[-1]["time"] if self.data else None


    @property
    def temperature(self):
        with self._lock:
            return self.data[-1]["temperature"] if self.data else None


    @property
    def humidity(self):
        with self._lock:
            return self.data[-1]["humidity"] if self.data else None


    @property
    def fan_pwm(self):
        with self._lock:
            return self.data[-1]["fan_pwm"] if self.data else None


    @property
    def fan_rpm(self):
        with self._lock:
            return self.data[-1]["fan_rpm"] if self.data else None


    @property
    def time_period(self):
        with self._lock:
            return self.data[-1]["time_period"] if self.data else None


    @property
    def min_temperature(self):
        with self._lock:
            return self.data[-1]["min_temperature"] if self.data else None


    @property
    def max_temperature(self):
        with self._lock:
            return self.data[-1]["max_temperature"] if self.data else None


    @property
    def min_humidity(self):
        with self._lock:
            return self.data[-1]["min_humidity"] if self.data else None


    @property
    def max_humidity(self):
        with self._lock:
            return self.data[-1]["max_humidity"] if self.data else None
