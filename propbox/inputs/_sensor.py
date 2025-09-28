from propbox._module import Module

import atexit
import threading
import smbus
import time

class Sensor(Module):
    def __init__(self, address, bus, max_heat_duration=60) -> None:
        super().__init__()
        self._address                  = address
        self._bus                      = smbus.SMBus(bus)
        self._max_heat_duration: int   = max_heat_duration
        self._temperature:       float = float("nan")
        self._humidity:          float = float("nan")
        self._last_update:       float = float("nan") 
        self._heater_status:     bool  = False
        self._heater_timer             = None
        
        atexit.register(self._fail_safe)
        self._update()
    
    
    @property
    def temperature(self) -> float:
        if time.time() - self._last_update > 0.1: 
            self._update()
        return self._temperature

    
    @property
    def humidity(self) -> float:
        if time.time() - self._last_update > 0.1: 
            self._update()
        return self._humidity
    
    
    @property
    def heater(self) -> bool:
        return self._heater_status
    

    @heater.setter
    def heater(self, value: bool) -> None:
        if value == True: 
            self._bus.write_i2c_block_data(self._address, 0x30, [0x6D])
            self._heater_status = True 
            self._heater_timer = threading.Thread(target=self._auto_heater_shutoff, daemon=True)
            self._heater_timer.start()

        elif value == False: 
            self._bus.write_i2c_block_data(self._address, 0x30, [0x66])
            self._heater_status = False
    

    def _update(self):
        with self._lock:
            # Request data
            self._bus.write_i2c_block_data(self._address, 0x24, [0x00]) 
            time.sleep(0.02)
            data = self._bus.read_i2c_block_data(self._address, 0, 6)
            # Interpret temperature
            raw_temperature = (data[0] << 8) | data[1]
            self._temperature = -45 + 175 * raw_temperature / 65535 
            # Interpret humidity
            raw_humidity = (data[3] << 8) | data[4]
            self._humidity = 100 * raw_humidity / 65535
            self._last_update = time.time()

    
    def _cleanup(self):
        self._fail_safe()
    
    
    def _auto_heater_shutoff(self):
        time.sleep(self._max_heat_duration)
        self._fail_safe()
        
    
    def _fail_safe(self):
        try:
            if self._heater_status == True:
                self.heater = False
        except: 
            pass
