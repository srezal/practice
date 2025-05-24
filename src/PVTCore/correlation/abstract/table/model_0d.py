from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Optional

import numpy as np

from PVTCore.correlation.abstract.correlation import Correlation

if TYPE_CHECKING:
    from PVTCore.aggregator.entity.abstract import CorrelationAggregator


class ZeroDimensionalTableCorrelation(Correlation, ABC):
    def __init__(
        self,
        value: float,
        collection: Optional[CorrelationAggregator] = None,
    ) -> None:
        self.value = value
        super().__init__(collection)

    def _get_value(self, x_value: np.ndarray) -> np.ndarray:
        value = np.ones(x_value.shape)
        return value * self.value
