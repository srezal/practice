import math
from typing import TYPE_CHECKING

from PVTCore.correlation.abstract.param import ViscosityCorrelation

if TYPE_CHECKING:
    from PVTCore.correlation.abstract import CorrelationVariable


class Lee(ViscosityCorrelation):
    K1 = 2.57
    K2 = 1914.5
    K3 = 1.8
    K4 = 0.275
    K5 = 1.11
    K6 = 0.04

    def calc(self, var: "CorrelationVariable") -> object:
        """
        :units temp: Температура, K
        :units dens_gas_standard: Плотность дгазированной газа, доли ед.
        :units dens_gas: Приведенная плотность газа в стандартных условиях, доли ед.
        :units volume_factor: газосодержание, м3 / м3
        :return:
        """
        # TODO проверить и доделать корреляцию

        temp = var.temp.get('Kelvin')
        solubility = var.oil.solubility.get('м3/м3')
        dens_gas_standard = var.gas.dens.get('kg_per_m3')
        dens_gas = var.gas.dens.get('kg_per_m3')

        exp_mult = self.K1 + self.K2 / self.K3 / temp + self.K4 * dens_gas_standard
        degree = solubility * (dens_gas / 1000) ** self.K5 + self.K6 * exp_mult
        multiplier1 = 10**-4 * (7.77 + 0.183 * dens_gas_standard)
        multiplier2 = (1.8 * temp) ** 1.5
        denomenator = 122.4 + 373.6 * dens_gas_standard + 1.8 * temp
        multiplier = multiplier1 * multiplier2 / denomenator
        return multiplier * math.exp(exp_mult * degree)
