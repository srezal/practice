from enum import StrEnum

from PVTCore.correlation.abstract.param import ViscosityCorrelation

from .beggs import Beggs


class FamousCorrelation(StrEnum):
    Beggs = "Beggs"
    Table_thermal_dead = "Table_thermal_dead"

    def get(self) -> ViscosityCorrelation:
        data = {
            "Beggs": Beggs,
        }
        return data[self.value]()
