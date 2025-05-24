from __future__ import annotations

from typing import TYPE_CHECKING

from PVTCore.correlation.abstract.param import SolubilityCorrelation

if TYPE_CHECKING:
    from PVTCore.units import Solubility

    from PVTCore.aggregator.aggregator import ModelCorrelationAggregator
    from PVTCore.aggregator.entity.oil import OilPhaseCorrelationAggregator
    from PVTCore.correlation.abstract import CorrelationVariable


class OilInContactWithGasSolubilityCorrelation(SolubilityCorrelation):
    _oil_model: OilPhaseCorrelationAggregator
    _collection: None

    @property
    def aggregator(self) -> ModelCorrelationAggregator:
        return self._oil_model._aggregator

    def calc(self, var: CorrelationVariable) -> Solubility:
        is_saturated, dissolved = self.aggregator.mixer.calc(var)
        gor = var.gas_oil_ratio

        var.set_gas_oil_ratio(dissolved)

        solubility = self._oil_model.sat.sol.calc(var)
        solubility.value[~is_saturated] = gor

        var.set_gas_oil_ratio(gor)

        return solubility
