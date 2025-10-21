from fastapi import HTTPException
from sqlalchemy import select, update
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


class WalletManager:
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
            raise HTTPException(500, f"Ошибка базы данных: {str(e)}")

    async def transaction(self, wallet_id: str, amount: int, operation_type):
        try:
            """
            Изменения в БД идут в один запрос.
            Поиск записи идёт по номеру кошелька "wallet_id" 
            Новое значение через "amount"
            Конкретная операция через "operation_type"
            """
            if operation_type == "DEPOSIT":
                total = await self.session.execute(
                    update(Wallet)
                    .where(Wallet.wallet_id == wallet_id)
                    .values(total=Wallet.total + amount)
                    .returning(Wallet.total)
                )
                new_total = total.scalar_one_or_none()
                if not new_total:
                    raise HTTPException(404, f"Кошелек {wallet_id} не найден")
                await self.session.commit()
                return new_total

            elif operation_type == "WITHDRAW":
                total = await self.session.execute(
                    update(Wallet)
                    .where(Wallet.wallet_id == wallet_id)
                    .values(total=Wallet.total - amount)
                    .returning(Wallet.total)
                )
                new_total = total.scalar_one_or_none()
                if not new_total:
                    raise HTTPException(404, f"Кошелек {wallet_id} не найден")
                await self.session.commit()
                return new_total
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise HTTPException(500, f"Ошибка базы данных: {str(e)}")

    async def balance(self, wallet_id: str):
        try:
            balance = (
                await self.session.execute(
                    select(Wallet.total).where(Wallet.wallet_id == wallet_id)
                )
            ).scalar_one_or_none()
            return balance
        except SQLAlchemyError as e:
            raise HTTPException(500, f"Ошибка базы данных: {str(e)}")
