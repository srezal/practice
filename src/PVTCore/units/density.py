from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Any

import numpy as np

from .abstract import AbstractParam, AbstractUnit

from pydantic_core import CoreSchema, core_schema

from pydantic import GetCoreSchemaHandler

if TYPE_CHECKING:
    from typing import Union


FamousDensityUnit = Literal["kg_per_m3", "relative", "api"]


class DensityUnit(AbstractUnit):
    kg_per_m3 = "kg_per_m3"
    relative = "relative"
    api = "api"

    def is_kg_per_m3(self) -> bool:
        return self == self.kg_per_m3

    def is_relative(self) -> bool:
        return self == self.relative

    def is_api(self) -> bool:
        return self == self.api


class Density(AbstractParam):

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(float))

    def __init__(
        self,
        value: Union[np.ndarray, int, float],
        unit: Union[DensityUnit, FamousDensityUnit] = DensityUnit.kg_per_m3,
        relative_coefficient: Union[int, float] = 1000,
    ) -> None:

        if isinstance(unit, str):
            unit = DensityUnit.from_string(unit)

        if unit.is_kg_per_m3():
            pass
        elif unit.is_relative():
            value = value * relative_coefficient
        elif unit.is_api():
            value = 141.5 / (value + 131.5)
        else:
            raise ValueError("Неизвестная еденица измерения плотности")

        self.__relative_coefficient = relative_coefficient
        self.value = value

    @staticmethod
    def default_unit() -> DensityUnit:
        return DensityUnit.kg_per_m3

    def relative(self) -> Union[np.ndarray, int, float]:
        return self.value / self.__relative_coefficient

    def kg_per_m3(self) -> Union[np.ndarray, int, float]:
        return self.value

    def api(self) -> Union[np.ndarray, int, float]:
        return 141.5 / self.value * 1000 - 131.5

    def get(self, unit: Union[AbstractUnit, FamousDensityUnit]) -> Union[np.ndarray, int, float]:

        if isinstance(unit, str):
            unit = DensityUnit.from_string(unit)

        if unit.is_kg_per_m3():
            return self.kg_per_m3()
        elif unit.is_relative():
            return self.relative()
        elif unit.is_api():
            return self.api()
        else:
            raise ValueError("Неизвестная еденица измерения плотности")
