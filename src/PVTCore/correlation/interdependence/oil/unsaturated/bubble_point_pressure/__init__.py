from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

from PVTCore.correlation.abstract.param.bubble_point_pressure import BubblePointPressureCorrelation

from .beggs import Beggs

if TYPE_CHECKING:
    pass


class FamousCorrelation(StrEnum):
    beggs = "beggs_robinson_1975"

    def get(self) -> BubblePointPressureCorrelation:
        data = {
            "beggs_robinson_1975": Beggs,
        }
        return data[self.value]()
