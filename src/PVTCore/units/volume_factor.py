from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import numpy as np

from .abstract import AbstractParam, AbstractUnit

if TYPE_CHECKING:
    from typing import Union

FamousVolumeFactorUnit = Literal["si"]


class VolumeFactorUnit(AbstractUnit):
    si = "si"

    def is_si(self) -> bool:
        return self == self.si


class VolumeFactor(AbstractParam):
    def __init__(
        self,
        value: Union[np.ndarray, int, float],
        unit: Union[VolumeFactorUnit, FamousVolumeFactorUnit] = VolumeFactorUnit.si,
    ):

        if isinstance(unit, str):
            unit = VolumeFactorUnit.from_string(unit)

        if unit.is_si():
            pass
        else:
            msg = "Неизвестная еденица измерения объемного коэфицента"
            raise ValueError(msg)

        self.value = value

    @staticmethod
    def default_unit() -> VolumeFactorUnit:
        return VolumeFactorUnit.si

    def si(self) -> Union[np.ndarray, int, float]:
        return self.value

    def get(self, unit: Union[AbstractUnit, FamousVolumeFactorUnit]) -> Union[np.ndarray, int, float]:

        if isinstance(unit, str):
            unit = VolumeFactorUnit.from_string(unit)

        if unit.is_si():
            return self.si()
        else:
            msg = "Неизвестная еденица измерения объемного коэфицента"
            raise ValueError(msg)
