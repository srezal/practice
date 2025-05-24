from typing import Optional

from pydantic import Field

from PVTCore.aggregator.entity.abstract import CorrelationAggregator
from PVTCore.correlation.abstract.param import ViscosityCorrelation, VolumeFactorCorrelation


class MixtureCorrelationAggregator(CorrelationAggregator):
    visc: Optional[ViscosityCorrelation] = Field(default=None)  # TODO убрать Optional
    dens: Optional[VolumeFactorCorrelation] = Field(default=None)  # TODO убрать Optional

    """
    def __init__(
        self,
        liq: LiquidCorrelationAggregator,
        gas: GasPhaseCorrelationAggregator,
    ) -> None:
        self.liq = liq
        self.gas = gas

    def calc_viscosity(
        self,
        normal_condition_value: NormalVolume,
        pres: Union[float, int],
        temp: Union[float, int],
    ):
        liq_visc = self.liq.calc_viscosity(normal_condition_value, pres, temp)
        gas_visc = self.gas.calc_viscosity(normal_condition_value, pres, temp)
        gf = self.gas_factor(normal_condition_value, pres, temp)
        return liq_visc * (1 - gf) + gas_visc * gf

    def calc_density(
        self,
        normal_condition_value: NormalVolume,
        pres: Union[float, int],
        temp: Union[float, int],
    ):
        liq_dens = self.liq.calc_density(normal_condition_value, pres, temp)
        gas_dens = self.gas.calc_density(normal_condition_value, pres, temp)
        gf = self.gas_factor(normal_condition_value, pres, temp)
        return liq_dens * (1 - gf) + gas_dens * gf

    def calc_value(
        self,
        normal_condition_value: NormalVolume,
        pres: Union[float, int],
        temp: Union[float, int],
    ) -> Union[float, int]:
        liq_vol = self.liq.calc_value(normal_condition_value, pres, temp)
        gas_vol = self.gas.calc_value(normal_condition_value, pres, temp)
        gf = self.gas_factor(normal_condition_value, pres, temp)
        return liq_vol * (1 - gf) + gas_vol * gf

    def gas_factor(
        self,
        normal_condition_value: NormalVolume,
        pres: Union[float, int],
        temp: Union[float, int],
    ) -> Union[float, int]:
        liq_volume = self.liq.calc_value(normal_condition_value, pres, temp)
        gas_volume = self.gas.calc_value(normal_condition_value, pres, temp)
        try:
            return gas_volume / (liq_volume + gas_volume)
        except ZeroDivisionError:
            return 0
"""
