from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.config import create_db_and_tables
from backend.routes.chat import chat_router
from backend.routes.health_check import health_check_router
from backend.routes.maintenance import maintenance_router
from backend.routes.personalisation import personalization_router
from backend.routes.staticFiles import router as StaticFiles_router
from backend.routes.tasks import task_router

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # <-- Startup logic
    create_db_and_tables()
    yield
    # <-- Shutdown logic


app = FastAPI(lifespan=lifespan)

static_files = StaticFiles(directory="./public")
app.mount("/public", static_files, name="public")
app.include_router(StaticFiles_router)
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(personalization_router, prefix="/personalization", tags=["personalization"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])
app.include_router(maintenance_router, prefix="/maintenance", tags=["maintenance"])
app.include_router(health_check_router)
