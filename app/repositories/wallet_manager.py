from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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

    async def create_wallet(self, wallet_id: str):
        try:
            new_walletID = Wallet(wallet_id=wallet_id)
            self.session.add(new_walletID)
            await self.session.commit()
            await self.session.refresh(new_walletID)
            return 'Success'
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(500, 'databaase error')

    async def deposit(self, wallet_id: str, amount: int):
        try:
            id = (await self.session.execute(
                select(Wallet.id)
                .where(Wallet.wallet_id==wallet_id)
                )).scalar_one_or_none()
            wallet = await self.session.get(Wallet, id)
            wallet.total += amount
            await self.session.commit()
            return 'Success'
        except Exception as e:
            raise HTTPException(500)
        
    async def withdraw(self, wallet_id: str, amount: int):
        try:
            id = (await self.session.execute(
                select(Wallet.id)
                .where(Wallet.wallet_id==wallet_id)
                )).scalar_one_or_none()
            wallet = await self.session.get(Wallet, id)
            if amount > wallet.total:
                return 'Недостаточно средств'
            wallet.total -= amount
            await self.session.commit()
            return 'Success'
        except Exception as e:
            raise HTTPException(500)
        
    async def balance(self, wallet_id: str):
        try:
            balance = (await self.session.execute(
                select(Wallet.total)
                .where(Wallet.wallet_id==wallet_id)
            )).scalar_one_or_none()
            return balance
        except Exception as e:
            raise HTTPException(500)
