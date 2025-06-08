from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.models import Wallet


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


class WalletManager():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_wallet(self, wallet_id: str):
        try:
            new_walletID = Wallet(wallet_id=wallet_id)
            self.session.add(new_walletID)
            await self.session.commit()
            await self.session.refresh(new_walletID)
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(500, f'Ошибка базы данных: {str(e)}')

    async def deposit(self, wallet_id: str, amount: int) -> int:
        try:
            id = (await self.session.execute(
                select(Wallet.id)
                .where(Wallet.wallet_id == wallet_id)
                )).scalar_one_or_none()
            if not id:
                raise HTTPException(404, f'Кошелек {wallet_id} не найден')
            # Поиск кошелька по id записи
            wallet = await self.session.get(Wallet, id)
            wallet.total += amount
            result_total = wallet.total
            await self.session.commit()

            return result_total
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise HTTPException(500, f'Ошибка базы данных: {str(e)}')

    async def withdraw(self, wallet_id: str, amount: int) -> int:
        try:
            id = (await self.session.execute(
                select(Wallet.id)
                .where(Wallet.wallet_id == wallet_id)
                )).scalar_one_or_none()
            if not id:
                raise HTTPException(404, f'Кошелек {wallet_id} не найден')
            # Поиск кошелька по id записи
            wallet = await self.session.get(Wallet, id)
            # Ошибка при недостатке средств
            if amount > wallet.total:
                return HTTPException(400, 'Недостаточно средств')       
            wallet.total -= amount
            total_result = wallet.total
            await self.session.commit()
            return total_result
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise HTTPException(500, f'Ошибка базы данных: {str(e)}')

    async def balance(self, wallet_id: str):
        try:
            balance = (await self.session.execute(
                select(Wallet.total)
                .where(Wallet.wallet_id==wallet_id)
            )).scalar_one_or_none()
            return balance
        except SQLAlchemyError as e:
            raise HTTPException(500, f'Ошибка базы данных: {str(e)}')
