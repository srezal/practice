from __future__ import annotations

from enum import StrEnum

from typing import TYPE_CHECKING, Literal, Any

from pydantic_core import CoreSchema, core_schema

from pydantic import GetCoreSchemaHandler

import numpy as np

from .abstract import AbstractParam, AbstractUnit

if TYPE_CHECKING:
    from typing import Union


FamousSolubilityUnit = Literal["м3/м3", "Foot_per_barrel"]


class SolubilityUnit(AbstractUnit):
    m3_per_m3 = "м3/м3"
    Foot_per_barrel = "Foot_per_barrel"

    def is_m3_per_m3(self) -> bool:
        return self == self.m3_per_m3

    def is_foot_per_barrel(self) -> bool:
        return self == self.Foot_per_barrel


class Solubility(AbstractParam):
    __foot_per_barrel = 0.17810760667903522

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(float))

    def __init__(
        self,
        value: Union[np.ndarray, int, float],
        unit: Union[SolubilityUnit, FamousSolubilityUnit] = SolubilityUnit.m3_per_m3,
    ):
        self.value = value

        if isinstance(unit, str):
            unit = SolubilityUnit.from_string(unit)

        if unit.is_m3_per_m3():
            self.value = self.__from_m3_per_m3()
        elif unit.is_foot_per_barrel():
            self.value = self.__from_foot_per_barrel()
        else:
            msg = "Неизвестная еденица измерения газосодержания"
            raise ValueError(msg)

    def __from_m3_per_m3(self) -> Union[np.ndarray, int, float]:
        return self.value

    def __from_foot_per_barrel(self) -> Union[np.ndarray, int, float]:
        return self.value / self.__foot_per_barrel

    @staticmethod
    def default_unit() -> SolubilityUnit:
        return SolubilityUnit.m3_per_m3

    def m3_per_m3(self) -> Union[np.ndarray, int, float]:
        return self.value

    def foot_per_barrel(self) -> Union[np.ndarray, int, float]:
        return self.value * self.__foot_per_barrel

    def get(self, unit: Union[AbstractUnit, FamousSolubilityUnit]) -> Union[np.ndarray, int, float]:

        if isinstance(unit, str):
            unit = SolubilityUnit.from_string(unit)

        if unit.is_m3_per_m3():
            return self.m3_per_m3()
        elif unit.is_foot_per_barrel():
            return self.foot_per_barrel()
        else:
            msg = "Неизвестная еденица измерения газосодержания"
            raise ValueError(msg)
