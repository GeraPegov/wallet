# import pytest
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.core.models.wallet import Wallet
# from app.repositories.wallet_manager import WalletManager
from app.services.get_wallet_id import CreateWalletHash

# from tests.test_db_for_test import async_db_session


def test_createhash():
    test_class = CreateWalletHash()
    test_example = test_class.hash()

    assert len(test_example) == 10
    assert test_example.isalnum()

# @pytest.mark.asyncio
# async def test_add_wallet(async_db_session: AsyncSession):
#     test_class = WalletManager(async_db_session)
#     example_wallet_id = '123qwe456q'
#     await test_class.add_wallet(example_wallet_id)

#     test_sample = await async_db_session.execute(
#         select(Wallet.wallet_id)
#         .where(Wallet.wallet_id == example_wallet_id)
#     )
#     result = test_sample.scalar_one_or_none()

#     assert result == '123qwe456q'
