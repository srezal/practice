from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from aggregator.entity.abstract import CorrelationAggregator
    from correlation.abstract.variable import CorrelationVariable


class Correlation(ABC):
    _collection: CorrelationAggregator

    @abstractmethod
    def calc(self, var: CorrelationVariable) -> object:
        pass
