from fastapi import FastAPI

from backend.routes.chat import chat_router
from backend.routes.health_check import health_check_router

app = FastAPI()

# Registering routers
app.include_router(health_check_router)
app.include_router(chat_router, prefix="/chat", tags=["chat"])
