from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from PVTCore.units import Viscosity

from PVTCore.correlation.abstract import Correlation

if TYPE_CHECKING:
    from correlation.abstract import CorrelationVariable


class ViscosityCorrelation(Correlation, ABC):
    @abstractmethod
    def calc(self, var: CorrelationVariable) -> Viscosity:
        pass
