from pydantic import BaseModel


class OilPhaseParams(BaseModel):
    vis: float
    fvf: float


class WatPhaseParams(BaseModel):
    vis: float
    fvf: float


class GasPhaseParams(BaseModel):
    visc: float
    dens: float


class PVTResponse(BaseModel):
    oil: OilPhaseParams
    wat: WatPhaseParams
    gas: GasPhaseParams