from fastapi import APIRouter

from app.api.endpoints.balance import router as balance_router
from app.api.endpoints.home import router as home_router
from app.api.endpoints.wallet import router as wallet_router

api_router = APIRouter()

api_router.include_router(
    wallet_router,
    prefix='/api/v1',
    tags=['Wallet']
    )

api_router.include_router(
    balance_router,
    prefix='/api/v1',
    tags=['Balance']
    )

api_router.include_router(
    home_router,
    tags=['Home']
    )
