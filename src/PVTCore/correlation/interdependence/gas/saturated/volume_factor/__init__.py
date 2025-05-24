from enum import StrEnum

from PVTCore.correlation.abstract.param import VolumeFactorCorrelation

from .lee import Lee


class FamousCorrelation(StrEnum):
    lee = "lee"

    def get(self) -> VolumeFactorCorrelation:
        data = {
            "lee": Lee,
        }
        return data[self.value]()
