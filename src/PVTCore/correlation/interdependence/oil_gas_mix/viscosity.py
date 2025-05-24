from __future__ import annotations

from typing import TYPE_CHECKING

from PVTCore.units import Viscosity

from PVTCore.correlation.abstract.param import ViscosityCorrelation

if TYPE_CHECKING:
    from PVTCore.aggregator.aggregator import ModelCorrelationAggregator
    from PVTCore.aggregator.entity.oil import OilPhaseCorrelationAggregator
    from PVTCore.correlation.abstract import CorrelationVariable


class OilInContactWithGasViscosityCorrelation(ViscosityCorrelation):
    _oil_model: OilPhaseCorrelationAggregator
    _collection: None

    @property
    def aggregator(self) -> ModelCorrelationAggregator:
        return self._oil_model._aggregator

    def calc(self, var: CorrelationVariable) -> Viscosity:
        is_saturated, dissolved = self.aggregator.mixer.calc(var)
        gor = var.gas_oil_ratio

        var.set_gas_oil_ratio(dissolved)
        viscosity = self._oil_model.sat.vis.calc(var)
        unsaturated_vis = self._oil_model.unsat.vis.calc(var)

        viscosity.value[~is_saturated] = unsaturated_vis.value[~is_saturated]
        var.set_gas_oil_ratio(gor)

        return viscosity
