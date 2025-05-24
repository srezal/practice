from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from PVTCore.correlation.abstract import CorrelationVariable
from PVTCore.correlation.abstract.param.viscosity import ViscosityCorrelation
from PVTCore.correlation.abstract.phase import WatCorrelation

if TYPE_CHECKING:
    from typing import Union


class McCain(ViscosityCorrelation, WatCorrelation):
    """https://nafta.wiki/pages/viewpage.action?pageId=74482295"""

    k1 = 0.9994
    k2 = 4.0295 * 10**-5
    k3 = 3.1062 * 10**-9

    k4 = 109.574
    k5 = -8.40564
    k6 = 0.313314
    k7 = 8.72213 * 10**-5

    k8 = -1.2166
    k9 = 2.63951 * 10**-2
    k10 = -6.79461 * 10**-4
    k11 = -5.47119 * 10**-5
    k12 = 1.55586 * 10**-6

    @classmethod
    def a(
        cls,
        var: CorrelationVariable,
    ) -> Union[np.ndarray, int, float]:
        s = var.wat.sali
        results = cls.k8 + cls.k9 * s + cls.k10 * s**2 + cls.k11 * s**3 + cls.k12 * s**4
        return results

    @classmethod
    def atm_visc(
        cls,
        var: CorrelationVariable,
    ) -> Union[np.ndarray, int, float]:
        s = var.wat.sali
        a = cls.a(var)
        temp = var.temp.fahrenheit()
        mult = cls.k4 + cls.k5 * s + cls.k6 * s**2 + cls.k7 * s**3
        results = mult * temp**a
        return results

    @classmethod
    def calc(
        cls,
        var: CorrelationVariable,
    ) -> Union[np.ndarray, int, float]:
        atm_visc = cls.atm_visc(var)
        pres = var.pres.psi()
        mult = cls.k1 * cls.k2 * pres + cls.k3 * pres**2
        results = atm_visc * mult
        return results
