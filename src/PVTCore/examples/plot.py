import units

import correlation
from aggregator import (
    DeadOilCorrelationAggregator,
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
    Settings,
    WatVariableCorrelation,
)
from ploter import OilParamPloter

aggregator = ModelCorrelationAggregator(
    wat=WatPhaseCorrelationAggregator(
        vis=correlation.wat.viscosity.FamousCorrelation.McCain.get(),
        fvf=correlation.wat.volume_factor.FamousCorrelation.McCain.get(),
    ),
    oil=OilPhaseCorrelationAggregator(
        dead=DeadOilCorrelationAggregator(
            vis=correlation.oil.dead.viscosity.FamousCorrelation.beggs.get()
        ),
        sat=SaturatedOilCorrelationAggregator(
            fvf=correlation.oil.saturated.volume_factor.FamousCorrelation.beggs.get(),
            vis=correlation.oil.saturated.viscosity.FamousCorrelation.beggs.get(),
            sol=correlation.oil.saturated.solubility.FamousCorrelation.Beggs.get(),
        ),
        unsat=UnSaturatedOilCorrelationAggregator(
            fvf=correlation.oil.unsaturated.volume_factor.FamousCorrelation.vasquez_beggs.get(),
            vis=correlation.oil.unsaturated.viscosity.FamousCorrelation.no_viscosibility.get(),
            bpp=correlation.oil.unsaturated.bubble_point_pressure.FamousCorrelation.beggs.get(),
        ),
        vis=correlation.interdependence.OilInContactWithGasViscosityCorrelation(),
        fvf=correlation.interdependence.OilInContactWithGasVolumeFactorCorrelation(),
    ),
    gas=GasPhaseCorrelationAggregator(
        visc=correlation.gas.saturated.viscosity.FamousCorrelation.lee.get(),
        dens=correlation.gas.saturated.volume_factor.FamousCorrelation.lee.get(),
    ),
    mixer=correlation.BlackOilModelMixer(),
    liq=LiquidCorrelationAggregator(
        visc=None,
        dens=None,
    ),
    mix=MixtureCorrelationAggregator(
        visc=None,
        dens=None,
    ),
)


var = CorrelationVariable(
    settings=Settings(
        thermal=True,
        model_type="Dead",
    ),
    pres=units.Pressure(
        value=100,
        unit=units.PresUnit.Bar,
    ),
    temp=units.Temperature(
        value=293,
        unit=units.TempUnit.Celsius,
    ),
    oil=OilVariableCorrelation(
        mass=units.Mass(
            value=10,
            unit=units.MassUnit.kg,
        ),
        dens=units.Density(
            value=800,
            unit=units.DensityUnit.kg_per_m3,
        ),
        solubility=units.Solubility(
            value=80,
            unit=units.SolubilityUnit.m3_per_m3,
        ),
        heat_capacity=4200,
        heat_conductivity=0.063,
    ),
    wat=WatVariableCorrelation(
        mass=units.Mass(
            value=10,
            unit=units.MassUnit.kg,
        ),
        dens=units.Density(
            value=1000,
            unit=units.DensityUnit.kg_per_m3,
        ),
        sali=0,
        heat_capacity=4200,
        heat_conductivity=0.063,
    ),
    gas=GasVariableCorrelation(
        mass=units.Mass(
            value=10,
            unit=units.MassUnit.kg,
        ),
        dens=units.Density(
            value=1,
            unit=units.DensityUnit.kg_per_m3,
            relative_coefficient=1.2754,
        ),
        # heat_capacity=,
        # heat_conductivity=,
    ),
)

plotter = OilParamPloter(
    max_press=units.Pressure(500, units.PresUnit.Bar),
    max_sol=units.Solubility(400, units.SolubilityUnit.m3_per_m3),
    min_temp=units.Temperature(20, units.TempUnit.Celsius),
    max_temp=units.Temperature(200, units.TempUnit.Celsius),
    pres_unit=units.PresUnit.Bar,
    fvf_unit=units.VolumeFactorUnit.si,
    vis_unit=units.ViscUnit.cP,
    sol_unit=units.SolubilityUnit.m3_per_m3,
)

plotter.plot_param(var, aggregator)
