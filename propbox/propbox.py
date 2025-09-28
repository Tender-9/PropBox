from propbox.inputs import Inputs, Sensor, Fan, Parameters
from propbox.climate import ClimateManager
from propbox.data import DataManager

import time
import os



def main():

    inputs = Inputs()
    inputs.add("sensor", input=Sensor(address=0x44, bus=1))
    inputs.add("fan", input=Fan(pwm_pin=18, rpm_pin=24))
    inputs.add("parameters", input=Parameters(os.path.join(os.getcwd(), "parameters.json")))

    inputs.sensor.start(period=1)      # Updates every 1s, on the second
    inputs.fan.start(period=1)         # Updates every 1s, on the second
    inputs.parameters.start(period=10) # Updates every 10s, on the second

    data = DataManager(sensor=inputs.sensor, fan=inputs.fan, parameters=inputs.parameters)
    data.start(offset=0.2) 
    
    # Setup and start climate
    climate = ClimateManager(data, fan=inputs.fan)
    climate.start(offset=0.5)

    try:
        while True: 
            time.sleep(2)

    except:
        inputs.stop()
