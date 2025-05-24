from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

from PVTCore.correlation.abstract.param import VolumeFactorCorrelation

from .vasquez_beggs_1980 import Beggs

if TYPE_CHECKING:
    pass


class FamousCorrelation(StrEnum):
    vasquez_beggs = "vasquez_beggs_1980"
    Table_thermal_dead = "table_thermal_dead"

    def get(self) -> VolumeFactorCorrelation:
        data = {
            "vasquez_beggs_1980": Beggs,
        }
        return data[self.value]()
