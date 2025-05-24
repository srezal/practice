from __future__ import annotations

from typing import TYPE_CHECKING

from PVTCore.units import Viscosity

from PVTCore.correlation.abstract import CorrelationVariable
from PVTCore.correlation.abstract.param import ViscosityCorrelation
from PVTCore.correlation.abstract.phase import SaturatedOilCorrelation

if TYPE_CHECKING:
    from PVTCore.aggregator.entity import oil


class LiveBeggs(ViscosityCorrelation, SaturatedOilCorrelation):
    """https://nafta.wiki/pages/viewpage.action?pageId=85393806"""

    _collection: oil.SaturatedOilCorrelationAggregator

    c1 = 10.715
    c2 = 100
    c3 = -0.515
    c4 = 5.44
    c5 = 150
    c6 = -0.338

    def calc(
        self,
        var: CorrelationVariable,
    ) -> Viscosity:
        sol = var.gas_oil_ratio.foot_per_barrel()
        deed_viscosity = self._collection._oil_model.dead.vis.calc(var)
        b = self.c4 * (sol + self.c5) ** self.c6
        a = self.c1 * (sol + self.c2) ** self.c3
        results = a * deed_viscosity**b
        return Viscosity(results)
