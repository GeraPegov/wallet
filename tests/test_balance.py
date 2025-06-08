import pytest

from app.repositories.wallet_manager import WalletManager
from tests.test_db_for_test import db_session


@pytest.mark.asyncio
async def test_balance(db_session):
    '''
    Проверка методов класса WalletManager в эндпоинте get
    '''
    test_manager = WalletManager(db_session)
    example_wallet = '123qwe123q'
    example_amount = 1000
    await test_manager.add_wallet(example_wallet)
    await test_manager.deposit(example_wallet, example_amount)
    test_show_balance = await test_manager.balance(example_wallet)
    assert test_show_balance == example_amount
    
