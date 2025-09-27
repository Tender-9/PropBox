from ._module import Module
from ._parameters import Parameters
from ._sensor import Sensor
from ._fan import Fan

# I'm going to need some new hardware to fully implement my dreams here

class Climate(Module):
    def __init__(self, parameters:Parameters, sensor:Sensor, fan:Fan) -> None:
        super().__init__()
        self._parameters: Parameters = parameters
        self._sensor:     Sensor     = sensor
        self._fan:        Fan        = fan
       
        self._max_speed:  int  = 100
        self._min_speed:  int  = 80
        self._cooldown:   bool = False
    
    def _update(self):
        temp     = self._sensor.temperature
        max_temp = self._parameters.max_temperature
        min_temp = self._parameters.min_temperature

        if self._cooldown == False and temp >= max_temp:
            self._cooldown = True

        elif self._cooldown == True and temp <= min_temp:
            self._cooldown = False

        if self._cooldown == True: self._fan.pwm = self._max_speed
        else: self._fan.pwm = self._min_speed
