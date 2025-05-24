from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from PVTCore.correlation.abstract import CorrelationVariable
from PVTCore.correlation.interdependence.oil.unsaturated.viscosity import abstract

if TYPE_CHECKING:

    from PVTCore.units import Pressure, Temperature, Viscosity

    from PVTCore.aggregator.entity.abstract import CorrelationAggregator


class ThermalDeadOilViscosityTable(abstract.ViscosityUnSaturatedOilTable):
    def __init__(
        self,
        pressure: Pressure,
        temperature: Temperature,
        viscosity: Viscosity,
        collection: Optional[CorrelationAggregator] = None,
    ) -> None:
        super().__init__(
            x_value=pressure.value,
            y_value=temperature.value,
            z_value=viscosity.value,
            collection=collection,
        )

    def calc(self, var: CorrelationVariable) -> Viscosity:
        results = self._get_value(
            x_value=var.pres.value,
            y_value=var.temp.value,
        )
        return Viscosity(results)
