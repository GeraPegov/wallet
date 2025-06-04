from fastapi import APIRouter, Depends

from app.dependencies.depends_wallet import get_wallet_manager
from app.services import WalletManager

router = APIRouter()

@router.get('/wallet/{wallet_id}')
async def show_balance(
    wallet_id,
    get_balance: WalletManager = Depends(get_wallet_manager)
):
    result = await get_balance.balance(wallet_id)

    return result