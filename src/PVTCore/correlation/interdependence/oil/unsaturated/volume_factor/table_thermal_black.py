from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from PVTCore.correlation.abstract import CorrelationVariable
from PVTCore.correlation.abstract.param import VolumeFactorCorrelation
from PVTCore.correlation.abstract.phase import UnSaturatedOilCorrelation
from PVTCore.correlation.abstract.table import TwoDimensionalTableCorrelation

if TYPE_CHECKING:

    from PVTCore.units import Pressure, Temperature, VolumeFactor

    from PVTCore.aggregator.entity.abstract import CorrelationAggregator


class ThermalDeadOilFormationVolumeFactorTable(
    TwoDimensionalTableCorrelation,
    VolumeFactorCorrelation,
    UnSaturatedOilCorrelation,
):
    def __init__(
        self,
        pressure: Pressure,
        temperature: Temperature,
        volume_factor: VolumeFactor,
        collection: Optional[CorrelationAggregator] = None,
    ) -> None:
        super().__init__(
            x_value=pressure.value,
            y_value=temperature.value,
            z_value=volume_factor.value,
            collection=collection,
        )

    def calc(self, var: CorrelationVariable) -> VolumeFactor:
        results = self._get_value(
            x_value=var.pres.value,
            y_value=var.temp.value,
        )
        return VolumeFactor(results)
