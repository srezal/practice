from __future__ import annotations

from typing import TYPE_CHECKING, Union, Self, Optional, Iterable, Literal
from enum import StrEnum
import numpy as np

from abc import ABC, abstractmethod

if TYPE_CHECKING:
    pass


class AbstractUnit(StrEnum):

    @classmethod
    def from_string(cls, value: str) -> Self:
        for v in cls:
            if v.value == value:
                return v

        raise ValueError()


class AbstractParam(ABC):
    value: np.ndarray

    @abstractmethod
    def __init__(
        self,
        value: Union[np.ndarray, int, float],
        unit: AbstractUnit = None,
    ):
        pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        original_init = cls.__init__

        def new_init(
            self,
            *args,
            **kwargs,
        ):
            if len(args) > 0:
                value = args[0]
            else:
                value = kwargs["value"]

            if not isinstance(value, np.ndarray):
                value = np.array([value])

            if len(args) > 0:
                args = (value, *args[1:])
            else:
                kwargs["value"] = value

            original_init(self, *args, **kwargs)

        cls.__init__ = new_init

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.value.__repr__()}"

    @staticmethod
    @abstractmethod
    def default_unit() -> AbstractUnit:
        pass

    @abstractmethod
    def get(self, unit: Union[AbstractUnit, str]) -> Union[np.ndarray, int, float]:
        pass

    @classmethod
    def create(
        cls,
        start: Union[float, AbstractParam],
        stop: Union[float, AbstractParam],
        step: Optional[float] = None,
        num: Optional[int] = None,
        unit: Optional[AbstractUnit] = None,
    ) -> Self:

        if isinstance(start, AbstractParam):
            start = start.value[0]
        else:
            start = cls(start, unit).value[0]

        if isinstance(stop, AbstractParam):
            stop = stop.value[0]
        else:
            stop = cls(stop, unit).value[0]

        if (step is not None and num is not None) or (step is None and num is None):
            raise ValueError("необходимо задать step или num")
        elif step is not None:
            value = np.arange(start, stop, step)
        elif num is not None:
            value = np.linspace(start, stop, num=num)
        else:
            raise ValueError("Неизвестная ошибка при исполнении функции generate")

        return cls(value=value, unit=cls.default_unit())

    @classmethod
    def generate(
        cls,
        start: Union[float, AbstractParam],
        stop: Union[float, AbstractParam],
        step: Optional[float] = None,
        num: Optional[int] = None,
        unit: Optional[AbstractUnit] = None,
    ) -> Iterable[Self]:

        if isinstance(start, AbstractParam):
            start = start.value[0]
        else:
            start = cls(start, unit).value[0]

        if isinstance(stop, AbstractParam):
            stop = stop.value[0]
        else:
            stop = cls(stop, unit).value[0]

        if (step is not None and num is not None) or (step is None and num is None):
            raise ValueError("необходимо задать step или num")
        elif step is not None:
            value = np.arange(start, stop, step)
        elif num is not None:
            value = np.linspace(start, stop, num=num)
        else:
            raise ValueError("Неизвестная ошибка при исполнении функции generate")

        for v in value:
            results = cls(
                value=v,
                unit=cls.default_unit(),
            )
            yield results

    def cut(
        self,
        value: AbstractParam,
        direction: Literal["more", "less"] = "less",
        method: Literal["in", "out"] = "in",
    ) -> Self:
        if direction == "more":
            mask = self.value > value.value
        elif direction == "less":
            mask = self.value < value.value
        else:
            raise ValueError("Неизвестный direction для cut из AbstractParam")

        new_value = self.value[mask]
        if method == "in" and direction == "less":
            new_value = np.concatenate((new_value, value.value))
        elif method == "in" and direction == "more":
            new_value = np.concatenate((value.value, new_value))
        elif method == "out":
            new_value = new_value
        else:
            raise ValueError("Неизвестный method для cut из AbstractParam")

        results = self.__class__(new_value, self.default_unit())
        return results
