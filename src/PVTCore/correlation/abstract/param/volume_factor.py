from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from PVTCore.correlation.abstract import Correlation

if TYPE_CHECKING:
    from units import VolumeFactor

    from correlation.abstract import CorrelationVariable


class VolumeFactorCorrelation(Correlation, ABC):
    @abstractmethod
    def calc(self, var: CorrelationVariable) -> VolumeFactor:
        pass
