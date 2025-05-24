from __future__ import annotations

from typing import TYPE_CHECKING

from PVTCore.correlation.interdependence.oil.unsaturated.viscosity import abstract

if TYPE_CHECKING:
    from PVTCore.correlation.abstract import CorrelationVariable


class NoViscosibility(abstract.ViscosityUnSaturatedOilCorrelation):
    def calc(self, var: CorrelationVariable):
        bp_viscosity = self._collection._oil_model.sat.vis.calc(var)
        return bp_viscosity
