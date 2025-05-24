from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from PVTCore.correlation.abstract.param import VolumeFactorCorrelation
from PVTCore.correlation.abstract.phase import GasCorrelation

if TYPE_CHECKING:
    from PVTCore.units import VolumeFactor

    from PVTCore.correlation.abstract import CorrelationVariable


class Lee(VolumeFactorCorrelation, GasCorrelation):
    FVF_k1 = 350.958

    def calc(self, var: "CorrelationVariable") -> VolumeFactor:
        """
        :units temp: Температуры, К
        :units pres: Давления, Па
        :units supercompressibility: Коэффицент сверхсжимаемости
        :return: Объемный коэфицент м3 / м3
        """

        temp_k = var.temp.get('Kelvin')
        pres_pa = var.pres.get('Pascal')
        z_factor = 1
        
        if isinstance(pres_pa, (int, float)) and pres_pa == 0:
            raise ValueError("Давление не может быть нулевым")
        elif isinstance(pres_pa, np.ndarray):
            pres_pa = np.where(pres_pa == 0, np.nan, pres_pa)
        
        return self.FVF_k1 * z_factor * temp_k / pres_pa
        
