from __future__ import annotations

from PVTCore.units import VolumeFactor

from PVTCore.correlation.abstract import CorrelationVariable
from PVTCore.correlation.abstract.param import VolumeFactorCorrelation
from PVTCore.correlation.abstract.phase import SaturatedOilCorrelation


class Beggs(VolumeFactorCorrelation, SaturatedOilCorrelation):
    FVF_k1 = 0.972
    FVF_k2 = 0.000147
    FVF_k3 = 5.614583333333334
    FVF_k4 = 2.25
    FVF_k5 = 574.5875
    FVF_k6 = 1.175

    def calc(
        self,
        var: CorrelationVariable,
    ) -> VolumeFactor:
        solubility = self._collection.sol.calc(var).m3_per_m3()
        dens_gas = var.gas.dens.relative()
        dens_oil = var.oil.dens.relative()
        temp = var.temp.kelvin()

        dens_rel = solubility * (dens_gas / dens_oil) ** 0.5
        brackets = self.FVF_k3 * dens_rel + self.FVF_k4 * temp - self.FVF_k5
        results = self.FVF_k1 + self.FVF_k2 * brackets**self.FVF_k6
        return VolumeFactor(results)
