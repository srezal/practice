from typing import Optional

from pydantic import Field

from PVTCore.aggregator.entity.abstract import CorrelationAggregator
from PVTCore.correlation.abstract.param import ViscosityCorrelation, VolumeFactorCorrelation


class LiquidCorrelationAggregator(CorrelationAggregator):
    visc: Optional[ViscosityCorrelation] = Field(default=None)  # TODO убрать Optional
    dens: Optional[VolumeFactorCorrelation] = Field(default=None)  # TODO убрать Optional

    """
    def __init__(
        self,
        wat: WatPhaseCorrelationAggregator,
        oil: OilPhaseCorrelationAggregator,
    ) -> None:
        self.wat = wat
        self.oil = oil

    def calc_viscosity(
        self,
        normal_condition_value: NormalVolume,
        pres: Union[float, int],
        temp: Union[float, int],
    ) -> Union[float, int]:
        oil_visc = self.oil.calc_viscosity(normal_condition_value, pres, temp)
        wat_visc = self.wat.calc_viscosity(normal_condition_value, pres, temp)
        wct = normal_condition_value.wct
        return oil_visc * (1 - wct) + wat_visc * wct

    def calc_density(
        self,
        normal_condition_value: NormalVolume,
        pres: Union[float, int],
        temp: Union[float, int],
    ) -> Union[float, int]:
        oil_dens = self.oil.calc_density(normal_condition_value, pres, temp)
        wat_dens = self.wat.calc_density(normal_condition_value, pres, temp)
        wct = normal_condition_value.wct
        return oil_dens * (1 - wct) + wat_dens * wct

    def calc_value(
        self,
        normal_condition_value: NormalVolume,
        pres: Union[float, int],
        temp: Union[float, int],
    ) -> Union[float, int]:
        oil_dens = self.oil.calc_value(normal_condition_value, pres, temp)
        wat_dens = self.wat.calc_value(normal_condition_value, pres, temp)
        return oil_dens + wat_dens

    def wct(
        self,
        normal_condition_value: NormalVolume,
        pres: Union[float, int],
        temp: Union[float, int],
    ) -> Union[float, int]:
        oil_vol = self.oil.calc_value(normal_condition_value, pres, temp)
        wat_vol = self.wat.calc_value(normal_condition_value, pres, temp)
        return wat_vol / (oil_vol + wat_vol)
    """
