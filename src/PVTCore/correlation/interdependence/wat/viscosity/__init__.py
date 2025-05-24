from enum import StrEnum

from PVTCore.correlation.abstract.param.viscosity import ViscosityCorrelation

from .likhachev import Likhachev
from .mccain import McCain


class FamousCorrelation(StrEnum):
    McCain = "McCain"
    Likhachev = "Likhachev"

    def get(self) -> ViscosityCorrelation:
        data = {
            "McCain": McCain,
            "Likhachev": Likhachev,
        }
        return data[self.value]()
