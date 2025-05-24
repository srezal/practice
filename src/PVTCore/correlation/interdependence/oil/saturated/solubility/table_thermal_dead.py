from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from PVTCore.correlation.abstract import CorrelationVariable
from PVTCore.correlation.abstract.param import SolubilityCorrelation
from PVTCore.correlation.abstract.phase import SaturatedOilCorrelation
from PVTCore.correlation.abstract.table import ZeroDimensionalTableCorrelation

if TYPE_CHECKING:

    from units import Solubility

    from aggregator.entity.abstract import CorrelationAggregator


class ThermalDeadOilSolubilityTable(
    ZeroDimensionalTableCorrelation,
    SolubilityCorrelation,
    SaturatedOilCorrelation,
):
    def __init__(
        self,
        solubility: Solubility,
        collection: Optional[CorrelationAggregator] = None,
    ) -> None:
        super().__init__(solubility.value, collection)

    def calc(self, var: CorrelationVariable) -> Solubility:
        results = self._get_value(var.pres.value)
        return Solubility(results)
