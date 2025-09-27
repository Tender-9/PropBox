from ._parameters import Parameters
from ._climate import Climate
from ._sensor import Sensor
from ._logger import Logger
from ._fan import Fan

import time
import os

def main():
    directory = os.path.dirname(__file__)
    modules = []
    
    # Setup sensor
    sensor = Sensor(address=0x44, bus=1)
    sensor.start()
    modules.append(sensor)

    # Setup fan
    fan = Fan(pwm_pin=18, rpm_pin=24)
    fan.start()
    modules.append(fan)

    # Setup and start parameter manager to update just before the minute
    parameters = Parameters(os.path.join(directory, "parameters.json"))
    parameters.start(period=60, offset=-0.5)
    modules.append(parameters)
    
    climate = Climate(sensor=sensor, fan=fan, parameters=parameters)
    climate.start(offset=0.1)
    modules.append(climate)

    # Setup and start logger to update on the minute
    logger = Logger(parameters=parameters, sensor=sensor, fan=fan)
    logger.start(period=60)
    modules.append(logger)

    try:
        while True: 
            time.sleep(1)

    except(KeyboardInterrupt):
        for module in modules:
            module.stop()
