from fastapi import APIRouter, Depends, Form

from app.dependencies.depends_wallet import get_wallet_hash, get_wallet_manager
from app.repositories import WalletManager
from app.services import CreateWalletHash

router = APIRouter()


@router.get('/wallets')
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
    await create_wallet.add_wallet(wallet_id=generator_hash)
    return {
        'wallet_id': generator_hash,
        'status': 'success'
    }


@router.post('/wallets/wallet_id/operation')
async def transaction(
        operation_type: str,
        wallet_id: str = Form(...),
        amount: int = Form(
            ...,
            gt=0,
            lt=10**5,
            description='Число должно быть положительным'),
        manager: WalletManager = Depends(get_wallet_manager)
        ) -> dict:
    """
    Выполнение транзакции (внесение или снятие средств).

    Обрабатывает операции вида `DEPOSIT` и `WITHDRAW`,
    используя данные из формы,
    а также проверяет корректность суммы транзакции.

    Args:
        operation_type (str): Тип операции: 'DEPOSIT' или 'WITHDRAW'.
        wallet_id (str): Уникальный ID кошелька.
        amount (int): Сумма транзакции. Положительная и меньше 100,000.
        access_to_repositories (WalletManager): Менеджер для работы с кошельками.

    Returns:
        dict: Статус операции и текущий баланс кошелька после транзакции.

    Raises:
        HTTPException: Если тип операции неверный или произошла ошибка.
    """
    result = await manager.transaction(wallet_id, amount, operation_type)
    return {
        'status': 'success',
        'balance': result
    }
