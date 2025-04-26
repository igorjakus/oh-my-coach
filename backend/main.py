from fastapi import FastAPI

from backend.config import create_db_and_tables
from backend.routes.chat import chat_router
from backend.routes.health_check import health_check_router
from backend.routes.tasks import task_router

app = FastAPI()

# Initialize database tables
@app.lifespan("startup")
async def on_startup():
    create_db_and_tables()

# Registering routers
app.include_router(health_check_router)
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])
