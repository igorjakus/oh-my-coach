from fastapi import FastAPI
from backend.routes.health_check import health_check_router
from backend.routes.realtime import realtime_router

app = FastAPI()

# Registering routers
app.include_router(health_check_router)
app.include_router(realtime_router)
