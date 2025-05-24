from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from PVTCore.correlation.abstract import CorrelationVariable
from PVTCore.correlation.abstract.param.volume_factor import VolumeFactorCorrelation
from PVTCore.correlation.abstract.phase import WatCorrelation

if TYPE_CHECKING:
    from typing import Union


class McCain(VolumeFactorCorrelation, WatCorrelation):
    """
    https://nafta.wiki/pages/viewpage.action?pageId=84344836
    https://nafta.wiki/display/GLOSSARY/Water+compressibility+%3D+cw
    """

    compressibility = 4.53 * 10**-5  # atm-1
    k1 = 62.368
    k2 = 0.438603
    k3 = 0.00160074

    @classmethod
    def pure_water_density(
        cls,
        var: CorrelationVariable,
    ) -> Union[np.ndarray, int, float]:
        s = var.sali
        results = cls.k1 + cls.k2 * s + cls.k3 * s**2
        return results

    @classmethod
    def vfv(
        cls,
        var: CorrelationVariable,
    ) -> Union[np.ndarray, int, float]:
        temp = var.temp.fahrenheit()
        pres = var.pres.psi()
        v_wp = -1.0001 * 10**-2 + 1.33391 * 10**-4 * temp + 5.50654 * 10**-7 * temp**2
        v_wt = (
            -1.95301 * 10**-9 * pres * temp
            - 1.72834 * 10**-13 * pres**2 * temp
            - 3.58922 * 10**-7 * pres
            - 2.25341 * 10**-10 * pres**2
        )
        results = (1 + v_wp) * (1 - v_wt)
        return results

    @classmethod
    def calc(
        cls,
        var: CorrelationVariable,
    ) -> Union[np.ndarray, int, float]:
        # pure_water_density = var.wat_dens.kg_per_m3()
        # base_pres = var.pres.standard_conditions().bar()
        # pres = var.pres.bar()
        # mult = np.exp(cls.compressibility * (pres - base_pres))
        # dens = pure_water_density * mult
        # results = dens / var.wat_dens.kg_per_m3()
        return cls.vfv(var)
