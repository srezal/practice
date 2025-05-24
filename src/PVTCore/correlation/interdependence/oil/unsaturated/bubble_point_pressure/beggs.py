from __future__ import annotations

from typing import TYPE_CHECKING

from PVTCore.units import Pressure, PresUnit

from PVTCore.correlation.abstract import CorrelationVariable
from PVTCore.correlation.abstract.param import BubblePointPressureCorrelation
from PVTCore.correlation.abstract.phase import UnSaturatedOilCorrelation

if TYPE_CHECKING:
    pass


class Beggs(BubblePointPressureCorrelation, UnSaturatedOilCorrelation):
    k1 = 1.2254503
    k2 = 0.001638
    k3 = 1.76875
    k4 = 1.9243101395421235 * 10**-6
    k5 = 1.2048192771084338

    def calc(
        self,
        var: CorrelationVariable,
    ) -> Pressure:
        temp = var.temp.kelvin()
        dens_oil = var.oil.dens.relative()
        solubility = var.gas_oil_ratio.m3_per_m3()
        dens_gas = var.gas.dens.relative()

        yg = self.k1 + self.k2 * temp - self.k3 / dens_oil
        value = (10**yg) / self.k4 * ((solubility / dens_gas) ** (1 / self.k5))
        return Pressure(value, PresUnit.Pa)
