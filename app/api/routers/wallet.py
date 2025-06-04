from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import CreateWalletHash, WalletManager
from app.dependencies.depends_wallet import get_hash, get_wallet_manager


router = APIRouter()

@router.get('/wallets')
async def operation_wallet(
    wallet_id: CreateWalletHash = Depends(get_hash),
    create_wallet_id: WalletManager = Depends(get_wallet_manager),
    ):
    wallet_id = wallet_id.hash()
    #Создание кошелька
    result = await create_wallet_id.create_wallet(wallet_id=wallet_id)
    return wallet_id, result

@router.post('/wallet/{wallet_id}/operation')
async def transaction(
    operation: str,
    wallet_id: str, 
    amount: int, 
    transaction: WalletManager = Depends(get_wallet_manager),
    ):
    if operation == 'DEPOSIT':
        result = await transaction.deposit(wallet_id, amount)
    elif operation == 'WITHDRAW':
        result = await transaction.withdraw(wallet_id, amount)

    return result