from abc import ABC
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

from PVTCore.correlation.abstract import Correlation

if TYPE_CHECKING:
    pass


class CorrelationAggregator(BaseModel, ABC):
    class Config:
        arbitrary_types_allowed = True

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        for key, value in self:
            if isinstance(value, Correlation):
                setattr(value, "_collection", self)

    def __setattr__(
        self,
        key: str,
        value: object,
    ) -> None:

        if isinstance(value, Correlation):
            value._collection = self
        super().__setattr__(key, value)


class PhaseCorrelationAggregator(CorrelationAggregator, ABC):
    pass
