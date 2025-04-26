from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/")
async def root():
    return FileResponse("./public/chat.html")


@router.get("/chat")
async def chat_page():
    return FileResponse("./public/chat.html")


@router.get("/goals")
async def goals_page():
    return FileResponse("./public/goals.html")


@router.get("/retro")
async def retro_page():
    return FileResponse("./public/retro.html")


@router.get("/progress")
async def progress_page():
    return FileResponse("./public/progress.html")
