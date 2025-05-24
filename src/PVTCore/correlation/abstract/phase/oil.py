from __future__ import annotations

from abc import ABC

from PVTCore.correlation.abstract import Correlation


class DeadOilCorrelation(Correlation, ABC):
    pass


class UnSaturatedOilCorrelation(Correlation, ABC):
    pass


class SaturatedOilCorrelation(Correlation, ABC):
    pass
