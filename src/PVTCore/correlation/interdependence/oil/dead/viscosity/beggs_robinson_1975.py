from __future__ import annotations

from typing import TYPE_CHECKING

from PVTCore.units import Viscosity

from PVTCore.correlation.abstract.param import ViscosityCorrelation
from PVTCore.correlation.abstract.phase import DeadOilCorrelation

if TYPE_CHECKING:
    from PVTCore.correlation.abstract import CorrelationVariable


class DeadBeggs(ViscosityCorrelation, DeadOilCorrelation):
    """https://nafta.wiki/pages/viewpage.action?pageId=85393777"""

    c1 = 3.0324
    c2 = -0.02023
    c3 = -1.163

    def calc(self, var: CorrelationVariable) -> Viscosity:
        temp = var.temp.kelvin()
        dens_oil = var.oil.dens.api()

        z = self.c1 + self.c2 * dens_oil
        x = (10**z) * (temp**self.c3)
        return (10**x) - 1
