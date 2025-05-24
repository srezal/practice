from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aggregator.aggregator import ModelCorrelationAggregator


class ComponentAggregator:
    _aggregator: ModelCorrelationAggregator
