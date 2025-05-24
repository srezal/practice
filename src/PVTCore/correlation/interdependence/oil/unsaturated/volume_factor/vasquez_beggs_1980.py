from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

import numpy as np

from PVTCore.correlation.abstract.param import VolumeFactorCorrelation
from PVTCore.correlation.abstract.phase import UnSaturatedOilCorrelation

if TYPE_CHECKING:
    from typing import Union

    from PVTCore.correlation.abstract import CorrelationVariable

from PVTCore.units import VolumeFactor


class Beggs(VolumeFactorCorrelation, UnSaturatedOilCorrelation):
    """https://nafta.wiki/display/GLOSSARY/Vasquez-Beggs+%281980%29+undersaturated+oil+isothermal+compressibility++@model"""

    c1 = -1.433 * 10**-5
    c2 = 5 * 10**-5
    c3 = 17.2 * 10**-5
    c4 = -1.180 * 10**-5
    c5 = 12.61 * 10**-5

    def compressibility(
        self,
        var: CorrelationVariable,
    ) -> Union[float, int]:
        temp = var.temp.fahrenheit()
        dens_gas = var.gas.dens.relative()
        dens_oil = var.oil.dens.relative()
        solubility = var.gas_oil_ratio.foot_per_barrel()
        bpp = self._collection.bpp.calc(var).psi()

        numerator = (
            self.c1
            + self.c2 * solubility
            + self.c3 * temp
            + self.c4 * dens_gas
            + self.c4 * dens_oil
        )
        if not isinstance(bpp, np.ndarray):
            results = numerator / bpp if bpp != 0 else numerator
        else:
            results = numerator / bpp
            results[np.isnan(results)] = numerator[np.isnan(results)]

        return results

    def calc(
        self,
        var: CorrelationVariable,
    ) -> VolumeFactor:
        model = self._collection._oil_model
        cvar = deepcopy(var)
        cvar.pres = model.unsat.bpp.calc(var)
        bubble_point_fvf = model.sat.fvf.calc(cvar).si()
        compressibility = self.compressibility(var)
        delta_press = cvar.pres.psi() - var.pres.psi()
        results = bubble_point_fvf * np.exp(compressibility * delta_press)
        return VolumeFactor(results)
