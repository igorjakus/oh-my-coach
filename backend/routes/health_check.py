from fastapi import APIRouter
from fastapi.responses import JSONResponse

health_check_router = APIRouter()


@health_check_router.get("/")
async def health_check():
<<<<<<< HEAD
    return JSONResponse(content={"status": "Iam Alive!"}, status_code=200)
=======
    return JSONResponse(content={"status": "I'm Alive!"}, status_code=200)
>>>>>>> c075ada830a41bd00a68e916a21ed71f8f22da56
