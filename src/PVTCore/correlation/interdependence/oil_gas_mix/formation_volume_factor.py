from __future__ import annotations

from typing import TYPE_CHECKING

from PVTCore.correlation.abstract.param import VolumeFactorCorrelation

if TYPE_CHECKING:
    from PVTCore.units import VolumeFactor

    from PVTCore.aggregator.aggregator import ModelCorrelationAggregator
    from PVTCore.aggregator.entity.oil import OilPhaseCorrelationAggregator
    from PVTCore.correlation.abstract import CorrelationVariable


class OilInContactWithGasVolumeFactorCorrelation(VolumeFactorCorrelation):
    _oil_model: OilPhaseCorrelationAggregator
    _collection: None

    @property
    def aggregator(self) -> ModelCorrelationAggregator:
        return self._oil_model._aggregator

    def calc(self, var: CorrelationVariable) -> VolumeFactor:
        is_saturated, dissolved = self.aggregator.mixer.calc(var)
        gor = var.gas_oil_ratio

        var.set_gas_oil_ratio(dissolved)
        formation_volume_factor = self._oil_model.sat.fvf.calc(var)
        unsaturated_fvf = self._oil_model.unsat.fvf.calc(var)

        formation_volume_factor.value[~is_saturated] = unsaturated_fvf.value[~is_saturated]
        var.set_gas_oil_ratio(gor)

        return formation_volume_factor
