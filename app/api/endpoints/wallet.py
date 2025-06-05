from fastapi import APIRouter, Depends, Form

from app.dependencies.depends_wallet import get_wallet_hash, get_wallet_manager
from app.repositories import WalletManager
from app.services import CreateWalletHash

router = APIRouter()


@router.get('/')
async def create_new_wallet(
        wallet_hash: CreateWalletHash = Depends(get_wallet_hash),
        create_wallet: WalletManager = Depends(get_wallet_manager)
        ) -> dict:
    """
    Создание нового кошелька.

    Генерирует уникальный идентификатор кошелька с помощью `CreateWalletHash`,
    а затем добавляет новый кошелёк в базу данных через `WalletManager`.

    Args:
        wallet_hash (CreateWalletHash): Сервис для генерации хэша кошелька.
        create_wallet (WalletManager): Менеджер для работы с кошельками.

    Returns:
        dict: Статус операции и ID созданных кошельков.

    Raises:
        HTTPException: Если произошла ошибка при добавлении в базу данных.
    """
    generator_hash = wallet_hash.hash()
    # Создание кошелька
    await create_wallet.add_wallet(wallet_id=generator_hash)
    return {
        'wallet_id': generator_hash,
        'status': 'success',
    }


@router.post('/wallet_id/operation')
async def transaction(
        type_of_operation: str,
        wallet_id: str = Form(...),
        amount: int = Form(
            ...,
            gt=0,
            lt=10**5,
            description='Число должно быть положительным'),
        make_transaction: WalletManager = Depends(get_wallet_manager)
        ) -> dict:
    """
    Выполнение транзакции (внесение или снятие средств).

    Обрабатывает операции вида `DEPOSIT` и `WITHDRAW`,
    используя данные из формы,
    а также проверяет корректность суммы транзакции.

    Args:
        type_of_operation (str): Тип операции: 'DEPOSIT' или 'WITHDRAW'.
        wallet_id (str): Уникальный ID кошелька.
        amount (int): Сумма транзакции. Положительная и меньше 100,000.
        make_transaction (WalletManager): Менеджер для работы с кошельками.

    Returns:
        dict: Статус операции и текущий баланс кошелька после транзакции.

    Raises:
        HTTPException: Если тип операции неверный или произошла ошибка.
    """
    if type_of_operation == 'DEPOSIT':
        result = await make_transaction.deposit(wallet_id, amount)
    elif type_of_operation == 'WITHDRAW':
        result = await make_transaction.withdraw(wallet_id, amount)
    return {
        'status': 'success',
        'balance': result}
