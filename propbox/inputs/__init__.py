from propbox._module import Module

from ._parameters import Parameters
from ._sensor import Sensor
from ._fan import Fan

from typing import TYPE_CHECKING

class Inputs:
    if TYPE_CHECKING:
        sensor: Sensor
        fan: Fan
        parameters: Parameters

    Sensor = Sensor
    Fan = Fan
    Parameters = Parameters

    def __init__(self) -> None:
        self._instances = {}

    def add(self, name: str, input: Module) -> None:
        self._instances[name] = input
        setattr(self, name, input)

    def stop(self) -> None:
        for module in self._instances.values():
            module.stop()
