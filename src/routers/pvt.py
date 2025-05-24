from fastapi import APIRouter
from PVTCore.correlation.abstract.variable import CorrelationVariable
from handlers import pvt

router = APIRouter(prefix="/pvt")

@router.post("/calc")
async def calc_pvt(request: CorrelationVariable):
    response = await pvt.calc_pvt_handler(request)
    return response