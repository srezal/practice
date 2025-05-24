from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Any

import numpy as np

from .abstract import AbstractParam, AbstractUnit

from pydantic_core import CoreSchema, core_schema

from pydantic import GetCoreSchemaHandler

if TYPE_CHECKING:
    from typing import Union


FamousMassUnit = Literal["kg"]


class MassUnit(AbstractUnit):
    kg = "kg"

    def is_kg(self) -> bool:
        return self == self.kg


class Mass(AbstractParam):

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(float))

    def __init__(
        self,
        value: Union[np.ndarray, int, float],
        unit: Union[MassUnit, FamousMassUnit] = MassUnit.kg,
    ) -> None:

        if isinstance(unit, str):
            unit = MassUnit.from_string(unit)

        if unit.is_kg():
            pass
        else:
            raise ValueError("Неизвестная еденица измерения Массы")

        self.value = value

    @staticmethod
    def default_unit() -> MassUnit:
        return MassUnit.kg

    def kg(self) -> Union[np.ndarray, int, float]:
        return self.value

    def get(self, unit: Union[AbstractUnit, FamousMassUnit]) -> Union[np.ndarray, int, float]:

        if isinstance(unit, str):
            unit = MassUnit.from_string(unit)

        if isinstance(unit, str):
            unit = MassUnit.from_string(unit)

        if unit.is_kg():
            return self.kg()
        else:
            raise ValueError("Неизвестная еденица измерения Массы")
