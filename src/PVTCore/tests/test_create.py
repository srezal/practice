from units import (
    Density,
    DensityUnit,
    Mass,
    MassUnit,
    Pressure,
    PresUnit,
    Solubility,
    SolubilityUnit,
    Temperature,
    TempUnit,
)

import correlation
from aggregator import (
    GasPhaseCorrelationAggregator,
    LiquidCorrelationAggregator,
    MixtureCorrelationAggregator,
    ModelCorrelationAggregator,
    OilPhaseCorrelationAggregator,
    SaturatedOilCorrelationAggregator,
    UnSaturatedOilCorrelationAggregator,
    WatPhaseCorrelationAggregator,
)
from correlation.abstract import (
    CorrelationVariable,
    GasVariableCorrelation,
    OilVariableCorrelation,
    WatVariableCorrelation,
)


def test_create_aggregator():
    ModelCorrelationAggregator(
        wat=WatPhaseCorrelationAggregator(
            vis=correlation.wat.viscosity.FamousCorrelation.McCain.get(),
            fvf=correlation.wat.volume_factor.FamousCorrelation.McCain.get(),
        ),
        oil=OilPhaseCorrelationAggregator(
            sat=SaturatedOilCorrelationAggregator(
                fvf=correlation.oil.saturated.volume_factor.FamousCorrelation.beggs.get(),
                dvis=correlation.oil.dead.viscosity.FamousCorrelation.beggs.get(),
                lvis=correlation.oil.saturated.viscosity.FamousCorrelation.beggs.get(),
                sol=correlation.oil.saturated.solubility.FamousCorrelation.Beggs.get(),
            ),
            unsut=UnSaturatedOilCorrelationAggregator(
                fvf=correlation.oil.unsaturated.volume_factor.FamousCorrelation.vasquez_beggs.get(),
                vis=correlation.oil.unsaturated.viscosity.FamousCorrelation.no_viscosibility.get(),
                bpp=correlation.oil.unsaturated.bubble_point_pressure.FamousCorrelation.beggs.get(),
            ),
        ),
        gas=GasPhaseCorrelationAggregator(
            visc=correlation.gas.saturated.viscosity.FamousCorrelation.lee.get(),
            dens=correlation.gas.saturated.volume_factor.FamousCorrelation.lee.get(),
        ),
        liq=LiquidCorrelationAggregator(
            visc=None,
            dens=None,
        ),
        mix=MixtureCorrelationAggregator(
            visc=None,
            dens=None,
        ),
    )


def test_create_empty_aggregator():
    ModelCorrelationAggregator()


def test_create_correlation_variable():
    CorrelationVariable(
        pres=Pressure(
            value=100,
            unit=PresUnit.Bar,
        ),
        temp=Temperature(value=293, unit=TempUnit.Celsius),
        oil=OilVariableCorrelation(
            mass=Mass(
                value=10,
                unit=MassUnit.kg,
            ),
            dens=Density(
                value=800,
                unit=DensityUnit.kg_per_m3,
            ),
            solubility=Solubility(
                value=80,
                unit=SolubilityUnit.m3_per_m3,
            ),
            heat_capacity=4200,
            heat_conductivity=0.063,
        ),
        wat=WatVariableCorrelation(
            mass=Mass(
                value=10,
                unit=MassUnit.kg,
            ),
            dens=Density(
                value=1000,
                unit=DensityUnit.kg_per_m3,
            ),
            sali=0,
            heat_capacity=4200,
            heat_conductivity=0.063,
        ),
        gas=GasVariableCorrelation(
            mass=Mass(
                value=10,
                unit=MassUnit.kg,
            ),
            dens=Density(
                value=1,
                unit=DensityUnit.kg_per_m3,
                relative_coefficient=1.2754,
            ),
            # heat_capacity=,
            # heat_conductivity=,
        ),
    )
