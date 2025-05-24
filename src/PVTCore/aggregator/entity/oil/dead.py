from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

import PVTCore.correlation as correlation
from PVTCore.aggregator.entity.abstract import CorrelationAggregator
from PVTCore.correlation.abstract.param import ViscosityCorrelation

if TYPE_CHECKING:
    from PVTCore.aggregator.aggregator import ModelCorrelationAggregator
    from PVTCore.aggregator.entity.oil.model import OilPhaseCorrelationAggregator


class DeadOilCorrelationAggregator(CorrelationAggregator):
    _oil_model: OilPhaseCorrelationAggregator

    vis: ViscosityCorrelation = Field(
        title="",
        alias="vis",
        default=correlation.oil.dead.viscosity.FamousCorrelation.beggs.get(),
    )

    @property
    def _aggregator(self) -> ModelCorrelationAggregator:
        return self._oil_model._aggregator
