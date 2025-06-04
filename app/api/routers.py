from fastapi import APIRouter

from app.api.routers import balance, wallet

api_router = APIRouter()
api_router.include_router(wallet.router, tags=['wallet'])