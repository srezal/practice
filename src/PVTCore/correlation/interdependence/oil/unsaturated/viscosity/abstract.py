from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from PVTCore.correlation.abstract.param import ViscosityCorrelation
from PVTCore.correlation.abstract.phase import UnSaturatedOilCorrelation
from PVTCore.correlation.abstract.table import TwoDimensionalTableCorrelation

if TYPE_CHECKING:
    from PVTCore.correlation.abstract import CorrelationVariable


class ViscosityUnSaturatedOilCorrelation(ViscosityCorrelation, UnSaturatedOilCorrelation, ABC):
    def convert_to_thermal_black(self, var: "CorrelationVariable") -> ViscosityUnSaturatedOilTable:
        pass


class ViscosityUnSaturatedOilTable(
    TwoDimensionalTableCorrelation, ViscosityCorrelation, UnSaturatedOilCorrelation, ABC
):
    pass
