from __future__ import annotations

from typing import TYPE_CHECKING

from PVTCore.aggregator import entity
from PVTCore.correlation import BlackOilModelMixer

if TYPE_CHECKING:
    from typing import Optional


class ModelCorrelationAggregator:
    def __init__(
        self,
        wat: Optional[entity.WatPhaseCorrelationAggregator] = None,
        oil: Optional[entity.OilPhaseCorrelationAggregator] = None,
        gas: Optional[entity.GasPhaseCorrelationAggregator] = None,
        liq: Optional[entity.LiquidCorrelationAggregator] = None,
        mix: Optional[entity.MixtureCorrelationAggregator] = None,
        comp: Optional[entity.ComponentAggregator] = None,
        mixer: Optional[BlackOilModelMixer] = None,
    ) -> None:
        self.wat = wat if wat else entity.WatPhaseCorrelationAggregator()
        self.oil = oil if oil else entity.OilPhaseCorrelationAggregator()
        self.gas = gas if gas else entity.GasPhaseCorrelationAggregator()
        self.liq = liq if liq else entity.LiquidCorrelationAggregator()
        self.mix = mix if mix else entity.MixtureCorrelationAggregator()
        self.comp = comp if comp else entity.ComponentAggregator()
        self.mixer = mixer if mixer else BlackOilModelMixer()

    def __setattr__(self, key: str, value: object) -> None:
        if isinstance(
            value,
            (
                entity.GasPhaseCorrelationAggregator,
                entity.LiquidCorrelationAggregator,
                entity.MixtureCorrelationAggregator,
                entity.OilPhaseCorrelationAggregator,
                entity.WatPhaseCorrelationAggregator,
                BlackOilModelMixer,
            ),
        ):
            setattr(value, "_aggregator", self)
        super().__setattr__(key, value)
