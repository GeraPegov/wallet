from fastapi import APIRouter, Depends, Form

from app.repositories import WalletManager
from app.services import CreateWalletHash
from app.dependencies.depends_wallet import get_wallet_hash, get_wallet_manager


router = APIRouter()

@router.get('/')
async def operation_wallet(
    wallet_id: CreateWalletHash = Depends(get_wallet_hash),
    create_wallet: WalletManager = Depends(get_wallet_manager),
    ) -> dict:
    '''Создание кошелька

    Args:
        wallet_id: Генерация айди кошелька через класс CreateWalletHash
        create_wallet: Создание кошелька через метод add_wallet класса WalletManager
    
    Returns:
        dict: Статус и ID кошелька
    '''
    generator_hash = wallet_id.hash()
    #Создание кошелька
    await create_wallet.add_wallet(wallet_id=generator_hash)
    return {
        'wallet_id': wallet_id,
        'status': 'success',
    }

@router.post('/wallet_id/operation')
async def transaction(
    operation_type: str,
    wallet_id: str = Form(...), 
    amount: int = Form(..., gt=0, lt=10**5, description='Число должно быть положительным'), 
    make_transaction: WalletManager = Depends(get_wallet_manager),
    ) -> dict:
    '''Транзакция(внесение(DEPOSIT) или снятие(WITHDRAW))
    
    Args:
        wallet_id: ID кошелька из шаблона HTML
        operation_type: Вид операции, передается через шаблон HTML
        amount: Сумма при транзакции
        make_transaction: Проведение транзакции через методы класса WalletManager

    Returns:
        dict: Статус код и баланс после транзакции
    '''
    if operation_type == 'DEPOSIT':
        result = await make_transaction.deposit(wallet_id, amount)
    elif operation_type == 'WITHDRAW':
        result = await make_transaction.withdraw(wallet_id, amount)
    return {
        'status': 'success',
        'balance': result
    }