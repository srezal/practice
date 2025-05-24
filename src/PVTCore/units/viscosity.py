from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import numpy as np

from .abstract import AbstractParam, AbstractUnit

if TYPE_CHECKING:
    from typing import Union


FamousViscUnit = Literal["CentiPoise", "Newton_second"]


class ViscUnit(AbstractUnit):
    cP = "CentiPoise"
    Newton = "Newton_second"

    def is_cp(self) -> bool:
        return self == self.cP

    def is_newton(self) -> bool:
        return self == self.Newton


class Viscosity(AbstractParam):
    __cp_coefficient = 10**-3

    def __init__(
        self,
        value: Union[np.ndarray, int, float],
        unit: Union[ViscUnit, FamousViscUnit] = ViscUnit.cP,
    ):

        if isinstance(unit, str):
            unit = ViscUnit.from_string(unit)

        if unit.is_newton():
            pass
        if unit.is_cp():
            value = value * self.__cp_coefficient
        else:
            raise ValueError("Неизвестная еденица измерения вязкости")

        self.value = value

    @staticmethod
    def default_unit() -> ViscUnit:
        return ViscUnit.Newton

    def newton(self) -> Union[np.ndarray, int, float]:
        return self.value

    def cp(self) -> Union[np.ndarray, int, float]:
        return self.value / self.__cp_coefficient

    def get(self, unit: Union[AbstractUnit, FamousViscUnit]) -> Union[np.ndarray, int, float]:

        if isinstance(unit, str):
            unit = ViscUnit.from_string(unit)

        if unit.is_newton():
            return self.newton()
        if unit.is_cp():
            return self.cp()
        else:
            raise ValueError("Неизвестная еденица измерения вязкости")
