from __future__ import annotations

from typing import Optional

from pydantic import Field

import PVTCore.correlation as correlation
from PVTCore.aggregator.entity.abstract import PhaseCorrelationAggregator
from PVTCore.correlation.abstract.param import ViscosityCorrelation, VolumeFactorCorrelation


class GasPhaseCorrelationAggregator(PhaseCorrelationAggregator):
    visc: Optional[ViscosityCorrelation] = Field(
        title="",
        default=correlation.gas.saturated.viscosity.FamousCorrelation.lee.get(),
    )
    dens: Optional[VolumeFactorCorrelation] = Field(
        title="",
        default=correlation.gas.saturated.viscosity.FamousCorrelation.lee.get(),
    )
