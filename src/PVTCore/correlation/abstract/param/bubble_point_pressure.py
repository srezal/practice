from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from PVTCore.units import Pressure

from PVTCore.correlation import CorrelationVariable
from PVTCore.correlation.abstract import Correlation

if TYPE_CHECKING:
    from aggregator.entity.oil import UnSaturatedOilCorrelationAggregator


class BubblePointPressureCorrelation(Correlation, ABC):
    _collection: "UnSaturatedOilCorrelationAggregator"

    @abstractmethod
    def calc(self, var: CorrelationVariable) -> Pressure:
        pass
