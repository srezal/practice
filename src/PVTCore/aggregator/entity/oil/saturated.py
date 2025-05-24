from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

import PVTCore.correlation as correlation
from PVTCore.aggregator.entity.abstract import CorrelationAggregator
from PVTCore.correlation.abstract.param import (
    SolubilityCorrelation,
    ViscosityCorrelation,
    VolumeFactorCorrelation,
)

if TYPE_CHECKING:
    from PVTCore.aggregator.aggregator import ModelCorrelationAggregator
    from PVTCore.aggregator.entity.oil.model import OilPhaseCorrelationAggregator


class SaturatedOilCorrelationAggregator(CorrelationAggregator):
    _oil_model: OilPhaseCorrelationAggregator

    fvf: VolumeFactorCorrelation = Field(
        title="",
        alias="fvf",
        default=correlation.oil.saturated.volume_factor.FamousCorrelation.beggs.get(),
    )
    vis: ViscosityCorrelation = Field(
        title="",
        alias="vis",
        default=correlation.oil.saturated.viscosity.FamousCorrelation.beggs.get(),
    )
    sol: SolubilityCorrelation = Field(
        title="",
        alias="sol",
        default=correlation.oil.saturated.solubility.FamousCorrelation.Beggs.get(),
    )

    @property
    def _aggregator(self) -> ModelCorrelationAggregator:
        return self._oil_model._aggregator
