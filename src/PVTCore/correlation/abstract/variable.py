from __future__ import annotations

from abc import ABC
from copy import deepcopy
from typing import Literal, Union

import numpy as np
import PVTCore.units as units
from pydantic import BaseModel, Field


class PhaseVariableCorrelation(BaseModel, ABC):
    _var: CorrelationVariable

    mass: units.Mass = Field(
        title="Масса фазы, при полном отделении компонентов друг от друга",
    )
    dens: units.Density = Field(
        title="Плотность фазы",
    )
    heat_capacity: Union[float, int] = Field(
        title="Теплоемкость фазы",
        default=4200,
    )
    heat_conductivity: Union[float, int] = Field(
        title="",
        default=0.603,
    )

    class Config:
        arbitrary_types_allowed = True

    @property
    def volume(self) -> units.Volume:
        """Oбъем в стандартных условиях"""
        results = units.Volume(
            value=self.mass.kg() / self.dens.kg_per_m3(),
            unit=units.VolumeUnit.m3,
        )
        return results


class WatVariableCorrelation(PhaseVariableCorrelation):
    mass: units.Mass = Field(
        title="Масса воды",
    )
    dens: units.Density = Field(
        title="Плотность фазы",
        default=units.Density(
            value=1000,
            unit=units.DensityUnit.kg_per_m3,
        ),
    )
    sali: Union[np.ndarray, int, float, None] = (
        Field(
            title="Соленость воды",
            default=None,
        ),
    )


class OilVariableCorrelation(PhaseVariableCorrelation):

    mass: units.Mass = Field(
        title="Масса дегазированной нефти",
    )

    solubility: units.Solubility = Field(
        title="Гахосодержание"
    )


class GasVariableCorrelation(PhaseVariableCorrelation):

    mass: units.Mass = Field(
        title="Масса сухого газа",
    )


class Settings(BaseModel):

    thermal: bool = Field(
        title="Флаг указывающий, является ли модель термической",
        default=True,
    )
    model_type: Literal["Dead", "Black", "Volatile"] = Field(
        title="Поле указывающие тип модели",
        default="Black",
    )


class CorrelationVariable(BaseModel):

    pres: units.Pressure = Field(
        title="Давление для которого будет осуществлен расчет",
    )
    temp: units.Temperature = Field(
        title="Температура для которого будет осуществлен расчет",
    )
    oil: OilVariableCorrelation = Field(
        title="Параметры относящиеся к нефтяной фазе",
    )
    wat: WatVariableCorrelation = Field(
        title="Параметры относящиеся к водной фазе",
    )
    gas: GasVariableCorrelation = Field(
        title="Параметры относящиеся к газовой фазе",
    )
    settings: Settings = Field(title="Настройки расчета")

    class Config:
        arbitrary_types_allowed = True

    def __setattr__(self, key, value) -> None:
        if isinstance(value, PhaseVariableCorrelation):
            value._var = self
        super().__setattr__(key, value)

    @property
    def gas_oil_ratio(self) -> units.Solubility:
        """"""
        results = units.Solubility(
            value=self.gas.volume.m3() / self.oil.volume.m3(),
            unit=units.SolubilityUnit.m3_per_m3,
        )
        return results

    def set_gas_oil_ratio(self, value: units.Solubility) -> None:
        gas_volume = value.m3_per_m3() * self.oil.volume.m3()
        self.gas.mass = units.Mass(
            value=gas_volume * self.gas.dens.kg_per_m3(),
            unit=units.MassUnit.kg,
        )

    def convert_to_thermal_black_matrix(self) -> CorrelationVariable:
        new = deepcopy(self)
        new.pres.value, new.temp.value = np.meshgrid(self.pres.value, self.temp.value)
        return new

    @classmethod
    def create(
        cls,
        max_pres: Union[float, int],
        min_pres: Union[float, int],
        step_pres: Union[float, int],
        max_temp: Union[float, int],
        min_temp: Union[float, int],
        step_temp: Union[float, int],
        oil_dens: Union[float, int],
        gas_dens: Union[float, int],
        solubility: Union[float, int],
        oil_heat_capacity: Union[float, int],
        oil_heat_conductivity: Union[float, int],
        wat_dens: Union[float, int] = 1000,
        wat_salinity: Union[float, int] = 0,
        wat_heat_capacity: Union[float, int] = 4200,
        wat_heat_conductivity: Union[float, int] = 0.603,
    ):
        pres, temp = np.meshgrid(
            np.linspace(min_pres, max_pres, (max_pres - min_pres) // step_pres),
            np.linspace(min_temp, max_temp, (max_temp - min_temp) // step_temp),
        )

        results = cls(
            pres=units.Pressure(
                value=pres,
                unit=units.PresUnit.Bar,
            ),
            temp=units.Temperature(value=temp, unit=units.TempUnit.Celsius),
            oil=OilVariableCorrelation(
                dens=units.Density(
                    value=oil_dens,
                    unit=units.DensityUnit.kg_per_m3,
                ),
                solubility=units.Solubility(
                    value=solubility,
                    unit=units.SolubilityUnit.m3_per_m3,
                ),
                heat_capacity=oil_heat_capacity,
                heat_conductivity=oil_heat_conductivity,
            ),
            wat=WatVariableCorrelation(
                dens=units.Density(
                    value=wat_dens,
                    unit=units.DensityUnit.kg_per_m3,
                ),
                sali=wat_salinity,
                heat_capacity=wat_heat_capacity,
                heat_conductivity=wat_heat_conductivity,
            ),
            gas=GasVariableCorrelation(
                dens=units.Density(
                    value=gas_dens,
                    unit=units.DensityUnit.kg_per_m3,
                    relative_coefficient=1.2754,
                ),
                # heat_capacity=,
                # heat_conductivity=,
            ),
        )
        return results
