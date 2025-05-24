from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Optional

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from PVTCore.correlation.abstract.correlation import Correlation

if TYPE_CHECKING:
    from PVTCore.aggregator.entity.abstract import CorrelationAggregator


class TwoDimensionalTableCorrelation(Correlation, ABC):
    def __init__(
        self,
        x_value: np.ndarray,
        y_value: np.ndarray,
        z_value: np.ndarray,
        kind: str = "linear",
        collection: Optional[CorrelationAggregator] = None,
    ) -> None:
        self.model = RegularGridInterpolator(
            (y_value, x_value),
            z_value,
            method=kind,
        )
        super().__init__(collection)

    def _get_value(
        self,
        x_value: np.ndarray,
        y_value: np.ndarray,
    ) -> np.ndarray:
        try:
            return self.model((y_value, x_value))
        except ValueError as e:
            min_x, max_x = min(x_value), max(x_value)
            min_y, max_y = min(y_value), max(y_value)
            x_array, y_array = self.model.grid[1], self.model.grid[0]
            lower_x, upper_x = min(x_array), max(x_array)
            lower_y, upper_y = min(y_array), max(y_array)

            if min_x < lower_x:
                print(f"for x (press): min value: {min_x} < border: {lower_x}")
            if max_x > upper_x:
                print(f"for x (press): min value: {max_x} > border: {upper_x}")

            if min_y < lower_y:
                print(f"for y (temp): min value: {min_y} < border: {lower_y}")
            if max_y > upper_y:
                print(f"for y (temp): min value: {max_y} < border: {upper_y}")

            raise e
