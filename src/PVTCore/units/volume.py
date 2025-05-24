from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import numpy as np

from .abstract import AbstractParam, AbstractUnit

if TYPE_CHECKING:
    from typing import Union


FamousVolumeUnit = Literal["m3"]


class VolumeUnit(AbstractUnit):
    m3 = "m3"

    def is_m3(self) -> bool:
        return self == self.m3


class Volume(AbstractParam):
    def __init__(
        self,
        value: Union[np.ndarray, int, float],
        unit: Union[VolumeUnit, FamousVolumeUnit] = VolumeUnit.m3,
    ) -> None:

        if isinstance(unit, str):
            unit = VolumeUnit.from_string(unit)

        if unit.is_m3():
            pass
        else:
            raise ValueError("Неизвестная еденица измерения oбъема")

        self.value = value

    @staticmethod
    def default_unit() -> VolumeUnit:
        return VolumeUnit.m3

    def m3(self) -> Union[np.ndarray, int, float]:
        return self.value

    def get(self, unit: Union[AbstractUnit, FamousVolumeUnit]) -> Union[np.ndarray, int, float]:

        if isinstance(unit, str):
            unit = VolumeUnit.from_string(unit)

        if unit.is_m3():
            return self.m3()
        else:
            raise ValueError("Неизвестная еденица измерения oбъема")