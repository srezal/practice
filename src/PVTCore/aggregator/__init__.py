from .aggregator import ModelCorrelationAggregator
from .entity.gas import GasPhaseCorrelationAggregator
from .entity.liq import LiquidCorrelationAggregator
from .entity.mix import MixtureCorrelationAggregator
from .entity.oil import (
    DeadOilCorrelationAggregator,
    OilPhaseCorrelationAggregator,
    SaturatedOilCorrelationAggregator,
    UnSaturatedOilCorrelationAggregator,
)
from .entity.wat import WatPhaseCorrelationAggregator
