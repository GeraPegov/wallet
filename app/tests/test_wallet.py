import pytest
from sqlalchemy import select

from app.core.models.wallet import Wallet
from app.repositories.wallet_manager import WalletManager
from app.services.get_wallet_id import CreateWalletHash


def test_createhash():
    '''
    Проверка получения хэша CreateWallethash
    '''
    test_class = CreateWalletHash()
    test_example = test_class.hash()

    assert len(test_example) == 10
    assert test_example.isalnum()


@pytest.mark.asyncio
async def test_add_wallet(db_session):
    '''
    Проверка создания кошелька
    '''
    wallet_manager = WalletManager(db_session)
    example_wallet_id = '123qwe456q'
    await wallet_manager.add_wallet(example_wallet_id)

    # Проверяем, что данные добавились
    result = await db_session.execute(select(Wallet))
    assert result.scalars().first().wallet_id == example_wallet_id

@pytest.mark.asyncio
async def test_deposit_and_withdraw(db_session):
    '''
    Проверка методов класса WalletManager в эндпоинте post
    '''
    wallet_manager = WalletManager(db_session)
    example_wallet = '123qwe456q'
    await wallet_manager.add_wallet(example_wallet)
    example_amount_deposit = 2000
    example_amount_withdraw = 1000
    # Проверка метода deposit
    example_deposit = await wallet_manager.deposit(
        wallet_id=example_wallet,
        amount=example_amount_deposit)
    # Проверка метода withdraw
    example_withdraw = await wallet_manager.withdraw(
        wallet_id=example_wallet,
        amount=example_amount_withdraw
    )
    assert example_deposit == example_amount_deposit
    assert example_withdraw == example_amount_deposit-example_amount_withdraw
