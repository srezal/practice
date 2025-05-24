from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from PVTCore.correlation.abstract import CorrelationVariable
from PVTCore.correlation.abstract.param import ViscosityCorrelation
from PVTCore.correlation.abstract.phase import WatCorrelation

if TYPE_CHECKING:
    from typing import Union


class Likhachev(ViscosityCorrelation, WatCorrelation):
    """https://nafta.wiki/pages/viewpage.action?pageId=74482269"""

    a = 2.547 * 10**-4  # bar-1
    a1 = 6.42 * 10**-7  # K-1 · bar-1
    a2 = 7.967 * 10**-8  # bar-2
    a3 = 1.16 * 10**-10  # K-1 · bar-2

    b = 2.795 * 10**-4  # kJ · mol-1 · bar-1
    b1 = 2.48 * 10**-6  # kJ · mol-1 · K-1 ·bar-1

    c = -4.85 * 10**-3  # K · bar-1
    c1 = 6.32 * 10**-5  # bar-1

    e = 4.753  # kJ · mol-1
    o = 139.7  # K
    mu0 = 2.4055 * 10**-2  # cp
    r = 8.31446 * 10**-3  # kJ ⋅ mol-1 ⋅ K-1

    @classmethod
    def fun1(
        cls,
        var: CorrelationVariable,
    ) -> Union[np.ndarray, int, float]:
        temp = var.temp.kelvin()
        pres = var.pres.bar()
        results = (cls.a + cls.a1 * temp) * pres
        return results

    @classmethod
    def fun2(
        cls,
        var: CorrelationVariable,
    ) -> Union[np.ndarray, int, float]:
        temp = var.temp.kelvin()
        pres = var.pres.bar()
        results = (cls.a2 + cls.a3 * temp) * pres**2
        return results

    @classmethod
    def fun3(
        cls,
        var: CorrelationVariable,
    ) -> Union[np.ndarray, int, float]:
        temp = var.temp.kelvin()
        pres = var.pres.bar()
        numerator = cls.e - (cls.b + cls.a1 * temp) * pres
        denominator = cls.r * (temp - cls.o - (cls.c + cls.c1 * temp) * pres)
        results = numerator / denominator
        return results

    @classmethod
    def calc(
        cls,
        var: CorrelationVariable,
    ) -> Union[np.ndarray, int, float]:
        k = cls.fun1(var) + cls.fun2(var) + cls.fun3(var)
        results = cls.mu0 * np.exp(k)
        return results
