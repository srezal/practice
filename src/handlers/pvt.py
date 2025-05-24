import PVTCore.correlation as correlation
from PVTCore.aggregator import (
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
from PVTCore.correlation.abstract import CorrelationVariable
from schemas import pvt


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

async def calc_pvt_handler(correlation_variable: CorrelationVariable):
    return pvt.PVTResponse(
        wat=pvt.WatPhaseParams(
            vis=aggregator.wat.vis.calc(correlation_variable)[0],
            fvf=aggregator.wat.fvf.calc(correlation_variable)[0]
        ),
        oil=pvt.OilPhaseParams(
            vis=aggregator.oil.vis.calc(correlation_variable).get("Newton_second"),
            fvf=aggregator.oil.fvf.calc(correlation_variable).get("si")
        ),
        gas=pvt.GasPhaseParams(
            visc=aggregator.gas.visc.calc(correlation_variable)[0],
            dens=aggregator.gas.dens.calc(correlation_variable)[0]
        )
    )