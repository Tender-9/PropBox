from ._module import Module

import RPi.GPIO as GPIO
import time

class Fan(Module):
    def __init__(self, pwm_pin, rpm_pin) -> None:
        super().__init__()
        self._pwm_pin = pwm_pin
        self._rpm_pin = rpm_pin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pwm_pin, GPIO.OUT)
        GPIO.setup(self._rpm_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self._pwm = GPIO.PWM(self._pwm_pin, 25000) 
        self._duty_cycle  = 100
        self._pwm.start(self._duty_cycle) 
        self._rpm = 0
        self._last_update = 0
        self._update()

    
    @property
    def rpm(self) -> float:
        if time.time() - self._last_update > 0.1:
            self._update()
        return self._rpm
    
    
    @property
    def pwm(self) -> int:
        return self._duty_cycle

    
    @pwm.setter
    def pwm(self, percent):
        self._duty_cycle = percent
        self._pwm.ChangeDutyCycle(percent)

    
    def _update(self):
        with self._lock:
            pulses = 0
            last_state = GPIO.input(self._rpm_pin)
            start_time = time.time()

            while pulses < 20:
                current_state = GPIO.input(self._rpm_pin)
                if last_state == 1 and current_state == 0: 
                    pulses += 1
                last_state = current_state

            elapsed = time.time() - start_time
            self._rpm = (10 / elapsed) * 60
            self._last_update = time.time()

    
    def _cleanup(self):
        time.sleep(0.1)
        self._pwm.stop()
        GPIO.cleanup([self._pwm_pin, self._rpm_pin])
