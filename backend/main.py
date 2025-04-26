from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.config import create_db_and_tables
from backend.routes.chat import chat_router
from backend.routes.health_check import health_check_router
from backend.routes.tasks import task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # <-- Startup logic
    create_db_and_tables()
    yield
    # <-- Shutdown logic

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="../frontend/public"), name="static")

app.include_router(health_check_router)
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])
app.include_router(staticFiles_router, prefix="/")