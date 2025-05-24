from fastapi import APIRouter
from PVTCore.correlation.abstract.variable import CorrelationVariable
from handlers import pvt
from schemas.pvt import PVTResponse

router = APIRouter(prefix="/pvt")

@router.post("/calc")
async def calc_pvt(request: CorrelationVariable) -> PVTResponse:
    response = await pvt.calc_pvt_handler(request)
    return response