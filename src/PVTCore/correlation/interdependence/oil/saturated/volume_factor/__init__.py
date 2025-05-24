from enum import StrEnum

from PVTCore.correlation.abstract.param import ViscosityCorrelation

from .beggs import Beggs


class FamousCorrelation(StrEnum):
    beggs = "Beggs"

    def get(self) -> ViscosityCorrelation:
        data = {
            "Beggs": Beggs,
        }
        return data[self.value]()
