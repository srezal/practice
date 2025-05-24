from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from PVTCore.correlation.abstract import Correlation

if TYPE_CHECKING:
    from units import Solubility

    import aggregator
    from correlation.abstract.variable import CorrelationVariable


class SolubilityCorrelation(Correlation, ABC):
    _collection: aggregator.entity.oil.saturated.SaturatedOilCorrelationAggregator

    def calc(self, var: CorrelationVariable) -> Solubility:
        pass
