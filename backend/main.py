<<<<<<< HEAD
from fastapi import FastAPI

from backend.routes.health_check import health_check_router
from backend.routes.realtime import realtime_router

app = FastAPI()

# Registering routers
app.include_router(health_check_router)
app.include_router(realtime_router)
=======
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.config import create_db_and_tables
from backend.routes.chat import chat_router
from backend.routes.health_check import health_check_router
from backend.routes.personalisation import personalization_router
from backend.routes.tasks import task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # <-- Startup logic
    create_db_and_tables()
    yield
    # <-- Shutdown logic

app = FastAPI(lifespan=lifespan)

app.include_router(health_check_router)
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(personalization_router, prefix="/personalization", tags=["personalization"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])
>>>>>>> c075ada830a41bd00a68e916a21ed71f8f22da56
