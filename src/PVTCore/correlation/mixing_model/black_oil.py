from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

import numpy as np
from PVTCore.units import Solubility

if TYPE_CHECKING:
    from PVTCore.aggregator.aggregator import ModelCorrelationAggregator
    from PVTCore.correlation.abstract import CorrelationVariable


class BlackOilModelMixer:
    _aggregator: ModelCorrelationAggregator

    def calc(self, var: CorrelationVariable) -> Tuple[np.ndarray, Solubility]:
        solubility = self._aggregator.oil.sat.sol.calc(var)
        gor = var.gas_oil_ratio

        is_saturated = solubility.m3_per_m3() < gor.m3_per_m3()
        dissolved = solubility
        dissolved.value[~is_saturated] = gor.value
        return is_saturated, dissolved
