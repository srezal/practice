from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

from PVTCore.correlation.abstract.param import ViscosityCorrelation

from .no_viscosibility import NoViscosibility

if TYPE_CHECKING:
    pass


class FamousCorrelation(StrEnum):
    no_viscosibility = "no_viscosibility"
    Table_thermal_dead = "table_thermal_dead"

    def get(self) -> ViscosityCorrelation:
        data = {
            "no_viscosibility": NoViscosibility,
        }
        return data[self.value]()
