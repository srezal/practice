from fastapi import FastAPI
from routers import pvt

app = FastAPI()

app.include_router(pvt.router)