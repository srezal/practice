from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from PVTCore.aggregator.entity.oil.dead import DeadOilCorrelationAggregator
from PVTCore.aggregator.entity.oil.saturated import SaturatedOilCorrelationAggregator
from PVTCore.aggregator.entity.oil.unsatuarated import UnSaturatedOilCorrelationAggregator
from PVTCore.correlation.interdependence.oil_gas_mix import (
    OilInContactWithGasSolubilityCorrelation,
    OilInContactWithGasViscosityCorrelation,
    OilInContactWithGasVolumeFactorCorrelation,
)

if TYPE_CHECKING:
    from PVTCore.aggregator.aggregator import ModelCorrelationAggregator


class OilPhaseCorrelationAggregator:
    _aggregator: ModelCorrelationAggregator

    def __init__(
        self,
        dead: Optional[DeadOilCorrelationAggregator] = None,
        sat: Optional[SaturatedOilCorrelationAggregator] = None,
        unsat: Optional[UnSaturatedOilCorrelationAggregator] = None,
        vis: Optional[OilInContactWithGasViscosityCorrelation] = None,
        fvf: Optional[OilInContactWithGasVolumeFactorCorrelation] = None,
        sol: Optional[OilInContactWithGasSolubilityCorrelation] = None,
    ):
        self.dead = DeadOilCorrelationAggregator() if dead is None else dead
        self.sat = SaturatedOilCorrelationAggregator() if sat is None else sat
        self.unsat = UnSaturatedOilCorrelationAggregator() if unsat is None else unsat
        self.vis = OilInContactWithGasViscosityCorrelation() if vis is None else vis
        self.fvf = OilInContactWithGasVolumeFactorCorrelation() if fvf is None else fvf
        self.sol = OilInContactWithGasSolubilityCorrelation() if sol is None else sol

    def __setattr__(self, key: str, value: object) -> None:
        if isinstance(
            value,
            (
                DeadOilCorrelationAggregator,
                SaturatedOilCorrelationAggregator,
                UnSaturatedOilCorrelationAggregator,
                OilInContactWithGasViscosityCorrelation,
                OilInContactWithGasVolumeFactorCorrelation,
            ),
        ):
            setattr(value, "_oil_model", self)

        super().__setattr__(key, value)
