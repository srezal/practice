from __future__ import annotations

from typing import TYPE_CHECKING

from correlation.abstract.param import VolumeFactorCorrelation
from correlation.abstract.phase import GasCorrelation

if TYPE_CHECKING:
    from units import VolumeFactor

    from correlation.abstract import CorrelationVariable


class Lee(VolumeFactorCorrelation, GasCorrelation):
    FVF_k1 = 350.958

    def calc(self, var: "CorrelationVariable") -> VolumeFactor:
        pass
        """
        :units temp: Температуры, К
        :units pres: Давления, Па
        :units supercompressibility: Коэффицент сверхсжимаемости
        :return: Объемный коэфицент м3 / м3
        """

        # value = self.FVF_k1 * supercompressibility * temp / pres
        # return value
        raise NotImplementedError
