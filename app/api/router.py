from fastapi import APIRouter
from app.api.endpoints.wallet import router as wallet_router
from app.api.endpoints.balance import router as balance_router

api_router = APIRouter()
api_router.include_router(
    wallet_router, 
    prefix='/wallet',
    tags=['Wallet']
    )
api_router.include_router(
    balance_router, 
    prefix='/balance',
    tags=['Balance']
    )