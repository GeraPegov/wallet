from fastapi import APIRouter, Depends, Form

from app.repositories import WalletManager
from app.services import CreateWalletHash
from app.dependencies.depends_wallet import get_hash, get_wallet_manager


router = APIRouter()

@router.get('/')
async def operation_wallet(
    wallet_id: CreateWalletHash = Depends(get_hash),
    create_wallet_id: WalletManager = Depends(get_wallet_manager),
    ) -> dict:
    wallet_id = wallet_id.hash()
    #Создание кошелька
    await create_wallet_id.create_wallet(wallet_id=wallet_id)
    return {
        'wallet_id': wallet_id,
        'status': 'success',
    }

@router.post('/wallet_id/operation')
async def transaction(
    operation_type: str,
    wallet_id: str = Form(...), 
    amount: int = Form(..., gt=0, lt=10**5, description='Число должно быть положительным'), 
    transaction: WalletManager = Depends(get_wallet_manager),
    ) -> dict:
    if operation_type == 'DEPOSIT':
        result = await transaction.deposit(wallet_id, amount)
    elif operation_type == 'WITHDRAW':
        result = await transaction.withdraw(wallet_id, amount)
    return {
        'status': 'success',
        'balance': result
    }