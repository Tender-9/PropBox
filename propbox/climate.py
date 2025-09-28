from propbox._module import Module
from propbox.inputs import Fan
from propbox.data import DataManager


# I'm going to need some new hardware to fully implement my dreams here
# I realize the "inputs" phrasing for fan in this context doesn't make sense

class ClimateManager(Module):
    def __init__(self, data:DataManager, fan:Fan) -> None:
        super().__init__()
        
        self._data_manager: DataManager = data
        self._fan:          Fan         = fan
        
        self._max_speed:    int         = 100
        self._min_speed:    int         = 80
        self._cooldown:     bool        = False
    
    def _update(self):
        temp     = self._data_manager.temperature
        min_temp = self._data_manager.min_temperature
        max_temp = self._data_manager.max_temperature

        if self._cooldown == False and temp >= max_temp:
            self._cooldown = True

        elif self._cooldown == True and temp <= min_temp:
            self._cooldown = False

        if self._cooldown == True: self._fan.pwm = self._max_speed
        else: self._fan.pwm = self._min_speed
