from enum import StrEnum

from PVTCore.correlation.abstract.param import ViscosityCorrelation

from .lee import Lee


class FamousCorrelation(StrEnum):
    lee = "lee"

    def get(self) -> ViscosityCorrelation:
        data = {
            "lee": Lee,
        }
        return data[self.value]()
