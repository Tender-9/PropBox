from propbox._climate_manager import ClimateManager
from propbox._data_manager import DataManager
from propbox._parameters import Parameters
from propbox._module import Module
from propbox._sensor import Sensor
from propbox._gui import Gui
from propbox._fan import Fan
from propbox._api import Api

import time
import os

def main():
    
    modules = []

    sensor = Sensor(address=0x44, bus=1)
    sensor.start(period = 1, offset = -0.2)
    modules.append(sensor)

    fan = Fan(pwm_pin=18, rpm_pin=24)
    fan.start(period = 1, offset = -0.2)
    modules.append(fan)

    parameters = Parameters(os.path.join(os.getcwd(), "parameters.json"))
    parameters.start(period = 5)
    modules.append(parameters)

    data_manager = DataManager(sensor=sensor, fan=fan, parameters=parameters)
    data_manager.start(period=1)
    modules.append(data_manager) 

    climate_manager = ClimateManager(data_manager, fan=fan)
    climate_manager.start(period=5, offset=0.2)
    modules.append(climate_manager)

    api = Api(data_manager=data_manager)
    api.start()
    modules.append(api)

    gui = Gui(data_manager)
    gui.start()
    

    try:
        while True: 
            time.sleep(10)

    except:
        for module in modules:
            module.stop()
