from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

router = APIRouter()

@router.get("/")
async def root():
    return FileResponse("../public/chat.html")

@router.get("/chat.html")
async def chat_page():
    return FileResponse("../public/chat.html")

@router.get("/goals.html")
async def goals_page():
    return FileResponse("../public/goals.html")

@router.get("/retro.html")
async def retro_page():
    return FileResponse("../public/retro.html")

@router.get("/progress.html")
async def progress_page():
    return FileResponse("../public/progress.html")
