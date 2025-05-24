from enum import StrEnum

from PVTCore.correlation.abstract.param import ViscosityCorrelation

from .beggs_robinson_1975 import LiveBeggs


class FamousCorrelation(StrEnum):
    beggs = "beggs_robinson_1975"

    def get(self) -> ViscosityCorrelation:
        data = {
            "beggs_robinson_1975": LiveBeggs,
        }
        return data[self.value]()
