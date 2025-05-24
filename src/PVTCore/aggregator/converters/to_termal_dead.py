from __future__ import annotations

from typing import TYPE_CHECKING

from api import Phase, PVTModel
from correlation.abstract import CorrelationVariable
from tables.thermal.black import model as tdo_model

if TYPE_CHECKING:
    from aggregator import ModelCorrelationAggregator


def get_wat_model(
    correlation_aggregator: ModelCorrelationAggregator,
    var: CorrelationVariable,
) -> Phase:
    vis = correlation_aggregator.wat.visc.calc(var)
    fvf = correlation_aggregator.wat.dens.calc(var)
    pres = var.pres.value[0, :] / 10**5
    temp = var.temp.value[:, 0]
    dens_visc = var.wat.density.kg_per_m3() / fvf / vis

    wat_phase = Phase(
        density=var.density,
        visc=tdo_model.Viscosity(pres, temp, vis),
        fvf=tdo_model.VolumeFactor(pres, temp, fvf),
        dens=tdo_model.Denisty(),
        expected_dens=tdo_model.ExpectedDensity(pres, temp, var.density * fvf**-1),
        dens_visc=tdo_model.DensVisc(pres, temp, dens_visc),
        hcap=tdo_model.HeatCapacity(var.heat_capacity),
        hcon=tdo_model.HeatConductivity(var.heat_conductivity),
    )
    return wat_phase


def get_oil_model(
    correlation_aggregator: ModelCorrelationAggregator,
    var: CorrelationVariable,
) -> Phase:
    vis = correlation_aggregator.oil.unsat.vis.calc(var)
    fvf = correlation_aggregator.oil.unsat.fvf.calc(var)
    pres = var.pres.value[0, :] / 10**5
    temp = var.temp.value[:, 0]
    dens_visc = var.density / fvf / vis

    oil_phase = Phase(
        density=var.density,
        visc=tdo_model.Viscosity(pres, temp, vis),
        fvf=tdo_model.VolumeFactor(pres, temp, fvf),
        dens=tdo_model.Denisty(),
        expected_dens=tdo_model.ExpectedDensity(pres, temp, var.density * fvf**-1),
        dens_visc=tdo_model.DensVisc(pres, temp, dens_visc),
        hcap=tdo_model.HeatCapacity(var.heat_capacity),
        hcon=tdo_model.HeatConductivity(var.heat_conductivity),
    )
    return oil_phase


def covert_correlation_to_table(correlation_aggregator: ModelCorrelationAggregator) -> PVTModel:
    var = CorrelationVariable.create()
    wat_phase_model = get_wat_model(correlation_aggregator, var)
    oil_phase_model = get_oil_model(correlation_aggregator, var)

    return wat_phase_model, oil_phase_model
