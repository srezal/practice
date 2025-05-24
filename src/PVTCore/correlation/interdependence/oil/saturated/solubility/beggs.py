from __future__ import annotations

from typing import TYPE_CHECKING

from PVTCore.units import Solubility, SolubilityUnit

from PVTCore.correlation.abstract.param import SolubilityCorrelation
from PVTCore.correlation.abstract.phase import SaturatedOilCorrelation

if TYPE_CHECKING:
    from PVTCore.correlation.abstract import CorrelationVariable


class Beggs(SolubilityCorrelation, SaturatedOilCorrelation):
    RS_k1 = 1.2254503
    RS_k2 = 0.001638
    RS_k3 = 1.76875
    RS_k4 = 1.9243101395421235 * 10**-6
    RS_k5 = 1.2048192771084338

    # TODO Проверить откуда эта корреляция

    def calc(self, var: CorrelationVariable) -> Solubility:
        pres = var.pres.pa()
        temp = var.temp.kelvin()
        dens_oil = var.oil.dens.relative()
        dens_gas = var.gas.dens.relative()

        yg = self.RS_k1 + self.RS_k2 * temp - self.RS_k3 / dens_oil
        results = dens_gas * (self.RS_k4 * pres / 10**yg) ** self.RS_k5
        return Solubility(results, SolubilityUnit.m3_per_m3)
