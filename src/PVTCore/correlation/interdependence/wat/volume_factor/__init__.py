from enum import StrEnum

from PVTCore.correlation.abstract.param.volume_factor import VolumeFactorCorrelation

from .mccain import McCain


class FamousCorrelation(StrEnum):
    McCain = "McCain"
    Likhachev = "Likhachev"

    def get(self) -> VolumeFactorCorrelation:
        data = {
            "McCain": McCain,
        }
        return data[self.value]()
