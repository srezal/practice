from __future__ import annotations

from pydantic import Field

import PVTCore.correlation as correlation
from PVTCore.aggregator.entity.abstract import CorrelationAggregator
from PVTCore.correlation.abstract.param import ViscosityCorrelation, VolumeFactorCorrelation


class WatPhaseCorrelationAggregator(CorrelationAggregator):
    vis: ViscosityCorrelation = Field(
        title="",
        default=correlation.wat.viscosity.FamousCorrelation.McCain.get(),
    )
    fvf: VolumeFactorCorrelation = Field(
        title="",
        default=correlation.wat.viscosity.FamousCorrelation.McCain.get(),
    )

    """
    def __init__(
        self,
        visc: Optional[wat.viscosity.FamousCorrelation] = None,
        dens: Optional[wat.volume_factor.FamousCorrelation] = None,
    ) -> None:
        if not visc:
            visc = wat.viscosity.FamousCorrelation.McCain

        if not dens:
            dens = wat.volume_factor.FamousCorrelation.McCain
    """
