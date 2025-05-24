from enum import StrEnum

from PVTCore.correlation.abstract.param import ViscosityCorrelation

from .beggs_robinson_1975 import DeadBeggs


class FamousCorrelation(StrEnum):
    beggs = "beggs_robinson_1975"

    def get(self) -> ViscosityCorrelation:
        data = {
            "beggs_robinson_1975": DeadBeggs,
        }
        return data[self.value]()
