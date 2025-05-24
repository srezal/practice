from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Any

from pydantic_core import CoreSchema, core_schema

from pydantic import GetCoreSchemaHandler

import numpy as np

from .abstract import AbstractParam, AbstractUnit

if TYPE_CHECKING:
    from typing import Union


FamousTempUnit = Literal["Kelvin", "Celsius", "Fahrenheit"]


class TempUnit(AbstractUnit):
    Kelvin = "Kelvin"
    Celsius = "Celsius"
    Fahrenheit = "Fahrenheit"

    def is_kelvin(self) -> bool:
        return self == self.Kelvin

    def is_celsius(self) -> bool:
        return self == self.Celsius

    def is_fahrenheit(self) -> bool:
        return self == self.Fahrenheit


class Temperature(AbstractParam):
    __celsius_coefficient = 273.15

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(float))

    def __init__(
        self,
        value: Union[np.ndarray, int, float],
        unit: Union[TempUnit, FamousTempUnit] = TempUnit.Celsius,
    ):

        if isinstance(unit, str):
            unit = TempUnit.from_string(unit)

        if unit.is_kelvin():
            pass
        elif unit.is_celsius():
            value = value + self.__celsius_coefficient
        elif unit.is_fahrenheit():
            value = value + self.__celsius_coefficient
            value = value - 32
            value = value / 1.8
        else:
            raise ValueError("Неизвестная еденица измерения температуры")

        self.value = value

    @staticmethod
    def default_unit() -> TempUnit:
        return TempUnit.Kelvin

    def celsius(self) -> np.ndarray:
        return self.value

    def fahrenheit(self) -> np.ndarray:
        results = 1.8 * (self.value - self.__celsius_coefficient) + 32
        return results

    def kelvin(self) -> np.ndarray:
        return self.value

    def get(self, unit: Union[AbstractUnit, FamousTempUnit]) -> np.ndarray:

        if isinstance(unit, str):
            unit = TempUnit.from_string(unit)

        if unit.is_kelvin():
            return self.kelvin()
        elif unit.is_celsius():
            return self.celsius()
        elif unit.is_fahrenheit():
            return self.fahrenheit()
        else:
            raise ValueError("Неизвестная единица измерения температуры")
