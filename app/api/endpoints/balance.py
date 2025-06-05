from fastapi import APIRouter, Depends, Query

from app.dependencies.depends_wallet import get_wallet_manager
from app.repositories import WalletManager

router = APIRouter()


@router.get('/wallet_id')
async def show_balance(
    wallet_id: str = Query(...),
    get_balance: WalletManager = Depends(get_wallet_manager)
) -> dict:
    '''Просмотр баланса

    Args:
        wallet_id: ID кошелька из шаблона HTML
        get_balance: Просмотр баланса через метод класса WalletManager

    Returns:
        dict: Баланс счета
    '''
    balance = await get_balance.balance(wallet_id)
    return {'balance': balance}
