
from propbox._parameters import Parameters
from propbox._module import Module
from propbox._sensor import Sensor
from propbox._fan import Fan 

from datetime import datetime

class DataManager(Module):
    def __init__(self, parameters:Parameters, sensor:Sensor, fan:Fan, output=True) -> None:
        super().__init__()
        self._parameters: Parameters = parameters
        self._sensor:     Sensor     = sensor
        self._fan:        Fan        = fan
        
        self._print:      bool = output 
        
        self._date             = None
        self._time             = None
        self._temperature      = None
        self._humidity         = None
        self._fan_pwm          = None
        self._fan_rpm          = None
        self._time_period      = None
        self._min_temperature  = None
        self._max_temperature  = None
        self._min_humidity     = None
        self._max_humidity     = None
        
    def _update(self):
        with self._lock:
            now = datetime.now()
            self._date            = now.strftime("%y:%m:%d")
            self._time            = now.strftime("%H:%M:%S")
            self._temperature     = self._sensor.temperature
            self._humidity        = self._sensor.humidity
            self._fan_pwm         = self._fan.pwm
            self._fan_rpm         = self._fan.rpm
            self._time_period     = self._parameters.time_period
            self._min_temperature = self._parameters.min_temperature
            self._max_temperature = self._parameters.max_temperature
            self._min_humidity    = self._parameters.min_humidity
            self._max_humidity    = self._parameters.max_humidity

 
            if self._print == True:
                fields = [
                    f"{self._date}",
                    f"{self._time}",
                    f"\033[94m{self._temperature:.1f}°C\033[0m",
                    f"\033[94m{self._humidity:.1f}%\033[0m",
                    f"{self._fan_pwm}%",
                    f"{self._fan_rpm:.0f} RPM",
                    f"{self._time_period}",
                    f"{self._min_temperature:.1f}°C",
                    f"{self._max_temperature:.1f}°C",
                    f"{self._min_humidity:.1f}%",
                    f"{self._max_humidity:.1f}%"
                ]
                print("\033[90m | \033[0m".join(fields))

    @property
    def date(self):
        with self._lock: return self._date
    
    @property
    def time(self):
        with self._lock: return self._time
    
    @property
    def temperature(self):
        with self._lock: return self._temperature
    
    @property
    def humidity(self): 
        with self._lock: return self._humidity
    
    @property
    def fan_pwm(self):
        with self._lock: return self._fan_pwm
    
    @property
    def fan_rpm(self):
        with self._lock: return self._fan_rpm
    
    @property
    def time_period(self):
        with self._lock: return self._time_period
    
    @property
    def min_temperature(self):
        with self._lock: return self._min_temperature
    
    @property
    def max_temperature(self):
        with self._lock: return self._max_temperature
    
    @property
    def min_humidity(self):
        with self._lock: return self._min_humidity

    @property
    def max_humidity(self):
        with self._lock: return self._max_humidity

    def as_dict(self):
        with self._lock:
            return {
                "date": self._date,
                "time": self._time,
                "temperature": self._temperature,
                "humidity": self._humidity,
                "fan_pwm": self._fan_pwm,
                "fan_rpm": self._fan_rpm,
                "min_temperature": self._min_temperature,
                "max_temperature": self._max_temperature,
                "min_humidity": self._min_humidity,
                "max_humidity": self._max_humidity
            }
