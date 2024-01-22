from fastapi import APIRouter, HTTPException, Depends
from starlette.config import Config

config = Config('.env')

router = APIRouter(
    tags=["Main"],
    prefix="/router",
)

@router.get("/",)
async def create_board():
    return {"message": "router"}

